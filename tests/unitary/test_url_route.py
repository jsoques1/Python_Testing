def test_url_show_board(client):
    result = client.get('/')
    assert result.status_code == 200
    assert b"Clubs board" in result.data


def test_url_index(client):
    result = client.get('/index')
    assert result.status_code == 200
    assert b"Please enter your secretary email to continue:" in result.data


def test_url_show_summary(client):
    result = client.get('/showSummary')
    assert result.status_code == 405


def test_url_purchase_places(client):
    result = client.get('/purchasePlaces')
    assert result.status_code == 405


def test_url_logout(client):
    result = client.get('/logout')
    assert result.status_code == 200
    assert b"Clubs board" in result.data


def test_wrong_url_booking_club(client):
    result = client.get('/book/SpringFestival/Simply%20Lift')
    assert result.status_code == 400
    assert b'Booking refused to invalid request' in result.data


def test_wrong_url_booking_competition(client):
    result = client.get('/book/Spring%20Festival/SimplyLift')
    assert result.status_code == 400
    assert b'Booking refused to invalid request' in result.data


def test_incomplete_url(client):
    result = client.get('/book/Spring%20Festival')
    assert result.status_code == 404


def test_wrong_url_root(client):
    result = client.get('/b00k/Spring%20Festival/Simply%20Lift')
    assert result.status_code == 404


def test_good_url_booking(client):
    result = client.get('/book/Spring%20Festival/Simply%20Lift')
    assert result.status_code == 200
    assert b'How many places?' in result.data
    # print(result.get_data(as_text=True))
