import requests
from tests.iteration3_tests.endpoints import ENDPOINT_REGISTER_USR, ENDPOINT_USER_STATS, ENDPOINT_CREATE_CHNL, ENDPOINT_CHNL_INVITE, ENDPOINT_MESSAGE_SEND


def test_invalid_token():
    response = requests.get(ENDPOINT_USER_STATS, {'token': 'xxxxxxxxxxxx'})
    assert response.status_code == 403

def test_valid_input():
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user_data['token'],'name':"123", 'is_public':False})
    requests.post(ENDPOINT_CHNL_INVITE, json = {'token':user_data['token'],'channel_id':1, 'u_id':2})
    requests.post(ENDPOINT_MESSAGE_SEND, json = {'token':user_data['token'],'channel_id':1, 'message':'qqq'})
    response = requests.get(ENDPOINT_USER_STATS, {'token': user_data['token']})
    assert response.status_code == 200
    user_stats = response.json()['user_stats']
    assert len(user_stats['channels_joined']) == 2
    assert len(user_stats['dms_joined']) == 1
    assert len(user_stats['messages_sent']) == 2
    assert type(user_stats['involvement_rate']) == type(1.2345)

def test_valid_input_1():
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    response = requests.get(ENDPOINT_USER_STATS, {'token': user_data['token']})
    assert response.status_code == 200
    user_stats = response.json()['user_stats']
    assert len(user_stats['channels_joined']) == 1
    assert len(user_stats['dms_joined']) == 1
    assert len(user_stats['messages_sent']) == 1
    assert type(user_stats['involvement_rate']) == type(1.2345)

