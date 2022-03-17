"""
Test the behaviours of 
/dm/leave/v1
"""

# Imports
import code
import requests
from src.error import AccessError, InputError

# Import definitions
from tests.iteration2_tests.endpoints import *

# Import helpers
from tests.iteration2_tests.helper import generate_dm_input_json, generate_dm_json

INVALID_TOKEN = 'invalid'
INVALID_DM_ID = -1

def test_invalid_token(get_token_1):
    data = generate_dm_input_json(get_token_1, [])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']

    data = generate_dm_json(INVALID_TOKEN, dm_id)
    resp = requests.post(ENDPOINT_DM_LEAVE, json=data)

    assert resp.status_code == AccessError.code

def test_invalid_dm_id(get_token_1):
    data = generate_dm_json(get_token_1, INVALID_DM_ID)
    resp = requests.post(ENDPOINT_DM_LEAVE, json=data)
    assert resp.status_code == InputError.code

def test_not_a_member(get_token_1, get_token_2):
    data = generate_dm_input_json(get_token_1, [])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']

    data = generate_dm_json(get_token_2, dm_id)
    resp = requests.post(ENDPOINT_DM_LEAVE, json=data)
    assert resp.status_code == AccessError.code

def test_valid(get_usr_1, get_usr_2):
    data = generate_dm_input_json(get_usr_1['token'], [get_usr_2['auth_user_id']])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']

    data = generate_dm_json(get_usr_2['token'], dm_id)
    resp = requests.get(ENDPOINT_DM_DETAILS, data)
    name = resp.json()['name']

    data = generate_dm_json(get_usr_1['token'], dm_id)
    resp = requests.post(ENDPOINT_DM_LEAVE, json=data)
    assert resp.status_code == 200

    data = generate_dm_json(get_usr_2['token'], dm_id)
    resp = requests.get(ENDPOINT_DM_DETAILS, data)

    usr_details = requests.get(ENDPOINT_USER_PROF, {'token': get_usr_2['token'], 'u_id': get_usr_2['auth_user_id']}).json()['user']

    assert resp.json() == {'name': name, 'members': [usr_details]}
