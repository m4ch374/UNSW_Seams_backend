from src.data_store import data_store
from src.objecs import Notification
from src.config import TAGGED, MSG_REACTED, ADDED

# helper functions

'''
function that is given a notif_dict, and returns the name of the chnl/dm which 
the dm took place in
'''
def get_chnldm_name_from_notif_dict(notif_dict):
    if notif_dict['channel_id'] != -1:
        return (data_store.get_channel(notif_dict['channel_id'])).name
    else:
        return (data_store.get_dm(notif_dict['dm_id'])).name
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
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(notif_dict)
    return {
        'channel_id': notif_dict['channel_id'],
        'dm_id': notif_dict['dm_id'],
        'notification_message': notif_dict['msg']
    }
    '''
    return {
        'channel_id': notif_dict['channel_id'],
        'dm_id': notif_dict['dm_id'],
        'notification_message': notif_dict['msg']
        
    }
    '''
    '''
    return_dict = {'channel_id': -1, 'dm_id': -1, 'notification_message': ""}
    channel_dm_name = get_chnldm_name_from_notif_dict(notif_dict)
    
    # set the channel/dm id for the return dict
    if notif_dict['channel_id'] != -1:
        return_dict['channel_id'] = notif_dict['channel_id']
    else:
        return_dict['dm_id'] = notif_dict['dm_id']

    # set the message for the return dict
    if notif_dict['notif_type'] == ADDED:
        notif_message = (f"{notif_dict['user_handle']} added you to "
                         f"{channel_dm_name}")
    elif notif_dict['notif_type'] == TAGGED:
        notif_message = (f"{notif_dict['user_handle']} tagged you in "
                         f"{channel_dm_name}: {notif_dict['msg_content']}")
    else:
        # case when notif_dict['notif_type'] == MSG_REACTED
        notif_message = (f"{notif_dict['user_handle']} reacted to your message "
                         f"in {channel_dm_name}")
    return_dict['notification_message'] = notif_message
    
   
    return return_dict
    '''
'''
Function : notifications_get_v1
Return the user's most recent 20 notifications, ordered from most recent to 
                                      triggered by stuff like tagged, reacted 
                                      message or added to chnl)
'''
'''
List of dictionaries, where each dictionary contains types { channel_id, dm_id, notification_message } where channel_id is the id of the channel that the event happened in, and is -1 if it is being sent to a DM. dm_id is the DM that the event happened in, and is -1 if it is being sent to a channel. Notification_message is a string of the following format for each trigger action:
      
        tagged: "{User??s handle} tagged you in {channel/DM name}: {first 20 characters of the message}"
        reacted message: "{User??s handle} reacted to your message in {channel/DM name}"
        added to a channel/DM: "{User??s handle} added you to {channel/DM name}"
'''
def notifications_get_v1(auth_user_id):
    auth_user = data_store.get_user(auth_user_id)
    curr_notifs = auth_user.notifications
    
    notiffs = [dict_from_notif_obj(notif) for notif in auth_user.notifications]
    # notiffs = [notif.to_dict for notif in auth_user.notifications]
    notiffs = notiffs[:20]
    print(notiffs)

    '''
    #########################################################
    # for debugging
    print("#############################################################")
    #first_notif = Notification.decode_json(curr_notifs[0])
    #print(f"printing the first notification decoded:{first_notif}")
    first_notif = auth_user.notifications[0]
    print(first_notif)
    print("#############################################################")
    ########################################################
    '''
    
    return {'notifications': notiffs}

