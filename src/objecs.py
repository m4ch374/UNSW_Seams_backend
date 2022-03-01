# This python file contains all custom objects and classes
# besides the given ones

# Imports
from src.data_store import data_store

# User Class, store information of each user
# Contains:
#       email       (string) - User's email
#       password    (string) - User's password in plain text
#       name_first  (strong) - User's first name
#       name_last   (string) - User's last name
#       id          (int)    - User's id
#       handle      (string) - User's handle
#
# Help:
# To initialize a new user:
# new_user = User(.....) # Fill in arguments as how it is in functions
#
# To add new user to data_store:
# data = data_store.get()
# new_usr = User(.....)
# data['users'].append(new_usr)
# data_store.set(data)
#
# To access the content of User:
# email_account = new_user.email
#
# To change the content of User:
# new_user.email = new_email
#
# To represent User in dict
# usr_in_dict = new_user.to_dict()
#
# NOTE: When comparing whether 2 Users variable are the same,
# it compares by the equality of its attributes i.e. email, password .....
# instead of the equality of address in the memory
class User:
    def __init__(self, email, password, name_first, name_last):
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.id = self.__generate_id()
        self.handle = self.__create_handle(name_first, name_last)

    def __eq__(self, other):
        return all(
            [
                self.email == other.email,
                self.password == other.password,
                self.name_first == other.name_first,
                self.name_last == other.name_last,
                self.id == other.id,
                self.handle == other.handle
            ]
        )

    def __generate_id(self):
        store = data_store.get()
        return len(store['users']) + 1

    # Arguments:
    #     handle (sting)    - user's email
    #     users  (list)     - a list of all user

    # Return Value:
    #     Returns True when handle is exist
    #             False if not
    def __handle_exist(self, handle, users):
        return any([handle == user.handle for user in users])


    # Arguments:
    #     firsatname (sting)    - user's first name
    #     lastname (sting)    - user's last name

    # Return Value:
    #     handle (string)   - Remove non-alphanumeric characters and convert to lowercase
    #                         length of handle aim to less than 20 characters
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

    def to_dict(self):
        return_dict = {
            'u_id': int(self.id),
            'email': str(self.email),
            'name_first': str(self.name_first),
            'name_last': str(self.name_last),
            'handle_str': str(self.handle),
        }
        return return_dict

# Channel class, stores info of a channel
# Contains:
#       id          (int)           - id of the chanel
#       name        (str)           - name of the channel
#       owners      (list(Users))   - List of owners who owns the channel
#       members     (list(Users))   - List of members in the channel
#       is_public   (bool)          - weather its public or not
#
# Help:
# To initialize a new channel
# new_channel = Channel(.....)  # same as User
#
# To add new channel to data_store:
# data = data_store.get()
# new_chnl = Channel(.....)
# data['channel'].append(new_chnl)
# data_store.set(data)
#
# To access the content of User:
# channel_name = new_chnl.name
#
# To change the content of User:
# new_chnl.name = new_channel_name
#
# To represent User in dict:
# chnl_in_dict = new_chnl.to_dict()
#
# To know whether a member is in channel:
# has_mem = new_chnl.has_member(member)
#
# NOTE: member is of type User, NOT ITS ID
# If you want to use id, use `has_member_id()` instead
class Channel:
    def __init__(self, name, owner, is_public):
        self.id = self.__generate_id()
        self.name = name
        self.owners = [owner]
        self.members = [owner]
        self.is_public = is_public

    def __generate_id(self):
        data = data_store.get()
        return len(data['channel']) + 1

    # Might need it someday
    # def __eq__(self, other):
    #     return all(
    #         [
    #             self.id == other.id,
    #             self.name == other.name,
    #             len(set(self.owners) ^ set(other.owners)) == 0,  # Same owners
    #             len(set(self.members) ^ set(other.members)) == 0,
    #             self.is_public == other.is_public
    #         ]
    #     )

    def has_member(self, member):
        return member in self.members

    def has_member_id(self, member_id):
        return member_id in [mem.id for mem in self.members]

    def to_dict(self):
        return_dict = {
            'name': self.name,
            'owner_members': [owner.to_dict() for owner in self.owners],
            'all_members': [member.to_dict() for member in self.members],
        }
        return return_dict
