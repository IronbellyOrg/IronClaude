start=5838ab1093d28376c78ec96eb86ef82f854fcfda
Review one task for spec compliance.

Task brief: Task 2: Name all 59 reason codes in docs/designs/issue-watcher.md

Depends on: Task 1

`REASON_TABLE` in `src/superclaude/cli/issue_watch/audit.py` holds 59 names; `audit.REASONS` is the frozenset of its keys. The design never lists them: section 10.1 says the `reason` key is an "enum (spec reason table)" and that "`audit.REASONS` is a `frozenset` equal to the spec's reason table", and the exit-code table in section 4.3 has no row for exit 1 and does not name `cycle_complete`. The two names the build added are `cycle_complete` (cycle line, exit 0) and `cycle_crashed` (cycle line, exit 1, written by `once` only for an unexpected exception), both marked [PROPOSAL] in `audit.py`. The full 59-name table, grouped by exit code, already exists in section 10.2 of `docs/designs/issue-watcher-setup.md`; the design points at it rather than keeping a second copy.

Make these edits in `docs/designs/issue-watcher.md`:
- Section 10.1, the `reason` row of the audit line table: replace "enum (spec reason table)" with an enum reference to `audit.REASON_TABLE` (59 names).
- Section 10.1, the sentence that begins "`rate_remaining`, titles, bodies": replace "equal to the spec's reason table" with: the 59 keys of `audit.REASON_TABLE`, which are the spec's reason table plus the two [PROPOSAL] names `cycle_complete` and `cycle_crashed` added during the build; the full table, grouped by exit code, is section 10.2 of `issue-watcher-setup.md`. Keep the rest of that sentence (the `ValueError` rule) unchanged.
- Section 4.3: in the exit 0 row, add `cycle_complete` to the "Reasons that produce it" cell; add one row for exit 1 with the meaning "An unexpected exception out of the cycle, written by `once` only ([PROPOSAL])" and the reason `cycle_crashed`, placed between the 0 and 2 rows.

Acceptance criteria:
T2.AC1: `grep -c "cycle_complete" docs/designs/issue-watcher.md` and `grep -c "cycle_crashed" docs/designs/issue-watcher.md` each print at least 2.
T2.AC2: `grep -n "spec reason table\|equal to the spec's reason table" docs/designs/issue-watcher.md` prints nothing.
T2.AC3: The section 4.3 table has a row whose first cell is `1` naming `cycle_crashed`, and its exit 0 row names `cycle_complete`.
T2.AC4: Every reason name in section 4.3 of the design is a key of `REASON_TABLE`: the check (a loop over the backticked names in that table, each tested with `grep -c "\"<name>\":" src/superclaude/cli/issue_watch/audit.py`) and its output are saved to `./artifacts/t2-reason-check.log`, with zero misses.
T2.AC5: The section 10.2 table in `docs/designs/issue-watcher-setup.md` is unchanged (`git diff --stat docs/designs/issue-watcher-setup.md` shows no change from this task).
Global constraints: 
- Agent tasks change only `docs/designs/issue-watcher.md`, `docs/designs/issue-watcher-setup.md` (Tasks 1 to 4) and, in Task 5, the 19 files under `tests/issue_watch/fixtures/_assumed_shape/` and `tests/issue_watch/test_github.py`. No file under `src/` or `.claude/` changes.
- `enabled` stays `false`: the example configuration in section 2 of `docs/designs/issue-watcher-setup.md` (`"enabled": false`) and the default `raw.get("enabled", False)` in `src/superclaude/cli/issue_watch/cycle.py` are not touched by any task.
- No agent runs `gh`, `orca` or `superclaude issue-watch` against real GitHub or Orca, writes to GitHub, launches an Orca agent, takes the lock on a real state directory, edits a crontab or scheduler, commits or pushes. Those are owner-run items (listed below); the plan only writes them down.
- No agent writes `docs/designs/issue-watcher-live-test.md`. The design (section 1, "Deployment gate") and the runbook (section 14.1) say the owner writes and commits it.
- Task 2 adds one row to the exit-code table in section 4.3 of `docs/designs/issue-watcher.md`, which shifts the design line numbers that the fixture `source` fields cite by one. That is accepted: Task 5 rewrites the `source` field of every captured fixture. New text cites sections and table rows by name, never by line number.
- Out of scope: follow-ups FU-3 to FU-12, the owner questions Q1 to Q4 in section 16 of the design, the low regression fix recorded in the build's worker final report, renaming the `_assumed_shape` fixture directory, and any change to the parsers in `src/superclaude/cli/issue_watch/github.py` or `launch.py` (a captured shape that breaks a parser is recorded for a follow-up plan, never patched here).


Start sha: 5838ab1093d28376c78ec96eb86ef82f854fcfda
Diff against the start snapshot: diff --git a/docs/designs/issue-watcher.md b/docs/designs/issue-watcher.md
index acf478e99..c7cde0ed4 100644
--- a/docs/designs/issue-watcher.md
+++ b/docs/designs/issue-watcher.md
@@ -154,7 +154,8 @@ Unknown keys are rejected (exit 2), so a typo such as `enable` cannot silently l
 
 | Code | Meaning | Reasons that produce it |
 |---|---|---|
-| 0 | Cycle complete (any number of launches), `disabled`, `disabled_mid_cycle`, `not_enabled` | `disabled`, `disabled_mid_cycle`, `not_enabled`; every skip reason |
+| 0 | Cycle complete (any number of launches), `disabled`, `disabled_mid_cycle`, `not_enabled` | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled`; every skip reason |
+| 1 | An unexpected exception out of the cycle, written by `once` only ([PROPOSAL]) | `cycle_crashed` |
 | 2 | Usage, config, platform, origin, Orca probe | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch` |
 | 3 | GitHub auth, scope, timeout, non-JSON | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` |
 | 4 | Discovery truncated or duplicated | `truncated`, `discovery_duplicate` |
@@ -706,7 +707,7 @@ One JSON object per line, written with one `os.write` on an `O_WRONLY | O_APPEND
 | `cycle_id` | yes | yes | yes | `uuid4().hex` |
 | `dry_run` | yes | yes | yes | bool |
 | `exit` | yes | no | no | int |
-| `reason` | yes | yes | yes | enum (spec reason table) |
+| `reason` | yes | yes | yes | enum (`audit.REASON_TABLE`, 59 names) |
 | `gh_calls`, `duration_ms` | yes | no | no | int |
 | `issue` | no | yes | optional | int |
 | `state` | no | yes, when an entry was written | no | enum |
@@ -715,7 +716,7 @@ One JSON object per line, written with one `os.write` on an `O_WRONLY | O_APPEND
 | `clock_skew_s` | yes | no | `clock_skew` warning | int |
 | `note` | no | `"re-approved"` when the approval event changed | no | str |
 
-`rate_remaining`, titles, bodies, label names and stderr text are never keys (NFR-006, T11). `audit.REASONS` is a `frozenset` equal to the spec's reason table; `audit.line(...)` raises `ValueError` on any other reason, so a typo fails the first test that hits it.
+`rate_remaining`, titles, bodies, label names and stderr text are never keys (NFR-006, T11). `audit.REASONS` is a `frozenset` of the 59 keys of `audit.REASON_TABLE`, which are the spec's reason table plus the two [PROPOSAL] names `cycle_complete` and `cycle_crashed` added during the build (the full table, grouped by exit code, is in section 10.2 of [issue-watcher-setup.md](issue-watcher-setup.md)); `audit.line(...)` raises `ValueError` on any other reason, so a typo fails the first test that hits it.
 
 Rotation (`AuditLog.rotate_if_needed`, called only with the lock held): if `audit.jsonl` is at least 5 MiB, `os.replace` `.3` to `.4`, `.2` to `.3`, `.1` to `.2`, current to `.1`, then a directory fsync. The exit-75 path appends and never rotates.
 

New evidence file: .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t2-reason-check.log (read current contents).
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
