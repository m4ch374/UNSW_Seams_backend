from src.auth import users_all_v1
from src.auth import auth_register_v2
from src.other import clear_v1

def test_invalid_token():
    clear_v1()
    token = '123123123123'
    assert users_all_v1(token) == None

def test_1_user():
    clear_v1()
    user = auth_register_v2('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    assert users_all_v1(user['token']) == [{'id': 1, 'email': 'z8888888@ed.unsw.edu.au', 'name_first': 'Russell', 'name_last': 'Wang',  'handle': 'russellwang'}]

def test_2_user():
    clear_v1()
    user = auth_register_v2('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert users_all_v1(user['token']) == [{'id': 1, 'email': 'z8888888@ed.unsw.edu.au', 'name_first': 'Russell', 'name_last': 'Wang', 'handle': 'russellwang'},
                                        {'id': 2, 'email': 'z5555555@ed.unsw.edu.au', 'name_first': 'William', 'name_last': 'Wu',  'handle': 'williamwu'}]

