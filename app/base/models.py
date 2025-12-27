from datetime import datetime
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase


class TimestampMixin:
    """Adds created_at, updated_at timestamp fields to models."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# Combine into one base mixin for convenience
class BaseModel(DeclarativeBase, TimestampMixin):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
