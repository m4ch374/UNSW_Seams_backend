"""
Fixtures for channels endpoint
"""

# Imports
import pytest
import src.auth as auth
from src.other import clear_v1

# Runs clean_v1() before all tests
@pytest.fixture(autouse=True)
def clean():
    clear_v1()

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
