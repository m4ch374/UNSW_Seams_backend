""" This python file contains all custom objects and classes
besides the given ones """

# Imports
from src.data_store import data_store
from src.encrypt import hashing_password
from src.error import InputError

'''
User Class, store information of each user
Contains:
      email       (string) - User's email
      password    (string) - User's password in plain text
      name_first  (strong) - User's first name
      name_last   (string) - User's last name
      id          (int)    - User's id
      handle      (string) - User's handle
      channels    (list)   - User's channels
      ower        (boolean)- user's global permissions

Help:
To initialize a new user:
new_user = User(.....) # Fill in arguments as how it is in functions

To add new user to data_store:
data = data_store.get()
new_usr = User(.....)
data['users'].append(new_usr)
data_store.set(data)

To access the content of User:
email_account = new_user.email

To change the content of User:
new_user.email = new_email

To represent User in dict
usr_in_dict = new_user.to_dict()
'''
class User:
    def __init__(self, email, password, name_first, name_last):
        self.email = email
        self.password = hashing_password(password)
        self.name_first = name_first
        self.name_last = name_last
        self.id = self.__generate_id()
        self.handle = self.__create_handle(name_first, name_last)
        self.owner = self.id == 1
        self.removed = False

    '''
        Generates id for user
    '''
    def __generate_id(self):
        store = data_store.get()
        return len(store['users']) + 1

    '''
    Arguments:
        handle (string)    - user's email
        users  (list)     - a list of all user

    Return Value:
        Returns True when handle is exist
                False if not
    '''
    def __handle_exist(self, handle, users):
        return any(handle == user.handle for user in users)


    '''
    Arguments:
        firsatname (string)    - user's first name
        lastname (string)    - user's last name

    Return Value:
        handle (string)   - Remove non-alphanumeric characters and convert to lowercase
                            length of handle aim to less than 20 characters
    '''
    def __create_handle(self, firsatname, lastname):
        idx = 0
        handle = ''.join(c for c in firsatname + lastname if c.isalnum())
        handle = handle.lower()
        store = data_store.get()
        if len(handle) > 20:
            handle = handle[0:20]
        if self.__handle_exist(handle, store['users']):
            handle_temp = handle
            while self.__handle_exist(handle_temp, store['users']):
                handle_temp = handle
                handle_temp += str(idx)
                idx += 1
            handle = handle_temp
        return handle

    '''
        Output format following section 6.1. of the sepec
    '''
    def to_dict(self):
        return_dict = {
            'u_id': int(self.id),
            'email': str(self.email),
            'name_first': str(self.name_first),
            'name_last': str(self.name_last),
            'handle_str': str(self.handle),
        }
        return return_dict

    """
        for a removed user:
            Their profile must still be retrievable with user/profile.
            however name_first should be 'Removed'.
            name_last should be 'user'.
            The user's email and handle should be reusable.
    """
    # This is just bad code......
    def set_removed_user_profile(self, id):
        store = data_store.get()
        for user in store['users']:
            if user.id == id:
                user.email = ''
                user.name_first = 'Removed'
                user.name_last = 'user'
                user.handle = ''
                user.owner = False
                user.removed = True
        data_store.set(store)
               
'''
Channel class, stores info of a channel
Contains:
      id          (int)           - id of the chanel
      name        (str)           - name of the channel
      owners      (list(Users))   - List of owners who owns the channel
      members     (list(Users))   - List of members in the channel
      is_public   (bool)          - weather its public or not

Help:
To initialize a new channel
new_channel = Channel(.....)  # same as User

To add new channel to data_store:
data = data_store.get()
new_chnl = Channel(.....)
data['channel'].append(new_chnl)
data_store.set(data)

To access the content of User:
channel_name = new_chnl.name

To change the content of User:
new_chnl.name = new_channel_name

To represent User in dict:
chnl_in_dict = new_chnl.to_dict()

To know whether a member is in channel:
has_mem = new_chnl.has_member(member)

NOTE: member is of type User, NOT ITS ID
If you want to use id, use `has_member_id()` instead
'''
class Channel:
    def __init__(self, name, owner, is_public):
        self.id = self.__generate_id()
        self.name = name
        self.owners = [owner]
        self.members = [owner]
        self.is_public = is_public

    '''
        Generates id for Channel
    '''
    def __generate_id(self):
        data = data_store.get()
        return len(data['channel']) + len(data['dm']) + 1

    '''
        Argument:
            - member: User()
        
        Returns:
            True: when an User() object was found in this channel
            False: otherwise
    '''
    def has_member(self, member):
        return member in self.members

    '''
        Arugument:
            - member_id: int

        Returns:
            True: member_id was found in this channel
            False: otherwise
    '''
    def has_member_id(self, member_id):
        return member_id in [mem.id for mem in self.members]

    '''
        Arugument:
            - owner_id: int

        Returns:
            True: owner_id was found in this channel
            False: otherwise
    '''
    def has_owner_id(self, owner_id):
        return owner_id in [owner.id for owner in self.owners]

    '''
        Argument:
            - usr: User()

        Adds a user to the current channel
    '''
    def add_member(self, usr):
        self.members.append(usr)
        data_store.set_store()

    '''
        Argument:
            -usr_id: int

        Adds a usr corresponding to the id to the current channel
    '''
    def add_member_id(self, usr_id):
        self.add_member(data_store.get_user(usr_id))

    '''
        Argument:
            -usr_id: int

        Removes a usr from the current channel
    '''
    def remove_member(self, usr):
        self.members.remove(usr)
        data_store.set_store()

    '''
        Argument:
            - usr_id: int
        
        Removes a owner from the current channel
    '''
    def remove_owner(self, usr):
        self.owners.remove(usr)
        data_store.set_store()

    '''
        Argument:
            -usr_id: int

        Removes a usr corresponding to the id from the current channel
    '''
    def remove_member_id(self, usr_id):
        self.remove_member(data_store.get_user(usr_id))

    '''
        Argument:
            -usr_id: int

        Removes a owner corresponding to the id from the current channel
    '''
    def remove_owner_id(self, usr_id):
        self.remove_owner(data_store.get_user(usr_id))

    '''
        Gets all messages in the channel
    '''
    def get_messages(self):
        msg_list = data_store.get()['messages']
        return [msg for msg in msg_list if msg.chnl_id == self.id]

    '''
        Returns basic info of this channel in dictionary form (following docs)

        Return value: {channel_id, name}
    '''
    def channel_dict(self):
        return_dict = {
            'channel_id': int(self.id),
            'name': str(self.name),
        }
        return return_dict

    '''
        Returns detailed info of this channel in dictionary form (following docs)

        Return value: {name, is_public, owner_members, all_members}
    '''
    def channel_details_dict(self):
        return_dict = {
            'name': str(self.name),
            'is_public': bool(self.is_public),
            'owner_members': [owner.to_dict() for owner in self.owners],
            'all_members': [member.to_dict() for member in self.members],
        }
        return return_dict

class DmChannel(Channel):
    def __init__(self, owner, u_ids):
        # Sanity check
        if len(set(u_ids)) != len(u_ids):
            raise InputError(description="error: Duplicates of ids are not allowed.")
        
        if not all(data_store.has_user_id(u_id) for u_id in u_ids):
            raise InputError(description="error: Invalid user id")

        # Initiate class
        usr_list = [data_store.get_user(u_id) for u_id in u_ids]
        super().__init__('', owner, False)
        
        # Set id
        self.id = self.__generate_id()

        # add members in channel
        for usr in usr_list:
            self.add_member(usr)

        # Set name
        self.name = ', '.join(sorted([mem.handle for mem in self.members]))

    def __generate_id(self):
        data = data_store.get()
        return len(data['channel']) + len(data['dm']) + 1
    
    def channel_dict(self):
        result = super().channel_dict()

        # Replace key channel_id with dm_id
        new_dict = {(key if key != 'channel_id' else 'dm_id'): val for key, val in result.items()}
        return new_dict
    
    # get all messages from a channel OR dm
    def get_messages(self):
        msg_list = data_store.get()['messages']
        return [msg for msg in msg_list if msg.chnl_id == self.id]

    # NOTE: Members include the owner
    def channel_details_dict(self):
        result = {
            'name': self.name,
            'members': [usr.to_dict() for usr in self.members]
        }
        return result

    def has_member_id(self, member_id):
        return member_id in [mem.id for mem in self.members]

    def has_owner_id(self, owner_id):
        return owner_id in [owner.id for owner in self.owners]

    '''
        Argument:
            -usr_id: int

        Removes a usr from the current dm
    '''
    def remove_member(self, usr):
        self.members.remove(usr)
        data_store.set_store()

    '''
        Argument:
            -usr_id: int

        Removes a usr corresponding to the id from the current channel
    '''
    def remove_member_id(self, usr_id):
        self.remove_member(data_store.get_user(usr_id))

        

class Message:
    def __init__(self, u_id, message, chnl_id, time_sent):
        self.id = self.__generate_id()
        self.u_id = u_id
        self.message = message
        self.chnl_id = chnl_id
        self.time_sent = time_sent


    def __generate_id(self):
        data = data_store.get()
        return len(data['messages']) + 1
