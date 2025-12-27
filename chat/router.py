import json
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.base.schema import DataResponse, ListResponse

from chat.services import SessionService
from chat.utils.choices import PLATFORMS
from trading_agent.services import TradingAgentClient

from trading_agent.utils.file_parser import file_parser

router = APIRouter()

# session service dependency
async def get_session_service(
    db: AsyncSession = Depends(get_async_session),
) -> SessionService:
    return SessionService(db)


@router.get("/sessions", response_model=ListResponse)
async def get_session_list(
    platform: PLATFORMS = Query(..., description="Platform name"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: Optional[str] = Query(None),
    service: SessionService = Depends(get_session_service),
):
    """
    Get all sessions under a platform
    """
    session_list, total = await service.session_list(
        page=page,
        page_size=page_size,
        platform=platform,
        user_id=user_id,
    )

    return ListResponse(
        message="Session list retrieved successfully!",
        data=session_list,
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/sessions/messages/{session_id}", response_model=ListResponse)
async def get_session_messages(
    session_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: SessionService = Depends(get_session_service),
):
    """
    Get session messages with a session_id
    """
    message_list, total = await service.get_messages(
        session_id=session_id,
        page=page,
        page_size=page_size
    )

    return ListResponse(
        message="Session messages retrieved successfully!",
        data=message_list,
        page=page,
        page_size=page_size,
        total=total,
    )


# Chat
#======================================
# Dependency to get service
async def get_chat_service(
    db: AsyncSession = Depends(get_async_session),
    platform: PLATFORMS = Query(...),
    trade_data: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
) -> TradingAgentClient:

    parsed_data = None

    if trade_data:
        try:
            parsed_data = json.loads(trade_data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in trade_data")

    elif file:
        parsed_data = await file_parser(file)

    return TradingAgentClient(db, platform, parsed_data)



@router.post("", response_model=DataResponse)
async def chat(
    user_query: str = Form(...),
    user_id: str = Form(...),
    session_id: Optional[str] = Form(None),
    service: TradingAgentClient = Depends(get_chat_service),
):
    # Attach to request state
    new_message = await service.chat(
        user_query,
        user_id=user_id,
        session_id=session_id
    )

    return DataResponse(
        data=new_message,
        message="You have received a new message"
    )