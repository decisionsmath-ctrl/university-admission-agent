import os

from crewai import Agent, Crew, LLM, Process, Task

from requirements_agent import create_requirements_agent
from eligibility_agent import create_eligibility_agent
from recommendation_agent import create_recommendation_agent


def create_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    return LLM(
        model="groq/openai/gpt-oss-20b",
        api_key=api_key,
        temperature=0.2
    )


def run_admission_agents(student_profile, program_information):

    llm = create_llm()

    # Create the three independent agents
    requirements_agent = create_requirements_agent(llm)
    eligibility_agent = create_eligibility_agent(llm)
    recommendation_agent = create_recommendation_agent(llm)

    # ------------------------------------------------
    # REQUIREMENTS TASK
    # ------------------------------------------------

    requirements_task = Task(
        description=f"""
        Analyze the following program information.

        PROGRAM INFORMATION:
        {program_information}

        Identify:
        - Required degree
        - Minimum CGPA
        - English requirement
        - Prerequisites
        - Other requirements

        Use only the supplied information.
        Do not invent requirements.
        """,

        expected_output=(
            "A clear explanation of the admission requirements."
        ),

        agent=requirements_agent,
        async_execution=True
    )

    # ------------------------------------------------
    # ELIGIBILITY TASK
    # ------------------------------------------------

    eligibility_task = Task(
        description=f"""
        Evaluate the applicant against the supplied requirements.

        APPLICANT:
        {student_profile}

        PROGRAM INFORMATION:
        {program_information}

        Determine:

        1. Requirements the applicant appears to satisfy.
        2. Requirements the applicant does not satisfy.
        3. Missing information.
        4. Overall status:
           - Eligible based on supplied information
           - Not eligible based on supplied information
           - Needs verification

        Do not claim official university admission.
        """,

        expected_output=(
            "A clear eligibility assessment with reasons."
        ),

        agent=eligibility_agent,
        async_execution=True
    )

    # ------------------------------------------------
    # RECOMMENDATION TASK
    # ------------------------------------------------

    recommendation_task = Task(
        description=f"""
        Analyze the applicant and the supplied program.

        APPLICANT:
        {student_profile}

        PROGRAM INFORMATION:
        {program_information}

        Consider:
        - Degree
        - CGPA
        - Academic background
        - Interests
        - Relevant skills
        - Program field

        Explain whether the program appears suitable.

        Do not invent programs or requirements.
        """,

        expected_output=(
            "A concise program suitability recommendation with reasons."
        ),

        agent=recommendation_agent,
        async_execution=True
    )

    # ------------------------------------------------
    # CREW
    # ------------------------------------------------

    crew = Crew(
        agents=[
            requirements_agent,
            eligibility_agent,
            recommendation_agent
        ],

        tasks=[
            requirements_task,
            eligibility_task,
            recommendation_task
        ],

        process=Process.sequential,

        verbose=False
    )

    return crew.kickoff()
