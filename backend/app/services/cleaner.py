
def clean_and_deduplicate_jobs(jobs):
    cleaned_jobs = []
    seen_jobs = set()

    for job in jobs:
        if not isinstance(job, dict):
            continue

        title = str(job.get("title") or "").strip()
        raw_location = job.get("location", "")

        if isinstance(raw_location, dict):
            location = str(raw_location.get("name") or "").strip()
        else:
            location = str(raw_location or "").strip()

        company = str(
            job.get("source_company")
            or job.get("company")
            or ""
        ).strip()

        job_url = str(job.get("absolute_url") or "").strip()

        # Skip incomplete records.
        if not title or not location or not job_url:
            continue

        # Normalize text.
        job["title"] = " ".join(title.split())
        job["location"] = {
            "name": " ".join(location.split())
        }
        job["source_company"] = company

        # Normalize URL for deduplication.
        unique_key = job_url.lower().rstrip("/")

        if unique_key in seen_jobs:
            continue

        seen_jobs.add(unique_key)
        cleaned_jobs.append(job)

    return cleaned_jobs