# CACC Analysis for checkout_hardware & checkin_hardware

## Predicate

The selected predicate governs the availability guard in both functions:

```
p = (amount > 0) AND (amount <= bound)
```

Where `bound` is:
- `hw["available"]` — in `checkout_hardware` (guard at N11)
- `entry["amount"]` — in `checkin_hardware` (guard at N13)

Clauses:

```
c1 = (amount > 0)
c2 = (amount <= bound)
```

This predicate was selected because it directly controls whether a checkout or checkin operation is permitted. The two clauses correspond to distinct validation concerns: `c1` enforces that a non-zero amount is requested, and `c2` enforces that the requested amount does not exceed what is available.

---

## Goal

Apply Correlated Active Clause Coverage (CACC).

Requirement:

Each clause must independently determine the predicate outcome. That means:
- For each clause `ci`, we must find test pairs where flipping `ci` (while holding all other clauses fixed at the determination condition) changes the value of `p`.

---

## Determination Conditions

For conjunction `p = c1 ∧ c2`, a clause is *active* (determines `p`) under the following conditions:

| Major Clause | Determination Condition | Effect |
|---|---|---|
| c1 major | c2 = TRUE | `p[c1=T] = T`, `p[c1=F] = F` — c1 determines p |
| c2 major | c1 = TRUE | `p[c2=T] = T`, `p[c2=F] = F` — c2 determines p |

---

## c2 as Major Clause (c1 = TRUE is the determination condition)

Since Pydantic enforces `amount >= 1` before execution reaches the guard nodes, `c1` is always TRUE at N11/N13. This makes `c2` the only active clause in practice.

### Test Pair (c2 major, checkout)

**Test T-CACC-CO-01** — `{c1=T, c2=T}` -> `p=T`

| Input | c1 = (amount > 0) | c2 = (amount <= available) | p |
|-------|-------------------|----------------------------|---|
| amount=3, available=10 | TRUE (3 > 0) | TRUE (3 <= 10) | TRUE |

Result: p = TRUE -> N11 False branch -> checkout proceeds -> 200 OK

---

**Test T-CACC-CO-02** — `{c1=T, c2=F}` -> `p=F`

| Input | c1 = (amount > 0) | c2 = (amount <= available) | p |
|-------|-------------------|----------------------------|---|
| amount=7, available=5 | TRUE (7 > 0) | FALSE (7 <= 5 is False) | FALSE |

Result: p = FALSE -> N11 True branch -> 400 Insufficient availability

---

### CACC Determination Check (c2 major)

| Test | c1 | c2 | p | c2 determines p? |
|------|----|----|---|-----------------|
| T-CACC-CO-01 | T | T | T | — |
| T-CACC-CO-02 | T | F | F | Yes — flipping c2 changes p |

**c2 determines p** when c1 = TRUE (determination condition satisfied).

CACC for c2 as major clause: **SATISFIED**

---

## c1 as Major Clause (c2 = TRUE is the determination condition)

The CACC test pair for c1 as major clause requires:
- `{c1=T, c2=T}` -> `p=T` (feasible)
- `{c1=F, c2=T}` -> `p=F` (infeasible at guard node)

### Feasibility Analysis

**c1=F** requires `amount <= 0` (i.e., amount = 0 or negative).

However, `HardwareCheckout` and `HardwareCheckin` both enforce `amount >= 1` via Pydantic validation at node N2. If `amount <= 0` is submitted, execution terminates at N2 with a ValidationError and never reaches the guard nodes N11/N13.

Therefore:
- At N11 (checkout guard): `c1 = (amount > 0)` is **always TRUE** — Pydantic guarantees it
- At N13 (checkin guard): same guarantee applies
- The test pair `{c1=F, c2=T}` **cannot be constructed** at the guard nodes

The CACC test pair for c1 major is **structurally infeasible** at the availability guard. This is not a test limitation — it is a consequence of the Pydantic constraint that runs before the guard is reached.

### Infeasibility Table (c1 major)

| Test | c1 | c2 | p | Feasible at guard? |
|------|----|----|---|-------------------|
| `{c1=T, c2=T}` -> p=T | T | T | T | Yes |
| `{c1=F, c2=T}` -> p=F | F | T | F | **No — Pydantic blocks c1=F at N2** |

---

## c1=F at the Pydantic Boundary (N2)

Although `c1=F` is infeasible at the guard nodes, it **is** observable at the Pydantic validation node N2. These tests document the behavior and satisfy Clause Coverage (CC) for c1=F at the earliest reachable point.

### Test T-CACC-CO-03 (checkout, amount=0)

| Input | c1 = (amount > 0) | c2 | p |
|-------|-------------------|----|---|
| amount=0 | FALSE (0 > 0 is False) | not evaluated | FALSE (at N2) |

Result: Pydantic raises ValidationError at N2 -> 400 `{"error": "Validation failed"}`. Execution never reaches N11.

### Test T-CACC-CI-03 (checkin, amount=-1)

| Input | c1 = (amount > 0) | c2 | p |
|-------|-------------------|----|---|
| amount=-1 | FALSE (-1 > 0 is False) | not evaluated | FALSE (at N2) |

Result: Pydantic raises ValidationError at N2 -> 400 `{"error": "Validation failed"}`. Execution never reaches N13.

---

## c2 as Major Clause (checkin)

The same CACC analysis applies to `checkin_hardware`, where `bound = entry["amount"]` (units already checked out for the project).

### Test T-CACC-CI-01 — `{c1=T, c2=T}` -> `p=T`

| Input | c1 = (amount > 0) | c2 = (amount <= entry) | p |
|-------|-------------------|------------------------|---|
| amount=2, entry=3 | TRUE (2 > 0) | TRUE (2 <= 3) | TRUE |

Result: p = TRUE -> N13 False branch -> checkin proceeds -> 200 OK; available = 9 (7+2)

---

### Test T-CACC-CI-02 — `{c1=T, c2=F}` -> `p=F`

| Input | c1 = (amount > 0) | c2 = (amount <= entry) | p |
|-------|-------------------|------------------------|---|
| amount=5, entry=3 | TRUE (5 > 0) | FALSE (5 <= 3 is False) | FALSE |

Result: p = FALSE -> N13 True branch -> 400 "Cannot check in 5 units. Only 3 checked out"

---

### CACC Determination Check (c2 major, checkin)

| Test | c1 | c2 | p | c2 determines p? |
|------|----|----|---|-----------------|
| T-CACC-CI-01 | T | T | T | — |
| T-CACC-CI-02 | T | F | F | Yes — flipping c2 changes p |

CACC for c2 as major clause (checkin): **SATISFIED**

---

## Boundary Value: c2 at Exact Boundary (T-CACC-CO-04)

Test T-CACC-CO-04 reinforces the `{c1=T, c2=T}` requirement at the exact boundary of c2:

| Input | c1 = (amount > 0) | c2 = (amount <= available) | p |
|-------|-------------------|----------------------------|---|
| amount=5, available=5 | TRUE (5 > 0) | TRUE (5 <= 5) | TRUE |

Result: p = TRUE at the off-by-one boundary -> checkout proceeds -> 200 OK; available = 0

This confirms the guard uses `<` (strict less-than) not `<=`, so checking out the exact available quantity is permitted.

---

## Full CACC Coverage Summary

| Test ID | Function | Major Clause | c1 | c2 | p | Coverage |
|---------|----------|-------------|----|----|---|---------|
| T-CACC-CO-01 | checkout | c2 major | T | T | T | PC(p=T), CC(c2=T), CACC(c2 pair 1) |
| T-CACC-CO-02 | checkout | c2 major | T | F | F | PC(p=F), CC(c2=F), CACC(c2 pair 2) |
| T-CACC-CO-03 | checkout | c1 major | F | — | F | CC(c1=F at N2) — infeasible at N11 |
| T-CACC-CO-04 | checkout | c2 boundary | T | T | T | CACC(c2=T boundary off-by-one) |
| T-CACC-CI-01 | checkin | c2 major | T | T | T | PC(p=T), CC(c2=T), CACC(c2 pair 1) |
| T-CACC-CI-02 | checkin | c2 major | T | F | F | PC(p=F), CC(c2=F), CACC(c2 pair 2) |
| T-CACC-CI-03 | checkin | c1 major | F | — | F | CC(c1=F at N2) — infeasible at N13 |

---

## Why CACC for c1 Major Cannot Be Fully Satisfied

CACC requires that for c1 as major clause:
- Test pair `{c1=T, c2=T}` -> p=T (feasible — any normal checkout)
- Test pair `{c1=F, c2=T}` -> p=F (infeasible at guard — Pydantic prevents c1=F from reaching N11/N13)

Because `HardwareCheckout`/`HardwareCheckin` enforce `amount >= 1`:
- Any input with `amount <= 0` raises a ValidationError at N2
- Execution terminates before the availability guard is evaluated
- There is no test input that makes `c1=F` at N11 or N13

**CACC for c1 as major clause is structurally infeasible.** The code design (Pydantic pre-validation) prevents this clause from ever being false at the guard node — which is architecturally correct behavior.

---

## Conclusion

| Coverage Criterion | Status |
|---|---|
| Predicate Coverage (PC) | Satisfied — p=T (T-CACC-CO-01) and p=F (T-CACC-CO-02) |
| Clause Coverage (CC) for c2 | Satisfied — c2=T and c2=F both tested at guard |
| Clause Coverage (CC) for c1 | Partially satisfied — c1=T tested at guard; c1=F only observable at N2 (Pydantic) |
| CACC for c2 major | **Satisfied** — complete test pair at determination condition c1=T |
| CACC for c1 major | **Infeasible** — `{c1=F, c2=T}` cannot reach the guard node |

The CACC test suite achieves full coverage for all feasible requirements. The c1 major infeasibility is a structural consequence of Pydantic input validation, not a gap in the test design. The tests document this at the earliest observable point (N2) with explicit infeasibility notes.
