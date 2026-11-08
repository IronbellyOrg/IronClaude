# QA Report — Research Gate (Gap Detection Lens)

**Topic:** GitHub issue watcher MDTM task build (TASK-RF-issue-watcher-20261107-150955)
**Date:** 2026-11-07
**Phase:** research-gate
**Lens:** gap-detection
**Fix cycle:** N/A (fix_authorization: false, report only)

---

## Overall Verdict: FAIL (5 IMPORTANT, 0 CRITICAL, 5 MINOR)

## Coverage checked

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every design section 11 file has research | PASS | 01 F8 (9 modules + main.py), 05 sections 1.0 to 1.9, 05 section 4 (runbook), 05 section 3 (stubs, fixtures) |
| 2 | Every section 12 test has research | PASS | 05 sections 2.1/2.2 list all 19 test files; 03 section 7 gives recipes for the cross-cutting ones |
| 3 | Every section 13 gate has research | PASS with defects | 03 section 6 covers all 7; the 05 final gate list is not executable as written (I5) |
| 4 | Every section 17 AC (AC-1..AC-25) mapped | PASS | 03 section 8 and 05 section 5 both map all 25 (inferred; the design has no AC-to-file table) |
| 5 | Design citations still hold | PASS | I re-read main.py 559-565, install_user_setup.py:35 and :198, swarm/atomic.py:14: all match 01/02 |
| 6 | Reason count 52 incl. `re-approved` | PASS | I counted spec-final.md:334-358 = 52 |
| 7 | Integration points (worktree/cwd, config read, audit path) | FAIL | I4 (config path), M3 (audit path); cwd is carried as 05 G-01 |
| 8 | Verification of lint-architecture, verify-deps, verify-sync, pollution fixture | PASS | 01 F6, 03 sections 4 and 6 |
| 9 | Verification of shellcheck, check-json, detect-secrets, markdownlint on new non-Python files | FAIL (minor) | M1 |
| 10 | Every design-vs-spec conflict reaches one place with a recommended resolution | FAIL | I1, I2 |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I1 | IMPORTANT | 02 section G (G1 to G15), 05 section 5.1 and Gaps (G-01..G-21), 03 Gaps, 04 Gaps | There is no merged decision register. Overlapping items carry different ids (02 G1 = 05 G-01, 02 G2 = 05 G-08, 02 G6 = 05 X8), and 02 G3, G4, G5, G12 to G15 appear only in 02. Four items have NO recommended default. (a) 02 G3: a failed or incomplete G4 marker read or G5 edit-timestamp read has no reason in the closed enum. The spec reason table (spec-final.md:332-358) has none, and the spec failure table (:379) says the issue is "skipped with a reason". 02 offers either/or and says "flag as owner question", but no owner is present during execution, and 05's gap list omits it entirely. (b) 05 G-04: the `reset` audit line has no reason ("a reason from the table, or add reasons"; no table reason fits). (c) 05 G-19: `reset N` on a missing entry ("propose"). (d) 03 vs AC-23: AC-23 and design section 13 require `make test`, but 03 says the full run is too big for an agent turn "without an owner decision". `make test` also runs tests/cli/test_verify_sync_hooks.py, which mutates real src hook files (docstring lines 7-15). 05's gate 4 leaves sizing "for research 03", and 03 does not size it. | Add one consolidated "Decisions" list to research-notes or 05, with one chosen default and a reason for each. Suggested defaults: (a) map marker and edit read failures onto `events_unreadable`/`events_incomplete`, or add `marker_unreadable` and `edits_unreadable` to REASONS and to the spec-table pin test, and record the choice as a Deviation in the Task Log; (b) a decision-kind line with `note: "reset"` and a named existing reason; (c) exit 2, no audit; (d) run `uv run pytest tests/ --ignore=tests/cli/test_verify_sync_hooks.py` after `make sync-dev`, and record the deviation from literal `make test`. |
| I2 | IMPORTANT | 05 sections 1.8 and 1.9 and P8 checkpoint vs 01 F2 | 05 requires `issue-watch --help` to "list six verbs" and a `test_cli.py` assertion that "help lists six verbs". 01 F2 shows the design's six table rows are five distinct Click commands (`reset` is one command with an optional `N` and two flags). A builder following 05 writes an unsatisfiable assertion or invents a sixth command. This contradiction is not in 05's gap list. | Change 05 to "five commands (`once`, `status`, `check-config`, `init-state`, `reset`); six usage forms" and assert the five names in `--help`. |
| I3 | IMPORTANT | 04 Gaps (`{BASE}`), 05 P10, research-notes line 26 | The skill-mode POST reflect item is verbatim `--diff {BASE}..HEAD` (task-builder SKILL.md:2223, "do not paraphrase"). The task has no commit step (research-notes line 26; project rule: commit only when asked). All new files are untracked or staged and uncommitted, so `BASE..HEAD` is an empty diff and reflect audits nothing. 04 only says "choose a base ref, e.g. origin/master"; that does not fix it. The CLI arm stages with `git add -A` first (SKILL.md:2237), and sc-reflect-protocol/refs/remediation-handoff.md:103 says a single ref (not `A..B`) diffs the working tree while `git diff` omits untracked files. | Record the decision. Either stage all artifacts and use a single-ref working-tree `--diff <BASE>` with `--task-log` (a deviation from the verbatim prompt), or add an owner-approved commit step before the POST item. Do not leave `{BASE}` to builder guesswork. |
| I4 | IMPORTANT | 01 F2 (`--config` option), design 4.1 line 110 | The default `--config` is `~/.config/superclaude/issue-watch.json`. Click's `Path` type does not expand `~`, and `grep expanduser` over the research dir and the design returns nothing. A literal `~` path gives `config_invalid` on every default invocation. 05 says tests monkeypatch HOME but pass explicit `--config`, so the bug would slip through. The same gap applies to "Absolute after expansion" for `state_dir`. | Add to 01 F2 and 05 M7/M8: `.expanduser()` on the default and on `--config`, a stated rule for `~` in config values, and a `test_cli.py` case that runs a verb with no `--config` under a monkeypatched HOME. |
| I5 | IMPORTANT | 05 section 6 final gates 3 and 4 vs 03 section 6 and 02 section A | 05 gate 3 is bare `uv run ruff format --check src/ tests/`. I confirmed `uv run ruff --version` prints 0.17.3 (/usr/local/bin/ruff, no .venv ruff), not the pinned 0.15.20. 03 measured "12 files would be reformatted" (all Markdown) and gives the working form `uvx --offline ruff@0.15.20 format --check src/ tests/`. 05 gate 4 adds `pytest -n auto`, but xdist is not installed locally (02 A, 03 section 1). The fix lives in 03 and 02, but 05, which the builder takes the gate list from, was not updated. An executor would hit a false gate failure and might reformat 12 unrelated files. | Make 05's gate list use the 03 commands, name `uv run --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/` (untested, say so), and put `make sync-dev` before `make verify-sync`. |
| M1 | MINOR | 01 F6, 05 P8/P9/P10 | Pre-commit-only hooks (shellcheck --severity=warning on `stubs/gh` and `stubs/orca`, check-json on fixtures, detect-secrets on `PVT_...` strings, markdownlint on the runbook) are flagged in 01 but no phase step verifies them. I confirmed shellcheck, pre-commit, detect-secrets and markdownlint are all absent here. The stub choice (committed with exec bit, per design; or written at runtime into tmp_path, per 03's recommendation) is split across 01, 03 and 05. | Add an optional verification step (`uvx` shellcheck-py, `python -m json.tool` on fixtures) and pick the stub approach in the decision list. |
| M2 | MINOR | 03 / 05 | Repo-wide scans were not identified. tests/skills/test_model_alias_policy.py:140 walks `SRC.rglob("*.py")` for string constants matching `^claude-(opus\|sonnet\|haiku\|fable)-\d`, and :102-117 forbids the text `claude-gw-tier` under `src/superclaude/cli`. tests/docs/test_retired_docs_absent.py:40 scans every `docs/**/*.md` for retired doc paths. Low risk (ORCA_AGENT is the plain agent id), but the runbook and constants should avoid those strings. | One line in the Key constraints. |
| M3 | MINOR | 05 section 1.3 | `AuditLog` constructor and file path (`state_dir/audit.jsonl`, `.1` to `.4`; design 7.1 line 399) are not stated in 05. | Add to M3 text. |
| M4 | MINOR | 05 section 2 | Test list omits: unparseable `dry-run.json` replaced with a warning (design 7.2 line 449), the `clock_skew` warning above 60 s, the `discovery_count` warning at 80, and `/proc/self/mountinfo` octal-escape parsing. | Add cases to `test_cycle.py`. |
| M5 | MINOR | research-notes, 02 G10 | `docs/designs/issue-watcher.md` and the brainstorm directory are untracked (`git status`: `??`). The task must not claim to modify the design and must not read `.dev/` paths in tests. 02 and 05 say the latter; the former is not stated. | One line in the Key constraints. |

## Summary
- Checks passed: 7 / 10 (checks 7, 9, 10 failed)
- Critical issues: 0; blocking (IMPORTANT): 5; minor: 5
- Coverage is thorough. The gaps are in decision-making, not file coverage: the research hands the builder several unresolved conflicts spread over four files.
- Not read: design sections 1 to 3 (lines 1-99); the conclusions about C-rows rely on 02's table plus my spot checks.

## Confidence
Verified: 9/10 | Unverifiable: 0 | Unchecked: 1 (design lines 1-99) | Confidence: 90.0%
Tool engagement: Read: 14 | Grep: 14 | Glob: 1 | Bash: 5

## Recommendations
- Resolve I1 to I5 in research-notes or 05 (a single Decisions list), then re-run the gate.

## QA Complete

VERDICT: FAIL

