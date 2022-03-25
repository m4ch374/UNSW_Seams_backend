import pytest
from src.error import InputError
from src.auth import auth_register_v1


def test_email_unvalid_1():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567', '1234567', 'Donald', 'Trump')

def test_email_unvalid_2():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def test_email_unvalid_3():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed', '1234567', 'Donald', 'Trump')

def test_email_unvalid_4():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.$%^com', '1234567', 'Donald', 'Trump')

def test_email_unvalid_5():
    with pytest.raises(InputError):
        assert auth_register_v1('@ed.$%^com', '1234567', 'Donald', 'Trump')

def test_email_unvalid_6():
    with pytest.raises(InputError):
        assert auth_register_v1('@ed.com', '1234567', 'Donald', 'Trump')

def test_email_unvalid_7():
    with pytest.raises(InputError):
        assert auth_register_v1('', '1234567', 'Donald', 'Trump')

def test_email_unvalid_8():
    with pytest.raises(InputError):
        assert auth_register_v1('', '', '', '')

def test_email_exist_1():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    with pytest.raises(InputError):
        assert auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def test_email_exist_2():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    with pytest.raises(InputError):
        assert auth_register_v1('z7654321@ed.unsw.edu.au', '', '', '')

def test_password_too_short_1():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '', 'Donald', 'Trump')

def test_password_too_short_2():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1', 'Donald', 'Trump')

def testr_password_too_short_3():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '12345', 'Donald', 'Trump')

def test_password_too_short_4():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '@#$#', 'Donald', 'Trump')

def test_password_too_short_5():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '@#$#&', 'Donald', 'Trump')

def test_firstname_too_short():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', '', 'Trump')

def test_firstname_too_long():
    first_name_long = 'q' * 51
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', first_name_long, 'Trump')

def test_lastname_too_short():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'Donald', '')

def test_lastname_too_long():
    last_name_long = 'q' * 51
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'Donald', last_name_long)

def test_input_all_error_1():
    with pytest.raises(InputError):
        assert auth_register_v1('', '', '', '')

def test_input_all_error_2():
    with pytest.raises(InputError):
        assert auth_register_v1('123@.com', '', '', '')

def test_input_all_error_3():
    with pytest.raises(InputError):
        assert auth_register_v1('123@.com', '123', '', '')

def test_input_all_error_4():
    with pytest.raises(InputError):
        assert auth_register_v1('123@.com', '123123123', '', '')

def test_input_all_error_5():
    with pytest.raises(InputError):
        assert auth_register_v1('123@.com', '123123123', 'asdasd', '')

def test_input_all_error_6():
    first_name_long = 'q' * 51
    last_name_long = 'q' * 51
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567unsw.edu.au', '12345', first_name_long, last_name_long)

def test_correct_input_1():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    auth_register_v1('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    auth_register_v1('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    assert auth_register_v1('z100@ed.unsw.edu.au', '1234567', 'Donald', 'Trump')['auth_user_id'] == 4
    assert auth_register_v1('z200@ed.unsw.edu.au', '1234567', 'qqqqqqqqqq', 'qqqqqqqqqq')['auth_user_id'] == 5
    assert auth_register_v1('z300@ed.unsw.edu.au', '1234567', 'qqqqqqqqqq', 'qqqqqqqqqq')['auth_user_id'] == 6

def test_correct_input_2():
    assert auth_register_v1('z100@ed.unsw.edu.au', '1234567', '@#$@#%^', '&*)^&*^%&$')['auth_user_id'] == 1
