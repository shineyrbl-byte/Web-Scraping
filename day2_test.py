import requests
from bs4 import BeautifulSoup

url = "https://remoteok.com/api"
headers = {"User-Agent": "Mozilla/5.0"}

data = requests.get(url, headers=headers).json()[1:]

# Create simple HTML like the website structure
html = ""

for i, job in enumerate(data):
    html += f"""
    <tr data-offset="{i}">
        <td class="company position company_and_position">
            <a itemprop="url">
                <h2>{job['position']}</h2>
            </a>
        </td>
    </tr>
    """

soup = BeautifulSoup(html, "html.parser")

rows = soup.find_all("tr", attrs={"data-offset": True})
joblist=[]
for row in rows:
    titles = row.find_all("td", class_="company_and_position")
    for t in titles:
        link = t.find("a", attrs={"itemprop": "url"})
        if link:
            jobname = link.find("h2").text
            joblist.append(jobname)

print(joblist)

# Print first 10
for i, title in enumerate(joblist[:10]):
    print(f"{i+1}. {title}")