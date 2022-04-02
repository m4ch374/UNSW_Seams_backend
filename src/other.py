from src.data_store import data_store
import os

def clear_v1():
    # delete the jpg file made by tests
    for i in range(data_store.get()['last_used_id']['users'] + 1):
        f = f"images/{i}.jpg"
        if os.path.exists(f):
            os.remove(f)

    clearted_data = {
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
        'reset_code': {},
    }
    data_store.set(clearted_data)

