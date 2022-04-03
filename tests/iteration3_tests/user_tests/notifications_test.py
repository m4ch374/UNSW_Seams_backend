import requests
from tests.iteration3_tests.user_tests.definitions import REGISTER_V2, NOTIFICATIONS_GET_V1

def test_invalid_token():
    response = requests.get(NOTIFICATIONS_GET_V1, {'token': '123'})
    assert response.status_code == 403

def test_valid_input_empty():
    user = requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(REGISTER_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(REGISTER_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    user_data = user.json()
    response = requests.get(NOTIFICATIONS_GET_V1, {'token': user_data['token']})
    assert response.status_code == 200
    assert response.json() == {'notifications': []}

def test_valid_input():
    # user = requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    # requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    # requests.post(REGISTER_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    # requests.post(REGISTER_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    # user_data = user.json()
    # response = requests.get(NOTIFICATIONS_GET_V1, {'token': user_data['token']})
    # assert response.status_code == 200
    # assert response.json() == {'notifications': []}
    pass