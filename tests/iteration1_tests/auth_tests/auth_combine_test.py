import pytest
from src.error import InputError
from src.auth import auth_login_v1
from src.auth import auth_register_v1


def test_combined_1():
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', '1234567')
    user_id = auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', 'Donald', 'Trump')
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', '123123123')
    assert auth_login_v1('z1234567@ed.unsw.edu.au', '1234567') == user_id
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    auth_register_v1('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    auth_register_v1('z8888888@ed.unsw.edu.au', '321321321', 'Russell', 'Wang')
    assert auth_register_v1('z9999999@ed.unsw.edu.au', '321321321', 'Russell', 'Wang') == {'auth_user_id': 5}

def test_combined_2():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'aaaaaaaaaa', 'aaaaaaaaaaa')
    auth_register_v1('z5555555@ed.unsw.edu.au', '123123123', 'aaaaaaaaaa', 'aaaaaaaaaaa')
    auth_register_v1('z8888888@ed.unsw.edu.au', '321321321', 'aaaaaaaaaa', 'aaaaaaaaaaa')
    assert auth_login_v1('z8888888@ed.unsw.edu.au', '321321321') == {'auth_user_id': 3}
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', 'xxxxxxx')
    assert auth_login_v1('z5555555@ed.unsw.edu.au', '123123123') == {'auth_user_id': 2}
    assert auth_login_v1('z7654321@ed.unsw.edu.au', '1234567') == {'auth_user_id': 1}

def test_combined_3():
    auth_register_v1('z7654321@ed.unsw.edu.au', '1234567', 'Jason', 'Smith')
    auth_register_v1('z5555555@ed.unsw.edu.au', '123123123', 'William', 'Wu')
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567unsw.edu.au', '12345', '', '')
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '12345', '', '')
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '123456', '', '')
    with pytest.raises(InputError):
        assert auth_register_v1('z1234567@ed.unsw.edu.au', '123456', 'Hanqi', '')
    user_id = auth_register_v1('z1234567@ed.unsw.edu.au', '123456', 'Ha@#$nq$i', '$%^Bai')
    with pytest.raises(InputError):
        assert auth_login_v1('zsssssss@ed.unsw.edu.au', 'xxxxxxx')
    with pytest.raises(InputError):
        assert auth_login_v1('z1234567@ed.unsw.edu.au', 'xxxxxxx')
    assert user_id == auth_login_v1('z1234567@ed.unsw.edu.au', '123456')

def test_register_handle_number():
    auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', '123$123', '456%456')
    assert auth_login_v1('z1234567@ed.unsw.edu.au', '1234567') == {'auth_user_id': 1}

def test_register_handle_mix():
    auth_register_v1('z1234567@ed.unsw.edu.au', '1234567', '123$qwe', '456%ASD')
    assert auth_login_v1('z1234567@ed.unsw.edu.au', '1234567') == {'auth_user_id': 1}
