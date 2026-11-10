start=f5165be3b72cf7c71590073342a69e3244f27855
Review one task for spec compliance.

Task brief: Task 1: Replace the stale status line in docs/designs/issue-watcher.md

In `docs/designs/issue-watcher.md`, line 3 reads "**Status:** Design only, nothing implemented. Next: `/task-builder` with `--spec` on this file, then `/task`." The watcher was built and merged in PRs #447 and #448 (`src/superclaude/cli/issue_watch/`, `tests/issue_watch/`). Rewrite that one line, in place, so it states: implemented and merged in PRs #447 and #448, never run live, `enabled` ships as `false`, no schedule is installed, and the next step is the owner-run live test (FU-1) in section 14.1 of `docs/designs/issue-watcher-setup.md`. Then search the whole file for any other sentence that says the watcher is not implemented or is design only, and correct each hit the same way. The "built and tested with mocks only" wording of the section 1 scope table is true and stays.

Acceptance criteria:
T1.AC1: `grep -n "nothing implemented" docs/designs/issue-watcher.md` prints nothing.
T1.AC2: Line 3 names PRs #447 and #448, says the watcher has never run live, says `enabled` is `false` and nothing is scheduled, and points at FU-1 and section 14.1 of `docs/designs/issue-watcher-setup.md`; it no longer names `/task-builder` or `/task`.
T1.AC3: The output of `grep -n -i -E "not implemented|design only|not yet built" docs/designs/issue-watcher.md` is saved to `./artifacts/t1-status-search.log`, and every hit is either corrected or noted in that log as being about something else.
T1.AC4: The file still has the same number of lines as before the task (the status line is replaced in place).
Global constraints: 
- Agent tasks change only `docs/designs/issue-watcher.md`, `docs/designs/issue-watcher-setup.md` (Tasks 1 to 4) and, in Task 5, the 19 files under `tests/issue_watch/fixtures/_assumed_shape/` and `tests/issue_watch/test_github.py`. No file under `src/` or `.claude/` changes.
- `enabled` stays `false`: the example configuration in section 2 of `docs/designs/issue-watcher-setup.md` (`"enabled": false`) and the default `raw.get("enabled", False)` in `src/superclaude/cli/issue_watch/cycle.py` are not touched by any task.
- No agent runs `gh`, `orca` or `superclaude issue-watch` against real GitHub or Orca, writes to GitHub, launches an Orca agent, takes the lock on a real state directory, edits a crontab or scheduler, commits or pushes. Those are owner-run items (listed below); the plan only writes them down.
- No agent writes `docs/designs/issue-watcher-live-test.md`. The design (section 1, "Deployment gate") and the runbook (section 14.1) say the owner writes and commits it.
- Task 2 adds one row to the exit-code table in section 4.3 of `docs/designs/issue-watcher.md`, which shifts the design line numbers that the fixture `source` fields cite by one. That is accepted: Task 5 rewrites the `source` field of every captured fixture. New text cites sections and table rows by name, never by line number.
- Out of scope: follow-ups FU-3 to FU-12, the owner questions Q1 to Q4 in section 16 of the design, the low regression fix recorded in the build's worker final report, renaming the `_assumed_shape` fixture directory, and any change to the parsers in `src/superclaude/cli/issue_watch/github.py` or `launch.py` (a captured shape that breaks a parser is recorded for a follow-up plan, never patched here).


Start sha: f5165be3b72cf7c71590073342a69e3244f27855
Diff against the start snapshot: diff --git a/docs/designs/issue-watcher.md b/docs/designs/issue-watcher.md
index c22d42b52..acf478e99 100644
--- a/docs/designs/issue-watcher.md
+++ b/docs/designs/issue-watcher.md
@@ -1,6 +1,6 @@
 # Design: `superclaude issue-watch` GitHub issue watcher
 
-**Status:** Design only, nothing implemented. Next: `/task-builder` with `--spec` on this file, then `/task`.
+**Status:** Implemented and merged in PRs #447 and #448; never run live; `enabled` ships as `false`; no schedule is installed. Next: the owner-run live test (FU-1), section 14.1 of [issue-watcher-setup.md](issue-watcher-setup.md) (`docs/designs/issue-watcher-setup.md`).
 **Issue:** IronbellyOrg/IronClaude #331
 **Branch:** `ironbelly/issue-331-github-issue-watcher`
 **Source of truth:** `src/superclaude/` -> `make sync-dev` -> `.claude/` (never stage `.claude/`).

Full new evidence file: .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/artifacts/t1-status-search.log (read current contents).
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
