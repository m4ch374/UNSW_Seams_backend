import requests, time, imaplib, email
from tests.iteration3_tests.user_tests.definitions import REGISTER_V2, AUTH_PASSWORDRESET_RESET_V1, AUTH_PASSWORDRESET_REQUEST_V1
from src.config import SERVER_EMAIL, SERVER_PASSWORD


def get_code():
    server = imaplib.IMAP4_SSL("imap.gmail.com")
    server.login(SERVER_EMAIL, SERVER_PASSWORD)
    _ = server.select("INBOX")
    _, data = server.search(None, "ALL")
    msgList = data[0].split()
    latest = msgList[len(msgList) - 1]
    _, datas = server.fetch(latest, '(RFC822)')
    text = datas[0][1].decode('utf8')
    message = email.message_from_string(text)
    msglist = str(message).split('\n')
    msgline = [line for line in msglist if 'Your reset code is:' in line]
    return msgline[0][22:27]

def test_invalid_reset_code():
    requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(AUTH_PASSWORDRESET_REQUEST_V1, json = {'email': 'z8888888@ed.unsw.edu.au'})
    response = requests.post(AUTH_PASSWORDRESET_RESET_V1, json = {'reset_code': '123', 'new_password': '1234567'})
    assert response.status_code == 400

def test_short_password():
    requests.post(REGISTER_V2, json = {'email': SERVER_EMAIL, 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(AUTH_PASSWORDRESET_REQUEST_V1, json = {'email': SERVER_EMAIL})
    time.sleep(5)
    reset_code = get_code()
    response = requests.post(AUTH_PASSWORDRESET_RESET_V1, json = {'reset_code': reset_code, 'new_password': '123'})
    assert response.status_code == 400

def test_valid_input():
    requests.post(REGISTER_V2, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(REGISTER_V2, json = {'email': SERVER_EMAIL, 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(AUTH_PASSWORDRESET_REQUEST_V1, json = {'email': SERVER_EMAIL})
    time.sleep(5)
    reset_code = get_code()
    response = requests.post(AUTH_PASSWORDRESET_RESET_V1, json = {'reset_code': reset_code, 'new_password': '123456'})
    assert response.status_code == 200
    assert response.json() == {}

