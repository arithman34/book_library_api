from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Book, BookCreate, BookUpdate
from models_db import BookDB

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[Book])
def get_books(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(BookDB).offset(offset).limit(limit).all()

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    return book

@router.post("", response_model=Book, status_code=201)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = BookDB(title=book.title, author=book.author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    if updated_book.title is not None:
        book.title = updated_book.title
    if updated_book.author is not None:
        book.author = updated_book.author

    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", response_model=Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    db.delete(book)
    db.commit()
    return book
