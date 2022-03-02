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

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users' : [], 
    'channel' : [],
} # credit to Hanqi for this placeholder love you <3

## YOU SHOULD MODIFY THIS OBJECT ABOVE

## YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH
class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

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

print('Loading Datastore...')

global data_store
data_store = Datastore()
