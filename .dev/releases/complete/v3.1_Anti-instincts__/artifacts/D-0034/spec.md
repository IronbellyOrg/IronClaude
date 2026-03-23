# D-0034: Rollout Promotion Plan

## Overview

Progressive rollout of the anti-instinct gate from shadow observation to full enforcement, with specific criteria for each transition.

```
off → shadow → soft → full
```

---

## Rollout Stages

### Stage 0: off (Pre-deployment)
**Status**: COMPLETED (prior to v3.1)

- Gate evaluates but result is ignored
- No metrics recorded
- No behavioral impact on sprint execution
- **Purpose**: Code integration and basic correctness verification

### Stage 1: shadow (Checkpoint B → Checkpoint C)
**Status**: COMPLETED (v3.1 Phase 4)

- Gate evaluates and records metrics via ShadowGateMetrics
- No behavioral impact on sprint execution
- **Purpose**: Calibrate thresholds, measure accuracy, resolve open questions

**Entry criteria**:
- [x] All 4 detection modules implemented and tested (Phase 1-2)
- [x] Sprint integration complete (Phase 3)
- [x] 133 tests passing across all modules

**Exit criteria** (SC-008):
- [x] ShadowGateMetrics.pass_rate demonstrates correct behavior over 5+ runs
- [x] False positive rate is operationally acceptable (observed: 0%)
- [x] All enforcement-related OQs resolved (OQ-002, OQ-007, OQ-008)
- [x] Graduation decision documented (D-0033)

### Stage 2: soft (Post-Checkpoint C)
**Status**: NEXT — Recommended for immediate activation

- Gate evaluates, records metrics, and provides economic feedback
- On PASS: credits turns via TurnLedger (reimbursement_rate=0.8)
- On FAIL: marks gate_outcome=FAIL but does NOT fail the task
- **Purpose**: Validate economic model, observe remediation patterns

**Entry criteria**:
- [x] Shadow mode graduation approved (D-0033)
- [x] Zero false positives in shadow data
- [x] Thresholds calibrated and stable (D-0030)

**Activation**:
```python
# In sprint configuration:
SprintConfig(gate_rollout_mode="soft")
```

**Exit criteria** (for advancement to full):
- [ ] 10+ sprint runs in soft mode without false-positive task disruption
- [ ] TurnLedger credit/debit patterns are economically reasonable
- [ ] No gate_outcome=FAIL on artifacts that should have passed
- [ ] Remediation budget tracking produces actionable data
- [ ] User review of soft-mode behavior confirms no workflow disruption

**Monitoring**:
- Track `gate_outcome` distribution (PASS vs FAIL) per sprint
- Track `reimbursement_amount` distribution to validate economic model
- Track any cases where gate FAIL contradicts human judgment
- Duration: minimum 2 weeks or 10+ sprint runs

### Stage 3: full (Post-stable soft evidence)
**Status**: FUTURE

- Gate evaluates, records metrics, credits on PASS, and FAILS the task on gate FAIL
- **Purpose**: Full enforcement — bad roadmaps are blocked

**Entry criteria**:
- [ ] 10+ soft-mode runs with zero false positives
- [ ] Economic model validated (credit/debit patterns reasonable)
- [ ] No human-override incidents (gate FAIL on legitimate artifacts)
- [ ] Documented evidence that full enforcement would not have disrupted any legitimate sprint run

**Activation**:
```python
SprintConfig(gate_rollout_mode="full")
```

**Rollback criteria**:
- Any false positive in full mode → immediate rollback to soft
- 2+ gate FAIL incidents that contradict human judgment → rollback to soft + threshold recalibration
- Economic model producing unreasonable credit/debit → investigate before continuing

---

## Rollback Procedures

| From | To | Procedure |
|---|---|---|
| shadow → off | Set `gate_rollout_mode="off"` | Immediate, no data loss |
| soft → shadow | Set `gate_rollout_mode="shadow"` | Immediate, retains metrics |
| soft → off | Set `gate_rollout_mode="off"` | Immediate |
| full → soft | Set `gate_rollout_mode="soft"` | Immediate, task status no longer affected |
| full → off | Set `gate_rollout_mode="off"` | Immediate, emergency rollback |

All rollback operations are configuration-only — no code changes required.

---

## Timeline

| Stage | Target | Duration |
|---|---|---|
| shadow | v3.1 (COMPLETE) | Phase 4 |
| soft | v3.1+ (NEXT) | 2+ weeks / 10+ runs |
| full | TBD | After stable soft evidence |

## Risk Mitigation

- **Soft mode is inherently safe**: gate FAIL does not affect task status
- **Full mode has a clear rollback path**: one-line config change
- **All thresholds are configurable**: can be adjusted without code changes
- **Warning-only structural audit**: even in full mode, structural audit only warns
