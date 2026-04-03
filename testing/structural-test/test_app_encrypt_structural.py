# ============================================================
# Structural Test Suite for _encrypt()
# Course: EE360T Software Testing
# ============================================================
import pytest
import sys
import os
from app.routes.auth import _encrypt 

"""
Structural Test for _encrypt Function in auth.py

This test suite is designed using white box testing techniques 

Coverage Criteria:
- Node Coverage: each CFG Node is executed at least once
- Edge/Branch Coverage: each branch outcome is tested
- Prime Path Coverage: exercise all prime paths in the CFG

Testing approach: Based on CFG (N1-N19)
- RIP (Reachability, Infection, Propagation) 
    - reachability -> did execution reach the line
    - infection -> did the state change
    - propagation -> did it change the output
    
Notes:
- Infeasible branch(dir_sift < -1 AND dir_shift >1) is excluded from test.

"""



# Test 1 :N2 true -> N3 non-ASCII should raise TypeError
def test_non_ascii():
    """
    T1: Non-Ascii input.
    Test the branch where input_text  == False
    Input: "é" (non-ASCII character) -> trigger error in _encrypt function
    Execution steps:
    N1 -> start, N2 -> check input input_text.isascii(), 
                "é".isascii() == False → TRUE branch
    N3 -> raise TypeError exception for non-ASCII input
    
    CFG Path:
    N1 (start) -> N2(True) -> N3 (raise TypeError)
    
    Structural coverage:
    Nodes Covered: N2, N3
    Edges covered: E1 (N1-> N2) and E2 (N2 True -> N3)
    Prime Path Coverage: P1: N1 -> N2 -> N3
    
    IMPORTANT:
    Execution STOPS at N3 → no further nodes are reachable

    EXPECTED RESULT:
    TypeError is raised

    """
    with pytest.raises(TypeError):
        _encrypt("é",1 ,1)

# Test 2 :N4 true-> N5 num_shift < 1 should raise ValueError exception test

   # def test_name():
   # with pytest.raises(ExpectedException):
   #   function_call(arguments)
def test_num_shift_less_than_one():
    """
    T2: num_shift < 1
    Test the branch where num_shift < 1 is invalidN4 true -> N5 num_shift < 1 
    should raise ValueError exception test Verify that _encrypt raises 
    ValueError when num_shift is less than one
    
    Input: num_shift = 0 -> invalid (must be >= 1)
    Execution steps:
    N1 -> start, 
    N2 -> ASCII input_text.isascii() == True → FALSE branch (continues execution)
    N4 -> check num_shift < 1 , 0 < 1 -> True
    N5 -> raise ValueError exception for invalid num_shift
    
    CFG Path:
    N1 (start) -> N2(False) -> N4 (True) -> N5 (raise ValueError)
    
    Structural coverage:
    Nodes Covered: N4(True), N5
    Edges covered: E1 (N1-> N2) and E3 (N2 False -> N4)
         E4: (N4 True -> N5)
    Prime Path Coverage: P2: N1 -> N2 -> N4 -> N5 (Error path num_shift)
    
    IMPORTANT:
    Execution STOPS at N5 → no further nodes are reachable

    EXPECTED RESULT:
    ValueError is raised
    """
    with pytest.raises(ValueError):
        _encrypt("password", 0, 1)

# Test: Infeasible N6 -> N7 
# dir_shift < -1 or dir_shift > 1 should raise ValueError exception test

# Test 3: N8 -> N9 forbidden character should raise ValueError exception test
def test_forbidden_character():
    """
    T3: Forbidden Character 
    The test must trigger the branch where forbidden character is detected
    Input: "pass word!# " (contains space special characters that are forbidden)
    
    Execution steps:
    N1 -> start, 
    N2 -> input_text.isascii() == True → FALSE branch (continue execution)
    N4 -> num_shift valide -> False Branch
    N6 -> Infeasible branch (dir_shift < -1 or dir_shift > 1) -> False branch
    N8 -> forbidden character present -> True branch
    N9 -> raise ValueError exception for forbidden character
    
    CFG Path: 
    N1 (start) -> N2(False) -> N4(False) -> N6 (False) -> N8 (True) 
        -> N9 (raise ValueError)
        
    Structural coverage:
    Nodes Covered: N8(True), N9
    Edges covered: E5 (N4 -> N6), E7:(N6 -> N8), E8( N8 -> N9)
    Prime Path Coverage: P3
    Expected: ValueError is raised due to forbidden character
    """
    with pytest.raises(ValueError):
        _encrypt("pass word!#", 1, 1)

# Test 4 : Test Normal transform no wrap
def test_normal_no_wrap():
    """
    T4: Normal execution
    the test will Valid execution that does not trigger wrap Loop executes at 
    least once (N11 True branch taken)
    
    Input: "hello" with small shift
    Execution steps:
    
    Path: the test will go through the loop and normal transforation
    CFG Path: N10 -> N11 -> N12 -> N13(False) -> N15(False) -> N17
    
    Structural Coverage: 
    Edges: E10 - E21 : loop transformation 
    Prime Path: P4
    Expected: Valid string returned
    """
    result = _encrypt("hello", 1, 1) # $ is allowed
    assert len(result) == len("hello") # length should be the same as input
   
# Test 5 : N13 -> N14 Wrap High branch boundary test
def test_wrap_high():
    """
    T5: Wrap high
    the test must trigger new_ascii > 127
    
    input: "~" with large shift
    Execution steps:
    CFG Path: N13(True) -> N14 -> 17
    
    Structural Coverage:
    Edge: E14(N13 -> N14)
    
    Prime Path: P5 
    """
    result = _encrypt("~", 10, 1) # is allowed
    assert isinstance(result, str) # 
   

# Test 6: N15 -> N16 Wrap low branch boundary test 
def test_wrap_low():
    """
    T6: wrap low
    The test must trigger new_ascii < 34
    Input:
    Execution steps:
    CFG Path: N15(True) -> N16 -> N17
    Structural Coverage:
    Edge: E17 (N15 -> N16)
    Prime Path: P6
    
    """
    result = _encrypt("#", 10, -1) # is allowed
    assert isinstance(result, str) # 

# Test 7 : Empty String 
def test_empty_string():
    """
    T7: Empty input
    The test must loop not entered 
    Input:
    Execution steps:
    CFG Path: N10 -> N11 (False) -> N18 -> N19
    
    Structural Coverage:
    Edge: E12 (N11 -> N18)
    Prime Path: P7
    """
    result = _encrypt("", 1, 1) # $ is allowed
    assert result == ""

# Test 8: Multi character input loop cycle
def test_multi_character_loop():
    """
    T8 
    the test will loop will repeat
    Input:
    Execution steps:
    CFG Path: N11 -> N12 -> N17 -> N11 (cycle)
    
    Structural Coverage: 
    Edge: E20 
    Prime Path: Loop cycle behavior (supports P4–P6 execution paths)
    """
    result = _encrypt("hello", 1, 1) # $ is allowed
    assert len(result)== len("hello")

# Test 9: N17-> N11 loop test 
def test_multiple_iterations_loop():
    """
    T9: Multiple loop iterations
    We must confirm the loop executes more than once

    INPUT: "abcdef" → multiple characters

    EXECUTION STEPS:
    Loop runs repeatedly:
    N11 → N12 → N17 → N11 → N12 → N17 ...

    CFG PATH:
    N11 → N12 → N17 → N11 (repeated cycle)

    STRUCTURAL COVERAGE:
    - Edge: E20 (loop back edge exercised multiple times)
    - Reinforces loop behavior

    IMPORTANT:
    This test ensures the loop handles multiple iterations correctly

    EXPECTED:
    Output length matches input length
    """

    result = _encrypt("abcdef", 1, 1)
    assert len(result) == len("abcdef")
