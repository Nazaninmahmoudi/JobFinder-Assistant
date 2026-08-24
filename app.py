import textwrap
import streamlit as st

from cv.parser import parse_cv
from agents.job_analyzer import analyze_for_position
from agents.job_search_agent import search_jobs_for_candidate
from agents.job_llm_ranker import analyze_jobs


st.set_page_config(
    page_title="JobMatch AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)


PRIMARY = "#10B981"
PRIMARY_HOVER = "#059669"

BACKGROUND = "#090D0B"
CARD = "#111815"
CARD_2 = "#18221D"

BORDER = "#23322B"
BORDER_LIGHT = "#2E4239"

TEXT = "#F3F4F6"
TEXT_SECONDARY = "#9CA3AF"
TEXT_MUTED = "#6B7280"

MATCH_BG = "#064E3B"
MATCH_TEXT = "#34D399"

MISSING_BG = "#881337"
MISSING_TEXT = "#FDA4AF"

REQUIRED_BG = "#1E293B"
REQUIRED_BORDER = "#334155"
REQUIRED_TEXT = "#93C5FD"

RECOMMENDATION_BG = "#362B0D"
RECOMMENDATION_BORDER = "#715113"
RECOMMENDATION_TEXT = "#FCD34D"

COUNTRIES = [
    "Germany",
    "United States",
    "United Kingdom",
    "Netherlands",
    "Canada",
    "France",
    "Spain",
    "Italy",
    "Switzerland",
]



st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BACKGROUND};
    }}

    [data-testid="stAppViewContainer"] {{
        background: {BACKGROUND};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    footer, #MainMenu {{
        visibility: hidden;
    }}

    .block-container {{
        max-width: 1140px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }}

    body, p, label {{
        color: {TEXT};
    }}

    [data-testid="stWidgetLabel"] p {{
        color: {TEXT} !important;
        font-weight: 600;
        font-size: 14px;
    }}

    /* Input Fields Neutral Styling */
    .stTextInput input, 
    .stNumberInput input,
    div[data-baseweb="select"] > div,
    div[data-baseweb="popover"] {{
        background-color: {CARD_2} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 10px !important;
    }}

    div[data-baseweb="select"] * {{
        background-color: transparent !important;
        color: {TEXT} !important;
    }}

    /* File Uploader Neutral Theme */
    [data-testid="stFileUploader"] section {{
        background-color: {CARD_2} !important;
        border: 1px dashed {BORDER_LIGHT} !important;
        border-radius: 12px !important;
    }}

    [data-testid="stFileUploader"] section:hover {{
        border-color: {TEXT_SECONDARY} !important;
    }}

    [data-testid="stFileUploader"] section * {{
        color: {TEXT_SECONDARY} !important;
    }}

    /* Brand Header */
    .brand {{
        font-size: 28px;
        font-weight: 800;
        color: {TEXT};
        margin-bottom: 24px;
        letter-spacing: -0.5px;
    }}

    .brand-accent {{
        color: {PRIMARY};
    }}

    /* Hero Section */
    .hero-title {{
        font-size: 40px;
        font-weight: 800;
        color: {TEXT};
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }}

    .hero-subtitle {{
        font-size: 16px;
        color: {TEXT_SECONDARY};
        text-align: center;
        margin-bottom: 36px;
    }}

    /* Buttons */
    .stButton > button {{
        min-height: 45px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease;
    }}

    .stButton > button[type="primary"] {{
        background: {PRIMARY} !important;
        color: white !important;
        border: none !important;
    }}

    .stButton > button[type="primary"]:hover {{
        background: {PRIMARY_HOVER} !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
    }}

    .stButton > button[type="secondary"] {{
        background: {CARD_2} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
    }}

    .stButton > button[type="secondary"]:hover {{
        border-color: {PRIMARY} !important;
        color: {PRIMARY} !important;
    }}

    /* Dashboard Stats */
    .stat-box {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }}

    .stat-number {{
        font-size: 32px;
        font-weight: 800;
        color: {TEXT};
    }}

    .stat-label {{
        font-size: 13px;
        color: {TEXT_SECONDARY};
        margin-top: 4px;
        font-weight: 500;
    }}

    /* Job Card Styling */
    .job-title {{
        font-size: 22px;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 6px;
    }}

    .job-company {{
        font-size: 15px;
        color: {TEXT_SECONDARY};
        margin-bottom: 4px;
    }}

    .job-location {{
        font-size: 13px;
        color: {TEXT_MUTED};
    }}

    .score {{
        font-size: 32px;
        font-weight: 800;
        text-align: right;
    }}

    .score-high {{ color: {MATCH_TEXT}; }}
    .score-medium {{ color: #FBBF24; }}
    .score-low {{ color: {MISSING_TEXT}; }}

    .score-label {{
        color: {TEXT_MUTED};
        font-size: 12px;
        text-align: right;
    }}

    /* Tags */
    .tag {{
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 4px 6px 4px 0;
    }}

    .tag-match {{
        background: {MATCH_BG};
        color: {MATCH_TEXT};
        border: 1px solid #065F46;
    }}

    .tag-missing {{
        background: {MISSING_BG};
        color: {MISSING_TEXT};
        border: 1px solid #9F1239;
    }}

    .tag-required {{
        background: {REQUIRED_BG};
        color: {REQUIRED_TEXT};
        border: 1px solid {REQUIRED_BORDER};
    }}

    /* Requirements & Cards */
    .requirement-card {{
        background: {CARD_2};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }}

    .requirement-label {{
        font-size: 14px;
        font-weight: 700;
        color: #E5E7EB;
        margin-bottom: 8px;
    }}

    .requirement-value {{
        font-size: 13px;
        line-height: 1.6;
        color: {TEXT_SECONDARY};
    }}

    .recommendation-box {{
        background: {RECOMMENDATION_BG};
        border: 1px solid {RECOMMENDATION_BORDER};
        border-radius: 12px;
        padding: 16px;
        margin-top: 16px;
    }}

    .recommendation-text {{
        color: {RECOMMENDATION_TEXT};
        font-size: 14px;
        font-weight: 600;
    }}

    .explanation {{
        color: {TEXT_SECONDARY};
        font-size: 14px;
        line-height: 1.6;
        margin-top: 14px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="brand">
        Job<span class="brand-accent">Match</span> AI
    </div>
    """,
    unsafe_allow_html=True,
)


if "ranked_matches" not in st.session_state:

    st.markdown(
        """
        <div class="hero-title">Find jobs that actually match you</div>
        <div class="hero-subtitle">Upload your CV, select target options, and let AI rank top opportunities.</div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_cv = st.file_uploader(
        "CV / Resume",
        type=["pdf"],
        help="Upload your CV as a PDF.",
    )

    col1, col2 = st.columns(2)

    with col1:
        target_position = st.text_input(
            "Job title",
            placeholder="Machine Learning Engineer",
        )

    with col2:
        location = st.selectbox(
            "Location",
            COUNTRIES,
            index=0,
        )

    col3, col4 = st.columns(2)

    with col3:
        number_of_jobs = st.number_input(
            "Jobs to analyze",
            min_value=1,
            max_value=50,
            value=15,
            step=1,
        )

    with col4:
        job_type = st.multiselect(
            "Job type",
            options=[
                "Full-time",
                "Part-time",
                "Internship",
                "Working student",
            ],
            default=["Full-time", "Working student"],
            placeholder="Select job types...",
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    search = st.button(
        "🔎 Search & Match Jobs",
        type="primary",
        use_container_width=True,
    )

    if search:
        if uploaded_cv is None:
            st.error("Please upload your CV.")
            st.stop()

        if not target_position.strip():
            st.error("Please enter a job title.")
            st.stop()

        cv_path = "uploaded_cv.pdf"

        with open(cv_path, "wb") as f:
            f.write(uploaded_cv.getbuffer())

        try:
            with st.spinner("Analyzing CV..."):
                profile = parse_cv(cv_path)

            with st.spinner("Building profile..."):
                analysis = analyze_for_position(
                    profile=profile,
                    target_position=target_position.strip(),
                )

            with st.spinner("Searching jobs..."):
                country_code_map = {
                    "Germany": "de",
                    "United States": "us",
                    "United Kingdom": "gb",
                    "Netherlands": "nl",
                    "Canada": "ca",
                    "France": "fr",
                    "Spain": "es",
                    "Italy": "it",
                    "Switzerland": "ch",
                }
                c_code = country_code_map.get(location, "de")
                jobs = search_jobs_for_candidate(
                    profile=profile,
                    analysis=analysis,
                    country=c_code,
                )

            if not jobs:
                st.warning("No jobs were found.")
                st.stop()

            jobs_for_ranking = jobs[: int(number_of_jobs)]

            with st.spinner(f"Matching {len(jobs_for_ranking)} jobs (Handling Rate Limits automatically)..."):
                job_matches = analyze_jobs(
                    analysis=analysis,
                    jobs=jobs_for_ranking,
                )

            ranked_matches = sorted(
                job_matches.matches,
                key=lambda x: x.match_score,
                reverse=True,
            )

            st.session_state["ranked_matches"] = ranked_matches
            st.session_state["target_position"] = target_position.strip()
            st.session_state["location"] = location
            st.session_state["job_type"] = job_type

            st.rerun()

        except Exception as e:
            st.error(f"Error occurred: {e}")
            st.exception(e)
            st.stop()


else:
    ranked_matches = st.session_state["ranked_matches"]
    target_position = st.session_state["target_position"]

    top_col1, top_col2 = st.columns([4, 1])

    with top_col1:
        st.markdown(
            f"""
            <div class="job-title" style="font-size:32px; margin-bottom:4px;">
                {target_position}
            </div>
            <div style="color:{TEXT_SECONDARY}; font-size:14px; margin-bottom:24px;">
                AI-ranked matches in {st.session_state['location']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_col2:
        if st.button("🔄 New Search", type="secondary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    total = len(ranked_matches)
    strong = sum(1 for x in ranked_matches if x.match_score >= 70)
    medium = sum(1 for x in ranked_matches if 50 <= x.match_score < 70)
    weak = sum(1 for x in ranked_matches if x.match_score < 50)

    stats_html = textwrap.dedent(f"""
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:16px; margin-bottom:28px;">
            <div class="stat-box">
                <div class="stat-number">{total}</div>
                <div class="stat-label">Analyzed</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" style="color:{MATCH_TEXT}">{strong}</div>
                <div class="stat-label">Strong Matches</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" style="color:#FBBF24">{medium}</div>
                <div class="stat-label">Potential Matches</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" style="color:{MISSING_TEXT}">{weak}</div>
                <div class="stat-label">Low Matches</div>
            </div>
        </div>
    """)

    st.markdown(stats_html, unsafe_allow_html=True)

    f1, f2 = st.columns([1, 3])

    with f1:
        minimum_score = st.selectbox(
            "Minimum match",
            ["All", "50%+", "60%+", "70%+", "80%+"],
        )

    with f2:
        search_text = st.text_input(
            "Search results",
            placeholder="Filter by title or company name...",
        )

    filtered_matches = ranked_matches

    if minimum_score != "All":
        minimum = int(minimum_score.replace("%+", ""))
        filtered_matches = [
            x for x in filtered_matches if x.match_score >= minimum
        ]

    if search_text.strip():
        query = search_text.lower()
        filtered_matches = [
            x
            for x in filtered_matches
            if query in x.title.lower() or query in x.company.lower()
        ]

    st.markdown(
        f"""
        <div style="color:{TEXT_SECONDARY}; font-size:14px; margin:20px 0 12px 0; font-weight: 500;">
            Showing <b>{len(filtered_matches)}</b> positions
        </div>
        """,
        unsafe_allow_html=True,
    )

    for match in filtered_matches:
        with st.container():
            left, score_col = st.columns([5, 1])

            with left:
                st.markdown(
                    textwrap.dedent(f"""
                        <div class="job-title">{match.title}</div>
                        <div class="job-company">🏢 {match.company}</div>
                        <div class="job-location">📍 {match.location}</div>
                    """),
                    unsafe_allow_html=True,
                )

            with score_col:
                if match.match_score >= 70:
                    score_class = "score-high"
                elif match.match_score >= 50:
                    score_class = "score-medium"
                else:
                    score_class = "score-low"

                st.markdown(
                    textwrap.dedent(f"""
                        <div class="score {score_class}">{match.match_score:.0f}%</div>
                        <div class="score-label">match score</div>
                    """),
                    unsafe_allow_html=True,
                )

            st.progress(min(int(match.match_score), 100))

            if match.url:
                st.link_button("View Job Opening ↗", match.url)

            if match.matched_skills:
                skills_html = "".join(
                    [
                        f'<span class="tag tag-match">✓ {skill}</span>'
                        for skill in match.matched_skills
                    ]
                )
                st.markdown(
                    textwrap.dedent(f"""
                        <div style="font-weight:700; margin-top:16px; margin-bottom:6px; font-size:14px;">Matching Skills</div>
                        <div>{skills_html}</div>
                    """),
                    unsafe_allow_html=True,
                )

            if match.missing_skills:
                skills_html = "".join(
                    [
                        f'<span class="tag tag-missing">✕ {skill}</span>'
                        for skill in match.missing_skills
                    ]
                )
                st.markdown(
                    textwrap.dedent(f"""
                        <div style="font-weight:700; margin-top:12px; margin-bottom:6px; font-size:14px;">Missing Skills</div>
                        <div>{skills_html}</div>
                    """),
                    unsafe_allow_html=True,
                )

            st.markdown(
                '<div style="font-weight:700; margin-top:20px; margin-bottom:10px; font-size:15px;">Requirements Overview</div>',
                unsafe_allow_html=True,
            )

            education = getattr(match, "education", None)
            if education:
                st.markdown(
                    textwrap.dedent(f"""
                        <div class="requirement-card">
                            <div class="requirement-label">🎓 Education</div>
                            <div class="requirement-value">{education}</div>
                        </div>
                    """),
                    unsafe_allow_html=True,
                )

            if match.experience_requirement:
                st.markdown(
                    textwrap.dedent(f"""
                        <div class="requirement-card">
                            <div class="requirement-label">💼 Experience</div>
                            <div class="requirement-value">{match.experience_requirement}</div>
                        </div>
                    """),
                    unsafe_allow_html=True,
                )

            if match.required_skills:
                skills_html = "".join(
                    [
                        f'<span class="tag tag-required">{skill}</span>'
                        for skill in match.required_skills
                    ]
                )
                st.markdown(
                    textwrap.dedent(f"""
                        <div class="requirement-card">
                            <div class="requirement-label">🛠 Required Skills</div>
                            <div class="requirement-value">{skills_html}</div>
                        </div>
                    """),
                    unsafe_allow_html=True,
                )

            if match.eligibility_requirements:
                eligibility_html = "<br>".join(
                    [f"• {item}" for item in match.eligibility_requirements]
                )
                st.markdown(
                    textwrap.dedent(f"""
                        <div class="requirement-card">
                            <div class="requirement-label">📋 Eligibility</div>
                            <div class="requirement-value">{eligibility_html}</div>
                        </div>
                    """),
                    unsafe_allow_html=True,
                )

            if match.recommendation:
                st.markdown(
                    textwrap.dedent(f"""
                        <div class="recommendation-box">
                            <span class="recommendation-text">💡 {match.recommendation}</span>
                        </div>
                    """),
                    unsafe_allow_html=True,
                )

            if match.explanation:
                st.markdown(
                    textwrap.dedent(f"""
                        <div class="explanation">{match.explanation}</div>
                    """),
                    unsafe_allow_html=True,
                )

            st.markdown("<hr style='border-color: #23322B; margin: 30px 0;'>", unsafe_allow_html=True)