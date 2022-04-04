"""
This file contains all helper function for testing in iteration3
"""

# create json input message pin and unpin tests
def create_msg_pin_input_json(token, msg_id):
    return {
        'token': token,
        'message_id': msg_id,
    }
