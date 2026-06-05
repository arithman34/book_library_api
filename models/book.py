from database import Base
from sqlalchemy import func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class BookDB(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint("published_year >= 0 AND published_year < 2100", name="check_published_year"),
        CheckConstraint("char_length(isbn) = 13", name="check_isbn_length")
    )

    isbn: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    published_year: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"BookDB(isbn={self.isbn}, title='{self.title}', quantity='{self.quantity}')"
