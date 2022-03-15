import requests

BASE_ADDRESS = 'http://localhost:'
BASE_PORT = '30000'
BASE_URL = BASE_ADDRESS + BASE_PORT
REQUEST = "/users/all/v1"
URL = BASE_URL + REQUEST
REGISTER = BASE_URL + "/auth/register/v2"

def test_invalid_token():
    response = requests.get(URL, json = {'token': '123123123123123'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == None

def test_1_user():
    user = requests.post(REGISTER, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    user_data = user.json()
    response = requests.get(URL, {'token': user_data['token']})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == [{'id': 1, 'email': 'z1234567@ed.unsw.edu.au', 'name_first': 'Donald', 'name_last': 'Trump',  'handle': 'donaldtrump'}]

def test_2_user():
    user = requests.post(REGISTER, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.get(URL, {'token': user_data['token']})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == [{'id': 1, 'email': 'z8888888@ed.unsw.edu.au', 'name_first': 'Russell', 'name_last': 'Wang', 'handle': 'russellwang'},
                            {'id': 2, 'email': 'z5555555@ed.unsw.edu.au', 'name_first': 'William', 'name_last': 'Wu',  'handle': 'williamwu'}]

