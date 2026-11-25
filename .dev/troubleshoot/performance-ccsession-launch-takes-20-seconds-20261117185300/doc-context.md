# Documentation Context Card

**Generated**: 2026-11-17T18:58:57Z
**Wave**: 1.5
**Scope**: (none)

## Release context

- **Release**: v5.0.0 (current)
- **Artifacts**: /home/coder/workspaces/IronClaude/.dev/releases/current/v5.0.0/post-release/scan/DE2-claude-surface.md, /home/coder/workspaces/IronClaude/.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md
- **Summary**: No PRD, TDD, spec or roadmap in `.dev/releases/` scopes the session list or its speed. The post-release scans only record the CLI contract of `--ask` (list and question on the terminal, exit 1 on timeout, exit 130 on Ctrl+C) and the `ccsession-lists` surface (`--list`, `--here`, `--here --all`, `--rm`, `--ask`). A fix may change how fast the list is built, not that contract.
- **Confidence**: 0.7 (worker did not re-read the files after Grep)

Related repo task records (not release docs): .dev/issues/315/accuracy-check.md (plain `ccsession` never asks; only `--ask` lists on the launch route for Orca and Coder), .dev/tasks/done/TASK-WF-fixIssue389Ironb-20261105-174606/TASK-WF-fixIssue389Ironb-20261105-174606.md line 21 (output of `--ask`, `--auto-name`, `--list`, `--rm` must stay on standard output for shell capture), .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/TASK-WF-fixGitHubIssue31-20261105-031410.md (the `--ask` contract; whether it finished is unverified).

## Architectural docs consulted

- `/home/coder/workspaces/IronClaude/src/superclaude/skills/ccsession-tag/README.md` — verdict: `current` — contract of `--list`, `--here`, `--here --all` and `--ask`; the question gives up after 30 s and Orca fails a supervised worker whose Claude is not ready within 60 s; no speed or CPU expectation is stated for a large list.
- `/home/coder/workspaces/IronClaude/docs/testing/v5.0.0/user/D08-ccsession.md` — verdict: `current` for behaviour statements (its source line numbers do not match the 2072-line script) — manual test script for the same commands.

> CAUTION: the checkout's ccsession (1902 lines) is older than origin/master and the installed copy (2072 lines); line citations in D08 and in older .dev records point at the older script. Only the behaviour statements are usable.

## Restrictions / decisions that constrain the fix

(Full list with verbatim quotes in wave1_5-branch-C.md; installed path I = /home/coder/.claude/skills/ccsession-tag/ccsession.)

- `I:1380` (session_home) — "# Only the start and the end of the file are read (transcripts can be" gigabytes: a fix must not read whole transcripts and must keep both ends.
- `I:1378` (session_home) — "# <transcript> -> the folder the session was started in: the first recorded folder whose name matches the transcript's folder, else the first one."
- `I:1481` (session_transcript) — "# <session id> -> its transcript (the newest copy), or nothing."
- `I:1490` and `I:1516` (get_btime, get_mtime) — GNU `stat -c` first; BSD `stat -f` must never run first on Linux.
- `I:1533` (format_epoch) — BSD `date -r` first, GNU `date -d @` fallback; format `%Y-%m-%d %H:%M`.
- `I:1690` and `I:1823` (ask_session_name, ask_drain_waiting) — bash 3.2 (macOS) compatibility: no `read -t 0`, no fractional `read -t`.
- `I:1733` (ask_session_name) — "Every question gives up after CCSESSION_ASK_TIMEOUT seconds (default 30; 0 waits for ever): Orca fails a supervised worker whose Claude is not ready within 60 seconds"; listing time runs before the question.
- `/home/coder/.claude/skills/ccsession-tag/README.md:190` — "Listing never writes any file." (a cache file written during listing needs a README and rule change).
- README:275 — `last` in the list is each transcript's change time; nothing touches transcript files.
- Output formats pinned by tests (row format, "(transcript missing)", "(times unavailable)", "(was <folder>)", "N more sessions in other worktrees of this repo", first two lines dropped by show_saved): tests/unit/test_ccsession_tag.py `_listed` helper (line 3897) and tests at 4474, 4522, 4551, 4585, 3465, 2740 and others.

## Re-frame signals

- No document sets a speed or CPU target for the session list, so the symptom is not documented behaviour; a code change is not blocked by the docs (`consistency_with_docs` will be `no_docs_found` for the speed claim and `aligned` for the output contract).
- The `--ask` list runs before the 30 s question and counts against Orca's 60 s readiness window (I:1733), so a 20 to 27 s list consumes a third to nearly half of the start window; this is a documented-risk reframe, not a contradiction.
- Constraint for any fix: output text, exit codes (0, 1, 3, 130), the stdout/stderr split, the here/gone/other classification and "Listing never writes any file" (README:190) must stay as they are.
