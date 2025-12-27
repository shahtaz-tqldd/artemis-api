from typing import Optional
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.logging import setup_logging
from .root_agent import create_root_agent

from chat.utils.choices import PLATFORMS
from chat.db.crud import SessionCRUD
from chat.schema import MessageCreate
from chat.utils.choices import SENDER_OPTIONS

logger = setup_logging()


# utils
from .utils.call_agent import call_agent_async

settings = get_settings()

DEFAULT_RESPONSE = "I apologize, I couldn't process your request. Please try again."

class TradingAgentClient:
    """Service class for the Trading Assistant Agent with PostgreSQL session persistence."""
    
    def __init__(
        self, 
        db: AsyncSession,
        platform: PLATFORMS,
        parsed_data,
    ):
        self.db = db
        self.platform = platform
        self.app_name = platform.value
        self.session_crud = SessionCRUD(db)

        # Initialize database session service for PostgreSQL
        self.session_service = DatabaseSessionService(db_url=settings.adk_db_url)
        
        # Initial state for new sessions
        self.initial_state = {}
        
        # Create the traidng root agent
        self.trading_agent = create_root_agent(parsed_data)


    async def _get_or_create_session(self, user_id, session_id: Optional[str] = None) -> str:
        """Get existing session or create a new one (async)."""
        if session_id:
            # Try to get existing session
            try:
                session = await self.session_service.get_session(
                    app_name=self.app_name,
                    user_id=user_id,
                    session_id=session_id
                )
                if session:
                    return session_id
            except Exception as e:
                print(f"Session retrieval error: {e}")
        
        # Create new session
        new_session = await self.session_service.create_session(
            app_name=self.app_name,
            user_id=user_id,
            state=self.initial_state
        )
        session_data = {
            "user_id": user_id,
            "platform": self.platform
        }
        await self.session_crud.create_session(
            session_id=new_session.id,
            session_data=session_data
        )

        return new_session.id


    async def chat(
        self,
        user_query: str,
        user_id: str,
        session_id: Optional[str] = None
    ) -> dict:
        """Process a chat message and return the agent's response."""
        
        active_session_id = await self._get_or_create_session(user_id, session_id)

        # Create runner
        runner = Runner(
            app_name=self.app_name,
            agent=self.trading_agent,
            session_service=self.session_service 
        )
        
        text_response = await call_agent_async(
            runner=runner,
            user_id=user_id,
            session_id=active_session_id,
            query=user_query
        )

        response = text_response or DEFAULT_RESPONSE

        messages = [
            MessageCreate(
                message=user_query,
                sender=SENDER_OPTIONS.USER,
            ),
            MessageCreate(
                message=response,
                sender=SENDER_OPTIONS.AI,
            )
        ]

        await self.session_crud.create_message_bulk(active_session_id, messages)

        response_dict = {
            "session_id": active_session_id,
            "message": response,
        }

        return response_dict
    