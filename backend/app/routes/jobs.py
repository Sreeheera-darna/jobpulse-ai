
import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[2]
LATEST_JOBS_FILE = DATA_DIR / "india_jobs.json"
CLASSIFIED_JOBS_FILE = DATA_DIR / "india_jobs_classified.json"


def load_jobs():
    if not LATEST_JOBS_FILE.exists():
        return []

    with open(LATEST_JOBS_FILE, "r", encoding="utf-8") as file:
        latest_jobs = json.load(file)

    classifications = {}

    if CLASSIFIED_JOBS_FILE.exists():
        with open(CLASSIFIED_JOBS_FILE, "r", encoding="utf-8") as file:
            classified_jobs = json.load(file)

        for job in classified_jobs:
            job_url = job.get("absolute_url", "")
            if job_url and "ai_classification" in job:
                classifications[job_url] = job["ai_classification"]

    for job in latest_jobs:
        job_url = job.get("absolute_url", "")
        if job_url in classifications:
            job["ai_classification"] = classifications[job_url]

    return latest_jobs


@router.get("/jobs")
async def get_jobs(search: str = "", experience: str = ""):
    jobs = load_jobs()
    filtered_jobs = []

    for job in jobs:
        classification = job.get("ai_classification", {})

        title = job.get("title", "")
        company = job.get("source_company", "")
        original_location = job.get("location", {}).get("name", "")

        city = classification.get("city", original_location)
        role = classification.get("role_category", "Unclassified")
        experience_level = classification.get("experience_level", "Unknown")
        fresher_eligible = classification.get("is_fresher_eligible")

        if search:
            searchable_text = f"{title} {company} {city} {role}".lower()
            if search.lower() not in searchable_text:
                continue

        if experience:
            if experience.lower() == "fresher":
                if fresher_eligible is not True:
                    continue
            elif experience_level.lower() != experience.lower():
                continue

        filtered_jobs.append({
            "id": job.get("absolute_url", title + company),
            "title": title,
            "company": company,
            "city": city,
            "role": role,
            "experience": experience_level,
            "is_fresher_eligible": fresher_eligible,
            "job_url": job.get("absolute_url", "")
        })

    return {
        "total": len(filtered_jobs),
        "jobs": filtered_jobs
    }