'''
####################################################
##       Tests for channel_removeowner_v1         ##
####################################################
#
# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
#   - u_id does not refer to a valid user
#   - u_id refers to a user who is not an owner of the channel
#   - u_id refers to a user who is currently the only owner of the channel
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
    ENDPOINT_JOIN_CHNL, ENDPOINT_CREATE_CHNL, ENDPOINT_CHNL_ADDOWNER,
    ENDPOINT_CHNL_REMOVEOWNER,
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
def test_channel_removeowner_v1_invalid_token():
    json_input = generate_chnl_func_json(INVALID_TOKEN, INVALID_CHNL_ID,
                                         INVALID_U_ID)
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == AccessError.code

# raise InputError since channel_id does not refer to a valid channel
#
# note: both u_id and token passed should be valid
def test_channel_removeowner_v1_invalid_channel_id(get_token_1, get_u_id):
    json_input = generate_chnl_func_json(get_token_1, INVALID_CHNL_ID,
                                         get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == InputError.code

# raise inputerror since u_id does not refer to a valid user
#
# note: both channel_id and token passed should be valid
def test_channel_removeowner_v1_invalid_u_id(get_token_1):
    # create a chnl
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    # try to add a non existent u_id as owner of chnl
    json_input = generate_chnl_func_json(get_token_1, channel_id1, INVALID_U_ID)
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == InputError.code

# raise InputError since u_id refers to a user who isn't an owner of the channel
# but IS a member of the chnl
def test_channel_removeowner_v1_member_not_owner(user_1_made_channel, get_u_id):
    # create a chnl, then join user get_u_id
    channel_id1 = user_1_made_channel['channel']
    token_1 = user_1_made_channel['token']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # remove u_id as a owner
    json_input = generate_chnl_func_json(token_1, channel_id1, get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == InputError.code

# raise AccesError since u_id refers to a user who isn't an owner of the channel
# and also IS'NT a member of the chnl
def test_channel_removeowner_v1_member_nor_owner_member_1(get_token_2,
                                                          user_1_made_channel,
                                                          get_u_id):
    # create a chnl, then join user get_u_id
    channel_id1 = user_1_made_channel['channel']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # promote get_u_id to channel owner via the chnl owner user_1_made_channel
    user_1_tok = user_1_made_channel['token']
    json_input = generate_chnl_func_json(user_1_tok, channel_id1,
                                         get_u_id['id'])
    requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    # remove u_id as a owner (but fail since get_token_2 does not have perms)
    json_input = generate_chnl_func_json(get_token_2, channel_id1, get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == AccessError.code
    assert 1 == 0

# successfully remove a chnl owner since user has global owner permissions
# and theyre inside the chnl
def test_channel_removeowner_v1_member_nor_owner_member_2(get_u_id2,
                                                          user_1_made_channel,
                                                          get_u_id):
    # create a chnl, then join user get_u_id AND get_u_id2
    channel_id1 = user_1_made_channel['channel']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    json_input = create_chnl_join_input_json(get_u_id2['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # promote get_u_id to channel owner via the chnl owner user_1_made_channel
    user_1_tok = user_1_made_channel['token']
    json_input = generate_chnl_func_json(user_1_tok, channel_id1,
                                         get_u_id['id'])
    requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    # remove u_id as a owner (but fail since get_token_2 does not have perms)
    json_input = generate_chnl_func_json(get_u_id2['token'], channel_id1,
                                         get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == 200

# raise InputError since u_id refers to a user who is currently the only owner
# of the channel
def test_channel_removeowner_v1_only_chnl_owner(get_u_id):
    # create a chnl
    data1 = generate_channel_input_json(get_u_id['token'], "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    # remove the only owner from the channel
    json_input = generate_chnl_func_json(get_u_id['token'], channel_id1,
                                         get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == InputError.code

# raise AccessError since authorised user does not have owner permissions in
# the channel
#
# note: channel_id is valid
def test_channel_removeowner_v1_no_owner_permission(user_1_made_channel,
                                                    get_u_id, get_u_id2):
    # create a chnl, then join user get_u_id and get_u_id2
    channel_id1 = user_1_made_channel['channel']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    json_input = create_chnl_join_input_json(get_u_id2['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # promote get_u_id to channel owner via the chnl owner user_1_made_channel
    user_1_tok = user_1_made_channel['token']
    json_input = generate_chnl_func_json(user_1_tok, channel_id1,
                                         get_u_id['id'])
    requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    # attempt to remove the user get_u_id as an owner via the user get_u_id2
    json_input = generate_chnl_func_json(get_u_id2['token'], channel_id1,
                                         get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == AccessError.code

# successfully add then remove a user as a channel owner
# note this is via the user_1_made_channel (who is both a global and chnl owner)
def test_channel_removeowner_v1_success_simple_1(user_1_made_channel, get_u_id):
    # create a chnl, then join user get_u_id
    channel_id1 = user_1_made_channel['channel']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # promote get_u_id to channel owner via the chnl owner user_1_made_channel
    user_1_tok = user_1_made_channel['token']
    json_input = generate_chnl_func_json(user_1_tok, channel_id1,
                                         get_u_id['id'])
    requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    # remove the user get_u_id as an owner via the original chnl owner
    json_input = generate_chnl_func_json(user_1_tok, channel_id1,
                                         get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == 200

# successfully add then remove a user as a channel owner using another channel
# owner (that isn't a global owner)
def test_channel_removeowner_v1_success_2(user_1_made_channel,
                                          get_u_id, get_u_id2):
    # create a chnl, then join user get_u_id and get_u_id2
    channel_id1 = user_1_made_channel['channel']
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    json_input = create_chnl_join_input_json(get_u_id2['token'], channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # promote both get_u_id and get_u_id2 to channel owner via the chnl owner
    user_1_tok = user_1_made_channel['token']
    json_input = generate_chnl_func_json(user_1_tok, channel_id1,
                                         get_u_id['id'])
    requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    json_input = generate_chnl_func_json(user_1_tok, channel_id1,
                                         get_u_id2['id'])
    requests.post(ENDPOINT_CHNL_ADDOWNER, json = json_input)
    # remove the user get_u_id as an owner via the user get_u_id2
    json_input = generate_chnl_func_json(get_u_id2['token'], channel_id1,
                                         get_u_id['id'])
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == 200
    # verify that get_u_id no longer is chnl owner, by having get_u_id fail
    # to remove another channel owner
    json_input = generate_chnl_func_json(get_u_id['token'], channel_id1,
                                         get_u_id2['id'])
    response = requests.post(ENDPOINT_CHNL_REMOVEOWNER, json = json_input)
    assert response.status_code == AccessError.code
