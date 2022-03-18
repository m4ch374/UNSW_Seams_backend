"""
Tests for the behaviours of
/dm/create/v1
"""

# Imports
import requests
from src.error import InputError, AccessError

# Importing definitions
from tests.iteration2_tests.endpoints import *

# Import helpers
from tests.iteration2_tests.helper import generate_dm_input_json

INVALID_TOKEN = 'invalid'
INVALID_ID = -1

def test_invalid_token(get_usr_1):
    data = generate_dm_input_json(INVALID_TOKEN, [get_usr_1['auth_user_id']])
    resp = requests.post(ENDPOINT_DM_CREATE, json=data)
    assert resp.status_code == AccessError.code

def test_invalid_id(get_usr_1):
    data = generate_dm_input_json(get_usr_1['token'], [INVALID_ID])
    resp = requests.post(ENDPOINT_DM_CREATE, json=data)
    assert resp.status_code == InputError.code

def test_duped_id(get_usr_1, get_usr_2):
    data = generate_dm_input_json(get_usr_1['token'], [get_usr_2['auth_user_id'], get_usr_2['auth_user_id']])
    resp = requests.post(ENDPOINT_DM_CREATE, json=data)
    assert resp.status_code == InputError.code

def test_empty_uids(get_usr_1):
    data = generate_dm_input_json(get_usr_1['token'], [])
    resp = requests.post(ENDPOINT_DM_CREATE, json=data)
    assert resp.status_code == 200

def test_valid(get_usr_1, get_usr_2):
    data = generate_dm_input_json(get_usr_1['token'], [get_usr_2['auth_user_id']])
    resp = requests.post(ENDPOINT_DM_CREATE, json=data)
    assert resp.status_code == 200
