# QA Verification — Structural (cycle 2)

Date: 2026-06-20
Verdict: **PASS** (4/4 checks)

| # | Check | Result |
|---|-------|--------|
| 1 | Tier-1 negative `test_i11b_tier1_audit_once_does_not_call_ensemble` exists, builds genuine `depth="quick"` config, asserts ensemble spy NOT called + ClaudeProcess called; non-vacuous | PASS |
| 2 | Strengthened I10 partitions on `<<<TARGET>>>`; instruction prefix = lens fragment, no `/sc:reflect`; `/sc:reflect` only in target block; fixture-independent | PASS |
| 3 | Fix-D rejection sound: Steps 4.2/8.1 are immutable checklist items (F4); DoD matrix NFR-RH2.6 row records the guard extension scoping — substantive, not a cop-out | PASS |
| 4 | No regression: `tests/cli/reflect` 104 passed/1 xpassed; protected-floor `git diff` empty; touched-surface ruff clean; no forbidden NFR-7/proxy token | PASS |

Cycle-1 → cycle-2: all three IMPORTANT findings resolved or soundly rejected. No
further structural fix cycle required.

(Authored by the orchestrator from the cycle-2 structural rf-qa agent's returned
findings; verification commands re-run and confirmed.)
