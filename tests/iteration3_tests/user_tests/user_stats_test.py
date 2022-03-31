import requests
from tests.iteration3_tests.user_tests.definitions import REGISTER_V2, USER_STATS_V1


def test_invalid_token():
    json = {'token': 'xxxxxxxxxxxx'}
    response = requests.post(USER_STATS_V1, json = json)
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
    response = requests.post(USER_STATS_V1, json = json)
    assert response.status_code == 200
    user_stats = response.json()['user_stats']
    assert user_stats['channels_joined'] == []
    assert user_stats['dms_joined'] == []
    assert user_stats['messages_sent'] == []
    assert type(user_stats['involvement_rate']) == type(1.2345)

