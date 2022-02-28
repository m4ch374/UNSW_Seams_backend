# This python file contains all custom objects and classes
# besides the given ones

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
    def __init__(self, email, password, name_first, name_last, id, handle):
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.id = id
        self.handle = handle

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
    def __init__(self, id, name, owners, is_public):
        self.id = id
        self.name = name
        self.owners = [owners]
        self.members = [owners]
        self.is_public = is_public

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
            'owner_members': self.owners,
            'all_members': self.members,
        }
        return return_dict