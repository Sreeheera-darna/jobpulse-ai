
import json
import re
from pathlib import Path

from app.collectors.greenhouse import fetch_greenhouse_jobs
from app.collectors.other_ats import (
    fetch_lever_jobs,
    fetch_ashby_jobs,
    fetch_recruitee_jobs,
)
from app.services.cleaner import clean_and_deduplicate_jobs


GREENHOUSE_COMPANIES = [
    "stripe", "twilio", "gitlab", "rubrik",
    "elastic", "okta", "purestorage", "mongodb",
    "anthropic", "fivetran", "netskope", "inmobi",
    "devrev", "coinbase", "druva", "airbnb", "instawork"
]

# Format: board identifier: actual company name

LEVER_BOARDS = {
    "100ms": "100ms",
    "acceldata": "Acceldata",
    "cred": "CRED",
    "hevodata": "Hevo Data",
    "meesho": "Meesho",
    "mindtickle": "Mindtickle",
    "levelai": "Level AI",
    "mactores": "Mactores",
    "nium": "Nium",
    "onit": "Onit",
    "shieldai": "Shield AI",
    "shyftlabs": "ShyftLabs",
    "sonatype": "Sonatype",
    "sophos": "Sophos",
    "ttecdigital": "TTEC Digital",
    "turvo": "Turvo",
}

ASHBY_BOARDS = {
    "aiprise": "AiPrise",
    "atlan": "Atlan",
    "atlys": "Atlys",
    "sarvam": "Sarvam AI",
    "snowflake": "Snowflake",
}

# No Recruitee board identifiers verified yet.
RECRUITEE_BOARDS = {}


INDIAN_LOCATIONS = {
    "bengaluru", "bangalore",
    "hyderabad", "pune", "mumbai",
    "delhi", "new delhi", "gurugram", "gurgaon",
    "noida", "chennai", "kolkata",
    "kochi", "cochin", "thiruvananthapuram",
    "ahmedabad", "jaipur", "indore",
    "chandigarh", "lucknow", "bhubaneswar",
    "visakhapatnam", "vizag", "coimbatore",
    "mysore", "mysuru", "warangal"
}

OUTPUT_DIR = Path(__file__).resolve().parent


def is_india_location(location):
    """Match explicit Indian country names, country codes or city names."""

    if not location:
        return False

    text = str(location).lower().strip()
    text = re.sub(r"\s+", " ", text)

    components = {
        part.strip().strip(".")
        for part in text.split(",")
    }

    if "india" in components or "in" in components:
        return True

    for city in INDIAN_LOCATIONS:
        pattern = rf"(?<![a-z]){re.escape(city)}(?![a-z])"

        if re.search(pattern, text):
            return True

    return False


def get_location_name(job):
    location = job.get("location", "")

    if isinstance(location, dict):
        return location.get("name", "")

    return str(location or "")


def add_company_metadata(jobs, company, source):
    """Keep company and source fields consistent."""

    for job in jobs:
        job["source_company"] = company
        job["company"] = job.get("company") or company
        job["source"] = source

    return jobs


def collect_jobs():
    all_jobs = []

    # 1. Greenhouse
    for company in GREENHOUSE_COMPANIES:
        print(f"\nCollecting Greenhouse jobs from {company}...")

        try:
            jobs = fetch_greenhouse_jobs(company)

            all_jobs.extend(
                add_company_metadata(jobs, company, "Greenhouse")
            )

            print(f"Collected: {len(jobs)}")

        except Exception as error:
            print(f"Failed to collect from {company}: {error}")

    # 2. Lever
    for board, company_name in LEVER_BOARDS.items():
        print(f"\nCollecting Lever jobs from {company_name}...")

        try:
            jobs = fetch_lever_jobs(board, company_name)

            all_jobs.extend(
                add_company_metadata(jobs, company_name, "Lever")
            )

            print(f"Collected: {len(jobs)}")

        except Exception as error:
            print(f"Failed to collect from {company_name}: {error}")

    # 3. Ashby
    for board, company_name in ASHBY_BOARDS.items():
        print(f"\nCollecting Ashby jobs from {company_name}...")

        try:
            jobs = fetch_ashby_jobs(board, company_name)

            all_jobs.extend(
                add_company_metadata(jobs, company_name, "Ashby")
            )

            print(f"Collected: {len(jobs)}")

        except Exception as error:
            print(f"Failed to collect from {company_name}: {error}")

    # 4. Recruitee
    for board, company_name in RECRUITEE_BOARDS.items():
        print(f"\nCollecting Recruitee jobs from {company_name}...")

        try:
            jobs = fetch_recruitee_jobs(board, company_name)

            all_jobs.extend(
                add_company_metadata(jobs, company_name, "Recruitee")
            )

            print(f"Collected: {len(jobs)}")

        except Exception as error:
            print(f"Failed to collect from {company_name}: {error}")

    print(f"\nTotal collected before cleaning: {len(all_jobs)}")

    cleaned_jobs = clean_and_deduplicate_jobs(all_jobs)

    india_jobs = [
        job for job in cleaned_jobs
        if is_india_location(get_location_name(job))
    ]

    with open(
        OUTPUT_DIR / "cleaned_jobs.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(cleaned_jobs, file, indent=4, ensure_ascii=False)

    with open(
        OUTPUT_DIR / "india_jobs.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(india_jobs, file, indent=4, ensure_ascii=False)

    print(f"\nUnique jobs: {len(cleaned_jobs)}")
    print(f"India-based jobs: {len(india_jobs)}")
    print("Collection completed.")


if __name__ == "__main__":
    collect_jobs()