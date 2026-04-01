# _encrypt() Analysis

### Scope clarification

Two coverage measurements are reported in this project:

1. Full module coverage (auth.py): includes login(), register(), and _encrypt()
2. Function-level coverage (_encrypt only): used for structural testing analysis

The 42% value refers specifically to _encrypt() coverage, which is the target of structural testing.

The 84% value refers to overall module coverage from baseline endpoint tests.

## CFG
![CFG Diagram](./encrypt2.png)
*Figure 1: Control Flow Graph for _encrypt()*

## Nodes
N1: start<br>
N2: B1: input_text.isascii()?<br>
N3: Raise TypeError<br>
N4: B2: num_shift <1?<br>
N5: Raise ValueError (num_shift)<br>
N6: B3: dir_shift < -1 AND dir_shift > 1? (unsatisfiable predicate BUG)<br>
N7: Raise ValueError(dir_shift)(infeasible: dead code due to unsatisfiable predicate)<br>
N8: B4: forbidden char present?<br>
N9: Raise ValueError(forbidden char)<br>
N10: Reverse string and init loop<br>
N11: Loop condition(for char in input_text)<br>
N12: Compute new_ascii<br>
N13: B5: new_ascii > 127?<br>
N14: Wrap high(new_ascii -=128)<br>
N15: B6: new_ascii < 34<br>
N16: Wrap low(new_ascii += 128)<br>
N17: Append shifted char<br>
N18: Return encrypted string<br>
N19: End<br>

...

## Edges
(N1 → N2)<br>
(N2 True → N3)<br>
(N2 False → N4)<br>
(N4 True → N5)<br>
(N4 False → N6)<br>
(N6 True → N7) infeasible<br>
(N6 False → N8)<br>
(N8 True → N9)<br>
(N8 False → N10)<br>
(N10 → N11)<br>
(N11 True → N12)<br>
(N11 False → N18)<br>
(N12 → N13)<br>
(N13 True → N14)<br>
(N13 False → N15)<br>
(N14 → N17)<br>
(N15 True → N16)<br>
(N15 False → N17)<br>
(N16 → N17)<br>
(N17 → N11)<br>
(N18 → N19)<br>

## Prime Path Set

The prime path includes maximal simple paths through each major route. 

- N1 -> N2 -> N3 (non-ASCII Error path )
- N1 -> N2 -> N4 -> N5 (Error path num_shift)
- N1 -> N2 -> N4 -> N6 -> N8 -> N10 (forbidden char Error path )
- N1 -> N2 -> N4 -> N6 -> N8 -> N10 -> N11 -> N12 -> N13 -> N14 -> N17 -> N11 Valid path wrap-high
- N1 -> N2 -> N4 -> N6 -> N8 -> N10 -> N11 -> N12 -> N13 -> N15 -> N17 -> N11 Valid path no-wrap
- N1 -> N2 -> N4 -> N6 -> N8 -> N10 -> N11 -> N12 -> N13 -> N15 -> N16 -> N17 Valid path wrap-low
- N11 -> N18 -> N19 (Loop exit path or Loop cycle path through appended back t loop condition)
- N6 -> N7 (Infeasible path through N6 True (excluded))

## Infeasibility Proof
Let :
A = dir_shift < -1
B = dir_shift > 1

Predicate is P = A AND B

No real value can be both less than -1 and greater than 1 at the same time. 
So P is always false.

Therefore the True branch at N6 is infeasible and should be excluded from the feasible 
branch requirement counts.

## CACC Note
Since P is unsatisfiable, there is no test pair that makes clause A determine P 
or clause B determine P with P switching True/False as required CACC.

CACC requirement for predicate at B3 is infeasible by logic.

## Input Partitioning Model 
input_text: 
- non-ASCII
- ASCII with forbidden chars (space or !)
- ASCII valid normal chars
- ASCII char causing wrap-high (example with large positive shift)
- ASCII char causing wrap-low (example with negative shift)

num_shift:
- less than 1
- equal to 1
- greater than 1

dir_shift:
- +1
- -1
- other values (0, 2, -2) to show current validation defect behavior
...

## Coverage Requirements
- Node coverage: All nodes N1-N19 must be visited, except N7 (infeasible)
- Edge coverage: All edges must be covered except: (N6 -> N7) which is infeasible
- Prime paths: All feasible prime paths listed above must be covered. The path through N6 -> N7 is excluded due to infeasibility.

## Note

The predicate at N6 represents a logical defect in the program. It fails to correctly validate dir_shift, allowing invalid values (0,2,-2) to pass without raising an error.

From test_auth_encrypt.py 

Observed behavior : the system dos not enforce forbidden characters , this contradict my assumptions - this is a verifiable discrepancy 

### Baseline test results 
statements: 60 total, 34 missed -> Coverage for _encrypt() only: 42%
Branches: 26 total, 4 partially covered
Baseline test only exercised normal ASCII path, non_ASCII error, num_shift guard,
and standard transformation. 

The did not cover:
Missing 33,37, 50, 52, 63-78, 95-118

Missing: 
Forbidden character 
Wrap around high
Wrap around low
multi character loop paths
part of login/register

auth.py file covers login() and register(), and _encrypt so the baseline covers 42% statement
coverage and partial branch coverage of auth module.

Coverage is limited because the test were derived from expected behavior and simple error handling. There is no CFG path coverage and a significant portion of _encrypt() is not tested. This allows testing to move to phase 2 (structural Testing) for _encrypt. 


## update as needed