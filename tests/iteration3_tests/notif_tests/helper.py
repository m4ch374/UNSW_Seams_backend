"""
This file contains all helper function for testing notif func in iteration3
"""
# used for get requests with notifications/get/v1
def generate_get_notif_url(token):
    url = f'{ENDPOINT_DM_MESSAGE}?token={token}&dm_id={str(dm)}&start={start}'
    return url

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

