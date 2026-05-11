import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_rss(url, n=5, source_name="RSS Source"):
    """Fetch headlines from an RSS feed with safe error handling."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        headlines = []
        for item in items[:n]:
            title = item.find("title").text if item.find("title") is not None else "No title"
            link = item.find("link").text if item.find("link") is not None else "No link"
            date = item.find("pubDate").text if item.find("pubDate") is not None else "No date"

            headlines.append({
                "title": title,
                "url": link,
                "date": date,
                "source": source_name
            })

        return headlines

    except Exception as e:
        print(f"[ERROR] Could not fetch from {source_name}: {e}")
        return []


def fetch_cisa_kev(n=5):
    """Fetch latest Known Exploited Vulnerabilities from CISA."""
    try:
        url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
        data = requests.get(url, timeout=10).json()

        vulns = data.get("vulnerabilities", [])[:n]

        results = []
        for v in vulns:
            results.append({
                "title": v.get("cveID", "Unknown CVE"),
                "summary": v.get("shortDescription", "No description available"),
                "source": "CISA KEV"
            })
        return results

    except Exception as e:
        print(f"[ERROR] Could not fetch CISA KEV: {e}")
        return []


if __name__ == "__main__":
    print("\n=== Tech & Cyber News ===")
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # sources :
    sources = [
        ("https://feeds.feedburner.com/TheHackersNews", "The Hacker News"),
        ("https://krebsonsecurity.com/feed/", "Krebs on Security"),
        ("https://www.darkreading.com/rss.xml", "Dark Reading"),
        ("https://www.cisa.gov/cybersecurity-advisories/all.xml", "CISA Alerts")
    ]

    for url, name in sources:
        print(f"{name} – Latest Headlines:")
        print("--------------------------------")
        for h in fetch_rss(url, 5, name):
            print(f"- {h['title']}")
            print(f"  {h['url']}\n")

    print("Latest Known Exploited Vulnerabilities (CISA KEV):")
    print("--------------------------------------------------")
    for v in fetch_cisa_kev(5):
        print(f"- {v['title']}")
        print(f"  {v['summary']}\n")
