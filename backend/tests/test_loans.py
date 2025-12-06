def test_borrow_and_return_flow(client):
    # register admin and login
    client.post('/api/auth/register', json={'username': 'bob', 'email': 'bob@example.com', 'password': 'pwd', 'role': 'admin'})
    token = client.post('/api/auth/login', json={'username': 'bob', 'password': 'pwd'}).json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    # create book and copy
    book_id = client.post('/api/books', json={'title': 'DDD', 'author': 'Evans', 'isbn': '123'}).json()['id']
    copy = client.post('/api/copies', json={'book_id': book_id, 'barcode': 'C-001'}, headers=headers)
    assert copy.status_code == 200
    copy_id = copy.json()['id']
    # borrow
    r = client.post('/api/loans', params={'copy_id': copy_id}, headers=headers)
    assert r.status_code == 200
    loan_id = r.json()['id']
    # return
    r = client.post(f'/api/loans/{loan_id}/return', headers=headers)
    assert r.status_code == 200

