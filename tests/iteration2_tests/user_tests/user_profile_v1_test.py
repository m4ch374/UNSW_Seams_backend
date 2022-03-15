import pytest
from src.error import InputError
from src.auth import auth_register_v2
from src.auth import user_profile_v1
from src.other import clear_v1

def test_invalid_token():
    clear_v1()
    token = '123123123123'
    user = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert user_profile_v1(token, user['auth_user_id']) == None

def test_self_detail():
    clear_v1()
    user = auth_register_v2('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    assert user_profile_v1(user['token'], user['auth_user_id']) == {'id': 1, 'email': 'z8888888@ed.unsw.edu.au', 'name_first': 'Russell', 'name_last': 'Wang', 'handle': 'russellwang'}

def test_other_detail():
    clear_v1()
    user_1 = auth_register_v2('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    user_2 = auth_register_v2('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    assert user_profile_v1(user_1['token'], user_2['auth_user_id']) == {'id': 2, 'email': 'z5555555@ed.unsw.edu.au', 'name_first': 'William', 'name_last': 'Wu', 'handle': 'williamwu'}

def test_error_id():
    clear_v1()
    user_1 = auth_register_v2('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    with pytest.raises(InputError):
        assert user_profile_v1(user_1['token'], 99)

