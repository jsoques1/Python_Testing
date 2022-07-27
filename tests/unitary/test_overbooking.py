from server import get_club_competition, bookings


def test_overbooking_no_place_in_competition(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Planned Festival with no place',
              'club': 'Iron Temple', 'places': 1}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Not enough places left for the competition' in result.data


def test_overbooking_not_enough_place_in_competition(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'Simply Lift', 'places': 6}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Not enough places left for the competition' in result.data


def test_overbooking_in_2_shots(client):
    print(bookings)

    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'Simply Lift', 'places': 3}, follow_redirects=True)

    assert result.status_code == 200
    assert b'Booking complete!' in result.data
    competition, club = get_club_competition('Autumn Festival', 'Simply Lift')
    assert competition['numberOfPlaces'] == 2
    assert int(club['points']) == 10
    # assert bookings['Simply Lift']['Autumn Festival'] == 3
    
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'She Lifts', 'places': 3}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Not enough places left for the competition' in result.data
    competition, club = get_club_competition('Autumn Festival', 'She Lifts')
    assert competition['numberOfPlaces'] == 2
    assert int(club['points']) == 12
    # assert bookings['She Lifts']['Autumn Festival'] == 0
