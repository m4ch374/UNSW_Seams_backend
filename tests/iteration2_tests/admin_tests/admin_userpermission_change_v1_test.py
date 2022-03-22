'''
####################################################
##    Tests for admin/userpermission/change/v1    ##
####################################################

# Expected behaviour:
# InputError when:
#   - u_id does not refer to a valid user
#   - u_id refers to a user who is the only global owner and they are being demoted to a user
#   - permission_id is invalid
#   - the user already has the permissions level of permission_id
# AccessError when:
#   - the authorised user is not a global owner
# ==================================================
'''

# imports used
import requests
from src.error import InputError, AccessError
from tests.iteration2_tests.endpoints import (
    ENDPOINT_ADMIN_PERM_CHANGE, ENDPOINT_JOIN_CHNL, ENDPOINT_CREATE_CHNL,
    ENDPOINT_JOIN_CHNL, 
)
from tests.iteration2_tests.helper import (
    create_admin_perm_change_input_json, generate_channel_input_json
)
from tests.iteration2_tests.admin_tests.definitions import (
    INVALID_TOKEN, INVALID_U_ID, INVALID_PERM_ID, OWNER_PERM_ID, USER_PERM_ID
)

# raise AccessError since invalid token passed
#
# note: while the invalid channel id passed should raise
#       InputError on their own, the AccessError takes precedent
def test_admin_perm_change_invalid_token():
    json_input = create_admin_perm_change_input_json(INVALID_TOKEN, 
                                                     INVALID_U_ID, 
                                                     INVALID_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    assert response.status_code == AccessError.code

# raise InputError since invalid u_id passed
def test_admin_perm_change_invalid_user_id(get_token_1):
    json_input = create_admin_perm_change_input_json(get_token_1, INVALID_U_ID, 
                                                     OWNER_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    assert response.status_code == InputError.code

# raise InputError since demoting only global owner to user
def test_admin_perm_change_demote_only_global_owner(get_u_id):
    user1_id = get_u_id['id']
    user1_tok = get_u_id['token']
    json_input = create_admin_perm_change_input_json(user1_tok, user1_id, 
                                                     USER_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    assert response.status_code == InputError.code

# raise InputError since permission already = permission_id
def test_admin_perm_change_perm_already_set(get_token_1, get_u_id):
    json_input = create_admin_perm_change_input_json(get_token_1, 
                                                     get_u_id['id'], 
                                                     USER_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    assert response.status_code == InputError.code

# raise AccessError since authoriedsuser is not a global owner
def test_admin_perm_change_auth_user_not_allowed_1(get_u_id, get_token_1):
    json_input = create_admin_perm_change_input_json(get_token_1, 
                                                     get_u_id['id'], 
                                                     USER_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    assert response.status_code == AccessError.code

# raise AccessError since authoried user is not a global owner
def test_admin_perm_change_auth_user_not_allowed_2(get_token_1, get_token_2,
                                                   get_u_id):
    json_input = create_admin_perm_change_input_json(get_token_2, 
                                                     get_u_id['id'], 
                                                     OWNER_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    assert response.status_code == AccessError.code

# change a global user to a global owner (and test correct reponse code)
def test_admin_perm_change_promote_to_owner_1(get_token_1, get_u_id):
    json_input = create_admin_perm_change_input_json(get_token_1, 
                                                     get_u_id['id'], 
                                                     OWNER_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    assert response.status_code == 200

# change a global user to a global owner (and test via joining private chnl)
def test_admin_perm_change_promote_to_owner_2(get_token_1, get_u_id):
    # promote user to global owner
    json_input = create_admin_perm_change_input_json(get_token_1, 
                                                     get_u_id['id'], 
                                                     OWNER_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    # join the newly promoted user to a private chnl
    data1 = generate_channel_input_json(get_token_2, "First Chnl", False)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    json_input = create_chnl_join_input_json(get_token_1, channel_id1)
    requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    # check that user is now in the private chnl
    expected_output = [{'channel_id': channel_id1, 'name': "First Chnl"}]
    dict_tok = {'token': get_token_1}
    channel_list = requests.get(ENDPOINT_LIST_CHNL, dict_tok).json()['channels']
    assert channel_list == expected_output

# promote a user to global owner, then demote again (and test chnl join)
def test_admin_perm_change_promote_then_demote(get_token_1, get_u_id):
    # promote user to global owner
    json_input = create_admin_perm_change_input_json(get_token_1, 
                                                     get_u_id['id'], 
                                                     OWNER_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    # demote them again
    json_input = create_admin_perm_change_input_json(get_token_1, 
                                                     get_u_id['id'], 
                                                     USER_PERM_ID)
    response = requests.post(ENDPOINT_ADMIN_PERM_CHANGE, json = json_input)
    # join the newly promoted user to a private chnl
    data1 = generate_channel_input_json(get_token_2, "First Chnl", False)
    response = requests.post(ENDPOINT_CREATE_CHNL, json=data1).json()
    channel_id1 = response['channel_id']
    json_input = create_chnl_join_input_json(get_token_1, channel_id1)
    join_response = requests.post(ENDPOINT_JOIN_CHNL, json = json_input)
    assert join_response.status_code == AccessError.code
