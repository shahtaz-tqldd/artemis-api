from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_query: str
    user_id: str
    user_name: Optional[str] = "User"
    session_id: Optional[str] = None
