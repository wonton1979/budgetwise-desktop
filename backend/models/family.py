from datetime import datetime,UTC

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class Family(Base):
    __tablename__ = "families"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    family_name: Mapped[str] = mapped_column(String(255), nullable=True)
    family_code: Mapped[str] = mapped_column(String(255), nullable=False,unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    users = relationship("User", back_populates="family")