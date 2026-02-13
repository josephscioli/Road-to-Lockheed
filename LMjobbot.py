def get_jobs():
    response = requests.get(SEARCH_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for job_card in soup.find_all("li"):
        link = job_card.find("a", href=True)
        if not link:
            continue

        # Clean up title - remove all whitespace and newline characters
        title = " ".join(link.text.split())  # This removes all \r\n and extra spaces
        url = link["href"].strip('"')  # Remove extra quotes
        
        if not url.startswith("http"):
            url = "https://www.lockheedmartinjobs.com" + url
        
        job_id = url

        jobs.append({
            "id": job_id,
            "title": title,
            "url": url
        })

    return jobs

def send_to_discord(job):
    payload = {
        "content": f"🛰️ **New Lockheed Remote Job!**\n**{job['title']}**\n{job['url']}"
    }

    requests.post(WEBHOOK_URL, json=payload)
