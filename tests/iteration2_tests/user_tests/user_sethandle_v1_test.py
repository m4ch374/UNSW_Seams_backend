import requests

BASE_ADDRESS = 'http://localhost:'
BASE_PORT = '30000'
BASE_URL = BASE_ADDRESS + BASE_PORT
REQUEST = "/user/profile/sethandle/v1"
URL = BASE_URL + REQUEST
REGISTER = BASE_URL + "/auth/register/v2"

def test_invalid_token():
    response = requests.put(URL, json = {'token': '123123123123123', 'handle_str': '123123123123'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == None

def test_long_handle():
    long_handle = 'x' * 21
    user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(URL, json = {'token': user_data['token'], 'handle_str': long_handle})
    assert response.status_code == 400

def test_short_handle():
    short_handle = 'x'
    user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(URL, json = {'token': user_data['token'], 'handle_str': short_handle})
    assert response.status_code == 400

def test_invalid_handle():
    invalid_handle = 'asd123!@#'
    user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(URL, json = {'token': user_data['token'], 'handle_str': invalid_handle})
    assert response.status_code == 400

def test_exist_handle():
    exist_handle = 'williamwu'
    user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(URL, json = {'token': user_data['token'], 'handle_str': exist_handle})
    assert response.status_code == 400

def test_valid_input():
    new_handle = 'asdasdasd'
    user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.put(URL, json = {'token': user_data['token'], 'handle_str': new_handle})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

