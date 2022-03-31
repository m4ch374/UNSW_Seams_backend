import requests
from tests.iteration3_tests.user_tests.definitions import USER_PROFILE_UPLOADPHOTO_V1, REGISTER_V2


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
    #TODO
    size = 99999999
    json = {'token': user_data['token'], 'img_url':'asdasdasd', 'x_start': size, 'y_start': size, 'x_end': size, 'y_end': size}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 400

def test_invalid_range():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    #TODO
    json = {'token': user_data['token'], 'img_url':'asdasdasd', 'x_start': 10, 'y_start': 10, 'x_end': 5, 'y_end': 5}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 400

def test_not_jpg():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    #TODO
    json = {'token': user_data['token'], 'img_url':'asdasdasd', 'x_start': 0, 'y_start': 0, 'x_end': 1, 'y_end': 1}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 400

def test_valid_input():
    requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(REGISTER_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(REGISTER_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    #TODO
    json = {'token': user_data['token'], 'img_url':'asdasdasd', 'x_start': 0, 'y_start': 0, 'x_end': 1, 'y_end': 1}
    response = requests.post(USER_PROFILE_UPLOADPHOTO_V1, json = json)
    assert response.status_code == 200
    assert response.json() == {}

