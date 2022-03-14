from src.auth import auth_logout_v1
from src.auth import auth_register_v2
from src.auth import auth_login_v2


def test_register_logout():
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert auth_logout_v1(user['token']) == {}

def test_login_logout():
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    auth_logout_v1(user['token'])
    user = auth_login_v2('z5555555@ed.unsw.edu.au', '123123123')
    assert auth_login_v2(user['token']) == {}

