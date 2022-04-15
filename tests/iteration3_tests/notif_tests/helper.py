"""
This file contains all helper function for testing notif func in iteration3
"""
from tests.iteration3_tests.endpoints import ENDPOINT_MESSAGE_SEND
import requests
# used to get json input for channel invite function
def create_chnl_invite_input_json(token, channel_id, u_id):
    return {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id,
    }

def generate_dm_json(tok, dm_id):
    return {
        'token': tok,
        'dm_id': dm_id
    }

def send_dm_json(token, dm_id, message):
    return {
        'token': token,
        'dm_id': dm_id,
        'message': message,
    }

def generate_dm_input_json(tok, u_ids):
    return {
        'token': tok,
        'u_ids': u_ids,
    }

def create_chnl_join_input_json(token, channel_id):
    return {
        'token': token,
        'channel_id': channel_id,
    }

def edit_msg_json(token, msg_id, message):
    return {
        'token': token,
        'message_id': msg_id,
        'message': message,
    }


# helper function that repeatedly sends messages from a given list tagging 
# a given handle
def send_repeated_messages(message_list, handle_to_tag, sender_tok, chnl_id):
    for message in message_list:
        data = {
        'token': sender_tok,
        'channel_id': chnl_id,
        'message': f"@{handle_to_tag} {message}",
        }
        requests.post(ENDPOINT_MESSAGE_SEND, json=data).json()['message_id']
