from models.candidate import CandidateProfile
from models.job import JobPosting
from agents.job_analyzer import JobAnalysis
from tools.adzuna import search_jobs


def search_jobs_for_candidate(
    profile: CandidateProfile,
    analysis: JobAnalysis,
    country: str = "de",
):
    """
    Search for jobs based on the target-position analysis
    and remove duplicate job postings.
    """

    all_jobs = []

    for keyword in analysis.search_keywords:

        jobs = search_jobs(
            query=keyword,
            country=country,
            page=1,
            results_per_page=10,
        )

        all_jobs.extend(jobs)

    return remove_duplicate_jobs(all_jobs)


def remove_duplicate_jobs(
    jobs: list[JobPosting],
) -> list[JobPosting]:
    """
    Remove duplicate job postings.

    Jobs are considered duplicates primarily based on their URL.
    If URL is unavailable, title + company + location are used.
    """

    unique_jobs = []
    seen = set()

    for job in jobs:

        # -----------------------------------------
        # Prefer URL as the unique identifier
        # -----------------------------------------

        if job.url:

            identifier = (
                "url",
                job.url.strip().lower()
            )

        else:

            # -----------------------------------------
            # Fallback identifier
            # -----------------------------------------

            identifier = (
                "details",
                (job.title or "").strip().lower(),
                (job.company or "").strip().lower(),
                (job.location or "").strip().lower(),
            )

        if identifier in seen:
            continue

        seen.add(identifier)
        unique_jobs.append(job)

    return unique_jobs