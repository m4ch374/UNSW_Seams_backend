import re
import urllib.request
import smtplib
import string
import random
import requests
import threading
import imgspy
from email.message import EmailMessage
from PIL import Image
from src.data_store import data_store
from src.error import InputError, AccessError
from src.objecs import User
from src.encrypt import hashing_password
from src.config import SERVER_EMAIL, SERVER_PASSWORD, N, EXPIRATION, url


'''
    Compare two passwords
'''
def compare_password(password, user_password):
    # compare the password
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
        # find the user and not removed
        if email == user.email and not user.removed:
            # compare the password
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
    # check if the user is able to login
    state = login_account_check_v2(email, password)
    if state == -1: raise InputError(description="Account does not exist")
    if state == 0: raise InputError(description="Password incorrect")
    # generate new token for user
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
    # removed the token
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
    # check if the email is duplicated
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
    if not check_email_valid(email):
        raise InputError(description="Email address not valid")
    if not email_is_new(email):
        raise InputError(description="Email address already exists")
    if len(password) < 6:
        raise InputError(description="Length of password should more than 6 characters")
    if len(name_first) > 50 or len(name_first) < 1 or len(name_last) > 50 or len(name_last) < 1:
        raise InputError(description="Length of first/last name should between 1 to 50 characters (inclusive)")
    # generate a new user
    new_user = User(
        email = email,
        password = password,
        name_first = name_first,
        name_last = name_last,
    )
    store = data_store.get()
    # set 0 point for the server as first user has registered
    if new_user.id == 1:
        time = new_user.ch_list[0]['time_stamp']
        store['stats_list']['chs_list'] = [{'num_channels_exist': 0, 'time_stamp': time}]
        store['stats_list']['dms_list'] = [{'num_dms_exist': 0, 'time_stamp': time}]
        store['stats_list']['msg_list'] = [{'num_messages_exist': 0, 'time_stamp': time}]
    # generate new token for user
    token = data_store.generate_token(new_user.id)
    store['users'].append(new_user)
    data_store.set(store)
    return {'token': token, 'auth_user_id': new_user.id}


'''
Arguments:
    token (string)  Encrypted user id and time

Return Value:
    users (list)    A list of all user's detail
'''
def users_all_v1(token):
    if not data_store.is_valid_token(token):
        raise AccessError(description="Token is invalid!")
    users = []
    for user in data_store.get()['users']:
        # append non removed user
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
    # get user from data_store
    user = data_store.get_user(u_id)
    if user == None:
        raise InputError(description="u_id does not refer to a valid user")
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
    if len(name_first) > 50 or len(name_first) < 1 or len(name_last) > 50 or len(name_last) < 1:
        raise InputError(description="Length of first/last name should between 1 to 50 characters (inclusive)")
    store = data_store.get()
    User_id = data_store.get_id_from_token(token)
    # find the user and reset name
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
    User_id = data_store.get_id_from_token(token)
    if not check_email_valid(email):
        raise InputError(description="Email address not valid")
    if not email_is_new(email):
        raise InputError(description="Email address already exists")
    store = data_store.get()
    # find the user and reset email
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
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description="Length of handle should between 3 and 20 characters")
    if not handle_valid(handle_str):
        raise InputError(description="Handle contains characters that are not alphanumeric")
    if handle_exist(handle_str):
        raise InputError(description="Handle is already used by another user")
    User_id = data_store.get_id_from_token(token)
    store = data_store.get()
    # find the user and reset handle
    for user in store['users']:
        if user.id == User_id:
            user.handle = handle_str
    data_store.set(store)
    return {}


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
    if len(query_str) < 1 or len(query_str) > 1000:
        raise InputError(description="length of query_str should be 1 to 1000")
    u_id = data_store.get_id_from_token(token)
    user = data_store.get_user(u_id)
    store = data_store.get()
    id_list = []
    # find channel id that the user joins in
    for ch in store['channel']:
        if user in ch.members:
            id_list.append(ch.id)
    # find dm id that the user joins in
    for dm in store['dm']:
        if user in dm.members:
            id_list.append(dm.id)
    msg_list = []
    # append msg that the user send
    for msg in store['messages']:
        if msg.chnl_id in id_list and query_str.casefold() in msg.message.casefold():
            msg_list.append({'message_id': msg.id,
                            'u_id': msg.u_id,
                            'message': msg.message,
                            'time_sent': msg.time_sent,
                            'reacts': msg.reacts,
                            'is_pinned': msg.is_pinned})
    return {'messages': msg_list}


'''
Arguments:
    email (string)    - user's email
    reset_code (string) - reset code
'''
def send_email(email, reset_code):
    msg = EmailMessage()
    msg.set_content(f'Your reset code is: < {reset_code} >, expire in one minute.\n(Do not share this verification code with others)')
    msg['Subject'] = 'Seams Reset Code'
    msg['From'] = "UNSW Seams"
    msg['To'] = email
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(SERVER_EMAIL, SERVER_PASSWORD)
    server.send_message(msg)
    server.quit()


'''
Arguments:
    reset_code (string)
'''
def remove_reset_code(reset_code):
    store = data_store.get()
    # remove a reset code
    # set reset code point to -1 to prevent reset code used before expired
    store['reset_code'][reset_code.upper()] = -1
    store['reset_code'].pop(reset_code.upper())
    data_store.set(store)


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
            # remove the old reset code
            code_list = [code for code in store['reset_code'] if store['reset_code'][code] == user.id]
            for code in code_list:
                remove_reset_code(code)
            # generate a random string
            reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
            # save the string to data_store
            store['reset_code'][reset_code] = user.id
            data_store.set(store)
            # set an expiration for reset code
            t = threading.Timer(EXPIRATION, remove_reset_code, [reset_code])
            t.start()
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
    if not data_store.has_reset_code(reset_code.upper()): raise InputError(description="Invalid reset_code")
    u_id = data_store.get()['reset_code'][reset_code.upper()]
    # remove the rest code from data_store
    remove_reset_code(reset_code.upper())
    if len(new_password) < 6: raise InputError(description="Length of password should more than 6 characters")
    # find the user and reset password
    for user in data_store.get()['users']:
        if user.id == u_id:
            user.password = hashing_password(new_password)
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
    if not requests.get(img_url).status_code == 200:
        raise InputError(description="Image not available")
    if not imgspy.info(img_url)['type'] == 'jpg':
        raise InputError(description="Image must be JPG")
    if x_end <= x_start or y_end <= y_start:
        raise InputError(description="Image size is invalid")
    width = imgspy.info(img_url)['width']
    height = imgspy.info(img_url)['height']
    if x_start < 0 or x_end > width or y_start < 0 or y_end > height:
        raise InputError(description="Image size not matched")
    # download the img
    u_id = data_store.get_id_from_token(token)
    urllib.request.urlretrieve(img_url, f"src/static/{u_id}.jpg")
    img = Image.open(f"src/static/{u_id}.jpg")
    # cut the img
    cropped = img.crop((x_start, y_start, x_end, y_end))
    cropped.save(f"src/static/{u_id}.jpg")
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            url = f'{url}static/{u_id}.jpg'
            user.img = url
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
    u_id = data_store.get_id_from_token(token)
    user = data_store.get_user(u_id)
    rate = user.involvement_rate()
    ret_dict = {
        'channels_joined': user.ch_list,
        'dms_joined': user.dm_list,
        'messages_sent': user.mg_list,
        'involvement_rate': rate
    }
    return {'user_stats': ret_dict}


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
    store = data_store.get()
    rate = data_store.utilization_rate()
    return {
        'workspace_stats': {
                'channels_exist': store['stats_list']['chs_list'],
                'dms_exist': store['stats_list']['dms_list'],
                'messages_exist': store['stats_list']['msg_list'],
                'utilization_rate': rate
            }
        }

