import requests
from tests.iteration2_tests.user_tests.definitions import REGISTER_V2


def test_email_unvalid():
    response = requests.post(REGISTER_V2, json = {'email': 'z1234567', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    assert response.status_code == 400

def test_email_exist():
    requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    response = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    assert response.status_code == 400

def test_password_too_short():
    response = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '123', 'name_first': 'Donald', 'name_last': 'Trump'})
    assert response.status_code == 400

def test_firstname_too_short():
    response = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': '', 'name_last': 'Trump'})
    assert response.status_code == 400

def test_firstname_too_long():
    first_name_long = 'q' * 51
    response = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': first_name_long, 'name_last': 'Trump'})
    assert response.status_code == 400

def test_lastname_too_short():
    response = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': ''})
    assert response.status_code == 400

def test_lastname_too_long():
    last_name_long = 'q' * 51
    response = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': last_name_long})
    assert response.status_code == 400

def test_valid_input():
    response = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    assert response.status_code == 200
    response_data = response.json()
    assert str(type(response_data['token'])) == "<class 'str'>"
    assert response_data['auth_user_id'] == 1

    response = requests.post(REGISTER_V2, json = {'email': 'z7654321@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Jason', 'name_last': 'Smith'})
    assert response.status_code == 200
    response_data = response.json()
    assert str(type(response_data['token'])) == "<class 'str'>"
    assert response_data['auth_user_id'] == 2

