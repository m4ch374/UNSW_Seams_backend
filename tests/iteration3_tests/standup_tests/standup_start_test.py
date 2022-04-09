# Imports
import requests
from http.client import OK

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration3_tests.endpoints import ENDPOINT_STANDUP_START

# Makes json for posts
def json_helper(token, channel_id, length):
    return{'token':token,
            'channel_id':channel_id,
            'length':length}

# simple, working case
def test_standup_start_simple(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    response = requests.post(ENDPOINT_STANDUP_START, json=json_helper(token, channel_id, 10))

    assert response.status_code == OK


# Error cases
def test_standup_start_invalid_length(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    response = requests.post(ENDPOINT_STANDUP_START, json=json_helper(token, channel_id, -1))

    assert response.status_code == InputError.code

def test_standup_start_invalid_channel(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    response = requests.post(ENDPOINT_STANDUP_START, json=json_helper(token, channel_id + 1, 10))

    assert response.status_code == InputError.code

def test_standup_start_invalid_user_access_channel(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_2 = get_usr_2['token']

    response = requests.post(ENDPOINT_STANDUP_START, json=json_helper(token_2, channel_id, 10))

    assert response.status_code == AccessError.code

def test_standup_start_already_active(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper(token, channel_id, 10))
    response = requests.post(ENDPOINT_STANDUP_START, json=json_helper(token, channel_id, 10))

    assert response.status_code == InputError.code
