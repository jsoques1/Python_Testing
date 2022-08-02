from server import get_competition_club, get_bookings


def test_purchase_flow(client):

    result = client.get("/")
    assert result.status_code == 200
    assert b"Clubs board" in result.data in result.data

    result = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert result.status_code == 200
    assert b'Welcome, admin@irontemple.com' in result.data

    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'Iron Temple', 'places': 1}, follow_redirects=True)

    assert result.status_code == 200
    assert b'Booking complete!' in result.data
    competition, club = get_competition_club('Autumn Festival', 'Iron Temple')
    assert int(competition['numberOfPlaces']) == 5
    assert int(club['points']) == 3
    assert get_bookings('Iron Temple', 'Autumn Festival') == 1

    result = client.get('/book/Autumn%20Festival/Iron%20Temple')
    assert result.status_code == 200
    assert b'How many places?' in result.data

    result = client.get('/logout')
    assert result.status_code == 200
    assert b"Clubs board" in result.data

    result = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert result.status_code == 200
    assert b'Welcome, admin@irontemple.com' in result.data

    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'Iron Temple', 'places': 1}, follow_redirects=True)

    assert result.status_code == 200
    assert b'Booking complete!' in result.data
    competition, club = get_competition_club('Autumn Festival', 'Iron Temple')
    assert int(competition['numberOfPlaces']) == 4
    assert int(club['points']) == 0
    assert get_bookings('Iron Temple', 'Autumn Festival') == 2

    result = client.get('/book/Autumn%20Festival/Iron%20Temple')
    assert result.status_code == 200
    assert b'How many places?' in result.data

    result = client.get('/logout')
    assert result.status_code == 200
    assert b"Clubs board" in result.data

    result = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert result.status_code == 200
    assert b'Welcome, john@simplylift.co' in result.data

    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'Simply Lift', 'places': 0}, follow_redirects=True)

    assert result.status_code == 200
    assert b'Booking complete!' in result.data
    competition, club = get_competition_club('Autumn Festival', 'Simply Lift')
    assert int(competition['numberOfPlaces']) == 4
    assert int(club['points']) == 13
    assert get_bookings('Simply Lift', 'Autumn Festival') == 0

    competition, club = get_competition_club('Autumn Festival', 'Iron Temple')
    assert int(competition['numberOfPlaces']) == 4
    assert int(club['points']) == 0
    assert get_bookings('Iron Temple', 'Autumn Festival') == 2

    result = client.get('/book/Autumn%20Festival/Simply%20Lift')
    assert result.status_code == 200
    assert b'How many places?' in result.data

    result = client.get('/logout')
    assert result.status_code == 200
    assert b"Clubs board" in result.data

    result = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert result.status_code == 200
    assert b'Welcome, kate@shelifts.co.uk' in result.data

    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'She Lifts', 'places': 10}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Not enough places left for the competition' in result.data
    competition, club = get_competition_club('Autumn Festival', 'She Lifts')
    assert int(competition['numberOfPlaces']) == 4
    assert int(club['points']) == 12
    assert get_bookings('She Lifts', 'Autumn Festival') == 0

    competition, club = get_competition_club('Autumn Festival', 'Simply Lift')
    assert int(competition['numberOfPlaces']) == 4
    assert int(club['points']) == 13
    assert get_bookings('Simply Lift', 'Autumn Festival') == 0

    competition, club = get_competition_club('Autumn Festival', 'Iron Temple')
    assert int(competition['numberOfPlaces']) == 4
    assert int(club['points']) == 0
    assert get_bookings('Iron Temple', 'Autumn Festival') == 2

    result = client.get('/book/Autumn%20Festival/She%20Lifts')
    assert result.status_code == 200
    assert b'How many places?' in result.data

    result = client.get('/logout')
    assert result.status_code == 200
    assert b"Clubs board" in result.data
