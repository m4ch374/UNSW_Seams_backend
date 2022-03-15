"""
# ============ Channels list all v2 =================
# This section tests for the endpoint
# channels/listall/v2
# ==================================================
"""

# Imports
import requests

# Import errors
from src.error import AccessError

# Import definitions
from tests.iteration2_tests.channels_tests.definitions import NAMES_LIST, INVALID_TOKEN
from tests.iteration2_tests.endpoints import ENDPOINT_CREATE_CHNL, ENDPOINT_LISTALL

# Import helpers
from tests.iteration2_tests.helper import generate_channel_input_json

# Helper function
# helper function for testing listall with one user creating
# n channels
#
# NOTE: if is_alt is True, is_public will have no effect
# since the channels created will alternate between public and private 
def listall_helper_create_single(tok_1, n, is_public, is_alt):
    local_name_list = NAMES_LIST[:n]

    expected_output = []
    for i, name in enumerate(local_name_list):
        if is_alt:
            data = generate_channel_input_json(tok_1, name, bool(i % 2))
            resp = requests.post(ENDPOINT_CREATE_CHNL, json=data)
        else:
            data = generate_channel_input_json(tok_1, name, is_public)
            resp = requests.post(ENDPOINT_CREATE_CHNL, json=data)
        
        expected_output.append({'channel_id': resp.json()['channel_id'], 'name': name})
    
    chnl_list = requests.get(ENDPOINT_LISTALL, {'token': tok_1}).json()['channels']
    assert chnl_list == expected_output

# helper function for testing listall with multiple user creating
# n public and private channels
def listall_helper_create_multiple(tok_1, tok_2, n, is_public, is_alt):
    local_name_list = NAMES_LIST[:n]

    expected_output = []
    for i, name in enumerate(local_name_list):
        if i % 2:
            data = generate_channel_input_json(tok_1, name, is_public)
            resp = requests.post(ENDPOINT_CREATE_CHNL, json=data)
        else:
            pub = is_public if not is_alt else not is_public
            data = generate_channel_input_json(tok_2, name, pub)
            resp = requests.post(ENDPOINT_CREATE_CHNL, json=data)
        
        expected_output.append({'channel_id': resp.json()['channel_id'], 'name': name})

    chnl_list_1 = requests.get(ENDPOINT_LISTALL, {'token': tok_1}).json()['channels']
    chnl_list_2 = requests.get(ENDPOINT_LISTALL, {'token': tok_2}).json()['channels']
    
    assert chnl_list_1 == expected_output
    assert chnl_list_2 == expected_output

# should not raise any error
#
# Test the behaviour of one user creating one public channel
def test_channels_list_all_single_user_single_channel_public(get_token_1):
    listall_helper_create_single(get_token_1, 1, True, False)

# should not raise any error
#
# Test the behaviour of one user creating one private channel
def test_channels_list_all_single_user_single_channel_private(get_token_1):
    listall_helper_create_single(get_token_1, 1, False, False)

# should not raise any error
#
# Test the behaviour of one user creating one private channel
# and one public channel
def test_channels_list_all_single_user_pub_and_priv_each(get_token_1):
    listall_helper_create_single(get_token_1, 2, False, True)

# should not raise any error
#
# Test the behaviour of one user creating multiple public channels
def test_channels_list_all_single_user_multi_channels_public(get_token_1):
    listall_helper_create_single(get_token_1, len(NAMES_LIST), True, False)

# should not raise any error
#
# Test the behaviour of one user creating multiple private channels
def test_channels_list_all_single_user_multi_channels_private(get_token_1):
    listall_helper_create_single(get_token_1, len(NAMES_LIST), False, False)

# should not rause any error
#
# Test the behaviour of multiple user creating one
# public channel each
def test_channels_list_all_multi_users_one_channel_each_public(get_token_1, get_token_2):
    listall_helper_create_multiple(get_token_1, get_token_2, 2, True, False)

# should not rause any error
#
# Test the behaviour of multiple user creating one
# private channel each
def test_channels_list_all_multi_users_one_channel_each_private(get_token_1, get_token_2):
    listall_helper_create_multiple(get_token_1, get_token_2, 2, False, False)

# should not raise any error
#
# Test the behaviour of 2 user one creating a public channel
# and another one creates a private channel
def test_channels_list_all_multi_users_pub_and_priv_channels_respectively(get_token_1, get_token_2):
    listall_helper_create_multiple(get_token_1, get_token_2, 2, False, True)

# should not raise any error
#
# Test the behaviour of multiple user creating 
# multiple public channels
def test_channels_list_all_multi_user_multi_channels_public(get_token_1, get_token_2):
    listall_helper_create_multiple(get_token_1, get_token_2, len(NAMES_LIST), True, False)

# should not raise any error
#
# Test the behaviour of multiple user creating 
# multiple private channels
def test_channels_list_all_multi_user_multi_channels_private(get_token_1, get_token_2):
    listall_helper_create_multiple(get_token_1, get_token_2, len(NAMES_LIST), False, False)

# should not raise any error
#
# Test the behaviour of multiple user creating
# multiple public and private channels
def test_channels_list_all_multi_user_pub_and_priv_channels(get_token_1, get_token_2):
    listall_helper_create_multiple(get_token_1, get_token_2, len(NAMES_LIST), False, True)

# Should raise access error
#
# When:     auth_user_id is invalid
#
# Test for passing in invalid user id
def test_channels_list_all_access_error():
    resp = requests.get(ENDPOINT_LISTALL, {'token': INVALID_TOKEN})

    assert resp.status_code == AccessError.code
