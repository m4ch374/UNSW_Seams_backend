import re
from src.data_store import data_store
from src.error import InputError


'''
Arguments:
    email (sting)    - user's email
    password (string)    - password for login

Return Value:
    Returns   -1      when the email is not matched
              0       when the email matched but incorrect password
           user_id    when email and password both matched
'''
def login_account_check(email, password):
    store = data_store.get()
    for user in store['users']:
        if email == user['email']:
            if  password == user['password']:
                return user['id']
            return 0
    return -1


'''
Arguments:
    email (sting)    - user's email
    password (string)    - password for login

Exceptions:
    InputError  - Occurs when email entered does not belong to a user.
                         when password is not correct.

Return Value:
    Returns user's ID (integer) if the correct input
'''
def auth_login_v1(email, password):
    state = login_account_check(email, password)
    if state == -1:
        raise InputError("Account does not exist")
    elif state == 0:
        raise InputError("Password incorrect")
    else:
        user_id = state
        return {'auth_user_id' : user_id}


'''
Arguments:
    email (sting)    - user's email

Return Value:
    Returns True when email is valid
            False when email is not valid
'''
def check_email_valid(email):
    return re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email)


'''
Arguments:
    handle (sting)    - user's email
    users  (list)     - a list of all user

Return Value:
    Returns True when handle is exist
            False if not
'''
def handle_exist(handle, users):
    return any(handle == user['handle'] for user in users)


'''
Arguments:
    firsatname (sting)    - user's first name
    lastname (sting)    - user's last name

Return Value:
    handle (string)   - Remove non-alphanumeric characters and convert to lowercase
                        length of handle aim to less than 20 characters
'''
def creat_handle(firsatname, lastname):
    idx = 0
    handle = ''.join(c for c in firsatname if c.isalnum()) + ''.join(c for c in lastname if c.isalnum())
    handle = handle.lower()
    store = data_store.get()
    if len(handle) > 20:
        handle = handle[0:20]
    if handle_exist(handle, store['users']):
        handle_temp = handle
        while handle_exist(handle_temp, store['users']):
            handle_temp = handle + str(idx)
            idx += 1
        handle = handle_temp
    return handle


'''
Arguments:
    email (sting)   - user's email

Return Value:
    boolean         - False if email already exist
                      True if not
'''
def email_is_new(email):
    store = data_store.get()
    return email not in (user['email'] for user in store['users'])


'''
Arguments:
    email (sting)    - user's email
    password (string)    - user's password
    name_first (string)    - user's first name
    name_last (string)    - user's last name

Exceptions:
    InputError  - Occurs when email entered is not a valid email
                         when email address is already exist
                         when length of password is less than 6 characters
                         when length of name_last/name_first is not between 1 and 50 characters inclusive

Return Value:
    Returns user's ID (integer) on the correct input
'''
def auth_register_v1(email, password, name_first, name_last):
    if not check_email_valid(email):                        # email not valid
        raise InputError("Email address not valid")
    elif not email_is_new(email):                           # email exists
        raise InputError("Email address already exists")
    elif len(password) < 6:                                 # password less than 6 characters
        raise InputError("Length of password should more than 6 characters")
    elif len(name_first) > 50 or len(name_first) < 1 or len(name_last) > 50 or len(name_last) < 1:
        raise InputError("Length of first/last name should between 1 to 50 characters (inclusive)")
    else:
        store = data_store.get()
        handle = creat_handle(name_first, name_last)
        new_id = len(store['users']) + 1
        new_user = {'email': email,
                    'password' : password,
                    'firstname' : name_first,
                    'lastname' : name_last,
                    'id' : new_id,
                    'handle' : handle,
                    'is_in_channel' : [],
                    'owner' : False,}
        store['users'].append(new_user)
        data_store.set(store)
        return {'auth_user_id' : new_user['id']}                 # return user's id
