import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

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

            job_data = {
        "company": company,
        "location": location,
        "skills": skills,
        "url": job_url
    }

            all_jobs.append(job_data)

        # Respect crawl delay
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Error on page {page}: {e}")
        continue

# ---------- Convert list of dictionaries to DataFrame ----------
df = pd.DataFrame(all_jobs)

# ---------- Display basic info ----------
print(f"Total rows scraped: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nMissing values per column:\n{df.isnull().sum()}")

# ---------- Handle missing values ----------
# Replace empty strings or None with 'N/A'
df.fillna('N/A', inplace=True)

# Remove rows where critical fields are missing
df = df[(df['company'] != 'N/A') & (df['location'] != 'N/A') & (df['url'] != 'Not Available')]

# ---------- Remove duplicates ----------
# Based on company + location + url
df = df.drop_duplicates(subset=['company', 'location', 'url'])

# ---------- Clean text ----------
# Lowercase and strip whitespace
df['company'] = df['company'].str.lower().str.strip()
df['location'] = df['location'].str.lower().str.strip()

# For skills, join list into comma-separated string and lowercase
df['skills'] = df['skills'].apply(lambda x: ', '.join([s.lower().strip() for s in x]) if isinstance(x, list) else '')

# ---------- Save to CSV ----------
csv_filename = 'remoteok_jobs_cleaned.csv'
df.to_csv(csv_filename, index=False)

# ---------- Summary ----------
print(f"\nCleaned data saved to '{csv_filename}'. Final row count: {len(df)}")
print("\nSample data:")
print(df.head())