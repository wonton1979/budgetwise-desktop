from datetime import date,datetime,UTC

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False,unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False,unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[date] = mapped_column(Date, default=datetime.now(UTC))