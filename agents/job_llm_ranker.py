import os

from dotenv import load_dotenv
from openai import OpenAI

from models.job import JobPosting
from models.job_match import (
    JobMatch,
    JobMatchLLM,
    JobMatches,
    JobMatchesLLM,
)
from agents.job_analyzer import JobAnalysis


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

BATCH_SIZE = 3

MODEL_NAME = "openai/gpt-oss-120b"

MAX_COMPLETION_TOKENS = 3000


def _analyze_batch(
    analysis: JobAnalysis,
    jobs: list[JobPosting],
    start_index: int,
) -> list[JobMatch]:


    candidate_info = {
        "target_position": analysis.target_position,
        "relevant_skills": analysis.relevant_skills,
        "relevant_experience_years": (
            analysis.relevant_experience_years
        ),
        "seniority": analysis.seniority,
    }


    jobs_data = []

    for index, job in enumerate(jobs):

        jobs_data.append(
            {
                "job_id": str(start_index + index),
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description,
            }
        )

    prompt = f"""
You are an expert technical recruiter.

Evaluate ALL provided jobs against the candidate.

============================================================
CANDIDATE
============================================================

{candidate_info}


============================================================
JOBS
============================================================

{jobs_data}


============================================================
TASK
============================================================

For every job:

1. Read the FULL job description.

2. Identify the company's actual requirements.

3. Compare those requirements against the candidate.

4. Calculate a realistic match score from 0 to 100.

5. Be conservative.

6. Never invent candidate experience.

7. Teaching experience must NOT automatically count as
   professional industry experience.

8. Only list a skill as matched if the candidate actually
   demonstrates that skill.

9. List important missing skills and requirements.

10. Pay special attention to:
    - required skills
    - preferred skills
    - years of experience
    - seniority
    - education
    - certifications
    - domain knowledge
    - language requirements
    - production experience
    - deployment requirements
    - cloud requirements
    - eligibility requirements


============================================================
IMPORTANT DISTINCTION
============================================================

The following fields describe the COMPANY / JOB:

required_skills
experience_requirement
seniority_requirement
eligibility_requirements

The following fields describe the CANDIDATE'S MATCH:

matched_skills
missing_skills
experience_match

Do NOT mix these concepts.

For example:

experience_requirement:
"2+ years of professional ML experience"

experience_match:
"Candidate has 0 years of professional ML experience"


============================================================
OUTPUT
============================================================

Return EXACTLY one result for every provided job.

Use the exact job_id provided.

The output MUST be an object containing a "matches" array.

Each result MUST contain exactly these fields:

- job_id
- match_score
- matched_skills
- missing_skills
- required_skills
- experience_requirement
- seniority_requirement
- eligibility_requirements
- experience_match
- recommendation
- explanation


============================================================
FIELD RULES
============================================================

match_score:
Number between 0 and 100.

matched_skills:
Only skills actually supported by the candidate.

missing_skills:
Important skills required by the job that the candidate
does not demonstrate.

required_skills:
Important technical or professional skills explicitly
required by the job.

experience_requirement:
State the company's actual experience requirement.

Examples:
"2+ years of professional ML experience"
"3-5 years of software engineering experience"
"No professional experience required"

seniority_requirement:
State the seniority expected by the company.

Examples:
"Entry-level"
"Junior"
"Mid-level"
"Senior"
"Senior-level, 5+ years"

eligibility_requirements:
Important eligibility conditions such as:

- German language
- English language
- degree requirements
- work authorization
- location requirements
- citizenship requirements
- security clearance
- certifications

Only include requirements that are actually present
or clearly stated in the job description.

experience_match:
Compare the candidate's actual professional experience
against the company's experience requirement.

recommendation:
Give a concise practical recommendation.

Examples:

"Strong match - apply"
"Good junior opportunity - apply"
"Possible match - apply if willing to learn"
"Low match - consider other roles"
"Not recommended"

explanation:
Maximum 2 concise sentences explaining the main reason
for the score.

Do not repeat the entire job description.


============================================================
STRICT OUTPUT RULES
============================================================

Return exactly one result for every provided job.

Do NOT return a raw array.

Do NOT return markdown.

Do NOT add extra fields.

Do NOT omit required fields.

Do NOT generate:

- title
- company
- location
- url

Those fields are added by the application from the original
JobPosting object.


============================================================
EXPECTED STRUCTURE
============================================================

{{
    "matches": [
        {{
            "job_id": "0",
            "match_score": 75,
            "matched_skills": [
                "Python",
                "Machine Learning"
            ],
            "missing_skills": [
                "AWS"
            ],
            "required_skills": [
                "Python",
                "Machine Learning",
                "AWS"
            ],
            "experience_requirement":
                "2+ years of professional ML experience",
            "seniority_requirement":
                "Junior / Mid-level",
            "eligibility_requirements": [
                "Fluent English"
            ],
            "experience_match":
                "Candidate has 0 years of professional ML experience",
            "recommendation":
                "Possible match - apply if willing to learn",
            "explanation":
                "The candidate has strong core ML skills but lacks the required professional experience."
        }}
    ]
}}
"""


    response = client.beta.chat.completions.parse(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert technical recruiter. "
                    "Analyze every provided job carefully. "
                    "Return exactly one structured result "
                    "for every job. "
                    "The output must be an object containing "
                    "a matches array."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],

        response_format=JobMatchesLLM,

        max_completion_tokens=MAX_COMPLETION_TOKENS,
    )


    result = response.choices[0].message.parsed

    if result is None:
        raise ValueError(
            "LLM did not return a valid JobMatchesLLM result."
        )

    if len(result.matches) != len(jobs):

        raise ValueError(
            "LLM returned an incorrect number of job matches. "
            f"Expected {len(jobs)}, "
            f"received {len(result.matches)}."
        )



    enriched_matches = []

    seen_job_ids = set()


    for match in result.matches:



        try:

            absolute_job_id = int(
                match.job_id
            )

        except ValueError:

            raise ValueError(
                f"Invalid job_id returned by LLM: "
                f"{match.job_id}"
            )



        if match.job_id in seen_job_ids:

            raise ValueError(
                f"Duplicate job_id returned by LLM: "
                f"{match.job_id}"
            )

        seen_job_ids.add(
            match.job_id
        )


        job_index = (
            absolute_job_id
            - start_index
        )


        if (
            job_index < 0
            or job_index >= len(jobs)
        ):

            raise ValueError(
                f"job_id {match.job_id} "
                f"is outside the current batch."
            )



        job = jobs[job_index]



        enriched_match = JobMatch(

            # LLM data
            job_id=match.job_id,

            match_score=match.match_score,

            matched_skills=(
                match.matched_skills
            ),

            missing_skills=(
                match.missing_skills
            ),

            required_skills=(
                match.required_skills
            ),

            experience_requirement=(
                match.experience_requirement
            ),

            seniority_requirement=(
                match.seniority_requirement
            ),

            eligibility_requirements=(
                match.eligibility_requirements
            ),

            experience_match=(
                match.experience_match
            ),

            recommendation=(
                match.recommendation
            ),

            explanation=(
                match.explanation
            ),

            # Original JobPosting data
            title=job.title,

            company=job.company,

            location=job.location,

            url=job.url,
        )


        enriched_matches.append(
            enriched_match
        )


    if len(enriched_matches) != len(jobs):

        raise ValueError(
            "Enriched result count does not match "
            "the number of jobs in the batch."
        )


    return enriched_matches


def analyze_jobs(
    analysis: JobAnalysis,
    jobs: list[JobPosting],
) -> JobMatches:

    all_matches = []

    total_jobs = len(jobs)


    for start in range(
        0,
        total_jobs,
        BATCH_SIZE,
    ):

        batch = jobs[
            start:start + BATCH_SIZE
        ]


        print(
            f"Analyzing jobs "
            f"{start + 1}-{start + len(batch)} "
            f"of {total_jobs}..."
        )


        batch_matches = _analyze_batch(

            analysis=analysis,

            jobs=batch,

            start_index=start,
        )



        all_matches.extend(
            batch_matches
        )


    return JobMatches(
        matches=all_matches
    )
