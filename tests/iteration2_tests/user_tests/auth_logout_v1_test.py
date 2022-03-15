import requests
from tests.iteration2_tests.user_tests.definitions import LOGIN_V2, LOGOUT_V1, REGISTER_V2


def test_invalid_token():
    token = 'xxxxxxxxxxxx'
    response = requests.post(LOGOUT_V1, json = {'token': token})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == None

def test_register_logout():
    user = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    user_data = user.json()
    response = requests.post(LOGOUT_V1, json = {'token': user_data['token']})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

def test_login_logout():
    user = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    user_data = user.json()
    requests.post(LOGOUT_V1, json = {'token': user_data['token']})
    user = requests.post(LOGIN_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567'})
    user_data = user.json()
    response = requests.post(LOGOUT_V1, json = {'token': user_data['token']})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

