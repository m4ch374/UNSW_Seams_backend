"""This file encode the password
    example:
    password:           -------------------------------------------------------------------
    selted_password:    k--f--y--u--s--r--e--1--d--f--6--g--6--8--s--e--r--d--s--f--3--2--g--1--8--5--a--w--e--9--6--1--a--3-
    encode_password:    b'k--f--y--u--s--r--e--1--d--f--6--g--6--8--s--e--r--d--s--f--3--2--g--1--8--5--a--w--e--9--6--1--a--3-'
    hashed_password:    a2bef8ef61b1818af4e4c28fc008d69ab6f77f443bf58a04948cac54f2143525
"""

import hashlib
from src.config import PASSWORD_SECRET as SALT

PERIOD = 2
RANDOM_STR = 'ja13rt54v3er51ge6vt8'

"""
Input:
    password (str)

Process:
    Add random string if password length is less than 10.
    Insert random character to the password for every two characters in the password
    Encrypt with sha256

Return value:
    Encrypted password (str)
"""
def hashing_password(password):
    if len(password) < 10:
        password += RANDOM_STR
    selted_password = ''
    idx = 0
    for i in range(len(password)):
        if i % PERIOD == 0:
            selted_password += SALT[idx]
            if idx == len(SALT) - 1:
                idx = 0
            else:
                idx += 1
        selted_password += password[i]
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

