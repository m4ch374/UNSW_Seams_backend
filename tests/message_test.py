import pytest
from src.error import InputError, AccessError
from src.channel import channel_messages_v1
from src.data_store import data_store

store = data_store.get()
new_user = {'email': 'z7654321@ed.unsw.edu.au', 'password': '1234567',
            'firstname': 'Jason', 'lastname': 'Smith', 'id': 1, 'handle': 'jasonsmith', }
store['users'].append(new_user)
new_user = {'email': 'z5555555@ed.unsw.edu.au', 'password': '123123123',
            'firstname': 'William', 'lastname': 'Wu', 'id': 2, 'handle': 'williamwu', }
store['users'].append(new_user)
new_user = {'email': 'z8888888@ed.unsw.edu.au', 'password': '321321321',
            'firstname': 'Russell', 'lastname': 'Wang', 'id': 3, 'handle': 'russellwu', }
store['users'].append(new_user)
new_channel = {'channel_id': 1, 'name': 'COMP1521',
               'members': [], 'messages': []}
store['channels'].append(new_channel)
new_channel = {'channel_id': 2, 'name': 'Ant', 'members': [store['users'][0]], 'messages': [
    {'message_id': 0, 'id': 1, 'string': 'hi', 'time': '07:41:19'}]}
store['channels'].append(new_channel)


def invalid_channel_id():
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 5, 0)


def invalid_start_messgae_id_1():
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 1, -2)


def invalid_start_messgae_id_2():
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 2, 1)


def user_not_authorised():
    with pytest.raises(AccessError):
        assert channel_messages_v1(3, 1, 0)


def test_end_returns():
    assert channel_messages_v1(1, 2, 0) == ({'messages': [
        {'message_id': 0, 'id': 1, 'string': 'hi', 'time': '07:41:19'}], 'start': 0, 'end': -1})
