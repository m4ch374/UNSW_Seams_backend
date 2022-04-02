import requests
from tests.iteration3_tests.user_tests.definitions import REGISTER_V2, SEARCH, ENDPOINT_CHNL_INVITE, ENDPOINT_CREATE_CHNL, ENDPOINT_MESSAGE_SEND


def test_invalid_token():
    response = requests.get(SEARCH, {'token': '123', 'query_str': "123213"})
    assert response.status_code == 403

def test_invalid_query_str():
    user = requests.post(REGISTER_V2, json = {'email': 'z7654321@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Jason', 'name_last': 'Smith'})
    assert user.status_code == 200
    user_data = user.json()
    response = requests.get(SEARCH, {'token': user_data['token'], 'query_str': ''})
    assert response.status_code == 400
    response = requests.get(SEARCH, {'token': user_data['token'], 'query_str': 'q' * 1001})
    assert response.status_code == 400

def test_valid_input():
    user = requests.post(REGISTER_V2, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    requests.post(REGISTER_V2, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'})
    user_data = user.json()
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user_data['token'],'name':"123", 'is_public':False})
    requests.post(ENDPOINT_CHNL_INVITE, json = {'token':user_data['token'],'channel_id':1, 'u_id':2})
    requests.post(ENDPOINT_MESSAGE_SEND, json = {'token':user_data['token'],'channel_id':1, 'message':'qqq'})
    response = requests.get(SEARCH, {'token': user_data['token'], 'query_str': 'q'})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['messages']) == 1

