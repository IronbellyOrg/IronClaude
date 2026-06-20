# WS-C Deletion Authorization (Step 5.1 — L5 gate-check)

**Decision: AUTHORIZED**
**Date:** 2026-06-16

## Gate inputs (both required true)
- `phase-outputs/plans/parity-gate-status.md` → **PARITY_GREEN: true** (PG4.6; rebuilt CLI-vs-golden gate GREEN, deletion-survivability proven, 0 fix cycles).
- `phase-outputs/plans/golden-capture-verdict.md` → **PASS** (frozen golden complete: 3 scenario dirs, all per-reviewer `.md` + `return-contract.yaml` non-zero).

## Determination
Both conditions are satisfied: the permanent parity gate is GREEN and a complete frozen golden exists. The legacy retirement may proceed (mirrors the prior T08.07-after-T08.11 ordering). The rebuilt `test_bare_review_parity.py` keeps asserting after deletion (no `LEGACY_SCRIPT`/`importlib`/`skipif` runtime dependency — proven at PG4 by physically removing the script).

## AUTHORIZED actions (Phase 5 / WS-C)
1. Rework the second legacy-coupled test `tests/swarm/test_recipe_bare_review.py` (remove `assert LEGACY_SCRIPT.exists()` + legacy importlib; preserve legacy-independent tests) — Step 5.2.
2. `git rm` the 3 legacy scripts: `t2_preflight.sh`, `t2_dispatch.sh`, `t2_normalize.py` (+ clean `__pycache__`) — Steps 5.3-5.5.
3. `git rm` the 2 orphaned refs: `refs/prompts.md`, `refs/output-template.md` (KEEP `refs/templates/bare-review-output.md`) — Steps 5.6-5.7.
4. Reference scan + sync (`make sync-dev && make verify-sync`) + disk-verify + post-deletion gate — Steps 5.8-5.11.

Stage ONLY the `src/` side; NEVER `git add` any `.claude/` path (the sync regenerates the mirror).
