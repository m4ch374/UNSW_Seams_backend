from src.data_store import data_store
from src.error import InputError, AccessError
<<<<<<< HEAD
from src.objecs import Channel
=======
import src.channels as channels
import src.objecs as obj 
>>>>>>> james_channel_branch

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    
    }

<<<<<<< HEAD

=======
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
>>>>>>> james_channel_branch
def channel_details_v1(auth_user_id, channel_id):
    
    # testing if the auth_user_id passed is valid (AccessError if invalid)
    store = data_store.get()
    is_auth_user_id_valid = False
    for user in store['users']:
        if auth_user_id == user.id:
            is_auth_user_id_valid = True
    if is_auth_user_id_valid == False:
        raise AccessError("auth user id passed is invalid!")
        
        
    channels_dict = channels.channels_listall_v1(auth_user_id)
    channels_list = channels_dict['channels']
    
    # FOR DEBUGGING ONLY
    print(f"channels dict is {channels_dict}")
    print(channels_dict['channels'])
    print(f"channels_list[0] is :{channels_list[0]}")
    print(f"channels_list[0]['channel_id'] is :{channels_list[0]['channel_id']}")
    
    is_channel_id_valid = False
    for idx, channel in enumerate(channels_list):
        print(channel['channel_id'])
        if channel['channel_id'] == channel_id:
            is_channel_id_valid = True
            
    if is_channel_id_valid != False:
        raise InputError("channel id passed is invalid!")
    
    
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
    

print(data_store.get_channel(0))
def channel_messages_v1(auth_user_id, channel_id, start):
    
    channel = data_store.get_channel(channel_id)
    if channel == None:
        raise InputError

    if start > len(channel.messages) or start < 0:
        raise InputError

    user = data_store.get_user(auth_user_id)
    if user not in channel.members:
        raise AccessError

    if start + 50 < len(channel.messages):
        end = start +50
        messages = channel.messages[start:start+50]
    else: 
        end = -1
        messages = channel.messages[start:len(channel.messages)]

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }


def channel_join_v1(auth_user_id, channel_id):
    
    
    
    
    
    return {
    }


