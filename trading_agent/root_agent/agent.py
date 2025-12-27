from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from trading_agent.sub_agents import (
    create_trade_history_analyzer_agent, 
    create_market_intelligence_agent
)

def create_root_agent(parsed_data) -> Agent:
    """
    Creates the root trading assistant agent
    """
    
    llm_model = "gemini-2.0-flash"
    instruction = (
        "You are the root agent of Trading Assistant Agent specialized in Forex trading. "
        "Your job is to delegate specific tasks to the specialized sub-agents "
    )

    
    #  sub-agents
    trade_history_analyzer_agent = create_trade_history_analyzer_agent(parsed_data)
    market_intelligence_agent = create_market_intelligence_agent()

    return Agent(
        name="root_trading_agent",
        description="A root agent for trading assistance that delegates task to it's specialized sub agents",
        model=llm_model,
        instruction=instruction,
        sub_agents=[
            trade_history_analyzer_agent
        ],
        tools=[
            AgentTool(market_intelligence_agent)
        ]
    )