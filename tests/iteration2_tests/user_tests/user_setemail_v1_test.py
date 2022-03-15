import requests

BASE_ADDRESS = 'http://localhost:'
BASE_PORT = '30000'
BASE_URL = BASE_ADDRESS + BASE_PORT
REQUEST = "/user/profile/setemail/v1"
URL = BASE_URL + REQUEST
REGISTER = BASE_URL + "/auth/register/v2"

def test_invalid_token():
    response = requests.put(URL, json = {'token': '123123123123123', 'email': 'z5555555@ed.unsw.edu.au'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == None

def test_invalid_email():
    user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(URL, json = {'token': user_data['token'], 'email': '123123'})
    assert response.status_code == 400

def test_exist_email():
    user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(URL, json = {'token': user_data['token'], 'email': 'z5555555@ed.unsw.edu.au'})
    assert response.status_code == 400

def test_valid_input():
    user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(URL, json = {'token': user_data['token'], 'email': '987654321@unsw.edu.au'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

