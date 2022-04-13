import requests
from src.config import url

ENDPOINT_CLEAR = url + '/clear/v1'

"""
    discharge the change made by test in data_store
"""

def test_clear():
    requests.delete(ENDPOINT_CLEAR)
    pass



import json, os
from src.objecs import User, Channel, DmChannel, Message

"""
    Data persistence and functional functionality have been tested,
    this just for coverage,
    considering the server will not restart during pytest.
"""


def test_json():
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
    DATA_PATH = CURRENT_DIR + 'a.json'
    file_content = open(DATA_PATH, "r")
    JSON = json.load(file_content)

    JSON['users'] = [User.decode_json(item) for item in JSON['users']]

    id_to_usr = lambda x : next((usr for usr in JSON['users'] if usr.id == x), None)
    get_users = lambda li: [id_to_usr(u_id) for u_id in li]

    JSON['channel'] = [Channel.decode_json(item, get_users(item['owners']), get_users(item['members']))
        for item in JSON['channel']]

    JSON['dm'] = [DmChannel.decode_json(item, get_users(item['owners']), get_users(item['members']))
        for item in JSON['dm']]

    JSON['messages'] = [Message.decode_json(item) for item in JSON['messages']]
    # Notification.decode_json(JSON['Notification'])
    pass

