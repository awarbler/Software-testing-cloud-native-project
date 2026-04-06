# Input Domain Model — `register()`

**Endpoint:** `POST /api/auth/register`  
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
| b1 | Non-empty string | `"userId": "alice"` |
| b2 | Key omitted | *(key absent from body)* |
| b3 | Empty string | `"userId": ""` |
| b4 | Null | `"userId": null` |


---

### C2 — `password` field value
*What is the type and content of the `password` value supplied in the request body?*

| Block | Description | Representative Value |
|-------|-------------|----------------------|
| b1 | Non-empty string | `"password": "secure123"` |
| b2 | Key omitted | *(key absent from body)* |
| b3 | Empty string | `"password": ""` |
| b4 | Null | `"password": null` |


---

### C3 — `userId` uniqueness in the database
*Does a document with this `userId` already exist in the `users` collection?*

| Block | Description | Representative Value |
|-------|-------------|----------------------|
| b1 | `userId` is new — not in DB | `"userId": "new_user"` |
| b2 | `userId` is a duplicate — already registered | `"userId": "existing_user"` *(pre-inserted)* |

