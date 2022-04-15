""" This python file contains all custom objects and classes
besides the given ones """

# Imports
import re
from src.data_store import data_store
from src.encrypt import hashing_password
from src.error import InputError
from src.config import TAGGED, MSG_REACTED, ADDED, ICON, CHNL, DM, MSG
from src.time import get_time

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
    def __init__(self, email, password, name_first, name_last, is_load=False, **kwargs):
        self.email = email
        self.password = hashing_password(password) if not is_load else password
        self.name_first = name_first
        self.name_last = name_last
        self.id = self.__generate_id(kwargs.get('id', None))
        self.handle = kwargs.get('handle', self.__create_handle(name_first, name_last))
        self.owner = kwargs.get('owner', self.id == 1)
        self.removed = kwargs.get('removed', False)
        self.img = kwargs.get('img', ICON)
        self.notifications = [Notification.decode_json(item) for item in kwargs.get('notifications', [])]
        self.channels = kwargs.get('channels', 0)
        self.dms = kwargs.get('dms', 0)
        self.messages = kwargs.get('messages', 0)

        curr_time = get_time()
        self.ch_list = kwargs.get('ch_list', [{'num_channels_joined': 0, 'time_stamp': curr_time}])    # {'num_channels_joined': user.channels, 'time_stamp': user.chtime}
        self.dm_list = kwargs.get('dm_list', [{'num_dms_joined': 0, 'time_stamp': curr_time}])    # {'num_dms_joined': user.dms, 'time_stamp': user.dmtime}
        self.mg_list = kwargs.get('mg_list', [{'num_messages_sent': 0, 'time_stamp': curr_time}])    # {'num_messages_sent': user.messages, 'time_stamp': user.mgtime}

    '''
        Generates id for user
    '''
    def __generate_id(self, id):
        if id is not None:
            return int(id)

        store = data_store.get()
        curr_id = store['last_used_id']['users'] + 1
        store['last_used_id']['users'] = curr_id
        return curr_id

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

    # dosent look clean but i have no better idea
    def serialize(self):
        return {
            'email': self.email,
            'password': self.password,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'kwargs': {
                'id': self.id,
                'handle': self.handle,
                'owner': self.owner,
                'removed': self.removed,
                'img': self.img,
                'notifications': [notif.serialize() for notif in self.notifications],
                'channels': self.channels,
                'dms': self.dms,
                'messages': self.messages,
                'ch_list': self.ch_list,
                'dm_list': self.dm_list,
                'mg_list': self.mg_list,
            }
        }

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
            'profile_img_url': str(self.img)
        }
        return return_dict

    """
        for a removed user:
            Their profile must still be retrievable with user/profile.
            however name_first should be 'Removed'.
            name_last should be 'user'.
            The user's email and handle should be reusable.
    """
    def set_removed_user_profile(self):
        self.email = ''
        self.name_first = 'Removed'
        self.name_last = 'user'
        self.handle = ''
        self.owner = False
        self.removed = True
        data_store.set_store()

    def update_stats(self, item, number):
        time = get_time()
        store = data_store.get()

        if item == CHNL:
            self.channels += number
            self.ch_list.append({'num_channels_joined': self.channels, 'time_stamp': time})
        elif item == DM:
            self.dms += number
            self.dm_list.append({'num_dms_joined': self.dms, 'time_stamp': time})
        else:
            self.messages += number
            self.mg_list.append({'num_messages_sent': self.messages, 'time_stamp': time})

        data_store.set(store)

    def involvement_rate(self):
        store = data_store.get()
        global_num = store['stats_list']['chs_num'] + store['stats_list']['dms_num'] + store['stats_list']['msg_num']

        if global_num == 0:
            return float(0)

        ir = min((self.channels + self.dms + self.messages) / global_num, 1)
        return float(ir)

    @staticmethod
    def decode_json(jsn):
        return User(
            email=jsn['email'], 
            password=jsn['password'], 
            name_first=jsn['name_first'], 
            name_last=jsn['name_last'], 
            is_load=True, 
            **jsn['kwargs']
        )

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
    def __init__(self, name, owner, is_public, id=None, owners=None, members=None):
        self.id = self.__generate_id(id)
        self.name = name
        self.owners = owners if owners is not None else [owner]
        self.members = members if members is not None else [owner]
        self.is_public = is_public
        self.standup = {'active': False, 'user_id': None, 'end': None, 'message': '',}

    '''
        Generates id for Channel
    '''
    def __generate_id(self, id):
        if id is not None:
            return int(id)

        data = data_store.get()
        curr_id = data['last_used_id']['channel'] + 1
        data['last_used_id']['channel'] = curr_id
        return curr_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'owners': [usr.id for usr in self.owners],
            'members': [usr.id for usr in self.members],
            'is_public': self.is_public,
        }

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
    def add_member(self, usr, adder, dm_name=None):
        if not usr == adder and dm_name is None:
            Notification.push_notif(
                u_id=usr.id,
                notif_type=ADDED,
                user_handle=adder.handle,
                channel_id=self.id,
            )
        elif not usr == adder and dm_name is not None:
            Notification.push_notif(
                u_id=usr.id,
                notif_type=ADDED,
                user_handle=adder.handle,
                channel_id=self.id,
                dm_name=dm_name,
            )
        self.members.append(usr)
        data_store.set_store()

    '''
        Argument:
            -usr_id: int

        Adds a usr corresponding to the id to the current channel
    '''
    def add_member_id(self, usr_id, adder):
        self.add_member(data_store.get_user(usr_id), data_store.get_user(adder))

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
        msg_list = [msg for msg in msg_list if msg.chnl_id == self.id]
        msg_list.reverse()
        return msg_list

    '''
        Removes all messages in the channel
    '''
    def remove_associated_msg(self):
        data = data_store.get()
        data['messages'] = [msg for msg in data['messages'] if msg.chnl_id != self.id]
        data_store.set_store()

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
    
    def clear_standup(self):
        self.standup['active'] = False
        self.standup['user_id'] = None
        self.standup['end'] = None
        self.standup['message'] = ''
        data_store.set_store()

    @staticmethod
    def decode_json(jsn, owners, members):
        return Channel(jsn['name'], None, jsn['is_public'], 
            jsn['id'], owners, members)

class DmChannel(Channel):
    def __init__(self, owner, u_ids, id=None, owners=None, members=None):
        # Sanity check
        if owner is not None:
            if len(set(u_ids)) != len(u_ids) or owner.id in u_ids:
                raise InputError(description="error: Duplicates of ids are not allowed.")
            
            if not all(data_store.has_user_id(u_id) for u_id in u_ids):
                raise InputError(description="error: Invalid user id")

        # Initiate class
        super().__init__('', owner, False, id, owners, members)
        # add members in channel
        usr_list = [data_store.get_user(u_id) for u_id in u_ids]
        handle_list = [curr_user.handle for curr_user in usr_list]
        if owner is not None:
            handle_list.insert(0, owner.handle)
        
        dm_name = ', '.join(sorted(handle_list))
        for usr in usr_list:
            self.add_member(usr, owner, dm_name)

        # Set name
        self.name = ', '.join(sorted([mem.handle for mem in self.members]))
    
    def channel_dict(self):
        result = super().channel_dict()

        # Replace key channel_id with dm_id
        new_dict = {(key if key != 'channel_id' else 'dm_id'): val for key, val in result.items()}
        return new_dict
    
    # get all messages from a channel OR dm
    def get_messages(self):
        msg_list = data_store.get()['messages']
        msg_list = [msg for msg in msg_list if msg.chnl_id == self.id]
        msg_list.reverse()
        return msg_list

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

    @staticmethod
    def decode_json(jsn, owners, members):
        return DmChannel(None, [], jsn['id'], owners, members)

class Message:
    def __init__(self, u_id, message, chnl_id, **kwargs):
        self.u_id = u_id
        self.message = message
        self.chnl_id = chnl_id
        self.id = self.__generate_id(kwargs.get('id', None))
        self.time_sent = kwargs.get('time_sent', get_time())
        self.reacts = kwargs.get('reacts', [])
        self.is_pinned = kwargs.get('is_pinned', False)
        self.tagged_id = kwargs.get('tagged', [])

        # Push notif to the specified user if the user is tagged
        self.__push_notifs_if_tagged()

    def __generate_id(self, id):
        if id is not None:
            return int(id)

        data = data_store.get()
        curr_id = data['last_used_id']['messages'] + 1
        data['last_used_id']['messages'] = curr_id
        return curr_id

    def __get_usr_specific_react_dict(self, u_id):
        reacts = self.reacts.copy()
        for react in reacts:
            react['is_this_user_reacted'] = u_id in react['u_ids']

        return reacts

    def __push_notifs_if_tagged(self):
        tags = re.findall('@[a-zA-Z0-9]*', self.message)

        # getting rid of duplicates
        tags = list(set(tags))

        origin_chnl = self.get_origin_channel()

        if origin_chnl is None:
            return

        mem_list = origin_chnl.members
        
        handle_to_usr = lambda x: next((usr for usr in mem_list if usr.handle == x), None)

        for tag in tags:
            usr = handle_to_usr(tag[1:])

            if usr is not None and usr.id not in self.tagged_id:
                Notification.push_notif(
                    u_id=usr.id,
                    notif_type=TAGGED,
                    user_handle=data_store.get_user(self.u_id).handle,
                    channel_id=self.chnl_id,
                    msg_content=self.message,
                )
                self.tagged_id.append(usr.id)


    def get_origin_channel(self):
        channel_originated = (data_store.get_channel(self.chnl_id) 
            if data_store.has_channel_id(self.chnl_id) else data_store.get_dm(self.chnl_id))
        
        return channel_originated

    def edit_message(self, new_msg):
        self.message = new_msg
        self.__push_notifs_if_tagged()
        data_store.set_store()

    def add_reaction_from_id(self, u_id, react_id):
        react_dict = next((item for item in self.reacts if item['react_id'] == react_id), None)
        if react_dict is None:
            self.reacts.append({
                'react_id': react_id,
                'u_ids': [u_id]
            })
        else:
            if u_id in react_dict['u_ids']:
                raise InputError(description='error: Already reacted')
            else:
                react_dict['u_ids'].append(u_id)

        # Push notifications
        if self.get_origin_channel().has_member_id(self.u_id):
            Notification.push_notif(
                u_id=self.u_id,
                notif_type=MSG_REACTED,
                user_handle=data_store.get_user(u_id).handle,
                channel_id=self.chnl_id,
            )

        data_store.set_store()

    def remove_reaction_from_id(self, u_id, react_id):
        react_dict = next((item for item in self.reacts if item['react_id'] == react_id), None)
        if react_dict is None or u_id not in react_dict['u_ids']:
            raise InputError(description='error: User did not react in the first place')
        else:
            if len(react_dict['u_ids']) <= 1:
                self.reacts.remove(react_dict)
            else:
                react_dict['u_ids'].remove(u_id)

        data_store.set_store()

    def to_dict(self, u_id):
        return {
            'message_id': self.id,
            'u_id': self.u_id,
            'message': self.message,
            'time_sent': self.time_sent,
            'reacts': self.__get_usr_specific_react_dict(u_id),
            'is_pinned': self.is_pinned,
        }

    def serialize(self):
        return {
            'u_id': self.u_id,
            'message': self.message,
            'chnl_id': self.chnl_id,
            'kwargs': {
                'id': self.id,
                'time_sent': self.time_sent,
                'reacts': self.reacts,
                'is_pinned': self.is_pinned,
                'tagged_id': self.tagged_id,
            }
        }

    @staticmethod
    def decode_json(jsn):
        return Message(
            u_id=jsn['u_id'],
            message=jsn['message'], 
            chnl_id=jsn['chnl_id'], 
            **jsn['kwargs']
        )

class Notification:
    def __init__(self, **kwargs):
        self.notif_type = kwargs.get('notif_type')
        self.user_handle = kwargs.get('user_handle')
        self.channel_id = kwargs.get('channel_id', -1)
        self.dm_id = kwargs.get('dm_id', -1)
        self.msg_content = kwargs.get('msg_content', '')

        dm_name = kwargs.get('dm_name')
        if dm_name is not None:
            self.dm_name = dm_name

        self.msg = self.__generate_msg()
        
        

    def __get_chnl_name(self):
        if self.channel_id != -1:
            return data_store.get_channel(self.channel_id).name
        #####
        elif data_store.get_dm(self.dm_id) is not None:
            return data_store.get_dm(self.dm_id).name
        #####
        else:
            return self.dm_name

    def __generate_msg(self):
        notif = f"{self.user_handle} "
        if self.notif_type == TAGGED:
            notif += f"tagged you in {self.__get_chnl_name()}: {self.msg_content[:20]}"
        elif self.notif_type == MSG_REACTED:
            notif += f"reacted to your message in {self.__get_chnl_name()}"
        else:
            # for when self.notif_type == ADDED (condition removed for coverage)
            notif += f"added you to {self.__get_chnl_name()}"
        return notif

    def serialize(self):
        return {
            'notif_type': self.notif_type,
            'user_handle': self.user_handle,
            'channel_id': self.channel_id,
            'dm_id': self.dm_id,
            'msg_content': self.msg_content,
        }

    @staticmethod
    def decode_json(jsn):
        return Notification(**jsn)

    # Wanted to use **kwargs as arguments but pylint said no
    @staticmethod
    def push_notif(u_id, notif_type, user_handle, channel_id, 
                   msg_content='', dm_name=None):
        usr = data_store.get_user(u_id)

        # Should have a one line solution but i couldnt think of any
        if data_store.has_channel_id(channel_id):
            dm_id = -1
        else:
            dm_id = channel_id
            channel_id = -1

        kwargs = {
            'notif_type': notif_type,
            'user_handle': user_handle,
            'channel_id': channel_id,
            'dm_id': dm_id,
            'msg_content': msg_content,
        }
        if dm_name is not None:
            kwargs['dm_name'] = dm_name

        new_notif = Notification(**kwargs)
        usr.notifications.insert(0, new_notif)
        data_store.set_store()

    def to_dict(self):
        return {
            'notif_type': self.notif_type,
            'user_handle': self.user_handle,
            'channel_id': self.channel_id,
            'dm_id': self.dm_id,
            'msg_content': self.msg_content,
            'msg': self.msg
        }

