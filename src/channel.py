from src.data_store import data_store
from src.error import InputError, AccessError

import src.channels as channels

from src.objecs import Channel

'''
def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

Function that determines if auth_user_id passed in is invalid

Arguments:
   - auth_user_id (int) - id of the user being validated

Returns:
   - True if valid
   - False if invalid
'''

def is_auth_id_valid(auth_user_id):
    store = data_store.get()
    is_auth_user_id_valid = False
    for user in store['users']:
        if auth_user_id == user.id:
            is_auth_user_id_valid = True
    return is_auth_user_id_valid


'''
Function: channel_details_v1
Given a channel with ID channel_id that the authorised user is a member of, 
provide basic details about the channel.

Arguments:
   - auth_user_id - id of the user requesting channe details
   - channel_id - id of the channel whose details are being requested

 Exceptions:
   - InputError - Occurs when channel_id does not refer to valid channel
   - AccessError -> Occurs when the user id is invalid or when the ids are valid the 
                    user is not a member of the channel. Takes priority over InputError
 Returns:
   - name (string) when no errors raised
   - is_public (boolean) when no errors raised
   - owner_members (list of dictionaries) when no errors raised
   - all_members (list of dictionaires) when no errors raised
'''

def channel_details_v1(auth_user_id, channel_id):
    
    if data_store.has_user(auth_user_id) == False:
        raise AccessError
    if data_store.has_channel(channel_id) == False:
        raise InputError
    channel = data_store.get_channel(channel_id)
    
    if channel.has_member_id(auth_user_id) == False:
        raise AccessError

    return channel.channel_details_dict()

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
    if data_store.has_user(auth_user_id) == False:
        raise AccessError
    user = data_store.get_user(auth_user_id)
    
    if data_store.has_channel(channel_id) == False:
        raise InputError
    channel = data_store.get_channel(channel_id)
    
    if channel.has_member_id(auth_user_id) == False:
        raise AccessError
    if start > len(channel.messages) or start < 0:
        raise InputError
    
    

    # Splitting the stored messages list to paginate returned messages
    if start + 50 < len(channel.messages):
        end = start + 50
        messages = channel.messages[start:start+50]
    else: 
        end = -1
        messages = channel.messages[start:len(channel.messages)]

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }


def channel_id_exist(channel_id):
    channels = data_store.get()['channel']
    return any(channel_id == channel.id for channel in channels)

def user_in_channel(auth_user_id, channel_id):
    channels = data_store.get()['channel']
    for channel in channels:
        if channel.id == channel_id:
            for users in channel.members:
                if auth_user_id == users.id:
                    return True
    return False

def able_access(auth_user_id, channel_id):
    user = data_store.get_user(auth_user_id)
    channels = data_store.get_channel(channel_id)
    if not user.owner and not channels.is_public:
        return False
    return True

#
#
#
def channel_join_v1(auth_user_id, channel_id):
    if is_auth_id_valid(auth_user_id) == False:
        raise AccessError("Auth user id passed is invalid!")
    
    if not channel_id_exist(channel_id):
        raise InputError("Channel id invalid")
    if user_in_channel(auth_user_id, channel_id):
        raise InputError("User is already a member of the channel")
    if not able_access(auth_user_id, channel_id):
        raise AccessError("Channel is private")
    
    # now that no errors have been detected, join the user to the channel
    chnl = data_store.get_channel(channel_id)
    chnl.add_member_id(auth_user_id)
    
    return {}

