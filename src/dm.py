"""
This file contains function for the domain
/dm
"""

# Imports
from src.data_store import data_store
from src.error import InputError, AccessError
from src.objecs import DmChannel

# =================== helpers ======================
def check_valid_dm_id(dm_id):
    if not data_store.has_dm_id(dm_id):
        raise InputError(description="error: Invalid dm id.")

def check_is_creator(dm_chnl, u_id):
    if not (dm_chnl.has_owner_id(u_id) and dm_chnl.has_member_id(u_id)):
        raise AccessError(description="error: ID is not the creator or no longer in DM.")

def check_is_member(dm_chnl, u_id):
    if not dm_chnl.has_member_id(u_id):
        raise AccessError(description="error: ID not a member of dm.")
# ==================================================

def dm_create_v1(u_id, u_ids):
    # Create dm channel
    dm_chnl = DmChannel(data_store.get_user(u_id), u_ids)
    data_store.add_dm(dm_chnl)

    return {'dm_id': dm_chnl.id}

def dm_list_v1(u_id):
    dms = [dm.channel_dict() for dm in data_store.get()['dm'] if dm.has_member_id(u_id)]

    return {'dms': dms}

def dm_remove_v1(u_id, dm_id):
    check_valid_dm_id(dm_id)

    dm_chnl = data_store.get_dm(dm_id)
    
    check_is_creator(dm_chnl, u_id)

    data_store.remove_dm(dm_chnl)
    return {}

def dm_details_v1(u_id, dm_id):
    check_valid_dm_id(dm_id)

    dm_chnl = data_store.get_dm(dm_id)
    
    check_is_member(dm_chnl, u_id)

    return dm_chnl.channel_details_dict()

def dm_leave_v1(u_id, dm_id):
    check_valid_dm_id(dm_id)
    
    dm_chnl = data_store.get_dm(dm_id)
    
    check_is_member(dm_chnl, u_id)

    dm_chnl.remove_member_id(u_id)
    return {}

# Commented for coverage
# def dm_messages_v1(u_id, dm_id, start):
#     return {}
