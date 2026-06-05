from pydantic import BaseModel, Field
from datetime import datetime

class BorrowBase(BaseModel):
    book_id: str = Field(..., min_length=13, max_length=13)
    due_date: datetime = Field(...)

class BorrowCreate(BorrowBase):
    pass

class BorrowResponse(BorrowBase):
    id: int
    user_id: int
    borrowed_at: datetime
    returned: bool

    model_config = {"from_attributes": True}


class BorrowReturn(BaseModel):
    returned: bool = True
