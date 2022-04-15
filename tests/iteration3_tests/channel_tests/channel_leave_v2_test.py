'''
####################################################
##          Tests for channel_leave_v1            ##
####################################################
NOTE: the majority of the aspects of channel_lave were covered in iter2
This is only to cover the behviour when a user tries to leave the channel
depite being the owner of an active standup
'''
# imports used
import requests

# Import errors
from src.error import InputError

# Import definitions
from tests.iteration3_tests.endpoints import (
    ENDPOINT_STANDUP_START, ENDPOINT_CHNL_LEAVE, ENDPOINT_LIST_CHNL,
)
# helper functions for testing
def json_helper(token, channel_id, length):
    return{'token':token,
            'channel_id':channel_id,
            'length':length}
def create_chnl_join_input_json(token, channel_id):
    return {
        'token': token,
        'channel_id': channel_id,
    }
# raise InputError since the authorised user is the starter of an active
# standup in the channel
def test_channel_leave_owner_active_standup(user_1_made_channel):
    channel_id = user_1_made_channel['channel']
    token = user_1_made_channel['token']

    requests.post(ENDPOINT_STANDUP_START, json=json_helper(token, channel_id, 10))

    json_input = create_chnl_join_input_json(token, channel_id)
    response = requests.post(ENDPOINT_CHNL_LEAVE, json = json_input)

    # verify that token 2 has not left the channel
    channel_list = requests.get(ENDPOINT_LIST_CHNL,
                               {'token': token}).json()['channels']
    assert channel_list != []
    assert response.status_code == InputError.code
