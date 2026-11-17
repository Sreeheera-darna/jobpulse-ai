
import json
from pathlib import Path
from app.services.classifier import classify_job

data_file = Path(__file__).parent / "india_jobs.json"

with open(data_file, "r", encoding="utf-8") as file:
    jobs = json.load(file)

if not jobs:
    raise ValueError("No jobs found in india_jobs.json")

job = jobs[0]

print("Testing classification for:", job.get("title", "Unknown"))

result = classify_job(job)

print("Classification:", result.model_dump())
print("Cost test completed.")
