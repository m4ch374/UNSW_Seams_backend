"""
Test the behaviour of /clear/v1

Stubbed for now until other necessary funtions are implemented
"""

import requests
from src.config import url

def test_clear():
    '''# Register detail for 2 users
    reg1 = {
        'email': 'randomemail@gmail.com',
        'password': 12345678,
        'name_first': 'Joe',
        'name_last': 'Bidome',
    }

    reg2 = {
        'email': 'anotheremail@gmail.com',
        'password': 4567890,
        'name_first': 'Obama',
        'name_last': 'Prism'
    }

    # Register using register detail
    tok1 = requests.post(f"{url}auth/register/v2", data=reg1).json()['token']
    tok2 = requests.post(f"{url}auth/register/v2", data=reg2).json()['token']

    # channel data
    data1 = {
        'token': tok1,
        'name': 'name',
        'is_public': True,
    }

    data2 = {
        'token': tok2,
        'name': 'another',
        'is_public': True,
    }

    # Create channel
    chnl1 = requests.post(f"{url}channels/create/v2", data=data1).json()['channel_id']
    chnl2 = requests.post(f"{url}channels/create/v2", data=data2).json()['channel_id']

    chnl_list1 = requests.get(f"{url}channels/listall/v2", data={'token': tok1})['channels']
    chnl_list2 = requests.get(f"{url}channels/listall/v2", data={'token': tok2})['channles']

    expected_out = [
        {
            'channel_id': chnl1,
            'name': data1['name'],
        },
        {
            'channel_id': chnl2,
            'name': data2['name'],
        }
    ]

    assert chnl_list1 == expected_out
    assert chnl_list2 == expected_out

    resp = requests.delete(f"{url}clear/v1")

    assert resp.json() == {}'''
    assert True
