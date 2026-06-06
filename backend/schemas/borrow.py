from pydantic import BaseModel, Field
from datetime import datetime, timedelta

class BorrowBase(BaseModel):
    book_id: str = Field(..., min_length=13, max_length=13)

class BorrowCreate(BorrowBase):
    due_date: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=14))

class BorrowResponse(BorrowBase):
    id: int
    user_id: int
    borrowed_at: datetime
    due_date: datetime
    returned: bool

    model_config = {"from_attributes": True}

class BorrowReturn(BaseModel):
    returned: bool = True
