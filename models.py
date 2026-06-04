from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the book", examples=["The Great Gatsby"])
    author: str = Field(..., min_length=1, max_length=100, description="The author of the book", examples=["F. Scott Fitzgerald"])
    published_year: int | None = Field(None, ge=0, le=2100, description="The year the book was published", examples=[1925])

class Book(BookBase):
    id: int = Field(..., description="The unique identifier of the book", examples=[1])

    model_config = {"from_attributes": True}

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100, description="The title of the book", examples=["The Great Gatsby"])
    author: str | None = Field(None, min_length=1, max_length=100, description="The author of the book", examples=["F. Scott Fitzgerald"])
    published_year: int | None = Field(None, ge=0, le=2100, description="The year the book was published", examples=[1925])
