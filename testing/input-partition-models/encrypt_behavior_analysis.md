# Implementation Behavior Analysis - `_encrypt()`

Source: `backend/app/routes/auth.py`
IDM reference: `encrypt_idm.md`

This sections maps each input partition block to the observed behavior in the current implementation and identifies where behavior diverges from the expected validation. 

## C1 - input_text

What is the content and character validity of `input_text`?
| Block | Input | Observed | Intended | Diverges? |
|------|------------|---------|---------------|---------------|
| b1 | "mypassword" | Returns encrypted string | Valid execution | No |
| b2 | "mypasswordé" | Raises TypeError | Raises TypeError | No |
| b3 | "pass word!#" | Raises ValueError | Raises ValueError  | No |
| b4 | "~" | Returns encrypted string with wrap-around | Valid wrap-high behavior | No |
| b5 | "#" | Returns encrypted string with wrap-around | Valid wrap-low behavior | No |
| b6 |  "" | Returns empty string| Returns empty string | No |


## C2 - num_shift

What is the value of `num_shift` relative to validity constraints?

| Block | Input | Observed | Intended | Diverges? |
|------|------------|---------|---------------|---------------|
| b1 | 0 | Raises ValueError | Raises ValueError  | No |
| b2 | 1 | Normal execution | Valid execution | No |
| b3 | 10 | Normal execution | Valid execution | No |

## C3 - dir_shift

What is the direction and validity of `dir_shift`? 

| Block | Input | Observed | Intended | Diverges? |
|------|------------|---------|---------------|---------------|
| b1 | 1 | Normal execution | Valid execution | No |
| b2 | -1 | Normal execution | Valid execution | No |
| b3 | 2 | No error raised | Should raise ValueError | Yes | 

## Summary of Defects

| Block | Root Cause |
|------|------------|
| C3:b3 | Predicate `(dir_shift < -1 AND dir_shift > 1)` is unsatisfiable, the invalid values are not rejected |

 ## Behavioral Conclusion 

 The `_encrypt()` function correctly handles: 
 - ASCII validation 
 - forbidden character detection 
 - wrap-around logic
 - empty input handling 

However, the validation for `dir_shift` is incorrect. Due to an unsatisfiable predicate, invalid values are accepted instead of raising an ValueError.