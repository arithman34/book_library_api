from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the book", examples=["The Great Gatsby"])
    author: str = Field(..., min_length=1, max_length=100, description="The author of the book", examples=["F. Scott Fitzgerald"])

class Book(BookBase):
    id: int = Field(..., description="The unique identifier of the book", examples=[1])

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100, description="The title of the book", examples=["The Great Gatsby"])
    author: str | None = Field(None, min_length=1, max_length=100, description="The author of the book", examples=["F. Scott Fitzgerald"])
