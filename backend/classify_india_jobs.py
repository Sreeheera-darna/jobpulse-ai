
import json
import time
from pathlib import Path
from app.services.classifier import classify_job

INPUT_FILE = Path("india_jobs.json")
OUTPUT_FILE = Path("india_jobs_classified.json")

MAX_RETRIES = 5
NORMAL_DELAY = 5


# Load the latest India jobs dataset.
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    latest_jobs = json.load(file)

# Load previous classifications and preserve them by job URL.
previously_classified = {}

if OUTPUT_FILE.exists():
    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        old_jobs = json.load(file)

    for old_job in old_jobs:
        job_url = old_job.get("absolute_url", "")
        if job_url and "ai_classification" in old_job:
            previously_classified[job_url] = old_job["ai_classification"]

# Merge previous classifications into the latest dataset.
# Reuse previous classifications to avoid unnecessary API calls.
jobs = []

for job in latest_jobs:
    job_url = job.get("absolute_url", "")

    if job_url in previously_classified:
        job["ai_classification"] = previously_classified[job_url]

    jobs.append(job)


# Save the merged dataset.
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(jobs, file, indent=4, ensure_ascii=False)

total = len(jobs)
completed = sum(1 for job in jobs if "ai_classification" in job)

print(f"Total India jobs: {total}")
print(f"Already classified: {completed}")
print(f"Remaining: {total - completed}")

for index, job in enumerate(jobs):

    if "ai_classification" in job:
        continue

    print(f"\nClassifying {index + 1}/{total}: {job.get('title')}")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = classify_job(job)
            job["ai_classification"] = result.model_dump()

            with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
                json.dump(jobs, file, indent=4, ensure_ascii=False)

            completed += 1
            print(f"Successfully classified: {completed}/{total}")

            time.sleep(NORMAL_DELAY)
            break

       
        except Exception as error:
            error_message = str(error)

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):
                if attempt < MAX_RETRIES:
                    wait_time = (
                        15 * attempt
                        if "429" in error_message
                        else 5 * attempt
                    )
                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds "
                        f"({attempt}/{MAX_RETRIES})..."
                    )
                    time.sleep(wait_time)
                else:
                    print("Maximum retries reached. Stopping safely.")
                    print(f"Last error: {error}")
                    break
            else:
                print(f"Classification stopped: {error}")
                break