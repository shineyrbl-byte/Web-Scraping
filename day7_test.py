import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Load CSV ----------
df = pd.read_csv("remoteok_jobs_full.csv")

# ---------- Setup ----------
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10,6)

# ---------- Top 10 Job Titles ----------
top_titles = df['title'].value_counts().head(10)
plt.figure()
sns.barplot(x=top_titles.values, y=top_titles.index, palette="viridis")
plt.title("Top 10 Job Titles")
plt.xlabel("Number of Jobs")
plt.ylabel("Job Title")
plt.tight_layout()
plt.show()

# ---------- Top 10 Companies ----------
top_companies = df['company'].value_counts().head(10)
plt.figure()
sns.barplot(x=top_companies.values, y=top_companies.index, palette="magma")
plt.title("Top 10 Companies by Job Postings")
plt.xlabel("Number of Jobs")
plt.ylabel("Company")
plt.tight_layout()
plt.show()

# ---------- Top 10 Locations ----------
top_locations = df['location'].value_counts().head(10)
plt.figure()
sns.barplot(x=top_locations.values, y=top_locations.index, palette="coolwarm")
plt.title("Top 10 Job Locations")
plt.xlabel("Number of Jobs")
plt.ylabel("Location")
plt.tight_layout()
plt.show()

# ---------- Top 10 Skills ----------
# Explode skills into individual rows
df_skills = df.copy()
df_skills['skills'] = df_skills['skills'].str.split(', ')
df_skills = df_skills.explode('skills')
df_skills = df_skills[df_skills['skills'].str.strip() != '']
top_skills = df_skills['skills'].value_counts().head(10)

plt.figure()
sns.barplot(x=top_skills.values, y=top_skills.index, palette="cubehelix")
plt.title("Top 10 Skills in Job Listings")
plt.xlabel("Number of Jobs")
plt.ylabel("Skill")
plt.tight_layout()
plt.show()

# ---------- Job Type Distribution ----------
job_types = df['employment_type'].value_counts()
plt.figure()
sns.barplot(x=job_types.index, y=job_types.values, palette="Set2")
plt.title("Job Type Distribution")
plt.xlabel("Employment Type")
plt.ylabel("Number of Jobs")
plt.tight_layout()
plt.show()

# ---------- Average Skills per Job ----------
df['num_skills'] = df['skills'].apply(lambda x: len(str(x).split(', ')) if x else 0)
plt.figure()
sns.histplot(df['num_skills'], bins=range(0,15), kde=False, color="skyblue")
plt.title("Distribution of Number of Skills per Job")
plt.xlabel("Number of Skills")
plt.ylabel("Number of Jobs")
plt.tight_layout()
plt.show()