import pytest
from src.error import InputError, AccessError

from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.auth import auth_register_v1
# from tests.channels_test import another_id

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

# raise AccessError since invalid auth_user_id passed to function
#
# note: channel_id passed is also invalid (since no channels yet created)
def test_invalid_user_id_for_channel_details():
    clear_v1()
    invalid_channel_id = {'channel_id': -100}
    invalid_auth_user_id = {'auth_user_id': -100}
    with pytest.raises(AccessError):
        channel_details_v1(invalid_auth_user_id['auth_user_id'], invalid_channel_id['channel_id'])

# raise InputError since invalid channel_id passed
#
# note: one valid auth_id_is_created (but no channels)
def test_invalid_channel_id_channel_details():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    invalid_channel_id = {'channel_id': -100}
    with pytest.raises(InputError):
        channel_details_v1(auth_user_id['auth_user_id'], invalid_channel_id['channel_id'])

# raise InputError since channel_id passed doesn't match channel created
def test_channel_id_doesnt_match_valid_channel_1():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    valid_channel_id = channels_create_v1(auth_user_id['auth_user_id'], 'First Channel', True)
    
    invalid_channel_id = {'channel_id': -100}
    with pytest.raises(InputError):
        channel_details_v1(auth_user_id['auth_user_id'], invalid_channel_id['channel_id'])

# raise InputError since channel_id passed doesn't match any of channels created
def test_channel_id_doesnt_match_valid_channel_2():
    clear_v1()
    auth_user_id1 = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id1 = channels_create_v1(auth_user_id1['auth_user_id'], 'First Channel', True)
    auth_user_id2 = auth_register_v1('z7654321@ad.unsw.edu.au', 'password', 'dog', 'chicken');
    valid_channel_id2 = channels_create_v1(auth_user_id2['auth_user_id'], 'Second Channel', True)
    auth_user_id3 = auth_register_v1('z3141592@ad.unsw.edu.au', 'potatopotato', 'firstname', 'lastname');
    valid_channel_id3 = channels_create_v1(auth_user_id3['auth_user_id'], 'Third Channel', False)
    
    # create a channel id that doesn't match any of the created channels
    invalid_channel_id = {'channel_id': -100}
    with pytest.raises(InputError):
        channel_details_v1(auth_user_id1['auth_user_id'], invalid_channel_id['channel_id'])
    

# create a single private channel and list details with no errors
def test_valid_channel_details_1():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id = channels_create_v1(auth_user_id['auth_user_id'], 'First Channel', True)
    assert channel_details_v1(auth_user_id['auth_user_id'], valid_channel_id['channel_id']) == {'name': 'First Channel', 'is_public': True}

# create a single public channel and list details with no errors
def test_valid_channel_details_2():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id = channels_create_v1(auth_user_id, 'First Channel', False)
    assert channel_details_v1(auth_user_id['auth_user_id'], valid_channel_id['channel_id']) == {'name': 'First Channel', 'is_public': False}

# create several channels and list details with no errors
def test_valid_channel_details_3():
    clear_v1()
    auth_user_id1 = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id1 = channels_create_v1(auth_user_id1['auth_user_id'], 'First Channel', True)
    
    auth_user_id2 = auth_register_v1('z7654321@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id2 = channels_create_v1(auth_user_id2['auth_user_id'], 'Second Channel', False)
    
    assert channel_details_v1(auth_user_id1['auth_user_id'], valid_channel_id1['channel_id']) == {'name': 'First Channel', 'is_public': True}
    assert channel_details_v1(auth_user_id2['auth_user_id'], valid_channel_id2['channel_id']) == {'name': 'Second Channel', 'is_public': True}

# add a person to channel via join function, and correctly list channel details
    clear_v1()
    auth_user_id1 = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname');
    valid_channel_id1 = channels_create_v1(auth_user_id1['auth_user_id'], 'First Channel', True)
    
    auth_user_id2 = auth_register_v1('z1111111@ad.unsw.edu.au', 'ypspspsp', 'firstname', 'lastname');
    channel_join_v1(auth_user_id2['auth_user_id'], valid_channel_id['channel_id'])
    
    assert channel_details_v1(auth_user_id2, valid_channel_id1) == {'name': 'First Channel', 'is_public': True}
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
# note: while the invalid channel id passed should raise
#       InputError on their own, the AccessError takes precedent
def test_invalid_user_id_for_channel_join():
    clear_v1()
    invalid_channel_id = {'channel_id': -100}
    invalid_auth_user_id = {'auth_user_id': -100}
    with pytest.raises(AccessError):
        channel_join_v1(invalid_auth_user_id['auth_user_id'], invalid_channel_id['channel_id'])

# raise InputError since channel_id does not refer to a valid channel
#
# note: this is because no valid channels have been created
def test_invalid_channel_id_for_channel_join():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    invalid_channel_id = {'channel_id': -100}
    with pytest.raises(InputError):
        channel_join_v1(auth_user_id['auth_user_id'], invalid_channel_id['channel_id'])

# add an authorised user to a created channel with no errors
#
#
def test_channel_join_valid_1():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    valid_channel_id = channels_create_v1(auth_user_id['auth_user_id'], 'First Channel', True)
    '''
    auth_user_id2 = auth_register_v1('z1111111@ad.unsw.edu.au', 'ypspspsp', 'firstname', 'lastname');
    
    channel_join_v1(auth_user_id2['auth_user_id'], valid_channel_id['channel_id'])
    channel_details_1 = channel_details_v1(auth_user_id['auth_user_id'], valid_channel_id['channel_id'])
    '''
    # assert channel_details_1['all_members'][1]['u_id'] == auth_user_id2['auth_user_id']

# raise InputError since the auth user being joined is already the only
# member of the channel
# 
def test_channel_join_user_already_member_1():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    valid_channel_id = channels_create_v1(auth_user_id['auth_user_id'], 'First Channel', True)
    
    with pytest.raises(InputError):
        channel_join_v1(auth_user_id['auth_user_id'], valid_channel_id['channel_id'])
    
# raise AccessError since channel_id refers to private channel, auth 
#   user is not part of channel and member is not global owner
#
def test_channel_raise_access_error():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    valid_channel_id = channels_create_v1(auth_user_id['auth_user_id'], 'First Channel', False)
    auth_user_id2 = auth_register_v1('z1111111@ad.unsw.edu.au', 'ypspspsp', 'firstname', 'lastname');
    
    with pytest.raises(AccessError):
        channel_join_v1(auth_user_id2['auth_user_id'], valid_channel_id['channel_id'])
    
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

