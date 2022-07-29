from locust import HttpUser, task
from server import load_clubs, load_competitions, init_club_bookings


class TestPerformanceServer(HttpUser):
    competitions = load_competitions()
    clubs = load_clubs()
    bookings = init_club_bookings(clubs, competitions)
    club = clubs[0]
    competition = competitions[0]

    def on_start(self):
        self.client.get('/')

    def on_stop(self):
        self.client.get("/logout")

    @task
    def connect(self):
        self.client.post('/showSummary', data={'email': self.club['email']})

    @task
    def book(self):
        self.client.get(f"/book/{self.competition['name']}/{self.club['name']}")

    @task
    def purchase(self):
        self.client.post(
            '/purchasePlaces',
            data={
                'places': 0,
                'club': self.club['name'],
                'competition': self.competition['name']
            }
        )

    @task
    def logout(self):
        self.client.get('/logout')
