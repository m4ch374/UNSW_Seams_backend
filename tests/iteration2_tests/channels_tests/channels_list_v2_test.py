"""
# ============= Channels list v2 ===================
# This section tests for the endpoint
# channels/list/v2
# ==================================================
"""

# Imports
import requests

# Import errors
from src.error import AccessError

# Import definitions
from tests.iteration2_tests.channels_tests.definitions import NAMES_LIST, INVALID_TOKEN
from tests.iteration2_tests.endpoints import ENDPOINT_CREATE_CHNL, ENDPOINT_LIST_CHNL, ENDPOINT_JOIN_CHNL

# Import helpers
from tests.iteration2_tests.helper import generate_channel_input_json

# Helper funtion
# helper funtion for testing channels list with one user
# creating n channels
def list_helper_create_single(tok_1, n, is_public):
    local_name_list = NAMES_LIST[:n]

    expected_output = []
    for name in local_name_list:
        data = generate_channel_input_json(tok_1, name, is_public)
        resp = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()
        expected_output.append({'channel_id': resp['channel_id'], 'name': name})
    
    channel_list = requests.get(ENDPOINT_LIST_CHNL, {'token': tok_1}).json()['channels']
    assert channel_list == expected_output

# helper function for testing channels list with multiple user
# creating n channels
def list_helper_create_multiple(tok_1, tok_2, n, is_public):
    local_name_list = NAMES_LIST[:n]

    expected_output_1 = []
    expected_output_2= []
    for i, name in enumerate(local_name_list):
        if i % 2:
            data = generate_channel_input_json(tok_1, name, is_public)
            resp = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()
            expected_output_1.append({'channel_id': resp['channel_id'], 'name': name})
        else:
            data = generate_channel_input_json(tok_2, name, is_public)
            resp = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()
            expected_output_2.append({'channel_id': resp['channel_id'], 'name': name})

    channel_list_tok_1 = requests.get(ENDPOINT_LIST_CHNL, {'token': tok_1}).json()['channels']
    channel_list_tok_2 = requests.get(ENDPOINT_LIST_CHNL, {'token': tok_2}).json()['channels']

    assert channel_list_tok_1 == expected_output_1
    assert channel_list_tok_2 == expected_output_2

# Should not raise any error
#
# Test the behaviour with only one user creating one channel
def test_channels_list_single_user_one_channel(get_token_1):
    list_helper_create_single(get_token_1, 1, True)

# Should not raise any error
#
# Test the behaviour with only one user creating multiple channels
def test_channels_list_single_user_multi_channels(get_token_1):
    list_helper_create_single(get_token_1, len(NAMES_LIST), True)

# should not raise any error
#
# Test the behaviour with multiple user creating one channel each
def test_channels_list_multi_users_one_channel_each(get_token_1, get_token_2):
    list_helper_create_multiple(get_token_1, get_token_2, 2, True)

# should not raise any error
#
# Test the behaviour with multiple user creating multiple channel each
def test_channels_list_multi_users_multi_channels(get_token_1, get_token_2):
    list_helper_create_multiple(get_token_1, get_token_2, len(NAMES_LIST), True)

# should not raise any error
#
# Test the behaviour with one user with no groups associated
def test_channels_list_single_user_no_channel(get_token_1):
    resp = requests.get(ENDPOINT_LIST_CHNL, {'token': get_token_1}).json()
    channel_list = resp['channels']
    assert channel_list == []

# Commented until join is wrapped

# # should not raise any error
# #
# # Test the behaviour with multiple user creating multiple channels and
# # joining different channels
# def test_channels_list_multi_user_multi_channels_with_join(get_token_1, get_token_2):
#     expected_output = []

#     for i, name in enumerate(NAMES_LIST):
#         if i % 2 == 0:
#             data = generate_channel_input_json(get_token_1, name, True)
#             resp = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()
#             requests.post(ENDPOINT_JOIN_CHNL, json={'token': get_token_2, 'channel_id': resp['channel_id']})
#         else:
#             data = generate_channel_input_json(get_token_2, name, True)
#             resp = requests.post(ENDPOINT_CREATE_CHNL, json=data).json()
#             requests.post(ENDPOINT_JOIN_CHNL, json={'token': get_token_1, 'channel_id': resp['channel_id']})

#         expected_output.append({'channel_id': resp['channel_id'], 'name': name})
    
#     channel_list_tok_1 = requests.get(ENDPOINT_LIST_CHNL, {'token': get_token_1}).json()['channels']
#     channel_list_tok_2 = requests.get(ENDPOINT_LIST_CHNL, {'token': get_token_2}).json()['channels']
    
#     assert channel_list_tok_1 == expected_output
#     assert channel_list_tok_2 == expected_output

# Should raise access error
#
# When:     token is invalid
#
# Test for passing in invalid token
def test_channels_list_access_error():
    resp = requests.get(ENDPOINT_LIST_CHNL, {'token': INVALID_TOKEN})

    assert resp.status_code == AccessError.code
