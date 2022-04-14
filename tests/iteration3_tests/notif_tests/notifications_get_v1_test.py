'''
##############################################################################
##                  Tests for notifications/get/v1                           #
##############################################################################

# Expected error behaviour:
  NA - no errors are expected, apart from the usual access error raised from
       an invalid token

# =============================================================================
'''
# imports used
import requests
from src.error import AccessError

from tests.iteration3_tests.endpoints import (
    ENDPOINT_NOTIF_GET, ENDPOINT_CHNL_INVITE, ENDPOINT_DM_DETAILS,
    ENDPOINT_MESSAGE_SEND, ENDPOINT_MESSAGE_REACT, ENDPOINT_CHANNEL_MESSAGE,
    ENDPOINT_DM_SEND, ENDPOINT_DM_CREATE
)
from tests.iteration3_tests.notif_tests.helper import (
    generate_get_notif_url, create_chnl_invite_input_json, generate_dm_json,
    send_dm_json, generate_dm_input_json,
)

#local defintions
REACT_ID = 1

# Generates url for get method
def generate_notif_url(token):
    return f'{ENDPOINT_NOTIF_GET}?token={token}'
'''
# call the function just to test it exists and is callable
def test_basic_notif(user_1_made_channel, get_usr_2):
    token1 = user_1_made_channel['token']
    channel_id1 = user_1_made_channel['channel']
    user2_id = get_usr_2['auth_user_id']
    token2 = get_usr_2['token']
    json_input = create_chnl_invite_input_json(token1, channel_id1, user2_id)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    assert response.status_code == 200
    
    print("printing notifs for user2")
    response = requests.get(generate_notif_url(token2))
    print(response)
    print(response.json())
    
    
    assert 1 == 2
'''
# test that a user that should have no notifications, has no notifications
def test_no_notifications(user_1_made_channel, get_usr_2):
    token1 = user_1_made_channel['token']
    channel_id1 = user_1_made_channel['channel']
    user2_id = get_usr_2['auth_user_id']
    token2 = get_usr_2['token']
    json_input = create_chnl_invite_input_json(token1, channel_id1, user2_id)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)

    response = requests.get(generate_notif_url(token1))
    notif_list = (response.json())['notifications']
    assert notif_list == []

# return a single notification for a user who has been added to a channel
def test_single_notif_in_channel(user_1_made_channel, get_usr_2):
    token1 = user_1_made_channel['token']
    channel_id1 = user_1_made_channel['channel']
    user2_id = get_usr_2['auth_user_id']
    token2 = get_usr_2['token']
    json_input = create_chnl_invite_input_json(token1, channel_id1, user2_id)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)

    response = requests.get(generate_notif_url(token2))
    assert response.status_code == 200
    
    expected_output = {'channel_id': channel_id1, 
                       'dm_id': -1,
                       'notification_message': "joebidome added you to chnl_name"}
    notif_list = (response.json())['notifications']
    print(notif_list[0])
    print(expected_output)
    assert notif_list[0] == expected_output
    
# return a single notification for a user who has been added to a DM
def test_single_notif_in_dm(user_1_made_dm_with_global_owner):
    dm_id1 = user_1_made_dm_with_global_owner['dm']
    creator_tok = user_1_made_dm_with_global_owner['creator_token']
    member_tok = user_1_made_dm_with_global_owner['member_token']
    creator_id = user_1_made_dm_with_global_owner['creator_id']
    member_id = user_1_made_dm_with_global_owner['member_id']

    # get notifications for dm member
    response = requests.get(generate_notif_url(member_tok))
    assert response.status_code == 200

    # set up the expected output
    data = generate_dm_json(member_tok, dm_id1)
    resp = requests.get(ENDPOINT_DM_DETAILS, data).json()
    dm_name = resp['name']
    expected_output = {
        'channel_id': -1, 
        'dm_id': dm_id1,
        'notification_message': f"joebidome added you to {dm_name}"
    }
    notif_list = (response.json())['notifications']
    assert notif_list[0] == expected_output

# test the second notification for a user whose message was reacted to in chnl
def test_notif_for_chnl_msg_react(user_1_made_channel, get_usr_2):
    # create a chnl with two members
    user1_token = user_1_made_channel['token']
    chnl_id = user_1_made_channel['channel']
    user2_id = get_usr_2['auth_user_id']
    user2_token = get_usr_2['token']
    json_input = create_chnl_invite_input_json(user1_token, chnl_id, user2_id)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    # send a message via user 2, and user 1 reacts to it
    data = {
        'token': user2_token,
        'channel_id': chnl_id,
        'message': "lmao",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']

    data = {
        'token': user1_token,
        'message_id': msg_id,
        'react_id': REACT_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_REACT, json=data)
    
    # assert that the most recent notification is due to the react
    response = requests.get(generate_notif_url(user2_token))
    assert response.status_code == 200
    
    expected_output = {
        'channel_id': chnl_id, 
        'dm_id': -1,
        'notification_message': ("joebidome reacted to your message in "
                                 "chnl_name")
    }
    notif_list = (response.json())['notifications']
    assert notif_list[0] == expected_output

# test that a user receives notif if they're message is reacted to in DM
# def test_single_notif_in_dm(user_1_made_dm_with_global_owner):
def test_notif_for_dm_react(user_1_made_dm_with_global_owner):
    print("++++++++++++++++++++++++++++++++++++++++")
    '''
    dm_id1 = user_1_made_dm_with_global_owner['dm']
    creator_tok = user_1_made_dm_with_global_owner['creator_token']
    member_tok = user_1_made_dm_with_global_owner['member_token']
    creator_id = user_1_made_dm_with_global_owner['creator_id']
    member_id = user_1_made_dm_with_global_owner['member_id']
    
    # send a dm message via member, and have owner react to message
    data = send_dm_json(member_tok, dm_id1, 'hi')
    msg_id = requests.post(ENDPOINT_DM_SEND, json=data).json()['message_id']

    data = {
        'token': creator_token,
        'message_id': msg_id,
        'react_id': REACT_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_REACT, json=data)

    # get the name of the dm
    data = generate_dm_json(member_tok, dm_id1)
    resp = requests.get(ENDPOINT_DM_DETAILS, data).json()
    dm_name = resp['name']

    # assert that the most recent notification is due to the react
    response = requests.get(generate_notif_url(member_token))
    expected_output = {
        'channel_id': -1, 
        'dm_id': dm_id1,
        'notification_message': ("joebidome reacted to your message in "
                                 f"{dm_name}")
    }
    notif_list = (response.json())['notifications']
    assert notif_list[0] == expected_output
    '''
    


# return a single notification for a user who has been tagged in a chnl
def test_notif_for_tagged_in_chnl(user_1_made_channel, get_usr_2):
    # create a chnl with two members
    user1_token = user_1_made_channel['token']
    chnl_id = user_1_made_channel['channel']
    user2_id = get_usr_2['auth_user_id']
    user2_token = get_usr_2['token']
    json_input = create_chnl_invite_input_json(user1_token, chnl_id, user2_id)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    # send a message via user 1 tagging user2
    data = {
        'token': user2_token,
        'channel_id': chnl_id,
        'message': "@ObamaPrism hello hello :D",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']
    
    # assert that the most recent notification is because of the react
    response = requests.get(generate_notif_url(user2_token))
    assert response.status_code == 200
    
    # note: only first 20 char of message is to be returned in the notification
    expected_output = {
        'channel_id': chnl_id, 
        'dm_id': -1,
        'notification_message': ("joebidome tagged you in chnl_name: "
                                 "@ObamaPrism hello he")
    }
    notif_list = (response.json())['notifications']
    print(notif_list)
    print(notif_list[0])
    print(expected_output)
    assert notif_list[0] == expected_output

