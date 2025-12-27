from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Dict
from datetime import datetime
from chat.utils.choices import PLATFORMS, SENDER_OPTIONS


class SessionCreate(BaseModel):
    user_id: str
    platform: PLATFORMS


class SessionSchema(BaseModel):
    session_id: UUID
    user_id: str
    platform: PLATFORMS
    created_at: datetime

    class Config:
        from_attributes = True



# messages schema
#===============================================
class MessageCreate(BaseModel):
    message: str
    sender: SENDER_OPTIONS
    resource: Optional[Dict] = None


class MessageOut(BaseModel):
    session_id: UUID
    message: str
    sender: str
    resource: Optional[Dict]
    created_at: datetime

    class Config:
        from_attributes = True

