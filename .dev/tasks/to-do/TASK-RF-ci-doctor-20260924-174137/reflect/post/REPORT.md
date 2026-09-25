```yaml
contract_version: 1.7.0
status: partial
mode: post
tier_reached: 2
confidence_calibrated: 0.39
citations_total: 8
citations_revalidated: 8
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
reachability_gate_ran: false
reachability_ledger_path: null
reachability_requirements_scanned: 0
reachability_unreachable: 0
reachability_unproven: 0
reachability_real_boot_ran: false
reachability_skip_reason: no-side-effect-requirements
```

# POST reflection — TASK-RF-ci-doctor

**Merged verdict:** PASS-with-deviations
**run_id:** 20260924T194205Z-post-ci-doctor
**merge_method:** single-reviewer-fallback (F2; debate advocates blocked in nested Claude session)

## Deviations

### Deviation D-001: One-step doctor-check insert

- **Location:** `.github/workflows/test.yml:217-219`
- **Mapped tasklist item:** Step-2.1
- **Spec section:** related FR-1 then FR-4 (not `--spec`)
- **Evidence:** named step `Install native components` runs `superclaude install` after dependencies and before `superclaude doctor --verbose`
- **Classification:** none
- **Default remediation:** none

### Deviation D-002: Diff-file POST input

- **Location:** `TASK-RF-ci-doctor-20260924-174137.md:130-132`
- **Mapped tasklist item:** Step-4.2
- **Spec section:** sc-reflect `refs/input-resolution.md` `--diff` file path
- **Evidence:** unstaged hunk; `{BASE}..HEAD` would be empty
- **Classification:** necessary
- **Default remediation:** none (supported skill flag)

### Deviation D-003: `--no-promote`

- **Location:** `TASK-RF-ci-doctor-20260924-174137.md:130-132`
- **Mapped tasklist item:** Step-4.2
- **Spec section:** sc-reflect §14.5
- **Evidence:** to-do path must remain until Step 4.3
- **Classification:** necessary
- **Default remediation:** none

### Deviation D-004: Uncommitted workflow change

- **Location:** `.github/workflows/test.yml` working tree
- **Mapped tasklist item:** Step-2.1
- **Spec section:** BUILD-REQUEST EXECUTION_SCOPE
- **Evidence:** task forbids commit/push
- **Classification:** necessary
- **Default remediation:** none until separately authorized commit

## Grounding Gaps

- Verification triangle skipped (`execute_shell_command` unavailable). Captured task-log: install-integration 8 passed; isolated PRE doctor exit 1, install 0, POST 0.

## Dropped citations

- R2-1: `superclaude install` missing `--no-promote` — install CLI has no such flag.

## Recommendations

- Do not edit production doctor/install code.
- Do not promote this to-do folder.
- Remote GitHub doctor-check remains a follow-up after an authorized push.
