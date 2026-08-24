from pydantic import BaseModel, Field

class JobMatchLLM(BaseModel):

    job_id: str

    match_score: float = Field(
        ge=0,
        le=100
    )


    matched_skills: list[str] = Field(
        default_factory=list
    )

    missing_skills: list[str] = Field(
        default_factory=list
    )


    required_skills: list[str] = Field(
        default_factory=list
    )

    experience_requirement: str = ""

    seniority_requirement: str = ""

    eligibility_requirements: list[str] = Field(
        default_factory=list
    )


    experience_match: str = ""


    recommendation: str = ""

    explanation: str = ""


class JobMatchesLLM(BaseModel):

    matches: list[JobMatchLLM]


class JobMatch(BaseModel):

    job_id: str

    title: str

    company: str

    location: str

    url: str

    match_score: float


    matched_skills: list[str] = Field(
        default_factory=list
    )

    missing_skills: list[str] = Field(
        default_factory=list
    )

    required_skills: list[str] = Field(
        default_factory=list
    )



    experience_requirement: str = ""

    seniority_requirement: str = ""

    eligibility_requirements: list[str] = Field(
        default_factory=list
    )


    experience_match: str = ""


    recommendation: str = ""

    explanation: str = ""


class JobMatches(BaseModel):

    matches: list[JobMatch]