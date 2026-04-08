# Team Task Status (Project Plan Alignment)

This document summarizes what is still required per the Project Plan and what 
has already been completed in the repository.

---

# Remaining Work (Per Project Plan)

| Person/Team | Pending Item | Plan Basis | Evidence Gap in Current Repo | Status | Expected Completion Date
|---|---|---|---|---|---|
| Anita Woodford | Integrate all module outputs into one final report package with before/after coverage tables. | Team Responsibility + Milestone 6 | No single consolidated final testing report file yet. | Pending |
| Anita Woodford | Add final defect summary and presentation-ready test evidence bundle. | Team Responsibility + Milestone 6 | Defect evidence exists across files but not yet packaged as one final submission set. | Pending |
| David Cho | Create RIP worksheet for the login/register userId plaintext defect. | Target 2 Deliverables | No RIP worksheet artifact is present in testing docs. | Pending | 4/8/2026 |
| David Cho | Add mutation-analysis artifact for login/register defect exposure. | Target 2 Deliverables | No dedicated mutation-analysis artifact for this defect is present. | Pending | 4/8/2026 |
| David Cho | Add fix-verification tests for login/register if code fix is applied. | Target 2 Deliverables | Baseline endpoint tests exist, but no explicit fix-verification set is present. | Pending | 4/8/2026 |
| Eduardo Rosales | Implement hardware checkout/checkin formal pytest suite. | Target 3 Deliverables | No hardware-specific pytest files are currently present in testing folder. | Pending | 4/8/2026 |
| Eduardo Rosales | Add hardware CFG and prime-path/edge-pair test design artifact. | Target 3 Deliverables | No hardware CFG artifact is currently present in testing docs. | Pending | 4/9/2026 |
| Eduardo Rosales | Add CACC and input partition model for availability predicate. | Target 3 Deliverables | No hardware CACC or partition model artifact is currently present. | Pending | 4/9/2026 |
| Eduardo Rosales | Generate hardware coverage report and store under coverage-reports. | Target 3 Deliverables | No hardware structural coverage file is currently present. | Pending | 4/9/2026 |
| Whole Team | Complete remaining milestone phases (structural completion, partitioning, mutation/RIP, report packaging). | Milestones 3-6 | Encrypt work is advanced; hardware and auth-defect RIP artifacts are not complete at the same level. | Pending |

---

# Quick Checklist (Action Items)

## Anita Woodford
- [ ] Add `_encrypt` mutation analysis
- [ ] Add `_encrypt` RIP worksheet
- [ ] Add mutation summary to `encrypt-analysis.md`
- [ ] Build final report (coverage + defects)

## David Cho
- [ ] Create RIP worksheet (login/register defects)
- [ ] Add mutation analysis
- [ ] Add fix verification tests

## Eduardo Rosales
- [ ] Create hardware CFG
- [ ] Add prime path / edge-pair design
- [ ] Add CACC for availability predicate
- [ ] Add input partition model
- [ ] Generate hardware coverage report

## Whole Team
- [ ] Complete Milestones 3–6 deliverables
- [ ] Merge all artifacts into final report + presentation

---

# Completed Work (Comprehensive Contributions)

## Anita Woodford — Target 1 (_encrypt) and Project Organization

| Work Item | Evidence Artifact | Status |
|---|---|---|
| Project proposal start | Project Proposal document | Completed |
| Project plan creation and scope definition | `ProjectPlan.docx` | Completed |
| Repository structure and testing framework setup | testing + docs directories | Completed |
| Baseline test suite for `_encrypt` | `test_auth_encrypt.py` | Completed |
| Structural test suite (CFG-based, 9 tests) | `test_app_encrypt_structural.py` | Completed |
| Control Flow Graph (CFG) construction (nodes, edges, prime paths) | `encrypt-analysis.md` | Completed |
| Node, Edge, and Prime Path coverage requirements | `encrypt-analysis.md` | Completed |
| Infeasible branch proof (dir_shift predicate) | `encrypt-analysis.md` | Completed |
| CACC logic coverage analysis | `encrypt-analysis.md` | Completed |
| Input Domain Model (input_text, num_shift, dir_shift) | `encrypt_idm.md` | Completed |
| Base Choice Coverage model | `encrypt_base_choice.md` | Completed |
| Partition-based pytest suite | `test_encrypt_partition.py` | Completed |
| Behavior analysis (expected vs observed behavior) | `encrypt_behavior_analysis.md` | Completed |
| Coverage execution and report generation | `testing/coverage-reports/` | Completed |
| Coverage improvement analysis (42% → 49% → ~88%) | analysis documentation | Completed |
| Combined auth coverage execution | `auth-baseline-combined-coverage.txt` | Completed |
| Documentation refinement and alignment with testing criteria | `encrypt-analysis.md` updates | Completed |

### Summary of Contributions

- Designed and implemented all required testing techniques for Target 1:
  - Graph coverage (CFG, node, edge, prime path)
  - Logic coverage (CACC)
  - Input space partitioning (IDM and Base Choice)
- Identified and formally proved a critical defect:
  - unsatisfiable predicate in `_encrypt`
- Achieved full feasible structural coverage for `_encrypt`
- Established project structure, documentation, and testing workflow

**Status:**  
Target 1 is almost complete except for mutation and RIP analysis (final requirement)

---

## David Cho — Target 2 (login and register)

| Work Item | Evidence Artifact | Status |
|---|---|---|
| Baseline auth tests | baseline test files | Completed |
| Input Domain Model (login) | `login_idm.md` | Completed |
| Input Domain Model (register) | `register_idm.md` | Completed |
| Base Choice Coverage (login) | `login_base_choice.md` | Completed |
| Base Choice Coverage (register) | `register_base_choice.md` | Completed |
| Partition pytest suite (login) | `test_login_partition.py` | Completed |
| Partition pytest suite (register) | `test_register_partition.py` | Completed |
| Behavior analysis (login) | `login_behavior_analysis.md` | Completed |
| Behavior analysis (register) | `register_behavior_analysis.md` | Completed |
| Defect identification and documentation | behavior analysis files | Completed |

### Defects Identified

- login:
  - empty string treated as valid input
- register:
  - accepts empty and null userId
  - accepts empty password
  - crashes on null password

**Status:**  
Substantially complete  
Remaining: mutation analysis, RIP worksheet, fix verification tests

---

## Eduardo Rosales — Target 3 (hardware)

| Work Item | Evidence Artifact | Status |
|---|---|---|
| Hardware baseline tests (checkout/checkin) | hardware test file | Completed |
| Hardware testing scope defined | `ProjectPlan.docx` | Completed |

**Status:**  
Baseline completed  
Remaining: CFG, CACC, partitioning, coverage report

---

# Notes

- Coverage is measured at the module level (`auth.py`) and includes `_encrypt`, `login`, and `register`
- Structural testing focuses on `_encrypt`, so uncovered lines belong to other functions
- All feasible paths in `_encrypt` are fully covered; infeasible branch is correctly excluded

---

# Final Status

## Completed
- Structural testing (CFG, node, edge, prime paths) _encrypt()
- Input space partitioning (all auth modules)
- CACC logic coverage  _encrypt()
- Behavior analysis
- Coverage improvement demonstrated

## Remaining (Critical)
- Mutation and RIP analysis (required by project plan)
- Hardware formal testing artifacts
- Final report integration and presentation

---

# Project Status

Approximately 85–90% complete

