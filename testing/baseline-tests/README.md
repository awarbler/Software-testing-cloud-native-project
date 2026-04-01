# Baseline Tests (Phase 1)

This folder contains the baseline test suite for the backend auth module.

## Goal

Baseline testing captures expected behavior and simple input/guard handling before structural testing.

Baseline rules used in this project:

- 3 to 4 tests per target behavior
- Behavior-based checks only
- No CFG or path-targeted test design

## Files In This Folder

- README.md: baseline documentation for this phase
- conftest.py: shared pytest fixtures and test app setup
- test_auth.py: baseline endpoint tests for register() and login()
- test_auth_encrypt.py: baseline unit tests for auth._encrypt

## What Each Test File Covers

test_auth.py:

- POST /api/auth/register
	- valid user creates account (201)
	- missing required field returns 400
	- empty body returns 400
	- duplicate userId returns 409
- POST /api/auth/login
	- valid credentials return 200
	- wrong password returns 401
	- missing password returns 400
	- nonexistent user returns 401

test_auth_encrypt.py (auth._encrypt):

- happy path with valid ASCII input
- non-ASCII input raises TypeError
- num_shift < 1 raises ValueError
- valid special character input behavior

Observed note from baseline:

- forbidden character behavior did not match an earlier assumption and is documented for follow-up in analysis artifacts.

## How To Run Baseline Tests

Run all baseline tests in this folder:

```bash
python -m pytest -q testing/baseline-tests
```

Run only endpoint baseline tests:

```bash
python -m pytest -q testing/baseline-tests/test_auth.py
```

Run only encrypt baseline tests:

```bash
python -m pytest -q testing/baseline-tests/test_auth_encrypt.py
```

## Baseline Coverage

Generate coverage for this baseline suite:

```bash
python -m pytest -q testing/baseline-tests \
	--cov=app.routes.auth --cov-branch --cov-report=term-missing
```

Save coverage output artifact:

```bash
python -m pytest -q testing/baseline-tests \
	--cov=app.routes.auth --cov-branch --cov-report=term-missing \
	| tee testing/coverage-reports/auth-baseline-coverage.txt
```

Recorded baseline artifact:

- testing/coverage-reports/auth-baseline-coverage.txt
- statement coverage (full auth module): 84%
- branch data: 26 branches, 7 partial

## Handoff To Structural Testing

After baseline is recorded, structural tests continue in:

- testing/structural-test/README.md
- testing/structural-test/test_encrypt_structural.py
- docs/testing/encrypt-analysis.md