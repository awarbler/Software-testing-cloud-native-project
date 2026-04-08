# Input Domain Model- `_encrypt()`

## Partition Rules

1. Base the partitions on characteristics input behavior.
2. Each block needs to lead to a different branch/ path or trigger a different error. 
3. Disjoint and complete. The blocks cannot overlap (disjoint) and must cover all possibilities(complete). 

The IDM will define the blocks, choose the representative values, and combine the values into test cases. (ee382c16-260220-Chapter4.pdf)

## Characteristics 

| Characteristic  |Parameter  | Type   | Description |
| ------          |---------- | ------ | ------ |
| C1              |input_text | string | partition is based on ASCII validity, forbidden characters and wrap behavior|
| C2              |num_shift  | int    | partition is based on the validity and boundary values|
| C3              |dir_shift  | int    |partition is based on the direction and invalid values |

### C1 — input_text

What is the content and character validity of input_text?

| Block | Description | Example | Behavior / Coverage Impact |
|------|------------|---------|-----------------------------|
| b1 | ASCII valid (normal execution) | "mypassword" | Exercises normal execution path |
| b2 | Non-ASCII | "mypasswordé" | Triggers TypeError (B1) |
| b3 | Contains forbidden characters | "pass word!#" | Triggers ValueError (B4) |
| b4 | Causes wrap-high | "~" | Exercises branch B5 (wrap-high) |
| b5 | Causes wrap-low | "#" | Exercises branch B6 (wrap-low) |
| b6 | Empty String | "" | Exercises loop exit edge case |

### C2 — num_shift

What is the numeric value of num_shift relative to validity constraints? 

| Block | Description | Example | Behavior / Coverage Impact |
|------|------------|---------|---------|
| b1 | < 1 (invalid) | 0 | Triggers ValueError (B2)|
| b2 | = 1 | 1 | Boundary valid case |
| b3 | > 1 | 10 | Normal valid execution |

### C3 — dir_shift

What is the direction and validity of dir_shift? 

| Block | Description | Example |Behavior / Coverage Impact |
|------|------------|---------|---------|
| b1 | +1 (valid) | 1 | Forward shift behavior |
| b2 | -1 (valid) | -1 | Reverse shift behavior |
| b3 | invalid values (not properly validated) | 2| Demonstrates logic defect - predicate  unsatisfiable predicate (B3) |