# GET /books
def test_get_books_returns_list(client):
    response = client.get(
        "/books"
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_books_respects_limit_and_offset(client, books):
    response = client.get(
        "/books",
        params={
            "limit": 5,
            "offset": 5
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["isbn"] == books[5].isbn

# GET /books/{isbn}
def test_get_book_by_isbn_success(client, books):
    response = client.get(
        "/books/9780000000000"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["isbn"] == books[0].isbn
    assert data["title"] == books[0].title
    assert data["author"] == books[0].author
    assert data["published_year"] == books[0].published_year

def test_get_book_by_isbn_not_found(client, books):
    response = client.get(
        "/books/9790000000000"
    )

    assert response.status_code == 404

# POST /books
def test_add_book_as_admin_success(client, admin_auth_headers):
    response = client.post(
        "/books",
        json={
            "isbn": "9780000000010",
            "title": "fake_title_10",
            "author": "fake_author_10",
            "published_year": 1910,
            "quantity": 10
        },
        headers=admin_auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["isbn"] == "9780000000010"
    assert data["title"] == "fake_title_10"
    assert data["author"] == "fake_author_10"
    assert data["published_year"] == 1910
    assert data["quantity"] == 10
    assert "created_at" in data
    assert "updated_at" in data

def test_add_book_as_non_admin_forbidden(client, auth_headers):
    response = client.post(
        "/books",
        json={
            "isbn": "9780000000010",
            "title": "fake_title_10",
            "author": "fake_author_10",
            "published_year": 1910,
            "quantity": 10
        },
        headers=auth_headers
    )

    assert response.status_code == 403

def test_add_book_unauthenticated_fails(client):
    response = client.post(
        "/books",
        json={
            "isbn": "9780000000010",
            "title": "fake_title_10",
            "author": "fake_author_10",
            "published_year": 1910,
            "quantity": 10
        },
    )

    assert response.status_code == 401

def test_add_book_invalid_data_fails(client, admin_auth_headers):
    response = client.post(
        "/books",
        json={
            "isbn": "9780000000010",
            "title": "",
            "author": "",
            "published_year": 2101,
            "quantity": 0
        },
        headers=admin_auth_headers
    )

    assert response.status_code == 422

def test_add_book_duplicated_isbn_fails(client, books, admin_auth_headers):
    response = client.post(
        "/books",
        json={
            "isbn": "9780000000000",
            "title": "fake_title_10",
            "author": "fake_author_10",
            "published_year": 1910,
            "quantity": 10
        },
        headers=admin_auth_headers
    )

    assert response.status_code == 400

# PUT /books/{isbn}
def test_update_book_as_admin_success(client, books, admin_auth_headers):
    response = client.put(
        "/books/9780000000000",
        json={
            "title": "really_fake_title_0",
            "author": "really_fake_author_0",
            "published_year": 2000,
            "quantity": 100
        },
        headers=admin_auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "really_fake_title_0"
    assert data["author"] == "really_fake_author_0"
    assert data["published_year"] == 2000
    assert data["quantity"] == 100

def test_update_book_partial_update_only_changes_given_fields(client, books, admin_auth_headers):
    original_author = books[0].author
    original_quantity = books[0].quantity
    
    response = client.put(
        "/books/9780000000000",
        json={
            "title": "really_fake_title_0",
            "published_year": 2000,
        },
        headers=admin_auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "really_fake_title_0"
    assert data["author"] == original_author
    assert data["published_year"] == 2000
    assert data["quantity"] == original_quantity

def test_update_book_as_non_admin_forbidden(client, books, auth_headers):
    response = client.put(
        "/books/9780000000000",
        json={
            "title": "really_fake_title_0",
            "published_year": 2000,
        },
        headers=auth_headers
    )

    assert response.status_code == 403

def test_update_book_unauthenticated_fails(client):
    response = client.put(
        "/books/9780000000000",
        json={
            "title": "really_fake_title_0",
            "published_year": 2000,
        }
    )

    assert response.status_code == 401

def test_update_book_not_found(client, books, admin_auth_headers):
    response = client.put(
        "/books/9780000000010",
        json={
            "title": "really_fake_title_0",
            "published_year": 2000,
        },
        headers=admin_auth_headers
    )

    assert response.status_code == 404

# DELETE /books/{isbn}
def test_delete_book_as_admin_success(client, books, admin_auth_headers):
    response = client.delete(
        "/books/9780000000000",
        headers=admin_auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["isbn"] == "9780000000000"
    assert data["title"] == "fake_title_0"
    assert data["author"] == "fake_author_0"
    assert data["published_year"] == 1900
    assert data["quantity"] == 1
    assert "created_at" in data
    assert "updated_at" in data

def test_delete_book_as_non_admin_forbidden(client, books, auth_headers):
    response = client.delete(
        "/books/9780000000000",
        headers=auth_headers
    )

    assert response.status_code == 403

def test_delete_book_unauthenticated_fails(client):
    response = client.delete(
        "/books/9780000000000"
    )

    assert response.status_code == 401

def test_delete_book_not_found(client, books, admin_auth_headers):
    response = client.delete(
        "/books/9780000000010",
        headers=admin_auth_headers
    )

    assert response.status_code == 404