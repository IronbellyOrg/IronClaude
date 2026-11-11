5c3769b62813c84fca7b6133159cd1ad532d0bdd
Review one task for spec compliance.

Task brief: ## Task 3: Copy the two files to the plugin mirror and sync the dev copies

Depends on: Task 2

Copy the final `src/superclaude/commands/workflow.md` to `plugins/superclaude/commands/workflow.md` and the final `src/superclaude/skills/sc-workflow-protocol/SKILL.md` to `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md` (the other files in that skill folder are unchanged and already match). Then run `make sync-dev` and `make verify-sync`. If `make verify-sync` names files this plan does not own, run `make sync-dev` once more and re-check; never edit those files. Run the tests that cover the three edited files.

Acceptance criteria:
- [T3.AC1] `cmp src/superclaude/commands/workflow.md plugins/superclaude/commands/workflow.md` and `cmp src/superclaude/skills/sc-workflow-protocol/SKILL.md plugins/superclaude/skills/sc-workflow-protocol/SKILL.md` print nothing.
- [T3.AC2] `make sync-dev` and `make verify-sync` exit 0 (any failure naming a file owned by another session is reported, not fixed).
- [T3.AC3] `uv run pytest tests/commands/test_workflow_command.py tests/skills/test_worker_contract.py tests/skills/test_task_workspace_lifecycle.py` passes, including `test_plugin_mirror_matches_src`; any failure that cannot be attributed to this change is reported instead of fixed.
- [T3.AC4] `grep -rn 'src/superclaude' src/superclaude/commands/workflow.md src/superclaude/skills/sc-workflow-protocol` shows no hit that tells an agent to read a `src/superclaude/...` path beyond the hits present before this change.
- [T3.AC5] `git status --short` lists no `.claude/` path as staged and nothing is committed.

Global constraints: 
- Edit only `src/superclaude/skills/sc-workflow-protocol/SKILL.md`, `src/superclaude/commands/workflow.md` and, because `tests/commands/test_workflow_command.py::test_plugin_mirror_matches_src` pins them byte for byte, the two matching files under `plugins/superclaude/`. Do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, or any file another session owns.
- Cite only the installed guide `~/.claude/CODEGRAPH.md`; add no instruction that tells an agent to read a `src/superclaude/...` path.
- Keep `mcp-servers: []` and `Skill sc:workflow-protocol` in the command file, the template reference `refs/00_mdtm_template_simple_task.md` in SKILL.md, the Wave 3, 4, 5 order, and the `## Unattended mode` section and `refs/return-contract.md` wording that `tests/skills/test_worker_contract.py` parses.
- No commit, no push, no pull request, no `git add` of any `.claude/` path.


Start sha: 5c3769b62813c84fca7b6133159cd1ad532d0bdd
Diff against the start snapshot:
diff --git a/plugins/superclaude/commands/workflow.md b/plugins/superclaude/commands/workflow.md
index d7deb2033..c70d6074c 100644
--- a/plugins/superclaude/commands/workflow.md
+++ b/plugins/superclaude/commands/workflow.md
@@ -47,6 +47,7 @@ Banned (`E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`, and t
 ## Behavioral Summary
 
 Command file: parse flags → STOP on empty/banned → Activation. Protocol owns waves. Final generation step (after the gate, before any handoff): advisory `/sc:reflect --mode pre` of the plan against the source; its report path/status is printed and recorded in `return-contract.yaml`.
+The protocol runs one codegraph readiness check per run: a fresh index grounds the plan and that pre-check in the real code, otherwise Grep/Read do and the fallback is recorded.
 
 ## Activation
 
@@ -63,6 +64,19 @@ The full behavioral specification is in `~/.claude/skills/sc-workflow-protocol/S
 /sc:workflow "add logout to the header" --handoff none
 ```
 
+## Codegraph grounding
+
+One codegraph readiness check per run, owned by the protocol (`~/.claude/CODEGRAPH.md` section 2, run at the start of Wave 1); this command never repeats it. Codegraph is used only when `index_state` is `fresh`. In any other state, or when a lookup fails, Grep, Glob and Read do the same job and the matching `graph:*` token is recorded in `<pkg>/artifacts/codegraph-grounding.md`. It never stops the run, fails the gate or changes the package status. `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` is honoured (`graph:disabled`).
+
+| Step | Codegraph tool when fresh | Floor |
+|------|---------------------------|-------|
+| Wave 1, step 0 | `codegraph_status` (the readiness check) | guarded CLI `status`, else the floor |
+| Wave 1 | `codegraph_search`, `codegraph_node` with `symbolsOnly:true`: resolve the files and symbols the source names | Glob, Grep, Read |
+| Wave 2 | `codegraph_node` with `includeCode:true`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`: name real callers and dependents in tasks and acceptance criteria, order and size tasks by blast radius | Grep with a word-boundary pattern, then Read |
+| Wave 4 pre-check | the same lookups, read-only | the same floor |
+
+Under `--unattended` the same rules apply; no gate and no person-mode flag is added. The protocol (`~/.claude/skills/sc-workflow-protocol/SKILL.md`) holds the details.
+
 ## Unattended mode
 
 The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:workflow` resolves itself.
@@ -77,7 +91,7 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 
 ## Boundaries
 
-**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`.
+**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`. Ground the plan in the real code through codegraph when the index is fresh.
 
 **Will Not:** mutate product code; edit the plan from reflect findings; emit `tasklist-index.md`; run `superclaude roadmap`.
 
diff --git a/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md b/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
index 830aa9098..fcca92a15 100644
--- a/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
+++ b/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
@@ -1,10 +1,14 @@
 ---
 name: sc:workflow-protocol
 description: "Behavioral protocol for /sc:workflow — PRD/spec to phased tasklist (<id>.md)"
-allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill
+allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill, mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_callees, mcp__codegraph__codegraph_impact
 argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement|tasklist]"
 ---
 
+<!-- Extended metadata (for documentation, not parsed):
+mcp-servers: [codegraph]
+-->
+
 # /sc:workflow protocol
 
 Invoked only via `/sc:workflow` Activation. Plan only. Wave 2 is **Synthesize**.
@@ -16,6 +20,25 @@ Invoked only via `/sc:workflow` Activation. Plan only. Wave 2 is **Synthesize**.
 | Load ref | Read |
 | Write artifact | Write |
 | Invoke Skill | Skill (`sc:reflect-protocol` in Wave 4; `sc:implement-protocol` only on `--handoff implement`) |
+| Codegraph lookup | `mcp__codegraph__codegraph_<tool>` (exact names), only when `index_state` is `fresh` |
+
+## Codegraph grounding
+
+Rules, the closed `graph:*` token list and the caller-row, cap and read-before-cite rules are in `~/.claude/CODEGRAPH.md` (section 2 readiness, section 3 tokens, sections 5 and 6 rules, caps and `shown/total`). This protocol points there and copies none of it.
+
+- **One readiness check per run.** Step 0 of Wave 1 (the package exists, before any lookup) runs section 2 of the guide once. It records `index_state`, `checked_at`, `worktree_root`, `projectPath`, the access mode and any `graph:*` token under `## Run state` in `<pkg>/artifacts/codegraph-grounding.md`. Later waves read that record and never run the check again.
+- **Fresh only.** Codegraph runs only when `index_state` is `fresh` and its lookup tools are listed, with `projectPath` on every call. In any other state, or when a lookup fails or returns nothing, that step uses Grep, Glob and Read (the permanent floor, normal evidence) and the matching `graph:*` token goes into the grounding note. This never stops the run, fails the gate or changes the package status.
+- **Rows are leads.** A graph row locates code and is not a citation: Read the range before a task names it. A caller row gives the caller's definition, so a task says "calls X" only after the call site is confirmed under guide section 5; otherwise it names the caller as a dependent. An empty answer never means "no callers".
+
+| Step | Job | Codegraph tool when fresh | Floor |
+|------|-----|---------------------------|-------|
+| Wave 1, step 0 | Readiness check | `codegraph_status {projectPath}` | guarded CLI `status` per the guide, else the floor |
+| Wave 1 | Resolve the files and symbols the source names; outline each named file | `codegraph_search {query, kind?, limit}`, `codegraph_node {file, symbolsOnly:true}`, and for an area overview `codegraph_files {format:"grouped", maxDepth:2}` (outside `allowed-tools`: called only when the session lists it, else Glob) | Glob, Grep for definitions, Read |
+| Wave 2 | Body of each changed symbol; real callers and dependents; blast radius | `codegraph_node {symbol, file?, includeCode:true}`, `codegraph_callers {symbol, file?, limit}`, `codegraph_callees`, `codegraph_impact {symbol, depth:1}` | Grep with a word-boundary pattern, then Read each site |
+| Wave 4 pre-check | The same lookups, read-only | the same tools | the same floor |
+
+- **Sub-agent briefs.** Any brief this protocol writes for a sub-agent carries `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass; the receiver calls codegraph only when `index_state: fresh`, otherwise Grep and Read. The Wave 4 `/sc:reflect --mode pre` call takes flags only, so it cannot receive that state: reflect runs its own readiness check, which this run does not count as a second one.
+- **Artifact.** `<pkg>/artifacts/codegraph-grounding.md` has the sections `## Run state`, `## Resolved symbols`, `## Dependents` and `## Pre-check`. It is a file this run wrote, so under `--unattended` it is listed in `artifacts` by the rule "every other file the run wrote" in the `## Unattended mode` section of the `workflow` command file. It adds no plan field and no contract key.
 
 ## Wave 0 — Parse
 
@@ -37,6 +60,8 @@ Under `--unattended` that staging is deferred to the coordinator (`~/.claude/WOR
 
 Entry: readable source. Exit: phase list with Goal/Inputs/Outputs/Checkpoint/deps.
 
+Step 0 (once per run): the codegraph readiness check of `## Codegraph grounding`; then resolve the files and symbols the source names (codegraph when fresh, else Glob, Grep and Read) and record them under `## Resolved symbols` in `<pkg>/artifacts/codegraph-grounding.md`.
+
 If nothing actionable → STOP `E-NO-PHASES`.
 
 Depth caps phase count (quick 2–4, standard 4–8, deep 6–12).
@@ -47,6 +72,8 @@ Write `<pkg>/<id>.md` (the full package directory basename + `.md`, e.g. `TASK-W
 
 Each Wave 1 phase → `## Phase N:` then its `## Task N:` headings (numbered 1..N across the plan). Phase Inputs → files/sections named in the task body; Outputs → the body and `Acceptance criteria:` of the task that produces each one (every Output lands in some task); Checkpoint → the last task's `Acceptance criteria:`; deps → `Depends on: Task K`.
 
+Ground each task in the real code: its body names the real files and symbols it changes (repo-relative), and its `Acceptance criteria:` name the real callers and dependents that must keep working or be updated (recorded under `## Dependents` of the grounding artifact; codegraph when fresh, else Grep and Read). Size and order tasks by blast radius: a symbol with many dependents gets its own task, the tasks that update its dependents follow it with `Depends on: Task K`, and a change reaching more files than one task can hold is split, still within the depth cap.
+
 `source.md` MUST already exist from Wave 0 (snapshot of the file or the inline prompt) before `<id>.md` is written.
 
 ## Wave 3 — Gate
@@ -57,6 +84,8 @@ quick = schema-min. standard/deep = full. Fail → STOP `E-GATE`.
 
 ## Wave 4 — Reflect
 
+**Pre-check (advisory, before the reflect call).** For each task, confirm that the files it names exist, its symbols resolve and its listed dependents are real, and list dependents of the touched symbols that no task names (codegraph when fresh, else Grep, Glob and Read; no new readiness check). Write the result under `## Pre-check` in `<pkg>/artifacts/codegraph-grounding.md` and print a one-line count with the plan path. It never edits `<id>.md` and never changes `status`; a failure of this step is only a `graph:*` note.
+
 Final step of plan generation; runs only after Wave 3 passed, and **before** the Wave 5 contract and any `--handoff` (so an unreflected plan is never implemented). Invoke `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` via Skill (`sc:reflect-protocol`), defaults for every other flag, no `--remediate`. Record reflect's `status` and `report_path` (from its `return-contract.yaml`) as `reflect_status` / `reflect_report_path`, and print both with the plan path.
 
 Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) that call passes `--unattended --output <report-dir>/nested/reflect-<n>/` (reflect's own directory flag; workflow's `--output` stays retired; `<n>` counts from 1 and is never reused), still without `--remediate`, and the nested contract is listed in `artifacts`, also when the call failed.
@@ -73,6 +102,6 @@ After an `implement` handoff the package may have moved to `done/` (executor-own
 
 ## Will / Will Not
 
-**Will:** one new package `.dev/tasks/to-do/<id>/` with `<id>.md`, `source.md`, `return-contract.yaml`. Never overwrites or reuses an existing package. Run `/sc:reflect --mode pre` (advisory) on the gated plan as the final generation step, before any handoff.
+**Will:** one new package `.dev/tasks/to-do/<id>/` with `<id>.md`, `source.md`, `return-contract.yaml`; ground the plan in the real code through codegraph when the index is fresh. Never overwrites or reuses an existing package. Run `/sc:reflect --mode pre` (advisory) on the gated plan as the final generation step, before any handoff.
 
 **Will Not:** product code, tasklist files, roadmap CLI, new agents, Task fan-out; modify the plan from reflect findings.

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
