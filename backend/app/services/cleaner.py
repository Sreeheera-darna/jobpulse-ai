def clean_and_deduplicate_jobs(jobs):
    cleaned_jobs = []
    seen_jobs = set()

    for job in jobs:
        title = job.get("title", "").strip()
        location = job.get("location", {}).get("name", "").strip()
        company = job.get("source_company", "").strip()
        job_url = job.get("absolute_url", "").strip()

        # Skip records missing essential information
        if not title or not location or not job_url:
            continue

        # Normalize text
        job["title"] = " ".join(title.split())
        job["location"]["name"] = " ".join(location.split())
        job["source_company"] = company

        # Use the original job URL to identify duplicates
        unique_key = job_url.lower().rstrip("/")

        if unique_key in seen_jobs:
            continue

        seen_jobs.add(unique_key)
        cleaned_jobs.append(job)

    return cleaned_jobs