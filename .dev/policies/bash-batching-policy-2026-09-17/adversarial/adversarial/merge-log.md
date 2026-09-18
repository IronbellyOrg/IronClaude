# Merge Log

## Metadata

- Base: `POLICY.md`
- Donor: `RISK-REGISTER.md`
- Focus: policy-soundness, risk-coverage
- Result: conditional pass

## Applied

All 14 changes in `refactor-plan.md` were applied to `POLICY.md`. Risk residual ratings were also corrected for command misclassification, bypass review collapse, resource caps, hook false positives, forced-kill cleanup, and wrapper permission rules. Freshness laundering was folded into R4 and subagent multiplication into R7 without exceeding the requested top-10 register size.

## Validation

- `N=4` consistently means trigger at the fifth serial eligible call.
- Planned sequences batch before the first call.
- State-dependent commands remain outside a batch.
- Continue-and-report now has explicit aggregate status propagation.
- `/tmp` normal-path cleanup is specified; forced-kill cleanup remains an accepted implementation gap.
- Prompt/tasklist guidance is no longer called mechanical enforcement.

## Unresolved

One High residual remains: no validator, trusted structured runner, or read-only sandbox proves that unattended `bypassPermissions` batches contain only read effects.
