from models.job import JobPosting
from models.job_match import JobMatch


def rank_jobs(
    jobs: list[JobPosting],
    matches: list[JobMatch],
) -> list[tuple[JobPosting, JobMatch]]:
    """
    Combine job postings with their LLM match results
    and sort them by match score.
    """

    job_map = {
        str(index): job
        for index, job in enumerate(jobs)
    }

    ranked_jobs = []

    for match in matches:

        job = job_map.get(match.job_id)

        if job is None:
            continue

        ranked_jobs.append(
            (job, match)
        )

    ranked_jobs.sort(
        key=lambda item: item[1].match_score,
        reverse=True,
    )

    return ranked_jobs