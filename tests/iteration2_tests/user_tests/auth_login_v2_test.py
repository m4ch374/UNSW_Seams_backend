import requests
from tests.iteration2_tests.user_tests.definitions import LOGIN_V2, REGISTER_V2


def test_account_not_exist():
    response = requests.post(LOGIN_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567'})
    assert response.status_code == 400

def test_incorrect_password():
    requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    response = requests.post(LOGIN_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '123123123'})
    assert response.status_code == 400

def test_correct_input():
    requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    response = requests.post(LOGIN_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == 1
    assert str(type(response_data['token'])) == "<class 'str'>"

def test_correct_input_1():
    requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(REGISTER_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(REGISTER_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    response = requests.post(LOGIN_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == 1
    assert str(type(response_data['token'])) == "<class 'str'>"
    response = requests.post(LOGIN_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == 2
    assert str(type(response_data['token'])) == "<class 'str'>"
    response = requests.post(LOGIN_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == 3
    assert str(type(response_data['token'])) == "<class 'str'>"
    response = requests.post(LOGIN_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == 4
    assert str(type(response_data['token'])) == "<class 'str'>"

