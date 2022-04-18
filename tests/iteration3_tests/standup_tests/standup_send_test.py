# Imports
import requests
from http.client import OK
import time

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration3_tests.endpoints import ENDPOINT_STANDUP_START, ENDPOINT_STANDUP_SEND, ENDPOINT_CHANNEL_MESSAGE

# Makes json for posts
def json_helper_start(token, channel_id, length):
    return{'token':token,
            'channel_id':channel_id,
            'length':length}

def json_helper_send(token, channel_id, msg):
    return{'token':token,
            'channel_id':channel_id,
            'message':msg}

def generate_get_channel_message_url(token, channel, start):
    return f'{ENDPOINT_CHANNEL_MESSAGE}?token={token}&channel_id={str(channel)}&start={start}'

# Simple working cases, otherwise tested through frontend
def test_standup_send_simple(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper_start(token, channel_id, 0.5))
    response = requests.post(ENDPOINT_STANDUP_SEND, json=json_helper_send(token, channel_id, 'a'))
    assert response.status_code == OK
    time.sleep(0.5)
    response = requests.get(generate_get_channel_message_url(token, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 1

def test_standup_send_simple_second(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper_start(token, channel_id, 0.5))
    requests.post(ENDPOINT_STANDUP_SEND, json=json_helper_send(token, channel_id, 'a'))
    response = requests.post(ENDPOINT_STANDUP_SEND, json=json_helper_send(token, channel_id, 'b'))
    assert response.status_code == OK
    time.sleep(0.5)
    response = requests.get(generate_get_channel_message_url(token, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 1
    
def test_standup_send_simple_elapses(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper_start(token, channel_id, 0.5))
    time.sleep(0.5)
    response = requests.get(generate_get_channel_message_url(token, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 0

# Error cases
def test_standup_send_invalid_channel(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper_start(token, channel_id, 1))
    response = requests.post(ENDPOINT_STANDUP_SEND, json=json_helper_send(token, channel_id + 1, 'a'))
    assert response.status_code == InputError.code

def test_standup_send_invalid_accessl(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']
    token_2 = get_usr_2['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper_start(token, channel_id, 1))
    response = requests.post(ENDPOINT_STANDUP_SEND, json=json_helper_send(token_2, channel_id, 'a'))
    assert response.status_code == AccessError.code

def test_standup_send_no_active_standup(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    response = requests.post(ENDPOINT_STANDUP_SEND, json=json_helper_send(token, channel_id, 'a'))
    assert response.status_code == InputError.code

def test_standup_send_message_too_long(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper_start(token, channel_id, 1)) 
    response = requests.post(ENDPOINT_STANDUP_SEND, json=json_helper_send(token, channel_id, 'a'*1001))
    assert response.status_code == InputError.code

def test_standup_send_no_message(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper_start(token, channel_id, 1)) 
    response = requests.post(ENDPOINT_STANDUP_SEND, json=json_helper_send(token, channel_id, ''))
    assert response.status_code == InputError.code