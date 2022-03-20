from src.data_store import data_store
from src.error import InputError, AccessError


'''
Function: channel_messages_v1
Given a channel with ID channel_id that the authorised user is a member of, 
returns up to 50 messages starting from given start position.

Arguments:
   - auth_user_id - id of the user requesting messages
   - channel_id - id of the channel messages are being requested from
   - start - the id of first message that is required
 Exceptions:
   - InputError - Occurs when channel_id does not refer to valid channel or start does not 
                  refer to a valid message id
   - AccessError -> Occurs when the user id is invalid or when the ids are valid the 
                    user is not a member of the channel. Takes priority over InputError
 Returns:
   - messages (list of dictionaries) when no errors raised
   - start (integer) when no errors raised
   - end (integer) when no errors raised
'''

def channel_messages_v1(auth_user_id, channel_id, start):
    
    # Checking valid channel id, start id and user access
    if data_store.has_user_id(auth_user_id) == False:
        raise AccessError
    if data_store.has_channel_id(channel_id) == False:
        raise InputError
    channel = data_store.get_channel(channel_id)
    if channel.has_member_id(auth_user_id) == False:
        raise AccessError
    chnl_messages = channel.get_messages()
    if start > len(chnl_messages) or start < 0:
        raise InputError
    

    # Splitting the stored messages list to paginate returned messages
    if start + 50 < len(chnl_messages):
        end = start + 50
        messages = channel.get_messages()[start:start+50]
    else:
        end = -1
        messages = chnl_messages[start:len(chnl_messages)]

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

def dm_messages_v1(user_id, dm_id, start):
    return {}

def message_send_v1(user_id, channel_id, message):
    return {}

def message_senddm_v1(user_id, dml_id, message):
    return {}

def message_edit_v1(user_id, msg_id, message):
    return {}

def message_remove_v1(user_id, msg_id):
    return {}