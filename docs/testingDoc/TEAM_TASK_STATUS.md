# Team Task Status (Project Plan Alignment)

This document summarizes what is still required per the Project Plan and what 
has already been completed in the repository.

## Remaining Work (Per Project Plan)

| Person/Team | Pending Item | Plan Basis | Evidence Gap in Current Repo | Status |
|---|---|---|---|---|
| Anita Woodford | Integrate all module outputs into one final report package with before/after coverage tables. | Team Responsibility + Milestone 6 | No single consolidated final testing report file yet. | Pending |
| Anita Woodford | Add final defect summary and presentation-ready test evidence bundle. | Team Responsibility + Milestone 6 | Defect evidence exists across files but not yet packaged as one final submission set. | Pending |
| David Cho | Create RIP worksheet for the login/register userId plaintext defect. | Target 2 Deliverables | No RIP worksheet artifact is present in testing docs. | Pending |
| David Cho | Add mutation-analysis artifact for login/register defect exposure. | Target 2 Deliverables | No dedicated mutation-analysis artifact for this defect is present. | Pending |
| David Cho | Add fix-verification tests for login/register if code fix is applied. | Target 2 Deliverables | Baseline endpoint tests exist, but no explicit fix-verification set is present. | Pending |
| Eduardo Rosales | Implement hardware checkout/checkin formal pytest suite. | Target 3 Deliverables | No hardware-specific pytest files are currently present in testing folder. | Pending |
| Eduardo Rosales | Add hardware CFG and prime-path/edge-pair test design artifact. | Target 3 Deliverables | No hardware CFG artifact is currently present in testing docs. | Pending |
| Eduardo Rosales | Add CACC and input partition model for availability predicate. | Target 3 Deliverables | No hardware CACC or partition model artifact is currently present. | Pending |
| Eduardo Rosales | Generate hardware coverage report and store under coverage-reports. | Target 3 Deliverables | No hardware structural coverage file is currently present. | Pending |
| Whole Team | Complete remaining milestone phases (structural completion, partitioning, mutation/RIP, report packaging). | Milestones 3-6 | Encrypt work is advanced; hardware and auth-defect RIP artifacts are not complete at the same level. | Pending |

## Quick Checklist (Action Items)

### Anita Woodford

- [ ] Add `_encrypt` mutant list in `testing/mutation-analysis`.
- [ ] Add `_encrypt` RIP worksheet in `testing/mutation-analysis`.
- [ ] Add `_encrypt` killed/survived summary table in `testing/mutation-analysis`.
- [ ] Add short mutation summary for `_encrypt` in `docs/testingDoc/encrypt-analysis.md`.
- [ ] Consolidate final report package with before/after coverage table and defect summary.

### David Cho

- [ ] Create RIP worksheet for `login/register` userId plaintext defect.
- [ ] Add mutation-analysis artifact for `login/register` defect exposure.
- [ ] Add fix-verification tests for `login/register` if code fix is applied.

### Eduardo Rosales

- [ ] Implement `hardware` checkout/checkin pytest suite.
- [ ] Add hardware CFG + edge-pair/prime-path artifact.
- [ ] Add CACC + input partition model for availability predicate.
- [ ] Generate and save hardware coverage report in `testing/coverage-reports`.

### Whole Team

- [ ] Finish Milestones 3-6 deliverables as a complete package.
- [ ] Merge module evidence into one final report and presentation bundle.

## Completed So Far

| Work Item | Contributor | Evidence Artifact | Current Status |
|---|---|---|---|
| Project planning and scope definition | Anita Woodford | docs/testingDoc/ProjectPlan.docx | Completed |
| Repository setup and project structure organization | Anita Woodford | testing, docs/testingDoc, docs/design folders and test/report structure | Completed |
| Baseline auth endpoint tests for register and login | David Cho (git author: chodavey) | testing/baseline-tests/test_auth.py, commit 001eb9a | Completed |
| Baseline tests for _encrypt function | Anita Woodford | testing/baseline-tests/test_auth_encrypt.py, commit b5b459d | Completed |
| Structural tests for _encrypt function | Anita Woodford | testing/structural-test/test_app_encrypt_structural.py, commit aee6bcd | Completed |
| Encrypt analysis documentation updates | Anita Woodford | docs/testingDoc/encrypt-analysis.md, commits 3216757 and aee6bcd | Completed |
| Combined auth baseline coverage run (encrypt + login/register) | Anita Woodford + David Cho artifacts combined | testing/coverage-reports/auth-baseline-combined-coverage.txt | Completed |
| Hardware checkout/checkin formal testing target | Eduardo Rosales | Assignment listed in docs/testingDoc/ProjectPlan.docx | In Progress |
| Final integrated report packaging and presentation bundle | Team | docs/testingDoc + testing/coverage-reports final packaging | In Progress |

## Notes

- Coverage files for auth module are module-level measurements for backend/app/routes/auth.py, which includes _encrypt, login, and register.
- Encrypt-focused baseline and structural runs are valid for function-focused progress, even though coverage reports show auth.py as the measured module.
