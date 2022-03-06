import pytest
from src.error import InputError, AccessError

from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.auth import auth_register_v1

@pytest.fixture
def initialise_user_and_channel():
    clear_v1()
    valid_user_id_in_channel = auth_register_v1('z5555555@ad.unsw.edu.au', '123456a', 'Anthony', 'Smith')['auth_user_id']
    valid_channel = channels_create_v1(valid_user_id_in_channel, 'Ant', True)

# Test for invalid channel id where id doesn't exist yet
def test_invalid_channel_id(initialise_user_and_channel):
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 5, 0)

# Test for invalid start id where id doesn't exist yet
def test_invalid_start_messgae_id_1(initialise_user_and_channel):
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 1, 1)

# Test for invalid start id where id is negative
def test_invalid_start_messgae_id_2(initialise_user_and_channel):
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 1, -2)

# Test for invalid user id where id doesn't exist yet
def test_invalid_user_id(initialise_user_and_channel):
    with pytest.raises(AccessError):
        assert channel_messages_v1(2, 1, 0)

# Test that AccessError is raised when both user and channel id are invalid
def test_invalid_user_and_channel(initialise_user_and_channel):
    with pytest.raises(AccessError):
        assert channel_messages_v1(2, 2, 0)

# Test that AccessError is raised when both user and start id are invalid
def test_invalid_user_and_start(initialise_user_and_channel):
    with pytest.raises(AccessError):
        assert channel_messages_v1(2, 1, -1)

# Test that AccessError is raised when both user, channel and start id are invalid
def test_invalid_user_channel_start(initialise_user_and_channel):
    with pytest.raises(AccessError):
        assert channel_messages_v1(2, 2, -1)

# Test for non-member user trying to access channel messages
def test_user_not_authorised(initialise_user_and_channel):
    auth_register_v1('z5222222@ad.unsw.edu.au', 'abcde123', 'Brian', 'Smith')
    with pytest.raises(AccessError):
        assert channel_messages_v1(2, 1, 0)

# Test that a -1 is returned once the end of messages list is reached
def test_end_returns_neg1_when_finished(initialise_user_and_channel):
    assert channel_messages_v1(1, 1, 0) == {'messages': [], 'start': 0, 'end': -1}
        

# Further tests to be implemented once send_messages function is implemented.