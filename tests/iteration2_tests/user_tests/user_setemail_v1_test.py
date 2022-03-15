import requests
from tests.iteration2_tests.user_tests.definitions import REGISTER_V2, USERS_SETEMAIL_V1


def test_invalid_token():
    response = requests.put(USERS_SETEMAIL_V1, json = {'token': '123123123123123', 'email': 'z5555555@ed.unsw.edu.au'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == None

def test_invalid_email():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(USERS_SETEMAIL_V1, json = {'token': user_data['token'], 'email': '123123'})
    assert response.status_code == 400

def test_exist_email():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(USERS_SETEMAIL_V1, json = {'token': user_data['token'], 'email': 'z5555555@ed.unsw.edu.au'})
    assert response.status_code == 400

def test_valid_input():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(USERS_SETEMAIL_V1, json = {'token': user_data['token'], 'email': '987654321@unsw.edu.au'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

