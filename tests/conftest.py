import pytest
import server
from server import app
from server import init_club_bookings

app.config['TESTING'] = True


@pytest.fixture
def clubs():
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        },
        {
            "name": "Iron women",
            "email": "kate@iron.women.com",
            "points": "100"
        },
        {
            "name": "Club closed",
            "email": "kate@club.closed.co.uk",
            "points": "0"
         }
    ]
    return clubs


@pytest.fixture
def competitions():
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2023-6-22 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Summer Festival",
            "date": "2023-6-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Autumn Festival",
            "date": "2023-10-27 10:00:00",
            "numberOfPlaces": "5"
        },
        {
            "name": "Planned Festival with no place",
            "date": "2023-10-22 13:30:00",
            "numberOfPlaces": "0"
        },
        {
            "name": "Planned Festival with old date",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "2"
        },
        {
            "name": "Planned Festival with wrong date format",
            "date": "2023/10/22 25:30:60",
            "numberOfPlaces": "12"
        },
        {
            "name": "Planned Festival with wrong date",
            "date": "2023-22-22 25:30:60",
            "numberOfPlaces": "12"
        },
        {
            "name": "Planned Festival with wrong numberOfPlaces",
            "date": "2023-22-22 25:30:60",
            "numberOfPlaces": ""
        },
    ]
    return competitions


@pytest.fixture
def client(mocker, clubs, competitions):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)
    bookings = init_club_bookings(clubs, competitions)
    mocker.patch.object(server, "bookings", bookings)
    with server.app.test_client() as client:
        yield client
