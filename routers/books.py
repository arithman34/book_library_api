from fastapi import APIRouter, HTTPException
from models import Book, BookCreate, BookUpdate
from database import books

router = APIRouter(prefix="/books", tags=["books"])

@router.get("", response_model=list[Book])
def get_books(limit: int = 10, offset: int = 0):
    return books[offset : offset + limit]

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    
    raise HTTPException(status_code=404, detail="Book not found.")

@router.post("", response_model=Book, status_code=201)
def add_book(book: BookCreate):
    book_id = max(b.id for b in books) + 1
    new_book = Book(id=book_id, **book.model_dump())
    books.append(new_book)
    return new_book

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: BookUpdate):
    for book in books:
        if book.id == book_id:
            if updated_book.title is not None:
                book.title = updated_book.title
            
            if updated_book.author is not None:
                book.author = updated_book.author

            return book
    
    raise HTTPException(status_code=404, detail="Book not found.")

@router.delete("/{book_id}", response_model=Book)
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted_book = books.pop(index)
            return deleted_book
        
    raise HTTPException(status_code=404, detail="Book not found.")
