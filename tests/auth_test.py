import pytest

from src.data_store import data_store
from src.error import InputError
from src.auth import auth_login_v1
from src.auth import auth_register_v1



# add some uaser to data_store here
# data_store = {
# 	'users': [
# 		('email', 'password', 'firstname', 'lastname', 'id', 'handle'),
# 		('email', 'password', 'firstname', 'lastname', 'id', 'handle'),
# 		........],
# }
# data_store['users'].append(['z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith', '1', 'jasonsmith'])
# data_store['users'].append(['z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu', '2', 'williamwu'])
# data_store['users'].append(['z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang', '3', 'russellwu'])

def login_account_not_exist():
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', '1234567')

def login_incorrect_password():
    store = data_store.get()
    new_user = {'email': 'z7654321@ed.unsw.edu.au', 'password' : '1234567', 'firstname' : 'Jason', 'lastname' : 'Smith', 'id' : 1, 'handle' : 'jasonsmith',}
    store['users'].append(new_user)
    with pytest.raises(InputError):
        assert auth_login_v1('z7654321@ed.unsw.edu.au', '1111111')

def login_correct_input_1():
    store = data_store.get()
    new_user = {'email': 'z7654321@ed.unsw.edu.au', 'password' : '1234567', 'firstname' : 'Jason', 'lastname' : 'Smith', 'id' : 1, 'handle' : 'jasonsmith',}
    store['users'].append(new_user)
    new_user = {'email': 'z5555555@ed.unsw.edu.au', 'password' : '123123123', 'firstname' : 'William', 'lastname' : 'Wu', 'id' : 2, 'handle' : 'williamwu',}
    store['users'].append(new_user)
    new_user = {'email': 'z8888888@ed.unsw.edu.au', 'password' : '321321321', 'firstname' : 'Russell', 'lastname' : 'Wang', 'id' : 3, 'handle' : 'russellwu',}
    store['users'].append(new_user)
    assert auth_login_v1('z7654321@ed.unsw.edu.au', '1234567') == {1}

def login_correct_input_3():
    store = data_store.get()
    new_user = {'email': 'z7654321@ed.unsw.edu.au', 'password' : '1234567', 'firstname' : 'Jason', 'lastname' : 'Smith', 'id' : 1, 'handle' : 'jasonsmith',}
    store['users'].append(new_user)
    new_user = {'email': 'z5555555@ed.unsw.edu.au', 'password' : '123123123', 'firstname' : 'William', 'lastname' : 'Wu', 'id' : 2, 'handle' : 'williamwu',}
    store['users'].append(new_user)
    new_user = {'email': 'z8888888@ed.unsw.edu.au', 'password' : '321321321', 'firstname' : 'Russell', 'lastname' : 'Wang', 'id' : 3, 'handle' : 'russellwu',}
    store['users'].append(new_user)
    assert auth_login_v1('z8888888@ed.unsw.edu.au', '321321321') == {3}

def register_email_unvalid_1():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567', '1234567', 'Donald', 'Trump')

def register_email_unvalid_2():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def register_email_unvalid_3():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed', '1234567', 'Donald', 'Trump')

def register_email_exist():
    store = data_store.get()
    new_user = {'email': 'z7654321@ed.unsw.edu.au', 'password' : '1234567', 'firstname' : 'Jason', 'lastname' : 'Smith', 'id' : 1, 'handle' : 'jasonsmith',}
    store['users'].append(new_user)
    new_user = {'email': 'z5555555@ed.unsw.edu.au', 'password' : '123123123', 'firstname' : 'William', 'lastname' : 'Wu', 'id' : 2, 'handle' : 'williamwu',}
    store['users'].append(new_user)
    new_user = {'email': 'z8888888@ed.unsw.edu.au', 'password' : '321321321', 'firstname' : 'Russell', 'lastname' : 'Wang', 'id' : 3, 'handle' : 'russellwu',}
    store['users'].append(new_user)
    with pytest.raises(InputError):
        assert auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Donald', 'Trump')

def register_password_too_short_1():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1', 'Donald', 'Trump')

def register_firstname_too_short():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', '', 'Trump')

def register_firstname_too_long():
    first_name_long = 'qweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqwe'
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', first_name_long, 'Trump')

def register_firstname_too_short():
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'Donald', '')

def register_firstname_too_long():
    last_name_long = 'qweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqweqwe'
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'Donald', last_name_long)

def register_correct_input_1():
    assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'Donald', 'Trump') == {4}

def register_correct_input_2():
    assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'qqqqqqqqqq', 'qqqqqqqqqq') == {5}

def register_correct_input_2():
    assert auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'qqqqqqqqqq', 'qqqqqqqqqq') == {6}
