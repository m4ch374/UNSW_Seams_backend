import pytest
from src.error import InputError, AccessError

from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1, channels_list_v1
from src.auth import auth_register_v1

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
def test_channel_details_invalid_channel_id(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(InputError):
        assert channel_details_v1(user, channel + 1)

# Test invalid user id where id doesn't exist yet
def test_channel_details_invalid_user_id(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(AccessError):
        assert channel_details_v1(user + 1, channel)

# Test invalid user access permissions
def test_channel_details_invalid_access(first_user_and_channel):
    channel = first_user_and_channel['first_channel_id']
    second_user = auth_register_v1('z5555551@ad.unsw.edu.au', '123456b', 'Brian', 'Smith')['auth_user_id']
    
    with pytest.raises(AccessError):
        assert channel_details_v1(second_user, channel)

# Test that AccessError is raised when both user and channel ids are invalid
def test_channel_details_invalid_channel_and_user(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    with pytest.raises(AccessError):
        assert channel_details_v1(user + 1, channel + 1)

# Test that correct channel details are returned when all inputs valid
def test_channel_details_simple(first_user_and_channel):
    user = first_user_and_channel['first_user_id']
    channel = first_user_and_channel['first_channel_id']

    assert channel_details_v1(user, channel) == {'name': 'Ant', 'is_public': True, 
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

# helper function that clears data already stored and initialises a user for
# testing (returns id of created user)
def create_new_user_z1234567():
    auth_user_id = auth_register_v1('z1234567@ad.unsw.edu.au',
                                    'password',
                                    'firstname',
                                    'lastname')
    return auth_user_id

# helper function that initialises 2nd user for testing
def create_new_user_z1111111():
    auth_user_id = auth_register_v1('z1111111@ad.unsw.edu.au',
                                    'ypspspsp',
                                    'firstname',
                                    'lastname')
    return auth_user_id
# helper function that initialises 3rd user for testing
def create_new_user_z3141592():
    auth_user_id = auth_register_v1('z3141592@ad.unsw.edu.au',
                                    'potatopotato',
                                    'firstname',
                                    'lastname')
    return auth_user_id
# helper function that creates a public channel called 'First channel '
# Argument: auth_user_id (dictionary), is_public (boolean)
# Returns the id (int) of created channel
def create_first_channel(auth_user_id, is_public):
    channel_id = channels_create_v1(auth_user_id['auth_user_id'],
                                   'First Channel',
                                    is_public)
    return channel_id
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
    # Since no channels or id's have been created yet, any arbritary integer 
    # passed to the function should be considered invalid
    invalid_channel_id = -100
    invalid_auth_user_id = -100
    with pytest.raises(AccessError):
        channel_join_v1(invalid_auth_user_id, invalid_channel_id)

# raise InputError since channel_id does not refer to a valid channel
#
# note: this is because no valid channels have been created
def test_invalid_channel_id_for_channel_join():
    auth_user_id = create_new_user_z1234567()
    invalid_channel_id = -100
    with pytest.raises(InputError):
        channel_join_v1(auth_user_id['auth_user_id'], invalid_channel_id)

# add an authorised user to a created channel with no errors
def test_channel_join_valid_1():
    auth_user_id = create_new_user_z1234567()
    channel_id = create_first_channel(auth_user_id, True)
    auth_user_id2 = create_new_user_z1111111()
    channel_join_v1(auth_user_id2['auth_user_id'], channel_id['channel_id'])
    correct_output = {'channels': [{'channel_id': channel_id['channel_id'],
                                    'name': 'First Channel'}]}
    assert channels_list_v1(auth_user_id['auth_user_id']) == correct_output
    
# add several authorised users to a created channel with no errors
def test_channel_join_valid_2():
    auth_user_id = create_new_user_z1234567()
    channel_id = create_first_channel(auth_user_id, True)
    
    auth_user_id2 = create_new_user_z1111111()
    auth_user_id3 = create_new_user_z3141592()
    channel_join_v1(auth_user_id2['auth_user_id'], channel_id['channel_id'])
    channel_join_v1(auth_user_id3['auth_user_id'], channel_id['channel_id'])
    
    int_channel_id = channel_id['channel_id']
    correct_output_user = {'channels': [{'channel_id': int_channel_id,
                                         'name': 'First Channel'}]}
    assert channels_list_v1(auth_user_id2['auth_user_id']) == correct_output_user
    assert channels_list_v1(auth_user_id3['auth_user_id']) == correct_output_user

# raise InputError since the auth user being joined is already the only
# member of the channel
def test_channel_join_user_already_member():
    auth_user_id = create_new_user_z1234567()
    channel_id = create_first_channel(auth_user_id, True)
    with pytest.raises(InputError):
        channel_join_v1(auth_user_id['auth_user_id'], channel_id['channel_id'])
    
# raise AccessError since channel_id refers to private channel, auth 
# user is not part of channel and member is not global owner
def test_channel_raise_access_error():
    auth_user_id = create_new_user_z1234567()
    channel_id = create_first_channel(auth_user_id, False)
    auth_user_id2 = create_new_user_z1111111()
    
    with pytest.raises(AccessError):
        channel_join_v1(auth_user_id2['auth_user_id'], channel_id['channel_id'])

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
# note: while the invalid u_id & channel id's passed should raise
#       InputErrors on their own, the AccessError takes precedent
def test_invalid_auth_user_id_for_channel_invite():
    invalid_channel_id = -100
    invalid_auth_user_id = -100
    invalid_u_id = -100
    with pytest.raises(AccessError):
        channel_invite_v1(invalid_auth_user_id, invalid_channel_id,
                          invalid_u_id)

# raise InputError since invalid channel_id and invalid_u_id passed
def test_invalid_channel_and_u_id_for_channel_invite():
    auth_user_id = create_new_user_z1234567()
    invalid_u_id = -100  
    invalid_channel_id = -100
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id['auth_user_id'], invalid_channel_id,
                          invalid_u_id)

# raise InputError since invalid channel_id passed
#
# note: the auth_ser_id and u_id passed are both valid
def test_invalid_channel_id_for_channel_invite():
    auth_user_id = create_new_user_z1234567()
    u_id = create_new_user_z1111111()
    invalid_channel_id = -100
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id['auth_user_id'], invalid_channel_id,
                          u_id['auth_user_id'])

# raise InputError since invalid u_id passed
#
# note: the auth_user_id and channel_id passed are both valid
def test_invalid_u_id_for_channel_invite():
    auth_user_id = create_new_user_z1234567()
    channel_id = create_first_channel(auth_user_id, True)
    invalid_u_id = -100
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id['auth_user_id'], 
                          channel_id['channel_id'], invalid_u_id)

# raise InputError since u_id refers to user already a member of the channel
def test_already_a_member_channel_invite_1():
    auth_user_id = create_new_user_z1234567()
    channel_id = create_first_channel(auth_user_id, True)
    u_id = create_new_user_z1111111()
    channel_invite_v1(auth_user_id['auth_user_id'],
                      channel_id['channel_id'],
                      u_id['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v1(auth_user_id['auth_user_id'], 
                          channel_id['channel_id'],
                          u_id['auth_user_id'])

# raise AccessError since authorised user is not a member of the channel
def test_auth_user_not_in_channel_for_channel_invite():
    auth_user_id = create_new_user_z1234567()
    channel_id = create_first_channel(auth_user_id, True)
    auth_user_id2 = create_new_user_z3141592()
    u_id = create_new_user_z1111111()
    with pytest.raises(AccessError):
        channel_invite_v1(auth_user_id2['auth_user_id'], 
                          channel_id['channel_id'],
                          u_id['auth_user_id'])

# invite a user to a public channel with no errors
def test_public_channel_for_channel_invite():
    auth_user_id = create_new_user_z1234567()
    channel_id = create_first_channel(auth_user_id, True)
    u_id = create_new_user_z1111111()
    channel_invite_v1(auth_user_id['auth_user_id'], channel_id['channel_id'],
                      u_id['auth_user_id'])
    int_channel_id = channel_id['channel_id']
    correct_output = {'channels': [{'channel_id': int_channel_id, 
                                     'name': 'First Channel'}]}
    assert channels_list_v1(u_id['auth_user_id']) == correct_output

# invite a user to a private channel with no errors
def test_private_channel_for_channel_invite():
    auth_user_id = create_new_user_z1234567()
    channel_id = create_first_channel(auth_user_id, False)
    u_id = create_new_user_z1111111()
    channel_invite_v1(auth_user_id['auth_user_id'], channel_id['channel_id'],
                      u_id['auth_user_id'])
    int_channel_id = channel_id['channel_id']
    correct_output = {'channels': [{'channel_id': int_channel_id, 
                                     'name': 'First Channel'}]}
    assert channels_list_v1(u_id['auth_user_id']) == correct_output
