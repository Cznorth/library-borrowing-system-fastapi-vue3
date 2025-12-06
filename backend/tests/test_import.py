from app.main import app


def auth_headers(client):
    client.post('/api/auth/register', json={
        'username': 'admin', 'email': 'admin@example.com', 'password': 'Admin@12345', 'role': 'admin'
    })
    r = client.post('/api/auth/login', json={'username': 'admin', 'password': 'Admin@12345'})
    token = r.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_bulk_import_json(client):
    headers = auth_headers(client)
    items = [
        {"isbn": "9780132350884", "title": "Clean Code", "author": "Robert C. Martin"},
        {"isbn": "9780131103627", "title": "The C Programming Language", "author": "Brian W. Kernighan, Dennis M. Ritchie"},
    ]
    r = client.post('/api/books/bulk', json=items, headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body['inserted'] == 2
    # call again to test upsert
    r = client.post('/api/books/bulk', json=items, headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body['updated'] == 2
