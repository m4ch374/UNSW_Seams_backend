'''
####################################################
##          Tests for channel/messages/v2         ##
####################################################

# Expected behaviour:
#   - retrieves the next 50 sequential messages in a channel when given a valid channel
#   - id by an authorised user
# InputError when:
#   - channel_id does not refer to a valid channel
#   - start is greater than the total number of messages in the channel
# AccessError when:
#   - channel_id is valid and the authorised user is not a member of the
#     channel
#   - user token is invalid
# ==================================================
'''

# Imports
import requests
from http.client import OK

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration2_tests.endpoints import ENDPOINT_CHANNEL_MESSAGE, ENDPOINT_MESSAGE_SEND

# Import helper
from tests.iteration2_tests.helper import send_msg_json, generate_get_channel_message_url


# Test invalid channel
def test_channel_messages_invalid_channel_id(user_1_made_channel):
    token = user_1_made_channel['token']
    channel = user_1_made_channel['channel']

    response = requests.get(generate_get_channel_message_url(token, channel + 1, 0))
    response_code = response.status_code
    assert response_code == InputError.code

# Test invalid user
def test_channel_messages_invalid_user_id(user_1_made_channel):
    channel = user_1_made_channel['channel']

    response = requests.get(generate_get_channel_message_url("bad_token", channel, 0))
    response_code = response.status_code
    assert response_code == AccessError.code


# Test invalid start id
def test_channel_messages_invalid_start_id(user_1_made_channel):
    token = user_1_made_channel['token']
    channel = user_1_made_channel['channel']

    response = requests.get(generate_get_channel_message_url(token, channel, 2))
    response_code = response.status_code
    assert response_code == InputError.code

def test_channel_messages_start_id_negative(user_1_made_channel):
    token = user_1_made_channel['token']
    channel = user_1_made_channel['channel']

    response = requests.get(generate_get_channel_message_url(token, channel, -2))
    response_code = response.status_code
    assert response_code == InputError.code


# Test that AccessError is raised when both user and channel id are invalid
def test_channel_messages_invalid_user_and_channel(user_1_made_channel):
    channel = user_1_made_channel['channel']

    response = requests.get(generate_get_channel_message_url("bad_token", channel + 1, 0))
    response_code = response.status_code
    assert response_code == AccessError.code

# Test that AccessError is raised when both user, channel and start id are invalid
def test_channel_messages_invalid_all(user_1_made_channel):
    channel = user_1_made_channel['channel']

    response = requests.get(generate_get_channel_message_url("bad_token", channel + 1, 1))
    response_code = response.status_code
    assert response_code == AccessError.code


# Test for non-member user trying to access channel messages
def test_channel_messages_invalid_user_access(user_1_made_channel, get_usr_2):
    invalid_token = get_usr_2['token']
    channel = user_1_made_channel['channel']

    response = requests.get(generate_get_channel_message_url(invalid_token, channel, 0))
    response_code = response.status_code
    assert response_code == AccessError.code


# tests below can't test exact response as msg timestamp is constantly changing

def test_channel_messages_simple(user_1_made_channel):
    token = user_1_made_channel['token']
    channel_id = user_1_made_channel['channel']
    for _ in range(2):
        requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, 'a'))

    response = requests.get(generate_get_channel_message_url(token, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 2
    assert response.json()['end'] == -1
    assert response.json()['start'] == 0
    
def test_channel_messages_edge_50(user_1_made_channel):
    token = user_1_made_channel['token']
    channel_id = user_1_made_channel['channel']
    for _ in range(50):
        requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, 'a'))

    response = requests.get(generate_get_channel_message_url(token, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 50
    assert response.json()['end'] == -1
    assert response.json()['start'] == 0

def test_channel_messages_edge_51(user_1_made_channel):
    token = user_1_made_channel['token']
    channel_id = user_1_made_channel['channel']
    for _ in range(51):
        requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, 'a'))

    response = requests.get(generate_get_channel_message_url(token, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 50
    assert response.json()['end'] == 50
    assert response.json()['start'] == 0
    
def test_channel_messages_many(user_1_made_channel):
    token = user_1_made_channel['token']
    channel_id = user_1_made_channel['channel']
    for _ in range(75):
        requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, 'a'))

    response = requests.get(generate_get_channel_message_url(token, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 50
    assert response.json()['end'] == 50
    assert response.json()['start'] == 0

    response = requests.get(generate_get_channel_message_url(token, channel_id, 50))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 25
    assert response.json()['end'] == -1
    assert response.json()['start'] == 50

