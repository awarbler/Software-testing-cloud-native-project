# ============================================================
# CACC Test Suite for _encrypt()
# Course: EE360T Software Testing
# File: test_encrypt_cacc.py
# ============================================================
import pytest  # import pytest for testing
from app.routes.auth import _encrypt  # import function under test
import sys  # access Python path
import os   # work with file paths

sys.path.append(os.path.abspath("backend"))  # add backend to Python path

# Clause A = TRUE (dir_shift < -1)
def test_clause_A_true():
    result = _encrypt("mypassword", 1, -2)  # A = True, B = False
    assert isinstance(result, str)  # function still runs


#  Clause A = FALSE
def test_clause_A_false():
    result = _encrypt("mypassword", 1, 0)  # A = False, B = False
    assert isinstance(result, str)


# Clause B = TRUE (dir_shift > 1)
def test_clause_B_true():
    result = _encrypt("mypassword", 1, 2)  # A = False, B = True
    assert isinstance(result, str)


#  Clause B = FALSE
def test_clause_B_false():
    result = _encrypt("mypassword", 1, 0)  # A = False, B = False
    assert isinstance(result, str)