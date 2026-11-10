# Troubleshoot Report

**Target**: `uv run pytest tests/cli/eval/test_ban_import_rule.py` fails 3 tests (test_clean_tree_passes_ruff_check, test_synthetic_import_anthropic_is_flagged_by_ruff, test_ban_message_references_fr_g1); find the root cause
**Type**: test
**Tier reached**: 2
**Confidence**: 0.50
**Status**: partial
**Escalation reason**: low_confidence
**Test is wrong**: false
**Behavior is documented**: false
**Doc context card**: .dev/p0-live/troubleshoot/doc-context.md
**Duration**: 2647
**Date**: 2026-11-04T06:47:34Z

---

## Summary

Status is partial only because the evidence validator dropped one citation for a wrong line locator (re-cited below to the line that holds the quote); the diagnosis itself is backed by a two-arm experiment. The three tests fail because ruff is not installed in the project environment, not because of a lint regression or a broken FR-G1 rule. ruff is declared only in the optional `dev` extra, a plain `uv run` never installs extras, so in a fresh worktree the test's `uv run ruff check` subprocess cannot start and exits 2 with "Failed to spawn: `ruff`"; with ruff supplied the same tests pass. The chosen fix is to provision with `make install` now and, separately, add a fail-fast guard so a missing tool is reported as a setup error instead of a lint failure.

## Documentation Context

- **Relevant refs**: CLAUDE.md, Makefile, pyproject.toml, docs/getting-started/installation.md, docs/developer-guide/contributing-code.md, PROJECT_INDEX.md, KNOWLEDGE.md, docs/user-guide/eval-pipeline.md (no release artifact found)
- **Documented behavior**: the documented setup is `uv venv` then `make install` (`uv pip install -e ".[dev]"`, "ruff included"); tests are then run with `uv run pytest`.
- **Restrictions honored**: UV-only operations (CLAUDE.md:7); keep the subprocess `uv run ruff` design and no `--select` (tests/cli/eval/test_ban_import_rule.py:19-23, :44); keep the exact ruff pin (pyproject.toml:50-54).
- **Restrictions overridden**: None
- **Card path**: .dev/p0-live/troubleshoot/doc-context.md

## Diagnosability Context

**Verdict**: sufficient
**Complexity classification**: trivial
**Captured-bytes (failing run)**: n/a

Existing signal: three pytest assertion messages print the subprocess stdout and stderr verbatim (the one at tests/cli/eval/test_ban_import_rule.py:88 also prints the return code).
Gap: none for this symptom; the `returncode != 0` check at tests/cli/eval/test_ban_import_rule.py:120 cannot tell "tool missing" from "rule fired".
Implication: the decisive datum was observed directly, so no instrumentation round was needed (rubric row S1).

(Full card: /home/coder/workspaces/worktrees/IronClaude/p0-live-troubleshoot/.dev/p0-live/troubleshoot/diagnosability-context.md)

## Diagnosis

**Root cause**: The project `.venv` that `uv run` creates contains no ruff, because ruff is declared only in the optional `dev` extra of pyproject.toml and `uv run` does not install extras; the test helper's `uv run ruff` subprocess therefore fails to start (exit 2), and all three tests receive uv's spawn error instead of ruff output.

**Cause class**: Build / packaging (install step missing)

**Detailed explanation**: All three tests call one helper, `_run_ruff` (Evidence 2), which launches `uv run ruff check --no-cache src/superclaude/cli/eval/`. In a fresh worktree the first `uv run pytest` builds `.venv` without ruff (Evidence 4; the installed package list has no ruff, mypy or pytest-cov, `.dev/p0-live/troubleshoot/capture-env.txt:4-33`). ruff sits in the `dev` extra (Evidence 1), which uv does not sync by default (Evidence 7). The nested `uv run` finds no ruff in the venv or on PATH and exits 2 (Evidence 3, 5). Test 1 fails its `returncode == 0` check; test 2 passes its `returncode != 0` check on the spawn error and then fails on the missing `TID251` text (Evidence 9); test 3 fails on the missing `FR-G1` text. Supplying ruff 0.15.20 with no other change makes all three pass (Evidence 6), which rules out a lint regression and a broken banned-api configuration. CI is unaffected because every CI job installs `.[dev]` first (Evidence 11). The same failure is already recorded in an earlier fresh worktree (Evidence 13), and a sibling test file fails for the same reason (Evidence 10).

## Evidence

1. `pyproject.toml:45-46` — `[project.optional-dependencies]` / `dev = [`; `pyproject.toml:54` — `"ruff==0.15.20",` (the runtime `dependencies` list at pyproject.toml:34-43 has no ruff)
2. `tests/cli/eval/test_ban_import_rule.py:50` — `["uv", "run", "ruff", "check", "--no-cache", str(target)],` (inside `_run_ruff`, called by all three tests: `.dev/p0-live/troubleshoot/tier1-callers.md:9-11`)
3. Command: `uv run pytest tests/cli/eval/test_ban_import_rule.py -q -p no:cacheprovider` → `.dev/p0-live/troubleshoot/capture-failing-run.txt:19-20` `error: Failed to spawn: \`ruff\`` / `Caused by: No such file or directory (os error 2)`; `capture-failing-run.txt:44` `3 failed`; `:45` `exit=1`
4. `.dev/p0-live/troubleshoot/capture-env.txt:1-2` — `venv_ruff: absent` / `path_ruff: none`
5. Command: `uv run ruff --version` → `.dev/p0-live/troubleshoot/capture-ruff-version-probe.txt:1-3` — `error: Failed to spawn: \`ruff\``, `exit=2`
6. Command: `uv run --with ruff==0.15.20 pytest tests/cli/eval/test_ban_import_rule.py -q -p no:cacheprovider` → `.dev/p0-live/troubleshoot/capture-ruff-overlay-run.txt:11-12` — `3 passed`, `exit=0`
7. `.dev/p0-live/troubleshoot/tier1-observation.md:53` — "uv does not sync extras by default. Use the `--extra` option to include an extra." (quoted from uv 0.11.0 docs, concepts/projects/sync.md; recorded as row 1 at `.dev/p0-live/troubleshoot/behaviour-definitions.md:5`, Status `fetched:context7 /astral-sh/uv/0.11.0`)
8. `Makefile:7` — `uv pip install -e ".[dev]"`; `CLAUDE.md:140` — `make install          # Install editable + dev dependencies (ruff included)`
9. `tests/cli/eval/test_ban_import_rule.py:120` — `assert result.returncode != 0, (` passes on the spawn error; the test then fails at `tests/cli/eval/test_ban_import_rule.py:125` — `assert "TID251" in combined, ...` (capture-failing-run.txt:31)
10. `tests/cli/eval/test_claude_process_adapter.py:453` — `assert result.returncode != 0, (`; command `uv run pytest tests/cli/eval/test_claude_process_adapter.py -k ruff -q -p no:cacheprovider` → `.dev/p0-live/troubleshoot/capture-sibling-adapter-ruff.txt:27` `2 failed, 11 deselected`, with stderr `No module named ruff` (capture-sibling-adapter-ruff.txt:21)
11. `.github/workflows/test.yml:27` — `uv pip install -e ".[dev]"` (also at :65, :91, :167) before pytest runs
12. `uv.lock:1563-1564` — `name = "ruff"` / `version = "0.15.20"`
13. `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-baseline-wider.txt:204` — the identical `error: Failed to spawn: \`ruff\`` in an earlier fresh worktree

## Proposed Fix

Chosen by the adversarial debate (base: the fail-fast guard proposal, combined score 0.857; merged proposal at .dev/p0-live/troubleshoot/adversarial/merged-output.md; self-review PASS with 7 minor notes).

1. Immediate, no file change: in the worktree, run `uv venv` (if needed) then `make install`, then re-run the tests.
2. Code change (two test files, so it needs a written plan under the CLAUDE.md hard limit):
   - In `tests/cli/eval/test_ban_import_rule.py`, define the ruff command prefix once (`("uv", "run", "ruff")`); `_run_ruff` builds `prefix + check --no-cache <target>` (effective command unchanged) and a module-scoped autouse guard runs `prefix + --version`; on non-zero it calls `pytest.fail(..., pytrace=False)` with a "ruff could not be started via `uv run`; run `make install`" message plus stderr. Fail, never skip, so a CI install regression cannot hide the FR-G1 check.
   - In `tests/cli/eval/test_claude_process_adapter.py`, give the two ruff tests their own guard that probes the same command they run (`sys.executable -m ruff --version`), requested only by those two tests.

**Files to change**:
- `tests/cli/eval/test_ban_import_rule.py` — single command-prefix source plus fail-fast guard fixture
- `tests/cli/eval/test_claude_process_adapter.py` — guard fixture for the two ruff tests

**Test to verify**:
- Failing arm (fresh `.venv`, no `make install`): the 3 ban-rule tests and the 2 adapter ruff tests error at setup with the "run `make install`" message; no lint-assertion failures; the other 11 adapter tests unaffected.
- Control arm: `uv run --with ruff==0.15.20 pytest tests/cli/eval/test_ban_import_rule.py -q -p no:cacheprovider` → 3 passed.
- Provisioned arm: fresh worktree, `uv venv && make install`, confirm `.venv/bin/ruff` exists, then `uv run pytest tests/cli/eval/test_ban_import_rule.py tests/cli/eval/test_claude_process_adapter.py -q -p no:cacheprovider` → all pass.

**Apply with**: `/sc:troubleshoot --fix ...` (Tier 3 plan chain via `sc:workflow` → `sc:implement`), or `/sc:workflow` with the merged proposal as input, or apply manually.

## Alternative Fixes Considered

- **Fix 1 — `make install` only, no file change** (from root-cause-analyst, combined 0.748)
  - Rejected as the sole fix because the failure recurs in every new worktree and is still misreported as a lint regression; kept as step 1 of the chosen fix.
- **Fix 3 — default `[dependency-groups] dev = ["superclaude[dev]"]` plus a regenerated uv.lock** (from refactoring-expert, combined 0.758)
  - Rejected because its core mechanism (a group referencing the project's own extra) is unverified, it may change the `make verify-deps` environment, and it changes packaging for every contributor.
- **Fix 4 — `uv run --extra dev ruff` inside `_run_ruff`** (from Tier 1 root-cause-analyst, combined 0.666)
  - Rejected because the test would install packages into the running `.venv` mid-session and make the sibling `sys.executable -m ruff` tests depend on test order.

## Risk + Rollback

- **Likelihood of regression**: low, in tests/cli/eval only (test-side guards; no production code change)
- **Test coverage of the changed code**: partial — the guard's failing and passing arms are specified but not yet run; the provisioned arm has not been captured on uv 0.11.8
- **Rollback**: revert the two test-file edits with `git revert`; `make install` needs no rollback
- Watch: a guard scoped too widely would fail the 11 non-ruff adapter tests; the guard message names the most common cause, so read the appended stderr when it fires for another reason (lock or sync failure, a different `UV_PROJECT_ENVIRONMENT`).

## Follow-up tasks

- Make Orca worktree setup run `make install` alongside `make sync-dev` so new worktrees are provisioned (owner of that setup step: UNVERIFIED). `Suggested type`: observability
- Address the self-review notes before planning: environment-identity wording (F1, F2), guard message wording (F3), reconcile the `sys.executable -m ruff` probe with CLAUDE.md:7 (F4), a baseline for the 11 non-ruff adapter tests (F5), one shared prefix for both adapter ruff commands (F6), full control-arm command and a capture of the sibling probe failing (F7). Evidence: .dev/p0-live/troubleshoot/self-review.md. `Suggested type`: test
- Optionally evaluate the default dependency-group change (Fix 3) as its own decision, after verifying that uv accepts `superclaude[dev]` in `[dependency-groups]` and that `make verify-deps` still passes. `Suggested type`: refactor

## Grounding Gaps

- Evidence validation dropped one citation (Evidence 7 originally pointed at behaviour-definitions.md:5 for a verbatim quote that lives at tier1-observation.md:53); it is re-cited to the line the validator identified, and the drop contributes `partial` to the status. Evidence 4 was tightened with the package-list lines the validator pointed to.
- MCP `auggie` was unavailable in this session and to every worker; grounding used codegraph, Grep, Glob and Read, and all Wave 1.5 and Wave 1.6 branches ran degraded.
- Documentation currency verdicts rest on checkout-time file mtimes (every file 2026-11-04T06:02:05Z), which carry little signal; the FR-G1 design spec cited by docs/user-guide/eval-pipeline.md is not present in this worktree.
- Calibration disagreement, unresolved: structural rule C7 capped three cards at 0.50 for naming an environment property without a 2x2 row, while the root-cause-analyst card was judged outside C7 and scored 0.92. Both values are kept as returned; the reported confidence uses the conservative 0.50. Uncapped scores were 0.83 to 0.92.
- The chosen fix was not executed in this run (diagnosis only; installs belong to the coordinator). The ruff overlay proves that ruff's presence flips the result, not that `make install` delivers ruff to the nested `uv run`; the provisioned arm is still to be captured.
- `uv run` keeping already installed extras (inexact sync) is documented for uv 0.11.0 and not captured on the local uv 0.11.8.
- The adversarial debate ran at quick depth and did not converge (24 of 33 points, 73% against an 80% threshold); the base was selected by score. One advocate omitted a position on one shared assumption (A-005).
- capture-env.txt does not record `VIRTUAL_ENV` or `UV_PROJECT_ENVIRONMENT`.

## Next Steps

- Coordinator: in this worktree run `make install`, then `uv run pytest tests/cli/eval/test_ban_import_rule.py tests/cli/eval/test_claude_process_adapter.py -q -p no:cacheprovider`; expect all to pass. This is the outstanding positive witness.
- Tier 2 without `--fix`: "Re-run with `--fix` added to your previous invocation to enter the remediation chain." The code change touches two files, so it goes through a written plan (`/sc:workflow` then `/sc:implement`).

## Audit

- **Hypothesis cards**: .dev/p0-live/troubleshoot/tier1-hypothesis.md, .dev/p0-live/troubleshoot/tier2-quality-engineer-hypothesis.md, .dev/p0-live/troubleshoot/tier2-root-cause-analyst-hypothesis.md, .dev/p0-live/troubleshoot/tier2-refactoring-expert-hypothesis.md
- **Adversarial artifacts** (Tier 2 only): merged proposal .dev/p0-live/troubleshoot/adversarial/merged-output.md; debate files in .dev/p0-live/troubleshoot/adversarial/adversarial/ (diff-analysis.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml with status partial: debate not converged)
- **Self-review** (Tier 2 only): OK (raw verdict PASS, 0 blocking, 7 minor) — .dev/p0-live/troubleshoot/self-review.md
- **Evidence validation**: .dev/p0-live/troubleshoot/evidence-validation.md
- **Audit log**: .dev/p0-live/troubleshoot/audit.log

## Pipeline Hardening Closure

**Applicable**: true
**Closure verdict**: advisory
**Waiver status**: latched
**Backtest status**: not_run
**Off-path review**: waived_with_rationale

**Wave statuses**:

- **HC0 Applicability + Boundary Scan**: PASS — CLI/subprocess boundary: a launcher spawn failure can satisfy the `returncode != 0` oracle (tests/cli/eval/test_ban_import_rule.py:120)
- **HC1 Runtime-Entrypoint Verification**: PASS — real spawn replayed through the reported command; negative witness = unprovisioned run (3 failed), positive witness = ruff overlay (3 passed), accepted substitute because no fix was applied
- **HC2 Contract Enumeration**: PASS — 10-row ledger: producers (pyproject extra, Makefile, CI installs), consumers (both FR-G1 test files, Makefile lint/format, CI lint job), pre-commit hook excluded with proof
- **HC3 Unmask + Sweep**: N/A — no generated-artifact classifier in the path; same-shape sweep still recorded (2 of 2 `returncode != 0` sites observed)
- **HC4 Effective-Input Proof**: N/A — no review or audit gate consumes an indirect selector here
- **HC5 Off-Path Reviewer + Waiver**: N/A — waived with rationale: a diagnosis-only run produces no change to review; the obligation moves to the remediation change

**Evidence cards**:

- Runtime-entrypoint card: /home/coder/workspaces/worktrees/IronClaude/p0-live-troubleshoot/.dev/p0-live/troubleshoot/hardening/runtime-entrypoint-card.md
- Contract ledger: /home/coder/workspaces/worktrees/IronClaude/p0-live-troubleshoot/.dev/p0-live/troubleshoot/hardening/contract-ledger.md
- Unmask/sweep card: /home/coder/workspaces/worktrees/IronClaude/p0-live-troubleshoot/.dev/p0-live/troubleshoot/hardening/unmask-sweep-card.md
- Effective-input card: /home/coder/workspaces/worktrees/IronClaude/p0-live-troubleshoot/.dev/p0-live/troubleshoot/hardening/effective-input-card.md

**Known escapes caught**: None claimed

**Closure blockers**:

- ADVISORY — closure relies on waived/substituted proof
