a449eb7540389a05a613f7e39d5e3689a878e4eb
Review one task for spec compliance.

Task brief: 
## Task 3: Rewrite the section 5 template and slot rules to a positive default

Depends on: Task 2

In `src/superclaude/core/WORKER-CONTRACT.md` section 5 ("Coordinator brief template", from line 283), change the template `Command:` placeholder (line 296) so it reads `Command: /sc:<name> <arguments> --unattended <the report directory flag: the command's own directory flag where its table row names one, else --report-dir <dir>> <other flags this command's brief rule requires>`. Rewrite the slot rules below it: the first bullet (line 303) becomes the default rule: put `--unattended` and exactly one report directory on every `Command:` line, for each step and never as a session-wide setting, unless the two-copy test of "Before the first task-create for a command" fails for that command; the default set is the 16 phase 1 commands (keep the list adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, build, business-panel, design, document, explain, index, test) until a phase 2 live check passes. Keep the existing bullet that starts `- From P2 ` as one line and keep all 15 phase 2 command names in it (the test helper `_p2_bullet` reads it); reword it to say these commands accept the flag under the same guard test and join the default set only after a phase 2 live check passes, and that the coordinator flags one of them before that only when the user's instruction names it. Add a bullet that lists what the flag drops: improve and cleanup skip approval-required items, test ends `succeeded` when its suite fails (read the verdict in the report), research is forced to `--strategy planning`, workflow skips `--handoff implement`, and WC-9 turns off every push, PR and other outward action. Add a bullet that a command must be started through its Skill call (WC-7; reading the command file does not do it, decision P1-C5) and that a person-in-the-loop run is not a worker.

Acceptance criteria:
- T3.AC1: The template's `Command:` line visibly contains `--unattended`, and the brief-template guard-before-command check in `tests/skills/test_worker_contract.py` (`_check_guard_before_command`) still passes.
- T3.AC2: Section 5 contains the 16 phase 1 command names in the default rule, exactly one line starting `- From P2 ` that still names all 15 phase 2 commands, the five drop items, the Skill-call sentence and the person-in-the-loop sentence.
- T3.AC3: No sentence in section 5 says the flag is allowed only where a section exists without also stating the default.
- T3.AC4: The rows of the flags table for `/sc:review-translation`, `/sc:cli-portify`, `/sc:cli-eval`, `/sc:reflect` and `/sc:tdd` are unchanged.

Global constraints: 
## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

Start sha: a449eb7540389a05a613f7e39d5e3689a878e4eb
Diff against the start snapshot: 
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 59dcb62db..57708379a 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -305,15 +305,17 @@ Report directory: <directory unique to this Task>
 Worktree: <shared feature worktree | child worktree created by Orca with worker-start --worktree new-child --base-branch <feature branch> --setup <skip | run (only when named in the user's instruction)>>
 Outward actions: none; the coordinator performs every push, PR, comment, install and paid run.
 P0 only: Report file: <the command's report file under AC-0.4>. Outcome rule: --outcome failed when the file is missing or empty, or its status is failed or blocked; otherwise --outcome succeeded. This rule replaces the WC-5 mapping for this Task.
-Command: /sc:<name> <arguments> <flags this command's brief rule requires>
+Command: /sc:<name> <arguments> --unattended <report-directory-flag> <other flags this command's brief rule requires>
 ```
 
 Slot rules:
 
 - `On a blocked gate:` is `report blocked` (the default) or `ask the coordinator` (WC-3).
 - `Local commit:` is `not authorized`, or `authorized` followed by the user's instruction naming a local commit for this Task, quoted word for word (WC-9, decision D4).
-- `--unattended` goes on a `Command:` line only when the guard's test shows that every copy of that command file the worker will see has an `## Unattended mode` section. At P0 no command accepts it. From P1 the 16 commands converted in P1 do (adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, build, business-panel, design, document, explain, index, test).
-- From P2 the 15 commands converted in P2 accept `--unattended` too, under the same guard test (auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot).
+- Put `--unattended` and exactly one report directory on every `Command:` line, for each step and never as a session-wide setting, unless the two-copy test in "Before the first task-create for a command" (section 4) fails for that command. `<report-directory-flag>` in the template is the command's own directory flag where its row in the table below names one (for example `--output <dir>`), else `--report-dir <dir>`; the directory is unique to the Task. The default set is the 16 commands converted in P1 (adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, build, business-panel, design, document, explain, index, test) until a phase 2 live check passes.
+- From P2 the 15 commands converted in P2 accept `--unattended` too, under the same guard test (auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot). They join the default set only after a phase 2 live check passes; until then the coordinator puts the flag on one of them only when the user's instruction names that command.
+- The flag changes what a command does, so the coordinator reads each report and never treats the flag as free: `/sc:improve` and `/sc:cleanup` skip every approval-required item and list it as not applied; `/sc:test` ends `succeeded` even when its suite fails (the verdict is in its report); `/sc:research` is forced to `--strategy planning`; `/sc:workflow` skips `--handoff implement`; every push, PR, comment and other outward action is off (WC-9).
+- A command is started through its Skill call (WC-7); reading the command file and following it from memory does not satisfy WC-7. A person-in-the-loop run is not a worker: a run that needs a person at a gate belongs in the person's own session.
 - The `P0 only:` line is used only before P1, when no command writes a worker contract. At P0 the report files are: troubleshoot, `<dir>/REPORT.md` with the status in its `**Status**:` line; workflow, the `return-contract.yaml` in the one new `TASK-WF-*` package directory the run creates under `.dev/tasks/to-do/`, with the status in its top-level `status`; adversarial, `<dir>/adversarial/merge-log.md` with the status in the `Status:` line of its `## Metadata` section. From P1 the line is dropped and WC-5 applies.
 
 Flags the brief must pass, for the 12 commands that are ready with brief constraints. `--report-dir` is marked "from P1": no command accepts it at P0. Under `--unattended` the brief passes exactly one report directory (`--report-dir <dir>`, or the command's own directory flag where the row names one); `/sc:index-repo` and `/sc:init-lite` have no directory flag of their own, so they take `--report-dir`. The table also lists the five P2 commands with a required brief flag (`/sc:auggie-review`, `/sc:cli-eval`, `/sc:cli-portify`, `/sc:review-translation`, `/sc:spec-panel`), so it has 17 rows.


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
