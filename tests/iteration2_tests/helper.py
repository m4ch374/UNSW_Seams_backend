"""
This file contains all helper function for testing
"""

def generate_channel_input_json(tok, name, is_public):
    return {
        'token': tok,
        'name': name,
        'is_public': is_public,
    }
