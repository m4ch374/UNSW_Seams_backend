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
    ENDPOINT_MESSAGE_SEND, ENDPOINT_MESSAGE_REACT, ENDPOINT_MESSAGE_EDIT,
    ENDPOINT_DM_SEND, ENDPOINT_CHNL_LEAVE, ENDPOINT_CREATE_CHNL,
    ENDPOINT_REGISTER_USR
)
from tests.iteration3_tests.notif_tests.helper import (
    create_chnl_invite_input_json, generate_dm_json, send_repeated_messages,
    send_dm_json, create_chnl_join_input_json, edit_msg_json,
)
from tests.iteration3_tests.notif_tests.definitions import (
    REACT_ID, INVALID_TOK, ALPHABET_LIST,
)
# Generates url for get method
def generate_notif_url(token):
    return f'{ENDPOINT_NOTIF_GET}?token={token}'

# test that an access error is raised when a invalid token is passed
def test_notif_invalid_token():
    response = requests.get(generate_notif_url(INVALID_TOK))
    assert response.status_code == AccessError.code

# test that a user that should have no notifications, has no notifications
def test_no_notifications(user_1_made_channel, get_usr_2):
    token1 = user_1_made_channel['token']
    channel_id1 = user_1_made_channel['channel']
    user2_id = get_usr_2['auth_user_id']
    # token2 = get_usr_2['token']
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
    assert notif_list[0] == expected_output

# return a single notification for a user who has been added to a DM
def test_single_notif_in_dm(user_1_made_dm_with_global_owner):
    dm_id1 = user_1_made_dm_with_global_owner['dm']
    member_tok = user_1_made_dm_with_global_owner['member_token']

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
    requests.post(ENDPOINT_MESSAGE_REACT, json=data)

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
def test_notif_for_dm_react(user_1_made_dm_with_global_owner):
    dm_id1 = user_1_made_dm_with_global_owner['dm']
    creator_tok = user_1_made_dm_with_global_owner['creator_token']
    member_tok = user_1_made_dm_with_global_owner['member_token']

    # send a dm message via member, and have owner react to message
    data = send_dm_json(member_tok, dm_id1, 'hi')
    msg_id = requests.post(ENDPOINT_DM_SEND, json=data).json()['message_id']

    data = {
        'token': creator_tok,
        'message_id': msg_id,
        'react_id': REACT_ID,
    }
    resp = requests.post(ENDPOINT_MESSAGE_REACT, json=data)

    # get the name of the dm
    data = generate_dm_json(member_tok, dm_id1)
    resp = requests.get(ENDPOINT_DM_DETAILS, data).json()
    dm_name = resp['name']

    # assert that the most recent notification is due to the react
    response = requests.get(generate_notif_url(member_tok))
    expected_output = {
        'channel_id': -1,
        'dm_id': dm_id1,
        'notification_message': ("joebidome reacted to your message in "
                                 f"{dm_name}")
    }
    notif_list = (response.json())['notifications']
    assert notif_list[0] == expected_output


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
        'token': user1_token,
        'channel_id': chnl_id,
        'message': "@obamaprism hello hello :D",
    }
    requests.post(ENDPOINT_MESSAGE_SEND, json=data)

    # assert that the most recent notification is because of the react
    response = requests.get(generate_notif_url(user2_token))
    assert response.status_code == 200

    # note: only first 20 char of message is to be returned in the notification
    expected_output = {
        'channel_id': chnl_id,
        'dm_id': -1,
        'notification_message': ("joebidome tagged you in chnl_name: "
                                 "@obamaprism hello he")
    }
    notif_list = (response.json())['notifications']
    assert notif_list[0] == expected_output

# return a single notification for a user who has been tagged in a dm
def test_notif_for_dm_tagged(user_1_made_dm_with_global_owner):
    dm_id1 = user_1_made_dm_with_global_owner['dm']
    creator_tok = user_1_made_dm_with_global_owner['creator_token']
    member_tok = user_1_made_dm_with_global_owner['member_token']

    data = send_dm_json(creator_tok, dm_id1, '@obamaprism hi how are you')
    requests.post(ENDPOINT_DM_SEND, json=data)

    # get the name of the dm and set up expected output
    data = generate_dm_json(member_tok, dm_id1)
    resp = requests.get(ENDPOINT_DM_DETAILS, data).json()
    dm_name = resp['name']

    expected_output = {
        'channel_id': -1,
        'dm_id': dm_id1,
        'notification_message': (f"joebidome tagged you in {dm_name}: "
                                 "@obamaprism hi how a")
    }

    # get the actual notification
    response = requests.get(generate_notif_url(member_tok))
    notif_list = (response.json())['notifications']
    assert notif_list[0] == expected_output

# return the most recent twenty notifications a user has received (although
# they actually have more than 20 notifs)
# return a single notification for a user who has been tagged in a chnl
def test_notif_for_many_tagged_in_chnl(user_1_made_channel, get_usr_2):
    # create a chnl with two members
    user1_token = user_1_made_channel['token']
    chnl_id = user_1_made_channel['channel']
    user2_id = get_usr_2['auth_user_id']
    user2_token = get_usr_2['token']
    json_input = create_chnl_invite_input_json(user1_token, chnl_id, user2_id)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)

    # send a tonne of messages to dm tagging obamaprism
    send_repeated_messages(ALPHABET_LIST, 'obamaprism', user1_token, chnl_id)

    response = requests.get(generate_notif_url(user2_token))
    notif_list = (response.json())['notifications']
    assert len(notif_list) == 20
    # check that the first notif is the notif from the most recent messge sent
    expected_output1 = {
        'channel_id': chnl_id,
        'dm_id': -1,
        'notification_message': ("joebidome tagged you in chnl_name: "
                                 "@obamaprism z")
    }
    assert notif_list[0] == expected_output1
    # check that the last notif is the correct notif
    expected_output2 = {
        'channel_id': chnl_id,
        'dm_id': -1,
        'notification_message': ("joebidome tagged you in chnl_name: "
                                 "@obamaprism g")
    }
    assert notif_list[19] == expected_output2

# return no notifications for a user who has been tagged in a chnl (since the
# tagged person has laready been removed from the channel)
def test_notif_tagged_left_member_in_chnl(user_1_made_channel, get_usr_2):
    # create a chnl with two members
    user1_token = user_1_made_channel['token']
    chnl_id = user_1_made_channel['channel']
    user2_id = get_usr_2['auth_user_id']
    user2_token = get_usr_2['token']
    json_input = create_chnl_invite_input_json(user1_token, chnl_id, user2_id)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)

    # remove the user from the channel
    json_input = create_chnl_join_input_json(user2_token, chnl_id)
    response = requests.post(ENDPOINT_CHNL_LEAVE, json = json_input)

    # send a message via user 1 tagging user2
    data = {
        'token': user1_token,
        'channel_id': chnl_id,
        'message': "@obamaprism hello hello :D",
    }
    requests.post(ENDPOINT_MESSAGE_SEND, json=data)

    # assert that there is not notification from the tagging
    response = requests.get(generate_notif_url(user2_token))
    expected_output = {
        'channel_id': chnl_id,
        'dm_id': -1,
        'notification_message': ("joebidome tagged you in chnl_name: "
                                 "@obamaprism hello he")
    }
    notif_list = (response.json())['notifications']
    assert notif_list[0] != expected_output

# return a notification when a message that previously didn't have a tag is
# edited to have a tag
def test_notif_tag_when_message_edited(user_1_made_channel, get_usr_2):
    # create a chnl with two members
    user1_token = user_1_made_channel['token']
    chnl_id = user_1_made_channel['channel']
    user2_id = get_usr_2['auth_user_id']
    user2_token = get_usr_2['token']
    json_input = create_chnl_invite_input_json(user1_token, chnl_id, user2_id)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)

    # send a message via user 1 that DOES NOT tag user2
    data = {
        'token': user1_token,
        'channel_id': chnl_id,
        'message': "there is no tag in this message :D",
    }
    msg_id = requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']

    # edit the message so that now it does tag the user
    new_msg = "@obamaprism this is now an edited message"
    response = requests.put(ENDPOINT_MESSAGE_EDIT,
                            json=edit_msg_json(user1_token, msg_id, new_msg))

    response = requests.get(generate_notif_url(user2_token))
    expected_output = {
        'channel_id': chnl_id,
        'dm_id': -1,
        'notification_message': ("joebidome tagged you in chnl_name: "
                                 "@obamaprism this is ")
    }
    notif_list = (response.json())['notifications']
    assert notif_list[0] == expected_output

def test_leave_before_react():
    a = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'}).json()
    b = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'}).json()

    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':a['token'],'name':"123", 'is_public':False})
    requests.post(ENDPOINT_CHNL_INVITE, json = {'token':a['token'],'channel_id':1, 'u_id':2})

    requests.post(ENDPOINT_MESSAGE_SEND, json = {'token':b['token'],'channel_id':1, 'message':'qqq'})
    requests.post(ENDPOINT_CHNL_LEAVE, json = {'token':b['token'],'channel_id':1})
    data = {
        'token': a['token'],
        'message_id': 1,
        'react_id': REACT_ID,
    }
    requests.post(ENDPOINT_MESSAGE_REACT, json=data)
