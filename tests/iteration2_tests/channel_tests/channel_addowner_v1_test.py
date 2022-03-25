'''
####################################################
##        Tests for channel_addowner_v1           ##
####################################################
#
# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
    - u_id does not refer to a valid user
    - u_id refers to a user who is not a member of the channel
    - u_id refers to a user who is already an owner of the channel
# AccessError when:
#   - channel_id is valid and the authorised user does not have owner 
#     permissions in the channelchannel_id is valid and the authorised user does
#     not have owner permissions in the channel
#
# ==================================================
'''
# imports used
import requests
from src.error import InputError, AccessError
from tests.iteration2_tests.endpoints import (
    ENDPOINT_JOIN_CHNL, ENDPOINT_CREATE_CHNL, ENDPOINT_LIST_CHNL, 
    ENDPOINT_CHNL_LEAVE, ENDPOINT_CHNL_ADDOWNER,
)
from tests.iteration2_tests.helper import (
    create_chnl_join_input_json, generate_channel_input_json, 
    generate_chnl_func_json,
)
from tests.iteration2_tests.channel_tests.definitions import (
    INVALID_TOKEN, INVALID_CHNL_ID, INVALID_U_ID
)

# raise AccessError since invalid token passed
#
# note: while the invalid channel id passed should raise
#       InputError on their own, the AccessError takes precedent
def test_channel_addowner_v1_invalid_token():
    json_input = generate_chnl_func_json(INVALID_TOKEN, INVALID_CHNL_ID,
                                         INVALID_U_ID)
    response = requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    assert response.status_code == AccessError.code

# raise inputerror since channel_id does not refer to a valid channel
#
# note: both u_id and token passed should be valid
def test_channel_addowner_v1_invalid_channel_id(get_token_1, get_u_id):
    json_input = generate_chnl_func_json(get_token_1, INVALID_CHNL_ID,
                                         get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    assert response.status_code == InputError.code

# raise inputerror since u_id does not refer to a valid user
#
# note: both channel_id and token passed should be valid
def test_channel_addowner_v1_invalid_u_id(get_token_1):
    # create a chnl
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    # try to add a non existent u_id as owner of chnl
    json_input = generate_chnl_func_json(get_token_1, channel_id1, INVALID_U_ID)
    response = requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    assert response.status_code == InputError.code

# raise inputerror since u_id refers to a user who isn't a member of the
# channel
def test_channel_addowner_v1_non_member(user_1_made_channel, get_u_id):
    # create a chnl
    channel_id1 = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    # try to add a non member u_id as owner of chnl
    json_input = generate_chnl_func_json(token_1, channel_id1, get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    assert response.status_code == InputError.code

# raise inputerror since u_id is already an owner of the channel
def test_channel_addowner_v1_already_owner(user_1_made_channel, get_u_id):
    # create a chnl, then join user get_u_id
    channel_id1 = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # add u_id as a owner, then add them again (to get inputerror)
    json_input = generate_chnl_func_json(token_1, channel_id1, get_u_id['id'])
    requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    response = requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    assert response.status_code == InputError.code
    
# raise AccessError since authorised user doesn't have owner permissions in
# the channel
def test_channel_addowner_v1_no_owner_permission(user_1_made_channel,
                                                 get_token_2, get_u_id):
    # create a chnl, then join user get_u_id and get_token_2
    channel_id1 = user_1_made_channel['channel']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    json_input = create_chnl_join_input_json(get_token_2, channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # try to add the user get_u_id as an owner via get_token_2 (who is not
    # an owner in this channel either)
    json_input = generate_chnl_func_json(get_token_2, channel_id1, 
                                         get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    assert response.status_code == AccessError.code

# make a member of a chnl an owner with no errors
def test_channel_addowner_v1_successful_1(user_1_made_channel, get_u_id):
    # create a chnl, then join user get_u_id
    channel_id1 = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # add u_id as a owner
    json_input = generate_chnl_func_json(token_1, channel_id1, get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    assert response.status_code == 200

# make a member of a chnl an owner, and test that this new owner has owner
# status by making another chnl member an owner
def test_channel_addowner_v1_successful_2(user_1_made_channel, get_u_id,
                                          get_u_id2):
    # create a chnl, then join user get_u_id and get_u_id2
    channel_id1 = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    json_input = create_chnl_join_input_json(get_u_id2['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # add u_id as a owner
    json_input = generate_chnl_func_json(token_1, channel_id1, get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    # add u_id2 as an owner through the owner u_id
    json_input = generate_chnl_func_json(get_u_id['token'], channel_id1,
                                         get_u_id2['id'])
    response = requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    assert response.status_code == 200





