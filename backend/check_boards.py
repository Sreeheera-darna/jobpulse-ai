
import requests

url = "https://boards-api.greenhouse.io/v1/boards/instawork/jobs"

response = requests.get(
    url,
    params={"content": "true"},
    timeout=20
)
response.raise_for_status()

jobs = response.json().get("jobs", [])

keywords = ["intern", "internship"]

for job in jobs:
    title = job.get("title", "")
    location = job.get("location", {}).get("name", "")

    if (
        "india" in location.lower()
        and any(word in title.lower() for word in keywords)
    ):
        print("\n" + "=" * 60)
        print("TITLE:", title)
        print("LOCATION:", location)
        print("JOB URL:", job.get("absolute_url"))

        description = job.get("content", "")
        print("\nDESCRIPTION:")
        print(description[:1800])
