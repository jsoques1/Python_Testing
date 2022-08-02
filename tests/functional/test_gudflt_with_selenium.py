from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from server import get_competition_club


def get_number(s):
    number = s.split(': ')[1]
    return int(number)


def book_places(competition_name, club_name, nb_of_places, status, msg):
    options = Options()
    options.add_argument("headless")

    service = Service(verbose=True)
    driver = webdriver.Edge(service=service, options=options, )

    driver.get('http://127.0.0.1:5000')
    result = True

    try:
        competition, club = get_competition_club(competition_name, club_name)

        link_id = f"id_{competition['name'].replace(' ', '_')}"

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "booking_manager"))
        element.click()

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "email"))
        element.send_keys(club['email'])

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "show_summary"))
        element.click()

        id_number_of_places = f"id_{competition['name'].replace(' ', '_')}_numberOfPlaces"
        id_booked = f"id_{competition['name'].replace(' ', '_')}_booked"

        points_available_before = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "id_points")).text
        number_of_places_before = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(By.ID, id_number_of_places)).text
        booked_before = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, id_booked)).text

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, link_id))
        element.click()

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "places"))
        element.send_keys(nb_of_places)

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "booking"))
        element.click()

        points_available_after = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "id_points")).text
        number_of_places_after = WebDriverWait(driver, 10).until(
            lambda x: x.find_element(By.ID, id_number_of_places)).text
        booked_after = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, id_booked)).text
        status_msg = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, status)).text

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "logout"))
        element.click()

        driver.quit()

        if status_msg == 'Success : Booking complete!':
            assert get_number(points_available_after) == get_number(points_available_before) - (3 * int(nb_of_places))
            assert get_number(number_of_places_after) == get_number(number_of_places_before) - int(nb_of_places)
            assert get_number(booked_after) == get_number(booked_before) + int(nb_of_places)
        elif status_msg == msg:
            assert get_number(points_available_after) == get_number(points_available_before)
            assert get_number(number_of_places_after) == get_number(number_of_places_before)
            assert get_number(booked_after) == get_number(booked_before)
        else:
            result = False

        return result

    except Exception as e:
        print(e)
        return False


def test_normal_booking_1st_club():
    result = book_places('Spring Festival', 'Simply Lift', '1', 'success', 'Success : Booking complete!')
    assert result


def test_normal_booking_2nd_club():
    result = book_places('Spring Festival', 'Iron Temple', '1', 'success', 'Success : Booking complete!')
    assert result


def test_wrong_booking_more_than_12_places():
    result = book_places('Spring Festival', 'Simply Lift', '12', 'error',
                         'Error : No more than 12 places can be purchased.')
    assert result


def test_wrong_booking_negative_number_of_places():
    result = book_places('Spring Festival', 'Simply Lift', '-10', 'error',
                         'Error : Required number of places should be at least 1')
    assert result


def test_normal_booking_2_places():
    result = book_places('Fall Classic', 'Simply Lift', '2', 'success', 'Success : Booking complete!')
    assert result


def test_exception_wrong_msg():
    result = book_places('Fall Classic', 'Simply Lift', '-1', 'error', 'error : Wrong message')
    assert not result


def test_exception_unknown_competition():
    result = book_places('Dummy Festival', 'Dumb club', '', 'error',
                         'list index out of range')
    assert not result
