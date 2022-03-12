import pytest

import src.channels as chnl
import src.channel as channel
import src.auth as auth

from src.error import InputError, AccessError
from src.other import clear_v1

# ================= Definitions ====================

# A list of channel names that could cause errors
ERROR_LIST = [
        None,                               # NULL
        "",                                 # Empty name
        "abcdefghijklmnopqrstu",            # 21 chars
        "...............................",  # non english chars
        "                               ",  # whitespaces with len > 20
        "123456789012345678901",            # numbers
        "!!!!!!!ldjfljasdlkjklsdj894",      # special chars, english chars and nums
    ]

# A list of channel names that are valid
NAMES_LIST = [
        "a",                    # single character
        "abcdef",               # english character
        "123456",               # nums
        "there is something",   # str with whitespaces
        "           ",          # str with all whitespaces
        "1234567890abcdefg![]", # combined strings, len == 20
        "trailing whitespace ", # str with trailing whitespace
        "a",                    # duplications
        "!!!!!!![[[]]]!!!!!!!", # all special chars
    ]

INVALID_ID = -1
# ==================================================

# ============= Channels create v1 =================
# This section tests for the function
# channels_create_v1()

# Should raise input error
#
# When:     length of name < 1 ||
#           Length of name > 20
#
# Test for creating public channels
def test_channels_create_error_public(auth_user_id):
    with pytest.raises(InputError):
        for s in ERROR_LIST:
            chnl.channels_create_v1(auth_user_id, s, True)

# Should raise input error
#
# When:     length of name < 1 ||
#           Length of name > 20
#
# Test for creating private channels
def test_channels_create_error_private(auth_user_id):
    with pytest.raises(InputError):
        for s in ERROR_LIST:
            chnl.channels_create_v1(auth_user_id, s, False)

# Should raise input error
#
# When:     length of name < 1 ||
#           Length of name > 20
#
# Test for creating both public and private channels
def test_channels_create_error_pub_and_priv(auth_user_id):
    with pytest.raises(InputError):
        for s in ERROR_LIST:
            chnl.channels_create_v1(auth_user_id, s, True)
            chnl.channels_create_v1(auth_user_id, s, False)

# Should raise access error
#
# When:     auth_user_id is invalid
#
# Test passing in invalid user id
def test_channels_create_error_invalid_id():
    with pytest.raises(AccessError):
        chnl.channels_create_v1(INVALID_ID, "dummy", True)

# Should not raise any error
# 
# Test for creating valid public channels
def test_channels_create_public(auth_user_id):
    for i, name in enumerate(NAMES_LIST):
        val = chnl.channels_create_v1(auth_user_id, name, True)

        assert val == { 'channel_id': i + 1 }

# Should not raise any error
# 
# Test for creating valid private channels
def test_channels_create_private(auth_user_id):
    for i, name in enumerate(NAMES_LIST):
        val = chnl.channels_create_v1(auth_user_id, name, False)

        assert val == { 'channel_id': i + 1 }

# Should not raise any error
# 
# Test for creating both valid public and private channels
def test_channels_create_pub_and_priv(auth_user_id):
    for i, name in enumerate(NAMES_LIST):
        val = chnl.channels_create_v1(auth_user_id, name, True)
        val_1 = chnl.channels_create_v1(auth_user_id, name, False)

        assert val == { 'channel_id': i * 2 + 1 }
        assert val_1 == { 'channel_id': i * 2 + 2 }

# ==================================================


# ============== Channels list v1 ==================
#
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

# Should raise access error
#
# When:     auth_user_id is invalid
#
# Test for passing in invalid user id
def test_channels_list_access_error():
    with pytest.raises(AccessError):
        chnl.channels_list_v1(INVALID_ID)

# ==================================================

# ============ Channels list all v1 =================
#
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

# Should raise access error
#
# When:     auth_user_id is invalid
#
# Test for passing in invalid user id
def test_channels_list_all_access_error():
    with pytest.raises(AccessError):
        chnl.channels_listall_v1(INVALID_ID)

# ==================================================
