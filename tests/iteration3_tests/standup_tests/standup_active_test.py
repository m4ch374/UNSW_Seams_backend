# Imports
from multiprocessing.connection import wait
import requests
from http.client import OK

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration3_tests.endpoints import ENDPOINT_STANDUP_START, ENDPOINT_STANDUP_ACTIVE

# Makes json for posts
def json_helper(token, channel_id, length):
    return{'token':token,
            'channel_id':channel_id,
            'length':length}

# Generates url for get method
def generate_standup_url(token, channel_id):
    return f'{ENDPOINT_STANDUP_ACTIVE}?token={token}&channel_id={str(channel_id)}'

# simple, working cases
def test_standup_active_simple_true(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper(token, channel_id, 10))
    response = requests.get(generate_standup_url(token, channel_id))
    assert response.status_code == OK
    assert response.json()['is_active'] == True

def test_standup_active_simple_false(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    response = requests.get(generate_standup_url(token, channel_id))
    assert response.status_code == OK
    assert response.json()['is_active'] == False

# Error cases
def test_standup_active_invalid_channel(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    response = requests.get(generate_standup_url(token, channel_id + 1))

    assert response.status_code == InputError.code

def test_standup_active_invalid_access(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_2 = get_usr_2['token']

    response = requests.get(generate_standup_url(token_2, channel_id))

    assert response.status_code == AccessError.code