import requests, time
from tests.iteration3_tests.user_tests.definitions import REGISTER_V2, SENDLATER, ENDPOINT_CREATE_CHNL
from src.time import get_time


def test_invalid_token():
    json = {'token': 'xxxxxxxxxxxx', 'channel_id':1, 'message':'', 'time_sent':0}
    response = requests.post(SENDLATER, json = json)
    assert response.status_code == 403

def test_invalid_ch_id():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    json = {'token': user['token'], 'channel_id':2, 'message':'', 'time_sent':0}
    response = requests.post(SENDLATER, json = json)
    assert response.status_code == 400

def test_not_a_member():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user['token'],'name':"123", 'is_public':False})
    user = requests.post(REGISTER_V2, json = {'email': 'z555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    json = {'token': user['token'], 'channel_id':1, 'message':'', 'time_sent':0}
    response = requests.post(SENDLATER, json = json)
    assert response.status_code == 403

def test_short_msg():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user['token'],'name':"123", 'is_public':False})
    json = {'token': user['token'], 'channel_id':1, 'message':'', 'time_sent':0}
    response = requests.post(SENDLATER, json = json)
    assert response.status_code == 400

def test_long_msg():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user['token'],'name':"123", 'is_public':False})
    json = {'token': user['token'], 'channel_id':1, 'message':'q'*1001, 'time_sent':0}
    response = requests.post(SENDLATER, json = json)
    assert response.status_code == 400

def test_past_time():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user['token'],'name':"123", 'is_public':False})
    json = {'token': user['token'], 'channel_id':1, 'message':'123123', 'time_sent':1649020253}
    response = requests.post(SENDLATER, json = json)
    assert response.status_code == 400

def test_valid_input():
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user['token'],'name':"123", 'is_public':False})
    json = {'token': user['token'], 'channel_id':1, 'message':'123123', 'time_sent':int(get_time()) + 3}
    response = requests.post(SENDLATER, json = json)
    time.sleep(3)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'message_id': 1}

