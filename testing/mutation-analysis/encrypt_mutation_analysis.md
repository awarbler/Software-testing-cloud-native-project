# Mutation Analysis for `_encrypt()`

The mutation test suite only affects the _encrypt() function. The other modules, such as login() , register(), and hardware, are not affected because they do not depend on the mutated condition. 

The mutation test suite is demonstrating proper test isolation and confirms that the mutation is localized to the affected function. 

Test Cycle: 

1. Modify the code 
2. Run all of the tests.
3. Observe the failures 
4. Document the results
5. Confirm that all of the tests pass.


## Mutation 1 Boundary Condition Mutation for num_shift

The mutation will change the boundary conditions , incorrectly treating num_shift = 1 as an invalid input. 

Mutation           | Description       | 
| ------            |----------         | 
| Original Code :   | num_shift < 1     | 
| Mutant:           | num_shift <= 1    | 
| Expected Behavior | num_shift = 1 -> Valid Execution   | 
| Results           | ValueError Raised | 
| Killed            | Yes               | 

Manual Mutation Applied:
The condition was manually modified from `num_shift < 1`  to `num_shift <= 1`

### RIP Analysis Mutation 1

RIP                | Description       |
| ------           |----------         |
| Reachability     | Test case calls `_encrypt` with `num_shift = 1` and reaches the condition |
| Infection        | The mutation changes the condition evaluation for `num_shift = 1 `|
| Propagation      | The mutation causes an execution to raise a `ValueError` instead of proceeding normally. |
| Result         | Mutation Killed                  |

Results:

Test failed -> Mutation killed.

Test Suite         | # Failures  |
| ------           |----------   |
| Baseline | 1 |
| Structural | 4 |
| Partition | 4 |
| CACC | 4 |
| Mutation | 2 |
| Total | 16 |

The 16 test failures occurred because several test cases depend on the boundary condition for `num_shift = 1`, and the mutation condition causes it to be rejected.

Files that Failed:

FAILED testing/baseline-tests/test_auth_encrypt.py::test_encrypt_allows_special_characters - ValueError: NUM shift N must be >=1
FAILED testing/cacc-analysis/test_encrypt_cacc.py::test_clause_A_true - ValueError: NUM shift N must be >=1
FAILED testing/cacc-analysis/test_encrypt_cacc.py::test_clause_A_false - ValueError: NUM shift N must be >=1
FAILED testing/cacc-analysis/test_encrypt_cacc.py::test_clause_B_true - ValueError: NUM shift N must be >=1
FAILED testing/cacc-analysis/test_encrypt_cacc.py::test_clause_B_false - ValueError: NUM shift N must be >=1
FAILED testing/input-partition-models/test_encrypt_partition.py::test_encrypt_bt_valid_case - ValueError: NUM shift N must be >=1
FAILED testing/input-partition-models/test_encrypt_partition.py::test_encrypt_wrap_high_partition - ValueError: NUM shift N must be >=1
FAILED testing/input-partition-models/test_encrypt_partition.py::test_encrypt_wrap_low_partition - ValueError: NUM shift N must be >=1
FAILED testing/input-partition-models/test_encrypt_partition.py::test_encrypt_invalid_dir_shift_partition - ValueError: NUM shift N must be >=1
FAILED testing/mutation-analysis/test_encrypt_mutation.py::test_num_shift_boundary_mutation - ValueError: NUM shift N must be >=1
FAILED testing/mutation-analysis/test_encrypt_mutation.py::test_dir_shift_logic_mutation - ValueError: NUM shift N must be >=1
FAILED testing/structural-test/test_app_encrypt_structural.py::test_normal_no_wrap - ValueError: NUM shift N must be >=1
FAILED testing/structural-test/test_app_encrypt_structural.py::test_empty_string - ValueError: NUM shift N must be >=1
FAILED testing/structural-test/test_app_encrypt_structural.py::test_multi_character_loop - ValueError: NUM shift N must be >=1
FAILED testing/structural-test/test_app_encrypt_structural.py::test_multiple_iterations_loop - ValueError: NUM shift N must be >=1

Conclusion:

The mutation is killed. The test suite shows strong sensitivity to boundary-condition errors and demonstrates high fault detection capability for incorrect logic. After auth.py was reverted, all 58 tests passed successfully. The test results confirm that the mutation was the sole cause of all of the failures. The test suite can distinguish between the original and mutated behavior. 

## Mutation 2 Logical Operator Mutation (dir_shift)

Mutation 2 connects to CACC. This mutation will change the boundary of `and` to `or`. The original condition is unsatisfiable and will always evaluate to FALSE, and the branch will never be executed, and no ValueError will be raised. The mutated condition becomes TRUE for invalid inputs. This mutation will test whether the test suite detects improper handling of invalid dir_shift values.  The test should now FAIL in the partition test suite. This mutation changes the behavior by enforcing validation that is missing in the original implementation.

Mutation           | Description       | 
| ------            |----------         | 
| Original Code :   | elif dir_shift < -1 and dir_shift > 1  | 
| Mutant:           | elif dir_shift < -1 or dir_shift > 1| 
| Expected Behavior | Invalid dir_shift should NOT be detected - BUG | 
| Results           | ValueError Raised | 
| Killed            | Yes     | 

Manual Mutation Applied:
The condition was manually modified from  `dir_shift < -1 and dir_shift > 1`  to `dir_shift < -1 or dir_shift > 1`


### RIP Analysis Mutation 2

RIP                | Description       |
| ------           |----------         |
| Reachability     | Test case calls _encrypt with invalid dir_shift values such as a 2 |
| Infection        | The mutation changes the condition from always FALSE to conditionally TRUE |
| Propagation      | The incorrect branch raises a ValueError instead of executing |
| Results          | Mutation Killed  |

Results :

Test failed -> Mutation killed.

Mutation 2 code resulted in 4 tests that failed, while 55 passed. The failures occurred in the test cases that previously exposed a defect in the original logic. The mutation test case expected normal execution for invalid dir_shift values, but the mutation corrected the logic and raised a ValueError instead. The test case exposes an existing defect in the original implementation. The tests expect the bug, and the mutation is set up to remove it, causing the test to fail. When the mutation introduces stricter validation, existing tests fail, revealing a dependency on incorrect logic. The mutation is killed because it introduces validation behavior that is absent in the original implementation, causing tests that expect normal execution to fail.

Test Suite         | # Failures  |
| ------           |----------   |
| Baseline | 0 |
| Structural | 0 |
| Partition | 1 |
| CACC | 2 |
| Mutation | 1 |
| Total | 4 |

Files Failed :

FAILED testing/cacc-analysis/test_encrypt_cacc.py::test_clause_A_true - ValueError: Direction shift D must be either +1 or -1
FAILED testing/cacc-analysis/test_encrypt_cacc.py::test_clause_B_true - ValueError: Direction shift D must be either +1 or -1
FAILED testing/input-partition-models/test_encrypt_partition.py::test_encrypt_invalid_dir_shift_partition - ValueError: Direction shift D must be either +1 or -1
FAILED testing/mutation-analysis/test_encrypt_mutation.py::test_dir_shift_logic_mutation - ValueError: Direction shift D must be either +1 or -1


Test Suite         | # Failures  |
| ------           |----------   |
| Baseline | 0 |
| Structural | 0 |
| Partition | 1 |
| CACC | 2 |
| Mutation | 1 |
| Total | 4 |

Conclusion:

The mutation is killed.  All failures showed a ValueError at the mutation dir_shift < -1 or dir_shift > 1.  The mutation reveals a bug in the original program. Unlike mutation 1 , mutation 2 reveals a defect in the original program logic. The original condition fails to validate invalid dir_shift values, while the mutation correctly detects them. 

This demonstrates that the test suite detects faults but also exposes existing weaknesses. Once the code is reverted back to the original state, all 59 tests pass. 


## Mutation 3 Relational Operator(Wrap- high Boundary)

This mutation tests the relations operator at the wrap- high boundary. 
The mutation changes the condition from > to >=, introducing an off-by-one error at the boundary value new_ascii =127. This mutation checks whether the test suite can detect the incorrect wrap-around behavior.

 Mutation           | Description       |
| ------            |----------         |
| Original Code :   | if new_ascii > 127  |
| Mutant:           | if new_ascii >= 127 |
| Expected Behavior | new_ascii = 127 should not wrap |
| Results           | ValueError raised  | 
| Killed            |    Yes  | 

Manual Mutation Applied:
The condition was manually modified from  `new_ascii > 127` to `new_ascii >= 127`

### RIP Analysis Mutation 3

RIP                | Description       |
| ------           |----------         |
| Reachability     | The test cases uses input "~" with num_shift = 1 to reach new_ascII = 127 |
| Infection        | The mutation changes evaluation at the boundary value new_ascii = 127 from FALSE to TRUE |
| Propagation      | The incorrect wrap produces new_ascii = -1  error, which  is outside the valid range for chr(), resulting in a ValueError. |
| Results          | Mutation killed.       |


Results :

Test failed -> Mutation Killed.

Mutation 3 resulted in 2 failed tests and 57 passed. 

The failed test resulted in a ValueError for the chr() arg not in range.  To compute the new ASCII is 126 and applied the shift 126 + (1 * 1 ) = 127. The original code suggests that if the new ASCII is  >127 -> FALSE,  which results in no wrap; chr(127) -> valid,  and the program continues. In the mutant, if new_ascii is >= 127 -> TRUE, and the wrap occurs. new ASCII is 127-128, and this equals -1. This causes a crash: chr(-1) ValueError: chr() arg not
in range. Failure occurred because the mutated condition incorrectly triggers wrap-around at the boundary, producing an invalid ASCII value.


Test Suite         | # Failures  |
| ------           |----------         |
| Baseline | 0 |
| Structural | 0 |
| Partition | 1 |
| CACC | 0 | 
| Mutation | 1 |
| Total | 2 |
      

FAILED testing/input-partition-models/test_encrypt_partition.py::test_encrypt_wrap_high_partition - ValueError: chr() arg not in range
FAILED testing/mutation-analysis/test_encrypt_mutation.py::test_wrap_high_boundary_mutation - ValueError: chr() arg not in range(0x110000)

Conclusion: The mutation breaks the ASCII range, creating an invalid character of -1, and causes a runtime error. 
The mutation is killed.  

The mutation demonstrates strong test coverage for boundary conditions and error propagation in the encryption algorithm. Mutation 3 shows that our test suite detects boundary condition errors, incorrect wrap logic, invalid ASCII handling , runtime failures, and off-by-one errors, which are correctly detected by the partition test. 

## Mutation 4 Relations Operator (Wrap-Low Boundary )

This mutation tests the relations operator for the wrap-low boundary. The mutation changes the condition from < to <= , introducing an off-by-one error at the boundary value new_ascii = 34. 

This mutation checks whether the test suite can detect incorrect wrap-around behavior at the lower ASCII boundary. 

Mutation           | Description       | 
| ------            |----------         | 
| Original Code :   | if new_ascii < 34    | 
| Mutant:           | if new_ascii <= 34 | 
| Expected Behavior | new_ascii = 34 should not wrap   | 
| Results           | Assertion failure | 
| Killed            |     Yes     | 

Manual Mutation Applied:
The condition was manually modified from `new_ascii < 34` to `new_ascii <= 34`

### RIP Analysis Mutation 4

RIP                | Description       |
| ------           |----------         |
| Reachability     | The test cases uses "#" with num_shift = 1 and dir_shift = -1 to reach new ascii = 34|
| Infection        | The mutation changes evaluation on the boundary from FALSE to TRUE  |
| Propagation      | The mutation causes new_ascii = 162 (34 + 128) -> '¢' (162)  |
| Results          |  Mutation killed.       |


Results :

Test failed -> Mutation killed. 

Mutation 4 resulted in an assertion failure because the mutated condition incorrectly triggered a wrap-around at the lower boundary, new_ascii = 34. 

The original code produces ASCII 34 (") while the mutation created ASCII 162 '¢', resulting in a mismatch. This difference is detected by the test, confirming that the mutation is killed.

Test Suite         | # Failures  |
| ------           |----------         |
| Baseline | 0 |
| Structural | 0 |
| Partition | 0 |
| CACC | 0 | 
| Mutation | 1 |
| Total | 1 |

Files failed:
FAILED testing/mutation-analysis/test_encrypt_mutation.py::test_wrap_low_boundary_mutation - assert '¢' == '"' 

Conclusion:

The mutation is killed. The test suite successfully detects off-by-one errors at the lower boundary and identifies incorrect wrap logic. 

This demonstrates strong test coverage for boundary precision and correct detection of behavioral differences introduced by relational operator mutation. 

## Mutation Testing Summary 

The mutation test suite evaluated the effectiveness of the test cases by introducing controlled faults into the _encrypted() function. 

All mutations were successfully killed:

- Mutation 1 (Boundary Condition): detected incorrect handling of num_shift
- Mutation 2 (Logical Operator): exposed missing validation logic
- Mutation 3 (Wrap-High Boundary): detected invalid ASCII generation
- Mutation 4 (Wrap-Low Boundary): detected incorrect boundary wrap behavior

The test suites demonstrated strong fault detection by:

- identifying both logical and boundary-related defects
- detecting failures through exceptions and assertion mismatches 
- exposing dependencies on current implementation behavior 

These results confirm that the tes suite is effective in distinguishing between correct and faulty program behavior. 

Mutant Summary Table 

Mutation         | Type  | Description  | Result |
| ------         |----------|----------|----------|
| 1 | Boundary | num_shift < 1 -> <=1  | Killed  |
| 2 | Logical Operator | and -> or(dir_shift) | Killed  |
| 3 | Relational | > -> >=(wrap-high) | Killed  |
| 4 | Relational | < -> <= (wrap-low) | Killed  |
