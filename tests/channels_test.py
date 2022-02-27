import pytest
import src.channels as chnl

from src.error import InputError
from src.other import clear_v1
from src.data_store import data_store

# =============== Global fixtures ==================
# These are the fixtures that would be used accross
# all tests
#
# Runs this function before all tests
@pytest.fixture(scope="session", autouse=True)
def clear_data():
    clear_v1()

# A dummy user id
@pytest.fixture
def auth_user_id():
    return 1
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
    with pytest.raises(InputError):
        for s in error_list:
            chnl.channels_create_v1(auth_user_id, s, False)

# Should raise input error
#
# When:     length of name < 1 ||
#           Length of name > 20
#
# Test for creating private channels
def test_channels_create_error_private(auth_user_id, error_list):
    with pytest.raises(InputError):
        for s in error_list:
            chnl.channels_create_v1(auth_user_id, s, True)

# Should raise input error
#
# When:     length of name < 1 ||
#           Length of name > 20
#
# Test for creating both public and private channels
def test_channels_create_error_pub_and_priv(auth_user_id, error_list):
    test_channels_create_error_public(auth_user_id, error_list)
    test_channels_create_error_private(auth_user_id, error_list)

# Should not raise any error
# 
# Test for creating valid public channels
def test_channels_create_public(auth_user_id, names_list):
    for name in names_list:
        val = chnl.channels_create_v1(auth_user_id, name, False)

        channel_list = data_store.get()['channel']
        assert val == { 'channel_id': len(channel_list) }

# Should not raise any error
# 
# Test for creating valid private channels
def test_channels_create_private(auth_user_id, names_list):
    for name in names_list:
        val = chnl.channels_create_v1(auth_user_id, name, True)

        channel_list = data_store.get()['channel']
        assert val == { 'channel_id': len(channel_list) }

# Should not raise any error
# 
# Test for creating both valid public and private channels
def test_channels_create_pub_and_priv(auth_user_id, names_list):
    test_channels_create_public(auth_user_id, names_list)
    test_channels_create_private(auth_user_id, names_list)

# ==================================================


# ============== Channels list v1 ==================
def test_channels_list():
    pass

# ==================================================