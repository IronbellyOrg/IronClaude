# A/B plans for the top 3 designs of RESEARCH-REPORT.md (baseline = Stage 2 arm 3, a3-r1..r6)

- PLAN-1-k3-union-verify.md: design 3.1 (k=3 first reviews, deterministic merge, verify gate), branch `346Claude-ab1-k3-union-verify`, runs b1-r1..r6 in `$SP/p12/ab1`; about 50 Sonnet workers (max 72), about 4.7M output tokens.
- PLAN-2-verify-gate.md: design 3.2 (verify-before-fix gate, k=1), branch `346Claude-ab2-verify-gate`, runs b2-r1..r6 in `$SP/p12/ab2`; about 40 workers (max 60), about 3.4M output tokens.
- PLAN-3-final-gate.md: design 3.3 (final whole-document gate, at most one gate loop, stall rule, ceiling 5 reviews / 3 fix cycles), branch `346Claude-ab3-final-gate`, runs b3-r1..r6 in `$SP/p12/ab3`; about 48 workers (max 60), about 4.6M output tokens.

Every plan gives each final spec two frozen audits and stays at or under 6 concurrent workers. The product edits of all three plans were checked in a throwaway clone of 69ac8b33: the new tests fail before the edits and pass after them; the 273 pinned tests pass; ruff is clean. With design 3 applied, `tests/skills` plus `tests/unit` gave 1 failure, `test_task_workspace_smoke.py::test_installer_ships_scripts_and_documented_invocation_runs`, which also fails on 69ac8b33 without the edits.

Open questions (I could not resolve these from the files):
1. Token baseline: the 0.33M in STAGE2-REPORT.md is an undercount, because state.json misses R1 of a3-r1..r3 and V1 of a3-r1. From the transcripts, the loop alone is 243,056 and the loop plus one audit is 381,702. The plans base their cost rules on 381,702 (the Stage 2 per-replicate definition) and exclude the second audit. Confirm this before launch: on a loop-only basis the cost rules for designs 1 and 3 would probably fire.
2. The baseline second audits under `$SP/p12/baseline-audit2/` were in progress when these plans were written. The plans score the reports directly and do not use `results.json` `n_blocking`, which counts regex tokens in raw text. Until the second audits exist, every comparison is labelled PROVISIONAL.
3. Orca is not installed here, so each implementer works in a private `git clone` under `$SP/p12/abN/repo`. Confirm this is acceptable under the CLAUDE.md worktree rule.
4. The three plans make no new baseline runs. Two fresh baseline replicates against drift run only if the coordinator asks (about 0.7-0.76M tokens).
