from crewai import Agent


def create_requirements_agent(llm):
    return Agent(
        role="Admission Requirements Checker",
        goal="Check and explain the admission requirements provided by the user.",
        backstory=(
            "You analyze university admission requirements. "
            "Use only the information provided by the user. "
            "Never invent requirements."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False
    )
