from typing import Optional
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

from app.core.config import get_settings
from .root_agent import create_root_agent


# utils
from .utils.call_agent import call_agent_async

settings = get_settings()


class TradingAgentClient:
    """Service class for the Trading Assistant Agent with PostgreSQL session persistence."""
    
    def __init__(
        self, 
        db,
        tenant_id,
        user_id: str, 
        user_name: str = "User",
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.db = db
        self.app_name = "Trading Assistant Agent"
        self.tenant_id = tenant_id

        # Initialize database session service for PostgreSQL
        self.session_service = DatabaseSessionService(db_url=settings.adk_db_url)
        
        # Initial state for new sessions
        self.initial_state = {
            "user_name": self.user_name,
            "conversation_history": []
        }
        
        # Create the traidng root agent
        self.trading_agent = create_root_agent()

    async def _get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """Get existing session or create a new one (async)."""
        if session_id:
            # Try to get existing session
            try:
                session = await self.session_service.get_session(
                    app_name=self.app_name,
                    user_id=self.user_id,
                    session_id=session_id
                )
                if session:
                    return session_id
            except Exception as e:
                print(f"Session retrieval error: {e}")
        
        # Check for existing sessions for this user
        try:
            existing = await self.session_service.list_sessions(
                app_name=self.app_name,
                user_id=self.user_id
            )
            
            if existing and existing.sessions:
                return existing.sessions[0].id
        except Exception as e:
            print(f"Session listing error: {e}")
        
        # Create new session
        new_session = await self.session_service.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            state=self.initial_state
        )
        return new_session.id

    async def chat(self, user_query: str, session_id: Optional[str] = None) -> dict:
        """Process a chat message and return the agent's response."""
        # Get or create session
        active_session_id = await self._get_or_create_session(session_id)
        
        # Create runner
        runner = Runner(
            app_name=self.app_name,
            agent=self.trading_agent,
            session_service=self.session_service 
        )
        
        text_response, _ = await call_agent_async(
            runner=runner,
            user_id=self.user_id,
            session_id=active_session_id,
            query=user_query
        )
        
        return {
            "response": text_response or "I apologize, I couldn't process your request. Please try again.",
            "session_id": active_session_id,
            "user_query": user_query
        }
    