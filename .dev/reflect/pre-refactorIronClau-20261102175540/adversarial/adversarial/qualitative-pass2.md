# Qualitative scoring — Pass 2 (reverse order 3, 2, 1)

Returned by a read-only scoring agent; persisted by the orchestrator. NOT MET verdicts reproduced in full, with the summary.

## NOT MET verdicts
- Variant 3: C1 (no finding on `.claude/` staging or proof internal checkouts work); L1 (R3-F1 "likely a fifth ... or a project-worktree rewrite" leaves the class open); R3 (R3-F5 names a leftover worktree but gives no recovery); E1.
- Variant 2: C5 (no out-of-scope statement); K1 (R2-F4 misquotes .gitignore:129); K3 (R2-F4 calls drift a constraint CLAUDE.md's absolute rule authorizes); T1 (order Task 3, Task 1, Task 6/7, Constraints with no principle); L4 ("INF-007", "T1 S2" undefined); R3; R4 (Orca surface only an inferred claim); E4 (no count check; misses the eval_runner hit).
- Variant 1: C1 (no `.claude/` staging finding; misses eval_runner.py); L3 (R1-2 headline two sentences); E1.

## Agent notes
- R3-F1's added regex matched scripts/eval_runner.py:143 when run; it also matches tests/unit/test_ccsession_tag.py:1858, :1912 and tests/troubleshoot/backtest/test_git_replay_unit.py:34, none of which Variant 3 mentions.
- `.claude/cache/sc-recommend-lookup.yaml` is tracked (`git ls-files`).
- T5 uncertain: no reviewer-card schema found; src/superclaude/commands/reflect.md:185 mentions a `missing_requirements` list that only Variant 2 carries.

## Summary
| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total/30 |
|---|---|---|---|---|---|---|---|
| 3 | 4 | 5 | 5 | 4 | 4 | 4 | 26 |
| 2 | 4 | 3 | 4 | 4 | 3 | 4 | 22 |
| 1 | 4 | 5 | 5 | 4 | 5 | 4 | 27 |
