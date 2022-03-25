import pytest
from src.error import InputError
from src.auth import auth_login_v1
from src.auth import auth_register_v1


def test_account_not_exist_1():
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', '1234567')

def test_account_not_exist_2():
    with pytest.raises(InputError):
        assert auth_login_v1('z123456au', '1234567')

def test_account_not_exist_3():
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', '')

def test_incorrect_password_1():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    with pytest.raises(InputError):
        assert auth_login_v1('z7654321@ed.unsw.edu.au', '1111111')

def test_incorrect_password_2():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    with pytest.raises(InputError):
        assert auth_login_v1('z7654321@ed.unsw.edu.au', '')

def test_incorrect_password_3():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    with pytest.raises(InputError):
        assert auth_login_v1('z7654321@ed.unsw.edu.au', 'ASDASDASDA')

def test_incorrect_password_4():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    with pytest.raises(InputError):
        assert auth_login_v1('z7654321@ed.unsw.edu.au', '@#$%$^&^*(')

def test_correct_input_1():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    assert auth_login_v1('z7654321@ed.unsw.edu.au', '1234567')['auth_user_id'] == 1

def test_correct_input_2():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    auth_register_v1('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    auth_register_v1('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    assert auth_login_v1('z8888888@ed.unsw.edu.au', '321321321')['auth_user_id'] == 3
