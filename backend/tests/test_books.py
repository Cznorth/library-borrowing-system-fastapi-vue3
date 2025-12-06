def test_create_and_list_books(client):
    # create
    r = client.post('/api/books', json={
        'title': 'Clean Code', 'author': 'Robert C. Martin', 'isbn': '9780132350884'
    })
    assert r.status_code == 200
    book_id = r.json()['id']
    # list
    r = client.get('/api/books')
    assert r.status_code == 200
    assert r.json()['total'] >= 1
    # get
    r = client.get(f'/api/books/{book_id}')
    assert r.status_code == 200

