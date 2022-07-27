import server


def test_url_display_board_is_available(client):
    response = client.get('/')
    assert response.status_code == 200


def test_url_index(client):
    response = client.get('/index')
    assert response.status_code == 200


def test_url_show_summary(client):
    response = client.get('/showSummary')
    assert response.status_code == 405


def test_url_purchase_places(client):
    response = client.get('/purchasePlaces')
    assert response.status_code == 405


def test_url_logout(client):
    response = client.get('/logout')
    assert response.status_code == 200


def test_wrong_url_booking(client):
    response = client.get('/book/SpringFestival/Simply%20Lift')
    assert response.status_code == 400


def test_good_url_booking(client):
    response = client.get('/book/Spring%20Festival/Simply%20Lift')
    assert response.status_code == 200
