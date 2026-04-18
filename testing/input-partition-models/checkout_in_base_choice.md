# Base Choice Coverage Test Frames — `checkout_hardware` & `checkin_hardware`

Coverage criterion: Base Choice Coverage (BCC)
IDM reference: `checkout_in_idm.md`

In Base Choice Coverage, one characteristic changes per non-base test while all others remain at the base choice. This ensures that each non-base block is exercised in isolation, holding all other factors constant.

BCC formula: `1 + Σ(|bi| − 1) = 1 + (5−1) + (2−1) + (2−1) = 8 tests`

## Base Choice Selection

| Characteristic | Base Block | Reasoning |
|---|---|---|
| C1 — `amount` | b3 (amount = 1) | Minimum valid amount — exercises the normal checkout path without triggering Pydantic or availability errors |
| C2 — `userId` | b1 (assigned) | Authorized user — allows execution to proceed past the auth check at N10 |
| C3 — `projectId` | b1 (valid) | Existing project — allows execution to proceed past the DB lookup at N8 |

---

## Base Test Frame

**T-ISP-CO-BASE** — (C1:b3, C2:b1, C3:b1) — checkout_hardware

| Input | Value |
|---|---|
| `amount` | 1 |
| `userId` | "test-user" (present in `assignedUsers`) |
| `projectId` | "test-project" (exists in DB) |
| `hardware` | available=10, capacity=10 |

Expected:
- 200 OK
- `available` decremented to 9 (10 − 1)
- `projectId` appears in hardware's `assignedProjects`

---

## Varying C1 — `amount`

### T-ISP-CO-C1-b1 — C1:b1 (amount negative)

| Input | Value |
|---|---|
| `amount` | -2 |
| `userId` | (any — not reached) |
| `projectId` | (any — not reached) |

Expected:
- 400 `{"error": "Validation failed"}`

Notes:
- Pydantic `HardwareCheckout` enforces `amount >= 1`; `-2` fails immediately at N2
- Neither C2 nor C3 is evaluated — DB is never queried

---

### T-ISP-CO-C1-b2 — C1:b2 (amount zero)

| Input | Value |
|---|---|
| `amount` | 0 |
| `userId` | (any — not reached) |
| `projectId` | (any — not reached) |

Expected:
- 400 `{"error": "Validation failed"}`

Notes:
- `0` is the lower domain boundary; Pydantic still rejects it (`amount >= 1` required)
- Same N2 termination as b1 — no DB interaction

---

### T-ISP-CO-C1-b4 — C1:b4 (amount == available, exact capacity)

| Input | Value |
|---|---|
| `amount` | 5 |
| `userId` | "test-user" |
| `projectId` | "test-project" |
| `hardware` | available=5, capacity=5 |

Expected:
- 200 OK
- `available` becomes 0 (all units checked out)

Notes:
- Guard condition: `hw["available"] < body.amount` -> `5 < 5` -> False -> checkout proceeds
- Confirms off-by-one: exact capacity is allowed, not blocked

---

### T-ISP-CO-C1-b5 — C1:b5 (amount > available, over capacity)

| Input | Value |
|---|---|
| `amount` | 8 |
| `userId` | "test-user" |
| `projectId` | "test-project" |
| `hardware` | available=5, capacity=10 |

Expected:
- 400 `{"error": "Insufficient availability. Only 5 units available"}`

Notes:
- Guard condition: `5 < 8` -> True -> guard fires, checkout blocked
- Only 5 units available; request for 8 exceeds stock

---

## Varying C2 — `userId`

### T-ISP-CO-C2-b2 — C2:b2 (user not assigned)

| Input | Value |
|---|---|
| `amount` | 1 |
| `userId` | "outsider-user" (absent from `assignedUsers`) |
| `projectId` | "test-project" |
| `hardware` | available=10, capacity=10 |

Expected:
- 403 `{"error": "User is not assigned to this project"}`

Notes:
- Project is found (C3=b1), so execution reaches the auth check at N10
- `"outsider-user"` is not in `assignedUsers` -> N10 True branch -> 403

---

## Varying C3 — `projectId`

### T-ISP-CO-C3-b2 — C3:b2 (project not in DB)

| Input | Value |
|---|---|
| `amount` | 1 |
| `userId` | (any — not reached) |
| `projectId` | "ghost-project" (no matching document) |

Expected:
- 404 `{"error": "Project not found"}`

Notes:
- Project lookup at N8 fails -> N9 (404) returned immediately
- C2 is unobservable: auth check at N10 is never reached when C3=b2

---

## checkin_hardware — Base Test Frame

**T-ISP-CI-BASE** — (C1:b3, C2:b1, C3:b1) — checkin_hardware

| Input | Value |
|---|---|
| `amount` | 1 |
| `userId` | "test-user" (present in `assignedUsers`) |
| `projectId` | "test-project" (exists in DB) |
| `hardware` | available=7, capacity=10 |
| `assignedHardware entry` | `{hardwareId: hw_id, amount: 3}` |

Expected:
- 200 OK
- `available` incremented to 8 (7 + 1)
- Project entry amount decremented to 2 (3 − 1, partial checkin)

Notes:
- The same IDM and BCC base apply to `checkin_hardware`
- Amount=1 is less than entry amount=3 -> partial checkin path (N15 False -> N16 `$inc`)
- Full non-base BCC deviation tests for checkin follow the same structure as checkout

---

## BCC Summary Table

| Test | C1 | C2 | C3 | Input Values | Expected |
|---|---|---|---|---|---|
| T-ISP-CO-BASE | b3 | b1 | b1 | amount=1, assigned, valid project | 200; available=9 |
| T-ISP-CO-C1-b1 | b1 | — | — | amount=-2 | 400 ValidationError |
| T-ISP-CO-C1-b2 | b2 | — | — | amount=0 | 400 ValidationError |
| T-ISP-CO-C1-b4 | b4 | b1 | b1 | amount=5, available=5 | 200; available=0 |
| T-ISP-CO-C1-b5 | b5 | b1 | b1 | amount=8, available=5 | 400 Insufficient |
| T-ISP-CO-C2-b2 | b3 | b2 | b1 | amount=1, outsider user | 403 Unauthorized |
| T-ISP-CO-C3-b2 | b3 | — | b2 | amount=1, ghost project | 404 Project not found |
| T-ISP-CI-BASE | b3 | b1 | b1 | amount=1, assigned, valid project (checkin) | 200; available=8 |

### ECC Subsumption

Each Choice Coverage (ECC) requires that each block appears in at least one test. BCC subsumes ECC because the 8 BCC tests cover:
- All 5 `amount` blocks (b1–b5 each appear at least once)
- Both `userId` blocks (b1 in most tests, b2 in T-ISP-CO-C2-b2)
- Both `projectId` blocks (b1 in most tests, b2 in T-ISP-CO-C3-b2)
