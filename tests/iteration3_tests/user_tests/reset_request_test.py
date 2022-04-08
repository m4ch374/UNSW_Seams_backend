import requests
from tests.iteration3_tests.endpoints import ENDPOINT_REGISTER_USR, ENDPOINT_PWORD_REQUEST

def test_invalid_email():
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Russell', 'name_last': 'Wang'})
    response = requests.post(ENDPOINT_PWORD_REQUEST, json = {'email': '123'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

def test_valid_email():
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Russell', 'name_last': 'Wang'})
    response = requests.post(ENDPOINT_PWORD_REQUEST, json = {'email': 'z8888888@ed.unsw.edu.au'})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

