'''
####################################################
##          Tests for message/senddm/v1           ##
####################################################

# Expected behaviour:
# InputError when:
#   - dm_id does not refer to a valid dm
# AccessError when:
#   - dm_id is valid and the authorised user is not a member of the
#     dm
#   - user token is invalid
# ==================================================
'''
# Imports
from ast import In
import requests

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration2_tests.endpoints import ENDPOINT_DM_SEND
from tests.iteration2_tests.helper import send_msg_json

def test_dm_send_invalid_user(user_1_made_dm):
    dm_id = user_1_made_dm['dm']

    response = requests.post(ENDPOINT_DM_SEND, json=send_msg_json('bad_token', dm_id, 'a'))
    assert response.status_code == AccessError.code


def test_dm_send_invalid_dm(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']

    response = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, dm_id + 1, 'a'))
    assert response.status_code == InputError.code

def test_dm_send_invalid_user_access(user_1_made_dm, get_usr_3):
    dm_id = user_1_made_dm['dm']
    invalid_token = get_usr_3['token']

    response = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(invalid_token, dm_id, 'a'))
    assert response.status_code == AccessError.code

def test_dm_send_missing_message(user_1_made_dm, ):
    dm_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']

    response = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, dm_id, ''))
    assert response.status_code == InputError.code

def test_dm_send_message_too_long(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']

    response = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, dm_id, 'a'*1001))
    assert response.status_code == InputError.code

