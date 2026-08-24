from pydantic import BaseModel, Field


class JobPosting(BaseModel):

    title: str = Field(
        description="Job title"
    )

    company: str | None = Field(
        default=None,
        description="Company name"
    )

    location: str | None = Field(
        default=None,
        description="Job location"
    )

    description: str | None = Field(
        default=None,
        description="Job description"
    )

    url: str | None = Field(
        default=None,
        description="URL of the job posting"
    )

    salary_min: float | None = Field(
        default=None,
        description="Minimum salary if available"
    )

    salary_max: float | None = Field(
        default=None,
        description="Maximum salary if available"
    )

    contract_type: str | None = Field(
        default=None,
        description="Contract type if available"
    )

    category: str | None = Field(
        default=None,
        description="Job category"
    )