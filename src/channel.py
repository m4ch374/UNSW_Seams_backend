from src.data_store import data_store
from src.error import InputError, AccessError

import src.channels as channels

from src.objecs import Channel


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }
# Function that determines if auth_user_id passed in is invalid
#
# Arguments:
#   - auth_user_id (int)
#
# Returns:
#   - True if valid
#   - False if invalid
def is_auth_id_valid(auth_user_id):
    store = data_store.get()
    is_auth_user_id_valid = False
    for user in store['users']:
        if auth_user_id == user.id:
            is_auth_user_id_valid = True
    return is_auth_user_id_valid

# Arguments:
#   - auth_user_id (int)
#   - channel_id (int)
#
# Exceptions:
#   - InputError -> raised when channel_id does not refer to a valid channel
#   - AccessError -> raised when channel_id is valid and the authorised user is 
#                    not a member of the channel
#
# Returns:
#   - name (string)
#   - is_public (boolean)
#   - owner_members (list of dictionaries)
#   - all_members (list of dictionaires)

def channel_details_v1(auth_user_id, channel_id):
    
    if data_store.has_user(auth_user_id) == False:
        raise AccessError
    if data_store.has_channel(channel_id) == False:
        raise InputError
    channel = data_store.get_channel(channel_id)
    
    if channel.has_member(auth_user_id) == False:
        raise AccessError

    return channel.channel_details_dict()


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

