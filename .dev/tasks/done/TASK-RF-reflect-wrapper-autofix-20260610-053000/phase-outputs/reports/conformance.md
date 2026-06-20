# Conformance Report — Contract §§2–7 + 9 Acceptance Criteria (Step 7.3)

**Date:** 2026-06-10
**Branch:** `feat/reflect-wrapper-autofix` @ base `a5343f57`
**Contract:** `.dev/handoffs/reflect-wrapper-contract.md` (v1.0; reflect skill target 1.4.0)
**Spec:** `.dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md` §8

## Part A — Contract §§2–7 requirement → implementation + test

| Contract § | Requirement | Implementation (file:line) | Covering test | Verdict |
|---|---|---|---|---|
| §2 O1 shape | `reflect run <abs> --depth deep --fix --promote` parses & routes | `commands.py` options `--depth`/`--fix`/`--promote` (default True) + threaded to `resolve_config` | `test_promote_plumbing.py::test_o1_default_prompt_omits_no_promote`; pipx `--help` (phase7-pipx-help) | CONFORMS |
| §2 O2 shape | `... --fix --no-promote --base <SHA>` parses & routes | `--base`→`base_override`, `--no-promote` | `test_promote_plumbing.py::test_o2_...`; `test_base_precedence.py` | CONFORMS |
| §2 forbidden flags | no `--reflect`, no `--max-turns`, no `..` range | dial never added (base is audit-only); `--base` stored verbatim single-ref | `test_base_precedence.py::test_..._range_value_stored_verbatim_not_split` + de-range assert | CONFORMS |
| §2 exit codes | 0/10/11/2 fail-closed (only 0 completes) | `models.Verdict.exit_code` (unchanged v1) | `test_verdict_mapping.py` (v1) + `test_fix_loop.py` (10/11/2 paths) | CONFORMS |
| §3 recursion breaker | marker=="1" → exit 0 before audit; exported into every fix-subtree child; truthy exactly "1" | `commands.py` group-callback guard; `runner._WRAPPER_MARKER` exported in `_audit_once` + `_apply_remediation` | `test_marker_suppression.py` (5, incl. neg controls); `test_fix_loop.py` apply env_vars assert | CONFORMS |
| §4 AUTO-FIXABLE | solely drift/necessary, none of the hard signals | `contract.classify_fix` (pure) | `test_classify_fix.py` (11 matrix rows) | CONFORMS |
| §4 HUMAN-REQUIRED | any hard signal OR degraded/blocked → terminal HALT, no /task, no promote | `classify_fix` + loop `verdict is not HALTED → break` | `test_classify_fix.py` + `test_fix_loop.py::test_human_required_halts_no_apply` / `test_degraded_with_drift_never_autofixed` / `test_blocked_with_drift_never_autofixed` | CONFORMS |
| §4 bound (D3) | `--max-fix-iterations` default 2; sidecar `fix_iterations`/`fix_converged` | loop `iteration > max` break; `write_sidecar` fields | `test_fix_loop.py::test_non_convergence_exit10_five_launches` | CONFORMS |
| §4 enabling field | reflect emits `remediation_task_path: <abs>|null`; wrapper reads | SKILL.md:746 (emit) → `contract._make_result` `c.get("remediation_task_path")` (consume) | PG5 cross-check + `test_fix_loop.py` (drives apply / cannot-repair) | CONFORMS |
| §4 honors human-decision-halt | no auto-applied default ships a human-decision change | human-required → terminal HALT before apply | `test_fix_loop.py::test_human_required_halts_no_apply` | CONFORMS |
| §5 promotion | O1 `--promote` default; NO wrapper-side O2 force (generator's job) | `--promote` default True; no O2 detection in wrapper | `test_promote_plumbing.py` (3); PG3 confirmed no O2 logic | CONFORMS |
| §6 frontmatter | `start_commit` base precedence (`--base` > start_commit > merge-base) | `config._resolve_base` short-circuit | `test_base_precedence.py` (3 precedence branches) | CONFORMS |
| **§7 / NFR-2 cost band** | docs state deep band + `(iterations+1)` audits + `iterations` applies bound | contract §7:179-186 documents it; `--max-fix-iterations` enforces; loop arithmetic = (N+1) audits + N applies | `test_fix_loop.py` call_count==3 (N=1), ==5 (N=2) PINS the arithmetic; consistent with §7 | CONFORMS |

## Part B — Nine Acceptance Criteria (§8) → covering test + PASS/FAIL

| AC | Criterion | Covering test | Status |
|---|---|---|---|
| AC-1 | marker self-suppress exit 0 | `test_marker_suppression.py::test_marker_one_suppresses_before_launch` (+4) | PASS |
| AC-2 | drift-only + path → /task + re-audit → exit 0 | `test_fix_loop.py::test_convergence_exit0_three_launches` | PASS |
| AC-3 | hard signals → terminal HALT 10, no /task, no promote | `test_classify_fix.py` (11) + `test_fix_loop.py::test_human_required_halts_no_apply` | PASS |
| AC-4 | non-convergence → exit 10, fix_converged:false sidecar | `test_fix_loop.py::test_non_convergence_exit10_five_launches` | PASS |
| AC-5 | O1 promote / O2 --no-promote exit 0 verified-not-promoted | `test_promote_plumbing.py` (3) | PASS |
| AC-6 | --base overrides start_commit; --diff single ref | `test_base_precedence.py` (6) | PASS |
| AC-7 | reflect emits remediation_task_path (1.4.0); wrapper reads | SKILL.md:746 + `contract._make_result`; `test_fix_loop.py` consumes it | PASS |
| AC-8 | no sprint/roadmap import; no async; only ClaudeProcess; pipx exposes run | `test_no_nesting_guard.py` (thinness) + `phase7-pipx-help.md` | PASS |
| AC-9 | all v1 fail-closed tests green (FR-10) | full `tests/cli/reflect/` suite: 75 passed, 1 justified xfail | PASS |

## GAP analysis

**No unexplained GAP.** Every contract §§2–7 requirement and all nine §8 ACs map to concrete
implementation file:line + covering test with PASS status.

Two documented, non-blocking, out-of-this-task-scope items carried to Follow-Up Items:
1. The grounding-gaps→HUMAN-REQUIRED carve-out rests on reflect's external contract guarantee
   (`needs_human_decision IFF grounding-gaps non-empty`) — wrapper code is correct; flagged for the
   wrapper↔generator integration gate before O1/O2 go live.
2. `test_layer_a` (task-builder Mode-2 marker) is xfail(strict=False) — generator-side content, NFR-5
   decouple; auto-recovers (XPASS) when the generator lands.

## Validation state (Step 7.1 + 7.2)

- ruff check + ruff format --check (my files): clean. pytest reflect suite: 75 passed, 1 xfailed. `make verify-sync`: in sync.
- `pipx install --force` (from this worktree): `superclaude reflect run --help` resolves with `--fix`/`--no-fix`/`--max-fix-iterations`/`--base` + promote-default. NFR-5 met.
