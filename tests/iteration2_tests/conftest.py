"""
Fixtures for iteration 2
"""

# Imports
import pytest
import requests

# Import definitions
from tests.iteration2_tests.endpoints import ENDPOINT_REGISTER_USR, ENDPOINT_CLEAR

# =============== Local Definitions ================
REGISTER_DETAILS_1 = { 
    'email': 'randomemail@gmail.com',
    'password': 'thisisapassword', 
    'name_first': 'joe',
    'name_last': 'bidome',
}

REGISTER_DETAILS_2 = {
    'email': 'anotherrandomemail@gmail.com',
    'password': 'verysecurepassword',
    'name_first': 'Obama',
    'name_last': 'Prism',
}
# ==================================================

@pytest.fixture(autouse=True)
def clear():
    requests.delete(ENDPOINT_CLEAR)

@pytest.fixture
def get_token_1():
    resp = requests.post(ENDPOINT_REGISTER_USR, data=REGISTER_DETAILS_1).json()
    return resp['token']

@pytest.fixture
def get_token_2():
    resp = requests.post(ENDPOINT_REGISTER_USR, data=REGISTER_DETAILS_2).json()
    return resp['token']
