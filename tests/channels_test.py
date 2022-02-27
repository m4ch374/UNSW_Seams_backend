# ==================== Note =======================
# Since the structure of the channels is not yet
# defined, this piece of testing is half finished
#
# Will modify once the structure is set
# ==================================================

import pytest
import src.channels as chnl
import src.auth as auth

from src.error import InputError
from src.other import clear_v1
from src.data_store import data_store

# =============== Global fixtures ==================
# These are the fixtures that would be used accross
# all tests
#
# A dummy user id
@pytest.fixture
def auth_user_id():
    auth_id = auth.auth_register_v1(
        'z100@ed.unsw.edu.au', 
        '1234567', 
        'Donald', 
        'Trump'
    )
    return auth_id

# Returns another dummy user id
@pytest.fixture
def another_id():
    auth_id = auth.auth_register_v1(
        'z200@ed.unsw.edu.au', 
        '1234567', 
        'qqqqqqqqqq', 
        'qqqqqqqqqq'
    )
    return auth_id

# Returns a valid channel name
@pytest.fixture
def channel_name():
    return "This is a name"
# ==================================================

# ============= Channels create v1 =================
# This section tests for the function
# channels_create_v1()
#
# Returns a list of channels names that could cause error
@pytest.fixture
def error_list():
    err_list = [
        None,                               # NULL
        "",                                 # Empty name
        "abcdefghijklmnopqrstu",            # 21 chars
        "...............................",  # non english chars
        "                               ",  # whitespaces with len > 20
        "123456789012345678901",            # numbers
        "!!!!!!!ldjfljasdlkjklsdj894",      # special chars, english chars and nums
    ]
    return err_list

# Returns a list of channel names that would not cause error
@pytest.fixture
def names_list():
    names_list = [
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
    return names_list

# Should raise input error
#
# When:     length of name < 1 ||
#           Length of name > 20
#
# Test for creating public channels
def test_channels_create_error_public(auth_user_id, error_list):
    clear_v1()
    with pytest.raises(InputError):
        for s in error_list:
            chnl.channels_create_v1(auth_user_id, s, True)

# Should raise input error
#
# When:     length of name < 1 ||
#           Length of name > 20
#
# Test for creating private channels
def test_channels_create_error_private(auth_user_id, error_list):
    clear_v1()
    with pytest.raises(InputError):
        for s in error_list:
            chnl.channels_create_v1(auth_user_id, s, False)

# Should raise input error
#
# When:     length of name < 1 ||
#           Length of name > 20
#
# Test for creating both public and private channels
def test_channels_create_error_pub_and_priv(auth_user_id, error_list):
    clear_v1()
    with pytest.raises(InputError):
        for s in error_list:
            chnl.channels_create_v1(auth_user_id, s, True)
            chnl.channels_create_v1(auth_user_id, s, False)

# Should not raise any error
# 
# Test for creating valid public channels
def test_channels_create_public(auth_user_id, names_list):
    clear_v1()
    for name in names_list:
        val = chnl.channels_create_v1(auth_user_id, name, True)

        channel_list = data_store.get()['channel']
        assert val == { 'channel_id': len(channel_list) }

# Should not raise any error
# 
# Test for creating valid private channels
def test_channels_create_private(auth_user_id, names_list):
    clear_v1()
    for name in names_list:
        val = chnl.channels_create_v1(auth_user_id, name, False)

        channel_list = data_store.get()['channel']
        assert val == { 'channel_id': len(channel_list) }

# Should not raise any error
# 
# Test for creating both valid public and private channels
def test_channels_create_pub_and_priv(auth_user_id, names_list):
    clear_v1()
    for name in names_list:
        val = chnl.channels_create_v1(auth_user_id, name, True)
        val_1 = chnl.channels_create_v1(auth_user_id, name, False)

        channel_list = data_store.get()['channel']
        assert val == { 'channel_id': len(channel_list) - 1 }
        assert val_1 == { 'channel_id': len(channel_list) }

# ==================================================


# ============== Channels list v1 ==================
#
# Should not raise any error
#
# Test the behaviour with only one user creating on channel
def test_channels_list_1(auth_user_id, channel_name):
    clear_v1()
    chnl.channels_create_v1(auth_user_id, channel_name, True)
    val = chnl.channels_list_v1(auth_user_id)
    assert val['channels'][0]['owner_id'] == auth_user_id and len(val['channels']) == 1

# Should not raise any error
#
# Test the behaviour with only one user creating multiple channels
def test_channels_list_2(auth_user_id, channel_name):
    clear_v1()

    # User creates 5 channels
    for i in range(5):
        chnl.channels_create_v1(auth_user_id, channel_name, True)
    
    channel_list = chnl.channels_list_v1(auth_user_id)['channels']
    assert (all(channel['owner_id'] == auth_user_id for channel in channel_list) and
        len(channel_list) == 5)

# should not raise any error
#
# Test the behaviour with multiple user creating one channel each
def test_channels_list_3(auth_user_id, another_id, channel_name):
    clear_v1()

    chnl.channels_create_v1(auth_user_id, channel_name, True)
    chnl.channels_create_v1(another_id, channel_name, True)

    channel_list_usr_1 = chnl.channels_list_v1(auth_user_id)['channels']
    channel_list_usr_2 = chnl.channels_list_v1(another_id)['channels']

    assert (all(channel['owner_id'] == auth_user_id for channel in channel_list_usr_1) and
        len(channel_list_usr_1) == 1)
    assert (all(channel['owner_id'] == another_id for channel in channel_list_usr_2) and
        len(channel_list_usr_2) == 1) 

# should not raise any error
#
# Test the behaviour with multiple user creating multiple channel each
def test_channels_list_4(auth_user_id, another_id, channel_name):
    clear_v1()

    for i in range(5):
        chnl.channels_create_v1(auth_user_id, channel_name, True)
        chnl.channels_create_v1(another_id, channel_name, True)

    channel_list_usr_1 = chnl.channels_list_v1(auth_user_id)['channels']
    channel_list_usr_2 = chnl.channels_list_v1(another_id)['channels']

    assert (all(channel['owner_id'] == auth_user_id for channel in channel_list_usr_1) and
        len(channel_list_usr_1) == 5)
    assert (all(channel['owner_id'] == another_id for channel in channel_list_usr_2) and
        len(channel_list_usr_2) == 5) 

# should not raise any error
#
# Test the behaviour with one user with no groups associated
def test_channels_list_5(auth_user_id):
    clear_v1()

    channel_list = chnl.channels_list_v1(auth_user_id)['channels']
    assert len(channel_list) == 0

# ==================================================

# ============ Channels list all v1 =================
#
# should not raise any error
#
# Test the behaviour of one user creating one public channel
def test_channels_list_all_1(auth_user_id, channel_name):
    clear_v1()

    chnl.channels_create_v1(auth_user_id, channel_name, True)
    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 1

# should not raise any error
#
# Test the behaviour of one user creating one private channel
def test_channels_list_all_2(auth_user_id, channel_name):
    clear_v1()

    chnl.channels_create_v1(auth_user_id, channel_name, False)
    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 1

# should not raise any error
#
# Test the behaviour of one user creating one private channel
# and one public channel
def test_channels_list_all_3(auth_user_id, channel_name):
    clear_v1()

    chnl.channels_create_v1(auth_user_id, channel_name, False)
    chnl.channels_create_v1(auth_user_id, channel_name, True)
    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 2

# should not raise any error
#
# Test the behaviour of one user creating multiple public channels
def test_channels_list_all_4(auth_user_id, channel_name):
    clear_v1()

    for i in range(5):
        chnl.channels_create_v1(auth_user_id, channel_name, True)
    
    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 5

# should not raise any error
#
# Test the behaviour of one user creating multiple private channels
def test_channels_list_all_5(auth_user_id, channel_name):
    clear_v1()

    for i in range(5):
        chnl.channels_create_v1(auth_user_id, channel_name, False)
    
    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 5

# should not rause any error
#
# Test the behaviour of multiple user creating one
# public channel each
def test_channels_list_all_6(auth_user_id, another_id, channel_name):
    clear_v1()

    chnl.channels_create_v1(auth_user_id, channel_name, True)
    chnl.channels_create_v1(another_id, channel_name, True)

    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 2
    assert len(chnl.channels_listall_v1(another_id)['channels']) == 2

# should not rause any error
#
# Test the behaviour of multiple user creating one
# private channel each
def test_channels_list_all_7(auth_user_id, another_id, channel_name):
    clear_v1()

    chnl.channels_create_v1(auth_user_id, channel_name, False)
    chnl.channels_create_v1(another_id, channel_name, False)

    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 2
    assert len(chnl.channels_listall_v1(another_id)['channels']) == 2

# should not raise any error
#
# Test the behaviour of 2 user one creating a public channel
# and another one creates a private channel
def test_channels_list_all_8(auth_user_id, another_id, channel_name):
    clear_v1()

    chnl.channels_create_v1(auth_user_id, channel_name, True)
    chnl.channels_create_v1(another_id, channel_name, False)

    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 2
    assert len(chnl.channels_listall_v1(another_id)['channels']) == 2

# should not raise any error
#
# Test the behaviour of multiple user one creating 
# multiple public channels
def test_channels_list_all_9(auth_user_id, another_id, channel_name):
    clear_v1()

    for i in range(5):
        chnl.channels_create_v1(auth_user_id, channel_name, True)
        chnl.channels_create_v1(another_id, channel_name, True)

    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 10
    assert len(chnl.channels_listall_v1(another_id)['channels']) == 10

# should not raise any error
#
# Test the behaviour of multiple user one creating 
# multiple private channels
def test_channels_list_all_10(auth_user_id, another_id, channel_name):
    clear_v1()

    for i in range(5):
        chnl.channels_create_v1(auth_user_id, channel_name, False)
        chnl.channels_create_v1(another_id, channel_name, False)

    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 10
    assert len(chnl.channels_listall_v1(another_id)['channels']) == 10

# should not raise any error
#
# Test the behaviour of multiple user creating
# multiple public and private channels
def test_channels_list_all_11(auth_user_id, another_id, channel_name):
    clear_v1()

    for i in range(5):
        chnl.channels_create_v1(auth_user_id, channel_name, True)
        chnl.channels_create_v1(another_id, channel_name, False)

    assert len(chnl.channels_listall_v1(auth_user_id)['channels']) == 10
    assert len(chnl.channels_listall_v1(another_id)['channels']) == 10

# ==================================================