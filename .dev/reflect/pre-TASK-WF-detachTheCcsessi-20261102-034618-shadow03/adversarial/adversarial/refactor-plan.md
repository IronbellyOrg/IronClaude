# Refactoring Plan (Step 4)

Base: Card 1. Approval: auto-approved (non-interactive).

## Planned Changes
1. Incorporate Card 2 F1 as MEDIUM, scope-halved per R2: "HC1 Pipeline Hardening requirement absent from coverage matrix and tasklist" (remediation-source.md:35); note HC5 discharged by the existing post-run audit (.dev/reflect/post-detachTheCcsessi-20261102044547/).
2. Incorporate Card 2 F3 as MEDIUM upgraded by INV-007: the narrowed grep excluded 3 path-referencing test files (tests/review/test_review_panel_live7.py, tests/skills/test_model_alias_policy.py, tests/skills/test_issue_worker_agents.py) from T5's certification run; non-blocking only because those files passed later.
3. Correct Card 1 F1's mechanism per INV-001: the verify-sync failure is unconditional in a fresh worktree (.claude/ gitignored, Makefile:174-176 MISSING branch), not caused by the src/ edits; conclusion (AC unmeetable without sync-dev) unchanged and strengthened.
4. Incorporate Card 3 F1 (isatty divergence) as MINOR strengthened by INV-004: verified invisible on BOTH test paths (fixture stderr is a file; outlives test redirects to /dev/null).
5. Correct Card 1 F4 per INV-003: no leak is possible (the exec'd sleep holds the terminal root's own pid and is killed by the root-kill); the finding reduces to "wrong certifier for the AC's claim".
6. Add INV-002 note to Card 1 F2: the pid AC can also false-fail on external state (reboot, operator restart).
7. Add INV-008 compounding note to the stale-anchor finding: plan:52's range at HEAD is streaming code ~150 lines from the real __main__.

## Changes NOT Being Made
- Card 2's original "largest coverage hole" framing (halved in R2).
- Card 3's MINOR on X-001 (withdrawn R2, unanimous MEDIUM).
- Any blocking finding: none survived the debate or the invariant probe.

## Risk Summary
All changes additive/wording; risk Low. Merged verdict remains PASS (0 blocking, 3 medium, 4 minor).
