# Input Domain Model — `checkout_hardware` & `checkin_hardware`

Source: `backend/app/routes/hardware.py`
Test suite: `testing/input-partition-models/test_checkout_in_partition.py`

## Partition Rules

1. Base partitions on characteristic input behavior — each block must lead to a distinct branch, path, or error.
2. Blocks must be disjoint (no overlap) and complete (cover all meaningful values for the characteristic).
3. Characteristics are defined from a functionality-based perspective, not from code structure.

The IDM defines the blocks, chooses representative values, and provides the structure for combining values into test cases using BCC.

## Characteristics

| Characteristic | Parameter | Type | Description |
|---|---|---|---|
| C1 | `amount` | int | Partition based on numeric value relative to Pydantic constraints and available stock |
| C2 | `userId` | string | Partition based on whether the requesting user is authorized for the project |
| C3 | `projectId` | string | Partition based on whether the project document exists in the database |

---

### C1 — `amount` value

What is the numeric value of `amount` relative to validity constraints and available stock?

| Block | Description | Example | Behavior / Coverage Impact |
|---|---|---|---|
| b1 | negative (< 0) | -2 | Pydantic rejects at N2 — ValidationError before any DB lookup |
| b2 | zero (== 0) | 0 | Pydantic rejects at lower domain boundary — ValidationError |
| b3 | one (== 1, min valid) | 1 | Minimum valid amount — normal checkout/checkin execution path |
| b4 | exact capacity (== available) | 5 | Boundary valid case — availability guard evaluates to False, checkout proceeds |
| b5 | over capacity (> available) | 8 | Availability guard fires — request rejected |

**Notes:**
- b1 and b2 are infeasible at the availability guard (N11/N13) because Pydantic enforces `amount >= 1` at N2. Any test with C1=b1 or C1=b2 terminates at N2 and never exercises C2 or C3.
- b4 is the off-by-one boundary: the guard condition is `hw["available"] < body.amount`, so `amount == available` evaluates the guard to False and checkout proceeds.
- b5 confirms the guard correctly fires when `amount > available`.

---

### C2 — `userId` authorization

Is the requesting user assigned to the project?

| Block | Description | Example | Behavior / Coverage Impact |
|---|---|---|---|
| b1 | assigned (base) | "test-user" (present in `assignedUsers`) | Authorization check at N10 passes — execution continues to availability guard |
| b2 | not assigned | "outsider-user" (absent from `assignedUsers`) | Authorization check at N10 fails — 403 Unauthorized |

**Notes:**
- C2 is only observable when C3=b1. If the project is not found (C3=b2), execution terminates at N9 before the auth check at N10 is reached.

---

### C3 — `projectId` existence

Does the referenced project exist in the database?

| Block | Description | Example | Behavior / Coverage Impact |
|---|---|---|---|
| b1 | valid (base) | "test-project" (document found in DB) | Project lookup at N8 succeeds — execution continues to auth check |
| b2 | invalid | "ghost-project" (no matching document) | Project lookup at N8 fails — 404 Project not found |

**Notes:**
- When C3=b2, the C2 characteristic is unobservable (constraint: auth check is unreachable if project not found).
- C3=b2 exercises prime path PP4 in both `checkout_hardware` and `checkin_hardware`.

---

## Constraints Summary

| Constraint | Reason |
|---|---|
| C1=b1 or C1=b2 -> C2 and C3 not observable | Pydantic rejects before any DB lookup |
| C3=b2 -> C2 not observable | Auth check only reached after project is found |
| C1=b4, C1=b5 require C3=b1 and C2=b1 | Availability guard only reached after auth passes |
