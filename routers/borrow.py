from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
from models.user import UserDB
from schemas import BorrowCreate, BorrowResponse
from models import BorrowDB

router = APIRouter(prefix="/borrows", tags=["borrows"])

@router.post("", response_model=BorrowResponse, status_code=201)
def borrow_book(borrow: BorrowCreate, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    new_borrow = BorrowDB(**borrow.model_dump(), user_id=current_user.id)
    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)
    return new_borrow

@router.post("/{borrow_id}/return", response_model=BorrowResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    borrow_record = db.query(BorrowDB).filter(BorrowDB.id == borrow_id, BorrowDB.user_id == current_user.id).first()
    
    if not borrow_record:
        raise HTTPException(status_code=404, detail="Borrow record not found.")
    
    if borrow_record.returned:
        raise HTTPException(status_code=400, detail="Book already returned.")
    
    borrow_record.returned = True
    db.commit()
    db.refresh(borrow_record)
    return borrow_record
