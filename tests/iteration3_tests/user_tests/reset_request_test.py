import requests
from tests.iteration3_tests.user_tests.definitions import REGISTER_V2, AUTH_PASSWORDRESET_REQUEST_V1

def test_invalid_email():
    pass
    # requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Russell', 'name_last': 'Wang'})
    # response = requests.post(AUTH_PASSWORDRESET_REQUEST_V1, json = {'email': '123'})
    # assert response.status_code == 200
    # response_data = response.json()
    # assert response_data == {}

def test_valid_email():
    pass
    # requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Russell', 'name_last': 'Wang'})
    # response = requests.post(AUTH_PASSWORDRESET_REQUEST_V1, json = {'email': 'z8888888@ed.unsw.edu.au'})
    # assert response.status_code == 200
    # response_data = response.json()
    # assert response_data == {}

