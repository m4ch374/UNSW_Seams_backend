'''
##############################################################################
##                     Tests for message/pin/v1                              #
##############################################################################

# Expected error behaviour:
# InputError when:
#   - message_id is not a valid message within a channel or DM that the 
#     authorised user has joined
#   - the message is already pinned
# AccessError when:
#   - message_id refers to a valid message in a joined channel/DM and the 
#     authorised user does not have owner permissions in the channel/DM
# =============================================================================
'''
# imports used
import requests
from src.error import InputError, AccessError
from tests.iteration3_tests.endpoints import (
    ENDPOINT_MESSAGE_PIN,
)
from tests.iteration3_tests.message_tests.definitions import (
    INVALID_TOKEN, INVALID_MSG_ID,
)
from tests.iteration3_tests.helper import (
    create_msg_pin_input_json,
)

# raise AccessError since invalid token passed
#
# while invalid msg should raise input error, accesserror takes precedent
def test_message_pin_v1_invalid_token():
    json_input = create_msg_pin_input_json(INVALID_TOKEN, INVALID_MSG_ID)
    response = requests.post(ENDPOINT_MESSAGE_PIN, json = json_input)
    assert response.status_code == AccessError.code
'''
# raise input error since message id is not a valid message within a chnl user
# has joined
def test_message_pin_v1_invalid_msg_id(user_1_made_channel):
    user1_tok = user_1_made_channel['token']
    json_input = create_msg_pin_input_json(user1_tok, INVALID_MSG_ID)
    response = requests.post(ENDPOINT_MESSAGE_PIN, json = json_input)
    print(response)
'''


