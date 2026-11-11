98a3123b8cf701e2714c03b48156f8cf9dffd9d9
Review one task for spec compliance.

Task brief: 
## Task 6: Replace the stale rollout state in the developer guide

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, under "#### Rollout state" (lines 983-987), replace the first two bullets (the P0 statement that no command accepts `--unattended` and that `UNATTENDED_COMMANDS` is empty, and the "Per the rollout plan ... from P1 on" bullet) with current text: all 31 converted commands have an `## Unattended mode` section (16 from phase 1, 15 from phase 2) and `UNATTENDED_EXPECT` in `tests/skills/test_worker_contract.py` holds exactly those 31 entries; coordinators put `--unattended` on the 16 phase 1 commands by default and the phase 2 commands join that default after a phase 2 live check; the coordinator decides by the two-copy test in `~/.claude/WORKER-CONTRACT.md` before the first task-create. Keep the third bullet (SA-1, without `--unattended` every command behaves as today) unchanged.

Acceptance criteria:
- T6.AC1: `grep -n 'At P0' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints nothing.
- T6.AC2: The Rollout state section states 31 commands, 16 plus 15, and keeps the SA-1 bullet word for word.

Global constraints: 
## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

Start sha: 98a3123b8cf701e2714c03b48156f8cf9dffd9d9
Diff against the start snapshot: 
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 0b4d3ec28..0e86725c3 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -982,8 +982,8 @@ Orca can run IronClaude commands as workers under an Orca coordinator (the `/orc
 
 #### Rollout state
 
-- At P0 no command accepts `--unattended` or `--report-dir`, and `UNATTENDED_COMMANDS` in `tests/skills/test_worker_contract.py` is empty.
-- Per the rollout plan, a command gains `--unattended` and its `## Unattended mode` section in the phase that converts its gates, from P1 on, so no command accepts the flag while it can still stop for a human.
+- All 31 converted commands have an `## Unattended mode` section (16 from phase 1, 15 from phase 2), and `UNATTENDED_EXPECT` in `tests/skills/test_worker_contract.py` holds exactly those 31 entries.
+- A coordinator puts `--unattended` and one report directory on the 16 phase 1 commands by default; the phase 2 commands join that default after a phase 2 live check passes. It decides by the two-copy test in `~/.claude/WORKER-CONTRACT.md` ("Before the first task-create for a command"), not by a list in this guide. A command gains `--unattended` and its section in the phase that converts its gates, so no command accepts the flag while it can still stop for a human.
 - Per the rollout plan (SA-1), without `--unattended` every command behaves exactly as it does today: the same prompts, approval gates, default values, output paths and outward defaults.
 
 #### Deciding whether a new command can be a worker


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
