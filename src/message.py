from src.data_store import data_store
from src.objecs import Message
from src.error import InputError, AccessError
import src.stats_helper as User
from src.config import REACT_IDS
from src.time import get_time
from datetime import timezone
import datetime as dt
import threading


'''
Function: channel_messages_v1
Given a channel with ID channel_id that the authorised user is a member of, 
returns up to 50 messages starting from given start position.

Arguments:
   - auth_user_id - id of the user requesting messages
   - channel_id - id of the channel messages are being requested from
   - start - the id of first message that is required
 Exceptions:
   - InputError - Occurs when channel_id does not refer to valid channel or start does not 
                  refer to a valid message id
   - AccessError -> Occurs when the user id is invalid or when the ids are valid the 
                    user is not a member of the channel. Takes priority over InputError
 Returns:
   - messages (list of dictionaries) when no errors raised
   - start (integer) when no errors raised
   - end (integer) when no errors raised
'''
def channel_messages_v1(auth_user_id, channel_id, start):
    
    # Checking valid channel id, start id and user access
    if data_store.has_channel_id(channel_id) == False:
        raise InputError(description='Invalid channel')
    channel = data_store.get_channel(channel_id)
    if channel.has_member_id(auth_user_id) == False:
        raise AccessError('Invalid access to channel')
    chnl_messages = channel.get_messages()
    if start > len(chnl_messages) or start < 0:
        raise InputError('Invalid message start index')
    
    # Splitting the stored messages list to paginate returned messages
    if start + 50 < len(chnl_messages):
        end = start + 50
        messages = channel.get_messages()[start:start+50]
    else:
        end = -1
        messages = channel.get_messages()[start:len(chnl_messages)+1]
    
    msg_list = [msg.to_dict(auth_user_id) for msg in messages]

    return {
        'messages': msg_list,
        'start': start,
        'end': end,
    }

'''
Function: dm_messages_v1
Given a channel with ID channel_id that the authorised user is a member of, 
returns up to 50 messages starting from given start position.

Arguments:
   - user_id - id of the user requesting messages
   - dm_id - id of the dm messages are being requested from
   - start - the id of first message that is required
 Exceptions:
   - InputError - Occurs when dm_id does not refer to valid dm or start does not 
                  refer to a valid message id
   - AccessError -> Occurs when the user id is invalid or when the ids are valid but the 
                    user is not a member of the dm. Takes priority over InputError
 Returns:
   - messages (list of dictionaries) 
   - start (integer) 
   - end (integer)
'''
def dm_messages_v1(user_id, dm_id, start):

    # Checking valid channel id, start id and user access
    if data_store.has_dm_id(dm_id) == False:
        raise InputError(description='Invalid channel')
    dm = data_store.get_dm(dm_id)
    if dm.has_member_id(user_id) == False:
        raise AccessError(description='Invalid access to channel')
    chnl_messages = dm.get_messages()
    if start > len(chnl_messages) or start < 0:
        raise InputError(description='Invalid message start index')

    # Splitting the stored messages list to paginate returned messages
    if start + 50 < len(chnl_messages):
        end = start + 50
        messages = dm.get_messages()[start:start+50]
    else:
        end = -1
        messages = chnl_messages[start:len(chnl_messages)]
    
    msg_list = [msg.to_dict(user_id) for msg in messages]

    return {
        'messages': msg_list,
        'start': start,
        'end': end,
    }


'''
Function: message_send_v1
Creates and stores a new message in a given channel when given a valid string by an
authorised user.

Arguments:
   - user_id - id of the user sending the message
   - channel_id - id of the channel the message is being sent in
   - message - the string of the message to be created
 Exceptions:
   - InputError -> Occurs when channel_id does not refer to valid channel or the string is too long
                  (>1000 characters) or empty
   - AccessError -> Occurs when the user id is invalid or when the ids are valid but the 
                    user is not a member of the channel. Takes priority over InputError
 Returns:
   - message_id -> the newly generated id of the new message
'''
def message_send_v1(user_id, channel_id, message):
    
    # Checking valid ids, access, and message length
    if data_store.has_channel_id(channel_id) == False:
        raise InputError(description='Invalid channel')
    channel = data_store.get_channel(channel_id)
    if channel.has_member_id(user_id) == False:
        raise AccessError(description='Invalid access to channel')
    if message is None or len(message) == 0 or len(message) > 1000:
        raise InputError(description='Message must be between 1 and 1000 character inclusive')

    new_message = Message(
        u_id=user_id,
        message=message,
        chnl_id=channel_id,
    )

    # Append new message to data_store
    data = data_store.get()
    data['messages'].append(new_message)
    data_store.set(data)

    User.user_sent_msg(user_id)
    User.add_msg()

    return {'message_id': new_message.id}


'''
Function: message_senddm_v1
Creates and stores a new message in a given dm when given a valid string by an
authorised user.

Arguments:
   - user_id - id of the user sending the message
   - dm_id - id of the dm the message is being sent in
   - message - the string of the message to be created
 Exceptions:
   - InputError -> Occurs when dm_id does not refer to valid dm or the string is too long
                  (>1000 characters) or empty
   - AccessError -> Occurs when the user id is invalid or when the ids are valid but the 
                    user is not a member of the dm. Takes priority over InputError
 Returns:
   - message_id (integer) -> the newly generated id of the new message
'''
def message_senddm_v1(user_id, dm_id, message):

    # Checking valid ids, access, and message length
    if data_store.has_dm_id(dm_id) == False:
        raise InputError(description='Invalid channel')
    dm = data_store.get_dm(dm_id)
    if dm.has_member_id(user_id) == False:
        raise AccessError(description='Invalid access to channel')
    if message is None or len(message) == 0 or len(message) > 1000:
        raise InputError(description='Message must be between 1 and 1000 character inclusive')

    new_message = Message(
        u_id=user_id,
        message=message,
        chnl_id=dm_id,
    )

    # Append new message to data_store
    data = data_store.get()
    data['messages'].append(new_message)
    data_store.set(data)

    User.user_sent_msg(user_id)
    User.add_msg()

    return {'message_id': new_message.id}


# Helper function which checks for valid user id, msg id and permissions before 
# editing or removing a message
def message_edit_and_remove_checks(user_id, msg_id):
    if data_store.has_msg_id(msg_id) == False:
        raise InputError(description='Message id does not exist')
    msg = data_store.get_msg(msg_id)
    channel = data_store.get_channel(msg.chnl_id)
    channel_type = 'channel'
    if channel == None:
        channel_type = 'dm'
        channel = data_store.get_dm(msg.chnl_id)
    if not channel.has_member_id(user_id):
        raise InputError(description='Message id does not exist in your channels')

    if channel_type == 'dm':
        if not msg.u_id == user_id and not channel.has_owner_id(user_id):
            raise AccessError(description='You cannot change that dm message')
    else:
        if not msg.u_id == user_id and not channel.has_owner_id(user_id) and not data_store.get_user(user_id).owner:
            raise AccessError(description='You cannot change that message')
 


'''
Function: message_edit_v1
Edits an existing message in a channel/dm that the user is a part of. User must be the message
sender or have owner permission in the channel/dm

Arguments:
   - user_id - id of the user sending the message
   - msg_id - id of the channel the message is being sent in
   - message - the string of the message to be created
 Exceptions:
   - InputError -> Occurs when msg_id does not refer to a valid message in a channel that the user is in,
                when the string is too long (>1000 characters)
   - AccessError -> Occurs when the user id is invalid or when the ids are valid but the 
                    user does not have permissions to edit a message. Takes priority over InputError
 Returns:
   - Empty dictionary upon succes
'''
def message_edit_v1(user_id, msg_id, message):

    message_edit_and_remove_checks(user_id, msg_id)
    
    if len(message) > 1000:
        raise InputError(description='Message must be less than 1000 characters')

    if len(message) == 0:
        message_remove_v1(user_id, msg_id)
    else:
        msg = data_store.get_msg(msg_id)
        msg.edit_message(message)

    return {}
    


'''
Function: message_remove_v1
Deletes an existing message in a channel/dm that the user is a part of. User must be the message
sender or have owner permission in the channel/dm

Arguments:
   - user_id - id of the user sending the message
   - msg_id - id of the channel the message is being sent in
 Exceptions:
   - InputError -> Occurs when msg_id does not refer to a valid message in a channel that the user is in
   - AccessError -> Occurs when the user id is invalid or when the ids are valid but the 
                    user does not have permissions to delete a message. Takes priority over InputError
 Returns:
   - Empty dictionary upon succes
'''
def message_remove_v1(user_id, msg_id):

    message_edit_and_remove_checks(user_id, msg_id)

    msg = data_store.get_msg(msg_id)
    data = data_store.get()
    data['messages'].remove(msg)
    data_store.set_store()

    User.remove_msg()

    return {}
# ============================
#        Helper Function 
# ============================
'''
Function that checks if a user has owner permissions in the channel /dm where
the message originated from
Return true if user has owner permissions
return false otherwise
'''
def does_user_have_owner_permissions_for_msg_chnl(auth_user_id, message_id):
    message = data_store.get_msg(message_id)
    channel_originated = (data_store.get_channel(message.chnl_id) 
        if data_store.has_channel_id(message.chnl_id) 
        else data_store.get_dm(message.chnl_id))
    user = data_store.get_user(auth_user_id)
    # works if they are a global owner
    if user.owner:
        return user.owner
    else:
        return channel_originated.has_owner_id(auth_user_id)
'''
Function: message_pin_v1
Given a message within a channel or DM, mark it as "pinned".

Arguments:
    - auth_user_id (int) - id of user pinning message
    - message_id (int) - id of the message being pinned
Exceptions:
    - InputError - Occurs when message_id is not a valid message within a 
                   channel or DM that the authorised user has joined
    - InputError - Occurs when the message is already pinned
    - AccessError - Occurs when message_id refers to a valid message in a joined
                    channel/DM and the authorised user does not have owner
                    permissions in the channel/DM
Return Value: {}
'''
def message_pin_v1(auth_user_id, msg_id):
    
    check_valid_msg_id(msg_id, auth_user_id)
    if not does_user_have_owner_permissions_for_msg_chnl(auth_user_id, msg_id):
        raise AccessError(description = 'User does not have owner permissions')
    message = data_store.get_msg(msg_id)
    if message.is_pinned == True:
        raise InputError(description = 'Message is already pinned')
    
    message.is_pinned = True
    data_store.set_store()
    return {}

'''
Function: message_unpin_v1
Given a message within a channel or DM, remove its mark as pinned.

Arguments:
    - auth_user_id (int) - id of user pinning message
    - message_id (int) - id of the message being unpinned
Exceptions
    - InputError - Occurs when message_id is not a valid message within a 
                   channel or DM that the authorised user has joined
    - InputError - Occurs when the message is not already pinned
    - AccessError - Occurs when message_id refers to a valid message in a joined
                    channel/DM and the authorised user does not have owner
                    permissions in the channel/DM
'''
def message_unpin_v1(auth_user_id, msg_id):
    check_valid_msg_id(msg_id, auth_user_id)
    if not does_user_have_owner_permissions_for_msg_chnl(auth_user_id, msg_id):
        raise AccessError(description = 'User does not have owner permissions')
    message = data_store.get_msg(msg_id)
    if message.is_pinned == False:
        raise InputError(description = 'Message is already not pinned')
    
    message.is_pinned = False
    data_store.set_store()
    return {}

# ===============================================
# Every thing below here is written by Hanqi
# ===============================================
"""
    sent msg to channel/dm
    for sentlater ch/dm
"""
def send_msg(new_message, u_id):
    data = data_store.get()
    data['messages'].append(new_message)
    data_store.set(data)

    User.user_sent_msg(u_id)
    User.add_msg()


'''
Arguments:
    token           (string)
    channel_id      (int)
    message         (string)
    time_sent       (int) send time

Exceptions:
    InputError  - Occurs    Invalid channel id
                            message < 1 or > 1000
                            time_sent is a time in the past
    AccessError - Occurs    Invalid token
                            user not a member

Return Value:
    message_id      (int)
'''
def message_sendlater_v1(token, channel_id, message, time_sent):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")

    if not data_store.has_channel_id(channel_id):
        raise InputError(description="channel_id does not refer to a valid channel")

    user_id = data_store.get_id_from_token(token)
    channel = data_store.get_channel(channel_id)
    if not channel.has_member_id(user_id):
        raise AccessError(description="user not a member")

    if len(message) < 1 or len(message) > 1000:
        raise InputError(description="message should be 1 to 1000")

    time_now = get_time()
    if time_sent <= time_now:
        raise InputError(description="time_sent is a time in the past")

    new_message = Message(
        u_id=user_id,
        message=message,
        chnl_id=channel_id,
        time_sent=time_sent
    )
    t = threading.Timer(time_sent - time_now, send_msg, [new_message, user_id])
    t.start()

    return {'message_id': new_message.id}


'''
Arguments:
    token           (string)
    dm_id      (int)
    message         (string)
    time_sent       (int) send time

Exceptions:
    InputError  - Occurs    Invalid channel id
                            message < 1 or > 1000
                            time_sent is a time in the past
    AccessError - Occurs    Invalid token
                            user not a member

Return Value:
    message_id      (int)
'''
def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")

    if not data_store.has_dm_id(dm_id):
        raise InputError(description="dm_id does not refer to a valid dm")

    user_id = data_store.get_id_from_token(token)
    dm = data_store.get_dm(dm_id)
    if not dm.has_member_id(user_id):
        raise AccessError(description="user not a member")

    if len(message) < 1 or len(message) > 1000:
        raise InputError(description="message should be 1 to 1000")

    time_now = get_time()
    if time_sent <= time_now:
        raise InputError(description="time_sent is a time in the past")

    new_message = Message(
        u_id=user_id,
        message=message,
        chnl_id=dm_id,
        time_sent=time_sent
    )
    t = threading.Timer(time_sent - time_now, send_msg, [new_message, user_id])
    t.start()

    return {'message_id': new_message.id}

# ===============================================
# Every thing below here is written by Henry
# ===============================================

# ================= Helper ======================
def check_valid_msg_id(message_id, u_id):
    if not data_store.has_msg_id(message_id):
        raise InputError(description="error: Invalid msg id")

    message = data_store.get_msg(message_id)
    channel_originated = message.get_origin_channel()

    if not channel_originated.has_member_id(u_id):
        raise InputError(description="error: Not in channel of associated message")

def check_valid_react_id(react_id):
    if react_id not in REACT_IDS:
        raise InputError(description="error: Invalid react ID")
# ===============================================

def message_share_v1(u_id, og_msg_id, msg, chnl_id, dm_id):
    # Error checks
    if chnl_id == -1 and dm_id == -1:
        raise InputError(description="error: Both channel and dm id are invalid")
    
    if chnl_id != -1 and dm_id != -1:
        raise InputError(description="error: Neither id is invalid")

    check_valid_msg_id(og_msg_id, u_id)
    
    if len(msg) > 1000:
        raise InputError(description="error: Message too large")

    dest_chnl = data_store.get_channel(chnl_id) if chnl_id != -1 else data_store.get_dm(dm_id)
    if not dest_chnl.has_member_id(u_id):
        raise AccessError(description="error: Not in channel")

    # share mesage
    original_msg_content = data_store.get_msg(og_msg_id).message
    shared_msg = Message(
        u_id=u_id,
        message=msg + 
                "\n==========\n" + 
                original_msg_content,
        chnl_id=dest_chnl.id
    )

    data = data_store.get()
    data['messages'].append(shared_msg)
    data_store.set_store()

    return {'shared_message_id': shared_msg.id}

def message_react_v1(u_id, message_id, react_id):
    check_valid_msg_id(message_id, u_id)
    check_valid_react_id(react_id)

    message = data_store.get_msg(message_id)
    message.add_reaction_from_id(u_id, react_id)

    return {}

def message_unreact_v1(u_id, message_id, react_id):
    check_valid_msg_id(message_id, u_id)
    check_valid_react_id(react_id)

    message = data_store.get_msg(message_id)
    message.remove_reaction_from_id(u_id, react_id)

    return {}
