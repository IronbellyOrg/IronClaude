---
title: Fix of blocking finding B1 (dual-surface rubric lookup in the /sc:issue workers)
task_id: task_9d63cca8bf77
dispatch_id: ctx_ac64ef18623c
branch: ironbelly/feat-sc-issue-command
base_commit: 119622e3
date: 2026-11-04
role: fix worker (B1 only; minor notes m1 to m7 not applied)
status: fixed (all acceptance items hold)
---

# Fix report: B1 (issue #302)

Structure follows the task brief's OBSERVABLE ACCEPTANCE list (no registered template exists for this report type). Source finding: `.dev/tasks/issue-302-handoff/verify/04-verification-report.md` section 5, B1.

## 1. Diff summary

The three files are untracked (the /sc:issue implementation is uncommitted), so there is no `git diff`; the changes are:

| File | Change |
|---|---|
| `src/superclaude/agents/issue-worker-t1.md:17` | "the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md`," became "the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md` (the in-checkout copy is the project `.claude/skills/sc-issue-protocol/refs/claim.md`; read the installed copy first),". Same form as line 27 (templates). |
| `src/superclaude/agents/issue-worker-t2.md:17` | Identical change. |
| `tests/skills/test_issue_worker_agents.py` | New helper `skills_lookups_missing_project_copy(text)`: returns every line that contains `~/.claude/skills/` but no project `.claude/skills/` (regex `(?<!~/)\.claude/skills/`), skipping the provenance line. New tests: `test_every_skills_lookup_names_both_copies` (all three workers, real files), `test_skills_lookup_check_fails_on_old_rubric_line` (t1 and t2, negative case on a `tmp_path` copy), `test_skills_lookup_helper` (4 unit cases for the helper, including the exemption and a `~/.claude/commands/` line that is out of the check's scope). 9 new test cases in total. |

`make sync-dev` copied the two agent files to `.claude/agents/` (byte-identical, checked with `cmp`). Nothing under `.claude/` was staged.

## 2. Line-11 choice

**Exempted in the test, agent text unchanged.** Line 11 of each worker ("Spawned only by the `sc:issue-protocol` skill (`~/.claude/skills/sc-issue-protocol/SKILL.md`) ...") says who spawns the worker; it does not tell the worker to read anything. The test skips lines starting with "Spawned only by the `sc:issue-protocol` skill" (constant `_PROVENANCE_PREFIX`, with a comment explaining why), and a helper unit case pins that the exemption holds. Exempting kept the agent-file edits to the one B1 line each, as the "fix B1 only" constraint asks; t3 needed no edit.

## 3. Proof that the new test fails on the old text

Two independent proofs; the real agent files were never edited back.

1. **Run against the real unfixed files.** The test was added before the agent files were fixed and run once (`fix-1/pre-fix-new-test.log`, `EXIT_CODE=1`): `test_every_skills_lookup_names_both_copies[issue-worker-t1]` and `[issue-worker-t2]` FAILED, each reporting exactly the old line 17 (the "1. **Accuracy check and summary ..." line ending "using the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md`, and links ..."); `[issue-worker-t3]` PASSED. (The two negative-case tests also failed in that run, as expected, because the fixed text they revert did not exist yet.)
2. **Permanent negative case in the suite.** `test_skills_lookup_check_fails_on_old_rubric_line[t1|t2]` reads the fixed file, asserts the new rubric text occurs exactly once, writes a copy to pytest's `tmp_path` with the new text replaced by the old line-17 text, and asserts the helper flags exactly one line, the accuracy-check line, containing the old rubric text. It passes in `fix-1/targeted.log` and `fix-1/full-pytest.log`, so the check is shown to catch the old text on every run.

## 4. Suite, lint and sync results

All logs are in `.dev/tasks/issue-302-handoff/fix-1/` and end with an `EXIT_CODE=` line.

| Step | Log | Result |
|---|---|---|
| `make sync-dev` | `sync-dev.log` | exit 0 |
| `make verify-sync` | `verify-sync.log` | exit 0, "All components in sync." |
| `uv run pytest tests/skills/test_issue_worker_agents.py tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py -v` | `targeted.log` | exit 0, 110 passed |
| `uv run pytest` (full) | `full-pytest.log` | exit 0, 14839 passed, 136 skipped, 2 xpassed, 0 failed |
| `make lint` | `lint.log` | exit 0, "All checks passed!" |

The verification run before this fix had 14830 passed (`verify/full-pytest.log`); the difference is exactly the 9 new test cases.

## 5. Out of scope (not touched)

Minor notes m1 to m7 of the verification report were not applied. No other file was edited. No commit, push or `gh` write; only `git add .dev/tasks` was run.
