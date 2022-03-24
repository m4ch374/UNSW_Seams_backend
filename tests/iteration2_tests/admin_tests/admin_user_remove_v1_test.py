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
    ENDPOINT_CREATE_CHNL,
)
from tests.iteration2_tests.admin_tests.definitions import (
    INVALID_TOKEN, INVALID_U_ID,
)
from tests.iteration2_tests.helper import (
    create_admin_remove_user_input_json, create_chnl_join_input_json,
    generate_channel_input_json,
)

# raise AccessError since invalid token passed
#
# note: while the invalid channel u_id passed should raise
#       InputError on their own, the AccessError takes precedent
def test_admin_remove_user_invalid_token():
    json_input = create_admin_remove_user_input_json(INVALID_TOKEN,
                                                     INVALID_U_ID)
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == AccessError.code

# raise InputError since invalid u_id passed
def test_admin_remove_user_invalid_u_id(get_token_1):
    json_input = create_admin_remove_user_input_json(get_token_1, INVALID_U_ID)
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == InputError.code

# raise Inputerror since u_id refers to a user who is the only global owner
def test_admin_remove_user_only_global_user(get_u_id):
    json_input = create_admin_remove_user_input_json(get_u_id['token'],
                                                     get_u_id['id'])
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == InputError.code

# raise AccessError since the authorised user is not a global owner
def test_admin_remove_user_not_authorised(get_u_id, get_token_1):
    json_input = create_admin_remove_user_input_json(get_token_1,
                                                     get_u_id['id'])
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == AccessError

# remove a user with no errors raised (test via status_code)
def test_admin_remove_user_simple_code_test(get_token_1, get_u_id):
    json_input = create_admin_remove_user_input_json(get_token_1,
                                                     get_u_id['id'])
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    assert response.status_code == 200

# remove a user, and assert that they are removed from all channels
def test_admin_remove_user_from_channels(get_token_1, get_u_id):
    # get_token_1 user create channel
    data1 = generate_channel_input_json(get_token_1, "First Chnl", True)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id = response['channel_id']
    # join get_u_id user to the first channel created by fixture
    json_input = create_chnl_join_input_json(get_u_id['token'], channel_id)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # remove the user that was just inserted
    json_input = create_admin_remove_user_input_json(get_token_1,
                                                     get_u_id['id'])
    response = requests.delete(ENDPOINT_ADMIN_REMOVE, json = json_input)
    # assert that the user is no longer in any channle
    channel_list = requests.get(ENDPOINT_LIST_CHNL, {'token': get_u_id['token']}).json()['channels']
    assert channel_list == []

