"""
Fixtures for iteration 3
"""

# Imports
import pytest
import requests

# Import definitions
from tests.iteration3_tests.endpoints import *

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
def get_usr_1():
    resp = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_1).json()
    return resp

@pytest.fixture
def get_usr_2():
    resp = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_2).json()
    return resp

@pytest.fixture
def user_1_made_channel():
    user = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_1).json()
    chnl = requests.post(ENDPOINT_CREATE_CHNL, json ={'token':user['token'],
                                                      'name':"chnl_name",
                                                      'is_public':True}).json()

    return {'channel': chnl['channel_id'], 'token':user['token']}

@pytest.fixture
def user_1_made_dm_with_global_owner():
    dm_member = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_2).json()
    dm_creator = requests.post(ENDPOINT_REGISTER_USR, json=REGISTER_DETAILS_1).json()

    dm = requests.post(ENDPOINT_DM_CREATE, json ={'token':dm_creator['token'],
                                                  'u_ids':[dm_member['auth_user_id'],]}).json()
    return {
        'dm': dm['dm_id'], 
        'creator_token':dm_creator['token'],
        'member_token':dm_member['token'],
        'creator_id':dm_creator['auth_user_id'],
        'member_id':dm_member['auth_user_id'],
    }

