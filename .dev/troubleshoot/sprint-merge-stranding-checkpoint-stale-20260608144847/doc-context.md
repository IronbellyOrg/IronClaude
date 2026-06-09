# Documentation Context Card

## Release context
No release-doc governs this surface as a contract. The code references an internal "TDD §T5" (7-step merge sequence) and "§T9" (post-merge verify-checkpoints auto-invoke) in comments only; those steps were specified for `results/` file families, never for TASKLIST_ROOT deliverable trees or stale-verdict re-evaluation.

## Architectural docs consulted
- `recovery.py` module docstring + step comments (merge sequence) — CURRENT (matches code).
- `checkpoints.py` `recover_missing_checkpoints` docstring (lines 220-244) — CURRENT; explicitly documents the *intended* "regenerate only missing files" behavior, confirming the stale-verdict gap is a design omission, not a regression.

## Restrictions / decisions that constrain the fix
- `recover_missing_checkpoints` deliberately stamps recovered checkpoints `UNKNOWN`, never `PASS`, because "the original real-time verification did not occur" (checkpoints.py:436-437). Any Defect-2 fix MUST honor this: never auto-flip a checkpoint to PASS from artifact heuristics.
- `merge_recovery_bundle` is verb-agnostic (future `sprint repair from-reflect` consumer). New params must default to preserve today's behavior.
- Steps 1-3 preserve prior canonical files as `.failed-<ts>` (forensic). Deliverable-tree copy-back should follow a compatible overwrite/preserve discipline.

## Re-frame signals
- Both defects share ONE root: the rerun executes with `release_dir=bundle` + `TASKLIST_ROOT=bundle`, redirecting every release-anchored output into the bundle, while the merge reconciles only the three `results/phase-N-*` file families. Deliverable trees (Defect 1) and the end-of-phase checkpoint verdict (Defect 2) both live outside that narrow reconciliation.
- `behavior_is_documented = false`. The success-but-stranded behavior is a genuine code-side data-integrity gap.
