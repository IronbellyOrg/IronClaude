# Q6 decision — M==0 reason slug

Status: Resolved
Date: 2026-06-20
Task step: 0.2

**DECISION: RESOLVED → Option B (working default, preserves FR-RH2.7 literally; map M==0 onto an existing BLOCKED Stage-1 slug)**

**Recommended:** Option B

**Chosen existing Stage-1 slug for implementation/tests:** `contract-missing`.

## Verbatim source facts

Spec §5.3 `mn_guard_table` row 1:

```yaml
  - {condition: "M==0 (all workers failed / no artifacts)", verdict: blocked,  exit: 2,  slug: "ensemble-empty"}
```

Spec FR-RH2.9 acceptance bullet:

> An M==0 outcome routes `blocked` (exit 2), not `degraded`.

Spec FR-RH2.7 acceptance bullet:

> `derive_verdict` and the `Verdict` exit-code map (`pass→0`, `halted→10`, `degraded→11`, `blocked→2`) are unchanged.

TDD §22 Q6 establishes that the spec vocabulary assigns `ensemble-empty`, but `ensemble-empty` is absent from `src/superclaude/cli/reflect/contract.py` (grep returned zero hits). Existing BLOCKED slugs are structural: `child-crash` / `contract-missing` at `contract.py:156-163`, `contract-version-missing` at `contract.py:167-170`, `unknown-major-version` at `contract.py:175-178`, `malformed-degraded-components` at `contract.py:187-190`, and `malformed-contract-boolean` at `contract.py:203-206`.

## Options considered

### Option B — preserve FR-RH2.7 literally (selected working default)

`ensemble.py` maps the empty-ensemble condition onto an EXISTING BLOCKED Stage-1 slug so the verdict map stays byte-identical, `derive_verdict` is UNTOUCHED, and FR-RH2.7 ("`derive_verdict` ... unchanged") is preserved literally. Cost: the reason slug is less specific than the spec vocabulary. This record chooses `contract-missing` as the concrete existing slug because M==0 means no trustworthy reviewer artifact/contract can support a Tier-2 verdict, and `derive_verdict(None, ...)` already returns BLOCKED/`contract-missing` with exit 2.

### Option A — add `ensemble-empty` to `derive_verdict` (not selected)

Add `ensemble-empty` as a NEW M==0 BLOCKED branch in `derive_verdict`. This preserves the 4-state verdict and exit code (`blocked`/2) but deliberately amends the FR-RH2.7 claim that `derive_verdict` is unchanged. This must only happen if a human edits this decision record before Step 3.1 to override the working default.

## Downstream effect

This item informs (does not halt) Phase 3 Step 3.1 M==0 wiring and Phase 6 I6 slug assertion. Unless a human edits this record before Step 3.1, implementation and tests must assert M==0 → BLOCKED/exit 2 with reason slug `contract-missing`, not `ensemble-empty`.

Override window: a human may edit this record to Option A before Step 3.1 runs. Absent that override, Option B ships.
