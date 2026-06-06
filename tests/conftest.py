import os
import pytest
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

load_dotenv(".env.test")

from backend.main import app
from backend.database import Base, get_db
from backend.models import UserDB, BookDB, BorrowDB
from backend.auth import hash_password


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL is not set in .env.test")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Book fixtures

@pytest.fixture()
def books(db_session):
    new_books = []
    for i in range(10):
        new_book = BookDB(
            isbn=f"97800000{i:05d}",
            title=f"fake_title_{i}",
            author=f"fake_author_{i}",
            published_year=1900 + i,
            quantity=i + 1
        )

        new_books.append(new_book)
        db_session.add(new_book)
    
    db_session.commit()
    return new_books


# User fixtures

DEFAULT_PASSWORD = "password123"

def _create_user(db_session, username, email, is_admin=False):
    user = UserDB(
        username=username,
        email=email,
        hashed_password=hash_password(DEFAULT_PASSWORD),
        is_admin=is_admin
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def test_user(db_session):
    return _create_user(db_session, "test_user", "test_user@example.com", is_admin=False)

@pytest.fixture()
def admin_user(db_session):
    return _create_user(db_session, "admin_user", "admin_user@example.com", is_admin=True)


def _login(client, username, password=DEFAULT_PASSWORD):
    response = client.post(
        "/auth/login",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200, response.text
    token = response.json().get("access_token")
    assert token is not None, "Login did not return access token"
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def auth_headers(client, test_user):
    return _login(client, test_user.username)


@pytest.fixture()
def admin_auth_headers(client, admin_user):
    return _login(client, admin_user.username)

# Borrow fixtures
@pytest.fixture()
def borrow_book(db_session, test_user, books):
    new_borrow = BorrowDB(
        user_id=test_user.id,
        book_id=books[0].isbn,
        due_date=datetime.now() + timedelta(days=14),
        returned=False
    )
    db_session.add(new_borrow)
    db_session.commit()
    db_session.refresh(new_borrow)
    return new_borrow

@pytest.fixture()
def returned_book(db_session, test_user, books):
    new_borrow = BorrowDB(
        user_id=test_user.id,
        book_id=books[0].isbn,
        due_date=datetime.now() + timedelta(days=14),
        returned=True
    )
    db_session.add(new_borrow)
    db_session.commit()
    db_session.refresh(new_borrow)
    return new_borrow