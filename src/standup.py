"""
This file contains function for the domain
/standup
"""

import datetime as dt
from src.config import MSG, INCREMENT
from src.data_store import data_store
from src.objecs import Message
from src.error import InputError, AccessError
import threading
import time

# Helper function which keeps sleeps for the length of a standup then sends 
# standup message at the end of the wait time and ends standup.
def standup_thread_helper(user_id, channel_id, length):
    time.sleep(length)
    channel = data_store.get_channel(channel_id)
    
    if channel.standup['message'] != '':
        new_message = Message(
            u_id=user_id,
            message=channel.standup['message'],
            chnl_id=channel_id,
        )
        data = data_store.get()
        data['messages'].append(new_message)
        data_store.set(data)

        data_store.update_stats(MSG, INCREMENT)

    channel.clear_standup()

'''
Arguments:
      user_id (int) - id of user who is starting the standup
      channel_id (int) - id of channel standup will be started in
      length (int) - Time of standup in seconds

Exceptions:
      Access Error - Occurs when auth_user_id is invalid
      Input Error - When the channel id is invalid, when length is less than 1 or when stnadup
                     is already active in the channel

Return value:
        { end } - Timestamp of when the standup is to end
'''
def standup_start_v1(user_id, channel_id, length):
    if not data_store.has_channel_id(channel_id):
        raise InputError(description='Invalid channel')
    channel = data_store.get_channel(channel_id)
    if not channel.has_member_id(user_id):
        raise AccessError(description='Invalid access to channel')
    if length < 0:
        raise InputError(description='Length must be a positive number')
    if channel.standup['active']:
        raise InputError(description='Standup already active in channel')
    
    channel.standup['active'] = True
    channel.standup['user_id'] = user_id
    channel.standup['end'] = (dt.datetime.now() + dt.timedelta(seconds=length)).timestamp()

    standup = threading.Thread(target=standup_thread_helper, args=(user_id, channel_id, length))
    standup.start()

    return channel.standup['end']

'''
Arguments:
      user_id (int) - id of user who is starting the standup
      channel_id (int) - id of channel standup will be started in

Exceptions:
      Access Error - Occurs when auth_user_id is invalid
      Input Error - When the channel id is invalid

Return value:
        { is_active, time_finish } - If standup is active in channel and timestamp of when it will end
'''

def standup_active_v1(user_id, channel_id):
    if not data_store.has_channel_id(channel_id):
        raise InputError(description='Invalid channel')
    channel = data_store.get_channel(channel_id)
    if not channel.has_member_id(user_id):
        raise AccessError(description='Invalid access to channel')

    return {'is_active': channel.standup['active'],
            'time_finish': channel.standup['end']}


def standup_send_v1(user_id, channel_id, message):
    if not data_store.has_channel_id(channel_id):
        raise InputError(description='Invalid channel')
    channel = data_store.get_channel(channel_id)
    if not channel.has_member_id(user_id):
        raise AccessError(description='Invalid access to channel')
    if not channel.standup['active']:
        raise InputError(description='No standup active in this channel')
    if len(message) > 1000 or len(message) == 0:
        raise InputError(description='Message must be between 1 and 1000 characters')

    if channel.standup['message'] != '':
        channel.standup['message'] += '\n'

    channel.standup['message'] += f'{data_store.get_user(user_id).handle}: {message}'

    return {}