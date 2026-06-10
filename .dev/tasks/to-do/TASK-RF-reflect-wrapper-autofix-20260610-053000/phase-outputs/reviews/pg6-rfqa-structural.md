# PG6 Structural QA Review — `tests/cli/reflect/`

**Reviewer:** rf-qa (adversarial, fail-closed structural lens)
**Date:** 2026-06-10
**Scope:** `tests/cli/reflect/**` + `phase6-summary.md`
**Authorization:** Report only — no fixes applied.

---

## Overall Verdict: **PASS**

All nine structural criteria verified against the source files (not just the summary's claims). The full suite reproduces **75 passed, 1 xfailed** under `uv run pytest tests/cli/reflect/`. The single xfail is a justified non-blocker (analysis below). Every thinness regex is correctly anchored and source-grounded; the apply-launch subprocess guard is correctly scoped to `runner.py` and would NOT false-positive on `commands.py`'s legitimate tmux `subprocess.run`. No CRITICAL findings.

---

## Per-criterion table

| # | Criterion | Result | Evidence (file:line) |
|---|-----------|--------|----------------------|
| 1 | Four `1.4.0` fixtures w/ correct shapes (drift+path / drift+null-path / human-required / postfix-pass) | **PASS** | `autofixable_drift.yaml:1` ver=1.4.0, drift=1 (L10), `remediation_task_path: /abs/...` (L28); `autofixable_drift_no_path.yaml:1` ver=1.4.0, drift=1, `remediation_task_path: null` (L28); `human_required_needs_decision.yaml:1` ver=1.4.0, `needs_human_decision: true` (L24), path null (L28); `postfix_pass.yaml:1` ver=1.4.0, `status: success` (L2), all-zero deviations (L8-11), all hard-signal bools false (L22-25) |
| 2 | AC-1 marker suppression: exit-0 assert + negative controls for `0`/absent/`2` | **PASS** | `test_marker_suppression.py`: exit-0 + `mock_cls.assert_not_called()` for `"1"` (L26-28, L38-40); neg controls `"0"`→not-suppressed (L56-66), absent→not-suppressed (L69-79), `"2"`→not-suppressed (L82-92). Helper asserts `_SUPPRESS_MSG not in output` AND `call_count >= 1` (L51-52). Exact-string-`"1"`-only discrimination confirmed. |
| 3 | AC-3 carve-out matrix: one row per HALT/HUMAN trigger incl. mixed drift+regression→human | **PASS** | `test_classify_fix.py`: drift-only→auto (L31), necessary-only→auto (L35), `regression_present`→human (L39), regression-count→human (L44), `needs_human_decision`→human (L48), `user_decision_required`→human (L53), `unauthorized_deviation`→human (L58), **mixed drift+regression→human** (L63-68), authorized-only→none (L71), all-zero→none (L76), malformed-bool→BLOCKED-upstream (L80-99). Matches source carve-out `contract.py:356-366` exactly (5 hard signals incl. `regression>0` count at L361). |
| 4 | AC-2/AC-4 bounded-loop EXACT call-count arithmetic + apply `env_vars` marker | **PASS** | `test_fix_loop.py`: convergence `call_count == 3` ((N+1)=2 audits + N=1 apply), `fix_iterations==1`, `fix_converged True` (L49-62); non-convergence `call_count == 5` (3 audits + 2 applies), `fix_iterations==2`, `fix_converged False` (L81-88); cannot-repair (null path) `call_count == 1`, `fix_iterations==0` (L99-102); apply `env_vars == {_MARKER: "1"}` (L56) AND audit-launch marker (L59). Arithmetic matches source loop `runner.py:535-576`. |
| 5 | AC-5 O1/O2 prompt asserts | **PASS** | `test_promote_plumbing.py`: O1 default → `--no-promote` absent (L26-28); O2 `--no-promote` → present (L33-35); CLI default-promote-on regression guard via `--print-command` (L46-52). Source `_build_prompt` plumbing confirmed indirectly via passing run. |
| 6 | AC-6 base precedence (3 branches) + de-range `..` absent | **PASS** | `test_base_precedence.py`: `--base` > frontmatter (L51-54); frontmatter > merge-base (L57-60); merge-base fallback (L63-71); de-range single-ref `.. not in diff_value` (L74-82); range-value stored verbatim/no-split (L85-93); +U7 resume short-circuit (L96-114). |
| 7 | AC-8 thinness guards: regexes ANCHORED (docstring false-positive dodge) + apply-launch guard SCOPED to runner.py | **PASS** | `test_no_nesting_guard.py`: regexes anchored on `^\s*(?:from\|import)` (L29-31), `^\s*async\s+def` (L33), `^\s*await\s` (L34), raw-call requires `\s*\(` (L38). **Independently re-ran all anchored regexes against `runner.py` → all False** (sprint/roadmap-import, async-def, await, raw-subprocess-call, import-subprocess) despite the docstring prose at `runner.py:9-10,436-437`. Apply guard `_RAW_SUBPROCESS_CALL_RE`/`_IMPORT_SUBPROCESS_RE` scoped to `_RUNNER_SRC` only (L120-134), explicitly avoiding `commands.py:267-274` tmux. |
| 8 | `_SPEC9_FLAGS` extended with four new flags | **PASS** | `test_cli_smoke.py:15-31`: `--fix`, `--no-fix`, `--max-fix-iterations`, `--base` added under "Auto-fix evolution flags (D1/D3/D6)" comment (L25-30); asserted present in `run --help` (L40-44). |
| 9 | Full suite PASSES per summary | **PASS** | Re-ran `uv run pytest tests/cli/reflect/` → **75 passed, 1 xfailed in 0.28s**. Matches `phase6-summary.md:8`. |

---

## CRITICAL-tier checks (all clear)

- **Missing AC:** none. AC-1..AC-9 all have covering tests (verified file-by-file, not from the summary's mapping table).
- **Unanchored thinness regex (docstring false-positive risk):** none. Independently executed all five anchored patterns against the real `runner.py` source — every one returns `False`, confirming the docstring prose (`- No imports from ...sprint...roadmap`, `Zero ``async def`` / ``await```, `never a raw ``subprocess.run`` / ``Popen```) does not trip the guards.
- **Wrong call-count assertion:** none. The (N+1)-audits + N-applies arithmetic (3 / 5 / 1) was checked against the actual `runner.py:535-576` loop and the sequence fixtures fed in each test; the convergence=3, non-convergence=5, cannot-repair=1 counts are internally consistent with the launch sequences.
- **Package-wide subprocess grep false-positive on commands.py tmux:** correctly avoided. Confirmed `commands.py:320,325,327` does use `subprocess.run(["tmux", ...])` and `commands.py:20` imports subprocess — a package-wide grep WOULD false-positive. The test scopes the raw-subprocess assertions to `_RUNNER_SRC` (runner.py) only. The package-wide guards that DO run across all `*.py` (`_SPRINT_ROADMAP_IMPORT_RE`, `_ASYNC_DEF_RE`, `_AWAIT_RE`) are safe because none of those tokens appear as code in `commands.py`.

---

## xfail adjudication (justified non-blocker)

`test_layer_a_wrapper_branch_is_bash_shellout` — `xfail(strict=False)` at `test_no_nesting_guard.py:63-74`.

**Verdict: justified non-blocker, NOT a missing/broken test.**

It asserts GENERATOR-side task-builder SKILL Mode-2 content (the `auto-resolved-2` marker / `**Mode `2` ... wrapper shell-out` block) that is emitted by the companion generator worktree, absent on this wrapper-only base. The xfail reason explicitly cites NFR-5 (forbids coupling the wrapper to unmerged generator work) and `strict=False` so it auto-recovers (XPASS-tolerant) once the generator block lands. This is the correct fail-closed posture: the test exists and is wired (it will activate automatically), but is parked rather than deleted or coupling to absent content. Consistent with the NOTE in the spawn prompt.

---

## Confidence

**Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

Every criterion was checked against source files AND/OR a live test run, not against the summary's self-report. The two highest-risk CRITICAL traps (unanchored regex, scoped-vs-package-wide subprocess grep) were independently reproduced: I re-executed the anchored regexes against `runner.py` and grepped `commands.py` to confirm the tmux `subprocess.run` that justifies the scoping.

**Tool engagement:** Read: 13 | Grep(Bash): 4 | Glob(Bash find/ls): 2 | Bash(pytest+python): 2

No web research performed (all claims source-truth-local).

## QA Complete
