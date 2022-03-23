'''
####################################################
##          Tests for message/senddm/v1           ##
####################################################

# Expected behaviour:
# InputError when:
#   - dm_id does not refer to a valid dm
# AccessError when:
#   - dm_id is valid and the authorised user is not a member of the
#     dm
#   - user token is invalid
# ==================================================
'''
# Imports
from ast import In
import requests

# Import errors
from src.error import InputError, AccessError

# Import definitions
from tests.iteration2_tests.endpoints import ENDPOINT_MESSAGE_EDIT
from tests.iteration2_tests.helper import send_msg_json


# owner permission can edit whenever
# non-owner permission can only edit their msg
'''
def test_invalid_user_token():

def test_message_edit_message_too_long():

def test_message_edit_message_id_nonexist():

def test_message_edit_invalid_message_id_():
    #case where message exists in a different channel than what the user has access to (inputerror)

def test_message_edit_invalid_message_access():
    #case where user didn't send the message and user is not a channel owner

def test_message_edit_simple_user_is_owner():

def test_message_edit_simple_user_is_sender():

def test_mesage_edit_delete():
    '''