
import json
import time
from pathlib import Path

from app.services.classifier import classify_job


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "india_jobs.json"
OUTPUT_FILE = BASE_DIR / "india_jobs_classified.json"

MAX_RETRIES = 5
NORMAL_DELAY = 5


def save_jobs(jobs):
    """Save progress safely after each classification."""
    temp_file = OUTPUT_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=4, ensure_ascii=False)

    temp_file.replace(OUTPUT_FILE)


# Load latest India jobs.
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    latest_jobs = json.load(file)


# Load previous classifications.
previously_classified = {}

if OUTPUT_FILE.exists():
    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        old_jobs = json.load(file)

    for old_job in old_jobs:
        job_url = old_job.get("absolute_url", "")

        if job_url and old_job.get("ai_classification"):
            previously_classified[job_url] = old_job["ai_classification"]


# Preserve classifications for jobs already processed.
jobs = []

for job in latest_jobs:
    job_url = job.get("absolute_url", "")

    if job_url in previously_classified:
        job["ai_classification"] = previously_classified[job_url]

    jobs.append(job)


save_jobs(jobs)

total = len(jobs)

completed = sum(
    1 for job in jobs
    if job.get("ai_classification")
)

remaining = total - completed

print(f"Total India jobs: {total}")
print(f"Already classified: {completed}")
print(f"Remaining: {remaining}")


# Classify only jobs without an existing classification.
for index, job in enumerate(jobs):

    if job.get("ai_classification"):
        continue

    print(
        f"\nClassifying {index + 1}/{total}: "
        f"{job.get('title')}"
    )

    classified_successfully = False

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            result = classify_job(job)

            job["ai_classification"] = result.model_dump()

            save_jobs(jobs)

            completed += 1
            classified_successfully = True

            print(f"Successfully classified: {completed}/{total}")

            time.sleep(NORMAL_DELAY)
            break

        except Exception as error:

            error_message = str(error).upper()

            temporary_error = any(
                code in error_message
                for code in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                ]
            )

            if temporary_error and attempt < MAX_RETRIES:

                wait_time = (
                    15 * attempt
                    if "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                    else 5 * attempt
                )

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds "
                    f"({attempt}/{MAX_RETRIES})..."
                )

                time.sleep(wait_time)

            else:
                print(f"\nClassification stopped: {error}")
                print("Progress has been saved.")
                break

    if not classified_successfully:
        print("Stopping classification to avoid repeated failures.")
        break


# Final progress report.
remaining = total - completed

print("\n========== CLASSIFICATION SUMMARY ==========")
print(f"Total India jobs: {total}")
print(f"Successfully classified: {completed}")
print(f"Still unclassified: {remaining}")
print("============================================")