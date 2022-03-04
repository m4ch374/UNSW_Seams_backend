from re import A
import pytest
from src.error import InputError, AccessError

from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.auth import auth_register_v1

from src.other import clear_v1
from src.data_store import data_store


# Registers user 1 and has them create channel 1
@pytest.fixture
def initialise_user_and_channel():
    clear_v1()
    auth_register_v1('z5555555@ad.unsw.edu.au', '123456a', 'Anthony', 'Smith')
    channels_create_v1(1, 'Ant', 'y')


####################################################
##          Tests for channel_details_v1          ##
####################################################
#
# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
# AccessError when:
#   - channel_id is valid and the authorised user is not a member of the
#     channel
# ==================================================
#user, channel

# Test invalid channel id where id doesn't exist yet
def test_channel_details_invalid_channel_id(initialise_user_and_channel):
    with pytest.raises(InputError):
        assert channel_details_v1(1, 2)

# Test invalid user id where id doesn't exist yet
def test_channel_details_invalid_user_id(initialise_user_and_channel):
    with pytest.raises(AccessError):
        assert channel_details_v1(2, 1)

# Test invalid user access permissions
def test_channel_details_invalid_access(initialise_user_and_channel):
    auth_register_v1('z5222222@ad.unsw.edu.au', 'abcde123', 'Brian', 'Smith')
    with pytest.raises(AccessError):
        assert channel_details_v1(2, 1)


# Test that AccessError is raised when both user and channel ids are invalid
def test_channel_details_invalid_channel_and_user(initialise_user_and_channel):
    with pytest.raises(AccessError):
        assert channel_details_v1(2, 2)
