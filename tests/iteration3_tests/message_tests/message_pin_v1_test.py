'''
##############################################################################
##                     Tests for message/pin/v1                              #
##############################################################################

# Expected error behaviour:
# InputError when:
#   - message_id is not a valid message within a channel or DM that the 
#     authorised user has joined
#   - the message is already pinned
# AccessError when:
#   - message_id refers to a valid message in a joined channel/DM and the 
#     authorised user does not have owner permissions in the channel/DM
# =============================================================================
'''
# imports used
import requests
from src.error import InputError, AccessError
from tests.iteration3_tests.endpoints import (
    ENDPOINT_MESSAGE_PIN, ENDPOINT_JOIN_CHNL, ENDPOINT_MESSAGE_SEND,
    ENDPOINT_CHANNEL_MESSAGE,
)
from tests.iteration3_tests.message_tests.definitions import (
    INVALID_TOKEN, INVALID_MSG_ID,
)
from tests.iteration3_tests.message_tests.helper import (
    create_msg_pin_input_json, create_msg_send_input_json,
    create_chnl_join_input_json, create_chnl_get_msgs,
)

# raise AccessError since invalid token passed
#
# while invalid msg should raise input error, accesserror takes precedent
def test_message_pin_v1_invalid_token():
    json_input = create_msg_pin_input_json(INVALID_TOKEN, INVALID_MSG_ID)
    response = requests.post(ENDPOINT_MESSAGE_PIN, json = json_input)
    assert response.status_code == AccessError.code

# raise input error since message id is not a valid message within a chnl user
# has joined (ie, chnl one)
def test_message_pin_v1_invalid_msg_id(user_1_made_channel):
    user1_tok = user_1_made_channel['token']
    json_input = create_msg_pin_input_json(user1_tok, INVALID_MSG_ID)
    response = requests.post(ENDPOINT_MESSAGE_PIN, json = json_input)
    assert response.status_code == InputError.code

# raise input error since message is already pinned
def test_message_pin_v1_already_pinned(user_1_made_channel, get_usr_2):
    # create a chnl, then join a second user and send a message
    user1_token = user_1_made_channel['token']
    chnl_id1 = user_1_made_channel['channel']
    user2_token = get_usr_2['token']
    chnl_join_json = create_chnl_join_input_json(user2_token, chnl_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = chnl_join_json)
    
    msg_send_json = create_msg_send_input_json(user2_token, chnl_id1, "hello!")
    send_response = requests.post(ENDPOINT_MESSAGE_SEND, json=
                                  msg_send_json).json()
    msg_id = send_response['message_id']

    # try to pin the same message after it's already been pinned
    pin_json_input = create_msg_pin_input_json(user1_token, msg_id)
    requests.post(ENDPOINT_MESSAGE_PIN, json = pin_json_input)
    response = requests.post(ENDPOINT_MESSAGE_PIN, json = pin_json_input)

    assert response.status_code == InputError.code

# raise  access error since message_id refers to a valid message in a joined 
# channel/DM and the auth user does not have owner permissions in the channel/DM
def test_message_pin_v1_not_an_owner(user_1_made_channel, get_usr_2):
    # create a chnl, then join a second user and send a message
    chnl_id1 = user_1_made_channel['channel']
    user2_token = get_usr_2['token']
    chnl_join_json = create_chnl_join_input_json(user2_token, chnl_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = chnl_join_json)
    
    msg_send_json = create_msg_send_input_json(user2_token, chnl_id1, "hello!")
    send_response = requests.post(ENDPOINT_MESSAGE_SEND,
                                  json=msg_send_json).json()
    msg_id = send_response['message_id']
    
    # try (& fail) to pin a message through the non owner member of the channel
    pin_json_input = create_msg_pin_input_json(user2_token, msg_id)
    response = requests.post(ENDPOINT_MESSAGE_PIN, json = pin_json_input)

    assert response.status_code == AccessError.code

# pin a message with no problems (since original owner of chnl)
def test_message_pin_v1_success_1(user_1_made_channel, get_usr_2):
    # create a chnl, then join a second user and send a message
    user1_token = user_1_made_channel['token']
    chnl_id1 = user_1_made_channel['channel']
    user2_token = get_usr_2['token']
    chnl_join_json = create_chnl_join_input_json(user2_token, chnl_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = chnl_join_json)
    
    msg_send_json = create_msg_send_input_json(user2_token, chnl_id1, "hello!")
    send_response = requests.post(ENDPOINT_MESSAGE_SEND,
                                  json=msg_send_json).json()
    msg_id = send_response['message_id']

    pin_json_input = create_msg_pin_input_json(user1_token, msg_id)
    response = requests.post(ENDPOINT_MESSAGE_PIN, json = pin_json_input)
    assert response.status_code == 200

    # verify that the message has been pinned
    get_msg_input = create_chnl_get_msgs(user1_token, chnl_id1, 0)
    msg = requests.get(ENDPOINT_CHANNEL_MESSAGE, 
                       params=get_msg_input).json()['messages'][0]

    assert msg['is_pinned'] == True

# pin a message with no problems even though user 2 is not the owner ( since 
#user2 has global permissions)
def test_message_pin_v1_success_2(get_usr_2, user_1_made_channel):
    # create a chnl, then join a second user and send a message
    user1_token = user_1_made_channel['token']
    chnl_id1 = user_1_made_channel['channel']
    user2_token = get_usr_2['token']
    chnl_join_json = create_chnl_join_input_json(user2_token, chnl_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = chnl_join_json)
    
    msg_send_json = create_msg_send_input_json(user2_token, chnl_id1, "hello!")
    send_response = requests.post(ENDPOINT_MESSAGE_SEND,
                                  json=msg_send_json).json()
    msg_id = send_response['message_id']

    pin_json_input = create_msg_pin_input_json(user2_token, msg_id)
    response = requests.post(ENDPOINT_MESSAGE_PIN, json = pin_json_input)
    assert response.status_code == 200

    # verify that the message has been pinned
    get_msg_input = create_chnl_get_msgs(user1_token, chnl_id1, 0)
    msg = requests.get(ENDPOINT_CHANNEL_MESSAGE, 
                       params=get_msg_input).json()['messages'][0]

    assert msg['is_pinned'] == True
