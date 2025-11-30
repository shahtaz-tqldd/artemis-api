from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from trading_agent.sub_agents.performance_review_agent import create_performance_review_agent
from trading_agent.sub_agents.trade_news_agent import create_trade_news_agent

def create_root_agent() -> Agent:
    """
    Creates the root trading assistant agent (chat-only, no autonomous execution).
    User connects account or uploads history → asks questions → agent analyzes and advises.
    """
    
    llm_model = "gemini-2.0-flash"
    instruction = (
        "You are the root agent of Trading Assistant Agent specialized in Forex trading. "
        "Your job is to delegate specific tasks to the specialized sub-agents "
        "You have access to the following sub-agents:\n"
        "1. performance_review_agent: Analyzes closed trade history and market conditions to review performance.\n\n"
        "You have access to the following tools:\n"
        "1. trade_news_agent: Delivers updated news about forex trading.\n\n"
    )

    
    #  sub-agents
    performance_review_agent = create_performance_review_agent()
    trade_news_agent = create_trade_news_agent()

    return Agent(
        name="Forex_Assistant_Root",
        description="Professional chat-only Forex trading assistant with specialized sub-agents for analysis and advice.",
        model=llm_model,
        instruction=instruction,
        sub_agents=[
            performance_review_agent
        ],
        tools= [
            AgentTool(trade_news_agent)
        ]
    )