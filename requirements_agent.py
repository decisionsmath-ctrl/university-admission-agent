from crewai import Agent


def create_requirements Checker",
        goal="Check and explain ements_agent(llm):
    return Agent(
        role="Admission Requirthe admission requirements provided by the user.",
        backstory=(
            "You analyze university admission requirements. "
            "Use only the information provided by the user. "
            "Never invent requirements."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False
    )
