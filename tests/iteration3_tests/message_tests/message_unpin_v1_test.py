'''
##############################################################################
##                     Tests for message/unpin/v1                            #
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
    
)
from tests.iteration3_tests.message_tests.definitions import (
    INVALID_TOKEN, INVALID_MSG_ID, INVALID_U_ID,
)
from tests.iteration3_tests.helper import (
    
)












