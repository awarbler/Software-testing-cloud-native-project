# Base Choice Test Frames — `login()`

**Endpoint:** `POST /api/auth/login`  
**Source:** `backend/app/routes/auth.py`  
**IDM reference:** `login_idm.md`  
**Coverage criterion:** Base Choice Coverage (BCC)

---

## Base Choice Selection

| Characteristic | Base Block | Rationale |
|----------------|------------|-----------|
| C1 — `userId` value | **b1** (non-empty string) | A well-formed login request supplies a valid string userId |
| C2 — `password` value | **b1** (non-empty string) | A well-formed login request supplies a valid string password |
| C3 — Credential validity | **b1** (correct match) | The normal case is a registered user supplying the correct password |

---

## Base Test Frame

**BT — Base test (C1:b1, C2:b1, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "carol", "password": "mypassword"}` |
| DB state before | user `"carol"` pre-registered with password `"mypassword"` |
| Expected status | `200` |
| Expected body | `{"ok": true, "message": "Login successful", "user": {"userId": "carol"}}` |

---

## Varied Test Frames

### Varying C1 — `userId` value

**T1 — C1:b2 — `userId` key omitted (C1:b2, C2:b1, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"password": "mypassword"}` |
| DB state before | any |
| Expected status | `400` |
| Expected body | `{"ok": false, "error": "Missing userId or password"}` |

---

**T2 — C1:b3 — `userId` is empty string (C1:b3, C2:b1, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "", "password": "mypassword"}` |
| DB state before | any |
| Expected status | `401` |
| Expected body | `{"ok": false, "error": "Invalid credentials"}` |
| Note | `data.get("userId")` returns `""` which is not `None`, so the guard passes. The DB is queried for `userId: ""` which yields no match. The endpoint returns 401 rather than 400, meaning an empty string is silently treated as an invalid credential rather than a malformed input. |

---

**T3 — C1:b4 — `userId` is null (C1:b4, C2:b1, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": null, "password": "mypassword"}` |
| DB state before | any |
| Expected status | `400` |
| Expected body | `{"ok": false, "error": "Missing userId or password"}` |
| Note | `data.get("userId")` returns `None` for an explicit null value, identical to a missing key. b2 and b4 collapse to the same behavior here. |

---

### Varying C2 — `password` value

**T4 — C2:b2 — `password` key omitted (C1:b1, C2:b2, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "carol"}` |
| DB state before | any |
| Expected status | `400` |
| Expected body | `{"ok": false, "error": "Missing userId or password"}` |

---

**T5 — C2:b3 — `password` is empty string (C1:b1, C2:b3, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "carol", "password": ""}` |
| DB state before | user `"carol"` pre-registered with password `"mypassword"` |
| Expected status | `401` |
| Expected body | `{"ok": false, "error": "Invalid credentials"}` |
| Note | `data.get("password")` returns `""` which is not `None`, so the guard passes. `_encrypt("")` returns `""`. The DB is queried for the encrypted form of a real password against `""` — no match. Returns 401 instead of 400, same classification gap as T2. |

---

**T6 — C2:b4 — `password` is null (C1:b1, C2:b4, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "carol", "password": null}` |
| DB state before | any |
| Expected status | `400` |
| Expected body | `{"ok": false, "error": "Missing userId or password"}` |
| Note | `data.get("password")` returns `None` for an explicit null value, identical to a missing key. b2 and b4 collapse to the same behavior here. |

---

### Varying C3 — Credential validity

**T7 — C3:b2 — wrong password (C1:b1, C2:b1, C3:b2)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "carol", "password": "wrongpass"}` |
| DB state before | user `"carol"` pre-registered with password `"mypassword"` |
| Expected status | `401` |
| Expected body | `{"ok": false, "error": "Invalid credentials"}` |

---

**T8 — C3:b3 — userId not found (C1:b1, C2:b1, C3:b3)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "ghost", "password": "anypass"}` |
| DB state before | no user `"ghost"` exists in `users` collection |
| Expected status | `401` |
| Expected body | `{"ok": false, "error": "Invalid credentials"}` |

---

## Summary

| Frame | C1 | C2 | C3 | Expected Status |
|-------|----|----|----|-----------------|
| BT | b1 | b1 | b1 | `200` |
| T1 | **b2** | b1 | b1 | `400` |
| T2 | **b3** | b1 | b1 | `401` — actual; intended `400` |
| T3 | **b4** | b1 | b1 | `400` |
| T4 | b1 | **b2** | b1 | `400` |
| T5 | b1 | **b3** | b1 | `401` — actual; intended `400` |
| T6 | b1 | **b4** | b1 | `400` |
| T7 | b1 | b1 | **b2** | `401` |
| T8 | b1 | b1 | **b3** | `401` |

Total test frames: **9** (1 base + 8 variations)  
Frames T2 and T5 reflect what the implementation currently does, not what a correct implementation would return. An empty string bypasses the None guard and is misclassified as an invalid credential rather than a malformed input.