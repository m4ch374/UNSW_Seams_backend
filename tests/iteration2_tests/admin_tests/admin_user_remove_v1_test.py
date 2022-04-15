'''
####################################################
##          Tests for admin/user/remove/v1        ##
####################################################

# Expected behaviour:
# InputError when:
#   - u_id does not refer to a valid user
#   - u_id refers to a user who is the only global owner
# AccessError when:
#   - channel_id is valid and the authorised user is not a member of the
#     channel
# ==================================================
'''
# imports used
import requests
from src.error import InputError, AccessError
from tests.iteration2_tests.endpoints import (
    ENDPOINT_ADMIN_REMOVE, ENDPOINT_JOIN_CHNL, ENDPOINT_LIST_CHNL,
    ENDPOINT_CREATE_CHNL, ENDPOINT_DM_CREATE, ENDPOINT_USER_PROF,
    ENDPOINT_DM_DETAILS, ENDPOINT_USERS_ALL, ENDPOINT_MESSAGE_SEND,
    ENDPOINT_LOGOUT, ENDPOINT_REGISTER_USR, ENDPOINT_CHNL_INVITE
)
from tests.iteration2_tests.admin_tests.definitions import (
    INVALID_TOKEN, INVALID_U_ID,
)
from tests.iteration2_tests.helper import (
    create_admin_remove_user_input_json, create_chnl_join_input_json,
    generate_channel_input_json, generate_dm_input_json, generate_dm_json,
    generate_get_channel_message_url, send_msg_json,
)

# raise AccessError since invalid token passed
#
# note: while the invalid channel u_id passed should raise
#       InputError on their own, the AccessError takes precedent
def test_admin_remove_user_v1_invalid_token():
    json_input = create_admin_remove_user_input_json(INVALID_TOKEN,
                                                     INVALID_U_ID)
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == AccessError.code

# raise InputError since invalid u_id passed
def test_admin_remove_user_v1_invalid_u_id(get_token_1):
    json_input = create_admin_remove_user_input_json(get_token_1, INVALID_U_ID)
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == InputError.code

# raise Inputerror since u_id refers to a user who is the only global owner
def test_admin_remove_user_v1_only_global_user(get_u_id):
    json_input = create_admin_remove_user_input_json(get_u_id['token'],
                                                     get_u_id['id'])
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == InputError.code

# raise AccessError since the authorised user is not a global owner
def test_admin_remove_user_v1_not_authorised(get_u_id, get_token_1):
    json_input = create_admin_remove_user_input_json(get_token_1,
                                                     get_u_id['id'])
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == AccessError.code

# remove a user with no errors raised (test via status_code)
def test_admin_remove_user_v1_simple_code_test(get_token_1, get_u_id):
    json_input = create_admin_remove_user_input_json(get_token_1,
                                                     get_u_id['id'])
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == 200

# # remove a user, and assert that they are removed from all channels
# def test_admin_remove_user_v1_from_channels(get_token_1, get_u_id, get_u_id2):
#     # get_token_1 user create channel
#     data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
#     response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
#     channel_id = response['channel_id']
#     # join get_u_id user to the first channel created by fixture
#     json_input = create_chnl_join_input_json(get_u_id['token'], channel_id)
#     requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
#     # create a new chnl with get_u_id as owner
#     data2 = generate_channel_input_json(get_u_id['token'], "second Chnl", True)
#     requests.post(ENDPOINT_CREATE_CHNL, json=data2)
#     # create a new chnl with get_u_id2 as owner (for coverage sake)
#     data3 = generate_channel_input_json(get_u_id2['token'], "third Chnl", True)
#     requests.post(ENDPOINT_CREATE_CHNL, json=data3)
#     # remove the user that was just inserted
#     json_input = create_admin_remove_user_input_json(get_token_1,
#                                                      get_u_id['id'])
#     response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
#     # assert that the user is no longer in any channle
#     channel_list = requests.get(ENDPOINT_LIST_CHNL, {'token': get_u_id['token']}).json()['channels']
#     assert channel_list == []

# test that a removed user is removed from all dms
def test_admin_remove_user_v1_not_in_dms(get_usr_1, get_usr_2, get_u_id):
    # create a dm with two users
    data = generate_dm_input_json(get_usr_1['token'], [get_usr_2['auth_user_id']])
    dm_id = requests.post(ENDPOINT_DM_CREATE, json=data).json()['dm_id']
    # create another dm without get_usr_2 for coverages sake
    data2 = generate_dm_input_json(get_usr_1['token'], [get_u_id['id']])
    requests.post(ENDPOINT_DM_CREATE, json=data2)
    # create the expected data for once user is removed
    data = generate_dm_json(get_usr_1['token'], dm_id)
    prof1_dict = {'token': get_usr_1['token'],
                  'u_id': get_usr_1['auth_user_id']}
    prof2_dict = {'token': get_usr_2['token'],
                  'u_id': get_usr_2['auth_user_id']}
    usr1 = requests.get(ENDPOINT_USER_PROF, prof1_dict).json()['user']
    usr2 = requests.get(ENDPOINT_USER_PROF, prof2_dict).json()['user']

    expected_name = ', '.join(sorted([usr1['handle_str'], usr2['handle_str']]))
    expected_output = {
        'name': expected_name,
        'members': [usr1],
    }
    # remove the user get_usr_2 from existence
    json_input = create_admin_remove_user_input_json(get_usr_1['token'],
                                                     get_usr_2['auth_user_id'])
    requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    # fetch the dm details
    resp = requests.get(ENDPOINT_DM_DETAILS, data).json()
    assert resp == expected_output


# test that removed user will not be included in the list of users returned by
# users/all
def test_admin_remove_user_v1_via_user_all(get_usr_1, get_usr_2):
    json_input = create_admin_remove_user_input_json(get_usr_1['token'],
                                                     get_usr_2['auth_user_id'])
    requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    response = requests.get(ENDPOINT_USERS_ALL, {'token': get_usr_1['token']})
    response_data = response.json()
    # expected_output = {'users': [{'u_id': get_usr_1['auth_user_id'],
    #                               'email': 'randomemail@gmail.com',
    #                               'name_first': 'joe',
    #                               'name_last': 'bidome',
    #                               'handle_str': 'joebidome'}]}
    assert len(response_data['users']) == 1

# test that the profile of a removed user must still be retrievable with
# user/profile, however name_first should be 'Removed' and 'name_last' should
# be 'user'.
# def test_admin_remove_user_v1_new_profile(get_usr_1, get_usr_2):
#     # remove user via admin remove function
#     json_input = create_admin_remove_user_input_json(get_usr_1['token'],
#                                                      get_usr_2['auth_user_id'])
#     requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
#     # verify that user profile exists and is updated
#     user_2_id = get_usr_2['auth_user_id']
#     user_2_tok = get_usr_2['token']
#     response = requests.get(ENDPOINT_USER_PROF, {'token': user_2_tok,
#                                                  'u_id': user_2_id})
#     assert response.status_code == 200
#     response_data = response.json()
#     assert (response_data['user'])['name_first'] == 'Removed'
#     assert (response_data['user'])['name_last'] == 'user'

# test that once users are removed, the contents of the messages they sent
# will be replaced by 'Removed user'.
def test_admin_remove_user_v1_modified_messages(get_u_id, get_usr_1):
    data1 = generate_channel_input_json(get_usr_1['token'], "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id = response['channel_id']
    token = get_usr_1['token']
    for _ in range(2):
        requests.post(ENDPOINT_MESSAGE_SEND, json=send_msg_json(token, channel_id, 'a'))
    # join get_u_id user to the first channel created by fixture
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # remove the original message creator
    json_input = create_admin_remove_user_input_json(get_u_id['token'],
                                                     get_usr_1['auth_user_id'])
    requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    # verify messages of removed user have been modified
    response = requests.get(generate_get_channel_message_url(get_u_id['token'], channel_id, 0))
    dict_of_messages = (response.json())['messages']
    for i in range(2):
        assert dict_of_messages[i]['message'] == 'Removed user'

def test_removed_user_cant_logout(get_usr_1, get_usr_2):
    json_input = create_admin_remove_user_input_json(get_usr_1['token'],
                                                     get_usr_2['auth_user_id'])
    requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    response = requests.post(ENDPOINT_LOGOUT, json = {'token': get_usr_2['token']})
    assert response.status_code == 403

def test_valid_input():
    a = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z1@ed.unsw.edu.au', 'password': '1234567', 'name_first': '11', 'name_last': '11'}).json()
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z2@ed.unsw.edu.au', 'password': '1234567', 'name_first': '22', 'name_last': '22'}).json()
    c = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z3@ed.unsw.edu.au', 'password': '1234567', 'name_first': '33', 'name_last': '33'}).json()
    d = requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z4@ed.unsw.edu.au', 'password': '1234567', 'name_first': '44', 'name_last': '44'}).json()

    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':c['token'],'name':"123", 'is_public':False})
    requests.post(ENDPOINT_CHNL_INVITE, json = {'token':c['token'],'channel_id':1, 'u_id':4})
    requests.post(ENDPOINT_CREATE_CHNL, json = {'token':d['token'],'name':"123", 'is_public':False})
    requests.post(ENDPOINT_CHNL_INVITE, json = {'token':d['token'],'channel_id':1, 'u_id':1})
    requests.post(ENDPOINT_CHNL_INVITE, json = {'token':d['token'],'channel_id':1, 'u_id':2})
    requests.post(ENDPOINT_CHNL_INVITE, json = {'token':d['token'],'channel_id':1, 'u_id':3})

    json_input = create_admin_remove_user_input_json(a['token'], 2)
    requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    json_input = create_admin_remove_user_input_json(a['token'], 4)
    requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
