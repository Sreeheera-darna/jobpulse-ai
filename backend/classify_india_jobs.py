
import json
import time
from pathlib import Path
from app.services.classifier import classify_job

INPUT_FILE = Path("india_jobs.json")
OUTPUT_FILE = Path("india_jobs_classified.json")

# Load existing progress or start with original jobs.
if OUTPUT_FILE.exists():
    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        jobs = json.load(file)
else:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=4, ensure_ascii=False)

    print("Created classification progress file.")

total = len(jobs)
completed = sum(
    1 for job in jobs
    if "ai_classification" in job
)

print(f"Total India jobs: {total}")
print(f"Already classified: {completed}")
print(f"Remaining: {total - completed}")

if completed == total:
    print("All jobs have already been classified.")

else:
    for index, job in enumerate(jobs):

        if "ai_classification" in job:
            continue

        print(
            f"\nClassifying {index + 1}/{total}: "
            f"{job.get('title')}"
        )

        try:
            result = classify_job(job)

            job["ai_classification"] = result.model_dump()

            # Save progress after every successful job.
            with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    jobs,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            completed += 1
            print(f"Successfully classified: {completed}/{total}")

            time.sleep(4)

        except Exception as error:
            print(f"Classification stopped: {error}")
            print("Successful results have been saved.")
            break

print(f"\nClassification progress: {completed}/{total}")
print(f"Results file: {OUTPUT_FILE}")