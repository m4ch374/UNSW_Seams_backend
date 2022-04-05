import datetime as dt
from src.data_store import data_store
from src.objecs import Message, Channel, DmChannel
from src.error import InputError, AccessError
import src.stats_helper as User

def standup_start_v1(user_id, channel_id, length):
    # Error raises
        # Make sure it is a channel type, not dm

    # set standup period to true and channel standup_end to the end datetime(figure out how datetime works lol)
    channel.standup['end'] = dt.datetime.now() + dt.timedelta(seconds=length)
    
    # start thread to send messages at the end of timer
    return channel.standup_end

def standup_send_v1(user_id, channel_id):
    # Error raises

    # Add messages to messages string in standup


def standup_active_v1(user_id, channel_id):
    # Error raises

    # Return true/false and time