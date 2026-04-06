# Implementation Behavior Analysis — `register()`

**Endpoint:** `POST /api/auth/register`  
**Source:** `backend/app/routes/auth.py`  
**IDM reference:** `register_idm.md`

This document maps each IDM block to the behavior observed in the current implementation
and identifies where that behavior diverges from the intended specification.

---

## C1 — `userId` field value

The field guard in `register()` uses `field in data`, which checks key presence only — not value validity.

| Block | Input | Observed | Intended | Diverges? |
|-------|-------|----------|----------|-----------|
| b1 | Non-empty string | `201` — proceeds normally | `201` | No |
| b2 | Key omitted | `400` — caught by field check | `400` | No |
| b3 | Empty string | `201` — key is present so guard passes; empty string stored as userId | `400` | Yes |
| b4 | Null | `201` — key is present so guard passes; `None` stored as userId | `400` | Yes |

---

## C2 — `password` field value

Same guard applies. Additionally, the value is passed directly to `_encrypt()` without a null check.

| Block | Input | Observed | Intended | Diverges? |
|-------|-------|----------|----------|-----------|
| b1 | Non-empty string | `201` — encrypted and stored | `201` | No |
| b2 | Key omitted | `400` — caught by field check | `400` | No |
| b3 | Empty string | `201` — `_encrypt("")` returns `""`; empty password stored | `400` | Yes |
| b4 | Null | `500` — `_encrypt(None)` calls `None.isascii()` → `AttributeError` | `400` | Yes |

---

## C3 — `userId` uniqueness in the database

No divergence in this characteristic — the duplicate check behaves as intended.

| Block | Input | Observed | Intended | Diverges? |
|-------|-------|----------|----------|-----------|
| b1 | New user | `201` — insertion proceeds | `201` | No |
| b2 | Duplicate | `409` — duplicate detected before insertion | `409` | No |

---

## Summary of Defects

| Block | Field | Root cause |
|-------|-------|------------|
| C1:b3 | `userId` | `field in data` checks key presence only; does not reject empty string |
| C1:b4 | `userId` | `field in data` checks key presence only; does not reject null |
| C2:b3 | `password` | `field in data` checks key presence only; does not reject empty string |
| C2:b4 | `password` | No null guard before `_encrypt()`; null propagates and causes a crash |
