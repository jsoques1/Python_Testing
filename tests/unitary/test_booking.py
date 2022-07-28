from server import get_club_competition, get_bookings


def test_overbooking_no_place_in_competition(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Planned Festival with no place',
              'club': 'Iron Temple', 'places': 1}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Not enough places left for the competition' in result.data
    competition, club = get_club_competition('Planned Festival with no place', 'Iron Temple')
    assert int(competition['numberOfPlaces']) == 0
    assert int(club['points']) == 4
    assert get_bookings('Simply Lift', 'Autumn Festival') == 0


def test_overbooking_not_enough_place_in_competition(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'Simply Lift', 'places': 6}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Not enough places left for the competition' in result.data
    competition, club = get_club_competition('Autumn Festival', 'Simply Lift')
    assert int(competition['numberOfPlaces']) == 5
    assert int(club['points']) == 13
    assert get_bookings('Simply Lift', 'Autumn Festival') == 0


def test_overbooking_more_than_12_places(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Spring Festival',
              'club': 'Simply Lift', 'places': 13}, follow_redirects=True)

    assert result.status_code == 400
    assert b'No more than 12 places can be purchased.' in result.data
    competition, club = get_club_competition('Spring Festival', 'Simply Lift')
    assert int(competition['numberOfPlaces']) == 25
    assert int(club['points']) == 13
    assert get_bookings('Simply Lift', 'Spring Festival') == 0


def test_overbooking_in_2_shots(client):

    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'Simply Lift', 'places': 3}, follow_redirects=True)

    assert result.status_code == 200
    assert b'Booking complete!' in result.data
    competition, club = get_club_competition('Autumn Festival', 'Simply Lift')
    assert int(competition['numberOfPlaces']) == 2
    assert int(club['points']) == 10
    assert get_bookings('Simply Lift', 'Autumn Festival') == 3

    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'She Lifts', 'places': 3}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Not enough places left for the competition' in result.data
    competition, club = get_club_competition('Autumn Festival', 'She Lifts')
    assert int(competition['numberOfPlaces']) == 2
    assert int(club['points']) == 12
    assert get_bookings('She Lifts', 'Autumn Festival') == 0


def test_overbooking_no_points_in_club(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Spring Festival',
              'club': 'Club closed', 'places': 1}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Not enough points left for the club' in result.data
    competition, club = get_club_competition('Spring Festival', 'Club closed')
    assert int(competition['numberOfPlaces']) == 25
    assert int(club['points']) == 0
    assert get_bookings('Club closed', 'Spring Festival') == 0


# def test_booking_0_place(client):
#
#     result = client.post(
#         '/purchasePlaces',
#         data={'competition': 'Autumn Festival',
#               'club': 'Simply Lift', 'places': 0}, follow_redirects=True)
#
#     assert result.status_code == 400
#     assert b'Required number of places should be at least 1' in result.data
#     competition, club = get_club_competition('Autumn Festival', 'Simply Lift')
#     assert int(competition['numberOfPlaces']) == 5
#     assert int(club['points']) == 13
#     assert get_bookings('Simply Lift', 'Autumn Festival') == 0


def test_booking_for_a_terminated_competition(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Planned Festival with old date',
              'club': 'Simply Lift', 'places': 1}, follow_redirects=True)

    assert result.status_code == 400
    assert b'The competition is already finished' in result.data
    competition, club = get_club_competition('Planned Festival with old date', 'Simply Lift')
    assert int(competition['numberOfPlaces']) == 2
    assert int(club['points']) == 13
    assert get_bookings('Simply Lift', 'Planned Festival with old date') == 0


def test_booking_for_a_wrong_date_format_competition(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Planned Festival with wrong date format',
              'club': 'Simply Lift', 'places': 3}, follow_redirects=True)

    assert result.status_code == 400
    assert b'The date is invalid' in result.data
    competition, club = get_club_competition('Planned Festival with wrong date format', 'Simply Lift')
    assert int(competition['numberOfPlaces']) == 12
    assert int(club['points']) == 13
    assert get_bookings('Simply Lift', 'Planned Festival with wrong date format') == 0


def test_booking_for_a_wrong_date_competition(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Planned Festival with wrong date',
              'club': 'Simply Lift', 'places': 3}, follow_redirects=True)

    assert result.status_code == 400
    assert b'The date is invalid' in result.data
    competition, club = get_club_competition('Planned Festival with wrong date', 'Simply Lift')
    assert int(competition['numberOfPlaces']) == 12
    assert int(club['points']) == 13
    assert get_bookings('Simply Lift', 'Planned Festival with wrong date') == 0


def test_booking_for_unknown_competition(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Unknown competition',
              'club': 'Simply Lift', 'places': 3}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Purchase refused to invalid request' in result.data


def test_booking_for_unknown_club(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'Unknown club', 'places': 3}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Purchase refused to invalid request' in result.data


def test_booking_for_invalid_places_value(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Unknown competition',
              'club': 'Simply Lift', 'places': 'one'}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Purchase refused to invalid request' in result.data


def test_booking_for_invalid_no_places_value(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Unknown competition',
              'club': 'Simply Lift', 'places': ''}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Purchase refused to invalid request' in result.data


def test_booking_for_invalid_number_of_places(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Planned Festival with wrong numberOfPlaces',
              'club': 'Simply Lift', 'places': 1}, follow_redirects=True)

    assert result.status_code == 400
    assert b'Purchase refused to invalid request' in result.data


def test_normal_booking(client):
    result = client.post(
        '/purchasePlaces',
        data={'competition': 'Autumn Festival',
              'club': 'Simply Lift', 'places': 3}, follow_redirects=True)

    assert result.status_code == 200
    assert b'Booking complete!' in result.data
    competition, club = get_club_competition('Autumn Festival', 'Simply Lift')
    assert int(competition['numberOfPlaces']) == 2
    assert int(club['points']) == 10
    assert get_bookings('Simply Lift', 'Autumn Festival') == 3
