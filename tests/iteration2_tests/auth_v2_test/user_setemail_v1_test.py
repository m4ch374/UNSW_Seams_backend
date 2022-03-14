import pytest
from src.error import InputError
from src.auth import auth_register_v2
from src.auth import user_profile_setemail_v1


def test_invalid_token():
    auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    token = '123123123123'
    assert user_profile_setemail_v1(token, 'asad@unsw.edu.au') == None

def test_invalid_email():
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    with pytest.raises(InputError):
        assert user_profile_setemail_v1(user['token'], '123123')

def test_exist_email():
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    with pytest.raises(InputError):
        assert user_profile_setemail_v1(user['token'], 'z5555555@ed.unsw.edu.au')

def test_valid_input():
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert user_profile_setemail_v1(user['token'], '987654321@unsw.edu.au') == 'str'

