from fastapi import FastAPI
from routers import books

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Book Library API is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(books.router)
