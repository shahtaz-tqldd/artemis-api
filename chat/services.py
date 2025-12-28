from uuid import uuid4, UUID

from chat.db.crud import SessionCRUD
from chat.schema import SessionCreate
from chat.utils.choices import PLATFORMS


class SessionService:
    def __init__(self, db):
        self.session_crud = SessionCRUD(db)

    async def session_list(
        self,
        page: int,
        page_size: int,
        platform: PLATFORMS,
        user_id: str | None = None,
    ):
        return await self.session_crud.get_list(
            page=page,
            page_size=page_size,
            platform=platform,
            user_id=user_id,
        )

    
    async def delete_session(self, session_id):
        return await self.session_crud.delete(session_id)

    async def get_messages(
        self,
        session_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ):
        return await self.session_crud.get_session_messages(
            session_id=session_id,
            page=page,
            page_size=page_size,
        )
