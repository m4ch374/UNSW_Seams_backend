import requests
from tests.iteration3_tests.endpoints import ENDPOINT_REGISTER_USR, ENDOPINT_SEARCH, ENDPOINT_CHNL_INVITE, ENDPOINT_CREATE_CHNL, ENDPOINT_MESSAGE_SEND, ENDPOINT_DM_CREATE, ENDPOINT_DM_SEND


def test_invalid_token():
    response = requests.get(ENDOPINT_SEARCH, {'token': '123', 'query_str': "123213"})
    assert response.status_code == 403

def test_invalid_query_str():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z7654321@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'Jason', 'name_last': 'Smith'})
    assert user.status_code == 200
    user_data = user.json()
    response = requests.get(ENDOPINT_SEARCH, {'token': user_data['token'], 'query_str': ''})
    assert response.status_code == 400
    response = requests.get(ENDOPINT_SEARCH, {'token': user_data['token'], 'query_str': 'q' * 1001})
    assert response.status_code == 400

def test_valid_input_ch():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    user2 = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'}).json()
    user_data = user.json()
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user_data['token'],'name':"123", 'is_public':False})
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':user2['token'],'name':"1234", 'is_public':False})
    requests.post(ENDPOINT_CHNL_INVITE, json = {'token':user_data['token'],'channel_id':1, 'u_id':2})
    requests.post(ENDPOINT_MESSAGE_SEND, json = {'token':user_data['token'],'channel_id':1, 'message':'qqq'})
    requests.post(ENDPOINT_MESSAGE_SEND, json = {'token':user_data['token'],'channel_id':1, 'message':'zzzz'})
    response = requests.get(ENDOPINT_SEARCH, {'token': user_data['token'], 'query_str': 'q'})
    requests.get(ENDOPINT_SEARCH, {'token': user2['token'], 'query_str': 'q'})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['messages']) == 1

def test_valid_input_dm():
    user = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'})
    user2 = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'}).json()
    user_data = user.json()
    requests.post(ENDPOINT_DM_CREATE, json = {'token':user_data['token'],'u_ids':[]})
    requests.post(ENDPOINT_DM_CREATE, json = {'token':user2['token'],'u_ids':[]})
    requests.post(ENDPOINT_DM_SEND, json = {'token':user_data['token'],'dm_id':1, 'message':'qqq'})
    requests.post(ENDPOINT_DM_SEND, json = {'token':user2['token'],'dm_id':2, 'message':'qqqq'})
    response = requests.get(ENDOPINT_SEARCH, {'token': user_data['token'], 'query_str': 'q'})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['messages']) == 1

