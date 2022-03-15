import pytest
from src.error import InputError
from src.auth import auth_register_v2
from src.auth import user_profile_sethandle_v1
from src.auth import user_profile_v1
from src.other import clear_v1

def test_invalid_token():
    clear_v1()
    auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    token = '123123123123'
    assert user_profile_sethandle_v1(token, 'jamesbond') == None

def test_long_handle():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    long_handle = 'xxxxxxxxxxxxxxxxxxxxxx'
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(user['token'], long_handle)

def test_short_handle():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    short_handle = 'x'
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(user['token'], short_handle)

def test_invalid_handle():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(user['token'], '@#$%AS123')

def test_exist_handle():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(user['token'], 'williamwu')

def test_valid_input():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert user_profile_sethandle_v1(user['token'], 'jamesbond') == {}
    assert user_profile_v1(user['token'], user['auth_user_id']) == {'id': 1, 'email': 'z5555555@ed.unsw.edu.au', 'name_first': 'William', 'name_last': 'Wu', 'handle': 'jamesbond'}

