"""
A test on data persistence

Test is in WHITEBOX format
since `clear_v1()` will also wipe the data stored in file 
or its just that im not smart enough
"""

from src.auth import auth_register_v1
from src.channels import channels_create_v1

from src.data_store import Datastore, data_store

def test_persistent():
    # Add user to data
    usr1 = auth_register_v1('email@gmail.com', '123456', 'joe', 'bidome')['auth_user_id']
    usr2 = auth_register_v1('another@gmail.com', '132435', 'obama', 'prism')['auth_user_id']

    # Add channels
    channels_create_v1(usr1, 'name', True)['channel_id']
    channels_create_v1(usr2, 'another', True)['channel_id']

    # Create new Datastore object, if data is not persistent,
    # get() method should only return initial object
    new_datastore = Datastore()
    data = new_datastore.get()

    # check if both users and channels have the same attributes
    assert [usr.to_dict() for usr in data_store.get()['users']] == [usr.to_dict() for usr in data['users']]
    assert ([chnl.channel_details_dict() for chnl in data_store.get()['channel']] == 
        [chnl.channel_details_dict() for chnl in data['channel']])

    # Ensure they are not objects with the same pointer
    assert new_datastore != data_store

def test_inconsistent():
    # Add user to data
    usr1 = auth_register_v1('email@gmail.com', '123456', 'joe', 'bidome')['auth_user_id']

    # change user data without saving
    data_store.get()['users'][0].name_first = "another"

    # get data from file
    new_datastore = Datastore()
    data = new_datastore.get()

    assert data['users'][0].name_first != "another"

    # Ensure they are not objects with the same pointer
    assert new_datastore != data_store
