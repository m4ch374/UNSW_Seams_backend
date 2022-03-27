'''
####################################################
##          Tests for message/remove/v1           ##
####################################################

# Expected behaviour:
#    - Removes a given message from the frontend when called by an authorised user
# InputError when:
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
from tests.iteration2_tests.endpoints import ENDPOINT_MESSAGE_REMOVE, ENDPOINT_MESSAGE_SEND, ENDPOINT_JOIN_CHNL
from tests.iteration2_tests.helper import *


# Case where message id does not exist
def test_message_remove_message_id_nonexist(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']
    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(token, msg['message_id'] + 1))

    assert response.status_code == InputError.code

    response = requests.get(generate_get_channel_message_url(token, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 1


# Case where message exists in a different channel than what the user has access to (inputerror)
def test_message_remove_invalid_message_id(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    token_2 = get_usr_2['token']
    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_1, channel_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(token_2, msg['message_id']))

    assert response.status_code == InputError.code

    response = requests.get(generate_get_channel_message_url(token_1, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 1

# Case where user is not the sender of the message and does not have owner permissions in the channel
def test_message_remove_invalid_message_access(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    token_2 = get_usr_2['token']
    requests.post(ENDPOINT_JOIN_CHNL, json={'token':token_2, 'channel_id':channel_id})

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_1, channel_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(token_2, msg['message_id']))

    assert response.status_code == AccessError.code

    response = requests.get(generate_get_channel_message_url(token_1, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 1

# Case where user sent the message (should work)
def test_message_remove_by_sender(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    token_2 = get_usr_2['token']
    requests.post(ENDPOINT_JOIN_CHNL, json={'token':token_2, 'channel_id':channel_id})

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_2, channel_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(token_2, msg['message_id']))

    assert response.status_code == OK

    response = requests.get(generate_get_channel_message_url(token_1, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 0

# Case where user did not send the message but is local owner
def test_message_remove_by_local_owner(user_1_made_channel, get_usr_2):
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    token_2 = get_usr_2['token']
    requests.post(ENDPOINT_JOIN_CHNL, json={'token':token_2, 'channel_id':channel_id})

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_2, channel_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(token_1, msg['message_id']))

    assert response.status_code == OK

    response = requests.get(generate_get_channel_message_url(token_1, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 0

# Case where user did not send the message but is global owner
def test_message_remove_by_global_owner(get_usr_2, user_1_made_channel):
    token_2 = get_usr_2['token']
    channel_id = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    
    requests.post(ENDPOINT_JOIN_CHNL, json={'token':token_2, 'channel_id':channel_id})

    msg = requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token_1, channel_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(token_2, msg['message_id']))

    assert response.status_code == OK

    response = requests.get(generate_get_channel_message_url(token_1, channel_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 0


################ Same as above tests but for dm channels #################

def test_dm_message_remove_message_id_nonexist(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    token = user_1_made_dm['creator_token']
    msg = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(token, dm_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(token, msg['message_id'] + 1))

    assert response.status_code == InputError.code

    response = requests.get(generate_get_dm_message_url(token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 1

def test_dm_message_remove_invalid_message_id(user_1_made_dm, get_usr_3):
    dm_id = user_1_made_dm['dm']
    creator_token = user_1_made_dm['creator_token']
    external_token = get_usr_3['token']
    msg = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(creator_token, dm_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(external_token, msg['message_id']))

    assert response.status_code == InputError.code

    response = requests.get(generate_get_dm_message_url(creator_token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 1

def test_dm_message_remove_invalid_message_access(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    creator_token = user_1_made_dm['creator_token']
    member_token = user_1_made_dm['member_token']
    msg = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(creator_token, dm_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(member_token, msg['message_id']))

    assert response.status_code == AccessError.code

    response = requests.get(generate_get_dm_message_url(creator_token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 1

def test_dm_message_remove_by_sender(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    creator_token = user_1_made_dm['creator_token']
    member_token = user_1_made_dm['member_token']
    msg = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(member_token, dm_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(member_token, msg['message_id']))

    assert response.status_code == OK

    response = requests.get(generate_get_dm_message_url(creator_token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 0

def test_dm_message_remove_by_local_owner(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    creator_token = user_1_made_dm['creator_token']
    member_token = user_1_made_dm['member_token']
    msg = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(member_token, dm_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(creator_token, msg['message_id']))

    assert response.status_code == OK

    response = requests.get(generate_get_dm_message_url(creator_token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 0

# Tests the removal of a message by a global owner who is a member but not the local owner
# Unlike in channel removes this should not work in dms as global owners are not automatically local owners
def test_dm_message_remove_by_global_owner(user_1_made_dm_with_global_owner):
    dm_id = user_1_made_dm_with_global_owner['dm']
    creator_token = user_1_made_dm_with_global_owner['creator_token']
    member_token = user_1_made_dm_with_global_owner['member_token']
    msg = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(creator_token, dm_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(member_token, msg['message_id']))

    assert response.status_code == AccessError.code

    response = requests.get(generate_get_dm_message_url(creator_token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 1

def test_message_remove_twice(user_1_made_dm):
    dm_id = user_1_made_dm['dm']
    member_token = user_1_made_dm['member_token']
    msg = requests.post(ENDPOINT_DM_SEND, json=send_dm_json(member_token, dm_id, 'a')).json()
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(member_token, msg['message_id']))
    response = requests.delete(ENDPOINT_MESSAGE_REMOVE, json=remove_msg_json(member_token, msg['message_id']))

    assert response.status_code == InputError.code

    response = requests.get(generate_get_dm_message_url(member_token, dm_id, 0))
    assert response.status_code == OK
    assert len(response.json()['messages']) == 0
