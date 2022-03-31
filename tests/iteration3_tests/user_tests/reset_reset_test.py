import requests
from tests.iteration3_tests.user_tests.definitions import REGISTER_V2, AUTH_PASSWORDRESET_RESET_V1, AUTH_PASSWORDRESET_REQUEST_V1


def test_invalid_reset_code():
    requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(AUTH_PASSWORDRESET_REQUEST_V1, json = {'email': 'z8888888@ed.unsw.edu.au'})
    response = requests.post(AUTH_PASSWORDRESET_RESET_V1, json = {'reset_code': '123', 'new_password ': '1234567'})
    assert response.status_code == 400

def test_short_password():
    requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(AUTH_PASSWORDRESET_REQUEST_V1, json = {'email': 'z8888888@ed.unsw.edu.au'})
    #TODO
    reset_code = '1'
    response = requests.post(AUTH_PASSWORDRESET_RESET_V1, json = {'reset_code': reset_code, 'new_password ': '123'})
    assert response.status_code == 400

def test_valid_input():
    requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(REGISTER_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(REGISTER_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(AUTH_PASSWORDRESET_REQUEST_V1, json = {'email': 'z8888888@ed.unsw.edu.au'})
    #TODO
    reset_code = '1'
    response = requests.post(AUTH_PASSWORDRESET_RESET_V1, json = {'reset_code': reset_code, 'new_password ': '1234567'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

