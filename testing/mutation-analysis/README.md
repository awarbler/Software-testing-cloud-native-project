Manual mutants

RIP worksheets

Survived/killed mutant table


Example : 
## Mutation 1

Mutation explanation

Mutation           | Description       | 
| ------            |----------         | 
| Original Code :   | num_shift < 1     | 
| Mutant:           | num_shift <= 1    | 
| Expected Behavior | num_shift = 1 -> Valid Execution   | 
| Results           | ValueError Raised | 
| Killed            | Yes               | 

Manual Mutation Applied:
The condition was manually modified from `new_ascii > 34` to `new_ascii <= 34`

### RIP Analysis Mutation 1

RIP                | Description       |
| ------           |----------         |
| Reachability     | |
| Infection        |                   |
| Propagation      |                   |
| Results          |                   |


Results :

Test failed -> Mutation killed.
The mutation caused 15 failures in the following test suites.


`If you ran test suites`

Test Suite         | # Failures  |
| ------           |----------         |
| Baseline | |
| Structural | |
| Partition |  |
| CACC |  | 
| Mutation |  |
| Total |  |

explanation:      
The 16 test failures occurred because several test cases depend on the boundary condition for num_shift = 1, and the mutation condition causes it to be rejected.

Files that Failed:
FAILED testing/baseline-tests/test_auth_encrypt.py::test_encrypt_allows_special_characters - ValueError: NUM shift N must be >=1

Conclusion: