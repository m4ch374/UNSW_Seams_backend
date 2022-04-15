from src.data_store import data_store
import os

def clear_v1():
    # delete the jpg file made by tests
    for i in range(data_store.get()['last_used_id']['users'] + 1):
        f = f"src/static/{i}.jpg"
        if os.path.exists(f):
            os.remove(f)

    data_store.get_store()

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
        'stats_list': {
            'chs_num': 0,
            'dms_num': 0,
            'msg_num': 0,
            'chs_list': [],
            'dms_list': [],
            'msg_list': [],
        },
    }
    data_store.set(clearted_data)
