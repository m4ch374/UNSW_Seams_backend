"""
# ============= Channels create v1 =================
# This section tests for the function
# channels_create_v1()
# ==================================================
"""

# Imports
import pytest

# Import funtions
import src.channels as chnl

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration1_tests.channels_tests.definitions import ERROR_LIST, NAMES_LIST

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
