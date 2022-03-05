from src.data_store import data_store
from src.error import InputError, AccessError

import src.channels as channels

from src.objecs import Channel

'''
Function: channel_invite_v1
Invites a user with ID u_id to join a channel with ID channel_id. Once invited, 
the user is added to the channel immediately. In both public and private 
channels, all members are able to invite users.

Arguments:
    - auth_user_id (int) - The id of the person inviting the u_id
    - channel_id (int) - The channel to which the u_id is being invited
    - u_id (int) - The auth_user_id of the person being invited
Exceptions:
    - InputError - Occurs when channel_id does not refer to a valid channel
    - InputError - Occurs when the u_id is already a member of the channel
    - InputError - Occurs when u_id does not refer to a valid user
    - AccessError - Occurs when channel_id is valid and the authoried user is
                    not a member of the channel
Return Value:{}
'''
def channel_invite_v1(auth_user_id, channel_id, u_id):
    if is_auth_id_valid(auth_user_id) == False:
        raise AccessError("Auth user id passed is invalid!")
    if not channel_id_exist(channel_id):
        raise InputError("Channel id invalid")
    if not user_in_channel(auth_user_id, channel_id):
        raise AccessError("Auth user id is not a member of the channel")
    if is_auth_id_valid(u_id) == False:
        raise InputError("User id passed is invalid!")
    if user_in_channel(u_id, channel_id):
        raise InputError("User is already a member of the channel")
    # now that no errors have been detected, join the user to the channel
    chnl = data_store.get_channel(channel_id)
    chnl.add_member_id(u_id)
    return {}

'''
Function that determines if auth_user_id passed in is invalid

Arguments:
    - auth_user_id (int)
Exceptions:
    None
Return Value:
    - True if auth_user_id exists
    - False if auth_user_id does not exist
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
'''
Function that finds and returns a channel when given a channel_id
'''
def channel_id_exist(channel_id):
    channels = data_store.get()['channel']
    return any(channel_id == channel.id for channel in channels)

'''
Function that determines if a user is in the channel
Arguments:
    - auth_user_id (int)
    - channel_id (int)
Return Value:
    - True - if user is in channel
    - False - if user is not in channel
'''
def user_in_channel(auth_user_id, channel_id):
    channels = data_store.get()['channel']
    for channel in channels:
        if channel.id == channel_id:
            for users in channel.members:
                if auth_user_id == users.id:
                    return True
    return False

'''
Function that determines if a user is allowed to access the channel
Arguments:
    - auth_user_id (int)
    - channel_id (int)
Return Value:
    - True - if user is allowed
    - False - if user is not allowed
'''
def able_access(auth_user_id, channel_id):
    user = data_store.get_user(auth_user_id)
    channels = data_store.get_channel(channel_id)
    if not user.owner and not channels.is_public:
        return False
    return True

'''
Function : channel_join_v1
Given a channel_id of a channel that the authorised user can join, adds them
to that channel.

Arguments:
    - auth_user_id (int) 
    - channel_id (int)
Exceptions:
    - InputError - Occurs when channel_id does not refer to a valid channel
    - InputError - Occurs when the authorised user is already a member of the
                   channel
    - AccessError - Occurs when channel_id refers to a channel that is private
                    and the authorised user is not already a channel member
                    and is not a global owner
Return Value:{}
'''
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

