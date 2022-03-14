import pytest
from src.error import InputError
from src.auth import auth_register_v2


def test_email_unvalid_1():
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567', '1234567', 'Donald', 'Trump')

def test_email_unvalid_2():
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def test_email_unvalid_3():
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed', '1234567', 'Donald', 'Trump')

def test_email_unvalid_4():
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.$%^com', '1234567', 'Donald', 'Trump')

def test_email_exist():
    auth_register_v2('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    with pytest.raises(InputError):
        assert auth_register_v2('z7654321@ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def test_register_password_too_short():
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '', 'Donald', 'Trump')

def test_register_password_too_short_2():
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '12345', 'Donald', 'Trump')

def test_register_firstname_too_short():
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '1234567', '', 'Trump')

def test_register_firstname_too_long():
    first_name_long = 'qweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqwe'
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '1234567', first_name_long, 'Trump')

def test_register_lastname_too_short():
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '1234567', 'Donald', '')

def test_register_lastname_too_long():
    last_name_long = 'qweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqwe'
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '1234567', 'Donald', last_name_long)

def test_valid_input():
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert user['auth_user_id'] == 1
    assert str(type(user['token'])) == "<class 'str'>"

