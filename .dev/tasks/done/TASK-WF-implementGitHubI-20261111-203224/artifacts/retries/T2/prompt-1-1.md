036104cb53a1f9f190105bbdb612c01d8875e262
Review one task for spec compliance.

Task brief: 
## Task 2: Add the numbered coordinator preflight before the first task-create

Depends on: Task 1

In `src/superclaude/core/WORKER-CONTRACT.md`, section 4, replace the single sentence at line 216 ("The coordinator decides whether a `Command:` line carries `--unattended` by the guard's own test ...") and its follow-on sentence with a new subsection heading `### Before the first task-create for a command` directly after the brief-layout text, holding a numbered list. The text must say: the coordinator decides by the two-copy test whether a `Command:` line carries `--unattended`; the test runs once per command per run before the first `task-create` for that command (a Task spec cannot be edited afterwards) and again after any change to a command file, `make sync-dev` or `superclaude install`; the steps read, as plain files, the target worktree's `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md` (a missing copy is skipped), look for a line equal to `## Unattended mode` in each existing copy, then act: every existing copy has it, so the `Command:` line carries `--unattended` and one report directory; the copies disagree, so no Task is created until the stale copy is refreshed; no existing copy has it, so the line carries no flag and the brief says why, and a run of that command that needs a person is a person-in-the-loop run, not a worker. Keep the sentence "A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer."

Acceptance criteria:
- T2.AC1: `grep -n 'Before the first task-create for a command' src/superclaude/core/WORKER-CONTRACT.md` finds exactly one heading, inside section 4 before `## 5.`.
- T2.AC2: The subsection contains the phrase `the coordinator decides by the two-copy test` and the phrase `re-invocation keeps every token`, names both copy paths, and the numbered steps appear in run order.
- T2.AC3: The old line-216 sentence no longer exists as a separate paragraph.

Global constraints: 
## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

Start sha: 036104cb53a1f9f190105bbdb612c01d8875e262
Diff against the start snapshot: 
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 778e113a1..f8e4a8476 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -213,7 +213,17 @@ Chain line, right after the guard line and before the first `Command:` line (C-8
 Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
 ```
 
-The coordinator decides whether a `Command:` line carries `--unattended` by the guard's own test, run on the copies the worker will see (the target worktree's project `.claude/commands/sc/` copy and `~/.claude/commands/sc/`), not on its own copy. A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer.
+Whether a `Command:` line carries `--unattended` is decided by the preflight below. A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer.
+
+### Before the first task-create for a command
+
+Before it creates the first Task for a command, the coordinator decides by the two-copy test whether that command's `Command:` line carries `--unattended` and a report directory. The test is the brief guard's own test, run by the coordinator on the copies the worker will see, never on the coordinator's own copy. It runs once per command per run, before the first `task-create` that names the command (a Task spec cannot be edited afterwards, so a wrong line costs a refused Task and a new one under WC-6), and again after any change to that command's file or to an installed copy (a sync of the development copies, or a new `superclaude install`).
+
+1. Read, as plain files, the target worktree's `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`. A copy that does not exist is skipped.
+2. In each existing copy, look for a line that is exactly `## Unattended mode`.
+3. Every existing copy has the section: the `Command:` line carries `--unattended` and exactly one report directory (section 5).
+4. The existing copies disagree: create no Task for that command until the stale copy is refreshed, normally `~/.claude`, which the person refreshes with `superclaude install`. The worker's guard would refuse the Task as "copies disagree".
+5. No existing copy has the section: the `Command:` line carries no flag, and the brief says so. A run of that command that needs a person at a gate is a person-in-the-loop run, not a worker.
 
 ### Feature worktree and child worktrees
 


Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
