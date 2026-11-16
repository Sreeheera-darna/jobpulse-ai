
import requests


def fetch_greenhouse_jobs(board_token):
    """
    Fetch job listings from a company's public Greenhouse job board.
    """

    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"

    try:
        response = requests.get(
            url,
            params={"content": "true"},
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        jobs = data.get("jobs", [])

        print(f"Fetched {len(jobs)} jobs from Greenhouse.")

        return jobs

    except requests.RequestException as error:
        print(f"Error fetching Greenhouse jobs: {error}")
        return []