'''
File containing admin remove user and change permission functions
'''

# imports
from src.data_store import data_store
from src.error import InputError, AccessError

# helper functions
'''
function that returns true if the number of global owners >= 2
false is returned if there is no/only one global user
'''
def is_there_more_than_one_global_owner():
    users = data_store.get()['users']
    number_of_global_owners = 0
    for user in users:
        if user.owner:
            number_of_global_owners += 1
        if number_of_global_owners == 2:
            return True
    return False
'''
Function: admin_user_remove_v1
Given a user by their u_id, remove them from the Seams. This means they should 
be removed from all channels/DMs, and will not be included in the list of users
returned by users/all. Seams owners can remove other Seams owners (including 
the original first owner). Once users are removed, the contents of the messages
they sent will be replaced by 'Removed user'. Their profile must still be 
retrievable with user/profile, however name_first should be 'Removed' and 
name_last should be 'user'. The user's email and handle should be reusable.

Arguments:
    - token (string) - Encrypted user id and time
    - u_id (int) - The auth_user_id of the person being removed
Exceptions:
    - InputError - Occurs when the u_id does not refer to a valid user
    - InputError - Occurs when the u_id refers to a user who is the only global 
                   owner
    - AccessError - Occurs when the authorised user is not a global owner
Return Value:{}
'''
'''
CURRENTLY COMMENTED OUT AS NOT YET IMPLEMENTED OR CALLED :D
def admin_user_remove_v1():
'''

'''
Function: admin_userpermission_change_v1
Given a user by their user ID, set their permissions to new permissions 
described by permission_id.

Arguments:
    - auth_id (int) - id for a user
    - u_id (int) - The auth_user_id of the person being removed
    - permission_id (int) - The new permission level to be set to
Exceptions:
    - InputError - Occurs when u_id does not refer to a valid user
    - InputError - Occurs when u_id refers to a user who is the only global 
                   owner and they are being demoted to a user
    - InputError - Occurs when permission_id is invalid
    - InputError - Occurs when the user already has the permissions level of 
                   permission_id
    - AccessError - Occurs when the authorised user is not a global owner
Return Value:{}
'''
def admin_userpermission_change_v1(auth_user_id, u_id, permission_id):
    # checking for input and access errors
    if data_store.has_user_id(auth_user_id) == False:
        raise AccessError(description='Invalid auth user')
    if data_store.has_user_id(u_id) == False:
        raise InputError(description='Invalid user')
    # check that the auth user has global owner permissions
    auth_user = data_store.get_user(auth_user_id)
    if auth_user.owner == False:
        raise AccessError(description='Auth user is not global owner')
    user = data_store.get_user(u_id)
    if user.owner == permission_id:
        raise InputError(description='Permission already set to permission_id')
    if permission_id == 0:
        if not is_there_more_than_one_global_owner():
            raise InputError(description='Cannot demote only global owner')
    user.owner = permission_id
    return {}
