# Input Domain Model — `login()`

**Endpoint:** `POST /api/auth/login`  
**Source:** `backend/app/routes/auth.py`

---

## Input Parameters

| Parameter | Type | Source |
|-----------|------|--------|
| `userId` | string | JSON request body |
| `password` | string | JSON request body |
| DB state | external | MongoDB `users` collection |

---

## Characteristics, Blocks, and Representative Values

### C1 — `userId` field value
*What is the type and content of the `userId` value supplied in the request body?*

| Block | Description | Representative Value |
|-------|-------------|----------------------|
| b1 | Non-empty string | `"userId": "carol"` |
| b2 | Key omitted | *(key absent from body)* |
| b3 | Empty string | `"userId": ""` |
| b4 | Null | `"userId": null` |

---

### C2 — `password` field value
*What is the type and content of the `password` value supplied in the request body?*

| Block | Description | Representative Value |
|-------|-------------|----------------------|
| b1 | Non-empty string | `"password": "mypassword"` |
| b2 | Key omitted | *(key absent from body)* |
| b3 | Empty string | `"password": ""` |
| b4 | Null | `"password": null` |

---

### C3 — Credential validity
*Does the submitted `userId` + `password` pair match a record in the `users` collection?*

| Block | Description | Representative Value |
|-------|-------------|----------------------|
| b1 | `userId` exists and password matches | `"userId": "carol", "password": "mypassword"` *(pre-registered)* |
| b2 | `userId` exists but password does not match | `"userId": "carol", "password": "wrongpass"` |
| b3 | `userId` does not exist in DB | `"userId": "ghost", "password": "anypass"` |