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

def generate_chnl_func_input_json(token, channel_id, u_id):
    return {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id,
    }

'''
def create_admin_remove_user_input_json(token, u_id):
    return {
        'token': token,
        'u_id': u_id,
    }
'''
def create_admin_perm_change_input_json(token, u_id, permission_id):
    return {
        'token': token,
        'u_id': u_id,
        'permission_id': permission_id,
    }
def send_msg_json(token, channel_id, message):
    return {
        'token': token,
        'channel_id': channel_id,
        'message': message,
    }
