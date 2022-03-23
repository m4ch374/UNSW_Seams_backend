from datetime import timezone
import datetime as dt
from src.data_store import data_store
from src.objecs import Message, Channel, DmChannel
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
#TODO: Helper functions to reduce repetition

def channel_messages_v1(auth_user_id, channel_id, start):
    
    # Checking valid channel id, start id and user access
    if data_store.has_channel_id(channel_id) == False:
        raise InputError(description='Invalid channel')
    channel = data_store.get_channel(channel_id)
    if channel.has_member_id(auth_user_id) == False:
        raise AccessError('Invalid access to channel')
    chnl_messages = channel.get_messages()
    if start > len(chnl_messages) or start < 0:
        raise InputError('Invalid message start index')
    

    # Splitting the stored messages list to paginate returned messages
    if start + 50 < len(chnl_messages):
        end = start + 50
        messages = channel.get_messages()[start:start+50]
    else:
        end = -1
        messages = channel.get_messages()[start:len(chnl_messages)+1]

    # convert list of msgs to list of dictionaries containing msg info
    msg_list = []
    for message in messages:
        msg_list.append({'message_id': message.id,
                        'user_id': message.u_id,
                        'message': message.message,
                        'time_sent': message.time_sent,
                        })

    return {
        'messages': msg_list,
        'start': start,
        'end': end,
    }

def dm_messages_v1(user_id, dm_id, start):

    # Checking valid channel id, start id and user access
    if data_store.has_dm_id(dm_id) == False:
        raise InputError(description='Invalid channel')
    dm = data_store.get_dm(dm_id)
    if dm.has_member_id(user_id) == False:
        raise AccessError(description='Invalid access to channel')
    chnl_messages = dm.get_messages()
    if start > len(chnl_messages) or start < 0:
        raise InputError(description='Invalid message start index')
    

    # Splitting the stored messages list to paginate returned messages
    if start + 50 < len(chnl_messages):
        end = start + 50
        messages = dm.get_messages()[start:start+50]
    else:
        end = -1
        messages = chnl_messages[start:len(chnl_messages)]

     # convert list of msgs to list of dictionaries containing msg info
    msg_list = []
    for message in messages:
        msg_list.append({'message_id': message.id,
                        'user_id': message.u_id,
                        'message': message.message,
                        'time_sent': message.time_sent,
                        })
    return {
        'messages': msg_list,
        'start': start,
        'end': end,
    }

def message_send_v1(user_id, channel_id, message):
    
    # Checking valid ids, access, and message length
    if data_store.has_channel_id(channel_id) == False:
        raise InputError(description='Invalid channel')
    channel = data_store.get_channel(channel_id)
    if channel.has_member_id(user_id) == False:
        raise AccessError(description='Invalid access to channel')
    if message is None or len(message) == 0 or len(message) > 1000:
        raise InputError(description='Message must be between 1 and 1000 character inclusive')

    new_message = Message(
        u_id=user_id,
        message=message,
        chnl_id=channel_id,
        time_sent=((dt.datetime.now(timezone.utc)).replace(tzinfo=timezone.utc)).timestamp()
    )

    # Append new message to data_store
    data = data_store.get()
    data['messages'].append(new_message)
    data_store.set(data)

    return {'message_id': new_message.id}

def message_senddm_v1(user_id, dm_id, message):

    # Checking valid ids, access, and message length
    if data_store.has_dm_id(dm_id) == False:
        raise InputError(description='Invalid channel')
    dm = data_store.get_dm(dm_id)
    if dm.has_member_id(user_id) == False:
        raise AccessError(description='Invalid access to channel')
    if message is None or len(message) == 0 or len(message) > 1000:
        raise InputError(description='Message must be between 1 and 1000 character inclusive')

    new_message = Message(
        u_id=user_id,
        message=message,
        chnl_id=dm_id,
        time_sent=((dt.datetime.now(timezone.utc)).replace(tzinfo=timezone.utc)).timestamp()
    )

    # Append new message to data_store
    data = data_store.get()
    data['messages'].append(new_message)
    data_store.set(data)

    return {'message_id': new_message.id}


def message_edit_v1(user_id, msg_id, message):

    if data_store.has_dm_id(dm_id) == False:
        raise InputError(description='Invalid channel')


def message_remove_v1(user_id, msg_id):
    return {}