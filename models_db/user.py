from database import Base
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"UserDB(id={self.id}, username='{self.username}', email='{self.email}', is_admin='{self.is_admin}')"
