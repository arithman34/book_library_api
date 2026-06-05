from fastapi import FastAPI
from routers import auth, book, borrow

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Book Library API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(book.router)
app.include_router(borrow.router)
