# Team Task Status (Project Plan Alignment)

This document summarizes what is still required per the Project Plan and what 
has already been completed in the repository.

---

# Remaining Work (Per Project Plan)

| Person/Team | Pending Item | Plan Basis | Evidence Gap in Current Repo | Status | Expected Completion Date
|---|---|---|---|---|---|
| Anita Woodford | Build final report (coverage tables + defects) | Milestone 6 | Artifacts exist but not consolidated into single report | Pending | TBD |
| David Cho | Build final report (coverage tables + defects) | Milestone 6 | Artifacts exist but not consolidated into single report | Pending | TBD |
| Eduardo Rosales | Implement hardware checkout/checkin formal pytest suite — coverage report generation | Target 3 Deliverables | Coverage reports pending | Completed (tests), Pending (reports) | 4/9/2026 |
| Eduardo Rosales | Add hardware CFG and prime-path/edge-pair test design artifact | Target 3 Deliverables | No hardware CFG artifact currently present | Pending | 4/10/2026 |
| Eduardo Rosales | Add CACC and input partition model for availability predicate (documentation) | Target 3 Deliverables | Hardware CACC tests exist; documentation pending | Pending | 4/10/2026 |
| Eduardo Rosales | Create hardware behavior analysis document | Target 3 Deliverables | No hardware behavior analysis artifact present | Pending | 4/10/2026 |
| Whole Team | Complete remaining milestone phases (report packaging, final presentation) | Milestones 5-6 | Encrypt work is advanced; hardware documentation pending | Pending | 4/17/2026 |
| Whole Team | Integrate all module outputs into final report (coverage tables + defects) | Milestone 6 | Artifacts exist but not consolidated into single report | Pending | 4/17/2026 |
| Whole Team | Final presentation | Milestone 7 | Presentation not yet created | Pending | 4/17/2026 |

---

# Quick Checklist (Action Items)

## Anita Woodford — Target 1 (_encrypt)
- [x] Add `_encrypt` mutation analysis
- [x] Add `_encrypt` RIP worksheet
- [x] Add mutation summary to `encrypt-analysis.md`
- [ ] Build final report (coverage + defects) — Whole Team task


## David Cho — Target 2 (login/register)
- [x] Create RIP worksheet (login/register defects)
- [x] Add mutation analysis
- [x] Add coverage reports (baseline + partition)
- ~~[ ] Add fix verification tests~~ — out of scope per RQ
- Build final report (coverage + defects) — Whole Team task

## Eduardo Rosales
- [x] Create hardware baseline test suite
- [x] Create hardware partition test suite
- [x] Create hardware structural test suite
- [x] Create hardware CACC test suite
- [ ] Generate hardware coverage report
- [ ] Create hardware CFG and prime path design
- [ ] Create hardware IDM and Base Choice model
- [ ] Create hardware behavior analysis document
- [ ] Document hardware defects (if identified)
- [ ] Build final report (coverage + defects) — Whole Team task

## Whole Team
- [ ] Build final report (coverage + defects)
- [ ] Complete Milestones 3–6 deliverables
- [ ] Merge all artifacts into final report + presentation

---

# Completed Work (Comprehensive Contributions)

## Anita Woodford — Target 1 (_encrypt)

| Work Item | Evidence Artifact | Status | Completed Date |
|---|---|---|---|
| Project proposal start | Project Proposal document | Completed | 2026-02-28 |
| Project plan creation and scope definition | `ProjectPlan.docx` (created by Anita Woodford) | Completed | 2026-02-28 |
| Repository structure and testing framework setup | testing + docs directories | Completed | 2026-02-28 |
| Baseline test suite for `_encrypt` | `test_auth_encrypt.py` | Completed | 2026-03-19 |
| Structural test suite (CFG-based, 9 tests) | `test_app_encrypt_structural.py` | Completed | 2026-04-02 |
| Control Flow Graph (CFG) construction (nodes, edges, prime paths) | `encrypt-analysis.md` | Completed | 2026-04-02 |
| Node, Edge, and Prime Path coverage requirements | `encrypt-analysis.md` | Completed | 2026-04-02 |
| Infeasible branch proof (dir_shift predicate) | `encrypt-analysis.md` | Completed | 2026-04-02 |
| CACC logic coverage analysis | `encrypt-analysis.md` | Completed | 2026-04-06 |
| Input Domain Model (input_text, num_shift, dir_shift) | `encrypt_idm.md` | Completed | 2026-04-07 |
| Base Choice Coverage model | `encrypt_base_choice.md` | Completed | 2026-04-07 |
| Partition-based pytest suite | `test_encrypt_partition.py` | Completed | 2026-04-07 |
| Behavior analysis (expected vs observed behavior) | `encrypt_behavior_analysis.md` | Completed | 2026-04-07 |
| Coverage execution and report generation | `testing/coverage-reports/` | Completed | 2026-04-09 |
| Coverage improvement analysis (42% → 49% → ~88%) | analysis documentation | Completed | 2026-04-07 |
| Combined auth coverage execution | `auth-baseline-combined-coverage.txt` | Completed | 2026-04-07 |
| Documentation refinement and alignment with testing criteria | `encrypt-analysis.md` updates | Completed | 2026-04-02 |
| Mutation test suite for `_encrypt` | `test_encrypt_mutation.py` | Completed | 2026-04-09 |
| RIP analysis across four manual mutants | `encrypt_mutation_analysis.md` | Completed | 2026-04-09 |
| Mutation kill summary and defect sensitivity analysis | `encrypt_mutation_analysis.md` | Completed | 2026-04-09 |
| Mutation execution evidence and failure trace documentation | `encrypt_mutation_analysis.md` | Completed | 2026-04-09 |
| Mutation analysis README/template with example mutant + RIP worksheet format | `testing/mutation-analysis/README.md` | Completed | 2026-04-09 |
| Mutation-analysis documentation structure and reproducible artifact formatting | `testing/mutation-analysis/` docs | Completed | 2026-04-09 |
| Team task-status maintenance and progress tracking updates | `docs/testingDoc/TEAM_TASK_STATUS.md` revisions | Completed | 2026-04-09 |
| Cross-team integration support for teammate deliverables and PR merge readiness tracking | merge history + status updates | Completed | 2026-04-07 to 2026-04-09 |

| Report File | Description | Date Added |
|---|---|---|
| encrypt-baseline-coverage.txt | Baseline coverage output for `_encrypt` test phase | 2026-03-19 |
| auth-encrypty-structural-coverage.txt | Structural coverage output after CFG-based tests | 2026-04-02 |
| encrypt_cacc_coverage.txt | Coverage results associated with CACC analysis | 2026-04-06 |
| encrypt-partition-coverage.txt | Coverage results for input-partition test suite | 2026-04-07 |
| auth-baseline-combined-coverage.txt | Combined auth module baseline coverage snapshot | 2026-04-07 |
| encrypt-mutation4-results.txt | Mutation execution evidence/results artifact | 2026-04-09 |

### Test Results (Anita)

| Result Artifact | Scope | Outcome |
|---|---|---|
| test_auth_encrypt.py | Baseline suite for _encrypt | 9 passed, auth.py 42% coverage |
| test_app_encrypt_structural.py | Structural/CFG-based suite | 9 passed, auth.py 49% coverage (100% feasible _encrypt) |
| test_encrypt_partition.py | Partition-based suite | 8 passed, 100% Base Choice Coverage adequacy |
| test_encrypt_mutation.py | Mutation/RIP suite | 11 passed (4 mutants killed), 100% kill rate |
| Combined execution (all suites) | All _encrypt tests | 61 total passed, auth.py 88% coverage |

### Defects Identified (Anita)

| Defect | Location | Root Cause | Severity | Status |
|---|---|---|---|---|
| Unsatisfiable predicate in dir_shift validation | Line 26 in auth.py (_encrypt) | Condition `(dir_shift < -1 AND dir_shift > 1)` cannot be true; allows invalid dir_shift values (0, 2, -2, etc.) to pass unchecked | Critical | Documented - Infeasible branch identified |
| Invalid ASCII character generation from wrap-around | Lines 45, 51 in auth.py (_encrypt) | Boundary conditions on wrap-high (> 127) and wrap-low (< 34) could produce invalid chr() arguments if mutated | High | Detected via mutation testing; properly handled in original code |

### Summary of Contributions

- Designed and implemented all required testing techniques for Target 1:
  - Graph coverage (CFG, node, edge, prime path)
  - Logic coverage (CACC)
  - Input space partitioning (IDM and Base Choice)
- Identified and formally proved a critical defect:
  - unsatisfiable predicate in `_encrypt`
- Achieved full feasible structural coverage for `_encrypt`
- Established project structure, documentation, and testing workflow

Status:

Target 1 technical testing deliverables are complete.

Remaining: final report integration (Milestone 6).


---

## David Cho — Target 2 (login and register)

| Work Item | Evidence Artifact | Status | Completed Date |
|---|---|---|---|
| Baseline auth test suite implementation | `testing/baseline-tests/test_auth.py` | Completed | 2026-03-11 |
| Baseline coverage capture for login/register behavior | baseline coverage artifacts | Completed | 2026-03-11 |
| Input Domain Model (login) with characteristic/block decomposition | `login_idm.md` | Completed | 2026-04-06 |
| Input Domain Model (register) with characteristic/block decomposition | `register_idm.md` | Completed | 2026-04-06 |
| Base Choice Coverage model derivation (login) | `login_base_choice.md` | Completed | 2026-04-06 |
| Base Choice Coverage model derivation (register) | `register_base_choice.md` | Completed | 2026-04-06 |
| Partition test implementation for login endpoint | `test_login_partition.py` | Completed | 2026-04-06 |
| Partition test implementation for register endpoint | `test_register_partition.py` | Completed | 2026-04-06 |
| Missing-field and null-value validation tests for login/register | partition test suites + IDM mapping | Completed | 2026-04-06 |
| Empty-string boundary tests for `userId` and `password` | partition test suites | Completed | 2026-04-06 |
| Duplicate-user and conflict-response checks in register flow | register tests + analysis docs | Completed | 2026-04-06 |
| Behavior analysis (login): observed vs intended behavior tables | `login_behavior_analysis.md` | Completed | 2026-04-06 |
| Behavior analysis (register): observed vs intended behavior tables | `register_behavior_analysis.md` | Completed | 2026-04-06 |
| Defect root-cause documentation with IDM block traceability | behavior analysis files | Completed | 2026-04-06 |
| HTTP status classification analysis (400/401/409/500) for auth edge cases | behavior analysis files | Completed | 2026-04-06 |
| Add fix-verification tests for login/register if code fix is applied. |Baseline endpoint tests exist, but no explicit fix-verification set is present. | Omitted (determined to be out of project scope) | 4/8/2026 |
| Mutation test suite for login/register defect detection | baseline vs partition comparison | Completed | 2026-04-08 |
| RIP analysis for userId plaintext defects | `testing/mutation-analysis/auth_rip_worksheet.md` | Completed | 2026-04-08 |

### Test Reports Added (David)

| Report File | Description | Date Added |
|---|---|---|
| auth-baseline-coverage.txt | Baseline coverage for login/register | 2026-03-11 |
| auth-partition-coverage.txt | Partition coverage for login/register | 2026-04-06 |
| auth-baseline-combined-coverage.txt | Combined baseline and auth module coverage | 2026-04-07 |

### Test Results (David)

| Result Artifact | Scope | Outcome |
|---|---|---|
| test_auth.py | Baseline auth suite (login/register) | 8 passed, auth.py 84% coverage |
| test_login_partition.py + `test_register_partition.py` | Partition suites (login/register) | 17 passed, Input-partition validation complete |
| Combined execution (baseline + partition) | All auth tests (login/register) | 12 passed, auth.py 88% coverage |

### Defects Identified (David)

| Defect | Location | Root Cause | Severity | Affected Function |
|---|---|---|---|---|
| Empty string accepted as valid userId | login() endpoint | Input validation missing; treats empty string as valid falsy value instead of rejecting as empty | High | login() |
| Empty string accepted as valid userId in register | register() endpoint | Input validation missing; empty strings stored as-is in database | High | register() |
| Null userId accepted in register | register() endpoint | Null check missing; null values stored as None in database | High | register() |
| Empty password accepted in register | register() endpoint | Password validation missing; empty strings stored as-is | High | register() |
| Null password causes 500 error in register | register() endpoint | Null password passed to _encrypt() without validation; triggers AttributeError in encryption logic | Critical | register() |

### Summary of Contributions

- Implemented and stabilized baseline auth tests for login and register flows.
- Built complete login/register IDM and base-choice models, then mapped them directly to executable partition tests.
- Produced implementation-vs-spec behavior analyses that identified concrete validation defects and status-code mismatches.
- Documented defect causes and traceability from test input blocks to observed backend behavior.
- Executed mutation testing and RIP analysis to expose defect patterns in auth validation.

**Status:**  
Complete. All Target 2 technical deliverables finished
Fix-verification tests correctly omitted per project scope.


---

## Eduardo Rosales — Target 3 (hardware checkout/checkin)

| Work Item | Evidence Artifact | Status | Completed Date |
|---|---|---|---|
 Hardware baseline test suite (checkout/checkin endpoints) | test_hardware.py | Completed | |
| Baseline coverage capture for hardware checkout/checkin behavior | baseline coverage artifacts | Completed | |
| Input Domain Model (hardware checkout) with characteristic/block decomposition | Partition test documentation | Completed | 2026-04-?? |
| Input Domain Model (hardware checkin) with characteristic/block decomposition | Partition test documentation | Completed | 2026-04-?? |
| Base Choice Coverage model derivation (checkout) | Structural test documentation | Completed | 2026-04-?? |
| Base Choice Coverage model derivation (checkin) | Structural test documentation | Completed | 2026-04-?? |
| Partition test implementation for checkout endpoint | test_checkout_in_partition.py | Completed | 2026-04-?? |
| Partition test implementation for checkin endpoint | Included in partition test suite | Completed | 2026-04-?? |
| Amount boundary and validation tests for checkout/checkin | partition test suites | Completed | 2026-04-?? |
| Availability predicate coverage (CACC) for checkout logic | test_checkout_in_cacc.py | Completed | 2026-04-?? |

### Test Reports Added (Eduardo)

| Report File | Description | Date Added |
|---|---|---|
| Hardware baseline coverage report | PENDING - NOT YET GENERATED | TBD |
| Hardware partition coverage report | PENDING - NOT YET GENERATED | TBD |
| Hardware structural coverage report | PENDING - NOT YET GENERATED | TBD |
| Hardware CACC coverage report | PENDING - NOT YET GENERATED | TBD |

### Test Results (Eduardo)

| Result Artifact | Scope | Outcome |
|---|---|---|
| `test_hardware.py` | Baseline suite for checkout/checkin | Tests created; coverage report pending |
| `test_checkout_in_partition.py` | Partition-based suite for checkout | Tests created; coverage report pending |
| `test_checkout_in_cacc.py` | CACC/logic suite for availability predicate | Tests created; coverage report pending |
| `test_checkout_in_structural.py` | Structural/CFG-based suite for checkout logic | Tests created; coverage report pending |

### Defects Identified (Eduardo)

| Defect | Location | Root Cause | Severity | Status |
|---|---|---|---|---|
| Pending defect analysis | hardware.py checkout/checkin endpoints | Analysis in progress; formal documentation required | TBD | Under investigation |
| Pending defect analysis | hardware.py availability checking logic | Analysis in progress; formal documentation required | TBD | Under investigation |

### Summary of Contributions

- Implemented baseline test suite for hardware checkout and checkin endpoints.
- Built partition tests for hardware checkout endpoint with boundary condition testing.
- Implemented CACC tests targeting availability predicate logic coverage.
- Implemented structural/CFG tests for hardware checkout logic flow.
- Test suites created and functional; coverage reports and behavior analysis documentation in progress.

**Status:** Test implementation is COMPLETE (4 functional test suites). Documentation (CFG design, IDM models, behavior analysis, coverage reports, defect analysis) PENDING. Estimated completion: 4/10/2026.

---

# Notes

- Coverage is measured at the module level (`hardware.py`, `auth.py`) 
- Structural testing focuses on target functions (_encrypt, checkout, login/register)
- All feasible paths in _encrypt() are fully covered; infeasible branch correctly excluded
- Hardware test suites exist but formal documentation and coverage artifacts are pending

---

# Final Status

## Completed
- Structural testing (CFG, node, edge, prime paths) _encrypt() — Target 1
- Input space partitioning (login, register, hardware checkout) — Targets 2 & 3
- CACC logic coverage _encrypt() and hardware availability predicate — Targets 1 & 3
- Behavior analysis completed for Target 1 (_encrypt) and Target 2 (login/register)
- Mutation and RIP analysis for Target 1 (_encrypt) and Target 2 (login/register) — 100% kill rates
- Coverage improvement demonstrated: 42% → 49% → 88% (auth.py module)
- Hardware test implementation (baseline, partition, CACC, structural tests)

## Remaining (Critical)
- Hardware coverage report generation
- Hardware CFG design and documentation
- Hardware IDM and Base Choice model documentation
- Hardware behavior analysis documentation
- Hardware defect analysis and documentation
- Final report integration (all modules — Milestone 6) — Whole Team
- Final presentation (Milestone 7) — Whole Team

---

# Project Status

Approximately 90% complete

Breakdown by Target:
- Target 1 (_encrypt): 100% complete
- Target 2 (login/register): 100% complete
- Target 3 (hardware): 65% complete (tests done; documentation and coverage reporting pending)
- Milestone 6 (Final Report): 0% complete — Whole Team responsibility
- Milestone 7 (Presentation): 0% complete — Whole Team responsibility