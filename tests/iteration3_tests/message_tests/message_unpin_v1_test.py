'''
##############################################################################
##                     Tests for message/unpin/v1                            #
##############################################################################

# Expected error behaviour:
# InputError when:
#   - message_id is not a valid message within a channel or DM that the 
#     authorised user has joined
#   - the message is not already pinned
# AccessError when:
#   - message_id refers to a valid message in a joined channel/DM and the 
#     authorised user does not have owner permissions in the channel/DM
# =============================================================================
'''
# imports used
import requests
from src.error import InputError, AccessError
from tests.iteration3_tests.endpoints import (
    ENDPOINT_MESSAGE_PIN, ENDPOINT_MESSAGE_UNPIN
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
'''
def test_message_unpin_v1_invalid_token():
    json_input = create_msg_pin_input_json(INVALID_TOKEN, INVALID_MSG_ID)
    reponse = requests.post(ENDPOINT_MESSAGE_PIN, json = json_input)
    assert response.status_code == AccessError.code
'''
