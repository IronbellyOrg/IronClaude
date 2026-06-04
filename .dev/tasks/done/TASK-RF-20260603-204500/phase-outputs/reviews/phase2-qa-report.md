# Phase 2 QA Gate Report (F4) — task-integrity

**Date:** 2026-06-03 · **Verdict: PASS** (6/6, 0 fixes) · Fix cycles: 0

rf-qa (adversarial, fix_authorization, behavioral verification) verified the F4 1a-wire path:

| # | Check | Result |
|---|---|---|
| 1 | `eval plugin` calls run_preconditions→evaluate_adoption→patch_plugin_row in order; run_preconditions FIRST; HARD-BLOCK → print + `sys.exit(1)` (live test: exited 1, wrote no plugin.yaml); helpers no longer orphaned | PASS |
| 2 | Subcommand flags/contracts match real `plugin_eval.py` signatures; no fabricated flags | PASS |
| 3 | SKILL.md Phase 3 names real `recommend eval plugin` + 4-phase lifecycle → spec:211-220; threshold (+≥0.10 OR −≤−0.20, pass_rate must-not-regress) correct; R3 preserved | PASS |
| 4 | Tests cover HARD-BLOCK-raises + warn/skip + 3 adoption verdicts + patch round-trip; tmp_path only; `pytest` → 8 passed (re-run live) | PASS |
| 5 | No `import anthropic` in `cli/recommend/` | PASS |
| 6 | Deterministic core not modified beyond wiring (additive) | PASS |

Behavioral evidence (not trusting the summary): live CLI HARD-BLOCK exit-1 + no-patch; all 3 adoption verdicts re-run; t3 (50% token drop but pass-rate regressed → still `evaluated_negative`) proves the `must_not_regress` guard dominates. 0 issues, 0 fixes.
