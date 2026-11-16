
import json
from pathlib import Path

from app.collectors.greenhouse import fetch_greenhouse_jobs
from app.services.cleaner import clean_and_deduplicate_jobs

COMPANIES = [
    "stripe", "twilio", "gitlab", "rubrik",
    "elastic", "okta", "purestorage", "mongodb",
    "anthropic", "fivetran", "netskope", "inmobi",
    "devrev", "coinbase", "druva", "airbnb"
]

OUTPUT_DIR = Path(__file__).resolve().parent

def collect_jobs():
    all_jobs = []

    for company in COMPANIES:
        print(f"\nCollecting jobs from {company}...")

        jobs = fetch_greenhouse_jobs(company)

        for job in jobs:
            job["source_company"] = company

        all_jobs.extend(jobs)

    print(f"\nTotal collected: {len(all_jobs)}")

    cleaned_jobs = clean_and_deduplicate_jobs(all_jobs)

    india_jobs = [
        job for job in cleaned_jobs
        if "india" in job.get("location", {}).get("name", "").lower()
    ]

    with open(OUTPUT_DIR / "cleaned_jobs.json", "w", encoding="utf-8") as file:
        json.dump(cleaned_jobs, file, indent=4, ensure_ascii=False)

    with open(OUTPUT_DIR / "india_jobs.json", "w", encoding="utf-8") as file:
        json.dump(india_jobs, file, indent=4, ensure_ascii=False)

    print(f"\nUnique jobs: {len(cleaned_jobs)}")
    print(f"India-based jobs: {len(india_jobs)}")
    print("Collection completed.")

if __name__ == "__main__":
    collect_jobs()