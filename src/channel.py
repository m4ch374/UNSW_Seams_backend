from src.data_store import data_store
from src.error import InputError, AccessError

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
    chnl = data_store.get_channel(channel_id)
    return chnl.has_member_id(auth_user_id)

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
    '''
    note: commented out section since this error handled by token system
    if data_store.has_user_id(auth_user_id) == False:
        raise AccessError(description="Auth user id passed is invalid!")
    '''
    if not data_store.has_channel_id(channel_id):
        raise InputError("Channel id invalid")
    if not user_in_channel(auth_user_id, channel_id):
        raise AccessError("Auth user id is not a member of the channel")
    if data_store.has_user_id(u_id) == False:
        raise InputError("User id passed is invalid!")
    if user_in_channel(u_id, channel_id):
        raise InputError("User is already a member of the channel")
    # now that no errors have been detected, join the user to the channel
    chnl = data_store.get_channel(channel_id)
    chnl.add_member_id(u_id)
    return {}


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
    '''
    Commented out to improve coverage since token system handles this error
    if not data_store.has_user_id(auth_user_id):
        raise AccessError("Account does not exist valid")
    '''
    if not data_store.has_channel_id(channel_id):
        raise InputError("Channel does not exist")
    channel = data_store.get_channel(channel_id)
    
    if not channel.has_member_id(auth_user_id):
        raise AccessError("User not in channel")

    return channel.channel_details_dict()
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
    '''
    note: commented out section since this error handled by token 
    if data_store.has_user_id(auth_user_id) == False:
        raise AccessError(description="Auth user id passed is invalid!")
    '''
    if not data_store.has_channel_id(channel_id):
        raise InputError(description="Channel does not exist valid")
    if user_in_channel(auth_user_id, channel_id):
        raise InputError(description="User is already a member of the channel")
    if not able_access(auth_user_id, channel_id):
        raise AccessError(description="Channel is private")
    
    # now that no errors have been detected, join the user to the channel
    chnl = data_store.get_channel(channel_id)
    chnl.add_member_id(auth_user_id)
    
    return {}

'''
Function : channel_leave_v1
Given a channel with ID channel_id that the authorised user is a member of, 
remove them as a member of the channel. Their messages should remain in the 
channel. If the only channel owner leaves, the channel will remain.

Arguments:
    - auth_user_id (int) 
    - channel_id (int)
Exceptions:
    - InputError - Occurs when channel_id does not refer to a valid channel
    - AccessError - Occurs when channel_id is valid and the authorised user is 
                    not a member of the channel
Return Value:{}
'''
def channel_leave_v1(auth_user_id, channel_id):
    if not data_store.has_channel_id(channel_id):
        raise InputError(description="Channel does not exist")
    if not user_in_channel(auth_user_id, channel_id):
        raise AccessError(description="User is not a member of the channel")
    
    chnl = data_store.get_channel(channel_id)
    user = data_store.get_user(auth_user_id)
    chnl.remove_member(user)
    # remove them if they are an owner
    if user in chnl.owners:
        chnl.owners.remove(user)
        data_store.set_store()

    return {}
'''
Function : channel_addowner_v1
Make user with user id u_id an owner of the channel.

Arguments:
    - auth_user_id (int) 
    - channel_id (int)
    - u_id (int)
Exceptions:
    - InputError - Occurs when channel_id does not refer to a valid channel
    - InputError - Occurs when u_id does not refer to a valid user
    - InputError - Occurs when u_id refers to a user who is not a member of the 
                   channel
    - InputError - Occurs when u_id refers to a user who is already an owner of 
                   the channel
    - AccessError - channel_id is valid and the authorised user does not have 
                    owner permissions in the channel
Return Value:{}
'''
def channel_addowner_v1(auth_user_id, channel_id, u_id):
    if not data_store.has_channel_id(channel_id):
        raise InputError(description="Channel does not exist")
    
    chnl = data_store.get_channel(channel_id)
    auth_user = data_store.get_user(auth_user_id)
    # check that the auth user has owner permissions (either as a global owner
    # or channel owner)
    if auth_user not in chnl.owners and auth_user.owner == False:
        raise AccessError(description='Auth user is not a channel owner')
    
    if data_store.has_user_id(u_id) == False:
        raise InputError("User id passed is invalid!")
    if not user_in_channel(u_id, channel_id):
        raise InputError("User passed is not a member of the channel")
    
    
    # check that the user is not already an owner
    user = data_store.get_user(u_id)
    if user in chnl.owners:
        raise InputError(description='User is already a channel owner')
    
    chnl.owners.append(user)
    data_store.set_store()
    return {}
'''
Function : channel_removeowner_v1
Remove user with user id u_id as an owner of the channel.

Arguments:
    - auth_user_id (int) 
    - channel_id (int)
    - u_id (int)
Exceptions:
    - InputError - Occurs when channel_id does not refer to a valid channel
    - InputError - Occurs when u_id does not refer to a valid user
    - InputError - Occurs when u_id refers to a user who is not a member of the 
                   channel
    - InputError - Occurs when u_id refers to a user who is currently the only 
                   owner of the channel
    - AccessError - Occurs when channel_id is valid and the authorised user does
                    not have owner permissions in the channel
Return Value:{}
'''
def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    if not data_store.has_channel_id(channel_id):
        raise InputError(description="Channel does not exist")
    if data_store.has_user_id(u_id) == False:
        raise InputError("User id passed is invalid!")
    chnl = data_store.get_channel(channel_id)
    auth_user = data_store.get_user(auth_user_id)
    # check the auth user has owner permissions (either chnl or global owner)
    if auth_user not in chnl.owners:
        if auth_user not in chnl.members or auth_user.owner == False:
            raise AccessError(description='Auth user is not a channel owner')
    # check that the user is already an owner
    user = data_store.get_user(u_id)
    if user not in chnl.owners:
        raise InputError(description='User is not a channel owner')
    # check that the user is not the only channel owner
    if len(chnl.owners) == 1:
        raise InputError(description='User is currently the only channel owner')
    
    chnl.owners.remove(user)
    data_store.set_store()
    return {}

