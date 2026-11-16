
import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

DATA_FILE = Path(__file__).resolve().parents[2] / "india_jobs_classified.json"


def load_jobs():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


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
        experience_level = classification.get(
            "experience_level", "Unknown"
        )
        fresher_eligible = classification.get(
            "is_fresher_eligible", None
        )

        if search:
            search_text = search.lower()
            searchable_text = (
                f"{title} {company} {city} {role}"
            ).lower()

            if search_text not in searchable_text:
                continue

        if experience and experience_level.lower() != experience.lower():
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
