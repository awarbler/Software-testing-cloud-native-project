# Implementation Behavior Analysis — `checkout_hardware` & `checkin_hardware`

Source: `backend/app/routes/hardware.py`
IDM reference: `checkout_in_idm.md`
BCC reference: `checkout_in_base_choice.md`

This section maps each input partition block to the observed behavior in the current implementation and identifies whether any behavior diverges from what is intended.

---

## C1 — `amount` value

What is the numeric value of `amount` relative to validity constraints and available stock?

| Block | Input | Observed | Intended | Diverges? |
|---|---|---|---|---|
| b1 | amount=-2 | 400 `{"error": "Validation failed"}` | Pydantic rejects before DB lookup | No |
| b2 | amount=0 | 400 `{"error": "Validation failed"}` | Pydantic rejects at lower boundary | No |
| b3 | amount=1 | 200 OK; available decremented | Normal checkout/checkin proceeds | No |
| b4 | amount=5, available=5 | 200 OK; available=0 | Guard passes; all units checked out | No |
| b5 | amount=8, available=5 | 400 "Insufficient availability. Only 5 units available" | Availability guard fires | No |

---

## C2 — `userId` authorization

Is the requesting user assigned to the project?

| Block | Input | Observed | Intended | Diverges? |
|---|---|---|---|---|
| b1 | assigned user ("test-user") | Execution proceeds past auth check | Auth check passes | No |
| b2 | unassigned user ("outsider-user") | 403 "User is not assigned to this project" | Auth check blocks request | No |

---

## C3 — `projectId` existence

Does the referenced project exist in the database?

| Block | Input | Observed | Intended | Diverges? |
|---|---|---|---|---|
| b1 | valid project ("test-project") | Project lookup succeeds; execution continues | Normal path | No |
| b2 | invalid project ("ghost-project") | 404 "Project not found" | DB lookup fails; error returned | No |

---

## checkin_hardware — Additional Blocks

The checkin function shares the same C1/C2/C3 structure but adds a checkin-specific guard. The base test (T-ISP-CI-BASE) verifies partial checkin behavior.

| Input | Observed | Intended | Diverges? |
|---|---|---|---|
| amount=1, entry=3 (partial checkin) | 200 OK; available=8; entry decremented to 2 | Partial checkin: `$inc` decrements entry amount | No |

---

## Summary of Defects

No defects were found for the tested partitions in `checkout_hardware` or `checkin_hardware`.

| Block | Root Cause | Status |
|---|---|---|
| All C1 blocks | — | Correct |
| All C2 blocks | — | Correct |
| All C3 blocks | — | Correct |

---

## Coverage Gap Notes

The BCC test suite (8 tests) exercises the following prime paths from the CFG:

| Test | Prime Path(s) Covered |
|---|---|
| T-ISP-CO-BASE | PP10 (N13 False -> $push -> 200) |
| T-ISP-CO-C1-b1 | PP1 (ValidationError at N2) |
| T-ISP-CO-C1-b2 | PP1 (ValidationError at N2) |
| T-ISP-CO-C1-b4 | PP10 (N13 False -> $push -> 200, available=0) |
| T-ISP-CO-C1-b5 | PP6 (availability guard fires -> 400) |
| T-ISP-CO-C2-b2 | PP5 (auth check fails -> 403) |
| T-ISP-CO-C3-b2 | PP4 (project not found -> 404) |
| T-ISP-CI-BASE | PP11 (partial checkin -> $inc -> 200) |

Prime paths PP2 (invalid ObjectId), PP3 (hardware not found), PP7 (over-checkin), PP8/PP9 (500 paths), and PP6/PP9 (full checkin, $pull paths) are not exercised by the ISP suite. These are covered by the structural test suite in `testing/structural-test/test_checkout_in_structural.py`.

---

## Behavioral Conclusion

The `checkout_hardware` and `checkin_hardware` functions correctly handle all tested input partition blocks:

- **Pydantic validation**: Correctly rejects `amount <= 0` at N2 before any DB interaction
- **Availability guard**: Correctly permits checkout at exact capacity and rejects requests over capacity
- **Authorization**: Correctly blocks users absent from `assignedUsers`
- **Project existence**: Correctly returns 404 for non-existent projects
- **Partial checkin**: Correctly decrements entry amount and increments available count

All 8 BCC test cases pass with no behavioral divergence identified across the tested partition blocks.
