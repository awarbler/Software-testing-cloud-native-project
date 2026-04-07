# CACC Analysis for _encrypt()

## Predicate

The selected predicate is: 

P = (dir_shift < -1) AND (dir_shift > 1)

Clauses: 

A = (dir_shift < -1)

B = (dir_shift > 1)

This predicate was selected because it contains a logic defect

## Goal

Apply Correlated Active Clause Coverage(CACC)

Requirement: 

Each clause must independently determine the predicate outcome. That means:
- We must find test cases where flipping one clause changes the value of P.


## Feasibility Analysis 
Before applying CACC, the predicate was analyzed to determine whether it can evaluate to TRUE.

Clause A requires: (dir_shift < -1)

Clause B requires: (dir_shift > 1)

These conditions cannot be satisfied at the same time. 

Therefore:
- There is **no value of dir_shift** that makes both A and B TRUE
- So P can never evaluate to TRUE

This means the predicate is unsatisfiable, and the TRUE branch is infeasible

## Clause A Analysis 

Test 1: 
dir_shift = -2
A = TRUE
B = FALSE
P = FALSE 

Test 2: 
dir_shift = 0
A = FALSE
B = FALSE
P = FALSE 

### Table
| dir_shift | A | B | P |
|----------|---|---|---|
| -2       | T | F | F |
| 0        | F | F | F |

Result:

Flipping A does not change P -> A does NOT determine P

## Clause B Analysis

Test 1: 
dir_shift = 2
A = FALSE
B = TRUE
P = FALSE 

Test 2: 
dir_shift = 0
A = FALSE
B = FALSE
P = FALSE 

### Table 
| dir_shift | A | B | P |
|----------|---|---|---|
| 2        | F | T | F |
| 0        | F | F | F |

Result: 

Flipping B does not change P -> B does NOT determine P

## Why CACC Fails

CACC requires that:
- For each clause, we can find test cases where flipping the clause changes the predicate outcome

However:
- P is always FALSE for all inputs
- There is no test case where P becomes TRUE

Because of this:
- It is impossible for any clause to affect the outcome of P
- Therefore, CACC cannot be satisfied


## Conclusion 

No value of dir_shift can satisfies both clauses simultaneously.

Therefore: 
- Predicate P is always FALSE
- TRUE branch is infeasible 
- CACC cannot be satisfied 

This indicates a logical defect in the code. The condition is incorrectly written and can never evaluate to TRUE.

The coverage report confirms that the branch corresponding to the predicate 
(dir_shift < -1 AND dir_shift > 1) is not executed.

This aligns with the CACC analysis, which proved that the predicate is 
unsatisfiable. As a result, the TRUE branch is infeasible and cannot be covered 
by any test case.

## Coverage Results

The coverage results for the CACC tests are saved in:

coverage_reports/encrypt_cacc_coverage.txt

Summary:

- Statement Coverage: 37%
- Branch Coverage: Partial (incomplete due to infeasible branch)
- Several branches remain uncovered

These uncovered branches correspond to the predicate:
(dir_shift < -1 AND dir_shift > 1) which was proven to be infeasible during CACC analysis.

This demonstrates that logical analysis (CACC) is necessary to identify infeasible paths that cannot be revealed through coverage metrics alone.