import datetime as dt
from src.data_store import data_store
from src.objecs import Message
import src.stats_helper as User
from src.error import InputError, AccessError
import threading as thread


def standup_thread_helper(user_id, channel_id):
    
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

    # for stats
    User.user_sent_msg(user_id)
    User.add_msg()

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
        raise InputError('Standup already active in channel')
    
    channel.standup['active'] = True
    channel.standup['user_id'] = user_id
    channel.standup['end'] = (dt.datetime.now() + dt.timedelta(seconds=length)).timestamp()

    standup_timer = thread.Timer(length, standup_thread_helper, args=(user_id, channel_id))
    standup_timer.start

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
    if channel.standup['active']:
        raise InputError('Standup already active in channel')
    # Add messages to messages string in standup