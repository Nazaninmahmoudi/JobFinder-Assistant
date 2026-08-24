import os

import pymupdf
from dotenv import load_dotenv
from openai import OpenAI

from models.candidate import CandidateProfile


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF CV.
    """

    document = pymupdf.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def parse_cv(file_path: str) -> CandidateProfile:
    """
    Extract structured information from a CV.
    """

    cv_text = extract_text_from_pdf(file_path)

    if not cv_text.strip():
        raise ValueError("No text could be extracted from the CV.")

    prompt = f"""
You are an expert CV analyst.

Analyze the CV below and extract the candidate's professional profile.

You MUST return ALL fields required by the CandidateProfile schema.

Required fields:

1. possible_roles
2. skills
3. industry and research experiences
4. education 
5. locations

Important rules:

- Always return every field.
- Never omit a field.
- If a field has no information, return an empty list.
- Extract only information supported by the CV.
- Do not invent experience, skills, education, or locations.
- possible_roles should contain realistic job roles supported by the candidate's CV.
- Do not generate unrelated job roles.
- skills should contain relevant technical and professional skills supported by the CV.
- experience should contain the candidate's actual work experience.
- education should contain the candidate's actual educational background.
- locations should contain locations explicitly mentioned or clearly associated with the CV.
- Keep the extracted information concise.
- Do not add explanations outside the structured response.

CV:

{cv_text}
"""

    response = client.beta.chat.completions.parse(
        model="openai/gpt-oss-120b",
        messages=[
            {
    "role": "system",
    "content": """
You are a CV information extraction system.

You must always return a complete CandidateProfile.
Every required field must be present in the output,
even when its value is an empty list.
""",
},
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=CandidateProfile
    )

    return response.choices[0].message.parsed