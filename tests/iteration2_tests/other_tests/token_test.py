"""
This file test for the behaviours of token

Will be in WHITEBOX mode until some important
component of iteration 2 is finished
"""

import pytest
from src.data_store import data_store

# Make sure token generated is in data_store
def test_generate_token():
    token = data_store.generate_token(1)

    assert token in data_store.get()['tokens']

# Should raise error
def test_get_id_from_token_error():
    with pytest.raises(Exception):
        data_store.get_id_from_token('invalidToken')

# Test the behaviours of method get_id_from_token()
def test_get_id_from_token():
    tok1 = data_store.generate_token(1)
    tok2 = data_store.generate_token(2)

    assert data_store.get_id_from_token(tok1) == 1
    assert data_store.get_id_from_token(tok2) == 2

# Should raise error 
def test_remove_token_error():
    with pytest.raises(Exception):
        data_store.remove_token('invalidToken')

# Test the behaviours of method remove_token
def test_remove_token():
    tok1 = data_store.generate_token(1)
    tok2 = data_store.generate_token(2)

    data_store.remove_token(tok2)

    assert data_store.is_valid_token(tok1)
    assert not data_store.is_valid_token(tok2)
