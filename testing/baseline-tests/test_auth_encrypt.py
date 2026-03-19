"""
Baseline test  for _encrypt function in auth module

Baseline Rules:
- 1 happy Path 
- 1 invalid input
- 1 boundary / guard caase 

- Only expected behavior pluse simple error handling
- No CFG Reasoning
- No path targeting
- 3-4 test max
"""
import pytest
from app.routes.auth import _encrypt # import encryption function

# one valid test case for each type
# one invalid test case for each type
# one boundary guard test case for each type

# Test 1 : Happy Path- valid ascii input with positive shift
def test_encrypt_valid_simple_case():
    result = _encrypt("mypassword", 1,1) # shift forward by 1
    
    # expected behavior
    assert isinstance(result, str) # output should be a string
    assert len(result) == 10 # length sb the same
    
# Test 2: non-ASCII should raise TypeError Invalid input
def test_encrypt_non_ascii_input_raise_type_error():
    try:
        _encrypt("mypasswordé", 1, 1) # contains é which is non-ASCII
        assert False # should not reach
    except TypeError:
        assert True # expected exception
        

# Test 3 : Boundary Guard :num_shift < 1 should raise ValueError
def test_encrypt_invalid_shift_raises_value_error():
    try:
        _encrypt("mypassword", 0, 1) # shift of 0 is invalid
        assert False # should not reach
    except ValueError:
        assert True # expected exception

# test 4 : Valid input with special character 
def test_encrypt_allows_special_characters():
    result = _encrypt("my_password$", 1, 1) # $ is allowed
    assert isinstance(result, str) # output should be a string
    assert len(result) == len("my_password$") # length should be the same as input

# notes : 
# Observed behavior : the system dos not enforce forbidden characters , this contradict my
# assumptions - this is a verifiable discrepancy 

