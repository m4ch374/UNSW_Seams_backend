# import pytest

# from src.other import clear_v1
# import src.auth as auth
# from src.channels import channels_create_v1
# from src.channel import channel_details_v1

# USR1_CRED = {'email': 'z7654321@ed.unsw.edu.au', 'password': '1234567'}
# USR2_CRED = {'email': 'z5555555@ed.unsw.edu.au', 'password': '123123123'}

# def test_cleared():
#     user1 = auth.auth_register_v1(USR1_CRED['email'], USR1_CRED['password'], 'Jason', 'Smith')['auth_user_id']
#     user2 = auth.auth_register_v1(USR2_CRED['email'], USR2_CRED['password'], 'William', 'Wu')['auth_user_id']

#     chnl1 = channels_create_v1(user1, "COMP1521", True)['channel_id']
#     chnl2 = channels_create_v1(user2, 'Ant', False)['channel_id']

#     clear_v1()

#     # If it raises error, it means there are no entries with the id
#     # in data_store
#     with pytest.raises(Exception):
#         auth.auth_login_v1(USR1_CRED['email'], USR1_CRED['password'])
#         auth.auth_login_v1(USR2_CRED['email'], USR2_CRED['password'])

#         channel_details_v1(user1, chnl1)
#         channel_details_v1(user2, chnl2)
