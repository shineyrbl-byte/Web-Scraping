import requests
from bs4 import BeautifulSoup
import time
import json
headers = {"User-Agent": "Mozilla/5.0"}

all_jobs = []

base_url = "https://remoteok.com/remote-jobs"

for page in range(1, 6):

    print(f"Scraping page {page}...")

    # Page URL logic
    if page == 1:
        url = base_url
    else:
        url = f"{base_url}/{page}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.find_all("tr", attrs={"data-offset": True})

        for row in rows:
            company = row.get("data-company", "Not Specified")
            job_url = row.get("data-href", "Not Available")
            loc_tag = row.find("div", class_="location")
            if loc_tag:
                location_text = loc_tag.text.strip()
                if "🌏" in location_text or "worldwide" in location_text.lower():
                    location = "Worldwide"
                else:
                    location = location_text
            else:
                location = "Not Specified"


            skills = []
            tag_section = row.find("td", class_="tags")
            if tag_section:
                skill_links = tag_section.find_all("a", class_="no-border tooltip-set action-add-tag")
                for link in skill_links:
                    div = link.find("div")
                    if div:
                        h3 = div.find("h3")
                        if h3:
                            skills.append(h3.text.strip())

            # Employment Type from JSON-LD
            emp_type = "Not Specified"
            script_tag = row.find("td", class_="image has-logo")
            if script_tag:
                json_ld = script_tag.find("script", type="application/ld+json")
                if json_ld:
                    try:
                        data = json.loads(json_ld.string)
                        emp_type = data.get("employmentType", "Not Specified")
                    except json.JSONDecodeError:
                        emp_type = "Not Specified"

            job_data = {
        "company": company,
        "location": location,
        "skills": skills,
        "employment_type": emp_type,
        "url": job_url
    }

            all_jobs.append(job_data)

        # Respect crawl delay
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Error on page {page}: {e}")
        continue

print(f"\nTotal jobs scraped: {len(all_jobs)}")