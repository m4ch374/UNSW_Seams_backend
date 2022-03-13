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

# Initial object
initial_object = {
    'users' : [], 
    'channel' : [],
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
        file_content = open(DATA_PATH, "wb+")
        try:
            data = pickle.load(file_content)
        except EOFError:
            data = initial_object
        
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
        if len(self.__store['users']) == 0:
            return None
        else:
            return [usr for usr in self.__store['users'] if usr.id == id][0]

    def get_channel(self, id):
        if len(self.__store['channel']) == 0:
            return None
        else:
            return [chnl for chnl in self.__store['channel'] if chnl.id == id][0]

    def has_channel_id(self, id):
        return any(id == chnl.id for chnl in self.__store['channel'])
    
    def has_user_id(self, id):
        return any(id == usr.id for usr in self.__store['users'])
        
print('Loading Datastore...')

global data_store
data_store = Datastore()