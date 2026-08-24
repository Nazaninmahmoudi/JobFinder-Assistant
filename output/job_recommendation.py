from models.job_match import JobMatch, JobMatches


def rank_jobs(
    job_matches: JobMatches,
) -> list[JobMatch]:
    """
    Sort jobs by match score from highest to lowest.
    """

    return sorted(
        job_matches.matches,
        key=lambda job: job.match_score,
        reverse=True,
    )


def get_top_jobs(
    job_matches: JobMatches,
    top_n: int = 10,
) -> list[JobMatch]:
    """
    Return the top N jobs based on match score.
    """

    ranked_jobs = rank_jobs(job_matches)

    return ranked_jobs[:top_n]