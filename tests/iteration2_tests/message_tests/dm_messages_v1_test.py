'''
####################################################
##          Tests for dm/messages/v2         ##
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
import requests

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration2_tests.endpoints import ENDPOINT_DM_MESSAGE, ENDPOINT_DM_SEND

# Import helper
from tests.iteration2_tests.helper import send_msg_json

OK = 200

def generate_url(token, dm, start):
    url = f'{ENDPOINT_DM_MESSAGE}?token={token}&dm_id={str(dm)}&start={start}'
    return url

# Test invalid dm
def test_dm_messages_invalid_dm_id(user_1_made_dm):
    token = user_1_made_dm['creator_token']
    dm = user_1_made_dm['dm']

    response = requests.get(generate_url(token, dm + 1, 0))
    response_code = response.status_code
    assert response_code == InputError.code

# Test invalid user
def test_dm_messages_invalid_user_id(user_1_made_dm):
    dm = user_1_made_dm['dm']

    response = requests.get(generate_url("bad_token", dm, 0))
    response_code = response.status_code
    assert response_code == AccessError.code


# Test invalid start id
def test_dm_messages_invalid_start_id(user_1_made_dm):
    token = user_1_made_dm['creator_token']
    dm = user_1_made_dm['dm']

    response = requests.get(generate_url(token, dm, 2))
    response_code = response.status_code
    assert response_code == InputError.code

def test_dm_messages_start_id_negative(user_1_made_dm):
    token = user_1_made_dm['creator_token']
    dm = user_1_made_dm['dm']

    response = requests.get(generate_url(token, dm, -2))
    response_code = response.status_code
    assert response_code == InputError.code


# Test that AccessError is raised when both user and dm id are invalid
def test_dm_messages_invalid_user_and_dm(user_1_made_dm):
    dm = user_1_made_dm['dm']

    response = requests.get(generate_url("bad_token", dm + 1, 0))
    response_code = response.status_code
    assert response_code == AccessError.code

# Test that AccessError is raised when both user, dm and start id are invalid
def test_dm_messages_invalid_all(user_1_made_dm):
    dm = user_1_made_dm['dm']

    response = requests.get(generate_url("bad_token", dm + 1, 1))
    response_code = response.status_code
    assert response_code == AccessError.code


# Test for non-member user trying to access dm messages
def test_dm_messages_invalid_user_access(user_1_made_dm, get_usr_3):
    invalid_token = get_usr_3['token']
    dm = user_1_made_dm['dm']

    response = requests.get(generate_url(invalid_token, dm, 0))
    response_code = response.status_code
    assert response_code == AccessError.code

#############################################################
# tests below can't test exact response as msg timestamp is constantly changing

def test_dm_messages_simple(user_1_made_dm):
    token = user_1_made_dm['creator_token']
    dm_id = user_1_made_dm['dm']
    for _ in range(2):
        requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, dm_id, 'a'))

    response = requests.get(generate_url(token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 2
    assert response.json()['end'] == -1
    assert response.json()['start'] == 0
    
def test_dm_messages_edge_50(user_1_made_dm):
    token = user_1_made_dm['creator_token']
    dm_id = user_1_made_dm['dm']
    for _ in range(50):
        requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, dm_id, 'a'))

    response = requests.get(generate_url(token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 50
    assert response.json()['end'] == -1
    assert response.json()['start'] == 0

def test_dm_messages_edge_51(user_1_made_dm):
    token = user_1_made_dm['creator_token']
    dm_id = user_1_made_dm['dm']
    for _ in range(51):
        requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, dm_id, 'a'))

    response = requests.get(generate_url(token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 50
    assert response.json()['end'] == 50
    assert response.json()['start'] == 0
    
def test_dm_messages_many(user_1_made_dm):
    token = user_1_made_dm['creator_token']
    dm_id = user_1_made_dm['dm']
    for _ in range(75):
        requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, dm_id, 'a'))

    response = requests.get(generate_url(token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 50
    assert response.json()['end'] == 50
    assert response.json()['start'] == 0

    response = requests.get(generate_url(token, dm_id, 50))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 25
    assert response.json()['end'] == -1
    assert response.json()['start'] == 50
