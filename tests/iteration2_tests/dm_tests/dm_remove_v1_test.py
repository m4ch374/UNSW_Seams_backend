"""
Test the behaviours of
/dm/remove/v1
"""

# Imports
import requests
from src.error import InputError, AccessError

# Import definitions
from tests.iteration2_tests.endpoints import *

# Import helper
from tests.iteration2_tests.helper import generate_dm_input_json, generate_dm_json

INVALID_TOKEN = 'invalid'
INVALID_DM_ID = -1

def test_invalid_token(get_token_1):
    data = generate_dm_input_json(get_token_1, [])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']

    data = generate_dm_json(INVALID_TOKEN, dm_id)
    resp = requests.delete(ENDPOINT_DM_REMOVE, json=data)

    assert resp.status_code == AccessError.code

def test_invalid_dm_id(get_token_1):
    data = generate_dm_json(get_token_1, INVALID_DM_ID)
    resp = requests.delete(ENDPOINT_DM_REMOVE, json=data)
    assert resp.status_code == InputError.code

def test_not_member(get_token_1, get_token_2):
    data = generate_dm_input_json(get_token_1, [])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']

    data = generate_dm_json(get_token_2, dm_id)
    resp = requests.delete(ENDPOINT_DM_REMOVE, json=data)
    assert resp.status_code == AccessError.code

def test_not_owner(get_token_1, get_usr_2):
    data = generate_dm_input_json(get_token_1, [get_usr_2['auth_user_id']])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']

    data = generate_dm_json(get_usr_2['token'], dm_id)
    resp = requests.delete(ENDPOINT_DM_REMOVE, json=data)
    assert resp.status_code == AccessError.code

def test_global_owner_has_no_permission(get_usr_1, get_usr_2):
    data = generate_dm_input_json(get_usr_2['token'], [])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']

    data = generate_dm_json(get_usr_1['token'], dm_id)
    resp = requests.delete(ENDPOINT_DM_REMOVE, json=data)
    assert resp.status_code == AccessError.code

def test_valid(get_usr_1, get_usr_2):
    data = generate_dm_input_json(get_usr_1['token'], [get_usr_2['auth_user_id']])
    data1 = generate_dm_input_json(get_usr_2['token'], [get_usr_1['auth_user_id']])

    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']
    dm_id1 = requests.post(ENDPOINT_DM_CREATE, json=data1).json()['dm_id']

    handle = requests.get(ENDPOINT_USER_PROF, {'token': get_usr_1['token'], 'u_id': get_usr_1['auth_user_id']})
    handle1 = requests.get(ENDPOINT_USER_PROF, {'token': get_usr_2['token'], 'u_id': get_usr_2['auth_user_id']})
    expected_name = ', '.join(sorted([handle.json()['user']['handle_str'], handle1.json()['user']['handle_str']]))

    expected_output = [
        {
            'dm_id': dm_id,
            'name': expected_name,
        },
        {
            'dm_id': dm_id1,
            'name': expected_name,
        },
    ]

    data = generate_dm_json(get_usr_1['token'], dm_id)
    requests.delete(ENDPOINT_DM_REMOVE, json=data)

    resp = requests.get(ENDPOINT_DM_LIST, {'token': get_usr_1['token']}).json()['dms']
    resp1 = requests.get(ENDPOINT_DM_LIST, {'token': get_usr_2['token']}).json()['dms']

    expected_output.pop(0)

    assert resp == expected_output
    assert resp1 == expected_output

    data = generate_dm_json(get_usr_2['token'], dm_id1)
    requests.delete(ENDPOINT_DM_REMOVE, json=data)

    resp = requests.get(ENDPOINT_DM_LIST, {'token': get_usr_1['token']}).json()['dms']
    resp1 = requests.get(ENDPOINT_DM_LIST, {'token': get_usr_2['token']}).json()['dms']

    expected_output.pop(0)

    assert resp == expected_output
    assert resp1 == expected_output

def test_removed_associated_msg(get_usr_1):
    data = generate_dm_input_json(get_usr_1['token'], [])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']

    msg = {
        'token': get_usr_1['token'],
        'channel_id': dm_id,
        'message': 'hi',
    }
    msg_id = requests.post(ENDPOINT_DM_SEND, json=msg).json()['message_id']

    data = generate_dm_json(get_usr_1['token'], dm_id)
    requests.delete(ENDPOINT_DM_REMOVE, json=data)

    data = {
        'token': get_usr_1['token'],
        'message_id': msg_id,
        'message': 'lmao',
    }
    resp = requests.put(ENDPOINT_MESSAGE_EDIT, json=data)

    assert resp.status_code == InputError.code
