import pytest
from src.error import InputError
from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.other import clear_v1

from src.data_store import data_store

store = data_store.get()
new_user = {'email': 'z7654321@ed.unsw.edu.au', 'password' : '1234567', 'firstname' : 'Jason', 'lastname' : 'Smith', 'id' : 1, 'handle' : 'jasonsmith',}
store['users'].append(new_user)
new_user = {'email': 'z5555555@ed.unsw.edu.au', 'password' : '123123123', 'firstname' : 'William', 'lastname' : 'Wu', 'id' : 2, 'handle' : 'williamwu',}
store['users'].append(new_user)
new_user = {'email': 'z8888888@ed.unsw.edu.au', 'password' : '321321321', 'firstname' : 'Russell', 'lastname' : 'Wang', 'id' : 3, 'handle' : 'russellwu',}
store['users'].append(new_user)


def test_login_account_not_exist():
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', '1234567')

def test_login_incorrect_password():
    with pytest.raises(InputError):
        assert auth_login_v1('z7654321@ed.unsw.edu.au', '1111111')

def test_login_correct_input_1():
    assert auth_login_v1('z7654321@ed.unsw.edu.au', '1234567') == {1}

def test_login_correct_input_3():
    assert auth_login_v1('z8888888@ed.unsw.edu.au', '321321321') == {3}

def test_register_email_unvalid_1():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567', '1234567', 'Donald', 'Trump')

def test_register_email_unvalid_2():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def test_register_email_unvalid_3():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed', '1234567', 'Donald', 'Trump')

def test_register_email_unvalid_4():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.$%^com', '1234567', 'Donald', 'Trump')

def test_register_email_exist():
    with pytest.raises(InputError):
        assert auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def test_register_password_too_short_1():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1', 'Donald', 'Trump')

def test_register_firstname_too_short():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', '', 'Trump')

def test_register_firstname_too_long():
    first_name_long = 'qweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqwe'
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', first_name_long, 'Trump')

def test_register_firstname_too_short():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'Donald', '')

def test_register_firstname_too_long():
    last_name_long = 'qweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqwe'
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'Donald', last_name_long)

def test_register_correct_input():
    assert auth_register_v1('z100@ed.unsw.edu.au', '1234567', 'Donald', 'Trump') == {4}
    assert auth_register_v1('z200@ed.unsw.edu.au', '1234567', 'qqqqqqqqqq', 'qqqqqqqqqq') == {5}
    assert auth_register_v1('z300@ed.unsw.edu.au', '1234567', 'qqqqqqqqqq', 'qqqqqqqqqq') == {6}

def test_combined_test():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', '1234567')
    user_id = auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'Donald', 'Trump')
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', '123123123')
    assert auth_login_v1('z1234567@ed.unsw.edu.au', '1234567') == user_id
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    auth_register_v1('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    auth_register_v1('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    assert auth_register_v1('z9999999@ed.unsw.edu.au', '321321321', 'Russell', 'Wang') == {5}
    store = data_store.get()
    assert store['users'] == [{'email': 'z1234567@ed.unsw.edu.au', 'password' : '1234567', 'firstname' : 'Donald', 'lastname' : 'Trump', 'id' : 1, 'handle' : 'donaldtrump'},
    {'email': 'z7654321@ed.unsw.edu.au', 'password' : '1234567', 'firstname' : 'Jason', 'lastname' : 'Smith', 'id' : 2, 'handle' : 'jasonsmith'}, 
    {'email': 'z5555555@ed.unsw.edu.au', 'password' : '123123123', 'firstname' : 'William', 'lastname' : 'Wu', 'id' : 3, 'handle' : 'williamwu'}, 
    {'email': 'z8888888@ed.unsw.edu.au', 'password' : '321321321', 'firstname' : 'Russell', 'lastname' : 'Wang', 'id' : 4, 'handle' : 'russellwang'}, 
    {'email': 'z9999999@ed.unsw.edu.au', 'password' : '321321321', 'firstname' : 'Russell', 'lastname' : 'Wang', 'id' : 5, 'handle' : 'russellwang0'}]