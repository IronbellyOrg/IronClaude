---
high_severity_count: 1
medium_severity_count: 0
low_severity_count: 0
total_deviations: 1
validation_complete: false
tasklist_ready: false
---

# Spec Fidelity Report (Convergence Mode)

**Convergence Result**: FAIL
**Runs Completed**: 3
**Final HIGH Count**: 1

## Structural Progress
- Run 1 (catch): structural 0 -> 6, budget: consumed=10, reimbursed=0, available=51
- Run 2 (verify): structural 6 -> 1, budget: consumed=28, reimbursed=0, available=33
- Run 2: progress credit 20 turns (structural 6 -> 1)
- Run 3 (backup): structural 1 -> 1, budget: consumed=46, reimbursed=20, available=35

## Halt Reason
Convergence not reached after 3 runs. Remaining active HIGHs: 1. TurnLedger: available=35, consumed=46
