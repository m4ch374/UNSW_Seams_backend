'''
####################################################
##          Tests for message/senddm/v1             ##
####################################################

# Expected behaviour:
#   - creates a new message in a given dm from a valid string specified by
#     an authorised user   
# InputError when:
#   - dm_id does not refer to a valid dm
#   - given string is empty or has over 1000 characters
# AccessError when:
#   - user token is invalid
#   - dm_id is valid but the user is not in the dm
# ==================================================
'''

# Imports
from ast import In
import requests

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration2_tests.endpoints import ENDPOINT_DM_SEND
from tests.iteration2_tests.helper import send_dm_json

def test_dm_send_invalid_user(user_1_made_dm):
    dm_id = user_1_made_dm['dm']

    response = requests.post(ENDPOINT_DM_SEND, json=send_dm_json('bad_token', dm_id, 'a'))
    assert response.status_code == AccessError.code


def test_dm_send_invalid_dm(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']

    response = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(token, dm_id + 1, 'a'))
    assert response.status_code == InputError.code

def test_dm_send_invalid_user_access(user_1_made_dm, get_usr_3):
    dm_id = user_1_made_dm['dm']
    invalid_token = get_usr_3['token']

    response = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(invalid_token, dm_id, 'a'))
    assert response.status_code == AccessError.code

def test_dm_send_missing_message(user_1_made_dm, ):
    dm_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']

    response = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(token, dm_id, ''))
    assert response.status_code == InputError.code

def test_dm_send_message_too_long(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']

    response = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(token, dm_id, 'a'*1001))
    assert response.status_code == InputError.code

