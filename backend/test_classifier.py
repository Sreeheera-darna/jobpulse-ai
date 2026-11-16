import json

from app.services.classifier import classify_job

# Load our collected India-based jobs
with open("india_jobs.json", "r", encoding="utf-8") as file:
    jobs = json.load(file)

if not jobs:
    print("No India-based jobs found.")
else:
    # Test only one job to control API usage
    job = next(
    (j for j in jobs if j.get("title") == "Associate, Marketing Technology"),
    None
)
    if job is None:
       print("Test job not found.")
       exit()

    print("Testing AI classification...")
    print("Job title:", job.get("title"))

    result = classify_job(job)

    print("\nAI Classification Result:")
    print(result.model_dump_json(indent=2))