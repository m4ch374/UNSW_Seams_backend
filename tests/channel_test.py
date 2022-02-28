import pytest
from src.error import InputError, AccessError

from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.auth import auth_register_v1
from tests.channels_test import another_id

from src.other import clear_v1
from src.data_store import data_store


####################################################
##          Tests for channel_details_v1          ##
####################################################
#
# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
# AccessError when:
#   - channel_id is valid and the authorised user is not a member of the
#     channel
# ==================================================

# raise AccessError since invalid auth_user_id passed
#
# note: channel_id passed is also invalid (since no channels yet created)
def test_invalid_user_id_for_channel_details():
    clear_v1()
    invalid_channel_id = -100
    invalid_auth_user_id = -100
    with pytest.raises(AccessError):
        channel_details_v1(invalid_auth_user_id, invalid_channel_id)

# raise InputError since invalid channel_id passed
#
# note: one valid auth_id_is_created
def test_invalid_channel_id():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    invalid_channel_id = -100
    with pytest.raises(InputError):
        channel_details_v1(auth_user_id, invalid_channel_id)

# raise InputError since channel_id passed doesn't match channel created
def test_channel_id_doesnt_match_valid_channel():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id = channels_create_v1(auth_user_id, 'First Channel', True)
    
    # purposely change the valid channel_id to get an invalid_channel_id
    invalid_channel_id = valid_channel_id + 100
    with pytest.raises(InputError):
        channel_details_v1(auth_user_id, invalid_channel_id)

'''
NOTE ADD MORE test_channel_id_doesnt_match_valid_channel functions here
# delete once resolved
'''

# create a single channel and list details with no errors
def test_valid_channel_details_1():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id = channels_create_v1(auth_user_id, 'First Channel', True)
    assert channel_details_v1(auth_user_id, valid_channel_id) == {'name': 'First Channel', 'is_public': True}
    
    '''
    NOTE : i dont know why but the function stub for channel_details_v1 doesnt 
    include the key 'is_public' in it's return, but the specifications say that
    it should
    # delete once resolved
    '''
# create several channels and list details with no errors
def test_valid_channel_details_2():
    clear_v1()
    auth_user_id1 = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id1 = channels_create_v1(auth_user_id1, 'First Channel', True)
    
    auth_user_id2 = auth_register_v1('z1234568@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id2 = channels_create_v1(auth_user_id2, 'Second Channel', True)
    
    assert channel_details_v1(auth_user_id1, valid_channel_id1) == {'name': 'First Channel', 'is_public': True}
    assert channel_details_v1(auth_user_id2, valid_channel_id2) == {'name': 'Second Channel', 'is_public': True}

####################################################
##          Tests for channel_join_v1             ##
####################################################
#
# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
#   - the authorised user is already a member of the channel
# AccessError when:
#   - channel_id refers to a channel that is private and the authorised
#     user is not already a channel member and is not a global owner
#
# ==================================================

# raise AccessError since invalid auth_user_id passed
#
# note: while the invalid auth_user & channel id's passed should raise
#       InputErrors on their own, the AccessError takes precedent
def test_invalid_user_id_for_channel_join():
    clear_v1()
    invalid_channel_id = -100
    invalid_auth_user_id = -100
    with pytest.raises(AccessError):
        channel_join_v1(invalid_auth_user_id, invalid_channel_id)

# 
#
#

####################################################
##          Tests for channel_invite_v1           ##
####################################################

# Expected behaviour:
# InputError when:
#   - channel_id does not refer to a valid channel
#   - u_id does not refer to a valid user
#   - u_id refers to a user who is already a member of the channel
# AccessError when:
#   - channel_id is valid and the authorised user is not a member of the
#     channel
# ==================================================

# raise AccessError since invalid auth_user_id passed
#
# note: while the invalid auth_user & channel id's passed should raise
#       InputErrors on their own, the AccessError takes precedent
def test_invalid_user_id_for_channel_invite():
    clear_v1()
    invalid_channel_id = -100
    invalid_auth_user_id = -100
    invalid_u_id = -100
    with pytest.raises(AccessError):
        channel_invite_v1(invalid_auth_user_id, invalid_channel_id,
                          invalid_u_id)

