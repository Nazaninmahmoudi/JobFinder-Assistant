import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

from models.candidate import CandidateProfile


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


class JobAnalysis(BaseModel):

    target_position: str = Field(
        description="The job position selected by the user"
    )

    relevant_skills: list[str] = Field(
        default_factory=list,
        description="Skills from the CV that are relevant to the target position"
    )

    relevant_experience_years: float = Field(
        default=0,
        description="Estimated years of professional experience directly relevant to the target position"
    )

    seniority: str = Field(
        description="Estimated seniority for the target position, such as Entry-level, Junior, Mid-level, or Senior"
    )

    search_keywords: list[str] = Field(
        default_factory=list,
        description="Job titles and search keywords that should be used to find relevant jobs"
    )

    explanation: str = Field(
        description="Short explanation of why the candidate matches or does not match the target position"
    )


def analyze_for_position(
    profile: CandidateProfile,
    target_position: str
) -> JobAnalysis:

    prompt = f"""
You are an expert career and recruitment analyst.

Analyze the candidate's CV specifically for the target job position.

TARGET POSITION:
{target_position}

CANDIDATE PROFILE:
{profile.model_dump_json(indent=2)}

Important rules:

- Evaluate the candidate specifically for the target position.
- Do not assume that all work experience is relevant.
- Only count professional experience that is directly relevant to the target position.
- Teaching experience should not automatically be treated as professional industry experience.
- Skills should only be considered relevant when they have a reasonable connection to the target position.
- Determine seniority based on relevant experience, relevant skills, responsibilities, and the requirements normally expected for the target position.

- Generate 3 to 6 highly relevant search terms and alternative job titles.
- Search terms must remain closely related to the user's target position.
- Do not turn individual skills into unrelated job titles.
- For example, if the target position is "ML", do not generate "SQL Engineer",
  "Python Engineer", or "Vector Database Engineer" unless they are genuinely
  recognized alternative titles for the target position.
- Use the candidate's skills to improve the search terms, but do not change
  the career direction selected by the user.

- Do not change the user's target position.
- If the candidate is a weak match, clearly explain why.
- Be conservative when estimating years of relevant professional experience.


Return the result according to the JobAnalysis schema.
"""

    response = client.beta.chat.completions.parse(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are an expert career and recruitment analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=JobAnalysis
    )

    return response.choices[0].message.parsed