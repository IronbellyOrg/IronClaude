# remediate_parser.py deletion DEFERRED

**Evaluated:** 2026-06-03 21:02 · Branch `integration`

## Verdict: **HALT** (remediate_parser.py NOT deleted or modified)

### (i) Cutover precondition NOT-MET — `remediation` step

`.dev/migrations/r1-4-cutover-counters.yaml` `steps.remediation` (verbatim):

```
remediation:
  tool_write_flag_default: false
  release_marker_count: 0
  last_marker_release: ""
  cutover_eligible: false
  cutover_at_count: 3
```

`cutover_eligible: false` (0/3) → NOT eligible → deletion HALTED.

### (ii) Zero production callers, but cutover-deferred + 3 live test callers

- `src/superclaude/cli/roadmap/remediate_parser.py` **exists** and has **ZERO production callers** in `src/`. The only `src/` mentions of "remediate_parser" are in `src/superclaude/cli/roadmap/remediate.py` at L22 (module docstring bullet) and L426 (inline comment) — **neither is an import or a call** (verified: no `from .remediate_parser import`, no `remediate_parser.` invocation).
- It is nonetheless explicitly **cutover-deferred** per the parent task (research file `05-area-de-dualwrite-vectorA-registry.md` Finding 4).
- **3 test files still CALL its functions** (all confirmed to exist):
  - `tests/roadmap/test_remediate_parser.py`
  - `tests/roadmap/test_pipeline_integration.py`
  - `tests/roadmap/test_phase7_hardening.py`

Therefore deletion would require BOTH (a) removing/retargeting those 3 calling test files AND (b) meeting the ≥3-parity-cycle cutover precondition (`remediation.cutover_eligible: true`). Neither holds today.

## Zero production-code / test change (explicit)

- `src/superclaude/cli/roadmap/remediate_parser.py` was **NOT** deleted or modified by this item.
- The 3 calling test files were **NOT** deleted or retargeted.

Under the current state the "proceed" branch (delete the parser + retarget the 3 tests) is NOT taken. Removal additionally requires SEPARATE user authorization (Open Questions).
