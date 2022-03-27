"""
This file contains all helper function for testing
"""

# Imports
from secrets import token_bytes
import requests

# Import definitions
from tests.iteration2_tests.endpoints import *

def generate_channel_input_json(tok, name, is_public):
    return {
        'token': tok,
        'name': name,
        'is_public': is_public,
    }

# Used for create
def generate_dm_input_json(tok, u_ids):
    return {
        'token': tok,
        'u_ids': u_ids,
    }

# Used for remove, details and leave
def generate_dm_json(tok, dm_id):
    return {
        'token': tok,
        'dm_id': dm_id
    }

def create_chnl_join_input_json(token, channel_id):
    return {
        'token': token,
        'channel_id': channel_id,
    }

def create_chnl_invite_input_json(token, channel_id, u_id):
    return {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id,
    }

def generate_chnl_func_json(token, channel_id, u_id):
    return {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id,
    }

def generate_get_dm_message_url(token, dm, start):
    url = f'{ENDPOINT_DM_MESSAGE}?token={token}&dm_id={str(dm)}&start={start}'
    return url


def generate_get_channel_message_url(token, channel, start):
    url = f'{ENDPOINT_CHANNEL_MESSAGE}?token={token}&channel_id={str(channel)}&start={start}'
    return url

def create_admin_remove_user_input_json(token, u_id):
    return {
        'token': token,
        'u_id': u_id,
    }

def create_admin_perm_change_input_json(token, u_id, permission_id):
    return {
        'token': token,
        'u_id': u_id,
        'permission_id': permission_id,
    }

# Used to create json for dm and channel send tests
def send_msg_json(token, channel_id, message):
    return {
        'token': token,
        'channel_id': channel_id,
        'message': message,
    }

<<<<<<< HEAD
def send_dm_msg_json(token, channel_id, message):
    return {
        'token': token,
        'dm_id': channel_id,
        'message': message,
    }


=======
def send_dm_json(token, dm_id, message):
    return {
        'token': token,
        'dm_id': dm_id,
        'message': message,
    }
>>>>>>> f4b54e6d7aca3aad2006625c93d0262b54264f16

def edit_msg_json(token, msg_id, message):
    return {
        'token': token,
        'message_id': msg_id,
        'message': message,
    }

# Used for msg_remove tests
def remove_msg_json(token, msg_id):
    return {
        'token': token,
        'message_id': msg_id,
    }

