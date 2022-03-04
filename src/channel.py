from src.data_store import data_store
from src.error import InputError, AccessError
from src.objecs import Channel

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }


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


def channel_join_v1(auth_user_id, channel_id):
    channel = data_store.get_channel(channel_id)
    user = data_store.get_user(auth_user_id)
    channel.add_member(user)

    return {

    }
