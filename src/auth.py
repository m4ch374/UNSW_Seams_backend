import re
from src.data_store import data_store
from src.error import InputError, AccessError
from src.objecs import User
from src.encrypt import hashing_password

# '''
# Arguments:
#     email (string)    - user's email
#     password (string)    - password for login

# Return Value:
#     Returns   -1      when the email is not matched
#               0       when the email matched but incorrect password
#            user_id    when email and password both matched
# '''
# def login_account_check(email, password):
#     users = data_store.get()['users']
#     for user in users:
#         if email == user.email:
#             if  password == user.password:
#                 return user.id
#             return 0
#     return -1


# '''
# Arguments:
#     email (string)    - user's email
#     password (string)    - password for login

# Exceptions:
#     InputError  - Occurs when email entered does not belong to a user.
#                          when password is not correct.

# Return Value:
#     Returns user's ID (integer) if the correct input
# '''
# def auth_login_v1(email, password):
#     state = login_account_check(email, password)
#     if state == -1:
#         raise InputError(description="Account does not exist")
#     elif state == 0:
#         raise InputError(description="Password incorrect")
#     else:
#         user_id = state
#         return {'auth_user_id': user_id}


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
        if email == user.email:
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


# '''
# Arguments:
#     email (string)    - user's email
#     password (string)    - user's password
#     name_first (string)    - user's first name
#     name_last (string)    - user's last name

# Exceptions:
#     InputError  - Occurs when email entered is not a valid email
#                          when email address is already exist
#                          when length of password is less than 6 characters
#                          when length of name_last/name_first is not between 1 and 50 characters inclusive

# Return Value:
#     Returns user's ID (integer) on the correct input
# '''
# def auth_register_v1(email, password, name_first, name_last):
#     if not check_email_valid(email):                        # email not valid
#         raise InputError(description="Email address not valid")
#     elif not email_is_new(email):                           # email exists
#         raise InputError(description="Email address already exists")
#     elif len(password) < 6:                                 # password less than 6 characters
#         raise InputError(description="Length of password should more than 6 characters")
#     elif len(name_first) > 50 or len(name_first) < 1 or len(name_last) > 50 or len(name_last) < 1:
#         raise InputError(description="Length of first/last name should between 1 to 50 characters (inclusive)")
#     else:
#         new_user = User(
#             email = email,
#             password = password,
#             name_first = name_first,
#             name_last = name_last,
#             iteration = 1,
#         )
#         store = data_store.get()
#         store['users'].append(new_user)
#         data_store.set(store)
#         return {'auth_user_id': new_user.id}         # return user's id


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

