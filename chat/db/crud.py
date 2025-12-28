from fastapi import HTTPException
from typing import Optional, List, Tuple
from uuid import UUID, uuid4

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from chat.db.models import Session, Message
from chat.utils.choices import PLATFORMS
from chat.schema import SessionSchema, SessionMessage

class SessionCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        page: int,
        page_size: int,
        platform: PLATFORMS,
        user_id: Optional[str] = None,
    ) -> Tuple[List[SessionSchema], int]:

        # Base query
        base_stmt = select(Session).where(Session.platform == platform)
        if user_id:
            base_stmt = base_stmt.where(Session.user_id == user_id)

        # Total count
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        # Pagination
        stmt = (
            base_stmt.order_by(Session.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.db.execute(stmt)
        sessions = result.scalars().all()

        session_list = [
            SessionSchema.model_validate(session)
            for session in sessions
        ]

        return session_list, total


    async def get_session_messages(
        self,
        session_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[SessionMessage], int]:
        
        # Base query for this session
        base_stmt = select(Message).where(Message.session_id == session_id)

        # Total count
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        # Paginated messages
        stmt = (
            base_stmt.order_by(Message.created_at.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.db.execute(stmt)
        messages = result.scalars().all()

        message_list = [
            SessionMessage.model_validate(message)
            for message in messages
        ]

        return message_list, total


    async def create_session(self, session_id: UUID, session_data:dict):
        session = Session(
            session_id=session_id,
            user_id=session_data.get("user_id", None),
            platform=session_data.get("platform", None),
        )

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session


    async def create_message_bulk(
        self,
        session_id: UUID,
        message_data: List,
    ):
        messages = []

        for msg in message_data:
            messages.append(
                Message(
                    id=uuid4(),
                    session_id=session_id,
                    message=msg.message,
                    sender=msg.sender,
                    resource=msg.resource,
                )
            )

        self.db.add_all(messages)
        await self.db.commit()
        return messages


    async def delete(self, session_id: UUID):
        result = await self.db.execute(
            select(Session).where(Session.session_id == session_id)
        )
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        await self.db.delete(session)
        await self.db.commit()

        return session
