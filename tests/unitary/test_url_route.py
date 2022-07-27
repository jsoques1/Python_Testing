def test_url_show_board(client):
    response = client.get('/')
    expected = b"Clubs board"
    assert response.status_code == 200
    assert expected in response.data


def test_url_index(client):
    response = client.get('/index')
    expected = b"Please enter your secretary email to continue:"
    assert response.status_code == 200
    assert expected in response.data


def test_url_show_summary(client):
    response = client.get('/showSummary')
    assert response.status_code == 405


def test_url_purchase_places(client):
    response = client.get('/purchasePlaces')
    assert response.status_code == 405


def test_url_logout(client):
    response = client.get('/logout')
    expected = b"Clubs board"
    assert response.status_code == 200
    assert expected in response.data


def test_wrong_url_booking(client):
    response = client.get('/book/SpringFestival/Simply%20Lift')
    assert response.status_code == 400


def test_good_url_booking(client):
    response = client.get('/book/Spring%20Festival/Simply%20Lift')
    assert response.status_code == 200
