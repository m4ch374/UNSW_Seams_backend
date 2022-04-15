from src.data_store import data_store
from src.objecs import Notification
from src.config import TAGGED, MSG_REACTED, ADDED

'''
Function that is given a notification object, and returns the dict of format:
{ channel_id, dm_id, notification_message } where channel_id and DM id are the
channels which it took place in (-1 if it did not take place in it)
 Notification_message is a string of the following format for each trigger action:
    - tagged: "{User's handle} tagged you in {channel/DM name}: {first 20 
                characters of the message}"
    - reacted message: "{User's handle} reacted to your message in 
                        {channel/DM name}"
    - added to a channel/DM: "{User's handle} added you to {channel/DM name}"
'''
def dict_from_notif_obj(notif):
    notif_dict = notif.to_dict()
    return {
        'channel_id': notif_dict['channel_id'],
        'dm_id': notif_dict['dm_id'],
        'notification_message': notif_dict['msg']
    }
'''
Return List of dictionaries, where each dictionary contains types {channel_id, 
dm_id, notification_message} where channel_id is the id of the channel that the
event happened in, and is -1 if it is being sent to a DM. dm_id is the DM that
the event happened in, and is -1 if it is being sent to a channel. 
Notification_message is a string of the following format for each trigger action:
    - tagged: "{User??s handle} tagged you in {channel/DM name}: {first 20 
               characters of the message}"
    - reacted message: "{User??s handle} reacted to your message in 
      {channel/DM name}"
    - added to a channel/DM: "{User??s handle} added you to {channel/DM name}"
'''
def notifications_get_v1(auth_user_id):
    auth_user = data_store.get_user(auth_user_id)
    notiffs = [dict_from_notif_obj(notif) for notif in auth_user.notifications]
    notiffs = notiffs[:20]
    return {'notifications': notiffs}
