# Base Choice Coverage Test Frames — `_encrypt()`

Coverage criterion: Base Choice Coverage (BCC)
IDM reference: encrypt_idm.md

In Base Choice Coverage only one characteristic should change per test. 

## Base Choice Selection

| Characteristic | Base Block | Rationale |
|---------------|-----------|-----------|
| C1 — input_text | b1 (ASCII valid) | normal valid string |
| C2 — num_shift | b2 (=1) | simplest valid shift |
| C3 — dir_shift | b1 (+1) | normal direction |

## Base Test Frame

BT — Base test (C1:b1, C2:b2, C3:b1)

| Input | Value |
|------|-------|
| input_text | "mypassword" |
| num_shift | 1 |
| dir_shift | 1 |

Expected:
- Returns a valid encrypted string
- Output length equals input length.

### Varying C1 — input_text

T1 — C1:b2 (non-ASCII)

| Input | Value |
|------|-------|
| input_text | "mypasswordé" |
| num_shift | 1 |
| dir_shift | 1 |

Expected:
- TypeError raised

T2 — C1:b3 (forbidden characters)

| Input | Value |
|------|-------|
| input_text | "pass word!#" |
| num_shift | 1 |
| dir_shift | 1 |

Expected:
- ValueError raised

T3 — C1:b4 (wrap-around-high)

| Input | Value |
|------|-------|
| input_text | "~" |
| num_shift | 1 |
| dir_shift | 1 |

Expected:
- Returns an encrypted string of the same length
- Wrap-around behavior occurs

T4 — C1:b5 (wrap-around-low)

| Input | Value |
|------|-------|
| input_text | "#" |
| num_shift | 1 |
| dir_shift | 1 |

Expected:
-  rReturns a valid encrypted string
- Wrap-around behavior occurs

### Varying C2 — num_shift

T5 — C2:b1 (<1)

| Input | Value |
|------|-------|
| input_text | "mypassword" |
| num_shift | 0 |
| dir_shift | 1 |

Expected:
- ValueError raised

### Varying C3 — dir_shift

T6 — C3:b3 (invalid dir_shift)

| Input | Value |
|------|-------|
| input_text | "mypassword" |
| num_shift | 1 |
| dir_shift | 2 |

Expected:
- Should raise ValueError

Observed:
- Function executes normally

Conclusion:
- This exposes a defect in validation logic

T7 - C1:b6 (Empty string)

| Input | Value |
|------|-------|
| input_text | "" |
| num_shift | 1 |
| dir_shift | 1 |

Expected:
- returns an empty string
- the loop is not executed

Observed:
- The function returns an empty string

Conclusion:
- The test confirms correct handling of an empty input
- The loop body is not executed when an input is empty. 


## Summary

| Test | C1 | C2 | C3 | Expected |
|------|----|----|----|----------|
| BT | b1 | b2 | b1 | valid |
| T1 | b2 | b2 | b1 | TypeError |
| T2 | b3 | b2 | b1 | ValueError |
| T3 | b4 | b2 | b1 | valid |
| T4 | b5 | b2 | b1 | valid |
| T5 | b1 | b1 | b1 | ValueError |
| T6 | b1 | b2 | b3 | BUG (should fail) |
| T7 | b6 | b2 | b1 | valid |