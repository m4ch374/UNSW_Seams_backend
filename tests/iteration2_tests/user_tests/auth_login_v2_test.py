import requests

BASE_ADDRESS = 'http://localhost:'
BASE_PORT = '30000'
BASE_URL = BASE_ADDRESS + BASE_PORT
REQUEST = "/auth/login/v2"
URL = BASE_URL + REQUEST
REGISTER = BASE_URL + "/auth/register/v2"

def test_account_not_exist():
    response = requests.post(URL, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567'})
    assert response.status_code == 400

def test_incorrect_password():
    requests.post(REGISTER, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    response = requests.post(URL, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '123123123'})
    assert response.status_code == 400

def test_correct_input():
    requests.post(REGISTER, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    response = requests.post(URL, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == 1
    assert str(type(response_data['token'])) == "<class 'str'>"

