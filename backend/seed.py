from backend.database import SessionLocal
from backend.models.book import BookDB

books = [
    {"isbn": "9798745274824", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "published_year": 2021, "quantity": 5},
    {"isbn": "9780060935467", "title": "To Kill a Mockingbird", "author": "Harper Lee", "published_year": 2002, "quantity": 4},
    {"isbn": "9780451524935", "title": "1984", "author": "George Orwell", "published_year": 1950, "quantity": 6},
    {"isbn": "9780679734505", "title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "published_year": 1993, "quantity": 3},
    {"isbn": "9781250788450", "title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "published_year": 2021, "quantity": 3},
    {"isbn": "9781408855652", "title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "published_year": 2014, "quantity": 8},
    {"isbn": "9780261103252", "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "published_year": 1995, "quantity": 5},
    {"isbn": "9783125776920", "title": "The Handmaid's Tale", "author": "Margaret Atwood", "published_year": 2005, "quantity": 4},
    {"isbn": "9780316769174", "title": "The Catcher in the Rye", "author": "J.D. Salinger", "published_year": 2001, "quantity": 4},
    {"isbn": "9780547951973", "title": "The Hobbit", "author": "J.R.R. Tolkien", "published_year": 2012, "quantity": 6},
    {"isbn": "9781451669411", "title": "Hamlet", "author": "William Shakespeare", "published_year": 2012, "quantity": 5},
    {"isbn": "9780140275360", "title": "The Iliad", "author": "Homer",  "published_year": 1998, "quantity": 3},
    {"isbn": "9780061122415", "title": "The Alchemist", "author": "Paulo Coelho", "published_year": 2006, "quantity": 6},
    {"isbn": "9798312838923", "title": "Romeo and Juliet", "author": "William Shakespeare", "published_year": 2025, "quantity": 5},
    {"isbn": "9780156012195", "title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "published_year": 2000, "quantity": 7},
    {"isbn": "9780593203392", "title": "Frankenstein", "author": "Mary Shelley", "published_year": 2020, "quantity": 4},
    {"isbn": "9780141439518", "title": "Pride and Prejudice", "author": "Jane Austen", "published_year": 1813, "quantity": 5},
    {"isbn": "9781503287839", "title": "Madame Bovary", "author": "Gustave Flaubert", "published_year": 2014, "quantity": 3},
    {"isbn": "9781503261389", "title": "Dracula", "author": "Bram Stoker", "published_year": 2014, "quantity": 4},
]

def seed():
    db = SessionLocal()
    try:
        for book in books:
            db.add(BookDB(**book))
        db.commit()
        print(f"Seeded {len(books)} books successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding books: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
