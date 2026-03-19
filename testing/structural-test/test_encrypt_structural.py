import pytest
from app.routes.auth import _encrypt 

# Test 1 : non-ASCII should raise TypeError

# Test 2 : num_shift < 1 should raise ValueError

# Test 3: forbidden character should raise ValueError 

# Test 4 : Normal transform no wrap 

# Test 5 Wrap High branch

# Test 6: Wrap low branch 

# Test 7 : Empty String 

# Test 8: Multi character input 
