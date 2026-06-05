from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import BookCreate, BookUpdate, BookResponse
from models import BookDB

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[BookResponse])
def get_books(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(BookDB).offset(offset).limit(limit).all()

@router.get("/{isbn}", response_model=BookResponse)
def get_book(isbn: str, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.isbn == isbn).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    return book

@router.post("", response_model=BookResponse, status_code=201)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = BookDB(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{isbn}", response_model=BookResponse)
def update_book(isbn: str, updated_book: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.isbn == isbn).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    if updated_book.title is not None:
        book.title = updated_book.title
    if updated_book.author is not None:
        book.author = updated_book.author
    if updated_book.genre is not None:
        book.genre = updated_book.genre
    if updated_book.published_year is not None:
        book.published_year = updated_book.published_year
    if updated_book.quantity is not None:
        book.quantity = updated_book.quantity

    db.commit()
    db.refresh(book)
    return book

@router.delete("/{isbn}", response_model=BookResponse)
def delete_book(isbn: str, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.isbn == isbn).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    db.delete(book)
    db.commit()
    return book
