import pytest
import sys
import os 
from app.routes.auth import _encrypt 

"""
Structural Test for _encrypt Function in auth.py

This test suite is desgined useing white box tesing techniques 

Coverage Criteria:
- Node Coverage: each CFG Node is executed at least once
- Edge/Branch Coverage: each branch outcome is tested
- Prime Path Coverage: exercise all prime paths in the CFG

Testing approach: 
- RIP (Reachability, Infection, Propagation) 
    - reachability -> did exectuion reach the line
    - infection -> did the state change
    - propagation -> did it change the output
    
Notes:
- Infeasible branch(dir_sift < -1 AND dir_shift >1) is excluded from test.

"""



# Test 1 :N2 -> N3 non-ASCII should raise TypeError
def test_non_ascii():
    """
    Verify that _encrypt reject non ASCII input
    
    Structural coverage:
    - reaches branch : input_text.isascii() == False
    - Test edge coverage  
    """
    with pytest.raises(TypeError):
        _encrypt("é",1 ,1)

# Test :N2 - ASCII 
# Test 2 :N4 -> N5 num_shift < 1 should raise ValueError exception test

# Test 3: N8 forbidden character should raise ValueError exception test

# Test 4 : Normal transform no wrap 

# Test 5 : N13Wrap High branch boundary test

# Test 6: N15 Wrap low branch boundary test 

# Test 7 : Empty String 

# Test 8: Multi character input 
