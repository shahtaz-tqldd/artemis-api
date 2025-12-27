from uuid import UUID
import uuid
from typing import Optional, Dict

from sqlalchemy import Enum, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column



from app.base.models import BaseModel
from chat.utils.choices import PLATFORMS, SENDER_OPTIONS


class Session(BaseModel):
    __tablename__ = "chat_sessions"

    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[str] = mapped_column(index=True, nullable=False)

    platform: Mapped[PLATFORMS] = mapped_column(
        Enum(PLATFORMS),
        index=True,
        nullable=False,
    )

    __table_args__ = (
        Index("idx_session_user_platform", "user_id", "platform"),
    )


class Message(BaseModel):
    __tablename__ = "chat_messages"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("chat_sessions.session_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    message: Mapped[str] = mapped_column(nullable=False)

    sender: Mapped[SENDER_OPTIONS] = mapped_column(
        Enum(SENDER_OPTIONS),
        nullable=False,
    )

    resource: Mapped[Optional[Dict]] = mapped_column(
        JSONB,
        nullable=True
    )
