import requests
from tests.iteration3_tests.user_tests.definitions import REGISTER_V2, AUTH_PASSWORDRESET_RESET_V1

def test_invalid_reset_code():
    pass
    # requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    # response = requests.post(AUTH_PASSWORDRESET_RESET_V1, json = {'reset_code': '123', 'new_password ': '1234567'})
    # assert response.status_code == 400

def test_short_password():
    pass
    # requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    # #TODO
    # reset_code = '1'
    # response = requests.post(AUTH_PASSWORDRESET_RESET_V1, json = {'reset_code': reset_code, 'new_password ': '123'})
    # assert response.status_code == 400

def test_valid_input():
    pass
    # requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    # #TODO
    # reset_code = '1'
    # response = requests.post(AUTH_PASSWORDRESET_RESET_V1, json = {'reset_code': reset_code, 'new_password ': '1234567'})
    # assert response.status_code == 200
    # response_data = response.json()
    # assert response_data == {}

