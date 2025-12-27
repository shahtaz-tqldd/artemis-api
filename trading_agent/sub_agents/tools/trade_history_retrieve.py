from google.adk.tools import FunctionTool
from app.core.logging import setup_logging

logger = setup_logging()

def trade_history_data_parsing_tool(parsed_data):
    async def trade_history_data_parsing_tool_wrapped():
        return {
            "status": "success", 
            "parsed_data": parsed_data
        }

    return FunctionTool(trade_history_data_parsing_tool_wrapped)