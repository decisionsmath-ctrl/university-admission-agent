from crewai import Agent


def create_recommendation_agent(llm):
    return Agent(
        role="Program Recommendation Agent",
        goal="Identify programs that match the applicant's background and interests.",
        backstory=(
            "You analyze the applicant's academic background, "
            "interests and program information to identify suitable "
            "programs. Do not invent programs or requirements."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False
    )
