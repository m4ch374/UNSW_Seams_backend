"""
This file contains all helper function for testing
"""

# Imports
import requests

# Import definitions
from tests.iteration2_tests.endpoints import *

def generate_channel_input_json(tok, name, is_public):
    return {
        'token': tok,
        'name': name,
        'is_public': is_public,
    }

def generate_dm_input_json(tok, u_ids):
    return {
        'token': tok,
        'u_ids': u_ids,
    }
