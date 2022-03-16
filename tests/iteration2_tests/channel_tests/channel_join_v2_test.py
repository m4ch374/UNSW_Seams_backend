'''
####################################################
##          Tests for channel/join/v2             ##
####################################################
#
# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
#   - the authorised user is already a member of the channel
# AccessError when:
#   - channel_id refers to a channel that is private and the authorised
#     user is not already a channel member and is not a global owner
#
# ==================================================

'''
# imports used
import requests
from src.error import InputError, AccessError
from tests.iteration2_tests.endpoints import (
    ENDPOINT_JOIN_CHNL, ENDPOINT_CREATE_CHNL, ENDPOINT_LIST_CHNL
)
from tests.iteration2_tests.helper import (
    create_chnl_join_input_json, generate_channel_input_json
)
from tests.iteration2_tests.channel_tests.definitions import (
    INVALID_TOKEN, INVALID_CHNL_ID, INVALID_U_ID
)

# raise AccessError since invalid auth_user_id passed
#
# note: while the invalid channel id passed should raise
#       InputError on their own, the AccessError takes precedent
def test_channel_join_v2_invalid_user_id():
    json_input = create_chnl_join_input_json(INVALID_TOKEN, INVALID_CHNL_ID)
    response = requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    assert response.status_code == AccessError.code

# raise InputError since channel_id does not refer to a valid channel
#
# note: this is because no valid channels have been creat
def test_channel_join_v2_invalid_channel_id(get_token_1):
    json_input = create_chnl_join_input_json(get_token_1, INVALID_CHNL_ID)
    response = requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    assert response.status_code == InputError.code

# add an authorised user to a created channel with no errors
def test_channel_join_v2_valid_1(get_token_1, get_token_2):
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    create_chnl_join_input_json(get_token_2, channel_id1)
    expected_output = [{'channel_id': channel_id1, 'name': "First Chnl"}]

    channel_list = requests.get(ENDPOINT_LIST_CHNL, {'token': get_token_2}).json()['channels']
    assert channel_list == expected_output

# raise InputError since the auth user being joined is already the only
# member of the channel
def test_channel_join_v2_user_already_member(get_token_1):
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    create_chnl_join_input_json(get_token_1, channel_id1)
    channel_list = requests.get(ENDPOINT_LIST_CHNL, {'token': get_token_1})
    assert channel_list.status_code == InputError.code

# raise AccessError since channel_id refers to private channel, auth 
# user is not part of channel and member is not global owner
def test_channel_invalid_join_private(get_token_1, get_token_2):
    data1 = generate_channel_input_json(get_token_1, "First Chnl", False)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    create_chnl_join_input_json(get_token_2, channel_id1)
    channel_list = requests.get(ENDPOINT_LIST_CHNL, {'token': get_token_2})
    assert channel_list.status_code == AccessError.code

# add an global user to a private channel with no errors
def test_channel_join_v2_global_user_to_private(get_token_1, get_token_2):
    data1 = generate_channel_input_json(get_token_2, "First Chnl", False)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    create_chnl_join_input_json(get_token_1, channel_id1)
    expected_output = [{'channel_id': channel_id1, 'name': "First Chnl"}]

    channel_list = requests.get(ENDPOINT_LIST_CHNL, {'token': get_token_1}).json()['channels']
    assert channel_list == expected_output
