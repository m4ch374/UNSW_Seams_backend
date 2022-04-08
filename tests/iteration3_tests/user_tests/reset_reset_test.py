import requests, time, imaplib, email
from tests.iteration3_tests.endpoints import ENDPOINT_REGISTER_USR, ENDOPINT_PWORD_RESET, ENDPOINT_PWORD_REQUEST
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
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(ENDPOINT_PWORD_REQUEST, json = {'email': 'z8888888@ed.unsw.edu.au'})
    response = requests.post(ENDOPINT_PWORD_RESET, json = {'reset_code': '123', 'new_password': '1234567'})
    assert response.status_code == 400

def test_short_password():
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': SERVER_EMAIL, 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(ENDPOINT_PWORD_REQUEST, json = {'email': SERVER_EMAIL})
    time.sleep(5)
    reset_code = get_code()
    response = requests.post(ENDOPINT_PWORD_RESET, json = {'reset_code': reset_code, 'new_password': '123'})
    assert response.status_code == 400

def test_valid_input():
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': 'z8888888@ed.unsw.edu.au', 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(ENDPOINT_REGISTER_USR, json = {'email': SERVER_EMAIL, 'password': '12345678', 'name_first': 'Russell', 'name_last': 'Wang'})
    requests.post(ENDPOINT_PWORD_REQUEST, json = {'email': SERVER_EMAIL})
    time.sleep(5)
    reset_code = get_code()
    response = requests.post(ENDOPINT_PWORD_RESET, json = {'reset_code': reset_code, 'new_password': '123456'})
    assert response.status_code == 200
    assert response.json() == {}

