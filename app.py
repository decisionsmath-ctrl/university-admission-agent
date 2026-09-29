import streamlit as st

from admission_crew import run_admission_agents



# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="University Admission Agent",
    page_icon="🎓",
    layout="wide"
)


# =====================================================
# HEADER
# =====================================================

st.title("🎓 University Admission Agent")

st.write(
    "A simple multi-agent system for admission requirements, "
    "eligibility evaluation and program recommendations."
)

st.info(
    "Three independent AI agents analyze the same applicant "
    "and program information."
)


# =====================================================
# APPLICANT INFORMATION
# =====================================================

st.header("👤 Applicant Information")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Name",
        placeholder="Enter applicant name"
    )

    degree = st.text_input(
        "Degree",
        placeholder="e.g. BS Mathematics"
    )

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=4.0,
        value=3.0,
        step=0.01
    )

    english = st.text_input(
        "English Test / Score",
        placeholder="e.g. IELTS 7.0"
    )


with col2:

    interests = st.text_area(
        "Academic / Career Interests",
        placeholder=(
            "e.g. AI, Machine Learning, "
            "Data Science, Optimization"
        )
    )

    background = st.text_area(
        "Academic Background",
        placeholder=(
            "e.g. Calculus, Linear Algebra, "
            "Statistics, Python, Optimization"
        )
    )


# =====================================================
# PROGRAM INFORMATION
# =====================================================

st.header("🎓 Program Information")

university = st.text_input(
    "University",
    placeholder="e.g. Demo University"
)

program = st.text_input(
    "Program",
    placeholder="e.g. MS Artificial Intelligence"
)

requirements = st.text_area(
    "Admission Requirements",
    height=220,
    placeholder="""Example:

Minimum CGPA: 3.0
Degree: Mathematics, Computer Science or related field
English: IELTS 6.5
Prerequisites: Linear Algebra, Statistics, Programming
Other requirements: CV and Statement of Purpose
"""
)


# =====================================================
# ANALYZE BUTTON
# =====================================================

if st.button(
    "🔍 Analyze Admission",
    type="primary",
    use_container_width=True
):

    # -----------------------------------------------
    # BASIC VALIDATION
    # -----------------------------------------------

    if not degree:

        st.error("Please enter the applicant's degree.")

    elif not university:

        st.error("Please enter the university.")

    elif not program:

        st.error("Please enter the program.")

    elif not requirements:

        st.error("Please enter the admission requirements.")

    else:

        # -------------------------------------------
        # CREATE APPLICANT PROFILE
        # -------------------------------------------

        student_profile = f"""
        Name:
        {name}

        Degree:
        {degree}

        CGPA:
        {cgpa}

        English Test / Score:
        {english}

        Academic / Career Interests:
        {interests}

        Academic Background:
        {background}
        """

        # -------------------------------------------
        # CREATE PROGRAM INFORMATION
        # -------------------------------------------

        program_information = f"""
        University:
        {university}

        Program:
        {program}

        Admission Requirements:
        {requirements}
        """

        # -------------------------------------------
        # RUN AGENTS
        # -------------------------------------------

        try:

            with st.spinner(
                "Running the three independent agents..."
            ):

                result = run_admission_agents(
                    student_profile,
                    program_information
                )

            st.success(
                "Analysis completed."
            )

            # ---------------------------------------
            # DISPLAY RESULTS
            # ---------------------------------------

            st.header("📊 Agent Results")

            if hasattr(result, "tasks_output"):

                outputs = result.tasks_output

                # Requirements
                if len(outputs) >= 1:

                    with st.expander(
                        "1️⃣ Requirements Agent",
                        expanded=True
                    ):

                        st.markdown(
                            outputs[0].raw
                        )

                # Eligibility
                if len(outputs) >= 2:

                    with st.expander(
                        "2️⃣ Eligibility Agent",
                        expanded=True
                    ):

                        st.markdown(
                            outputs[1].raw
                        )

                # Recommendation
                if len(outputs) >= 3:

                    with st.expander(
                        "3️⃣ Recommendation Agent",
                        expanded=True
                    ):

                        st.markdown(
                            outputs[2].raw
                        )

            else:

                st.write(result)

        except Exception as error:

            st.error(
                "The application could not complete the analysis."
            )

            st.exception(error)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "AI-assisted assessment only. Always verify final "
    "admission requirements with the official university."
)
