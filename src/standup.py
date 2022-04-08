import datetime as dt
from src.config import MSG, INCREMENT
from src.data_store import data_store
from src.objecs import Message
from src.error import InputError, AccessError
import threading
import time


def standup_thread_helper(user_id, channel_id, length):
    time.sleep(length)
    channel = data_store.get_channel(channel_id)
    # Create and send standup message (no 1000 character limit)
    new_message = Message(
        u_id=user_id,
        message=channel.standup['message'],
        chnl_id=channel_id,
    )
    data = data_store.get()
    data['messages'].append(new_message)
    data_store.set(data)

    data_store.update_stats(MSG, INCREMENT)

    # reset channel standup
    channel.clear_standup()

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
    if len(message) > 1000:
        raise InputError(description='message must be less than 1000 characters')

    channel.standup['message'] += f'{data_store.get_user(user_id).handle}: {message}\n'

    return {}