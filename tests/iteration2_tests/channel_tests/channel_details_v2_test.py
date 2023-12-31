'''
####################################################
##          Tests for channel/details/v2           ##
####################################################

# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
# AccessError when:
#   - channel_id is valid and the authorised user is not a member of the
#     channel
#   - user token is invalid
# ==================================================
'''
# Imports
import requests

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration2_tests.endpoints import ENDPOINT_CHANNEL_DETAILS

# Test invalid channel
def test_channel_details_invalid_channel_id(user_1_made_channel):
    token = user_1_made_channel['token']
    channel = user_1_made_channel['channel']

    response = requests.get(f'{ENDPOINT_CHANNEL_DETAILS}?token={token}&channel_id={str(channel+1)}')
    response_code = response.status_code
    assert response_code == InputError.code

# Test invalid user token
def test_channel_details_invalid_user_id(user_1_made_channel):
    channel = user_1_made_channel['channel']

    response = requests.get(
        f'{ENDPOINT_CHANNEL_DETAILS}?token="bad_token"&channel_id={str(channel)}')
    response_code = response.status_code
    assert response_code == AccessError.code

# Test invalid user access permissions
def test_channel_details_invalid_access(user_1_made_channel, get_usr_2):
    channel = user_1_made_channel['channel']
    invalid_token = get_usr_2['token']

    response = requests.get(
        f'{ENDPOINT_CHANNEL_DETAILS}?token={invalid_token}&channel_id={str(channel)}')
    response_code = response.status_code
    assert response_code == AccessError.code

# Test that AccessError is raised when both user and channel ids are invalid
def test_channel_details_invalid_channel_and_user(user_1_made_channel):
    channel = user_1_made_channel['channel']

    response = requests.get(
        f'{ENDPOINT_CHANNEL_DETAILS}?token={"invalid_token"}&channel_id={str(channel + 1)}')
    response_code = response.status_code
    assert response_code == AccessError.code

# Test that correct channel details are returned when all inputs valid
def test_channel_details_simple(user_1_made_channel):
    token = user_1_made_channel['token']
    channel = user_1_made_channel['channel']

    response = requests.get(
        f'{ENDPOINT_CHANNEL_DETAILS}?token={token}&channel_id={str(channel)}')
    assert len(response.json()['owner_members']) == 1
    assert len(response.json()['all_members']) == 1
    # assert response.json() == {'name': 'chnl_name',
    #                             'is_public': True,
    #                             'owner_members': [{'email': 'randomemail@gmail.com',
    #                                                 'handle_str': 'joebidome',
    #                                                 'name_first': 'joe',
    #                                                 'name_last': 'bidome',
    #                                                 'u_id': 1,},],
    #                             'all_members': [{'email': 'randomemail@gmail.com',
    #                                                 'handle_str': 'joebidome',
    #                                                 'name_first': 'joe',
    #                                                 'name_last': 'bidome',
    #                                                 'u_id': 1,},]}
