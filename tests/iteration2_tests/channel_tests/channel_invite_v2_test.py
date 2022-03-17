'''
####################################################
##          Tests for channel/invite/v2           ##
####################################################

# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
#   - u_id does not refer to a valid user
#   - u_id refers to a user who is already a member of the channel
# AccessError when:
#   - channel_id is valid and the authorised user is not a member of the
#     channel
# ==================================================
'''

# imports used
import requests
from src.error import InputError, AccessError
from tests.iteration2_tests.endpoints import (
    ENDPOINT_CHNL_INVITE, ENDPOINT_CREATE_CHNL, ENDPOINT_LIST_CHNL
)
from tests.iteration2_tests.helper import (
    create_chnl_invite_input_json, generate_channel_input_json
)
from tests.iteration2_tests.channel_tests.definitions import (
    INVALID_TOKEN, INVALID_CHNL_ID, INVALID_U_ID
)

# raise AccessError since invalid token passed
#
# note: while the invalid u_id & channel id's passed should raise
#       InputErrors on their own, the AccessError takes precedent
def test_channel_join_v2_invalid_token():
    json_input = create_chnl_invite_input_json(INVALID_TOKEN, INVALID_CHNL_ID,
                                               INVALID_U_ID)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    assert response.status_code == AccessError.code

# raise InputError since invalid_u_id passed
def test_channel_invite_v2_invalid_u_id(get_token_1):
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    json_input = create_chnl_invite_input_json(get_token_1, channel_id1,
                                               INVALID_U_ID)
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    assert response.status_code == InputError.code

# raise InputError since u_id refers to user already a member of the channel
def test_channel_invite_v2_already_a_member(get_token_1, get_u_id):
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    json_input = create_chnl_invite_input_json(get_token_1, channel_id1,
                                               get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    json_input = create_chnl_invite_input_json(get_token_1, channel_id1,
                                               get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    assert response.status_code == InputError.code

# raise AccessError since authorised user is not a member of the channel
def test_channel_invite_v2_auth_user_not_in_chnl(get_token_1, get_token_2,
                                                 get_u_id):
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    json_input = create_chnl_invite_input_json(get_token_2, channel_id1, get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    assert response.status_code == AccessError.code

# invite a user to a public channel with no errors
def test_channel_invite_v2_public_channel(get_token_1, get_u_id):
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    json_input = create_chnl_invite_input_json(get_token_1, channel_id1, get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    expected_output = [{'channel_id': channel_id1, 'name': "First Chnl"}]
    channel_list = requests.get(ENDPOINT_LIST_CHNL, {'token': get_u_id['token']}).json()['channels']
    assert channel_list == expected_output

# invite a user to a private channel with no errors
def test_channel_invite_v2_private_channel(get_token_1, get_u_id):
    data1 = generate_channel_input_json(get_token_1, "First Chnl", False)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    json_input = create_chnl_invite_input_json(get_token_1, channel_id1, get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_INVITE, json = json_input)
    expected_output = [{'channel_id': channel_id1, 'name': "First Chnl"}]
    channel_list = requests.get(ENDPOINT_LIST_CHNL, {'token': get_u_id['token']}).json()['channels']
    assert channel_list == expected_output
