from datetime import datetime,UTC

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from sqlalchemy import ForeignKey


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False,unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False,unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    family_id: Mapped[int] = mapped_column(ForeignKey("families.id"), nullable=False)
    expenses = relationship("Expense", back_populates="user")
    family = relationship("Family", back_populates="users")