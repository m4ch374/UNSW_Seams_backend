import pytest
from src.error import InputError, AccessError
from src.channel import channel_messages_v1
from src.other import clear_v1


def test_invalid_channel_id():
    clear_v1()
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 5, 0)


def test_invalid_start_messgae_id_1():
    clear_v1()
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 1, -2)


def test_invalid_start_messgae_id_2():
    clear_v1()
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 2, 1)


def test_user_not_authorised():
    clear_v1()
    with pytest.raises(AccessError):
        assert channel_messages_v1(3, 1, 0)


def test_end_returns():
    clear_v1()
    assert channel_messages_v1(1, 2, 0) == ({'messages': [
        {'message_id': 0, 'id': 1, 'string': 'hi', 'time': '07:41:19'}], 'start': 0, 'end': -1})
