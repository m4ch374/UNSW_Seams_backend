from src.data_store import data_store
from src.objecs import User

def user_join_ch(u_id):
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.channels += 1
    data_store.set(store)

def user_join_dm(u_id):
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.dms += 1
    data_store.set(store)

def user_sent_msg(u_id):
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.messages += 1
    data_store.set(store)

def user_leave_ch(u_id):
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.channels -= 1
    data_store.set(store)

def user_leave_dm(u_id):
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.dms -= 1
    data_store.set(store)

def user_remove_msg(u_id):
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.messages -= 1
    data_store.set(store)