
import requests
from html import unescape


HEADERS = {
    "User-Agent": "JobPulseAI/1.0 (public job-board collector)",
    "Accept": "application/json",
}

TIMEOUT = 20


def _get(url, params=None):
    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    except (requests.RequestException, ValueError) as error:
        print(f"Fetch failed: {url} — {error}")
        return None


def _location_text(location):
    """Convert different ATS location formats into readable text."""

    if isinstance(location, dict):
        return (
            location.get("name")
            or location.get("location")
            or location.get("city")
            or ""
        )

    if isinstance(location, list):
        return ", ".join(
            filter(None, (_location_text(item) for item in location))
        )

    return str(location or "").strip()


def _normalise(
    title,
    location,
    url,
    description,
    company,
    source,
):
    if not title or not url:
        return None

    return {
        "title": str(title).strip(),
        "location": _location_text(location),
        "absolute_url": str(url).strip(),
        "content": unescape(str(description or "")),
        "company": str(company or "").strip(),
        "source": source,
    }


def fetch_lever_jobs(board_token, company_name=None):
    """Fetch published jobs from a public Lever job board."""

    url = f"https://api.lever.co/v0/postings/{board_token}"

    data = _get(url, params={"mode": "json"})

    if not isinstance(data, list):
        return []

    jobs = []

    for item in data:
        categories = item.get("categories") or {}

        location = categories.get("location") or ""

        # Use all listed locations when available.
        if not location:
            location = categories.get("allLocations") or ""

        job = _normalise(
            title=item.get("text"),
            location=location,
            url=item.get("hostedUrl") or item.get("applyUrl"),
            description=(
                item.get("descriptionPlain")
                or item.get("description")
                or ""
            ),
            company=company_name or board_token,
            source="Lever",
        )

        if job:
            jobs.append(job)

    print(f"Lever [{board_token}]: {len(jobs)} jobs")
    return jobs


def fetch_ashby_jobs(board_token, company_name=None):
    """Fetch published jobs from a public Ashby job board."""

    url = (
        "https://api.ashbyhq.com/posting-api/"
        f"job-board/{board_token}"
    )

    data = _get(url)

    if not isinstance(data, dict):
        return []

    jobs = []

    for item in data.get("jobs", []):
        location = item.get("location") or ""

        # Include secondary locations for multi-location roles.
        secondary = item.get("secondaryLocations") or []

        secondary_names = [
            _location_text(loc.get("location") if isinstance(loc, dict) else loc)
            for loc in secondary
        ]

        all_locations = [location] + secondary_names
        location = ", ".join(
            dict.fromkeys(
                str(loc).strip()
                for loc in all_locations
                if loc and str(loc).strip()
            )
        )

        job = _normalise(
            title=item.get("title"),
            location=location,
            url=item.get("jobUrl") or item.get("applyUrl"),
            description=(
                item.get("descriptionPlain")
                or item.get("descriptionHtml")
                or ""
            ),
            company=company_name or board_token,
            source="Ashby",
        )

        if job:
            jobs.append(job)

    print(f"Ashby [{board_token}]: {len(jobs)} jobs")
    return jobs


def fetch_recruitee_jobs(board_token, company_name=None):
    """Fetch published jobs from a public Recruitee careers site."""

    url = f"https://{board_token}.recruitee.com/api/offers/"

    data = _get(url)

    if not isinstance(data, dict):
        return []

    offers = data.get("offers", [])
    jobs = []

    for item in offers:
        location = (
            item.get("locations")
            or item.get("location")
            or item.get("city")
            or ""
        )

        job_url = (
            item.get("careers_url")
            or item.get("careersUrl")
            or item.get("url")
        )

        if not job_url and item.get("slug"):
            job_url = (
                f"https://{board_token}.recruitee.com/o/"
                f"{item['slug']}"
            )

        job = _normalise(
            title=item.get("title"),
            location=location,
            url=job_url,
            description=(
                item.get("description")
                or item.get("description_html")
                or ""
            ),
            company=company_name or board_token,
            source="Recruitee",
        )

        if job:
            jobs.append(job)

    print(f"Recruitee [{board_token}]: {len(jobs)} jobs")
    return jobs