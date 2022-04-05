from src.data_store import data_store
from src.objecs import User
from src.time import get_time


def user_join_ch(u_id):
    time = get_time()
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.channels += 1
            user.ch_list.append({'num_channels_joined': user.channels, 'time_stamp': time})
    data_store.set(store)

def user_join_dm(u_id):
    time = get_time()
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.dms += 1
            user.dm_list.append({'num_dms_joined': user.dms, 'time_stamp': time})
    data_store.set(store)

def user_sent_msg(u_id):
    time = get_time()
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.messages += 1
            user.mg_list.append({'num_messages_sent': user.messages, 'time_stamp': time})
    data_store.set(store)

def user_leave_ch(u_id):
    time = get_time()
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.channels -= 1
            user.ch_list.append({'num_channels_joined': user.channels, 'time_stamp': time})
    data_store.set(store)

def user_leave_dm(u_id):
    time = get_time()
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.dms -= 1
            user.dm_list.append({'num_dms_joined': user.dms, 'time_stamp': time})
    data_store.set(store)

def user_remove_msg(u_id):
    time = get_time()
    store = data_store.get()
    for user in store['users']:
        if user.id == u_id:
            user.messages -= 1
            user.mg_list.append({'num_messages_sent': user.messages, 'time_stamp': time})
    data_store.set(store)

def add_ch():
    time = get_time()
    store = data_store.get()
    store['stats_list']['chs_num'] += 1
    store['stats_list']['chs_list'].append({'num_channels_exist': store['stats_list']['chs_num'], 'time_stamp': time})
    data_store.set(store)

def add_dm():
    time = get_time()
    store = data_store.get()
    store['stats_list']['dms_num'] += 1
    store['stats_list']['dms_list'].append({'num_dms_exist': store['stats_list']['dms_num'], 'time_stamp': time})
    data_store.set(store)

def add_msg():
    time = get_time()
    store = data_store.get()
    store['stats_list']['msg_num'] += 1
    store['stats_list']['msg_list'].append({'num_messages_exist': store['stats_list']['msg_num'], 'time_stamp': time})
    data_store.set(store)

def remove_dm():
    time = get_time()
    store = data_store.get()
    store['stats_list']['dms_num'] -= 1
    store['stats_list']['dms_list'].append({'num_dms_exist': store['stats_list']['dms_num'], 'time_stamp': time})
    data_store.set(store)

def remove_msg():
    time = get_time()
    store = data_store.get()
    store['stats_list']['msg_num'] -= 1
    store['stats_list']['msg_list'].append({'num_messages_exist': store['stats_list']['msg_num'], 'time_stamp': time})
    data_store.set(store)

def cal_involvement_rate(chs, dms ,mgs):
    store = data_store.get()
    sum = store['stats_list']['chs_num'] + store['stats_list']['dms_num'] + store['stats_list']['msg_num']
    if sum == 0:
        return float(0)
    ir = (chs + dms + mgs) / sum
    return float(1) if ir > 1 else float(ir)

def cal_utilization_rate():
    store = data_store.get()
    users = 0
    for user in store['users']:
        if not user.removed:
            users += 1
    last_ch_id = store['last_used_id']['channel']
    last_ch_users = 0
    for ch in store['channel']:
        if ch.id == last_ch_id:
            last_ch_users = len(ch.members)
    for dm in store['dm']:
        if dm.id == last_ch_id:
            last_ch_users = len(dm.members)
    ur = last_ch_users / users
    return float(ur)

