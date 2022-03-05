from re import A
import pytest
from src.error import InputError, AccessError

from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.auth import auth_register_v1

from src.other import clear_v1
from src.data_store import data_store


# Registers user 1 and has them create channel 1
@pytest.fixture
def initialise_user_and_channel():
    clear_v1()
    auth_register_v1('z5555555@ad.unsw.edu.au', '123456a', 'Anthony', 'Smith')
    channels_create_v1(1, 'Ant', 'y')


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
#user, channel

# Test invalid channel id where id doesn't exist yet
def test_channel_details_invalid_channel_id(initialise_user_and_channel):
    with pytest.raises(InputError):
        assert channel_details_v1(1, 2)

# Test invalid user id where id doesn't exist yet
def test_channel_details_invalid_user_id(initialise_user_and_channel):
    with pytest.raises(AccessError):
        assert channel_details_v1(2, 1)

# Test invalid user access permissions
def test_channel_details_invalid_access(initialise_user_and_channel):
    auth_register_v1('z5222222@ad.unsw.edu.au', 'abcde123', 'Brian', 'Smith')
    with pytest.raises(AccessError):
        assert channel_details_v1(2, 1)

# Test that AccessError is raised when both user and channel ids are invalid
def test_channel_details_invalid_channel_and_user(initialise_user_and_channel):
    with pytest.raises(AccessError):
        assert channel_details_v1(2, 2)

# Test that correct channel details are returned when all inputs valid
def test_channel_details_simple(initialise_user_and_channel):
    assert channel_details_v1(1, 1) == {'name': 'Ant', 'is_public': 'y', 
    'owner_members': [{'email': 'z5555555@ad.unsw.edu.au',
                       'handle_str': 'anthonysmith',
                       'name_first': 'Anthony',
                       'name_last': 'Smith',
                       'u_id': 1}], 
    'all_members': [{'email': 'z5555555@ad.unsw.edu.au',
                     'handle_str': 'anthonysmith',
                     'name_first': 'Anthony',
                     'name_last': 'Smith',
                     'u_id': 1}],
    }

#########################################

# add an authorised user to a created channel with no errors
#
# 
def test_channel_join_valid_1():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    valid_channel_id = channels_create_v1(auth_user_id['auth_user_id'], 'First Channel', True)
    auth_user_id2 = auth_register_v1('z1111111@ad.unsw.edu.au', 'ypspspsp', 'firstname', 'lastname')
    
    channel_join_v1(auth_user_id2['auth_user_id'], valid_channel_id['channel_id'])
    assert channels_listall_v1(auth_user_id['auth_user_id']) == {'channels': [{'channel_id': 1, 'name': 'First Channel'}]}
    
# add several authorised users to a created channel with no errors
#
# 
def test_channel_join_valid_2():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    valid_channel_id = channels_create_v1(auth_user_id['auth_user_id'], 'First Channel', True)
    
    auth_user_id2 = auth_register_v1('z1111111@ad.unsw.edu.au', 'ypspspsp', 'firstname', 'lastname')
    auth_user_id3 = auth_register_v1('z3141592@ad.unsw.edu.au', 'potatopotato', 'firstname', 'lastname')
    
    channel_join_v1(auth_user_id2['auth_user_id'], valid_channel_id['channel_id'])
    channel_join_v1(auth_user_id3['auth_user_id'], valid_channel_id['channel_id'])
    
    assert channels_listall_v1(auth_user_id2['auth_user_id']) == {'channels': [{'channel_id': 1, 'name': 'First Channel'}]}
    assert channels_listall_v1(auth_user_id3['auth_user_id']) == {'channels': [{'channel_id': 1, 'name': 'First Channel'}]}
    
# add a user to several channels with no errors
#
#
def test_channel_join_valid_3():
    clear_v1()
    auth_user_id1 = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    valid_channel_id1 = channels_create_v1(auth_user_id1['auth_user_id'], 'First Channel', True)
    
    auth_user_id2 = auth_register_v1('z7654321@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    valid_channel_id2 = channels_create_v1(auth_user_id2['auth_user_id'], 'Second Channel', True)
    auth_user_id3 = auth_register_v1('z3141592@ad.unsw.edu.au', 'potatopotato', 'firstname', 'lastname')
    channel_join_v1(auth_user_id3['auth_user_id'], valid_channel_id1['channel_id'])
    channel_join_v1(auth_user_id3['auth_user_id'], valid_channel_id2['channel_id'])
    assert channels_listall_v1(auth_user_id3['auth_user_id']) == {'channels': [{'channel_id': 1, 'name': 'First Channel'}, {'channel_id': 2, 'name': 'Second Channel'}]}



###############################################################

# raise InputError since the auth user being joined is already the only
# member of the channel
# 
def test_channel_join_user_already_member_1():
    clear_v1()
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au', 'password', 'firstname', 'lastname')
    valid_channel_id = channels_create_v1(auth_user_id['auth_user_id'], 'First Channel', True)