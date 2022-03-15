# import requests

# BASE_ADDRESS = 'http://localhost:'
# BASE_PORT = '20000'
# BASE_URL = BASE_ADDRESS + BASE_PORT
# REQUEST = "/user/profile/setname/v1"
# URL = BASE_URL + REQUEST
# REGISTER = BASE_URL + "/auth/register/v2"

# def test_invalid_token():
#     response = requests.post(URL, json = {'token': '123123123123123', 'name_first': 'James', 'name_last': 'Bond'})
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data == None

# def test_long_name():
#     long_name = 'x' * 51
#     user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
#     user_data = user.json()
#     response = requests.post(URL, json = {'token': user_data['token'], 'name_first': long_name, 'name_last': 'Bond'})
#     assert response.status_code == 400
#     response = requests.post(URL, json = {'token': user_data['token'], 'name_first': 'James', 'name_last': long_name})
#     assert response.status_code == 400

# def test_short_name():
#     short_name = ''
#     user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
#     user_data = user.json()
#     response = requests.post(URL, json = {'token': user_data['token'], 'name_first': short_name, 'name_last': 'Bond'})
#     assert response.status_code == 400
#     response = requests.post(URL, json = {'token': user_data['token'], 'name_first': 'James', 'name_last': short_name})
#     assert response.status_code == 400

# def test_valid_input():
#     user = requests.post(REGISTER, json = {'email': 'z5555555@ed.unsw.edu.au', 'password': '1234567', 'name_first': 'William', 'name_last': 'Wu'})
#     user_data = user.json()
#     response = requests.post(URL, json = {'token': user_data['token'], 'name_first': 'James', 'name_last': 'Bond'})
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data == {}

