"""
Fixtures for /channels domain
"""

# Imports
import pytest
import requests

# Import definitions
from src.config import url

REGISTER_URL = f"{url}auth/register/v2"

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

@pytest.fixture
def get_token_1():
    resp = requests.post(REGISTER_URL, data=REGISTER_DETAILS_1).json()
    return resp['token']

@pytest.fixture
def get_token_2():
    resp = requests.post(REGISTER_URL, data=REGISTER_DETAILS_2).json()
    return resp['token']
