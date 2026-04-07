import pytest  # import pytest for testing
from app.routes.auth import _encrypt  # import function under test
import sys  # access Python path
import os   # work with file paths

sys.path.append(os.path.abspath("backend"))  # add backend to Python path

def test_dir_shift_negative():  # test case for A = TRUE
    result = _encrypt("abc", 1, -2)  # call function
    assert isinstance(result, str)  # ensure valid output

def test_dir_shift_positive():  # test case for B = TRUE
    result = _encrypt("abc", 1, 2)  # call function
    assert isinstance(result, str)  # ensure valid output