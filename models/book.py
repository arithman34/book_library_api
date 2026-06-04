from pydantic import BaseModel, Field
from datetime import datetime


class BookBase(BaseModel):
    isbn: str = Field(..., min_length=13, max_length=13)
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    genre: str = Field(..., min_length=1, max_length=50)
    published_year: int = Field(..., ge=0, lt=2100)
    

class BookCreate(BookBase):
    quantity: int = Field(..., ge=1)


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    author: str | None = Field(None, min_length=1, max_length=100)
    genre: str | None = Field(None, min_length=1, max_length=50)
    published_year: int | None = Field(None, ge=0, lt=2100)
    quantity: int | None = Field(None, ge=0)


class BookResponse(BookBase):
    quantity: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
