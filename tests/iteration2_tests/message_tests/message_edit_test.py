'''
####################################################
##          Tests for message/edit/v1           ##
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
from http.client import OK
import requests

# Import errors
from src.error import InputError, AccessError
from src.data_store import data_store

# Import definitions
from tests.iteration2_tests.endpoints import ENDPOINT_MESSAGE_EDIT, ENDPOINT_MESSAGE_SEND, ENDPOINT_JOIN_CHNL
from tests.iteration2_tests.helper import *


def test_channel_message_edit_message_too_long(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']
    
    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token, msg['message_id'], 'a'*1001))

    assert response.status_code == InputError.code

def test_message_edit_message_id_nonexist(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']
    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token, msg['message_id'] + 1, 'b'))

    assert response.status_code == InputError.code

# Case where message exists in a different channel than what the user has access to (inputerror)
def test_message_edit_invalid_message_id(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    token_2 = get_usr_2['token']

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_1, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_2, msg['message_id'], 'b'))

    assert response.status_code == InputError.code
    
# Case where user did not send the message and is not a global/local owner
def test_message_edit_invalid_message_access(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    token_2 = get_usr_2['token']
    requests.post(ENDPOINT_JOIN_CHNL, json={'token':token_2, 'channel_id':channel_id})

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_1, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_2, msg['message_id'], 'b'))

    assert response.status_code == AccessError.code

# Case where user did not send the message but is a local owner
def test_message_edit_by_local_owner(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    token_2 = get_usr_2['token']
    requests.post(ENDPOINT_JOIN_CHNL, json={'token':token_2, 'channel_id':channel_id})

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_2, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_1, msg['message_id'], 'b'))

    assert response.status_code == OK
    
    response = requests.get(generate_get_channel_message_url(token_1, channel_id, 0))
    assert response.status_code == 200
    assert response.json()['messages'][0]['message'] == 'b'

# Case where user did not send the message or create channel but is a global owner 
# (user 2 is created first)
def test_message_edit_invalid_message_access(get_usr_2, user_1_made_channel):
    token_2 = get_usr_2['token']
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    requests.post(ENDPOINT_JOIN_CHNL, json={'token':token_2, 'channel_id':channel_id})

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_1, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_2, msg['message_id'], 'b'))

    assert response.status_code == OK
    
    response = requests.get(generate_get_channel_message_url(token_1, channel_id, 0))
    assert response.status_code == 200
    assert response.json()['messages'][0]['message'] == 'b'


def test_dm_message_edit_message_too_long(user_1_made_dm):
    channel_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']
    
    requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token, channel_id, 'a'*1001))

    assert response.status_code == InputError.code




    
''''


def test_message_edit_invalid_message_access():
    #case where user didn't send the message and user is not a channel owner

def test_message_edit_simple_user_is_owner():

def test_message_edit_simple_user_is_sender():

def test_mesage_edit_delete():


        response = requests.get(generate_get_dm_message_url(token, channel_id, 0))
    assert response.status_code == 200
    assert response.json()['messages'][0]['message'] == 'a'
    '''