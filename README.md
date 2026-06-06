# Book Library API

A REST API built with FastAPI and PostgreSQL to manage a collection of books. Covers CRUD operations, Pydantic validation, SQLAlchemy ORM, JWT authentication and database migrations with Alembic.

## Tech Stack

- Python, FastAPI, Pydantic
- PostgreSQL, SQLAlchemy, Alembic
- JWT authentication (python-jose, passlib/bcrypt)
- Uvicorn

## Getting Started

1. Clone the repo and navigate into it
```bash
git clone https://github.com/arithman34/book_library_api
cd book_library_api
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate # On Windows
source .venv/bin/activate # On Unix or MacOS
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Ensure PostgreSQL is installed and running on your machine. You can download it from [postgresql.org](https://www.postgresql.org/download/) and create a database for this project.

5. Set up your environment variables
```bash
cp .env.example .env
```
Then open `.env` and fill in your values:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/book_library
SECRET_KEY=your-secret-key
```

6. Run the application on port 8000
```bash
uvicorn backend.main:app --port 8000 --reload
```

7. Open http://127.0.0.1:8000/docs to explore the API documentation and test the endpoints.

## Project Structure

```
book_library_api/
├── .env.example
├── .gitattributes
├── .gitignore
├── alembic.ini
├── backend/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── seed.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── borrow.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── book.py
│   │   └── borrow.py
│   └── schemas/
│       ├── __init__.py
│       ├── book.py
│       ├── borrow.py
│       ├── token.py
│       └── user.py
├── LICENSE
├── migrations/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── README.md
└── requirements.txt
```

## Endpoints

### Auth
| Method | Endpoint           | Description                        | Auth required |
|--------|--------------------|------------------------------------|---------------|
| POST   | /auth/register     | Register a new user                | No            |
| POST   | /auth/login        | Log in and receive a JWT token     | No            |

### Books
| Method | Endpoint           | Description                        | Auth required |
|--------|--------------------|------------------------------------|---------------|
| GET    | /books             | Get all books (paginated)          | No            |
| GET    | /books/{isbn}      | Get a book by ISBN                 | No            |
| POST   | /books             | Add a new book (admin only)        | Yes           |
| PUT    | /books/{isbn}      | Update a book (admin only)         | Yes           |
| DELETE | /books/{isbn}      | Delete a book (admin only)         | Yes           |

### Borrows
| Method | Endpoint                   | Description                   | Auth required |
|--------|----------------------------|-------------------------------|---------------|
| POST   | /borrows                   | Borrow a book                 | Yes           |
| POST   | /borrows/{borrow_id}/return | Return a borrowed book        | Yes           |

## Future Work

- Pytest test suite (unit + integration tests)
- Tkinter desktop frontend (`frontend/`)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
