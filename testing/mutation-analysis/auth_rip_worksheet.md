# RIP Worksheet — register() and login()

**Target file:** `backend/app/routes/auth.py`  
**Methods under analysis:** `register()`, `login()`  
**Related artifacts:**
- IDM specs: `testing/input-partition-models/register_idm.md`, `login_idm.md`
- Behavior analysis: `register_behavior_analysis.md`, `login_behavior_analysis.md`
- Mutation scores: `testing/mutation-analysis/mutation_results/`

The RIP model states that for a fault to produce an observable failure, three conditions must hold:

1. **Reachability (R)** — a test input must execute the faulty line
2. **Infectiousness (I)** — the fault must cause the program state to diverge from the correct state
3. **Propagation (P)** — the infected state must reach an assertion that observes the difference

---

## Part 1 — Input Validation Defects (IDM-Derived)

These defects were identified through Base Choice Coverage testing. The root cause in both methods is the same field guard pattern:

```python
# register() — line 101
if not all(field in data for field in required_fields):

# login() — line 67
if userid is None or password is None:
```

Both guards check for key presence or None, but do not reject empty strings or null values beyond the None check.

---

### Defect R-1 — register(): empty string userId accepted (C1:b3)

| RIP Step | Analysis |
|---|---|
| **Fault location** | Line 101: `field in data` is True for `""` — key presence check passes |
| **Reachability** | POST `/api/auth/register` with `{"userId": "", "password": "secure123"}` reaches line 101 |
| **Infectiousness** | Guard evaluates to False (key is present), so execution continues. Program state diverges: should return 400, instead proceeds to store the user |
| **Propagation** | `""` is stored as userId, response is 201. A test asserting `status_code == 400` would observe the failure. Test T2 in `test_register_partition.py` asserts the actual 201 behavior and documents this as a defect |
| **Exposed by** | T2 (partition suite) — asserts actual behavior with defect note |

---

### Defect R-2 — register(): null userId accepted (C1:b4)

| RIP Step | Analysis |
|---|---|
| **Fault location** | Line 101: `"userId" in data` is True even when value is `null` (Python `None`) |
| **Reachability** | POST with `{"userId": null, "password": "secure123"}` reaches line 101 |
| **Infectiousness** | Guard bypassed; None stored as userId. State diverges from intended 400 |
| **Propagation** | 201 returned with `userId: null` in response body. Observable via status code assertion |
| **Exposed by** | T3 (partition suite) — asserts actual behavior with defect note |

---

### Defect R-3 — register(): empty string password accepted (C2:b3)

| RIP Step | Analysis |
|---|---|
| **Fault location** | Line 101: same guard, same key-presence-only logic |
| **Reachability** | POST with `{"userId": "alice", "password": ""}` reaches line 101 |
| **Infectiousness** | Guard bypassed; `_encrypt("")` is called and returns `""`. Empty password stored |
| **Propagation** | 201 returned. Observable via status code assertion |
| **Exposed by** | T5 (partition suite) — asserts actual behavior with defect note |

---

### Defect R-4 — register(): null password crashes server (C2:b4)

| RIP Step | Analysis |
|---|---|
| **Fault location** | Line 101 (guard bypassed) + line 109: `_encrypt(None, 3, 1)` calls `None.isascii()` |
| **Reachability** | POST with `{"userId": "alice", "password": null}` reaches line 101, then line 109 |
| **Infectiousness** | Guard bypassed; `_encrypt` receives None. `AttributeError` is raised — program state is catastrophically infected |
| **Propagation** | Unhandled exception propagates to Flask error handler, returning 500. Observable via status code assertion |
| **Exposed by** | T6 (partition suite) — asserts 500 and documents as unhandled crash |

---

### Defect L-1 — login(): empty string userId misclassified (C1:b3)

| RIP Step | Analysis |
|---|---|
| **Fault location** | Line 67: `userid is None` is False for `""` — empty string passes the None guard |
| **Reachability** | POST `/api/auth/login` with `{"userId": "", "password": "anything"}` reaches line 67 |
| **Infectiousness** | Guard bypassed; `_encrypt("anything")` is called. DB lookup finds no user with `userId: ""`. State diverges: should be 400 (malformed input), but proceeds as a credential check |
| **Propagation** | 401 returned instead of 400. Observable if assertion checks for 400 specifically. T2 in `test_login_partition.py` asserts actual 401 and documents the misclassification |
| **Exposed by** | T2 (partition suite) — asserts actual behavior with defect note |

---

### Defect L-2 — login(): empty string password misclassified (C2:b3)

| RIP Step | Analysis |
|---|---|
| **Fault location** | Line 67: `password is None` is False for `""` |
| **Reachability** | POST with `{"userId": "alice", "password": ""}` reaches line 67 |
| **Infectiousness** | Guard bypassed; `_encrypt("")` returns `""`. DB lookup with empty encrypted password finds no match. State diverges: should be 400, treated as 401 |
| **Propagation** | 401 returned instead of 400. Same observable effect as L-1 |
| **Exposed by** | T5 (partition suite) — asserts actual behavior with defect note |

---

## Part 2 — Mutation Testing RIP Observations

These observations come from the mutation comparison run
(`run_mutation_comparison.sh`). The scores were:

| Suite | Killed | Survived | Score |
|---|---|---|---|
| Baseline — `test_auth.py` (8 tests) | 77 | 44 | 63.6% |
| Partition — `test_register_partition.py` + `test_login_partition.py` (17 tests) | 75 | 46 | 62.0% |

Four mutants differed between the two runs. RIP analysis explains why each one was caught by one suite but not the other.

---

### Mutant 2 — `bp = None` (killed by partition, survived baseline)

```diff
-bp = Blueprint("auth", __name__)
+bp = None
```

| RIP Step | Baseline | Partition |
|---|---|---|
| **R** | Reached — all tests call auth endpoints | Reached — same |
| **I** | Infected — `bp = None` should break route registration | Infected — same |
| **P** | **Broken** — baseline's broad mock setup absorbs the startup failure silently | Propagates — partition's more targeted patching surfaces the crash as a test failure |

**Verdict:** Infrastructure difference, not test quality. The broader patch surface in the baseline conftest swallows the fault before any assertion observes it.

---

### Mutant 56 — `db["XXusersXX"]` in login() (killed by baseline, survived partition)

```diff
-user = db["users"].find_one({"userId": userid, "password": encrypt_password})
+user = db["XXusersXX"].find_one({"userId": userid, "password": encrypt_password})
```

| RIP Step | Baseline | Partition |
|---|---|---|
| **R** | Reached — login tests execute this line | Reached — same |
| **I** | Infected — `FakeDB.__getitem__("XXusersXX")` raises `KeyError`, crashing the handler | **Broken** — partition's `fake_db` is a `MagicMock` with `__getitem__` returning `fake_users` for any key. Wrong collection name returns the same data, no state change |
| **P** | Propagates — KeyError → 500 response, test expecting 200 fails | N/A — infection never occurred |

**Verdict:** The partition suite's simpler `MagicMock` fake database breaks infectiousness. The baseline's `FakeDB` class discriminates by key name, allowing the wrong lookup to fail.

---

### Mutant 81 — `"XXerrorXX"` key in register() empty-body response (killed by baseline, survived partition)

```diff
-return jsonify({"error": "Expected JSON object body"}), 400
+return jsonify({"XXerrorXX": "Expected JSON object body"}), 400
```

| RIP Step | Baseline | Partition |
|---|---|---|
| **R** | Reached — `test_register_empty_body_returns_400` sends `{}` | **Broken** — no partition test sends an empty body; the IDM starts from C1/C2 fields being present, omitted, empty, or null, but does not model an entirely absent request body |
| **I** | Infected — wrong key name in response | N/A |
| **P** | Propagates — `assert "error" in body` fails | N/A |

**Verdict:** Reachability gap in the partition suite. The empty `{}` body is outside the IDM's modeled input space.

---

### Mutant 83 — status 401 instead of 400 for empty body (killed by baseline, survived partition)

```diff
-return jsonify({"error": "Expected JSON object body"}), 400
+return jsonify({"error": "Expected JSON object body"}), 401
```

| RIP Step | Baseline | Partition |
|---|---|---|
| **R** | Reached — same baseline test as mutant 81 | **Broken** — same IDM gap as mutant 81 |
| **I** | Infected — wrong status code | N/A |
| **P** | Propagates — `assert status_code == 400` fails | N/A |

**Verdict:** Same reachability gap as mutant 81. Both mutants expose the same missing input block in the IDM.

---

## Summary

| Defect | Method | Fault Line | R | I | P | Caught by |
|---|---|---|---|---|---|---|
| R-1 Empty string userId | register | 101 | Yes | Yes | Yes | T2 partition |
| R-2 Null userId | register | 101 | Yes | Yes | Yes | T3 partition |
| R-3 Empty string password | register | 101 | Yes | Yes | Yes | T5 partition |
| R-4 Null password crash | register | 101, 109 | Yes | Yes | Yes | T6 partition |
| L-1 Empty string userId | login | 67 | Yes | Yes | Yes | T2 partition |
| L-2 Empty string password | login | 67 | Yes | Yes | Yes | T5 partition |
| Mutant 2 (bp=None) | both | 11 | Yes | Yes | No (baseline) | Partition only |
| Mutant 56 (wrong collection) | login | 73 | Yes | No (partition) | — | Baseline only |
| Mutant 81 (wrong key) | register | 98 | No (partition) | — | — | Baseline only |
| Mutant 83 (wrong status) | register | 98 | No (partition) | — | — | Baseline only |

The IDM-derived defects (R-1 through L-2) all satisfy RIP fully — the partition tests reach them, infect program state, and the assertions observe the divergence. The mutation testing observations reveal that the partition suite has one structural gap (no empty-body test case) and one infrastructure gap (MagicMock absorbs collection name mutations).
