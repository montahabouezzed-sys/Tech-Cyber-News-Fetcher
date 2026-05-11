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
