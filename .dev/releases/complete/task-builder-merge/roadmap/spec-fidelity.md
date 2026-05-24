---
high_severity_count: 10
medium_severity_count: 0
low_severity_count: 0
total_deviations: 10
validation_complete: false
tasklist_ready: false
---

# Spec Fidelity Report (Convergence Mode)

**Convergence Result**: FAIL
**Runs Completed**: 3
**Final HIGH Count**: 10

## Structural Progress
- Run 1 (catch): structural 0 -> 15, budget: consumed=10, reimbursed=0, available=51
- Run 2 (verify): structural 15 -> 15, budget: consumed=28, reimbursed=0, available=33
- Run 3 (backup): structural 15 -> 10, budget: consumed=46, reimbursed=0, available=15
- Run 3: progress credit 20 turns (structural 15 -> 10)

## Halt Reason
Convergence not reached after 3 runs. Remaining active HIGHs: 10. TurnLedger: available=35, consumed=46
