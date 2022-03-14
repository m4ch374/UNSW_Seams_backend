"""
# ============= Channels create v2 =================
# This section tests for the endpoint
# /channels/create/v2
# ==================================================
"""

# Stubbed until necessary funtion is finished

# # Imports
# import requests

# # Import errors
# from src.error import InputError, AccessError

# # Import definitions
# from tests.iteration2_tests.channels_tests.definitions import ERROR_LIST, NAMES_LIST, INVALID_TOKEN
# from src.config import url

# # Local definitions
# ENDPOINT = f"{url}channels/create/v2"

# def generate_channel_input_json(tok, name, is_public):
#     return {
#         'token': tok,
#         'name': name,
#         'is_public': is_public,
#     }

# # Should raise input error
# #
# # When:     length of name < 1 ||
# #           Length of name > 20
# #
# # Test for creating public channels
# def test_channels_create_error_public(get_token_1):
#     for s in ERROR_LIST:
#         data = generate_channel_input_json(get_token_1, s, True)
#         resp = requests.post(ENDPOINT, data=data)

#         assert resp.status_code == InputError.code

# # Should raise input error
# #
# # When:     length of name < 1 ||
# #           Length of name > 20
# #
# # Test for creating private channels
# def test_channels_create_error_private(get_token_1):
#     for s in ERROR_LIST:
#         data = generate_channel_input_json(get_token_1, s, False)
#         resp = requests.post(ENDPOINT, data=data)

#         assert resp.status_code == InputError.code

# # Should raise input error
# #
# # When:     length of name < 1 ||
# #           Length of name > 20
# #
# # Test for creating both public and private channels
# def test_channels_create_error_pub_and_priv(get_token_1):
#     for s in ERROR_LIST:
#         data1 = generate_channel_input_json(get_token_1, s, True)
#         data2 = generate_channel_input_json(get_token_1, s, False)
#         resp1 = requests.post(ENDPOINT, data=data1)
#         resp2 = requests.post(ENDPOINT, data=data2)

#         assert resp1.status_code == InputError.code
#         assert resp2.status_code == InputError.code

# # Should raise access error
# #
# # When:     auth_user_id is invalid
# #
# # Test passing in invalid token
# def test_channels_create_error_invalid_token():
#     data = generate_channel_input_json(INVALID_TOKEN, 'dummy', True)
#     resp = requests.post(ENDPOINT, data=data)

#     assert resp.status_code == AccessError.code

# # Should not raise any error
# # 
# # Test for creating valid public channels
# def test_channels_create_public(get_token_1):
#     for i, name in enumerate(NAMES_LIST):
#         data = generate_channel_input_json(get_token_1, name, True)
#         val = requests.post(ENDPOINT, data=data).json()

#         assert val == { 'channel_id': i + 1 }

# # Should not raise any error
# # 
# # Test for creating valid private channels
# def test_channels_create_private(get_token_1):
#     for i, name in enumerate(NAMES_LIST):
#         data = generate_channel_input_json(get_token_1, name, False)
#         val = requests.post(ENDPOINT, data=data).json()

#         assert val == { 'channel_id': i + 1 }

# # Should not raise any error
# # 
# # Test for creating both valid public and private channels
# def test_channels_create_pub_and_priv(get_token_1):
#     for i, name in enumerate(NAMES_LIST):
#         data = generate_channel_input_json(get_token_1, name, True)
#         data_1 = generate_channel_input_json(get_token_1, name, False)
#         val = requests.post(ENDPOINT, data=data).json()
#         val_1 = requests.post(ENDPOINT, data=data_1).json()

#         assert val == { 'channel_id': i * 2 + 1 }
#         assert val_1 == { 'channel_id': i * 2 + 2 }
