from src.data_store import data_store
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    
    }

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
    
    store = data_store.get()
    is_auth_user_id_valid = False
    for user in store['users']:
        print(user.id)
        #if auth_user_id == user.id:
         #   is_auth_user_id_valid = True
        print("traversed a loop")
    if is_auth_user_id_valid == False:
        raise AccessError("auth user id passed is invalid!")
    
    
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }


