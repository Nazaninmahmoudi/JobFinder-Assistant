## Project Overview

The job finder system first extracts information from the provided CV, including skills, experience, education, and possible job roles. It then analyzes the candidate's profile for the selected position and generates relevant job search keywords. Using these keywords, the application retrieves job postings from the Adzuna API.
The final matching process combines rule-based scoring with a Groq LLM model. The rule-based ranker performs an initial evaluation using factors such as job title, search keywords, relevant skills, and seniority. The Groq LLM then compares the job requirements with the candidate's skills and experience, producing a match score, matched and missing skills, experience requirements, eligibility requirements, and a practical recommendation for each position. Finally, the jobs are ranked based on their match scores and presented through a Streamlit interface.

## Features

- **CV Parsing** — Extracts structured information such as skills, experience, education, locations, and possible job roles from PDF CVs.
- **Target Position Analysis** — Analyzes the candidate's profile specifically for the selected job position and identifies relevant skills, experience, seniority, and search keywords.
- **Job Search** — Retrieves job opportunities from the Adzuna API using multiple relevant search keywords.
- **Duplicate Removal** — Removes duplicate job postings using their URL or job details.
- **Rule-Based Job Scoring** — Performs an initial job evaluation based on job titles, keywords, relevant skills, and seniority.
- **LLM-Based Job Matching** — Uses a Groq-hosted LLM to compare candidate profiles with job requirements.
- **Detailed Match Analysis** — Identifies matched skills, missing skills, experience requirements, seniority, eligibility requirements, and recommendations.
- **Job Ranking** — Ranks job opportunities based on their final match scores.
- **Interactive Streamlit UI** — Provides an interface for uploading a CV, selecting a target position and location, and exploring ranked job opportunities.

## Requirements

Before running the project, make sure you have the following:

- Python 3.10 or higher
- A Groq API key
- An Adzuna API account with an App ID and App Key
- Git
- uv (recommended for dependency and environment management) 

## Installation

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nazaninmahmoudi/JobFinder-Assistant.git
cd JobFinder-Assistant
```

### 2. Create a virtual environment

```bash
uv venv
```

### 3. Install dependencies 

```bash
uv sync
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
```

### 5. Run the application

```bash
streamlit run app.py
```

### 6. Enjoy 


- ## Contact

If you have any questions or suggestions, feel free to reach out:

- Email: Nazaninmahmoudy@gmail.com
- LinkedIn: www.linkedin.com/in/nazanin-mahmoudi-495a3a247
- Kaggle: https://www.kaggle.com/nazaninmahmoudy


## License

This project is licensed under the MIT License.
