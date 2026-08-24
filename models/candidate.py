from pydantic import BaseModel, Field


class Experience(BaseModel):
    role: str = Field(
        description="Job title or role"
    )

    company: str | None = Field(
        default=None,
        description="Company or organization name"
    )

    years: float | None = Field(
        default=None,
        description="Number of years of experience"
    )

    description: str | None = Field(
        default=None,
        description="Short description of responsibilities or achievements"
    )


class Education(BaseModel):
    degree: str = Field(
        description="Degree name"
    )

    field: str | None = Field(
        default=None,
        description="Field of study"
    )

    institution: str | None = Field(
        default=None,
        description="University or educational institution"
    )


class CandidateProfile(BaseModel):

    possible_roles: list[str] = Field(
        default_factory=list,
        description="Job roles that are reasonably supported by the CV"
    )

    skills: list[str] = Field(
        default_factory=list,
        description="Skills explicitly supported by the CV"
    )

    experience: list[Experience] = Field(
        default_factory=list,
        description="Work experience"
    )

    education: list[Education] = Field(
        default_factory=list,
        description="Educational background"
    )

    locations: list[str] = Field(
        default_factory=list,
        description="Locations mentioned in the CV"
    )