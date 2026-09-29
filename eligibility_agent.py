from crewai import Agent


def create_eligibility_agent(llm):
    return Agent(
        role="Eligibility Evaluator",
        goal="Evaluate whether the applicant meets the supplied requirements.",
        backstory=(
            "You compare the applicant's qualifications with "
            "the admission requirements. "
            "Do not assume that missing information is satisfied."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False
    )
