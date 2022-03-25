'''
####################################################
##          Tests for message/edit/v1             ##
####################################################

# Expected behaviour:
#    - Edits a given message to given string when called by an authorised user
# InputError when:
#   - given string is more than 1000 characters in length
#   - msg_id does not refer to a valid message
#   - msg_id refers to a message which is in a channel/dm the user is not in
# AccessError when:
#   - user token is invalid
#   - when msg_id and user_id refers to a message and user in the same channel/dm
#     but the user does not have access permissions to the message (the message
#     was not sent by the user and they do not have owner permissions in the channel/dn)
# ==================================================
'''

# Imports
from http.client import OK
import requests

# Import errors
from src.error import InputError, AccessError

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

# Case where user sent the message (should work)
def test_message_edit_by_non_owner_sender(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    token_2 = get_usr_2['token']
    requests.post(ENDPOINT_JOIN_CHNL, json={'token':token_2, 'channel_id':channel_id})

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_2, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_2, msg['message_id'], 'b'))

    assert response.status_code == OK
    
    response = requests.get(generate_get_channel_message_url(token_1, channel_id, 0))
    assert response.status_code == OK
    assert response.json()['messages'][0]['message'] == 'b'


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
# (user 2 is created first --> global owner)
def test_message_edit_by_global_owner(get_usr_2, user_1_made_channel):
    token_2 = get_usr_2['token']
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    requests.post(ENDPOINT_JOIN_CHNL, json={'token':token_2, 'channel_id':channel_id})

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_1, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_2, msg['message_id'], 'b'))

    assert response.status_code == OK
    
    response = requests.get(generate_get_channel_message_url(token_1, channel_id, 0))
    assert response.status_code == OK
    assert response.json()['messages'][0]['message'] == 'b'


def test_message_edit_delete_case():
    pass



###### DO all of the above tests again but for dms #######

def test_dm_message_edit_message_too_long(user_1_made_dm):
    channel_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']
    
    requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, channel_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token, channel_id, 'a'*1001))

    assert response.status_code == InputError.code

def test_dm_message_edit_message_id_nonexist(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']
    msg = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token, dm_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token, msg['message_id'] + 1, 'b'))

    assert response.status_code == InputError.code

# Dm already has users 1 and 2 in it, user 3 is external
def test_dm_message_edit_invalid_message_id(user_1_made_dm, get_usr_3):
    dm_id = user_1_made_dm['dm']
    token_1 = user_1_made_dm['creator_token']
    token_2 = get_usr_3['token']

    msg = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token_1, dm_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_2, msg['message_id'], 'b'))

    assert response.status_code == InputError.code


def test_dm_message_edit_invalid_message_access(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    token_1 = user_1_made_dm['creator_token']
    token_2 = user_1_made_dm['member_token']

    msg = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token_1, dm_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_2, msg['message_id'], 'b'))

    assert response.status_code == AccessError.code
    
def test_dm_message_edit_by_non_owner_sender(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    token_1 = user_1_made_dm['member_token']

    msg = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token_1, dm_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_1, msg['message_id'], 'b'))

    assert response.status_code == OK
   
    response = requests.get(generate_get_dm_message_url(token_1, dm_id, 0))
    assert response.status_code == OK
    assert response.json()['messages'][0]['message'] == 'b'


def test_dm_message_edit_by_local_owner(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    token_1 = user_1_made_dm['creator_token']
    token_2 = user_1_made_dm['member_token']

    msg = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token_2, dm_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_1, msg['message_id'], 'b'))

    assert response.status_code == OK
    
    response = requests.get(generate_get_dm_message_url(token_1, dm_id, 0))
    assert response.status_code == OK
    assert response.json()['messages'][0]['message'] == 'b'

# User 2 is the first registered member and has global owner permissions but should not have 
# owner permissions in the private dm.
def test_dm_message_edit_by_global_owner(get_usr_3, user_1_made_dm_with_global_owner):
    dm_id = user_1_made_dm_with_global_owner['dm']
    token_1 = user_1_made_dm_with_global_owner['creator_token']
    token_2 = user_1_made_dm_with_global_owner['member_token']

    msg = requests.post(ENDPOINT_DM_SEND, json=send_msg_json(token_1, dm_id, 'a')).json()
    response = requests.put(ENDPOINT_MESSAGE_EDIT, json=edit_msg_json(token_2, msg['message_id'], 'b'))

    assert response.status_code == AccessError.code

def test_dm_message_edit_delete_case():
    pass