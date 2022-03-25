'''
####################################################
##          Tests for message/send/v1             ##
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
from tests.iteration2_tests.endpoints import ENDPOINT_MESSAGE_SEND
from tests.iteration2_tests.helper import send_msg_json


def test_message_send_invalid_user(user_1_made_channel):
    channel_id = user_1_made_channel['channel']

    response = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json('bad_token', channel_id, 'a'))
    assert response.status_code == AccessError.code


def test_message_send_invalid_channel(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    response = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id + 1, 'a'))
    assert response.status_code == InputError.code

def test_message_send_invalid_user_access(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    invalid_token = get_usr_2['token']

    response = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(invalid_token, channel_id, 'a'))
    assert response.status_code == AccessError.code

def test_message_send_missing_message(user_1_made_channel, ):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    response = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, ''))
    assert response.status_code == InputError.code

def test_message_send_message_too_long(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    response = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, 'a'*1001))
    assert response.status_code == InputError.code

