from src.auth import users_all_v1
from src.auth import auth_register_v2

def test_invalid_token():
    token = '123123123123'
    assert users_all_v1(token) == None

def test_1_user():
    auth_register_v2('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    assert users_all_v1() == {'user 1': {'email': 'z8888888@ed.unsw.edu.au', 'password': '321321321', 'name_first': 'Russell', 'name_last': 'Wang', 'id': 1, 'handle': 'russellwang', 'channels': [], 'owner': False}}

def test_2_user():
    user = auth_register_v2('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert users_all_v1(user['token']) == {'user 1': {'email': 'z8888888@ed.unsw.edu.au', 'password': '321321321', 'name_first': 'Russell', 'name_last': 'Wang', 'id': 1, 'handle': 'russellwang', 'channels': [], 'owner': False},
                            'user 2': {'email': 'z5555555@ed.unsw.edu.au', 'password': '123123123', 'name_first': 'William', 'name_last': 'Wu', 'id': 2, 'handle': 'williamwu', 'channels': [], 'owner': False}}

