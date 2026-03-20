# Testing README 

## 1. What this folder is for
This folder contains all testing artifacts for the backend testing experiment.

The goal is to compare:
1. Baseline tests (small, behavior-based tests only)
2. Criteria-based tests (formal methods like CFG, prime path, CACC, input partitioning, mutation/RIP)

Backend behavior only.

## 2. Folder map and purpose
testing/baseline-tests
Baseline pytest files only. Keep these frozen after baseline coverage is recorded.

testing/structural-test
Criteria-based structural tests (CFG, edge-pair, prime path, CACC-driven test cases).

testing/input-partition-models
Input domain models (characteristics, partitions, representatives, mapping to tests).

testing/cacc-analysis
Clause tables, predicate analysis, CACC requirement mapping, infeasible condition proofs.

testing/mutation-analysis
Mutant descriptions, RIP analysis worksheets, killed/survived mutant notes.

testing/coverage-reports
Saved coverage outputs (before and after formal testing).

## 3. Prerequisites

1. Python installed
2. A virtual environment
3. pytest and pytest-cov installed

The .venv folder only stores Python packages and tools.

## 4. First-time setup in VS Code terminal
Step 1: Open terminal in VS Code
Use Terminal -> New Terminal

Step 2: Go to the project root

Step 3: Activate virtual environment
If venv is in backend:
source .venv/bin/activate

If venv is in project root:
source .venv/bin/activate

Step 4: Install testing packages
python -m pip install pytest pytest-cov

Step 5: Confirm tools
python -m pytest --version

## 5. Run baseline tests
From project root, run:
python -m pytest -q test_auth.py

If tests pass, run baseline coverage:
python -m pytest -q test_auth.py --cov=app.routes.auth --cov-branch --cov-report=term-missing

Save output to a report file:
python -m pytest -q test_auth.py --cov=app.routes.auth --cov-branch --cov-report=term-missing | tee auth-baseline-coverage.txt

Important:
Use --cov=app.routes.auth (module path), not a file path.
Using --cov=backend/app/routes/auth.py can fail in this project setup.

## 6. Run all baseline tests in the folder
python -m pytest -q testing/baseline-tests

Run all baseline tests with coverage:
python -m pytest -q testing/baseline-tests --cov=app.routes.auth --cov-branch --cov-report=term-missing

## 7. Run structural tests (phase 2)
Example command pattern:
python -m pytest -q testing/structural-test

Example with coverage:
python -m pytest -q testing/structural-test --cov=app.routes.auth --cov-branch --cov-report=term-missing

Save structural coverage evidence:
python -m pytest -q testing/structural-test --cov=app.routes.auth --cov-branch --cov-report=term-missing | tee testing/coverage-reports/auth-structural-coverage.txt

## 8. Baseline freeze rule
Once baseline coverage is measured and recorded:
1. Do not edit baseline test files
2. Put all new formal-method tests in structural-test or other phase-2 folders
3. Keep before/after coverage comparisons traceable

## 9. Team workflow checklist for each target
1. Run baseline test(s)
2. Save baseline coverage report
3. Build CFG and enumerate requirements
4. Create criteria-based tests
5. Save post-criteria coverage report
6. Document defects found in baseline vs criteria-based phase
7. Update analysis artifacts (CACC, IDM, mutation/RIP)

## 10. Common errors and fixes
Error: file or directory not found: test_auth.py  
Fix: Use full relative path from project root:
python -m pytest -q test_auth.py

Error: no tests ran  
Fix: Check filename starts with test_ and is inside a discovered folder.

Error: ModuleNotFoundError: app  
Fix: Run pytest from project root so conftest path setup works.

Error: pytest command not found  
Fix: Activate venv and use:
python -m pytest ...

Error: Coverage looks wrong or missing  
Fix: Use module path for cov:
--cov=app.routes.auth

## 11. Naming and evidence conventions
Test files:
test_<module>_<purpose>.py

Coverage report files:
<module>-baseline-coverage.txt
<module>-structural-coverage.txt

Artifacts:
Store diagrams/tables in their matching analysis folders.

## 12. Suggested minimum commands to remember
1. Activate env
source activate

2. Run one test file
python -m pytest -q test_auth.py

3. Run with branch coverage
python -m pytest -q test_auth.py --cov=app.routes.auth --cov-branch --cov-report=term-missing

4. Save report
python -m pytest -q test_auth.py --cov=app.routes.auth --cov-branch --cov-report=term-missing | tee auth-baseline-coverage.txt

