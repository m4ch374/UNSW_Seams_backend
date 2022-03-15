import pytest
from src.error import InputError
from src.auth import auth_register_v2
from src.auth import user_profile_setname_v1
from src.auth import user_profile_v1
from src.other import clear_v1

def test_invalid_token():
    clear_v1()
    auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    token = '123123123123'
    assert user_profile_setname_v1(token, 'James', 'Bond') == None

def test_long_name():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    long_name = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    with pytest.raises(InputError):
        assert user_profile_setname_v1(user['token'], long_name, 'Bond')
    with pytest.raises(InputError):
        assert user_profile_setname_v1(user['token'], 'James', long_name)

def test_short_name():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    short_name = ''
    with pytest.raises(InputError):
        assert user_profile_setname_v1(user['token'], short_name, 'Bond')
    with pytest.raises(InputError):
        assert user_profile_setname_v1(user['token'], 'James', short_name)

def test_valid_input():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert user_profile_setname_v1(user['token'], 'James', 'Bond') == {}
    assert user_profile_v1(user['token'], user['auth_user_id']) == {'id': 1, 'email': 'z5555555@ed.unsw.edu.au', 'name_first': 'James', 'name_last': 'Bond', 'handle': 'williamwu'}

