import pytest
from src.error import InputError
from src.auth import auth_register_v2
from src.auth import auth_login_v2

def test_account_not_exist():
    with pytest.raises(InputError):
        assert auth_login_v2('z1234567@ed.unsw.edu.au', '1234567')

def test_incorrect_password():
    auth_register_v2('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    with pytest.raises(InputError):
        assert auth_login_v2('z7654321@ed.unsw.edu.au', '1111111')

def test_correct_input():
    auth_register_v2('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    user = auth_login_v2('z7654321@ed.unsw.edu.au', '1234567')
    assert user['auth_user_id'] == 1
    assert str(type(user['token'])) == "<class 'str'>"

