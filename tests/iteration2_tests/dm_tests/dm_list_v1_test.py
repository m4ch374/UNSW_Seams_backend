"""
Test the behaviours of
/dm/list/v1
"""

# Imports
import requests
from src.error import AccessError

# Import definitions
from tests.iteration2_tests.endpoints import *

# Import helper
from tests.iteration2_tests.helper import generate_dm_input_json

from src.data_store import data_store

INVALID_TOKEN = 'invalid'

def test_invalid_token():
    resp = requests.get(ENDPOINT_DM_LIST)
    assert resp.status_code == AccessError.code

def test_empty(get_token_1):
    resp = requests.get(ENDPOINT_DM_LIST, {'token': get_token_1})
    assert resp.status_code == 200
    assert resp.json()['dms'] == []

def test_one_person(get_usr_1):
    data = generate_dm_input_json(get_usr_1['token'], [])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']
    args = {
        'token': get_usr_1['token'], 
        'u_id': get_usr_1['auth_user_id'],
    }
    handle = requests.get(ENDPOINT_USER_PROF, args).json()['user']['handle_str']
    resp = requests.get(ENDPOINT_DM_LIST, {'token': get_usr_1['token']}).json()['dms']
    expected_output = [
        {
            'dm_id': dm_id,
            'name': handle, 
        }
    ]
    assert resp == expected_output

def test_multiple_person(get_usr_1, get_usr_2):
    data = generate_dm_input_json(get_usr_1['token'], [get_usr_2['auth_user_id']])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']
    args = {
        'token': get_usr_1['token'],
        'u_id': get_usr_1['auth_user_id'],
    }

    args2 = {
        'token': get_usr_2['token'],
        'u_id': get_usr_2['auth_user_id'],
    }
    handle1 = requests.get(ENDPOINT_USER_PROF, args).json()['user']['handle_str']
    handle2 = requests.get(ENDPOINT_USER_PROF, args2).json()['user']['handle_str']
    resp = requests.get(ENDPOINT_DM_LIST, {'token': get_usr_1['token']}).json()['dms']
    resp1 = requests.get(ENDPOINT_DM_LIST, {'token': get_usr_2['token']}).json()['dms']
    expected_output = [
        {
            'dm_id': dm_id,
            'name': ', '.join(sorted([handle1, handle2]))
        }
    ]
    assert resp == expected_output
    assert resp1 == expected_output

def test_multiple_dms(get_usr_1, get_usr_2):
    data = generate_dm_input_json(get_usr_1['token'], [get_usr_2['auth_user_id']])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']
    data2 = generate_dm_input_json(get_usr_2['token'], [get_usr_1['auth_user_id']])
    dm_id2 = requests.post(ENDPOINT_DM_CREATE, json=data2).json()['dm_id']
    args = {
        'token': get_usr_1['token'],
        'u_id': get_usr_1['auth_user_id'],
    }

    args2 = {
        'token': get_usr_2['token'],
        'u_id': get_usr_2['auth_user_id'],
    }
    handle1 = requests.get(ENDPOINT_USER_PROF, args).json()['user']['handle_str']
    handle2 = requests.get(ENDPOINT_USER_PROF, args2).json()['user']['handle_str']
    resp = requests.get(ENDPOINT_DM_LIST, {'token': get_usr_1['token']}).json()['dms']
    resp1 = requests.get(ENDPOINT_DM_LIST, {'token': get_usr_2['token']}).json()['dms']
    expected_output = [
        {
            'dm_id': dm_id,
            'name': ', '.join(sorted([handle1, handle2]))
        },
        {
            'dm_id': dm_id2,
            'name': ', '.join(sorted([handle1, handle2]))
        }
    ]
    assert resp == expected_output
    assert resp1 == expected_output
