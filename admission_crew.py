
            "GROQ_API_KEY is missing. "
            "Please add it to Streamlit Cloud Secrets."
        )

    return LLM(
        model="groq/openai/gpt-oss-20b",
        api_key=api_key,
        temperature=0.2
    )


# ============================================================
# REQUIREMENTS AGENT
# ============================================================

def run_requirements_agent(student_profile, program_information):

    llm = create_llm()

    agent = create_requirements_agent(llm)

    task = Task(
        description=f"""
Analyze the supplied university program information.

PROGRAM INFORMATION:
{program_information}

Identify:

1. Required degree
2. Minimum CGPA
3. English language requirement
4. Required subjects or prerequisites
5. Other stated admission requirements

Rules:

- Only use information supplied above.
- Do not invent requirements.
- If information is missing, write "Not provided".
- Give a clear and structured answer.
""",

        expected_output="""
A structured admission requirements report containing:

- Required degree
- Minimum CGPA
- English requirement
- Prerequisites
- Other requirements
- Missing or unspecified requirements
""",

        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()

    return result


# ============================================================
# ELIGIBILITY AGENT
# ============================================================

def run_eligibility_agent(student_profile, program_information):

    llm = create_llm()

    agent = create_eligibility_agent(llm)

    task = Task(
        description=f"""
Evaluate the applicant against the supplied program requirements.

APPLICANT PROFILE:
{student_profile}

PROGRAM INFORMATION:
{program_information}

Evaluate:

1. Degree requirement
2. CGPA requirement
3. English requirement
4. Academic prerequisites
5. Other stated requirements

For each requirement, classify it as:

- Satisfied
- Not satisfied
- Cannot determine

Then provide an overall status:

- Eligible based on supplied information
- Not eligible based on supplied information
- Needs verification

Rules:

- Do not assume missing information is satisfied.
- Do not claim official university admission.
- Use only the information supplied above.
""",

        expected_output="""
A structured eligibility assessment containing:

- Requirement
- Applicant information
- Status
- Explanation

Then provide an overall eligibility status.
""",

        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()

    return result


# ============================================================
# RECOMMENDATION AGENT
# ============================================================

def run_recommendation_agent(student_profile, program_information):

    llm = create_llm()

    agent = create_recommendation_agent(llm)

    task = Task(
        description=f"""
Identify suitable programs for the applicant using only
the information supplied.

APPLICANT PROFILE:
{student_profile}

PROGRAM INFORMATION:
{program_information}

Consider:

- Degree background
- Academic background
- CGPA
- Interests
- Skills
- Program field

For each suitable program, explain why it matches the applicant.

Rules:

- Do not invent universities.
- Do not invent programs.
- Do not invent admission requirements.
- Use only supplied information.
""",

        expected_output="""
A concise program recommendation report containing:

- University
- Program
- Why the program matches the applicant
""",

        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()

    return result


# ============================================================
# RUN ALL THREE AGENTS
# ============================================================

def run_admission_agents(student_profile, program_information):

    """
    Run the three independent CrewAI agents concurrently.

    Each agent has its own Crew and Task.

    No agent depends on another agent's output.
    """

    with ThreadPoolExecutor(max_workers=3) as executor:

        requirements_future = executor.submit(
            run_requirements_agent,
            student_profile,
            program_information
        )

        eligibility_future = executor.submit(
            run_eligibility_agent,
            student_profile,
            program_information
        )

        recommendation_future = executor.submit(
            run_recommendation_agent,
            student_profile,
            program_information
        )

        requirements_result = requirements_future.result()

        eligibility_result = eligibility_future.result()

        recommendation_result = recommendation_future.result()

    return (
        requirements_result,
        eligibility_result,
        recommendation_result
    )
