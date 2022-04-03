"""
This tests for the behaviour of route
/message/share/v1
"""

# Import
import requests
from src.error import InputError, AccessError

# Import definitions
from tests.iteration3_tests.endpoints import *

# Definitions
INVALID_TOKEN = 'invalid'
INVALID_CHNL_ID = -1
INVALID_DM_ID = -1
NON_EXIST_MSG_ID = -1

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
        'og_message_id': msg_id,
        'message': '',
        'channel_id': chnl_id,
        'dm_id': INVALID_DM_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_SHARE, json=data)
    assert resp.status_code == AccessError.code

def test_both_are_invalid_id(get_usr_1):
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
        'og_message_id': msg_id,
        'message': '',
        'channel_id': INVALID_CHNL_ID,
        'dm_id': INVALID_DM_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_SHARE, json=data)
    assert resp.status_code == InputError.code

def test_neither_are_negative_one(get_usr_1):
    data = {
        'token': get_usr_1['token'],
        'name': "random name",
        'is_public': True,
    }
    chnl_id = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()['channel_id']

    data = {
        'token': get_usr_1['token'],
        'u_ids': [],
    }
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']

    data = {
        'token': get_usr_1['token'],
        'channel_id': chnl_id,
        'message': "lmao",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']

    data = {
        'token': get_usr_1['token'],
        'og_message_id': msg_id,
        'message': '',
        'channel_id': chnl_id,
        'dm_id': dm_id,
    }
    resp = requests.post(ENDPOINT_MESSAGE_SHARE, json=data)
    assert resp.status_code == InputError.code

def test_non_exist_msg_id(get_usr_1):
    data = {
        'token': get_usr_1['token'],
        'name': "random name",
        'is_public': True,
    }
    chnl_id = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()['channel_id']

    data = {
        'token': get_usr_1['token'],
        'og_message_id': NON_EXIST_MSG_ID,
        'message': '',
        'channel_id': chnl_id,
        'dm_id': INVALID_DM_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_SHARE, json=data)
    assert resp.status_code == InputError.code

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
    requests.post(ENDPOINT_CREATE_CHNL, json=data)

    data = {
        'token': get_usr_1['token'],
        'channel_id': chnl1_id,
        'message': "lmao",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']

    data = {
        'token': get_usr_2['token'],
        'og_message_id': msg_id,
        'message': '',
        'channel_id': chnl1_id,
        'dm_id': INVALID_DM_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_SHARE, json=data)
    assert resp.status_code == InputError.code

def test_more_than_thousand_char(get_usr_1):
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
        'og_message_id': msg_id,
        'message': ''.join(str(i) for i in range(1000)),
        'channel_id': chnl_id,
        'dm_id': INVALID_DM_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_SHARE, json=data)
    assert resp.status_code == InputError.code

def test_share_to_non_joined_chnl(get_usr_1, get_usr_2):
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
    chnl2_id = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()['channel_id']

    data = {
        'token': get_usr_1['token'],
        'channel_id': chnl1_id,
        'message': "lmao",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']

    data = {
        'token': get_usr_1['token'],
        'og_message_id': msg_id,
        'message': '',
        'channel_id': chnl2_id,
        'dm_id': INVALID_DM_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_SHARE, json=data)
    assert resp.status_code == AccessError.code

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
        'og_message_id': msg_id,
        'message': '',
        'channel_id': chnl_id,
        'dm_id': INVALID_DM_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_SHARE, json=data)
    assert resp.status_code == 200
