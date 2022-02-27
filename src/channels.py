# Imports
import src.channel as channel

from src.data_store import data_store
from src.error import InputError

# Arguments:
#       auth_user_id (int) - user's id

# Exceptions:
#       None

# Return value:
#       Returns a dick containing only field "channels" of type list
def channels_list_v1(auth_user_id):
    channels_list = data_store.get()['channel']

    return {
        'channels': [channel for channel in channels_list if channel['owner_id'] == auth_user_id],
    }

def channels_listall_v1(auth_user_id):
    channels_list = data_store.get()['channel']

    return {
        'channels': [channel for channel in channels_list],
    }

# Arguments:
#       auth_user_id (int)  - user's id
#       name         (str)  - name of the channel
#       is_public    (bool) - if the channel to be created is public

# Exceptions:
#       InputError - Occurs when length of name is less than 1 ||
#                                length of name is more than 20 ||
#                                name is None

# Return value:
#       Returns a dict containing channel_id of type int
def channels_create_v1(auth_user_id, name, is_public):
    if name == None or len(name) == 0 or len(name) > 20:
        raise InputError("error: Channel name should have 1 - 20 characters inclusive")

    # Append new channel to data_store
    data = data_store.get()
    new_channel_id = len(data['channel']) + 1
    channels = {
        'channel_id': new_channel_id,
        'name': name,
        'owner_id': auth_user_id,
        'member_ids': [auth_user_id],
        'is_public': is_public,
    }
    data['channel'].append(channels)
    data_store.set(data)

    # User who creates it joins the channel automatically
    channel.channel_join_v1(auth_user_id, new_channel_id)

    return {
        'channel_id': new_channel_id,
    }
