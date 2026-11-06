4bc4a227ee57b7b65857a90b16939cf3ae1e5d7e
Review one task for spec compliance.

Task brief: ## Task 6: Add the corrected wording to the worker-contract spec in two places

In `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` make two edits, each on one existing line.

First, the section 2.1 bullet `**Nested propagation rule**` (line 62) ends with "Each command's `## Unattended mode` section names its nested invocations." Append this sentence to that line, copied character for character:

```text
A nested directory `nested/<command>-<n>/` exists only for a nested command that actually ran, a run that failed included; a command that does the same work through a tool or a native-search fallback (brainstorm's codebase scan through `mcp__auggie__codebase-retrieval`, or through codegraph, then Glob and Grep) writes no nested directory and records the tier it used in its own contract, and brainstorm's live-check extra for this is in 7.2 step 4.
```

Second, section 7.2 step 4 is the line that begins "4. Check the contract (PyYAML is a declared dependency" (line 286) and ends "At P0, AC-0.4 replaces this step." The fenced shell block for that step follows on the next lines and is not edited. Append this sentence to the end of the step 4 line, copied character for character:

```text
A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts`; a `nested/analyze-<n>/` directory is required, and must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing, only when a `Skill` tool call (not a `Task` or `Agent` call whose prompt only names `/sc:analyze`) in the worker's session file or in one of its subagent files (7.2 step 5) invokes `sc:analyze` with `--report-dir <report directory>/nested/analyze-<n>/` and a number for `<n>` and returns no tool error, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).
```

Placement and wording are a Necessary deviation from the brief, recorded here. The brief allows either the live-check section or a note in the P1 rows, and sketches the wording as "a fallback_1 or auggie primary scan is recorded as the tier used with no nested folder". This plan puts the live-check sentence in 7.2 step 4 because every later live plan attaches its step-4 extras there, and sections 7.2 and 7.3 hold no per-command extras list of their own, so the P2 live-plan author reads 7.2 step 4. The wording departs from the sketch because tier does not decide whether the folder must exist: a clean `/sc:analyze` run is also `primary`, and neither `quality_tier` nor `source` names the tool. The trigger is an actual `Skill` call that invokes `sc:analyze`, because a `Task` or `Agent` prompt that only names the command can be followed by an auggie or `fallback_1` scan that writes no folder. The whole-text check in the acceptance criteria is required by the brief's rule that each correction's verifier has an equivalent check; it is not one of the pins correction F-7 lists. Task 6's second acceptance criterion also checks that the old trigger wording ``a `Skill`, `Agent` or `Task` tool call`` is gone; this goes beyond the pins correction F-7 lists, on purpose, because three of the four positive pins are also in the old sentence.

Residual risks of the live-check sentence are left in place on purpose; all are in the false-PASS direction, and the sentence has no known false FAIL on a correct run:
- A `/sc:analyze` call made without the nested `--report-dir` (a broken propagation, itself a defect) is not seen, so its missing folder passes. Related: INV-022 (no live check can force the analyze route).
- The required-directory clause sees only a `Skill` tool call that invokes `sc:analyze`. The spec's nested propagation rule (spec:62) names the Skill tool, but how the session file records the invoked command, its arguments and a tool error is INFERRED from Claude Code's session format (spec:302 says only "`tool_use` blocks with a `name`"); a `/sc:analyze` run made another way, or recorded under another name, is missed and its missing folder passes.
- The `skipped` carve-out also exempts an invoked `/sc:analyze` that wrote nothing and was recorded `skipped` for a reason other than the timeout, and, because `enrichment_used` holds one `codebase` entry, it exempts every `nested/analyze-<n>/` call of the run at once.
- The required-folder clause depends on the session file; when it is missing or ambiguous the clause is `not verifiable`, and spec:300 then blocks a PASS until the owner accepts the gap in writing (accepted by design, INV-023).
- An `artifacts` entry under a directory that is not required (a `skipped`, refused or tool-error call) is not checked for existence; Task 1's "also when the call failed" produces exactly this case.

Leave the `brainstorm` row of the section 3.1 table (line 142) and everything else in the spec as it is.

Acceptance criteria:
- The `**Nested propagation rule**` bullet in section 2.1 contains `only for a nested command that actually ran` and `7.2 step 4`.
- The section 7.2 step 4 line contains `lc10`, ``a `source: codebase` entry``, ``neither `quality_tier` nor `source` records`` and ``invokes `sc:analyze` ``, and does not contain ``a `Skill`, `Agent` or `Task` tool call``.
- `git diff --stat -- .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` shows two lines changed (two insertions, two deletions), and `git diff -U0` on that file shows hunks only at the section 2.1 bullet and the section 7.2 step 4 line.
- With `S` as in Task 1, `X=$(sed -n 223p "$S")` and `Y=$(sed -n 219p "$S")` are non-empty, `grep -cxF` on this plan prints 1 for each, and `grep -cF` against `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` prints 1 for each.
Global constraints: ## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker. The archived record is in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/` (`artifacts/lc10-result.md`, `artifacts/p1-owner-decisions-20261105.md`); those files are read, never edited.
- This plan replaces two earlier plans for the same work, packages `TASK-WF-brainstormFixBri-20261106-001016` and `TASK-WF-brainstormFixBri-20261106-021737`. An independent review found the first not ready to run (its Task 6 wording decided the nested folder by `quality_tier`, its Task 7 status check could not pass on the current tree, and the owner rule was not fully pinned). A second review found that the second plan's live-check sentence required the folder whenever any `Skill`, `Agent` or `Task` call passed the flag text, so a `Task` prompt followed by an auggie or `fallback_1` scan would fail a correct run; the owner amended the brief's Part 4 on 2026-11-06 and this plan carries the amended text. Both earlier packages are left as they are.
- Edit only these six files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, and no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill). It is not edited. This is this plan's resolution of spec open item 8 for `brainstorm.md`. Task 7 confirms nothing under `plugins/` changed.
- No new text in the installed files (the skill, its refs, the command file) may name a `src/superclaude/` path or an Orca command; `tests/skills/test_worker_contract.py` (`_check_unattended_section`) fails on both.
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the owner updates the installed copies under `~/.claude/` later). No git commit, push, merge or PR.
- The edits reach the next live plan only after the owner commits and merges them; this plan does not commit.
- Open conflict, no change planned here: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. This is an open conflict for the owner and the P2 live-plan author.
- Starting state: the working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. Task 1 records this state before any edit and Task 7 compares against it.
Start sha: 4bc4a227ee57b7b65857a90b16939cf3ae1e5d7e
Diff against the start snapshot: diff --git a/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md b/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
index 71ee2873..d95712cc 100644
--- a/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
+++ b/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
@@ -59,7 +59,7 @@ The evidence supports the decision. Three gaps are stated plainly:
 - **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/`: the installer copies every `*.md` in `core/` (`src/superclaude/cli/install_core.py:36,56,65-70`; `CLAUDE.md:83,408`). The new name is also added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-27`), which only controls which installed files `list_installed_core_files` reports (`install_core.py:12,155`); installation itself is checked by AC-0.1. The file holds the command-side rules (WC-2, WC-4, WC-8 to WC-11, the flag parse rule, the person-mode refusal above and the nested propagation rule below), the worker session's brief guard and the never-as-worker list below, and the coordinator's rules (WC-6 and section 2.3, including its brief template and the template's guard line). For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats) it states only the IronClaude-specific rule (outcome mapping from `worker_status`, including WC-5's P0 brief override, top-level only, ask only when the brief allows it) and points to the dispatch preamble as the authority for Orca verb syntax and heartbeat cadence; it never copies them, because the preamble is issued per dispatch by the running Orca version (`CAPS:130`). Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
 - **Brief guard** (worker session, from P1): it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (see "Worker run"). Before invoking anything, the worker checks every `Command:` line of its brief (section 2.3, "Brief layout"), and only those lines. It decides case 3 from the command name alone. For the other cases it reads, as plain files, every existing copy of the command file: the project `.claude/commands/sc/<name>.md` in its worktree and `~/.claude/commands/sc/<name>.md`. It refuses, runs nothing, writes no contract, and sends `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:` when: (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended` (`guard refused: brief lacks --unattended`); (case 2) no existing copy has the section and the line has the flag (`guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`); the copies disagree (`guard refused: command copies disagree (stale copy): <paths>`); (case 3) the command is on the never-as-worker list. A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer.
 - **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard` (section 4), plus `/sc:pr-submit` while the answer to D3 keeps it off workers. The list changes only when section 4 or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
-- **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.
+- **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations. A nested directory `nested/<command>-<n>/` exists only for a nested command that actually ran, a run that failed included; a command that does the same work through a tool or a native-search fallback (brainstorm's codebase scan through `mcp__auggie__codebase-retrieval`, or through codegraph, then Glob and Grep) writes no nested directory and records the tier it used in its own contract, and brainstorm's live-check extra for this is in 7.2 step 4.
 
 ### 2.2 Requirements
 Each requirement says what the command must do, what the worker session (the top-level agent that received the preamble) must do, and the evidence.
@@ -283,7 +283,7 @@ For each command under test, the coordinator runs the steps below with one worke
 1. `ORCA orchestration task-create --spec "<brief per section 2.3>" --json`. Then either `ORCA orchestration worker-start --task <task_id> --worktree new-top-level --base-branch <branch> --setup run --agent claude --json`, when the setup is confirmed to run `make sync-dev`; or create the worktree first with `ORCA worktree create` from `<branch>`, run `make sync-dev` inside it, and start the worker with `--worktree path:<worktree>`. For a command that accepts `--unattended` at this phase, confirm before dispatch that every existing copy of its file (`<worktree>/.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`) has its `## Unattended mode` section. **Pass:** exit 0 and `state: ready` (`CAPS:46`).
 2. While it runs, `ORCA orchestration worker-show --dispatch <dispatch_id> --json` at least once per 5 minutes. **Pass:** `observation.agentWait` is never non-null (a non-null value means the worker is parked on a prompt only a person can answer, `CAPS:129`). Sampling can only find a wait, not prove there was none; step 3 adds the positive proof.
 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. If the wait ends without one, read `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json`: a final agent turn that sent no `worker_done` is Orca's positive proof of a stall (`CAPS:126`), and the check fails; a transcript still growing means keep waiting. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `worker_status` under WC-5; its report path is the WC-4 contract path. At P0, before the contract exists, AC-0.4 replaces the last two conditions.
-4. Check the contract (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both commands exit 0. At P0, AC-0.4 replaces this step.
+4. Check the contract (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both commands exit 0. At P0, AC-0.4 replaces this step. A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts`; a `nested/analyze-<n>/` directory is required, and must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing, only when a `Skill` tool call (not a `Task` or `Agent` call whose prompt only names `/sc:analyze`) in the worker's session file or in one of its subagent files (7.2 step 5) invokes `sc:analyze` with `--report-dir <report directory>/nested/analyze-<n>/` and a number for `<n>` and returns no tool error, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).
    ```sh
    test -s <contract>
    uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['worker_contract_version'] == '1'; assert d['worker_status'] in {'succeeded','partial','failed','blocked'}; assert d['command']; assert d['worker_status'] != 'blocked' or d.get('blocked_question')" <contract>
diff --git a/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t6-checks.txt b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t6-checks.txt
new file mode 100644
index 00000000..03aad764
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/artifacts/t6-checks.txt
@@ -0,0 +1,26 @@
+== 2.1 bullet (line 62) pins
+1
+only for a nested command that actually ran: 1
+7.2 step 4: 1
+== 7.2 step 4 (line 286) pins
+1
+lc10: 1
+a `source: codebase` entry: 1
+neither `quality_tier` nor `source` records: 1
+invokes `sc:analyze` : 1
+forbidden (expect 0): 0
+== diff stat
+ .dev/orca-command-refactor/specs/orca-worker-contract-spec.md | 4 ++--
+ 1 file changed, 2 insertions(+), 2 deletions(-)
+2	2	.dev/orca-command-refactor/specs/orca-worker-contract-spec.md
+== hunk headers
+@@ -62 +62 @@ The evidence supports the decision. Three gaps are stated plainly:
+@@ -286 +286 @@ For each command under test, the coordinator runs the steps below with one worke
+== row 142 unchanged
+same
+== whole-text
+X_len=450 Y_len=1210
+X plan_cxF=1
+X spec_cF=1
+Y plan_cxF=1
+Y spec_cF=1
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
