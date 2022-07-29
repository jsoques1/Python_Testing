from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from server import get_competition_club


def book_places(competition_name, club_name, nb_of_places, status):
    options = Options()
    # options.add_argument("headless")

    service = Service(verbose=True)
    driver = webdriver.Edge(service=service, options=options, )

    driver.get('http://127.0.0.1:5000')
    result = True

    try:
        competition, club = get_competition_club(competition_name, club_name)

        link_id = 'id_' + competition['name'].replace(' ', '_')

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "booking_manager"))
        element.click()

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "email"))
        element.send_keys(club['email'])

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "show_summary"))
        element.click()

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, link_id))
        element.click()

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "places"))
        element.send_keys(nb_of_places)

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "booking"))
        element.click()

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, status))
        print(element.text)

        element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "logout"))
        element.click()

        driver.quit()

        return result

    except Exception as e:
        print(e)
        return False


def test_normal_booking_1():
    result = book_places('Spring Festival', 'Simply Lift', '1', 'success')
    assert result


def test_normal_booking_2():
    result = book_places('Spring Festival', 'Iron Temple', '4', 'success')
    assert result


def test_wrong_booking_3():
    result = book_places('Spring Festival', 'Simply Lift', '12', 'error')
    assert result


def test_exception():
    result = book_places('Dummy Festival', 'Dumb club', '', '')
    assert not result
