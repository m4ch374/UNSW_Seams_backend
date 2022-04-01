""" This file contains edpoints:
        - channels_list_v1()
        - channels_listall_v1()
        - channels_create_v1()
"""

# Imports
from src.data_store import data_store
from src.error import InputError
from src.objecs import Channel, User

'''
Arguments:
      auth_user_id (int) - user's id

Exceptions:
      Access Error - Occurs when auth_user_id is invalid

Return value:
        { channels }
'''
def channels_list_v1(auth_user_id):
    channels_list = data_store.get()['channel']

    usr_channel = [channel.channel_dict() for channel in channels_list
        if channel.has_member(data_store.get_user(auth_user_id))]

    return {'channels': usr_channel}

'''
Arguments:
      auth_user_id (int) - user's id

Exceptions:
      Access Error - Occurs when auth_user_id is invalid

Return value:
      Returns a dict containing only field "channels" of type list

Note:
      auth_user_id is useless for now afaik
'''
def channels_listall_v1(auth_user_id):
    channels_list = data_store.get()['channel']

    return {'channels': [channel.channel_dict() for channel in channels_list]}

'''
Arguments:
      auth_user_id (int)  - user's id
      name         (str)  - name of the channel
      is_public    (bool) - if the channel to be created is public

Exceptions:
      Access Error - Occurs when auth_user_id is invalid

      InputError - Occurs when length of name is less than 1 ||
                               length of name is more than 20 ||
                               name is None

Return value:
      Returns a dict containing channel_id of type int
'''
def channels_create_v1(auth_user_id, name, is_public):
    if name is None or len(name) == 0 or len(name) > 20:
        raise InputError(
            "error: Channel name should have 1 - 20 characters inclusive")

    new_channel = Channel(
        name=name,
        owner=data_store.get_user(auth_user_id),
        is_public=is_public
    )

    # Append new channel to data_store
    data = data_store.get()
    data['channel'].append(new_channel)
    data_store.set(data)

    User.user_join_ch(auth_user_id)

    return {'channel_id': new_channel.id}
