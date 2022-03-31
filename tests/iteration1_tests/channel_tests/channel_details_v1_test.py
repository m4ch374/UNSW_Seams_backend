import pytest
from src.error import InputError, AccessError

from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_list_v1
from src.auth import auth_register_v1


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
def test_channel_details_invalid_channel_id(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(InputError):
        assert channel_details_v1(user, channel + 1)

# Test invalid user id where id doesn't exist yet
def test_channel_details_invalid_user_id(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(AccessError):
        assert channel_details_v1(user + 1, channel)

# Test invalid user access permissions
def test_channel_details_invalid_access(first_user_and_channel):
    channel = first_user_and_channel['first_channel_id']
    second_user = auth_register_v1('z5555551@ad.unsw.edu.au', '123456b', 'Brian', 'Smith')['auth_user_id']
    
    with pytest.raises(AccessError):
        assert channel_details_v1(second_user, channel)

# Test that correct channel details are returned when all inputs valid
def test_channel_details_simple(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    assert len(channel_details_v1(user, channel)['owner_members']) == 1
    assert len(channel_details_v1(user, channel)['all_members']) == 1

