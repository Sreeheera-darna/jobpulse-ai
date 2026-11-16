
import json

from app.collectors.greenhouse import fetch_greenhouse_jobs
from app.services.cleaner import clean_and_deduplicate_jobs


companies = [
    "stripe",
    "twilio",
    "gitlab",
    "rubrik",
    "elastic",
    "okta",
    "purestorage",
    "mongodb",
    "anthropic",
    "fivetran",
    "netskope",
    "inmobi",
    "devrev",
    "coinbase",
    "druva",
    "airbnb"
]
all_jobs = []

# 1. Collect jobs from all companies
for company in companies:
    print(f"\nCollecting jobs from {company}...")

    jobs = fetch_greenhouse_jobs(company)

    for job in jobs:
        job["source_company"] = company

    all_jobs.extend(jobs)

print("\nRaw jobs collected:", len(all_jobs))

# 2. Clean jobs and remove duplicates
cleaned_jobs = clean_and_deduplicate_jobs(all_jobs)

print("Cleaned unique jobs:", len(cleaned_jobs))

# 3. Identify India-based jobs
india_jobs = [
    job for job in cleaned_jobs
    if "india" in job.get("location", {}).get("name", "").lower()
]

print("India-based jobs:", len(india_jobs))

# 4. Save cleaned jobs
with open("cleaned_jobs.json", "w", encoding="utf-8") as file:
    json.dump(cleaned_jobs, file, indent=4, ensure_ascii=False)

# 5. Save India-based jobs separately
with open("india_jobs.json", "w", encoding="utf-8") as file:
    json.dump(india_jobs, file, indent=4, ensure_ascii=False)

print("\nSaved cleaned_jobs.json and india_jobs.json")