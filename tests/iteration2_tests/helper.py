"""
This file contains all helper function for testing
"""

def generate_channel_input_json(tok, name, is_public):
    return {
        'token': tok,
        'name': name,
        'is_public': is_public,
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
