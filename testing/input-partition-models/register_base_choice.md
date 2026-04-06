# Base Choice Test Frames — `register()`

**Endpoint:** `POST /api/auth/register`  
**Source:** `backend/app/routes/auth.py`  
**IDM reference:** `register_idm.md`  
**Coverage criterion:** Base Choice Coverage (BCC)

---

## Base Choice Selection

| Characteristic | Base Block | Rationale |
|----------------|------------|-----------|
| C1 — `userId` value | **b1** (non-empty string) | A well-formed registration request supplies a valid string userId |
| C2 — `password` value | **b1** (non-empty string) | A well-formed registration request supplies a valid string password |
| C3 — `userId` uniqueness | **b1** (new user) | The normal case is registering a userId that does not yet exist |

---

## Base Test Frame

**BT — Base test (C1:b1, C2:b1, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "alice", "password": "secure123"}` |
| DB state before | `users` collection is empty |
| Expected status | `201` |
| Expected body | `{"user": {"userId": "alice"}}` |

---

## Varied Test Frames

### Varying C1 — `userId` value

**T1 — C1:b2 — `userId` key omitted (C1:b2, C2:b1, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"password": "secure123"}` |
| DB state before | any |
| Expected status | `400` |
| Expected body | error names `"userId"` as a missing field |

---

**T2 — C1:b3 — `userId` is empty string (C1:b3, C2:b1, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "", "password": "secure123"}` |
| DB state before | any |
| Expected status | `201` |
| Expected body | `{"user": {"userId": ""}}` |
| Note | Key is present so the field check passes; empty string is stored as userId. This exposes a validation gap — the implementation does not reject empty string values. |

---

**T3 — C1:b4 — `userId` is null (C1:b4, C2:b1, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": null, "password": "secure123"}` |
| DB state before | any |
| Expected status | `201` |
| Expected body | `{"user": {"userId": null}}` |
| Note | Key is present so the field check passes; `None` is stored as userId. This exposes a validation gap — the implementation does not reject null values. |

---

### Varying C2 — `password` value

**T4 — C2:b2 — `password` key omitted (C1:b1, C2:b2, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "alice"}` |
| DB state before | any |
| Expected status | `400` |
| Expected body | error names `"password"` as a missing field |

---

**T5 — C2:b3 — `password` is empty string (C1:b1, C2:b3, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "alice", "password": ""}` |
| DB state before | any |
| Expected status | `201` |
| Expected body | `{"user": {"userId": "alice"}}` |
| Note | Key is present so the field check passes; `_encrypt("")` returns `""` which is stored as the password. This exposes a validation gap — a user can be registered with an empty password. |

---

**T6 — C2:b4 — `password` is null (C1:b1, C2:b4, C3:b1)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "alice", "password": null}` |
| DB state before | any |
| Expected status | `500` |
| Expected body | unhandled server error |
| Note | Key is present so the field check passes; `_encrypt(None, 3, 1)` calls `None.isascii()` which raises `AttributeError`. This exposes a crash — the implementation does not guard against null values before passing to `_encrypt`. |

---

### Varying C3 — `userId` uniqueness

**T7 — C3:b2 — duplicate `userId` (C1:b1, C2:b1, C3:b2)**

| Field | Value |
|-------|-------|
| Request body | `{"userId": "alice", "password": "secure123"}` |
| DB state before | user `"alice"` already exists in `users` collection |
| Expected status | `409` |
| Expected body | error contains `"already exists"` |

---

## Summary

| Frame | C1 | C2 | C3 | Expected Status |
|-------|----|----|----|-----------------|
| BT | b1 | b1 | b1 | `201` |
| T1 | **b2** | b1 | b1 | `400` |
| T2 | **b3** | b1 | b1 | `201` — actual; intended `400` |
| T3 | **b4** | b1 | b1 | `201` — actual; intended `400` |
| T4 | b1 | **b2** | b1 | `400` |
| T5 | b1 | **b3** | b1 | `201` — actual; intended `400` |
| T6 | b1 | **b4** | b1 | `500` — actual; intended `400` |
| T7 | b1 | b1 | **b2** | `409` |

Total test frames: **8** (1 base + 7 variations)  
Frames T2, T3, T5, T6 reflect what the implementation currently does, not what a correct implementation would return. The field guard checks key presence only, not value validity.
