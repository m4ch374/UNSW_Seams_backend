'''
####################################################
##          Tests for channel_leave_v1            ##
####################################################
#
# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
# AccessError when:
#   - channel_id is valid and the authorised user is not a member of the channel
#
# ==================================================
'''
# imports used
import requests
from src.error import InputError, AccessError
from tests.iteration2_tests.endpoints import (
    ENDPOINT_JOIN_CHNL, ENDPOINT_CREATE_CHNL, ENDPOINT_LIST_CHNL, 
    ENDPOINT_CHNL_LEAVE,
)
from tests.iteration2_tests.helper import (
    create_chnl_join_input_json, generate_channel_input_json, 
    generate_chnl_func_json,
)
from tests.iteration2_tests.channel_tests.definitions import (
    INVALID_TOKEN, INVALID_CHNL_ID,
)

# raise AccessError since invalid token passed
#
# note: while the invalid channel id passed should raise
#       InputError on their own, the AccessError takes precedent
def test_channel_leave_v1_invalid_token():
    json_input = create_chnl_join_input_json(INVALID_TOKEN, INVALID_CHNL_ID)
    response = requests.post(ENDPOINT_CHNL_LEAVE, json = json_input)
    assert response.status_code == AccessError.code

# raise inputerror since channel_id does not refer to a valid channel
def test_channel_leave_v1_invalid_channel_id(get_token_1):
    json_input = create_chnl_join_input_json(get_token_1, INVALID_CHNL_ID)
    response = requests.post(ENDPOINT_CHNL_LEAVE, json = json_input)
    assert response.status_code == InputError.code

# raise AccessError since channel_id is valid & auth user is not a chnl member 
def test_channel_leave_v1_user_not_chnl_member(get_token_1, get_token_2):
    # create a chnl
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    # leave token_2 user from this chnl token_2 is not a part of
    json_input = create_chnl_join_input_json(get_token_2, channel_id1)
    response = requests.post(ENDPOINT_CHNL_LEAVE, json = json_input)
    assert response.status_code == AccessError.code

# channel user leave a channel with no errors
def test_channel_leave_v1_user_successful(get_token_1, get_token_2):
    # create a chnl with token 1 and join token 2 to it
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    json_input = create_chnl_join_input_json(get_token_2, channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # leave token 2 from this channel
    json_input = create_chnl_join_input_json(get_token_2, channel_id1)
    response = requests.post(ENDPOINT_CHNL_LEAVE, json = json_input)
    # verify that token 2 has successfully left the channel
    channel_list = requests.get(ENDPOINT_LIST_CHNL,
                               {'token': get_token_2}).json()['channels']
    assert channel_list == []

# channel owner leave a channel with no errors
def test_channel_leave_v1_owner_successful(get_token_1, get_token_2):
    # create a chnl with token 1 and join token 2 to it
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    json_input = create_chnl_join_input_json(get_token_2, channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # leave token 1 from this channel
    json_input = create_chnl_join_input_json(get_token_1, channel_id1)
    response = requests.post(ENDPOINT_CHNL_LEAVE, json = json_input)
    # verify that token 1 has successfully left the channel
    channel_list = requests.get(ENDPOINT_LIST_CHNL,
                               {'token': get_token_1}).json()['channels']
    assert channel_list == []
    # verify that token 2 is still part of the now onwerless chnl
    tok2_response = requests.get(ENDPOINT_LIST_CHNL,
                                 {'token': get_token_2}).json()['channels']
    expected_output = [{'channel_id': channel_id1, 'name': "First Chnl"}]
    assert expected_output == tok2_response
