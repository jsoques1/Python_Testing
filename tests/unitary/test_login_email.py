def test_empty_email(client):
    result = client.post('/showSummary', data={'email': ''})
    assert result.status_code == 400
    assert b'Please enter your email.' in result.data


def test_invalid_email(client):
    result = client.post('/showSummary', data={'email': 'john.doe@graveyard.com'})
    assert result.status_code == 400
    assert b'Unknown email' in result.data


def test_valid_email(client):
    result = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert result.status_code == 200
    assert b'Welcome, admin@irontemple.com' in result.data



