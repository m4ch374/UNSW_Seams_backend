from src.auth import auth_logout_v1
from src.auth import auth_register_v2
from src.auth import auth_login_v2
from src.other import clear_v1

def test_register_logout():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert auth_logout_v1(user['token']) == {}

def test_login_logout():
    clear_v1()
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    auth_logout_v1(user['token'])
    user = auth_login_v2('z5555555@ed.unsw.edu.au', '123123123')
    assert auth_logout_v1(user['token']) == {}

