import requests
from tests.iteration3_tests.endpoints import ENDPOINT_USER_UPLOAD_PHOTO, ENDPOINT_REGISTER_USR
# 771 * 480
JPG = 'http://t4.ftcdn.net/jpg/02/29/75/83/360_F_229758328_7x8jwCwjtBMmC6rgFzLFhZoEpLobB6L8.jpg'
PNG = 'http://cdn.onlinewebfonts.com/svg/img_527746.png'


def test_invalid_token():
    json = {'token': 'xxxxxxxxxxxx', 'img_url':'', 'x_start':0, 'y_start':0, 'x_end':0, 'y_end':0}
    response = requests.post(ENDPOINT_USER_UPLOAD_PHOTO, json = json)
    assert response.status_code == 403

def test_invalid_url():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    json = {'token': user_data['token'], 'img_url':'http://webcms3.cse.unsw.edu.au/COMP1531', 'x_start':0, 'y_start':0, 'x_end':0, 'y_end':0}
    response = requests.post(ENDPOINT_USER_UPLOAD_PHOTO, json = json)
    assert response.status_code == 400

def test_invalid_size():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    size = 9999
    json = {'token': user_data['token'], 'img_url': JPG, 'x_start': 0, 'y_start': 0, 'x_end': size, 'y_end': size}
    response = requests.post(ENDPOINT_USER_UPLOAD_PHOTO, json = json)
    assert response.status_code == 400

def test_invalid_range():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    json = {'token': user_data['token'], 'img_url': JPG, 'x_start': 10, 'y_start': 10, 'x_end': 5, 'y_end': 5}
    response = requests.post(ENDPOINT_USER_UPLOAD_PHOTO, json = json)
    assert response.status_code == 400

def test_not_jpg():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    json = {'token': user_data['token'], 'img_url': PNG, 'x_start': 0, 'y_start': 0, 'x_end': 1, 'y_end': 1}
    response = requests.post(ENDPOINT_USER_UPLOAD_PHOTO, json = json)
    assert response.status_code == 400

def test_valid_input():
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    json = {'token': user_data['token'], 'img_url': JPG, 'x_start': 0, 'y_start': 0, 'x_end': 1, 'y_end': 1}
    response = requests.post(ENDPOINT_USER_UPLOAD_PHOTO, json = json)
    assert response.status_code == 200
    assert response.json() == {}

