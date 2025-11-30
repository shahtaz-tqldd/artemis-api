from google.adk.agents import Agent
from google.adk.tools import google_search
from app.core.config import get_settings

settings = get_settings()


def create_trade_news_agent() -> Agent:
    """
    Sub-agent specialized in delivering forex news.
    """

    llm_model = "gemini-2.0-flash"

    instruction = (
        "You are a Forex Trading News Agent. You will use google_search_tool and find latest news about forex trading and answer user queries"

        "Core rules:\n"
        "- You NEVER give trade recommendations, entries, stops, or price targets.\n"
        "- You NEVER express bullish/bearish bias unless directly quoting a central bank or official source.\n"
        "- Always mention the exact timestamp (UTC) of the news/event when known.\n\n"

        "If no significant news in the last 24h, simply say: "
        "'No high-impact forex news in the past 24 hours. Market currently quiet on fundamentals.'"
    )

    return Agent(
        name="trade_news_agent",
        description="An agent that deliver updated news about forex trading",
        model=llm_model,
        instruction=instruction,
        tools=[google_search],
    )
