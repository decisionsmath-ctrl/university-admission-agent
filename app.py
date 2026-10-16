import os

import streamlit as st


# ============================================================
# PAGE CONFIGURATION (must be the first Streamlit command)
# ============================================================

st.set_page_config(
    page_title="UniMatch AI | Admission Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD GROQ API KEY FROM STREAMLIT SECRETS
# ============================================================

try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    # No secrets file (e.g. running locally). create_llm() will show
    # a clear message if the key is missing.
    pass


# ============================================================
# IMPORT AGENTS (after the key is set)
# ============================================================

from admission_crew import run_admission_agents


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fb;
    }

    [data-testid="stHeader"] {
        background-color: rgba(245, 247, 251, 0.95);
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 2rem 2.2rem;
        border-radius: 20px;
        background: linear-gradient(120deg, #102a43, #176b87);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: white;
        font-size: 2.35rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        color: #e1edf5;
        font-size: 1rem;
        margin-bottom: 0;
    }

    .section-label {
        color: #176b87;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .info-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 1.1rem 1.25rem;
        margin-bottom: 1rem;
    }

    .info-card h4 {
        margin-top: 0;
        color: #102a43;
    }

    div.stButton > button[kind="primary"] {
        background: #176b87;
        border: none;
        border-radius: 10px;
        min-height: 3rem;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #12566d;
        border: none;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
    }

    .footer-note {
        color: #64748b;
        font-size: 0.83rem;
        text-align: center;
        padding-top: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🎓 UniMatch AI")
    st.caption("University Admission Intelligence")

    st.divider()

    st.markdown("### How it works")

    st.markdown(
        """
        **01 — Requirements**

        Extract stated admission criteria.

        **02 — Eligibility**

        Compare the student profile with those criteria.

        **03 — Recommendations**

        Identify matching programs from the supplied information.
        """
    )

    st.divider()

    st.markdown("### Before you begin")

    st.markdown(
        """
        - Enter your academic details.
        - Paste the official program information.
        - Review each agent's independent analysis.
        """
    )

    st.info(
        "This tool provides preliminary guidance, "
        "not an official admission decision."
    )


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="section-label" style="color:#9ee7f5;">
            SMARTER ACADEMIC PLANNING
        </div>
        <h1>Find Your Next Academic Opportunity</h1>
        <p>
            Analyze admission requirements, assess your eligibility,
            and discover suitable programs with three specialized agents.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OVERVIEW
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <h4>📋 Requirements</h4>
            <p>Identify stated degree, CGPA, and prerequisite criteria.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <h4>✓ Eligibility</h4>
            <p>Compare academic information against supplied criteria.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <h4>🎯 Recommendations</h4>
            <p>Find programs aligned with your background and interests.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# INPUT FORM
# ============================================================

st.markdown("## Build Your Student Profile")
st.caption(
    "Complete the fields below. Only your degree and program "
    "information are required to start an analysis."
)

with st.form("admission_analysis_form"):

    st.markdown("### 1. Academic Information")

    name_col, degree_col, cgpa_col = st.columns([1, 2, 1])

    with name_col:
        student_name = st.text_input(
            "Student name (optional)",
            placeholder="Your name"
        )

    with degree_col:
        degree = st.text_input(
            "Current / Previous Degree *",
            placeholder="e.g. BS Mathematics"
        )

    with cgpa_col:
        cgpa = st.text_input(
            "CGPA (optional)",
            placeholder="e.g. 3.73 / 4.00"
        )

    academic_background = st.text_area(
        "Academic Background (optional)",
        placeholder=(
            "Relevant courses, academic achievements, "
            "research experience, or previous qualifications..."
        ),
        height=110
    )

    st.markdown("### 2. Interests and Skills")

    interest_col, skills_col = st.columns(2)

    with interest_col:
        interests = st.text_area(
            "Research / Academic Interests",
            placeholder="e.g. Optimization, AI, Applied Mathematics",
            height=100
        )

    with skills_col:
        skills = st.text_area(
            "Technical and Academic Skills",
            placeholder="e.g. Python, Statistics, Data Analysis",
            height=100
        )

    st.markdown("### 3. University Program Information")

    st.caption(
        "Paste the available official information. You can include "
        "multiple programs, provided their details are clearly identified."
    )

    program_information = st.text_area(
        "Program details *",
        placeholder=(
            "University: [University name]\n"
            "Program: [Degree/program name]\n"
            "Required degree: ...\n"
            "Minimum CGPA: ...\n"
            "Prerequisites: ...\n"
            "Other admission conditions: ..."
        ),
        height=240
    )

    submitted = st.form_submit_button(
        "🔍 Analyze My Admission Options",
        type="primary",
        use_container_width=True
    )


# ============================================================
# VALIDATION AND AGENT EXECUTION
# ============================================================

if submitted:

    if not degree.strip():
        st.error("Please enter your current or previous degree.")

    elif not program_information.strip():
        st.error(
            "Please paste the university or program information "
            "before starting the analysis."
        )

    else:

        student_profile = f"""
STUDENT PROFILE

Name: {student_name.strip() or "Not provided"}

Degree: {degree.strip()}

CGPA: {cgpa.strip() or "Not provided"}

Academic Background:
{academic_background.strip() or "Not provided"}

Academic / Research Interests:
{interests.strip() or "Not provided"}

Skills:
{skills.strip() or "Not provided"}
"""

        st.markdown("---")
        st.markdown("## Your Admission Analysis")

        try:
            with st.spinner(
                "The three agents are analyzing your information. "
                "This may take a little time..."
            ):
                (
                    requirements_result,
                    eligibility_result,
                    recommendation_result
                ) = run_admission_agents(
                    student_profile,
                    program_information.strip()
                )

            st.success("All three agents returned their results.")

            tab1, tab2, tab3 = st.tabs(
                [
                    "📋 Requirements",
                    "✓ Eligibility",
                    "🎯 Recommendations"
                ]
            )

            with tab1:
                st.subheader("Admission Requirements")
                st.caption(
                    "Requirements identified from the information you supplied."
                )
                st.markdown(str(requirements_result))

            with tab2:
                st.subheader("Eligibility Assessment")
                st.caption(
                    "A preliminary comparison, not an official admission decision."
                )
                st.markdown(str(eligibility_result))

            with tab3:
                st.subheader("Program Recommendations")
                st.caption(
                    "Recommendations based only on the supplied program details."
                )
                st.markdown(str(recommendation_result))

            st.divider()

            st.download_button(
                label="⬇️ Download Analysis as Text",
                data=(
                    "UNIMATCH AI — ADMISSION ANALYSIS\n\n"
                    "STUDENT PROFILE\n"
                    f"{student_profile}\n\n"
                    "PROGRAM INFORMATION\n"
                    f"{program_information}\n\n"
                    "ADMISSION REQUIREMENTS\n"
                    f"{requirements_result}\n\n"
                    "ELIGIBILITY ASSESSMENT\n"
                    f"{eligibility_result}\n\n"
                    "PROGRAM RECOMMENDATIONS\n"
                    f"{recommendation_result}\n"
                ),
                file_name="unimatch_admission_analysis.txt",
                mime="text/plain"
            )

            st.caption(
                "Please verify admission criteria with the university's "
                "official admissions office before making decisions."
            )

        except Exception as error:
            st.error(
                "The analysis could not be completed. "
                "Check the application logs for the underlying error."
            )

            # Show the error to the developer for debugging.
            st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">
        UniMatch AI · Multi-Agent University Admission Assistant
        <br>
        Preliminary guidance only — always verify requirements with
        the relevant university.
    </div>
    """,
    unsafe_allow_html=True
)
