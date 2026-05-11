import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# ------------------------------------------------------------
# Generic RSS fetcher
# ------------------------------------------------------------

def fetch_rss(url, n=5, source_name="RSS Source"):
    """Fetch headlines from an RSS feed."""
    response = requests.get(url)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = root.findall(".//item")

    headlines = []
    for item in items[:n]:
        title = item.find("title").text
        link = item.find("link").text
        pub_date = item.find("pubDate").text if item.find("pubDate") is not None else "No date"

        headlines.append({
            "title": title,
            "url": link,
            "date": pub_date,
            "source": source_name
        })

    return headlines


# ------------------------------------------------------------
# Hacker News (Tech)
# ------------------------------------------------------------

def fetch_hackernews_top(n=5):
    ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
    headlines = []

    for story_id in ids[:n]:
        data = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json").json()
        if data and "title" in data:
            headlines.append({
                "title": data["title"],
                "url": data.get("url", "No link available"),
                "source": "Hacker News"
            })
    return headlines


# ------------------------------------------------------------
# CVE Feed (Cybersecurity)
# ------------------------------------------------------------

def fetch_latest_cves(n=5):
    data = requests.get("https://cve.circl.lu/api/last").json()
    cves = []

    for item in data[:n]:
        cves.append({
            "title": item.get("id", "Unknown CVE"),
            "summary": item.get("summary", "No summary available"),
            "source": "CVE Feed"
        })
    return cves


# ------------------------------------------------------------
# Main script
# ------------------------------------------------------------

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

    # Hacker News (Tech)
    print("Top Tech Headlines (Hacker News):")
    print("--------------------------------")
    for h in fetch_hackernews_top(5):
        print(f"- {h['title']}")
        print(f"  {h['url']}\n")

    # CVE
    print("Latest Cybersecurity Alerts (CVE):")
    print("----------------------------------")
    for c in fetch_latest_cves(5):
        print(f"- {c['title']}")
        print(f"  {c['summary']}\n")
import requests
from datetime import datetime

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def fetch_hackernews_top(n=10):
    """Fetch top tech headlines from Hacker News."""
    ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
    headlines = []

    for story_id in ids[:n]:
        url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        data = requests.get(url).json()
        if data and "title" in data:
            headlines.append({
                "title": data["title"],
                "url": data.get("url", "No link available"),
                "source": "Hacker News"
            })
    return headlines


def fetch_latest_cves(n=10):
    """Fetch latest cybersecurity vulnerabilities (CVE feed)."""
    url = "https://cve.circl.lu/api/last"
    data = requests.get(url).json()

    cves = []
    for item in data[:n]:
        cves.append({
            "title": item.get("id", "Unknown CVE"),
            "summary": item.get("summary", "No summary available"),
            "source": "CVE Feed"
        })
    return cves


# ------------------------------------------------------------
# Main script
# ------------------------------------------------------------

if __name__ == "__main__":
    print("\n=== Tech & Cyber News ===")
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    print("Top Tech Headlines (Hacker News):")
    print("--------------------------------")
    for h in fetch_hackernews_top(5):
        print(f"- {h['title']}")
        print(f"  {h['url']}\n")

    print("\nLatest Cybersecurity Alerts (CVE):")
    print("----------------------------------")
    for c in fetch_latest_cves(5):
        print(f"- {c['title']}")
        print(f"  {c['summary']}\n")
