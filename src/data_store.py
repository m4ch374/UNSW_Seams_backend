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
import pickle
import os
import jwt
from datetime import datetime
from src.config import TOKEN_SECRET
from src.error import AccessError

# Initial object
initial_object = {
    'users' : [], 
    'channel' : [],
    'dm': [],
    'messages': [],
    'tokens' : [],
} # credit to Hanqi for this placeholder love you <3

# Definitions
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
DATA_PATH = CURRENT_DIR + '_data.bin'

## YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH
class Datastore:
    def __init__(self):
        self.__store = self.__get_store()

    # Get data and fill it to __store
    def __get_store(self):
        try:
            file_content = open(DATA_PATH, "rb")
            data = pickle.load(file_content)
        except Exception:   # if file is not found or file is empty, return initial obj
            file_content = open(DATA_PATH, "wb+")
            data = initial_object
            pickle.dump(data, file_content)
        
        file_content.close()
        return data

    # Store everything in __store to `_data.bin`
    def set_store(self):
        file_handler = open(DATA_PATH, "wb")
        pickle.dump(self.__store, file_handler)
        file_handler.close()

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store
        self.set_store()

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

print('Loading Datastore...')

global data_store
data_store = Datastore()
