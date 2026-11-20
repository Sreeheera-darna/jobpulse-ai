import csv
import html
import json
import random
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JOBS_FILE = BASE_DIR / "india_jobs_classified.json"
AUDIT_FILE = BASE_DIR / "manual_audit_50_review.csv"
SAMPLE_SIZE = 50

FIELDS = [
    "title",
    "company",
    "location",
    "description",
    "job_url",
    "ai_experience_level",
    "ai_fresher_eligible",
    "ai_employment_type",
    "ai_role_category",
    "ai_city",
    "manual_experience_level",
    "manual_fresher_eligible",
    "manual_employment_type",
    "manual_role_category",
    "manual_city",
    "reviewer_notes",
]


def clean_location(value):
    if isinstance(value, dict):
        return value.get("name", "")
    return value or ""


def clean_description(value):
    value = html.unescape(str(value or ""))
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


with JOBS_FILE.open(encoding="utf-8") as file:
    jobs = json.load(file)

classified = [
    job for job in jobs
    if isinstance(job.get("ai_classification"), dict)
]
sample = random.Random(42).sample(
    classified,
    min(SAMPLE_SIZE, len(classified)),
)

with AUDIT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=FIELDS)
    writer.writeheader()

    for job in sample:
        classification = job["ai_classification"]
        writer.writerow({
            "title": job.get("title", ""),
            "company": job.get("company", ""),
            "location": clean_location(job.get("location")),
            "description": clean_description(
                job.get("content") or job.get("description", "")
            ),
            "job_url": job.get("absolute_url", ""),
            "ai_experience_level": classification.get("experience_level", ""),
            "ai_fresher_eligible": classification.get(
                "is_fresher_eligible", ""
            ),
            "ai_employment_type": classification.get("employment_type", ""),
            "ai_role_category": classification.get("role_category", ""),
            "ai_city": classification.get("city", ""),
            "manual_experience_level": "",
            "manual_fresher_eligible": "",
            "manual_employment_type": "",
            "manual_role_category": "",
            "manual_city": "",
            "reviewer_notes": "",
        })

print(f"Classified jobs: {len(classified)}")
print(f"Audit sample: {len(sample)}")
print(f"Created: {AUDIT_FILE}")
