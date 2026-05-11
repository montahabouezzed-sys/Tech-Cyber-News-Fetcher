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


def fetch_latest_cves(n=5):
    """Fetch latest CVE vulnerabilities."""
    try:
        data = requests.get("https://cve.circl.lu/api/last", timeout=10).json()
        return [{
            "title": item.get("id", "Unknown CVE"),
            "summary": item.get("summary", "No summary available"),
            "source": "CVE Feed"
        } for item in data[:n]]
    except Exception as e:
        print(f"[ERROR] Could not fetch CVEs: {e}")
        return []


if __name__ == "__main__":
    print("\n=== Tech & Cyber News ===")
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # Cybersecurity RSS sources
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

    print("Latest Cybersecurity Alerts (CVE):")
    print("----------------------------------")
    for c in fetch_latest_cves(5):
        print(f"- {c['title']}")
        print(f"  {c['summary']}\n")
