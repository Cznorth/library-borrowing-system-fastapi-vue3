def test_register_and_login(client):
    # register
    r = client.post('/api/auth/register', json={
        'username': 'alice', 'email': 'alice@example.com', 'password': 'secret'
    })
    assert r.status_code == 200
    # login
    r = client.post('/api/auth/login', json={'username': 'alice', 'password': 'secret'})
    assert r.status_code == 200
    token = r.json()['access_token']
    assert token
    # me
    r = client.get('/api/users/me', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200
    assert r.json()['username'] == 'alice'

