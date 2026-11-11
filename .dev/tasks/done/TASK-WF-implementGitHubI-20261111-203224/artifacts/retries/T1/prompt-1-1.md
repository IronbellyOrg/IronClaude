ae4029c4fec0e023ba95b418efa39412b2727330
Review one task for spec compliance.

Task brief: 
## Task 1: Make the three guard refusal texts name the repair

In `src/superclaude/core/WORKER-CONTRACT.md`, in the "Brief guard" term (lines 16-22 of the current file), keep each refusal string's existing words, including the prefix `guard refused:`, and append the repair for the coordinator after it. Case 1 (`guard refused: brief lacks --unattended`) names: add `--unattended` and exactly one report directory to that `Command:` line in a new Task. Case 2 (`guard refused: loaded command has no Unattended mode section ...`) names: refresh `~/.claude` (a stale installed copy) or drop `--unattended` for that command, then create a new Task. The disagree refusal (`guard refused: command copies disagree (stale copy): <paths>`) names: refresh the stale copy listed in `<paths>`, normally `~/.claude`, then create a new Task. After the "A command invoked by another command ..." sentence add one sentence stating the refusal is report-only: the worker never installs or refreshes a command copy and never rewrites its own brief; the coordinator repairs and creates a new Task (WC-6).

Acceptance criteria:
- T1.AC1: Each of the three refusal strings in the file still contains its original text word for word, so the existing pins at lines 58-78 of `tests/skills/test_worker_contract.py` still match, and each is followed by a repair clause naming `--unattended` plus exactly one report directory (case 1) or refreshing `~/.claude` (case 2 and the disagree refusal).
- T1.AC2: The file states that the worker never installs or refreshes a copy and never rewrites its brief on a refusal.
- T1.AC3: `grep -c 'guard refused:' src/superclaude/core/WORKER-CONTRACT.md` still finds the prefix on every refusal line.

Global constraints: 
## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

Start sha: ae4029c4fec0e023ba95b418efa39412b2727330
Diff against the start snapshot: 
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 7b5972164..778e113a1 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -14,12 +14,12 @@ The dispatch preamble that Orca gives each worker is the authority for Orca verb
 - **Person-mode flags are refused**: under `--unattended`, every command refuses the flags that exist to involve a person: `--interactive`, `--format interactive` (explain), `--mode socratic` (business-panel), `--watch` (test), `--monitor 1` (pr-submit). A refusal is a stop before any work: the command writes its contract with `worker_status: failed` and the refused flag in `reason` (WC-4), or, when no report directory is known, prints the refusal in chat only (WC-4, last sentences). This one rule applies to every command.
 - **Report directory**: the directory that holds the worker contract (WC-4). Under `--unattended` the brief passes exactly one: either the command's own existing directory-valued output flag (`--output <dir>` or `--output-dir <dir>`), or the new flag `--report-dir <dir>` (for a command without such a flag, or a brief that does not pass it). An output flag added for worker use is file-valued, so those commands always take `--report-dir`. Passing neither, or both, is refused before any work (WC-4).
 - **Brief guard** (worker session, from P1): it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (see "Worker run"). Before invoking anything, the worker checks every `Command:` line of its brief (section 4, "Brief layout"), and only those lines. It decides case 3 from the command name alone. For the other cases it reads, as plain files, every existing copy of the command file: the project `.claude/commands/sc/<name>.md` in its worktree and `~/.claude/commands/sc/<name>.md`. It refuses, runs nothing, writes no contract, and sends `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:` when:
-  - (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended`: `guard refused: brief lacks --unattended`;
-  - (case 2) no existing copy has the section and the line has the flag: `guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`;
-  - the copies disagree: `guard refused: command copies disagree (stale copy): <paths>`;
+  - (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended`: `guard refused: brief lacks --unattended` followed by the repair `(coordinator: add --unattended and exactly one report directory to this Command: line, then create a new Task)`;
+  - (case 2) no existing copy has the section and the line has the flag: `guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)` followed by the repair `(coordinator: refresh ~/.claude if its copy is stale, or drop --unattended for this command, then create a new Task)`;
+  - the copies disagree: `guard refused: command copies disagree (stale copy): <paths>` followed by the repair `(coordinator: refresh the stale copy named in <paths>, normally ~/.claude, then create a new Task)`;
   - (case 3) the command is on the never-as-worker list; the body still starts `guard refused:`.
 
-  A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer.
+  A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer. A refusal is report-only: the worker never installs or refreshes a command copy and never rewrites its own brief; the coordinator repairs the cause and creates a new Task (WC-6).
 - **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode. The list changes only when the coordinator-only command set or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
 - **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.
   Reading a nested result: when the nested worker contract says `blocked`, the caller stops at that step and writes its own contract with `worker_status: blocked`, `blocked_question` set to the nested question prefixed with the nested command's name, and the nested contract in `artifacts`; when it says `failed`, or no nested contract exists, the caller takes its own documented failure path for that step (fallback, skip and record, or stop), and if that ends the run it writes `worker_status: failed` with the nested command and its reason in `reason`; `succeeded` and `partial` count as the step completing.


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
