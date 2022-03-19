import requests
from tests.iteration2_tests.user_tests.definitions import REGISTER_V2, USERS_ALL_V1


def test_invalid_token():
    response = requests.get(USERS_ALL_V1, json = {'token': '123123123123123'})
    assert response.status_code == 403

def test_1_user():
    user = requests.post(REGISTER_V2, json = {'email': 'z1234567@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Donald', 'name_last': 'Trump'})
    user_data = user.json()
    response = requests.get(USERS_ALL_V1, {'token': user_data['token']})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'users': [{'u_id': 1, 'email': 'z1234567@ed.unsw.edu.au', 'name_first': 'Donald', 'name_last': 'Trump',  'handle_str': 'donaldtrump'}]}

def test_2_user():
    user = requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.get(USERS_ALL_V1, {'token': user_data['token']})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'users': [{'u_id': 1, 'email': 'z8888888@ed.unsw.edu.au', 'name_first': 'Russell', 'name_last': 'Wang', 'handle_str': 'russellwang'},
                            {'u_id': 2, 'email': 'z5555555@ed.unsw.edu.au', 'name_first': 'William', 'name_last': 'Wu',  'handle_str': 'williamwu'}]}

