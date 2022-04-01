import re
import urllib.request
import smtplib, ssl
import string
import random
import requests
from datetime import timezone
import datetime as dt
from PIL import Image
from datetime import datetime
from src.data_store import data_store
from src.error import InputError, AccessError
from src.objecs import User
from src.encrypt import hashing_password
from src.config import SERVER_EMAIL, SERVER_PASSWORD
from src.config import N


'''
    Compare two passwords
'''
def compare_password(password, user_password):
    return user_password == hashing_password(password)


'''
Arguments:
    email (string)    - user's email
    password (string)    - password for login

Return Value:
    Returns   -1      when the email is not matched
              0       when the email matched but incorrect password
           user_id    when email and password both matched
'''
def login_account_check_v2(email, password):
    users = data_store.get()['users']
    for user in users:
        if email == user.email and not user.removed:
            if compare_password(password, user.password):
                return user.id
            return 0
    return -1


'''
Arguments:
    email (string)    - user's email
    password (string)    - password for login

Exceptions:
    InputError  - Occurs when email entered does not belong to a user.
                         when password is not correct.

Return Value:
    user's ID (integer) if the correct input
    token (string)  Encrypted user id and time
'''
def auth_login_v1(email, password):
    state = login_account_check_v2(email, password)
    if state == -1:
        raise InputError(description="Account does not exist")
    elif state == 0:
        raise InputError(description="Password incorrect")
    else:
        user_id = state
        store = data_store.get()
        token = data_store.generate_token(user_id)
        data_store.set(store)
        return {'token': token, 'auth_user_id': user_id}


'''
Arguments:
    token (string)  Encrypted user id and time
'''
def auth_logout_v1(token):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    else:
        data_store.remove_token(token)
        return {}


'''
Arguments:
    email (string)    - user's email

Return Value:
    Returns True when email is valid
            False when email is not valid
'''
def check_email_valid(email):
    return re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email)


'''
Arguments:
    email (string)   - user's email

Return Value:
    boolean         - False if email already exist
                      True if not
'''
def email_is_new(email):
    users = data_store.get()['users']
    return email not in [user.email for user in users]


'''
Arguments:
    email (string)    - user's email
    password (string)    - user's password
    name_first (string)    - user's first name
    name_last (string)    - user's last name

Exceptions:
    InputError  - Occurs when email entered is not a valid email
                         when email address is already exist
                         when length of password is less than 6 characters
                         when length of name_last/name_first is not between 1 and 50 characters inclusive

Return Value:
    user's ID (integer) on the correct input
    token (string)  Encrypted user id and time
'''
def auth_register_v1(email, password, name_first, name_last):
    if not check_email_valid(email):                        # email not valid
        raise InputError(description="Email address not valid")
    elif not email_is_new(email):                           # email exists
        raise InputError(description="Email address already exists")
    elif len(password) < 6:                                 # password less than 6 characters
        raise InputError(description="Length of password should more than 6 characters")
    elif len(name_first) > 50 or len(name_first) < 1 or len(name_last) > 50 or len(name_last) < 1:
        raise InputError(description="Length of first/last name should between 1 to 50 characters (inclusive)")
    else:
        new_user = User(
            email = email,
            password = password,
            name_first = name_first,
            name_last = name_last,
        )
        store = data_store.get()
        token = data_store.generate_token(new_user.id)
        store['users'].append(new_user)
        data_store.set(store)
        return {'token': token, 'auth_user_id': new_user.id}         # return user's id


'''
Arguments:
    token (string)  Encrypted user id and time

Return Value:
    users (list)    A list of all user's detail
'''
def users_all_v1(token):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    else:
        users = []
        for user in data_store.get()['users']:
            if not user.removed:
                users.append(user.to_dict())
        return {'users': users}


'''
Arguments:
    token (string)  Encrypted user id and time
    u_id (integer)    - user's id

Exceptions:
    InputError  - u_id does not refer to a valid user

Return Value:
    user's detail (dirt)    user's email, name, handle, id....
'''
def user_profile_v1(token, u_id):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    else:
        user = data_store.get_user(u_id)
        if user == None:
            raise InputError(description="u_id does not refer to a valid user")
        else:
            return {'user': user.to_dict()}


'''
Arguments:
    token (string)  Encrypted user id and time
    name_first (string)    - user's first name
    name_last (string)    - user's last name

Exceptions:
    InputError  - Occurs
    when length of name_last/name_first is not between 1 and 50 characters inclusive

Return Value:
    An empty dirt {}
'''
def user_profile_setname_v1(token, name_first, name_last):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    else:
        if len(name_first) > 50 or len(name_first) < 1 or len(name_last) > 50 or len(name_last) < 1:
            raise InputError(description="Length of first/last name should between 1 to 50 characters (inclusive)")
        else:
            store = data_store.get()
            User_id = data_store.get_id_from_token(token)
            for user in store['users']:
                if user.id == User_id:
                    user.name_first = name_first
                    user.name_last = name_last
            data_store.set(store)
            return {}


'''
Arguments:
    token (string)  Encrypted user id and time
    email (string)    - user's email

Exceptions:
    InputError  - Occurs    Email address not valid
                            Email address already exists

Return Value:
    An empty dirt {}
'''
def user_profile_setemail_v1(token, email):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    else:
        User_id = data_store.get_id_from_token(token)
        if not check_email_valid(email):
            raise InputError(description="Email address not valid")
        elif not email_is_new(email):
            raise InputError(description="Email address already exists")
        else:
            store = data_store.get()
            for user in store['users']:
                if user.id == User_id:
                    user.email = email
            data_store.set(store)
            return {}


'''
Arguments:
    handle (string)  new handle

Return Value:
    True    if handle is alphanumeric
    False   if handle is not alphanumeric
'''
def handle_valid(handle_str):
    return handle_str.isalnum()


'''
Arguments:
    handle (string)  new handle

Return Value:
    True    if handle is exist
    False   if handle is new
'''
def handle_exist(handle):
    return any(handle == user.handle for user in data_store.get()['users'])


'''
Arguments:
    token (string)  Encrypted user id and time
    handle_str (string)  new handle

Exceptions:
    InputError  - Occurs    Length of handle should between 3 and 20 characters
                            Handle contains characters that are not alphanumeric
                            Handle is already used by another user

Return Value:
    An empty dirt {}
'''
def user_profile_sethandle_v1(token, handle_str):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    else:
        User_id = data_store.get_id_from_token(token)
        if len(handle_str) < 3 or len(handle_str) > 20:
            raise InputError(description="Length of handle should between 3 and 20 characters")
        elif not handle_valid(handle_str):
            raise InputError(description="Handle contains characters that are not alphanumeric")
        elif handle_exist(handle_str):
            raise InputError(description="Handle is already used by another user")
        else:
            store = data_store.get()
            for user in store['users']:
                if user.id == User_id:
                    user.handle = handle_str
            data_store.set(store)
            return {}


# '''
# Arguments:
#     token (string)  Encrypted user id and time

# Exceptions:
#     AccessError  - Occurs    Invalid token

# Return Value:
#     list of dict        -[{channel_id, dm_id, notification_message}...]
# '''
# def notifications_get_v1(token):
#     return {'notifications': []}
#     if not data_store.is_valid_token(token):
#         raise AccessError(description="Token is invalid!")
#     else:
#         u_id = data_store.get_id_from_token(token)
#         for user in data_store.get()['users']:
#             if user.id == u_id:
#                 return {'notifications': user.notifications}


'''
Arguments:
    token (string)  Encrypted user id and time
    query_str (string)  string to search

Exceptions:
    AccessError  - Occurs   Invalid token
                            length of query_str should be 1 to 1000

Return Value:
    list of dict        -[{message_id, u_id, message...}...]
'''
def search_v1(token, query_str):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    elif len(query_str) < 1 or len(query_str) > 1000:
        raise InputError(description="length of query_str should be 1 to 1000")
    else:
        u_id = data_store.get_id_from_token(token)
        msg_list = []
        for msg in data_store.get()['messages']:
            if msg.u_id == u_id and query_str.casefold() in msg.message.casefold():
                #TODO
                msg_list.append({'message_id': msg.id,
                                'u_id': msg.u_id,
                                'message': msg.message,
                                'time_sent': msg.time_sent,
                                'reacts': 'msg.reacts',
                                'is_pinned': 'msg.is_pinned'})
        return {'messages': msg_list}


'''
Arguments:
    email (string)    - user's email
    reset_code (string) - reset code
'''
def send_email(email, reset_code):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = SERVER_EMAIL
    password = SERVER_PASSWORD
    receiver_email = email
    message = reset_code
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


'''
Arguments:
    email (string)    - user's email

Return Value:
    An empty dict {}
'''
def auth_passwordreset_request_v1(email):
    store = data_store.get()
    for user in store['users']:
        if user.email == email:
            data_store.remove_token_by_id(user.id)
            reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
            store['reset_code'][reset_code] = user.id
            data_store.set(store)
            send_email(email, reset_code)
    return {}


'''
Arguments:
    reset_code      (string)  resetcode
    new_password    (string)  new password

Exceptions:
    InputError  - Occurs    Invalid reset_code
                            Length of password less than 6 characters

Return Value:
    An empty dirt {}
'''
def auth_passwordreset_reset_v1(reset_code, new_password):
    reset_code = reset_code.upper()
    if not data_store.has_reset_code(reset_code):
        raise InputError(description="Invalid reset_code")
    elif len(new_password) < 6:                                 # password less than 6 characters
        raise InputError(description="Length of password should more than 6 characters")
    else:
        store = data_store.get()
        u_id = store['reset_code'][reset_code]
        for user in store['users']:
            if user.id == u_id:
                user.password = hashing_password(new_password)
                store['reset_code'].pop(reset_code)
                data_store.set(store)
                return {}



'''
Arguments:
    token   (string)  Encrypted user id and time
    img_url (int)
    x_start (int)
    y_start (int)
    x_end   (int)
    y_end   (int)

Exceptions:
    InputError  - Occurs    Invalid token
                            Invalid img_url
                            Pictures size not matched
                            Pictures size is not correct
                            Image not a JPG

Return Value:
    An empty dirt {}
'''
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    elif not requests.get(img_url).status_code == 200:
        raise InputError(description="Pictures not available")
    else:
        u_id = data_store.get_id_from_token(token)
        urllib.request.urlretrieve(img_url, f"images/{u_id}.jpg")
        img = Image.open(f"images/{u_id}.jpg")
        width, height = img.size
        if x_start < 0 or x_end > width or y_start < 0 or y_end > height:
            raise InputError(description="Pictures size not matched")
        elif x_end <= x_start or y_end <= y_start:
            raise InputError(description="Pictures size is invalid")
        elif img.mode != 'RGB':
            raise InputError(description="Image must be JPG")
        else:
            cropped = img.crop((x_start, y_start, x_end, y_end))
            cropped.save(f"images/{u_id}.jpg")
            store = data_store.get()
            for user in store['users']:
                if user.id == u_id:
                    user.img = img_url
            data_store.set(store)
            return {}


'''
Arguments:
    token (string)  Encrypted user id and time

Exceptions:
    InputError  - Occurs    Invalid token

Return Value:
    An dict         {'user_stats': ....}
'''
def user_stats_v1(token):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    else:
        u_id = data_store.get_id_from_token(token)
        for user in data_store.get()['users']:
            if user.id == u_id:
                time = ((dt.datetime.now(timezone.utc)).replace(tzinfo=timezone.utc)).timestamp()
                #TODO
                rate = 0.5
                return {'user_stats': {'channels_joined': [{'num_channels_joined': 1, 'time_stamp': time}],  # user.channels
                                       'dms_joined': [{'num_dms_joined': user.dms, 'time_stamp': time}],
                                       'messages_sent': [{'num_messages_sent': 1, 'time_stamp': time}],      # user.messages
                                       'involvement_rate': rate}}


'''
Arguments:
    token (string)  Encrypted user id and time

Exceptions:
    InputError  - Occurs    Invalid token

Return Value:
    An dict         {'workspace_stats': ....}
'''
def users_stats_v1(token):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    else:
        #TODO
        store = data_store.get()
        time = ((dt.datetime.now(timezone.utc)).replace(tzinfo=timezone.utc)).timestamp()
        chs = [{'num_channels_exist': len(store['channel']), 'time_stamp': time}]
        dms = [{'num_dms_exist': len(store['dm']), 'time_stamp': time}]
        mgs = [{'num_messages_exist': len(store['messages']), 'time_stamp': time}]
        rate = 0.5
        return {'workspace_stats': {'channels_exist': chs,
                                    'dms_exist': dms,
                                    'messages_exist': mgs,
                                    'utilization_rate': rate}}

