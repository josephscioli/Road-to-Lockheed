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

        # Optional: grab posting date or description if available
        date_elem = job_card.find("time")  # if there's a <time> tag
        date_posted = date_elem.text.strip() if date_elem else "Date N/A"

        desc_elem = job_card.find("p")  # if there's a short description paragraph
        description = desc_elem.text.strip() if desc_elem else ""

        jobs.append({
            "id": job_id,
            "title": title,
            "url": url,
            "date": date_posted,
            "description": description
        })

    return jobs

def send_to_discord(job):
    payload = {
        "embeds": [
            {
                "title": job['title'],
                "url": job['url'],
                "description": job['description'] or "🛰️ Remote, Full-Time, 4+ years college",
                "color": 0x1E90FF,
                "fields": [
                    {
                        "name": "Date Posted",
                        "value": job['date'],
                        "inline": True
                    },
                    {
                        "name": "Link",
                        "value": f"[Apply Here]({job['url']})",
                        "inline": True
                    }
                ]
            }
        ]
    }
    requests.post(WEBHOOK_URL, json=payload)
