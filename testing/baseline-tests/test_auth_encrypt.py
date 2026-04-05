# ============================================================
# Baseline Test Suite for _encrypt()
# Course: EE360T Software Testing
# ============================================================
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
    """
    T1 Happy Path: Valid ASCII input with positive shift
    Expected Behavior: 
    - Valid ASCII string is transformed by shifting characters 
    forward by num_shift positions
    
    """
    result = _encrypt("mypassword", 1,1) # shift forward by 1
    # expected behavior
    assert isinstance(result, str) # output should be a string
    assert len(result) == 10 # length should be the same
    
# Test 2: non-ASCII should raise TypeError Invalid input
def test_encrypt_non_ascii_input_raise_type_error():
    """
    T2: Invalid input
    
    Expected:
    - Non-ASCII characters should raise TypeError
    """
    try:
        _encrypt("mypasswordé", 1, 1) # contains é which is non-ASCII
        assert False # should not reach
    except TypeError:
        assert True # expected exception
        
    # Pytest version
    with pytest.raises(TypeError):
        _encrypt("mypasswordé", 1, 1)
        

# Test 3 : Boundary Guard :num_shift < 1 should raise ValueError
def test_encrypt_invalid_shift_raises_value_error():
    """
    T3: Boundary Condition
    Expected:
    - num_shift < 1 raises ValueError
    
    """
    try:
        _encrypt("mypassword", 0, 1) # shift of 0 is invalid
        assert False # should not reach
    except ValueError:
        assert True # expected exception
        
        
    # Pytest version
    with pytest.raises(ValueError):
        _encrypt("mypassword", 0, 1)

# test 4 : Valid input with special character 
def test_encrypt_allows_special_characters():
    """
    T4: Valid input with special characters
    Expected:
    - Special characters should be allowed and shifted correctly
     notes : 
     Observed behavior : the system dos not enforce forbidden characters 
     , this contradict my assumptions - this is a verifiable discrepancy 
    """
    result = _encrypt("my_password$", 1, 1) # $ is allowed
    assert isinstance(result, str) # output should be a string
    assert len(result) == len("my_password$") # length should be the same as input
    # pytest version
    #with pytest.raises(TypeError):
    #   _encrypt("my_password$", 1, 1)  # $ is non-ASCII and should raise TypeError