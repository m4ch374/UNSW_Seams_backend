'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)

    ================================

    Added functions and usage

    # To get the user:
    usr = data_store.get_user(auth_user_id)

    NOTE: assumes id is valid, returns None if there are no entries in users list
'''

# Imports
import json
import os
import jwt
from datetime import datetime
from src.config import TOKEN_SECRET
from src.error import AccessError
import traceback
from src.time import get_time
from src.config import CHNL, DM, MSG

# Initial object
initial_object = {
    'users' : [],
    'channel' : [],
    'dm': [],
    'messages': [],
    'tokens' : [],
    'last_used_id': {
        'users': 0,
        'channel': 0,
        'messages': 0,
    },
    'reset_code': {},   # (dict) for user to reset password
    'stats_list': {
        'chs_num': 0,
        'dms_num': 0,
        'msg_num': 0,
        'chs_list': [],     # [{'num_channels_exist': chs_num, 'time_stamp': time}]
        'dms_list': [],     # [{'num_dms_exist': dms_num, 'time_stamp': time}]
        'msg_list': [],     # [{'num_messages_exist': msg_num, 'time_stamp': time}]
    },
}

# Definitions
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
DATA_PATH = CURRENT_DIR + '_data.json'

## YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH
class Datastore:
    def __init__(self):
        self.__store = initial_object

    # Get data and fill it to __store
    def get_store(self):
        try:
            file_content = open(DATA_PATH, "r")
            data = self.__json_to_obj(json.load(file_content))
        except Exception as e:   # if file is not found or file is empty, return initial obj
            print(e)
            traceback.print_exc()
            file_content = open(DATA_PATH, "w+")
            data = initial_object
            json.dump(data, file_content, indent=4)
        
        file_content.close()
        return data

    def __to_json(self):
        store = self.__store.copy()
        store['users'] = [usr.serialize() for usr in store['users']]
        store['channel'] = [chnl.serialize() for chnl in store['channel']]
        store['dm'] = [dm.serialize() for dm in store['dm']]
        store['messages'] = [msg.serialize() for msg in store['messages']]
        return store

    def __json_to_obj(self, jsn):
        # would cause error if imported from the top
        # due to circular import issues
        # didnt want to, but have to
        from src.objecs import User, Channel, DmChannel, Message
        jsn['users'] = [User.decode_json(item) for item in jsn['users']]

        id_to_usr = lambda x : next((usr for usr in jsn['users'] if usr.id == x), None)
        get_users = lambda li: [id_to_usr(u_id) for u_id in li]

        jsn['channel'] = [Channel.decode_json(item, get_users(item['owners']), get_users(item['members'])) 
            for item in jsn['channel']]

        jsn['dm'] = [DmChannel.decode_json(item, get_users(item['owners']), get_users(item['members'])) 
            for item in jsn['dm']]

        jsn['messages'] = [Message.decode_json(item) for item in jsn['messages']]
        return jsn

    # Store everything in __store to `_data.bin`
    def set_store(self):
        file_handler = open(DATA_PATH, "w")
        json.dump(data_store.__to_json(), file_handler, indent=4)
        file_handler.close()

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store
        self.set_store()

    def tmp_set(self, store):
        self.__store = store

    def get_user(self, id):
        for user in self.__store['users']:
            if user.id == id:
                return user
        return None

    def get_channel(self, id):
        if len(self.__store['channel']) == 0:
            return None
        else:
            return [chnl for chnl in self.__store['channel'] if chnl.id == id][0]

    def get_msg(self, id):
        if len(self.__store['messages']) == 0:
            return None
        else:
            return [msg for msg in self.__store['messages'] if msg.id == id][0]

    def has_channel_id(self, id):
        return any(id == chnl.id for chnl in self.__store['channel'])
    
    def has_user_id(self, id):
        return any(id == usr.id for usr in self.__store['users'])

    def has_msg_id(self, id):
        return  any(id == msg.id for msg in self.__store['messages'])
        
    # Check if token is valid
    def is_valid_token(self, token):
        return token in self.__store['tokens']

    # Generates token, add it to data_store and returns it
    # takes in user_id
    def generate_token(self, auth_user_id):
        encode_msg = {
            'id': auth_user_id,
            'logged_in_at': str(datetime.now())  # so that it supports multi-instances
        }
        tok = jwt.encode(encode_msg, TOKEN_SECRET, "HS256")
        self.__store['tokens'].append(tok)
        self.set_store()
        return tok

    # Gets user id from token
    # Throws an exception if token is invalid
    def get_id_from_token(self, token):
        if not self.is_valid_token(token):
            raise AccessError(description='error: Invalid Token')

        decoded_data = jwt.decode(token, TOKEN_SECRET, "HS256")
        return decoded_data['id']

    # Invalidates a token by removing it
    # Throws an exception if token is invalid
    def remove_token(self, token):
        if not self.is_valid_token(token):
            raise AccessError(description='error: Invalid Token')

        self.__store['tokens'].remove(token)
        self.set_store()
        
    def has_dm_id(self, dm_id):
        return dm_id in [dm.id for dm in self.__store['dm']]

    def add_dm(self, dm):
        self.__store['dm'].append(dm)
        data_store.set_store()

    def get_dm(self, dm_id):
        for dm in self.__store['dm']:
            if dm.id == dm_id:
                return dm
        return None

    def remove_dm(self, dm):
        self.__store['dm'].remove(dm)
        data_store.set_store()
    
    def remove_msg(self, msg):
        self.__store['messages'].remove(msg)
        data_store.set_store()

    '''
        replace every message associated with the user given with
        the text 'Removed user'
    '''
    def modify_msg_removed_usr(self, u_id):
        data = self.get()
        for message in data['messages']:
            if message.u_id == u_id:
                message.message = 'Removed user'
        data_store.set(data)

    """
        return a list of user who is owner
    """
    def all_owners(self):
        return [user for user in data_store.get()['users'] if user.owner]

    """
        remove tokens associate with u_id
    """
    def remove_token_by_id(self, id):
        store = data_store.get()
        store['tokens'] = [tok for tok in store['tokens'] 
            if data_store.get_id_from_token(tok) != id]
        data_store.set(store)

    """
        true if reset_code exist
    """
    def has_reset_code(self, reset_code):
        return reset_code in data_store.get()['reset_code'].keys()

    def update_stats(self, item, number):
        time = get_time()
        store = self.__store
        stats = store['stats_list']
        if item == CHNL:
            stats['chs_num'] += number
            stats['chs_list'].append({
                'num_channels_exist': stats['chs_num'],
                'time_stamp': time,
            })
        elif item == DM:
            stats['dms_num'] += number
            stats['dms_list'].append({
                'num_dms_exist': stats['dms_num'],
                'time_stamp': time,
            })
        elif item == MSG:
            stats['msg_num'] += number
            stats['msg_list'].append({
                'num_messages_exist': stats['msg_num'],
                'time_stamp': time,
            })
        data_store.set(store)

    def utilization_rate(self):
        store = self.__store
        users = len([usr for usr in store['users'] if not usr.removed])
        num_joined = len([usr for usr in store['users'] if usr.channels > 0 or usr.dms > 0])
        return float(num_joined / users)


print('Loading Datastore...')

global data_store
data_store = Datastore()
store = data_store.get_store()
data_store.tmp_set(store)
