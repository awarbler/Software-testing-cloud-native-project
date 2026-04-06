# Implementation Behavior Analysis — `login()`

**Endpoint:** `POST /api/auth/login`  
**Source:** `backend/app/routes/auth.py`  
**IDM reference:** `login_idm.md`

This document maps each IDM block to the behavior observed in the current implementation
and identifies where that behavior diverges from the intended specification.

---

## C1 — `userId` field value

The field guard in `login()` uses `data.get("userId") is None`. This catches omitted keys and
explicit null values (both return `None` via `dict.get()`), but does not catch empty strings.

| Block | Input | Observed | Intended | Diverges? |
|-------|-------|----------|----------|-----------|
| b1 | Non-empty string | `200` — proceeds normally | `200` | No |
| b2 | Key omitted | `400` — `data.get()` returns `None`; caught by None check | `400` | No |
| b3 | Empty string | `401` — `data.get()` returns `""`; bypasses None check; DB queried for `userId: ""`; no match | `400` | Yes |
| b4 | Null | `400` — `data.get()` returns `None`; caught by None check | `400` | No |

> **Note:** b2 and b4 produce identical behavior — `dict.get()` returns `None` for both a missing
> key and an explicit null value. They are kept as distinct blocks because they represent
> different inputs even though the implementation does not distinguish them.

---

## C2 — `password` field value

Same guard applies via `data.get("password") is None`.

| Block | Input | Observed | Intended | Diverges? |
|-------|-------|----------|----------|-----------|
| b1 | Non-empty string | `200` — proceeds normally | `200` | No |
| b2 | Key omitted | `400` — `data.get()` returns `None`; caught by None check | `400` | No |
| b3 | Empty string | `401` — `data.get()` returns `""`; bypasses None check; `_encrypt("")` returns `""`; no DB match | `400` | Yes |
| b4 | Null | `400` — `data.get()` returns `None`; caught by None check | `400` | No |

---

## C3 — Credential validity

No divergence in this characteristic — all three blocks behave as intended.

| Block | Input | Observed | Intended | Diverges? |
|-------|-------|----------|----------|-----------|
| b1 | Correct match | `200` — userId and encrypted password match DB record | `200` | No |
| b2 | Wrong password | `401` — encrypted password does not match stored value | `401` | No |
| b3 | userId not found | `401` — DB query returns no document | `401` | No |

---

## Summary of Defects

| Block | Field | Root cause |
|-------|-------|------------|
| C1:b3 | `userId` | None check does not cover empty string; empty string is misclassified as an invalid credential rather than a malformed input |
| C2:b3 | `password` | None check does not cover empty string; same misclassification as C1:b3 |
