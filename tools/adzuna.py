import os

import requests
from dotenv import load_dotenv

from models.job import JobPosting


load_dotenv()


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


def search_jobs(
    query: str,
    country: str = "de",
    page: int = 1,
    results_per_page: int = 10,
) -> list[JobPosting]:
    """
    Search jobs using the Adzuna API and return
    standardized JobPosting objects.
    """

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise ValueError(
            "ADZUNA_APP_ID or ADZUNA_APP_KEY is missing."
        )

    url = (
        f"https://api.adzuna.com/v1/api/"
        f"jobs/{country}/search/{page}"
    )

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": query,
        "content-type": "application/json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("results", []):

        salary = job.get("salary_min")
        salary_max = job.get("salary_max")

        job_posting = JobPosting(
            title=job.get("title", "Unknown"),
            company=job.get("company", {}).get("display_name"),
            location=job.get("location", {}).get("display_name"),
            description=job.get("description"),
            url=job.get("redirect_url"),
            salary_min=salary,
            salary_max=salary_max,
            contract_type=job.get("contract_type"),
            category=job.get("category", {}).get("label"),
        )

        jobs.append(job_posting)

    return jobs