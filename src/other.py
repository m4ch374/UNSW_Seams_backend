from src.data_store import data_store


def clear_v1():
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
    }
    data_store.set(clearted_data)
