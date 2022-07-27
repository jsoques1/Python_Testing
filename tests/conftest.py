import pytest
import server 
from server import app

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
            "name": "Wrong email",
            "email": "kate@com",
            "points": "100"
        },
        {
            "name": "No points",
            "email": "kate@shelifts.co.uk",
            "points": "0"
         }
    ]
    return clubs


@pytest.fixture
def competitions():
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2022-01 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Summer Festival",
            "date": "2022-6-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Spring Festival",
            "date": "2022-10-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Planned Festival with no place",
            "date": "2023-10-22 13:30:00",
            "numberOfPlaces": "0"
        },
        {
            "name": "Planned Festival with wrong date",
            "date": "22/10/2022 13:30:00",
            "numberOfPlaces": "0"
        },
        {
            "name": "Planned Festival with wrong time",
            "date": "2023-10-22 25:30:60",
            "numberOfPlaces": "12"
        },
    ]
    return competitions


@pytest.fixture
def client(mocker, clubs, competitions):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)
    with server.app.test_client() as client:
        yield client
