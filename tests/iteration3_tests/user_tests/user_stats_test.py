import requests
from tests.iteration3_tests.user_tests.definitions import REGISTER_V2, USER_STATS_V1, ENDPOINT_CREATE_CHNL, ENDPOINT_CHNL_INVITE, ENDPOINT_MESSAGE_SEND


def test_invalid_token():
    response = requests.get(USER_STATS_V1, {'token': 'xxxxxxxxxxxx'})
    assert response.status_code == 403

def test_valid_input():
    requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(REGISTER_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(REGISTER_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    #TODO
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user_data['token'],'name':"123", 'is_public':False})
    requests.post(ENDPOINT_CHNL_INVITE, json = {'token':user_data['token'],'channel_id':1, 'u_id':2})
    requests.post(ENDPOINT_MESSAGE_SEND, json = {'token':user_data['token'],'channel_id':1, 'message':'qqq'})
    response = requests.get(USER_STATS_V1, {'token': user_data['token']})
    assert response.status_code == 200
    workspace_stats = response.json()['user_stats']
    assert workspace_stats['channels_joined'][0]['num_channels_joined'] == 1
    assert workspace_stats['dms_joined'][0]['num_dms_joined'] == 0
    assert workspace_stats['messages_sent'][0]['num_messages_sent'] == 1
    assert type(workspace_stats['involvement_rate']) == type(1.2345)

