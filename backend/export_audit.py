import csv
import json
import random
import re
import html
from pathlib import Path

DATA_FILE = Path(__file__).parent / "india_jobs_classified.json"
OUTPUT_FILE = Path(__file__).parent / "manual_audit_50.csv"

with open(DATA_FILE, "r", encoding="utf-8") as file:
    jobs = json.load(file)

eligible = [
    job for job in jobs
    if job.get("ai_classification", {}).get("is_fresher_eligible") is True
]

not_eligible = [
    job for job in jobs
    if job.get("ai_classification", {}).get("is_fresher_eligible") is not True
]

random.seed(42)
sample_size = min(35, len(not_eligible))
sample = eligible + random.sample(not_eligible, sample_size)

rows = []

for job in sample:
    classification = job.get("ai_classification", {})
    description = html.unescape(
        re.sub(r"<[^>]+>", " ", job.get("content", ""))
    )
    description = re.sub(r"\s+", " ", description).strip()

    rows.append({
        "Title": job.get("title", ""),
        "Company": job.get("source_company", ""),
        "Location": job.get("location", {}).get("name", ""),
        "AI Experience": classification.get("experience_level", ""),
        "AI Fresher Eligible": classification.get("is_fresher_eligible", ""),
        "AI Role": classification.get("role_category", ""),
        "AI Confidence": classification.get("confidence", ""),
        "Job Description": description[:4000],
        "Job URL": job.get("absolute_url", ""),
        "Human Experience": "",
        "Human Fresher Eligible": "",
        "Audit Notes": ""
    })

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Audit file created: {OUTPUT_FILE}")
print(f"Total listings exported: {len(rows)}")
print(f"AI-identified eligible listings included: {len(eligible)}")