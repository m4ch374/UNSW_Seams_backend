import requests
from tests.iteration3_tests.user_tests.definitions import USER_PROFILE_UPLOADPHOTO_V1, REGISTER_V2
# 771 * 480
JPG = 'data:image/jpeg;base64,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'
PNG = 'http://cdn.onlinewebfonts.com/svg/img_527746.png'


def test_invalid_token():
    json = {'token': 'xxxxxxxxxxxx', 'img_url':'', 'x_start':0, 'y_start':0, 'x_end':0, 'y_end':0}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 403

def test_invalid_url():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    json = {'token': user_data['token'], 'img_url':'asdasdasd', 'x_start':0, 'y_start':0, 'x_end':0, 'y_end':0}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 400

def test_invalid_size():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    size = 9999
    json = {'token': user_data['token'], 'img_url': JPG, 'x_start': size, 'y_start': size, 'x_end': size, 'y_end': size}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 400

def test_invalid_range():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    json = {'token': user_data['token'], 'img_url': JPG, 'x_start': 10, 'y_start': 10, 'x_end': 5, 'y_end': 5}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 400

def test_not_jpg():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    json = {'token': user_data['token'], 'img_url': PNG, 'x_start': 0, 'y_start': 0, 'x_end': 1, 'y_end': 1}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 400

def test_valid_input():
    requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(REGISTER_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(REGISTER_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    json = {'token': user_data['token'], 'img_url': JPG, 'x_start': 0, 'y_start': 0, 'x_end': 1, 'y_end': 1}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 200
    assert response.json() == {}

