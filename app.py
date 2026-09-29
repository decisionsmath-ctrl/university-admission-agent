import streamlit as st

from admission_crew import run_admission_agents


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="University Admission Agent",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🎓 University Admission Agent")

st.write(
    "Analyze university admission requirements, "
    "check eligibility, and get program recommendations."
)


# ============================================================
# STUDENT INFORMATION
# ============================================================

st.header("Student Information")

student_name = st.text_input(
    "Student Name"
)

degree = st.text_input(
    "Current / Previous Degree",
    placeholder="e.g. BS Mathematics"
)

cgpa = st.text_input(
    "CGPA",
    placeholder="e.g. 3.73"
)

academic_background = st.text_area(
    "Academic Background",
    placeholder="Describe your academic background."
)

interests = st.text_area(
    "Research / Academic Interests",
    placeholder="e.g. AI, Machine Learning, Optimization"
)

skills = st.text_area(
    "Skills",
    placeholder="e.g. Python, Machine Learning, Data Analysis"
)


# ============================================================
# PROGRAM INFORMATION
# ============================================================

st.header("University Program Information")

program_information = st.text_area(
    "Paste University / Program Information",
    height=250,
    placeholder=(
        "Paste the university program information here, "
        "including degree requirements, CGPA, prerequisites, "
        "and other stated admission requirements."
    )
)


# ============================================================
# ANALYZE
# ============================================================

if st.button("🔍 Analyze Admission", use_container_width=True):

    if not degree or not program_information:

        st.warning(
            "Please provide at least the student's degree "
            "and the university program information."
        )

    else:

        student_profile = f"""
Student Name: {student_name}

Degree: {degree}

CGPA: {cgpa}

Academic Background:
{academic_background}

Interests:
{interests}

Skills:
{skills}
"""

        with st.spinner(
            "Running Requirements, Eligibility, and Recommendation agents..."
        ):

            try:

                (
                    requirements_result,
                    eligibility_result,
                    recommendation_result
                ) = run_admission_agents(
                    student_profile,
                    program_information
                )

                # ====================================================
                # RESULTS
                # ====================================================

                st.success("Analysis completed.")

                st.header("📋 Admission Requirements")

                st.write(requirements_result)

                st.header("✅ Eligibility Assessment")

                st.write(eligibility_result)

                st.header("🎯 Program Recommendations")

                st.write(recommendation_result)

            except Exception as error:

                st.error("An error occurred while running the agents.")

                st.exception(error)
