from google.adk.agents import Agent
from app.core.config import get_settings

settings = get_settings()


def create_performance_review_agent() -> Agent:
    """
    Sub-agent specialized in review performance based on close trade history and market conditions.
    """

    llm_model = "gemini-2.0-flash"

    instruction = (
        "You are a performance review agent for a forex trading system. Your task is to analyze closed trade history "

        "Core rules:\n"
        "- You will review performance based on provided trade history data.\n"
        "- If no trade history data is provided you will ask user to give that to you.\n"
    )

    return Agent(
        name="performance_review_agent",
        description="An agent that review performance based on closed trade history and market conditions.",
        model=llm_model,
        instruction=instruction,
        tools=[]
    )
