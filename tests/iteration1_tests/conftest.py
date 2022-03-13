"""
Fixtures that (may or may not) shared across test files
"""

# Imports
import pytest
import src.auth as auth
import src.channels as chnls

# A dummy user id
@pytest.fixture
def auth_user_id():
    auth_id = auth.auth_register_v1(
        'z100@ed.unsw.edu.au', 
        '1234567', 
        'Donald', 
        'Trump'
    )
    return auth_id['auth_user_id']

# Returns another dummy user id
@pytest.fixture
def another_id():
    auth_id = auth.auth_register_v1(
        'z200@ed.unsw.edu.au', 
        '1234567', 
        'qqqqqqqqqq', 
        'qqqqqqqqqq'
    )
    return auth_id['auth_user_id']

# Registers user 1 and has them create channel 1
@pytest.fixture
def first_user_and_channel():
    first_user_id = auth.auth_register_v1('z5555555@ad.unsw.edu.au', '123456a', 'Anthony', 'Smith')['auth_user_id']
    first_channel_id = chnls.channels_create_v1(first_user_id, 'Ant', True)['channel_id']

    return {'first_user_id': first_user_id, 'first_channel_id': first_channel_id}
