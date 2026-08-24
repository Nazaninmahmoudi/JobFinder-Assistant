from models.candidate import CandidateProfile
from models.job import JobPosting
from agents.job_analyzer import JobAnalysis


def calculate_job_score(
    job: JobPosting,
    profile: CandidateProfile,
    analysis: JobAnalysis,
) -> float:
    """
    Calculate a preliminary rule-based match score
    for a job posting.
    """

    score = 0.0

    title = (job.title or "").lower()
    description = (job.description or "").lower()



    target_position = analysis.target_position.lower()

    if target_position in title:
        score += 30

    keyword_matches = 0

    for keyword in analysis.search_keywords:

        keyword_lower = keyword.lower()

        if keyword_lower in title:
            keyword_matches += 1

    if keyword_matches > 0:
        score += min(keyword_matches * 10, 30)


    relevant_skills = analysis.relevant_skills

    if relevant_skills:

        matched_skills = 0

        for skill in relevant_skills:

            skill_lower = skill.lower()

            if skill_lower in title or skill_lower in description:
                matched_skills += 1

        skill_score = (
            matched_skills / len(relevant_skills)
        ) * 25

        score += skill_score


    seniority = analysis.seniority.lower()

    junior_keywords = [
        "junior",
        "entry",
        "graduate",
        "trainee",
        "intern",
    ]

    senior_keywords = [
        "senior",
        "lead",
        "principal",
        "staff",
        "manager",
    ]

    if seniority in ["entry-level", "junior"]:

        if any(keyword in title for keyword in junior_keywords):
            score += 10

        if any(keyword in title for keyword in senior_keywords):
            score -= 10

    elif seniority == "senior":

        if any(keyword in title for keyword in senior_keywords):
            score += 10


    if job.description:
        score += 5

    score = max(0, min(score, 100))

    return round(score, 2)


def rank_jobs(
    jobs: list[JobPosting],
    profile: CandidateProfile,
    analysis: JobAnalysis,
    top_k: int = 15,
) -> list[tuple[JobPosting, float]]:
    """
    Rank jobs using rule-based scoring.
    """

    scored_jobs = []

    for job in jobs:

        score = calculate_job_score(
            job,
            profile,
            analysis,
        )

        scored_jobs.append(
            (job, score)
        )

    scored_jobs.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return scored_jobs[:top_k]