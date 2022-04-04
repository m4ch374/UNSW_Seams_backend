"""
This file contains all helper function for testing in iteration3
"""
# the below function format the endpoint requests input as json
def create_msg_pin_input_json(token, msg_id):
    return {
        'token': token,
        'message_id': msg_id,
    }

def create_msg_send_input_json(token, channel_id, message):
    return {
        'token': token,
        'channel_id': channel_id,
        'message': message,
    }

def create_chnl_join_input_json(token, channel_id):
    return {
        'token': token,
        'channel_id': channel_id,
    }

def create_chnl_get_msgs(token, channel_id, start):
    return {
        'token': token,
        'channel_id': channel_id,
        'start': start,
    }
