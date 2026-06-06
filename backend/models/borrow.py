from backend.database import Base
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class BorrowDB(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[str] = mapped_column(ForeignKey("books.isbn"), nullable=False)
    due_date: Mapped[datetime] = mapped_column(nullable=False)
    borrowed_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    returned: Mapped[bool] = mapped_column(nullable=False, default=False)
