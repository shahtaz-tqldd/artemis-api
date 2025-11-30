import time
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.base.schema import DataResponse

from .schema import ChatRequest
from .services import TradingAgentClient

router = APIRouter()

@router.post("/chat", response_model=DataResponse)
async def trading_agent_chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_async_session),
    tenant_id: Optional[UUID] = None,
    ):
    """
    Chat with the trading assistant agent.
    
    - Creates a new session if session_id is not provided
    - Persists session state in PostgreSQL
    - Returns the agent's response along with session info
    """
    try:
        start_time = time.time()

        agent_client = TradingAgentClient(
            db=db,
            tenant_id=tenant_id,
            user_id=request.user_id,
            user_name=request.user_name
        )
        
        data = await agent_client.chat(
            user_query=request.user_query,
            session_id=request.session_id
        )
        
        duration = round(time.time() - start_time, 2)
        
        return DataResponse(
            success=True,
            message="Trading Assistant Agent response generated successfully.",
            duration=duration,
            data=data
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process trading agent request: {str(e)}"
        )

