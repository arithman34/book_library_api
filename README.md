# Book Library API

A REST API built with FastAPI and PostgreSQL to manage a collection of books. Covers CRUD operations, Pydantic validation, SQLAlchemy ORM, JWT authentication, database migrations with Alembic, and a full pytest test suite with 99% coverage.

## Tech Stack

- Python, FastAPI, Pydantic
- PostgreSQL, SQLAlchemy, Alembic
- JWT authentication (python-jose, passlib/bcrypt)
- pytest, pytest-cov
- Docker, Docker Compose
- Uvicorn

## Running with Docker (Recommended)

1. Clone the repo and navigate into it
```bash
git clone https://github.com/arithman34/book_library_api
cd book_library_api
```

2. Set up your environment variables
```bash
cp .env.example .env
```
Then open `.env` and fill in your `DATABASE_URL` and `SECRET_KEY`.

3. Build and start the containers
```bash
docker compose up --build
```

4. In a second terminal, run migrations
```bash
docker compose exec backend alembic upgrade head
```

5. (Optional) Seed the database with sample books
```bash
docker compose exec backend python -m backend.seed
```

6. Open http://localhost:8000/docs to explore and test the API.

To stop:
```bash
docker compose down
```

---

## Getting Started (without Docker)

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

8. (Optional) Seed the database with sample books
```bash
python -m backend.seed
```

## Running Tests

1. Set up a separate test database and create a `.env.test` file
```bash
cp .env.test.example .env.test
```
Then open `.env.test` and fill in your values:
```bash
TEST_DATABASE_URL=postgresql://username:password@localhost:5432/book_library_test
SECRET_KEY=your-secret-key
```

2. Run the test suite
```bash
pytest
```

3. To view a browsable HTML coverage report, open `htmlcov/index.html` after running pytest.

## Project Structure

```
book_library_api/
├── .coveragerc
├── .dockerignore
├── .env.example
├── .env.test.example
├── .gitattributes
├── .gitignore
├── alembic.ini
├── backend/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
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
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── borrow.py
│   │   ├── token.py
│   │   └── user.py
│   └── seed.py
├── LICENSE
├── migrations/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       ├── 0e7729303c7d_remove_genre_column.py
│       └── 7025c99c1e50_initial_schema.py
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── README.md
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    ├── test_book.py
    └── test_borrow.py
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

- Tkinter desktop frontend (`frontend/`)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
