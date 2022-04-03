"""
This tests for the behaviour of route
/message/react/v1
"""

# Import
import requests
from src.error import InputError, AccessError

# Import definitions
from tests.iteration3_tests.endpoints import *

# Definitions
INVALID_TOKEN = 'invalid'
REACT_ID = 1
INVALID_REACT = -1

def test_invalid_token(get_usr_1):
    data = {
        'token': get_usr_1['token'],
        'name': "random name",
        'is_public': True,
    }
    chnl_id = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()['channel_id']

    data = {
        'token': get_usr_1['token'],
        'channel_id': chnl_id,
        'message': "lmao",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']
    
    data = {
        'token': INVALID_TOKEN,
        'message_id': msg_id,
        'react_id': REACT_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_REACT, json=data)
    assert resp.status_code == AccessError.code

def test_invalid_msg_id(get_usr_1, get_usr_2):
    data = {
        'token': get_usr_1['token'],
        'name': "random name",
        'is_public': True,
    }
    chnl1_id = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()['channel_id']

    data = {
        'token': get_usr_2['token'],
        'name': "another name",
        'is_public': True,
    }
    requests.post(ENDPOINT_CREATE_CHNL, json=data).json()['channel_id']

    data = {
        'token': get_usr_1['token'],
        'channel_id': chnl1_id,
        'message': "lmao",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']

    data = {
        'token': get_usr_2['token'],
        'message_id': msg_id,
        'react_id': REACT_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_REACT, json=data)
    assert resp.status_code == InputError.code

def test_invalid_react_id(get_usr_1):
    data = {
        'token': get_usr_1['token'],
        'name': "random name",
        'is_public': True,
    }
    chnl_id = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()['channel_id']

    data = {
        'token': get_usr_1['token'],
        'channel_id': chnl_id,
        'message': "lmao",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']

    data = {
        'token': get_usr_1['token'],
        'message_id': msg_id,
        'react_id': INVALID_REACT,
    }
    resp = requests.post(ENDPOINT_MESSAGE_REACT, json=data)
    assert resp.status_code == InputError.code

def test_already_reacted(get_usr_1):
    data = {
        'token': get_usr_1['token'],
        'name': "random name",
        'is_public': True,
    }
    chnl_id = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()['channel_id']

    data = {
        'token': get_usr_1['token'],
        'channel_id': chnl_id,
        'message': "lmao",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']

    data = {
        'token': get_usr_1['token'],
        'message_id': msg_id,
        'react_id': REACT_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_REACT, json=data)
    assert resp.status_code == 200

    data = {
        'token': get_usr_1['token'],
        'message_id': msg_id,
        'react_id': REACT_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_REACT, json=data)
    assert resp.status_code == InputError.code

def test_valid(get_usr_1):
    data = {
        'token': get_usr_1['token'],
        'name': "random name",
        'is_public': True,
    }
    chnl_id = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()['channel_id']

    data = {
        'token': get_usr_1['token'],
        'channel_id': chnl_id,
        'message': "lmao",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']

    data = {
        'token': get_usr_1['token'],
        'message_id': msg_id,
        'react_id': REACT_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_REACT, json=data)
    assert resp.status_code == 200

    data = {
        'token': get_usr_1['token'],
        'channel_id': chnl_id,
        'start': 0
    }
    msg = requests.get(ENDPOINT_CHANNEL_MESSAGE, params=data).json()['messages'][0]

    assert msg['reacts'][0]['is_this_user_reacted']
