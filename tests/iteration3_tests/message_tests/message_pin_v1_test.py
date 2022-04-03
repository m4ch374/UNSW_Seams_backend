'''
##############################################################################
##                     Tests for message/pin/v1                              #
##############################################################################

# Expected error behaviour:
# InputError when:
#   - message_id is not a valid message within a channel or DM that the 
#     authorised user has joined
#   - the message is already pinned
# AccessError when:
#   - message_id refers to a valid message in a joined channel/DM and the 
#     authorised user does not have owner permissions in the channel/DM
# =============================================================================
'''
# imports used








