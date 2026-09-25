# Refactoring Plan

Base: Variant 2. Approval: auto-approved.

## Planned Changes

1. **Entry table** (V1) → merge § Wave 8 arm table into FRs. Risk: Low.
2. **MIX pending test** (V3 AC-CLS-4) → test plan. Risk: Low.
3. **as_array empty test** (V3) → test plan. Risk: Low.
4. **E9** (V3): nonempty `--required` may ignore optional pending — document, not a bug. Risk: Low.
5. Drop V2 `incomplete` JSON field if script `state:polling` on parse miss is enough. Risk: Low.

## Changes NOT Being Made
- Separate CI round budget (all variants rejected)
- `--ci-timeout` (defer)
- `fsm.py` edits
- New EventType
