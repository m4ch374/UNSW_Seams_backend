from src.data_store import data_store


def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channel'] = []
    store['dm'] = []
    store['tokens'] = []
    store['messages'] = []
    data_store.set(store)
