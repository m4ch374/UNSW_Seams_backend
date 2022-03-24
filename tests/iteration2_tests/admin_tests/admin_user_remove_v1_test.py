'''
####################################################
##          Tests for admin/user/remove/v1        ##
####################################################

# Expected behaviour:
# InputError when:
#   - u_id does not refer to a valid user
#   - u_id refers to a user who is already a member of the channel
# AccessError when:
#   - channel_id is valid and the authorised user is not a member of the
#     channel
# ==================================================
'''

