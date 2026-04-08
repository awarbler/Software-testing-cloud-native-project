# _encrypt() Analysis

# Version History

* v1.6 (2026-04-06)

* v1.5 (2026-04-04)
  * Corrected coverage scope wording to explicitly distinguish module-level `auth.py ` percentages from the `_encrypt()` structural test scope.
* v1.4 (2026-04-02)
  * Added formal Test Requirements (TR) table and explicit branch definitions.
  * Expanded the logic coverage section to explicit CACC infeasibility reasoning.
  * Updated the input partitioning section to explicit input space partitioning classes.
* v1.3 (2026-04-02)
  * Added explicit T8 and T9 entries to the test-to-coverage mapping.
  * Added loop coverage justification for single-iteration and multi-iteration behavior.
  * Added explicit feasible-coverage interpretation and conclusion block.
* v1.2 (2026-04-02)
  * Added structural test execution command and reproducible run instructions.
  * Added structural coverage results summary (9 passed, 49% auth.py module coverage).
  * Clarified _encrypt()-only interpretation: full feasible node/edge/prime-path coverage; line 33 remains infeasible by logic.
* v1.1 (2026-04-01)
  * Added CFG-based structural test mapping, infeasibility proof for N6 -> N7, and CACC infeasibility note.
* v1.0 (2026-03-19)
  * Initial _encrypt() analysis with baseline coverage context and CFG documentation.

### Scope clarification
Coverage Measurements: 

- Full module coverage (auth.py) includes: login(), register(), and _encrypt. 
- Function level coverage -encrypt: used for structural testing analysis. 

The 42% baseline value specifically refers to module-level coverage for auth.py from a baseline suite focused on _encrypt().

It is not whole-project coverage, and it is not a pure function-only percentage.

statements at a Function-level _encrypt() are derived from CFG/path mapping and feasible-path analysis, not from the module percentage alone.

## Coverage Goals (By Scope)

* _encrypt() function: 100% feasible structural coverage (node, edge, prime path), excluding infeasible E6 (N6 -> N7) and N7.
* login() / register(): 90% target (baseline + input partitioning/spec-based tests).
* Hardware check-in/checkout: 95% target.
* Overall backend: 80%+ target.

### Note on interpreting coverage.

The following test will be explained. 

Module-level coverage may appear lower when structural tests focus only on _encrypt(). Coverage percentages must always be interpreted relative to the test scope and target component.


## CFG
![CFG Diagram](./encrypt2.png)
*Figure 1: Control Flow Graph for _encrypt()*

## CFG Nodes


| Node | Branch | Description |
|------|--------|------------|
| N1   | —      | start |
| N2   | B1     | input_text.isascii()? |
| N3   | —      | Raise TypeError |
| N4   | B2     | num_shift <1? |
| N5   | —      | Raise ValueError (num_shift) |
| N6   | B3     | dir_shift < -1 AND dir_shift > 1? (unsatisfiable predicate BUG) |
| N7   | —      | Raise ValueError(dir_shift)(infeasible: dead code due to unsatisfiable predicate) |
| N8   | B4     | forbidden char present? |
| N9   | —      | Raise ValueError(forbidden char) |
| N10  | —      | Reverse string and init loop |
| N11  | —      | Loop condition(for char in input_text) |
| N12  | —      | Compute new_ascii |
| N13  | B5     | new_ascii > 127? |
| N14  | —      | Wrap-around-high(new_ascii -=128) |
| N15  | B6     | new_ascii < 34 |
| N16  | —      | Wrap-around-low(new_ascii += 128) |
| N17  | —      | Append shifted char |
| N18  | —      | Return encrypted string |
| N19  | —      | End |

...

## Edges

| Edge | Definition |
|------|------------|
| E1   | (N1 → N2) |
| E2   | (N2 True → N3) |
| E3   | (N2 False → N4) |
| E4   | (N4 True → N5) |
| E5   | (N4 False → N6) |
| E6   | (N6 True → N7) infeasible |
| E7   | (N6 False → N8) |
| E8   | (N8 True → N9) |
| E9   | (N8 False → N10) |
| E10  | (N10 → N11) |
| E11  | (N11 True → N12) |
| E12  | (N11 False → N18) |
| E13  | (N12 → N13) |
| E14  | (N13 True → N14) |
| E15  | (N13 False → N15) |
| E16  | (N14 → N17) |
| E17  | (N15 True → N16) |
| E18  | (N15 False → N17) |
| E19  | (N16 → N17) |
| E20  | (N17 → N11) |
| E21  | (N18 → N19) |

## Prime Path Set

A simple path means you do not repeat nodes (unless it is a cycle where the start and end match).

A prime path is a maximal simple path that cannot be extended without repeating a node.

Note: Node paths do not have to start at the beginning; for example, in _encrypt, they can start within the loop ( N10).(ee282c16-260117-chapter2-1)

| Path | Definition |
|------|------------|
| P1   | N1 -> N2 -> N3 (non-ASCII Error path ) |
| P2   | N1 -> N2 -> N4 -> N5 (Error path num_shift) |
| P3   | N1 -> N2 -> N4 -> N6 -> N8 -> N9 (forbidden char Error path ) |
| P4   | N10 -> N11 -> N12 -> N13 -> N15 -> N17 Valid path no-wrap |
| P5   | N10 -> N11 -> N12 -> N13 -> N14 -> N17 Valid path wrap-high |
| P6   | N10 -> N11 -> N12 -> N13 -> N15 -> N16 -> N17 Valid path wrap-low |
| P7   | N10 -> N11 -> N18 -> N19 (Loop exit path when false) |
| P8   | N6 -> N7 (Infeasible path through N6 True (excluded)) dir_shift < -1 AND dir_shift > 1 is unsatisfiable |

## Test Case → Coverage Mapping

This table maps each test case to the CFG edges and prime paths it covers.

This shows how each test actually covers the nodes, edges, and paths from the CFG.

| Test Case | Description                         | CFG Edges Covered                          | Prime Paths Covered |
|-----------|-------------------------------------|--------------------------------------------|---------------------|
| T1        | Non-ASCII input                     | E1, E2                                     | P1                  |
| T2        | num_shift < 1                       | E1, E3, E4                                 | P2                  |
| T3        | Forbidden character                 | E1, E3, E5, E7, E8                         | P3                  |
| T4        | Valid input (no wrap)               | E10–E21 (loop execution edges)             | P4                  |
| T5        | Wrap-around-high condition                 | —                                          | P5                  |
| T6        | Wrap-around-low condition                  | —                                          | P6                  |
| T7        | Empty string (loop exit)            | —                                          | P7                  |
| T8        | Loop cycle (single iteration)       | E20 (loop back edge)                       | —                   |
| T9        | Multiple loop iterations            | E20 (loop back edge, repeated execution)   | —                   |

## Test Requirements Table (TR)

| Requirement Type | Requirement | Covered By |
|------------------|-------------|------------|
| Node | N2 True -> N3 | T1 |
| Node | N4 True -> N5 | T2 |
| Node | N8 True -> N9 | T3 |
| Edge | E14 (Wrap-around-high) | T5 |
| Edge | E17 (Wrap-around-low) | T6 |
| Edge | E20 (loop back) | T8, T9 |
| Prime Path | P1 | T1 |
| Prime Path | P2 | T2 |
| Prime Path | P3 | T3 |
| Prime Path | P4 | T4 |
| Prime Path | P5 | T5 |
| Prime Path | P6 | T6 |
| Prime Path | P7 | T7 |

## Branch Definitions

| Branch | Definition |
|--------|-----------|
| B1     | input_text.isascii() |
| B2     | num_shift < 1 |
| B3     | dir_shift < -1 AND dir_shift > 1 (infeasible) |
| B4     | forbidden character present |
| B5     | new_ascii > 127 |
| B6     | new_ascii < 34 |

## Loop Coverage Justification

The loop in _encrypt() (N11 -> N12 -> N17 -> N11) is explicitly tested:

* T8 is used to loop through a single iteration of the cycle.
* T9 validates multiple iterations of the loop.
* T7 validates if the loop condition is FALSE, and the function exits via N11 False branch.

This ensures:

* Coverage of the loop entry (N11 True branch).
* Coverage of the loop exit (N11 False branch).
* Coverage of the loop-back edge (E20).

Therefore, loop behavior is fully exercised and included in prime path coverage.

## Infeasibility Proof

Let :
A = dir_shift < -1
B = dir_shift > 1

Predicate is P = A AND B

No real value can be both less than -1 and greater than 1 at the same time.
So P is always false.

Therefore, the TRUE branch at N6 is infeasible and should be excluded from the feasible branch requirement counts.

## Logic Coverage (CACC)

Predicate at N6:
P = (dir_shift < -1 AND dir_shift > 1)

Clauses:
A: dir_shift < -1
B: dir_shift > 1

According to the CACC definition, each clause should be able to change the outcome of P by itself, and P should be able to be both true and false.

However:
No value of dir_shift can satisfy both A and B simultaneously.

Therefore:

* Predicate P is unsatisfiable.
* No test pair can make A or B independently determine P. That means there are no test cases that can make either clause actually affect the result.  

Conclusion:
CACC is infeasible due to an unsatisfiable predicate.(ee382c16-260131-Chapter3-I.pdf)

## Input Space Partitioning

input_text:

* non-ASCII
* ASCII valid
* ASCII with forbidden characters
* ASCII causing wrap-high
* ASCII causing wrap-low

num_shift:

* < 1 (invalid)
* = 1
* 1

dir_shift:

* +1
* -1
* invalid values (0, 2, -2)

## Input Partition Testing Implementation

The IPT model is defined above and implemented using applied base-choice coverage.

Test Suite: 
testing/input-partition-models/test_encrypt_partition.py

The test suite includes:

* base case (valid input), a normal, valid case
* non-ASCII error case
* num_shift invalid case
* forbidden character case
* wrap-around-high case
* wrap-around-low case
* invalid dir_shift case (demonstrates defect)

These test cases check each input category and also help show the issue with dir_shift. 

Coverage Requirements

* Node coverage: All of the nodes are visited. N1-N19 must be visited, except N7 (infeasible)
* Edge coverage: All of the edges are covered except: (N6 -> N7), which is infeasible
* Prime paths: All feasible prime paths listed in the prime path table are covered. The path through N6 -> N7 is excluded due to infeasibility.

## Note

The condition at N6 contains a logic error. As written, N6 does not prevent invalid dir_shift values from passing through. 

Values such as 0, 2, and -2 are accepted without raising an error, which indicates that the validation is ineffective. 


## Baseline test results

There are 60 total statements, with 34 missed or not covered, giving a module_level coverage result of 42% for auth.py. The baseline test mainly exercises the _encrypt function. 

There are 26 branches and 4 are partially covered. 

Baseline test only exercised normal ASCII path , non_ASCII error, num_shift guard, and standard transformation. 

They did not cover:
Missing 33,37, 50, 52, 63-78, 95-118

Missing:
Forbidden character
Wrap around high
Wrap around low
multi-character loop paths
part of login/register

auth.py file covers `login()` and `register()`, and `_encrypt`, which indicates that the baseline covers 42% statement coverage and partial branch coverage of the auth module.

Coverage is limited in the baseline test. The test were focus on expected behavior and basic error handling. There are many paths in the CFG that are not exercised. 

Several paths are still missing from the baseline tests. This mainly includes the wrap-around high/low cases and paths where the loop runs more than once. 

The uncovered cases and paths call for additional structural tests that are needed. 

## Structural test results

Command executed:

PYTHONPATH=backend python -m pytest testing/structural-test/test_app_encrypt_structural.py 
–cov=app.routes.auth 
–cov-branch 
–cov-report=term-missing | tee testing/coverage-reports/auth-encrypt-structural-coverage.txt

Observed result:

* collected 9 items
* 9 passed

Out of 60 statements, 31 were not covered. There are 26 branches, with 1 partially covered giving a total coverage of 49%.  

Missing lines reported: 33, 63-78, 95-118

Interpretation:

Coverage increased from 42% to 49% at the module level for auth.py. 

The uncovered lines are outside of _encrypt(), mainly in login() and register(), which are not part of this structural test scope. 


Structural testing of _encrypt() achieved full feasible coverage of nodes, edges, and prime paths. 

The only uncovered _encrypt line is the raise at line 33, which is tied to an unsatisfiable predicate (dir_shift < -1 AND dir_shift > 1) and is therefore infeasible by logic. 

Remaining uncovered lines in module coverage belong to login() and register(), not _encrypt().

## Alignment with Structural Testing Results

Structural testing was successfully implemented for the _encrypt() function.

The test suite achieved:

* Full feasible node coverage
* Full feasible edge coverage (excluding infeasible edge N6 -> N7)
* Full prime path coverage (P1-P7)

Coverage results show improvement from baseline (42%) to structural testing (49%) at the module level. The remaining uncovered lines belong to login() and register() and are outside the scope of _encrypt() structural testing.

This confirms that the structural test suite meets all graph-based coverage requirements defined in the project objectives.

## Final Structural Interpretation and Conclusion

Observed result:

* collected 9 items
* 9 passed
* auth.py coverage summary: 60 statements, 31 missed, 26 branches, 1 partial branch, 49% total coverage
* Missing lines reported: 33, 63-78, 95-118

Interpretation:

* Structural tests improved module-level coverage from 42% (baseline) to 49%.
* All feasible nodes (N1-N19 except N7), edges (E1-E21 except E6), and prime paths (P1-P7) for _encrypt() are covered.
* Edge E6 (N6 -> N7) is excluded due to infeasibility.
* The remaining uncovered lines belong to login() and register(), which are outside the scope of _encrypt() structural testing.

Conclusion:

* The structural test suite achieves 100% feasible node coverage for _encrypt().
* The structural test suite achieves 100% feasible edge coverage for _encrypt().
* The structural test suite achieves 100% feasible prime path coverage for _encrypt().
* The only uncovered branch corresponds to an unsatisfiable predicate and is correctly excluded.

### How to run structural tests

From repository root:

PYTHONPATH=backend python -m pytest testing/structural-test/test_app_encrypt_structural.py -v -s

With coverage report file output:

PYTHONPATH=backend python -m pytest testing/structural-test/test_app_encrypt_structural.py 
–cov=app.routes.auth 
–cov-branch 
–cov-report=term-missing | tee testing/coverage-reports/auth-encrypt-structural-coverage.txt

Partition Testing Coverage Results

Command executed:

PYTHONPATH=backend python -m pytest testing/input-partition-models/test_encrypt_partition.py 
–cov=app.routes.auth 
–cov-branch 
–cov-report=term-missing

Results:

* Partition testing exercised key input categories.
* Covered error cases (non-ASCII, invalid num_shift)
* Covered boundary behaviors (wrap-high, wrap-low)
* Exposed defect in dir_shift validation

Interpretation:

* Partition testing improves behavioral coverage.
* Complements structural testing by focusing on input diversity


TODO: Add new version and date and explanation for 1.7 

### Base Choice Coverage

The Base Choice Coverage tests achieved 49% statement coverage of all `auth.py`. 

The uncovered lines corresponds to: 
- the infeasible branch associated withe the predicate (dir_shift < -1 AND dir_shift > 1)
- the unrelated functionality in the module includes `login()`, and `register()` routes. 

Within the `_encrypt()` function all feasible branches and behaviors were exercised by the test suite. 

update as needed
