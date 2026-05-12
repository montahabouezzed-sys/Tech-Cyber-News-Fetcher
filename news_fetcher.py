import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime
from colorama import Fore, Style, init

import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

init(autoreset=True)

# ------------------------------------------------------------
# RSS FETCHER
# ------------------------------------------------------------

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
        print(Fore.RED + f"[ERROR] Could not fetch from {source_name}: {e}")
        return []


# ------------------------------------------------------------
# CISA KEV (VULNERABILITIES)
# ------------------------------------------------------------

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
        print(Fore.RED + f"[ERROR] Could not fetch CISA KEV: {e}")
        return []


# ------------------------------------------------------------
# EXPORT FUNCTIONS
# ------------------------------------------------------------

def save_to_html(results, filename="news.html"):
    html = "<h1>Tech & Cyber News</h1>\n<ul>"
    for item in results:
        title = item.get("title", "No title")
        source = item.get("source", "Unknown source")
        url = item.get("url")  # may be None
        summary = item.get("summary")

        html += f"<li><b>{title}</b> — {source}<br>"

        if url:
            html += f"<a href='{url}'>{url}</a><br>"
        if summary:
            html += f"{summary}<br>"

        html += "</li><br>"

    html += "</ul>"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(Fore.GREEN + f"Saved HTML to {filename}")



def save_to_markdown(results, filename="news.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Tech & Cyber News\n\n")
        for item in results:
            title = item.get("title", "No title")
            source = item.get("source", "Unknown source")
            url = item.get("url")
            summary = item.get("summary")

            f.write(f"### {title}\n")
            f.write(f"- **Source:** {source}\n")
            if url:
                f.write(f"- **Link:** {url}\n")
            if summary:
                f.write(f"- **Summary:** {summary}\n")
            f.write("\n")

    print(Fore.GREEN + f"Saved Markdown to {filename}")


def save_to_json(results, filename="news.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(Fore.GREEN + f"Saved JSON to {filename}")


# ------------------------------------------------------------
# CLI MENU
# ------------------------------------------------------------

def menu():
    print(Fore.CYAN + "\n=== Tech & Cyber News CLI ===")
    print("1. Cybersecurity News (RSS)")
    print("2. Tech News (Hacker News)")
    print("3. Vulnerabilities (CISA KEV)")
    print("4. Export ALL to HTML")
    print("5. Export ALL to Markdown")
    print("6. Export ALL to JSON")
    print("7. Exit")
    return input(Fore.YELLOW + "Choose an option: ")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    sources = [
        ("https://feeds.feedburner.com/TheHackersNews", "The Hacker News"),
        ("https://krebsonsecurity.com/feed/", "Krebs on Security"),
        ("https://www.darkreading.com/rss.xml", "Dark Reading"),
        ("https://www.cisa.gov/cybersecurity-advisories/all.xml", "CISA Alerts")
    ]

    all_results = []

    while True:
        choice = menu()

        if choice == "1":
            print(Fore.MAGENTA + "\n--- Cybersecurity News ---")
            for url, name in sources:
                print(Fore.CYAN + f"\n{name}:")
                results = fetch_rss(url, 5, name)
                all_results.extend(results)
                for item in results:
                    print(Fore.GREEN + f"- {item['title']}")
                    print(Fore.YELLOW + f"  {item['url']}")

        elif choice == "2":
            print(Fore.MAGENTA + "\n--- Tech News (Hacker News) ---")
            hn = fetch_rss("https://feeds.feedburner.com/TheHackersNews", 5, "Hacker News")
            all_results.extend(hn)
            for item in hn:
                print(Fore.GREEN + f"- {item['title']}")
                print(Fore.YELLOW + f"  {item['url']}")

        elif choice == "3":
            print(Fore.MAGENTA + "\n--- Vulnerabilities (CISA KEV) ---")
            kev = fetch_cisa_kev(5)
            all_results.extend(kev)
            for item in kev:
                print(Fore.RED + f"- {item['title']}")
                print(Fore.YELLOW + f"  {item['summary']}")

        elif choice == "4":
            save_to_html(all_results)
            input(Fore.CYAN + "Export successful. Press Enter to return to menu.")
            clear()

        elif choice == "5":
            save_to_markdown(all_results)
            input(Fore.CYAN + "Export successful. Press Enter to return to menu.")
            clear()

        elif choice == "6":
            save_to_json(all_results)
            input(Fore.CYAN + "Export successful. Press Enter to return to menu.")
            clear()

        elif choice == "7":
            print(Fore.CYAN + "Goodbye!")
            break

        else:
            print(Fore.RED + "Invalid choice")


if __name__ == "__main__":
    main()
