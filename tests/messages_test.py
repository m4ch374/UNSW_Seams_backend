import pytest
from src.error import InputError, AccessError

from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.auth import auth_register_v1

# Registers user 1 and has them create channel 1
@pytest.fixture
def first_user_and_channel():
    clear_v1()
    first_user_id = auth_register_v1('z5555555@ad.unsw.edu.au', '123456a', 'Anthony', 'Smith')['auth_user_id']
    first_channel_id = channels_create_v1(first_user_id, 'Ant', True)['channel_id']

    return {'first_user_id': first_user_id, 'first_channel_id': first_channel_id}
   
# Test for invalid channel id where id doesn't exist yet
def test_invalid_channel_id(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(InputError):
        assert channel_messages_v1(user, channel + 1, 0)

# Test for invalid start id where id doesn't exist yet
def test_invalid_start_messgae_id_1(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(InputError):
        assert channel_messages_v1(user, channel, 1)

# Test for invalid start id where id is negative
def test_invalid_start_messgae_id_2(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(InputError):
        assert channel_messages_v1(user, channel, -2)

# Test for invalid user id where id doesn't exist yet
def test_invalid_user_id(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(AccessError):
        assert channel_messages_v1(user + 1, channel, 0)

# Test that AccessError is raised when both user and channel id are invalid
def test_invalid_user_and_channel(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(AccessError):
        assert channel_messages_v1(user + 1, channel + 1, 0)

# Test that AccessError is raised when both user and start id are invalid
def test_invalid_user_and_start(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(AccessError):
        assert channel_messages_v1(user + 1, channel, -1)

# Test that AccessError is raised when both user, channel and start id are invalid
def test_invalid_user_channel_start(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(AccessError):
        assert channel_messages_v1(user + 1, channel + 1, 1)

# Test for non-member user trying to access channel messages
def test_user_not_authorised(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']
    second_user = auth_register_v1('z5222222@ad.unsw.edu.au', 'abcde123', 'Brian', 'Smith')['auth_user_id']

    with pytest.raises(AccessError):
        assert channel_messages_v1(second_user, channel, 0)

# Test that a -1 is returned once the end of messages list is reached
def test_end_returns_neg1_when_finished(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    assert channel_messages_v1(user, channel, 0) == {'messages': [], 'start': 0, 'end': -1}
        

# Further tests to be implemented once send_messages function is implemented.