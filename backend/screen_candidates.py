import json
import csv
import re
from pathlib import Path
path = Path("india_jobs_classified.json")
jobs = json.loads(path.read_text(encoding="utf-8"))
pattern = re.compile(
    r"\bintern(ship)?\b|"
    r"\bfresher(s)?\b|"
    r"\bgraduate\b|"
    r"\bnew grad(uate)?\b|"
    r"\bentry[- ]level\b|"
    r"\bcampus\b|"
    r"\btrainee\b|"
    r"\b0\s*[-–to]+\s*1\s+years?\b|"
    r"\bearly career\b|"
    r"\buniversity graduate\b",
    re.I
)
candidates = []
for job in jobs:
    classification = job.get("ai_classification") or {}
    text = " ".join(str(job.get(k, "")) for k in
                    ["title", "content", "description", "location"])
    if pattern.search(text):
        candidates.append({
            "title": job.get("title", ""),
            "company": job.get("company", ""),
            "location": job.get("location", ""),
            "ai_experience_level": classification.get("experience_level", ""),
            "ai_fresher_eligible": classification.get("is_fresher_eligible", ""),
            "job_url": job.get("absolute_url", ""),
            "manual_verification": "PENDING"
        })
with open("candidate_review.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=candidates[0].keys() if candidates else [
        "title", "company", "location", "ai_experience_level",
        "ai_fresher_eligible", "job_url", "manual_verification"
    ])
    writer.writeheader()
    writer.writerows(candidates)
print("Total jobs:", len(jobs))
print("Potential candidates for manual review:", len(candidates))
print("Created: candidate_review.csv")
