import requests
from tests.iteration2_tests.user_tests.definitions import REGISTER_V2, USER_PROFIILE_V1


def test_invalid_token():
    response = requests.get(USER_PROFIILE_V1, {'token': '123123123123123', 'u_id': 1})
    assert response.status_code == 403

def test_self_detail():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.get(USER_PROFIILE_V1, {'token': user_data['token'], 'u_id': user_data['auth_user_id']})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['user']['u_id'] == 1
    assert response_data['user']['email'] == 'z5555555@ed.unsw.edu.au'
    assert response_data['user']['name_first'] == 'William'
    assert response_data['user']['name_last'] == 'Wu'
    assert response_data['user']['handle_str'] == 'williamwu'

def test_other_detail():
    user = requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.get(USER_PROFIILE_V1, {'token': user_data['token'], 'u_id': 2})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['user']['u_id'] == 2
    assert response_data['user']['email'] == 'z5555555@ed.unsw.edu.au'
    assert response_data['user']['name_first'] == 'William'
    assert response_data['user']['name_last'] == 'Wu'
    assert response_data['user']['handle_str'] == 'williamwu'

def test_error_id():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.get(USER_PROFIILE_V1, {'token': user_data['token'], 'u_id': 2})
    assert response.status_code == 400

