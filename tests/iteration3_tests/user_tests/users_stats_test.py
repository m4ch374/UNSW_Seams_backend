import requests
from tests.iteration3_tests.user_tests.definitions import USERS_STATS_V1, REGISTER_V2


def test_invalid_token():
    json = {'token': 'xxxxxxxxxxxx'}
    response = requests.post(USERS_STATS_V1, json = json)
    assert response.status_code == 403

def test_valid_input():
    requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    requests.post(REGISTER_V2, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'})
    requests.post(REGISTER_V2, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'})
    user = requests.post(REGISTER_V2, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
    user_data = user.json()
    #TODO
    json = {'token': user_data['token']}
    response = requests.post(USERS_STATS_V1, json = json)
    assert response.status_code == 200
    workspace_stats = response.json()['workspace_stats']
    assert workspace_stats['channels_exist'] == []
    assert workspace_stats['dms_exist'] == []
    assert workspace_stats['messages_exist'] == []
    assert type(workspace_stats['utilization_rate']) == type(1.2345)

