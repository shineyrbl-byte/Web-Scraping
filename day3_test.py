import requests
from bs4 import BeautifulSoup
import json

url = "https://remoteok.com/api"
headers = {"User-Agent": "Mozilla/5.0"}

data = requests.get(url, headers=headers).json()[1:]

html = ""

# ---------- Create HTML Structure ----------
for i, job in enumerate(data):

    company = job.get("company", "Not Specified")
    location = job.get("location", "Not Specified")
    tags = job.get("tags", [])
    link = job.get("url", "")

    skills_html = ""

    for skill in tags:
        skills_html += f"""
        <a class='no-border tooltip-set action-add-tag'>
            <div>
                <h3>{skill}</h3>
            </div>
        </a>
        """

    html += f"""
    <tr data-offset="{i}" data-company="{company}" href="{link}">
        <td class="company position company_and_position">
            <div class="location tooltip">{location}</div>
        </td>

        <td class="tags">
            {skills_html}
        </td>
    </tr>
    """

# ---------- Parse HTML ----------
soup = BeautifulSoup(html, "html.parser")
rows = soup.find_all("tr", attrs={"data-offset": True})

joblist = []

# ---------- Extract Data ----------
for row in rows:

    # Company
    company = row.get("data-company", "Not Specified")

    # URL
    job_url = row.get("href", "Not Available")

    # Location
    loc_tag = row.find("div", class_="location")
    if loc_tag:
        location_text = loc_tag.text.strip()
        if "🌏" in location_text or "worldwide" in location_text.lower():
            location = "Worldwide"
        else:
            location = location_text
    else:
        location = "Not Specified"

    
    # Skills
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


    # Combine
    job_data = {
        "company": company,
        "location": location,
        "employment_type": emp_type,
        "skills": skills,
        "url": job_url
    }

    joblist.append(job_data)

# ---------- Print Output ----------
print (joblist)