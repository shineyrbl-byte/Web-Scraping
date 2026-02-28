# remoteok_full_pipeline.py
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- SETTINGS ----------
BASE_URL = "https://remoteok.com/remote-jobs"
HEADERS = {"User-Agent": "Mozilla/5.0"}
PAGES_TO_SCRAPE = 5  # adjust as needed
CSV_FILE = "remoteok_jobs_full.csv"

all_jobs = []

# ---------- SCRAPING ----------
for page in range(1, PAGES_TO_SCRAPE + 1):
    print(f"Scraping page {page}...")
    url = f"{BASE_URL}?page={page}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.find_all("tr", attrs={"data-offset": True})
        for row in rows:
            job = {}

            # Title
            td_tag = row.find("td", class_="company position company_and_position")
            h2_tag = td_tag.find("h2") if td_tag else None
            job_title = h2_tag.text.strip() if h2_tag else "N/A"

            # Company
            company = row.get("data-company", "N/A")

            # Location
            loc_div = td_tag.find("div", class_="location") if td_tag else None
            location = loc_div.text.strip() if loc_div else "Not Specified"

            # Skills
            skills_td = row.find("td", class_="tags")
            skills_list = []
            if skills_td:
                a_tags = skills_td.find_all("a", class_="no-border tooltip-set action-add-tag")
                for a in a_tags:
                    h3 = a.find("h3")
                    if h3:
                        skills_list.append(h3.text.strip())
            skills = ", ".join(skills_list) if skills_list else "N/A"

            # Employment type from JSON-LD
            emp_type = "Not Specified"
            img_td = row.find("td", class_="image has-logo")
            if img_td:
                script_tag = img_td.find("script", type="application/ld+json")
                if script_tag:
                    try:
                        data_json = json.loads(script_tag.string)
                        emp_type = data_json.get("employmentType", "Not Specified")
                    except:
                        pass

            # Job URL
            job_url = td_tag.find("a", itemprop="url").get("href") if td_tag and td_tag.find("a", itemprop="url") else "N/A"
            if job_url != "N/A" and not job_url.startswith("http"):
                job_url = "https://remoteok.com" + job_url

            # Add to dict
            job["title"] = job_title
            job["company"] = company
            job["location"] = location
            job["skills"] = skills
            job["employment_type"] = emp_type
            job["url"] = job_url

            all_jobs.append(job)

        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Error on page {page}: {e}")
        continue

print(f"Scraped {len(all_jobs)} jobs.")

# ---------- SAVE CSV ----------
df = pd.DataFrame(all_jobs)
# Remove duplicates
df = df.drop_duplicates(subset=["title", "company", "url"])
# Clean text
df['title'] = df['title'].str.strip().str.lower()
df['company'] = df['company'].str.strip().str.lower()
df['location'] = df['location'].str.strip()
df['skills'] = df['skills'].str.strip()
df['employment_type'] = df['employment_type'].str.strip()
df.to_csv(CSV_FILE, index=False)
print(f"Saved CSV: {CSV_FILE}")

import pandas as pd

# Load CSV
df = pd.read_csv("remoteok_jobs_full.csv")

print(f"Total jobs loaded: {len(df)}\n")

# Top 10 skills
df_skills = df.copy()
df_skills['skills'] = df_skills['skills'].str.split(', ')
df_skills = df_skills.explode('skills')
df_skills = df_skills[df_skills['skills'].str.strip() != '']
print("Top 10 Skills:")
print(df_skills['skills'].value_counts().head(10))

# Job type distribution
print("\nJob Type Distribution:")
print(df['employment_type'].value_counts())

# Top 10 locations
print("\nTop 10 Locations:")
print(df['location'].value_counts().head(10))

# Top 10 companies
print("\nTop 10 Companies:")
print(df['company'].value_counts().head(10))

# Average number of skills per job
df['num_skills'] = df['skills'].apply(lambda x: len(str(x).split(', ')) if x else 0)
print(f"\nAverage skills per job: {df['num_skills'].mean():.2f}")