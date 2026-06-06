from jose import jwt
from backend.auth import create_access_token, ALGORITHM

def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "new_password123"
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["username"] == "new_user"
    assert data["email"] == "new_user@example.com"
    assert "password" not in data
    assert "hashed_password" not in data

def test_register_duplicate_username_fails(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "username": test_user.username,
            "email": "different@example.com",
            "password": "new_password123"
        }
    )

    assert response.status_code == 400

def test_register_duplicate_email_fails(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "username": "different_user",
            "email": test_user.email,
            "password": "new_password123"
        }
    )

    assert response.status_code == 400

def test_register_invalid_data_fails(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "ab",  # too short (min_length=3)
            "email": "not_an_email",
            "password": "short"  # too short (min_length=8)
        }
    )

    assert response.status_code == 422


def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.username,
            "password": "password123"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password_fails(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.username,
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_login_nonexistent_user_fails(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": "non_existent",
            "password": "password123"
        }
    )

    assert response.status_code == 401

# Protected route security paths
def test_malformed_token_fails(client):
    response = client.post(
        "/borrows",
        json={"book_id": "9780000000000"},
        headers={"Authorization": "Bearer this_is_not_a_valid_token"}
    )
    assert response.status_code == 401


def test_tampered_token_fails(client):
    fake_token = jwt.encode(
        {"sub": "new_user"},
        "wrong_secret",
        algorithm=ALGORITHM
    )
    response = client.post(
        "/borrows",
        json={"book_id": "9780000000000"},
        headers={"Authorization": f"Bearer {fake_token}"}
    )
    assert response.status_code == 401


def test_valid_token_deleted_user_fails(client):
    token = create_access_token(data={"sub": "deleted_user"})
    response = client.post(
        "/borrows",
        json={"book_id": "9780000000000"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401