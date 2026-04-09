# ============================================================
# Mutation Test Suite for _encrypt()
# Course: EE360T Software Testing
# file: test_encrypt_mutation.py
# ============================================================
import pytest
import sys
import os
from app.routes.auth import _encrypt 

# ============================================================
# Mutation # 1 : Boundary Condition Mutation for num_shift
# ============================================================

def test_num_shift_boundary_mutation():
    
    """
    Mutation 1 : Boundary condition mutation for num_shift. 
    
    Original Code : if num_shift < 1, num_shift = 1 → valid input 
    → execution continues
    
    Mutant: num_shift <= 1  |num_shift = 1 → condition (<= 1) 
    becomes True → ValueError is raised incorrectly  
    
    Goal of the Test:
    This test aims to verify that the _encrypt function correctly 
    handles the boundary condition for num_shift and to see if the
    test suite can detect the incorrect mutation. 
    
    Input: "mypassword", num_shift = 1, num_iterations = 1
    
    Execution steps(based on CFG):
    N1 -> start, N2 -> false, N$ (True in mutant) → ERROR
    
    Expected Behavior for the original it should return an encrypted
    string 
    Expected behavior for the mutant: It should raise a ValueError 
    due to the incorrect mutation of the condition.
    
    Expected Results: the test should fail for the mutant and the mutation
    is killed. 
    """
    result = _encrypt("mypassword",1,1) # valid boundary case
    assert isinstance(result, str) # ensure we get a string back
    assert result != "mypassword" # ensure the result is different from input
    
    
    #assert result is not None # ensure we get a result back

# ============================================================
# Mutation # 2 : Logical Operator Mutation for dir_shift
# ============================================================
    
def test_dir_shift_logic_mutation():
    """
    Mutation 2 : logical operator mutation for dir_shift
    Original code: Always FALSE 
    Mutant : becomes true for invalid values 
    
    Goal of Test: to verify whether the test suite detects incorrect 
    handling of invalid dir_shift values and raises a ValueError
    
    Input: "mypassword", num_shift = 1, dir_shift = 2
    
    Execution steps (based on CFG):
    N1 -> N2(False) -> N4(False) -> N6(True in mutant) -> ERROR
    
    Expected Behavior for original : The function should execute 
    normally which returns a bug 
    
    Expected behavior for mutant : the function should raise a 
    ValueError due to the incorrect mutation of the condition.
    
    Expected Results: The test should fail if the mutation is detected
    and killed. 
    
    """
    result = _encrypt("mypassword",1,2) # invalid dir_shift value
    assert isinstance(result, str) # ensure we get a string back
    #assert result != "mypassword" # ensure the result is different from input

# ============================================================
# Mutation # 3 :
# ============================================================
def test_wrap_high_boundary_mutation():
    """
    Mutation 3 : Mutation for wrap around logic when new_ascii exceeds 127
    
    Original code: if new_ascii > 127, new_ascii = new_ascii - 128
    Mutant: if new_ascii >= 127, new_ascii = new_ascii - 128
    
    Goal of Test: to verify that the function correctly handles the wrap around 
    logic when new_ascii exceeds the upper boundary of valid ASCII values.
    
    Input: A string that results in new_ascii being exactly 127 after shifting.
    
    Execution steps (based on CFG):
    N1 -> N2(False) -> N3(True) -> N5(True in mutant) -> ERROR
    
    Expected Behavior for original: The function should execute normally and return an encrypted string.
    
    Expected behavior for mutant: The function should incorrectly wrap around when new_ascii is exactly 127, leading to an incorrect encrypted result.
    
    Expected Results: The test should fail if the mutation is detected and killed. 
    """
    # Choose a character that will result in new_ascii being exactly 127 after shifting
    input_text = "~" # ASCII 126
    num_shift = 1 # Shift of 1 will result in new_ascii = 126 + (1 * 1) = 127
    result = _encrypt(input_text, num_shift, 1)
    #assert isinstance(result, str) # ensure we get a string back
    
    # mutant would wrap incorrectly -> different result than expected
    expected_ascii = 127 # Expected result for original code
    expected_char = chr(expected_ascii)
    assert result == expected_char # ensure the result matches expected character for original code
    
    
def test_wrap_low_boundary_mutation():
    """
    Mutation 4 : Mutation for wrap around logic when new_ascii is less than 34
    
    Original code: if new_ascii < 34, new_ascii = new_ascii + 128
    Mutant: if new_ascii <= 34, new_ascii = new_ascii + 128
    
    Goal of Test: to verify that the function correctly handles the wrap around 
    logic when new_ascii is below the lower boundary of valid ASCII values.
    
    Input: A string that results in new ascii being exactly 34 after shifting.
    
    Execution steps (based on CFG):
    N1 -> N2(False) -> N3(False) -> N4(True) -> N6(True in mutant) -> ERROR
    
    Expected Behavior for original: The function should execute normally and return an encrypted string.
    
    Expected behavior for mutant: The function should incorrectly wrap around when new_ascii is exactly 34, leading to an incorrect encrypted result.
    
    Expected Results: The test should fail if the mutation is detected and killed. 
    """
    # Choose a character that will result in new_ascii being exactly 34 after shifting
    input_text = "#" # ASCII 35
    num_shift = 1 # Shift of 1 will result in new_ascii = 35 + (1 * 1) = 36
    dir_shift = -1 # Shift direction of -1 will result in new_ascii = 35 + (1 * -1) = 34
    result = _encrypt(input_text, num_shift, dir_shift)

    expected_ascii = 34 # Expected result for original code
    expected_char = chr(expected_ascii)
    assert result == expected_char # ensure the result matches expected character for original code