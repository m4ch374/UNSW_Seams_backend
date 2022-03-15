import pytest
from src.error import InputError
from src.auth import auth_register_v2
from src.other import clear_v1

def test_email_unvalid_1():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567', '1234567', 'Donald', 'Trump')

def test_email_unvalid_2():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def test_email_unvalid_3():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed', '1234567', 'Donald', 'Trump')

def test_email_unvalid_4():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.$%^com', '1234567', 'Donald', 'Trump')

def test_email_exist():
    clear_v1()
    auth_register_v2('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    with pytest.raises(InputError):
        assert auth_register_v2('z7654321@ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def test_register_password_too_short():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '', 'Donald', 'Trump')

def test_register_password_too_short_2():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '12345', 'Donald', 'Trump')

def test_register_firstname_too_short():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '1234567', '', 'Trump')

def test_register_firstname_too_long():
    clear_v1()
    first_name_long = 'q' * 51
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '1234567', first_name_long, 'Trump')

def test_register_lastname_too_short():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '1234567', 'Donald', '')

def test_register_lastname_too_long():
    clear_v1()
    last_name_long = 'q' * 51
    with pytest.raises(InputError):
        assert auth_register_v2('z1234567@ed.unsw.edu.au', '1234567', 'Donald', last_name_long)

def test_valid_input():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert user['auth_user_id'] == 1
    assert str(type(user['token'])) == "<class 'str'>"

