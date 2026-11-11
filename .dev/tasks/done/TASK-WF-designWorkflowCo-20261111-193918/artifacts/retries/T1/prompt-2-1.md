4656192e2213410d16af9164aeaa61915737960f
Review one task for spec compliance.

Task brief: ## Task 1: Add the codegraph grounding rules to the protocol SKILL.md

Edit `src/superclaude/skills/sc-workflow-protocol/SKILL.md` as specified in `./source.md` sections 3.2 to 3.8 and 4. In the frontmatter, append exactly these tools to `allowed-tools`: `mcp__codegraph__codegraph_status`, `mcp__codegraph__codegraph_search`, `mcp__codegraph__codegraph_node`, `mcp__codegraph__codegraph_callers`, `mcp__codegraph__codegraph_callees`, `mcp__codegraph__codegraph_impact` (no wildcard), and add an extended-metadata comment block carrying `mcp-servers: [codegraph]` in the style of `src/superclaude/skills/sc-reflect-protocol/SKILL.md`. Add a vocabulary row for codegraph lookups (exact tool names, only when `index_state` is `fresh`). Add a `## Codegraph grounding` section between the vocabulary table and Wave 0 that states: the one readiness check per run runs at the start of Wave 1 following section 2 of `~/.claude/CODEGRAPH.md` and is never repeated; the result `index_state`, `checked_at`, `worktree_root`, `projectPath` plus access and tokens is written to `<pkg>/artifacts/codegraph-grounding.md`; the tool-to-step table of `./source.md` section 3.3 (Wave 1 `codegraph_search`, `codegraph_node` with `symbolsOnly:true`, `codegraph_files`; Wave 2 `codegraph_node` with `includeCode:true`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`; Wave 4 pre-check); the fresh-only rule with the permanent Grep/Glob/Read floor and the closed `graph:*` token list from the guide, never a STOP, a gate failure or a status change; Read before cite, caller rows verified at the call site, an empty graph answer never meaning no callers; and that any sub-agent brief the protocol writes carries `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass, with the receiver using codegraph only when `index_state: fresh`. Add one line each in Wave 1 (readiness check, resolve named files and symbols), Wave 2 (name real callers and dependents in task bodies and acceptance criteria, order and split tasks by blast radius, within the depth cap) and Wave 4 (advisory read-only pre-check before the existing reflect call, findings under `## Pre-check` in the grounding artifact, the plan never edited).

Acceptance criteria:
- [T1.AC1] The SKILL.md frontmatter `allowed-tools` contains the six exact `mcp__codegraph__codegraph_*` names above and no `mcp__codegraph__*` wildcard, and the file contains `mcp-servers: [codegraph]`.
- [T1.AC2] The file states exactly one codegraph readiness check per run (Wave 1) and names which codegraph tool serves Wave 1, Wave 2 and the Wave 4 pre-check.
- [T1.AC3] The file states codegraph is used only when `index_state` is `fresh`, that otherwise Grep/Glob/Read run with a `graph:*` note, and that nothing in this feature halts the run, fails the gate or changes the package status.
- [T1.AC4] The file names `index_state`, `checked_at`, `worktree_root` and `projectPath` as the run state carried by any sub-agent brief.
- [T1.AC5] `grep -n 'src/superclaude' src/superclaude/skills/sc-workflow-protocol/SKILL.md` prints no line that tells an agent to read a `src/superclaude/...` path.
- [T1.AC6] Wave order, the template reference, the retired `--output` wording and the Wave 4 `nested/reflect-` line are unchanged: `uv run pytest tests/commands/test_workflow_command.py -k "not plugin_mirror"` passes.


Global constraints: 
- Edit only `src/superclaude/skills/sc-workflow-protocol/SKILL.md`, `src/superclaude/commands/workflow.md` and, because `tests/commands/test_workflow_command.py::test_plugin_mirror_matches_src` pins them byte for byte, the two matching files under `plugins/superclaude/`. Do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, or any file another session owns.
- Cite only the installed guide `~/.claude/CODEGRAPH.md`; add no instruction that tells an agent to read a `src/superclaude/...` path.
- Keep `mcp-servers: []` and `Skill sc:workflow-protocol` in the command file, the template reference `refs/00_mdtm_template_simple_task.md` in SKILL.md, the Wave 3, 4, 5 order, and the `## Unattended mode` section and `refs/return-contract.md` wording that `tests/skills/test_worker_contract.py` parses.
- No commit, no push, no pull request, no `git add` of any `.claude/` path.


Start sha: 4656192e2213410d16af9164aeaa61915737960f
Diff against the start snapshot:
diff --git a/src/superclaude/skills/sc-workflow-protocol/SKILL.md b/src/superclaude/skills/sc-workflow-protocol/SKILL.md
index 830aa9098..fcca92a15 100644
--- a/src/superclaude/skills/sc-workflow-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-workflow-protocol/SKILL.md
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

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/src/superclaude/skills/sc-workflow-protocol/SKILL.md b/src/superclaude/skills/sc-workflow-protocol/SKILL.md
index 661028a56..fcca92a15 100644
--- a/src/superclaude/skills/sc-workflow-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-workflow-protocol/SKILL.md
@@ -33,7 +33,7 @@ Rules, the closed `graph:*` token list and the caller-row, cap and read-before-c
 | Step | Job | Codegraph tool when fresh | Floor |
 |------|-----|---------------------------|-------|
 | Wave 1, step 0 | Readiness check | `codegraph_status {projectPath}` | guarded CLI `status` per the guide, else the floor |
-| Wave 1 | Resolve the files and symbols the source names; outline each named file | `codegraph_search {query, kind?, limit}`, `codegraph_node {file, symbolsOnly:true}` | Glob, Grep for definitions, Read |
+| Wave 1 | Resolve the files and symbols the source names; outline each named file | `codegraph_search {query, kind?, limit}`, `codegraph_node {file, symbolsOnly:true}`, and for an area overview `codegraph_files {format:"grouped", maxDepth:2}` (outside `allowed-tools`: called only when the session lists it, else Glob) | Glob, Grep for definitions, Read |
 | Wave 2 | Body of each changed symbol; real callers and dependents; blast radius | `codegraph_node {symbol, file?, includeCode:true}`, `codegraph_callers {symbol, file?, limit}`, `codegraph_callees`, `codegraph_impact {symbol, depth:1}` | Grep with a word-boundary pattern, then Read each site |
 | Wave 4 pre-check | The same lookups, read-only | the same tools | the same floor |
 
Earlier blocking findings of this start (empty on the first review): F1.1 ac=scope at=src/superclaude/skills/sc-workflow-protocol/SKILL.md:36 anchor="Wave 1 `codegraph_search`, `codegraph_node` with `symbolsOnly:true`, `codegraph_files`" chk=n,n,n,y family=table-tool-omission fix=list codegraph_files in the Wave 1 row (used only when the session lists it) while keeping the six-tool allowed-tools first=A1 origin=new: the Wave 1 row omits codegraph_files that the task text puts in the tool-to-step table
Saved-probe re-check hit locations (may be empty): 36:| Wave 1 | Resolve the files and symbols the source names; outline each named file | `codegraph_search {query, kind?, limit}`, `codegraph_node {file, symbolsOnly

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
