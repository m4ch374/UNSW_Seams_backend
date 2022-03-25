import requests
from tests.iteration2_tests.user_tests.definitions import REGISTER_V2, USERS_SETNAME_V1


def test_invalid_token():
    response = requests.put(USERS_SETNAME_V1, json = {'token': '123123123123123', 'name_first': 'James', 'name_last': 'Bond'})
    assert response.status_code == 403

def test_long_name():
    long_name = 'x' * 51
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(USERS_SETNAME_V1, json = {'token': user_data['token'], 'name_first': long_name, 'name_last': 'Bond'})
    assert response.status_code == 400
    response = requests.put(USERS_SETNAME_V1, json = {'token': user_data['token'], 'name_first': 'James', 'name_last': long_name})
    assert response.status_code == 400

def test_short_name():
    short_name = ''
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(USERS_SETNAME_V1, json = {'token': user_data['token'], 'name_first': short_name, 'name_last': 'Bond'})
    assert response.status_code == 400
    response = requests.put(USERS_SETNAME_V1, json = {'token': user_data['token'], 'name_first': 'James', 'name_last': short_name})
    assert response.status_code == 400

def test_valid_input():
    requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(REGISTER_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(REGISTER_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(USERS_SETNAME_V1, json = {'token': user_data['token'], 'name_first': 'James', 'name_last': 'Bond'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

