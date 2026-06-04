from database import Base
from sqlalchemy.orm import Mapped, mapped_column

class BookDB(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"BookDB(id={self.id}, title='{self.title}', author='{self.author}')"
