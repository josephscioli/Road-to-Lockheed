import requests
import json
import os
from bs4 import BeautifulSoup

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
SEEN_FILE = "seen_jobs.json"

SEARCH_URL = "https://www.lockheedmartinjobs.com/search-jobs/results?ActiveFacetID=4+yr+and+up+College&CurrentPage=1&RecordsPerPage=15&TotalContentResults=&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=Full-Time+Remote&FacetFilters%5B0%5D.FacetType=5&FacetFilters%5B0%5D.Count=79&FacetFilters%5B0%5D.Display=Full-Time+Remote&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=custom_fields.AbilitytoWorkRemotely&FacetFilters%5B1%5D.ID=4+yr+and+up+College&FacetFilters%5B1%5D.FacetType=5&FacetFilters%5B1%5D.Count=3&FacetFilters%5B1%5D.Display=4+yr+and+up+College&FacetFilters%5B1%5D.IsApplied=true&FacetFilters%5B1%5D.FieldName=job_status&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=6&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=&TotalContentPages=NaN"

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def get_jobs():
    response = requests.get(SEARCH_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for job_card in soup.find_all("li"):
        link = job_card.find("a", href=True)
        if not link:
            continue

        title = link.text.strip()
        url = "https://www.lockheedmartinjobs.com" + link["href"]
        job_id = link["href"]

        jobs.append({
            "id": job_id,
            "title": title,
            "url": url
        })

    return jobs

def send_to_discord(job):
    payload = {
        "content": f"🛰️ **New Lockheed Remote Job!**\n{job['title']}\n{job['url']}"
    }

    requests.post(WEBHOOK_URL, json=payload)

def main():
    seen = load_seen()
    jobs = get_jobs()

    for job in jobs:
        if job["id"] not in seen:
            send_to_discord(job)
            seen.add(job["id"])

    save_seen(seen)

if __name__ == "__main__":
    main()
