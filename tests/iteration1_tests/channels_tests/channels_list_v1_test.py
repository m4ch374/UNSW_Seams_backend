"""
# ============= Channels list v1 ===================
# This section tests for the function
# channels_list_v1()
# ==================================================
"""

# Imports
import pytest

# Import funtions
import src.channels as chnl
import src.channel as channel

# Import errors
from src.error import AccessError

# Import definitions
from tests.iteration1_tests.channels_tests.definitions import NAMES_LIST

# Helper funtion
# helper funtion for testing channels list with one user
# creating n channels
def list_helper_create_single(usr_1, n, is_public):
    local_name_list = NAMES_LIST[:n]

    for name in local_name_list:
        chnl.channels_create_v1(usr_1, name, is_public)
    
    channel_list = chnl.channels_list_v1(usr_1)['channels']
    expected_output = [{'channel_id': i + 1, 'name': name} for i, name in enumerate(local_name_list)]
    assert channel_list == expected_output

# helper function for testing channels list with multiple user
# creating n channels
def list_helper_create_multiple(usr_1, usr_2, n, is_public):
    local_name_list = NAMES_LIST[:n]

    for i, name in enumerate(local_name_list):
        if i % 2:
            chnl.channels_create_v1(usr_1, name, is_public)
        else:
            chnl.channels_create_v1(usr_2, name, is_public)

    channel_list_usr_1 = chnl.channels_list_v1(usr_1)['channels']
    channel_list_usr_2 = chnl.channels_list_v1(usr_2)['channels']

    expected_output_1 = [{'channel_id': i + 1, 'name': name} for i, name in enumerate(local_name_list) if i % 2]
    expected_output_2 = [{'channel_id': i + 1, 'name': name} for i, name in enumerate(local_name_list) if not i % 2]

    assert channel_list_usr_1 == expected_output_1
    assert channel_list_usr_2 == expected_output_2

# Should not raise any error
#
# Test the behaviour with only one user creating one channel
def test_channels_list_single_user_one_channel(auth_user_id):
    list_helper_create_single(auth_user_id, 1, True)

# Should not raise any error
#
# Test the behaviour with only one user creating multiple channels
def test_channels_list_single_user_multi_channels(auth_user_id):
    list_helper_create_single(auth_user_id, len(NAMES_LIST), True)

# should not raise any error
#
# Test the behaviour with multiple user creating one channel each
def test_channels_list_multi_users_one_channel_each(auth_user_id, another_id):
    list_helper_create_multiple(auth_user_id, another_id, 2, True)

# should not raise any error
#
# Test the behaviour with multiple user creating multiple channel each
def test_channels_list_multi_users_multi_channels(auth_user_id, another_id):
    list_helper_create_multiple(auth_user_id, another_id, len(NAMES_LIST), True)

# should not raise any error
#
# Test the behaviour with one user with no groups associated
def test_channels_list_single_user_no_channel(auth_user_id):
    channel_list = chnl.channels_list_v1(auth_user_id)['channels']
    assert channel_list == []

# should not raise any error
#
# Test the behaviour with multiple user creating multiple channels and
# joining different channels
def test_channels_list_multi_user_multi_channels_with_join(auth_user_id, another_id):
    for i, name in enumerate(NAMES_LIST):
        if i % 2 == 0:
            chnl.channels_create_v1(auth_user_id, name, True)
        else:
            chnl.channels_create_v1(another_id, name, True)
            

    for i in range(1, len(NAMES_LIST) + 1):
        if i % 2 == 0:
            channel.channel_join_v1(auth_user_id, i)
        else:
            channel.channel_join_v1(another_id, i)

    # Assertion will fail as join() wasnt finished
    expected_output_1 = [{'channel_id': i + 1, 'name': name} for i, name in enumerate(NAMES_LIST)]
    expected_output_2 = [{'channel_id': i + 1, 'name': name} for i, name in enumerate(NAMES_LIST)]
    
    assert chnl.channels_list_v1(auth_user_id)['channels'] == expected_output_1
    assert chnl.channels_list_v1(another_id)['channels'] == expected_output_2
