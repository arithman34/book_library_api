from datetime import datetime, timedelta

# POST /borrows
def test_borrow_book_success(client, books, auth_headers):
    response = client.post(
        "/borrows",
        json={
            "book_id": "9780000000000"
        },
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["book_id"] == "9780000000000"
    assert "borrowed_at" in data
    assert "user_id" in data
    assert not data["returned"]

def test_borrow_book_unauthenticated_fails(client, books):
    response = client.post(
        "/borrows",
        json={
            "book_id": "9780000000000"
        }
    )

    assert response.status_code == 401

def test_borrow_book_nonexistent_book_fails(client, auth_headers):
    response = client.post(
        "/borrows",
        json={
            "book_id": "9780000000000"
        },
        headers=auth_headers
    )

    assert response.status_code == 404

def test_borrow_book_invalid_data_fails(client, auth_headers):
    response = client.post(
        "/borrows",
        json={
            "book_id": "9780000000000",
            "due_date": "yesterday"
        },
        headers=auth_headers
    )

    assert response.status_code == 422

def test_borrow_book_custom_due_date(client, books, auth_headers):
    expected_due_date = datetime.now() + timedelta(days=7)
    response = client.post(
        "/borrows",
        json={
            "book_id": "9780000000000",
            "due_date": expected_due_date.isoformat()
        },
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    actual_due_date = datetime.fromisoformat(data["due_date"])

    assert (actual_due_date - expected_due_date).total_seconds() < 5  # Acceptable small tolerance

# POST /borrows/{borrow_id}/return
def test_return_book_success(client, borrow_book, auth_headers):
    borrow_id = borrow_book.id
    response = client.post(
        f"/borrows/{borrow_id}/return",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == borrow_id
    assert "user_id" in data
    assert data["book_id"] == "9780000000000"
    assert "borrowed_at" in data
    assert "due_date" in data
    assert data["returned"]

def test_return_book_unauthenticated_fails(client, borrow_book):
    borrow_id = borrow_book.id
    response = client.post(
        f"/borrows/{borrow_id}/return"
    )

    assert response.status_code == 401

def test_return_book_not_found(client, borrow_book, auth_headers):
    borrow_id = borrow_book.id + 1
    response = client.post(
        f"/borrows/{borrow_id}/return",
        headers=auth_headers
    )

    assert response.status_code == 404

def test_return_book_already_returned_fails(client, returned_book, auth_headers):
    borrow_id = returned_book.id
    response = client.post(
        f"/borrows/{borrow_id}/return",
        headers=auth_headers
    )

    assert response.status_code == 400

def test_return_book_belonging_to_another_user_fails(client, borrow_book, admin_auth_headers):
    borrow_id = borrow_book.id
    response = client.post(
        f"/borrows/{borrow_id}/return",
        headers=admin_auth_headers
    )

    assert response.status_code == 404
