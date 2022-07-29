import json
from flask import Flask, render_template, request, flash
from datetime import datetime


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def init_club_bookings(list_of_clubs, list_of_competitions):
    dict_bookings = {}
    for club in list_of_clubs:
        dict_bookings[club["name"]] = {}
        for competition in list_of_competitions:
            dict_bookings[club["name"]][competition["name"]] = 0

    return dict_bookings


app = Flask(__name__)
app.secret_key = '$25e!tiia27hdrae#vh7@_ybd=#6n8ork&#ceh^pmzlv_+l-%x'

competitions = load_competitions()
clubs = load_clubs()
bookings = init_club_bookings(clubs, competitions)


@app.route('/index')
def index():
    return render_template('index.html'), 200


@app.route('/showSummary', methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club, competitions=competitions,
                               bookings=bookings[club['name']]), 200
    except IndexError:
        if not request.form['email']:
            flash("Please enter your email.", 'error')
            return render_template('index.html'), 400

        flash('Unknown email', 'error')
        return render_template('index.html'), 400


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        found_club = [c for c in clubs if c["name"] == club][0]
        found_competition = [c for c in competitions if c["name"] == competition][0]
        if found_club and found_competition:
            return render_template('booking.html', club=found_club, competition=found_competition), 200
        # else:
        #     flash("Something went wrong-please try again")
        #     return render_template('welcome.html', club=club, competitions=competitions), 400
    except Exception:
        flash('Booking refused to invalid request.', 'error')
        return render_template('board.html', clubs=clubs, competitions=competitions), 400


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    status_code = 400
    # print(competitions)
    # print(clubs)
    # print(bookings)

    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        # print(competition)
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        # print(club)
        places_required = int(request.form['places'])
        # print(f' places_required={places_required}')
        places_booked = bookings[request.form['club']][request.form['competition']]
        # print(f' places_booked={places_booked}')
        if places_required < 0:
            flash('Required number of places should be at least 1', 'error')
        elif places_required > int(club['points']):
            flash('Not enough points left for the club', 'error')
        elif places_required > int(competition['numberOfPlaces']):
            flash('Not enough places left for the competition', 'error')
        elif places_required + places_booked > 12:
            flash("No more than 12 places can be purchased.", 'error')
        else:
            try:
                if datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") < datetime.now():
                    flash("The competition is already finished", 'error')
                    return render_template('board.html', clubs=clubs, competitions=competitions), 400
            except ValueError:
                flash("The date is invalid", 'error')
                return render_template('board.html', clubs=clubs, competitions=competitions), 400

            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
            club['points'] = int(club['points']) - places_required
            bookings[request.form['club']][request.form['competition']] += places_required
            flash('Booking complete!', 'success')
            status_code = 200
        return render_template('welcome.html', club=club, competitions=competitions,
                               bookings=bookings[club['name']]), status_code

    except Exception:
        flash('Purchase refused to invalid request', 'error')
        return render_template('board.html', clubs=clubs, competitions=competitions), 400


@app.route('/')
def show_board():
    return render_template('board.html', clubs=clubs, competitions=competitions)


@app.route('/logout')
def logout():
    return render_template('board.html', clubs=clubs, competitions=competitions)


def get_competition_club(competition_name, club_name):
    competition = [c for c in competitions if c['name'] == competition_name][0]
    club = [c for c in clubs if c['name'] == club_name][0]

    return competition, club


def get_bookings(club_name, competition_name):
    return bookings[club_name][competition_name]
