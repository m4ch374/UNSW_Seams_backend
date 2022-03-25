"""
# ============ Channels list all v1 =================
# This section tests for the function
# channels_list_all_v1()
# ==================================================
"""

# Imports
import pytest

# Import funtions
import src.channels as chnl

# Import errors
from src.error import AccessError

# Import definitions
from tests.iteration1_tests.channels_tests.definitions import NAMES_LIST

# Helper function
# helper function for testing listall with one user creating
# n channels
#
# NOTE: if is_alt is True, is_public will have no effect
# since the channels created will alternate between public and private 
def listall_helper_create_single(usr_1, n, is_public, is_alt):
    local_name_list = NAMES_LIST[:n]

    for i, name in enumerate(local_name_list):
        if is_alt:
            chnl.channels_create_v1(usr_1, name, i % 2)
        else:
            chnl.channels_create_v1(usr_1, name, is_public)
    
    expected_output = [{'channel_id': i + 1, 'name': name} for i, name in enumerate(local_name_list)]
    assert chnl.channels_listall_v1(usr_1)['channels'] == expected_output

# helper function for testing listall with multiple user creating
# n public and private channels
def listall_helper_create_multiple(usr_1, usr_2, n, is_public, is_alt):
    local_name_list = NAMES_LIST[:n]

    for i, name in enumerate(local_name_list):
        if i % 2:
            chnl.channels_create_v1(usr_1, name, is_public)
        else:
            pub = is_public if not is_alt else not is_public
            chnl.channels_create_v1(usr_2, name, pub)

    expected_output_1 = [{'channel_id': i + 1, 'name': name} for i, name in enumerate(local_name_list)]
    expected_output_2 = [{'channel_id': i + 1, 'name': name} for i, name in enumerate(local_name_list)]
    
    assert chnl.channels_listall_v1(usr_1)['channels'] == expected_output_1
    assert chnl.channels_listall_v1(usr_2)['channels'] == expected_output_2

# should not raise any error
#
# Test the behaviour of one user creating one public channel
def test_channels_list_all_single_user_single_channel_public(auth_user_id):
    listall_helper_create_single(auth_user_id, 1, True, False)

# should not raise any error
#
# Test the behaviour of one user creating one private channel
def test_channels_list_all_single_user_single_channel_private(auth_user_id):
    listall_helper_create_single(auth_user_id, 1, False, False)

# should not raise any error
#
# Test the behaviour of one user creating one private channel
# and one public channel
def test_channels_list_all_single_user_pub_and_priv_each(auth_user_id):
    listall_helper_create_single(auth_user_id, 2, False, True)

# should not raise any error
#
# Test the behaviour of one user creating multiple public channels
def test_channels_list_all_single_user_multi_channels_public(auth_user_id):
    listall_helper_create_single(auth_user_id, len(NAMES_LIST), True, False)

# should not raise any error
#
# Test the behaviour of one user creating multiple private channels
def test_channels_list_all_single_user_multi_channels_private(auth_user_id):
    listall_helper_create_single(auth_user_id, len(NAMES_LIST), False, False)

# should not rause any error
#
# Test the behaviour of multiple user creating one
# public channel each
def test_channels_list_all_multi_users_one_channel_each_public(auth_user_id, another_id):
    listall_helper_create_multiple(auth_user_id, another_id, 2, True, False)

# should not rause any error
#
# Test the behaviour of multiple user creating one
# private channel each
def test_channels_list_all_multi_users_one_channel_each_private(auth_user_id, another_id):
    listall_helper_create_multiple(auth_user_id, another_id, 2, False, False)

# should not raise any error
#
# Test the behaviour of 2 user one creating a public channel
# and another one creates a private channel
def test_channels_list_all_multi_users_pub_and_priv_channels_respectively(auth_user_id, another_id):
    listall_helper_create_multiple(auth_user_id, another_id, 2, False, True)

# should not raise any error
#
# Test the behaviour of multiple user creating 
# multiple public channels
def test_channels_list_all_multi_user_multi_channels_public(auth_user_id, another_id):
    listall_helper_create_multiple(auth_user_id, another_id, len(NAMES_LIST), True, False)

# should not raise any error
#
# Test the behaviour of multiple user creating 
# multiple private channels
def test_channels_list_all_multi_user_multi_channels_private(auth_user_id, another_id):
    listall_helper_create_multiple(auth_user_id, another_id, len(NAMES_LIST), False, False)

# should not raise any error
#
# Test the behaviour of multiple user creating
# multiple public and private channels
def test_channels_list_all_multi_user_pub_and_priv_channels(auth_user_id, another_id):
    listall_helper_create_multiple(auth_user_id, another_id, len(NAMES_LIST), False, True)
