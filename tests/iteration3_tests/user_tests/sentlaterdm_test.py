import requests
from tests.iteration3_tests.endpoints import ENDPOINT_REGISTER_USR, ENDPOINT_MESSAGE_SENDLATERDM, ENDPOINT_DM_CREATE


def test_invalid_token():
    json = {'token': 'xxxxxxxxxxxx', 'dm_id':1, 'message':'', 'time_sent':0}
    response = requests.post(ENDPOINT_MESSAGE_SENDLATERDM, json = json)
    assert response.status_code == 403

def test_invalid_ch_id():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    json = {'token': user['token'], 'dm_id':2, 'message':'', 'time_sent':0}
    response = requests.post(ENDPOINT_MESSAGE_SENDLATERDM, json = json)
    assert response.status_code == 400

def test_not_a_member():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_DM_CREATE, json = {'token':user['token'],'u_ids':[]})
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    json = {'token': user['token'], 'dm_id':1, 'message':'', 'time_sent':0}
    response = requests.post(ENDPOINT_MESSAGE_SENDLATERDM, json = json)
    assert response.status_code == 403

def test_short_msg():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_DM_CREATE, json = {'token':user['token'],'u_ids':[]})
    json = {'token': user['token'], 'dm_id':1, 'message':'', 'time_sent':0}
    response = requests.post(ENDPOINT_MESSAGE_SENDLATERDM, json = json)
    assert response.status_code == 400

def test_long_msg():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_DM_CREATE, json = {'token':user['token'],'u_ids':[]})
    json = {'token': user['token'], 'dm_id':1, 'message':'q'*1001, 'time_sent':0}
    response = requests.post(ENDPOINT_MESSAGE_SENDLATERDM, json = json)
    assert response.status_code == 400

def test_past_time():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_DM_CREATE, json = {'token':user['token'],'u_ids':[]})
    json = {'token': user['token'], 'dm_id':1, 'message':'123123', 'time_sent':1649020253}
    response = requests.post(ENDPOINT_MESSAGE_SENDLATERDM, json = json)
    assert response.status_code == 400

def test_valid_input():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'}).json()
    requests.post(ENDPOINT_DM_CREATE, json = {'token':user['token'],'u_ids':[]})
    json = {'token': user['token'], 'dm_id':1, 'message':'123123', 'time_sent':2649020253}
    response = requests.post(ENDPOINT_MESSAGE_SENDLATERDM, json = json)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'message_id': 1}

