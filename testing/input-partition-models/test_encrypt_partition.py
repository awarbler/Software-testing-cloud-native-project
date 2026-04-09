# ============================================================
# IDM Test Suite for _encrypt()
# Course: EE360T Software Testing
# File: test_encrypt_partition.py
# ============================================================

import pytest  # pytest is used to check for expected exceptions
from app.routes.auth import _encrypt  # import the encryption function

# Base Test (BT)
def test_encrypt_bt_valid_case():
    """
    BT: Base Choice Test
    C1:b1 (ASCII valid)
    C2:b2 (=1)
    C3:b1 (+1)

    Purpose:
    - Verify normal execution works correctly
    """

    result = _encrypt("mypassword", 1, 1)  # call function with valid inputs
    assert isinstance(result, str)  # output should be a string
    assert len(result) == len("mypassword")  # output length should match input
    
#  T1 — Non-ASCII input
def test_encrypt_non_ascii_partition():
    """
    T1: Non-ASCII input
    C1:b2

    Purpose:
    - Verify non-ASCII characters raise TypeError
    """

    with pytest.raises(TypeError):  # expect TypeError to be raised
        _encrypt("mypasswordé", 1, 1)  # contains non-ASCII character
        
#  T2 — Forbidden characters
def test_encrypt_forbidden_partition():
    """
    T2: Forbidden characters
    C1:b3

    Purpose:
    - Verify forbidden characters raise ValueError
    """

    with pytest.raises(ValueError):  # expect ValueError
        _encrypt("pass word!#", 1, 1)  # contains forbidden characters
        
# T3 — Wrap-high case
def test_encrypt_wrap_high_partition():
    """
    T3: Wrap-high case
    C1:b4

    Purpose:
    - Trigger new_ascii > 127 branch
    """

    result = _encrypt("~", 1, 1)  # high ASCII with large shift
    assert isinstance(result, str)  # should still return a string

# T4 — Wrap-low case
def test_encrypt_wrap_low_partition():
    """
    T4: Wrap-low case
    C1:b5

    Purpose:
    - Trigger new_ascii < 34 branch
    """

    result = _encrypt("#", 1, 1)  # low ASCII with negative shift
    assert isinstance(result, str)  # should still return a string

# T5 — Invalid num_shift
def test_encrypt_invalid_num_shift_partition():
    """
    T5: num_shift < 1
    C2:b1

    Purpose:
    - Verify invalid shift raises ValueError
    """

    with pytest.raises(ValueError):  # expect ValueError
        _encrypt("mypassword", 0, 1)  # invalid shift value

# T6 — Invalid dir_shift (BUG)
def test_encrypt_invalid_dir_shift_partition():
    """
    T6: Invalid dir_shift
    C3:b3

    Purpose:
    - Demonstrate bug in validation logic

    Expected:
    - Should raise ValueError

    Observed:
    - Function executes normally (BUG)
    """

    result = _encrypt("mypassword", 1, 2)  # invalid dir_shift
    assert isinstance(result, str)  # function incorrectly allows this