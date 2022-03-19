"""
Fixtures for iteration 2
"""

# Imports
import pytest
import requests

# Import definitions
from tests.iteration2_tests.endpoints import ENDPOINT_REGISTER_USR, ENDPOINT_CLEAR, ENDPOINT_CREATE_CHNL

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

REGISTER_DETAILS_3 = {
    'email': 'yayayayayayayayaya@gmail.com',
    'password': 'grassgrass',
    'name_first': 'dogdogdog',
    'name_last': 'catcatcat',
}


# ==================================================

@pytest.fixture(autouse=True)
def clear():
    requests.delete(ENDPOINT_CLEAR)

@pytest.fixture
def get_token_1():
    resp = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_1).json()
    return resp['token']

@pytest.fixture
def get_token_2():
    resp = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_2).json()
    return resp['token']

@pytest.fixture
def get_usr_1():
    resp = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_1).json()
    return resp

@pytest.fixture
def get_usr_2():
    resp = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_2).json()
    return resp

@pytest.fixture
def get_u_id():
    resp = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_3).json()
    return {"id": resp['auth_user_id'], "token": resp['token']}

@pytest.fixture
def user_made_channel():
    user = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_1).json()
    channel = requests.post(ENDPOINT_CREATE_CHNL, json ={'token':user['token'],
                                                        'name':"chnl_name",
                                                        'is_public':True}).json()

    return {'channel': channel['channel_id'], 'token':user['token']}


