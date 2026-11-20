40980041dad130b05e6fbca05ea27c2d49f260c8
Review one task for spec compliance.

Task brief: ## Task 8: Add the flags and Unattended rules to the workflow command

Depends on: Task 6, Task 7

Edit `src/superclaude/commands/workflow.md`: Usage and Options table gain `--remediate none|surgical|regenerate` (default: the route of the routing rule runs after Wave 4; `none` records counts and the chosen route and changes nothing; the other two force a route and are recorded as forced) and `--revise <package-dir> --review <REPORT.md>` (run the route for a package reviewed outside workflow); Behavioral Summary and Boundaries (Will, Will Not) describe the bounded remediation instead of "never edit the plan"; the Unattended section says the surgical route runs without a person, escalation after 2 fix cycles ends the run `partial` with the open blockers in `unresolved` and the last placed package keeps `review_verdict: FAIL`, and nested reflect calls for re-reviews use the next `nested/reflect-<n>/` directory and are listed in `artifacts`. Keep the existing `--unattended` rules and the `E-LEGACY` list unchanged. Update the `argument-hint` line of the command with the two new flags, and copy the finished file byte for byte to `plugins/superclaude/commands/workflow.md` (`tests/commands/test_workflow_command.py` requires the two to be identical).

Acceptance criteria:
- `grep -n -e '--remediate' -e '--revise' src/superclaude/commands/workflow.md` shows the two flags in Usage, Options and the Unattended section.
- The Boundaries text no longer says plans are never edited from findings.
- `cmp src/superclaude/commands/workflow.md plugins/superclaude/commands/workflow.md` prints nothing, and `uv run pytest tests/commands/test_workflow_command.py -q` passes.
- `make sync-dev` then `make verify-sync` is clean.
Global constraints: ## Constraints

- The design is `docs/designs/surgical-remediation.md`. Where it disagrees with `.dev/issues/624/accuracy-check.md` or `.dev/issues/624/analysis/analyze-sc-workflow-protocol.md`, those two files win: the reflect bump has consumers, the workflow package contract stays at `contract_version: "1.1"`, and seven packages (not four) are migrated. Anchor edits by text, not by the line numbers of the design (they moved).
- Edit only `src/superclaude/` sources, `tests/`, `scripts/`, `plugins/superclaude/` copies of the edited files (including the new `refs/remediation.md` and `scripts/remediate.py` of the workflow skill, which the plugin mirror must carry (the `diff -rq` checks of Task 6 require it), and `plugins/superclaude/commands/workflow.md`), `.dev/README.md` and the data migration. Never hand-edit the dev copies under the project `.claude/` folder; after each task that changes a primitive run `make sync-dev` and then `make verify-sync`.
- Installed primitives never point at a `src/superclaude/...` path. In every edited skill, command or core doc, name other primitives by their installed path (`~/.claude/skills/<name>/SKILL.md`) and name the project `.claude/` copy second.
- Where a file in `plugins/superclaude/` mirrors an edited file (the workflow and implement protocols and `commands/workflow.md`), keep the mirror byte-identical to the `src/` file (`diff -rq` shows no difference); a new file in an already mirrored folder is mirrored too. `remediate.py` uses only the Python standard library (installed skill scripts run under `uv run --no-project`) and edits archived contracts by appending lines, never by loading and re-writing the YAML.
- Decision made by this plan because the design leaves it open: `finding_counts.label_high` counts the Deviations-table label HIGH on the legacy reviewer path, and counts findings-v2 severity CRITICAL on the shadow-panel path (the panel has no HIGH label). `blocking`, `medium` and `note` count the grades `Blocking (...)`, `Medium:` and `Note:` (or the panel's `blocking` flag). On the panel path, `medium` counts findings-v2 severity MAJOR with `blocking` false and `note` counts severity MINOR.
- The workflow package contract adds only additive fields under `contract_version: "1.1"`: `remediation_route`, `supersedes`, `superseded_by`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`. `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` and `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` keep accepting only "1.1".
- Only blocking findings are ever repaired. No fix pass touches text for a Medium or Note finding.
- Out of scope: the wording of the review severity rule, reviewer models, `/sc:design`, `/sc:brainstorm`, `/sc:spec-panel`'s own loop, deleting archived packages, and `src/superclaude/rules/prompts/document_review_loop_prompts.md` (reused as written).
- Reflect's own `--remediate` plan route keeps calling `sc:workflow`; `src/superclaude/cli/reflect/runner.py` gets no code change (its fail-closed handling of a non-zero apply already covers a refused package).
Start sha: 40980041dad130b05e6fbca05ea27c2d49f260c8
Diff against the start snapshot: diff --git a/plugins/superclaude/commands/workflow.md b/plugins/superclaude/commands/workflow.md
index 96a9140e1..38a1b1032 100644
--- a/plugins/superclaude/commands/workflow.md
+++ b/plugins/superclaude/commands/workflow.md
@@ -4,7 +4,7 @@ description: "Generate a phased implementation plan from a PRD, spec, or feature
 category: orchestration
 complexity: standard
 mcp-servers: [codegraph]
-argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement]"
+argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement] [--remediate none|surgical|regenerate] [--revise <package-dir> --review <REPORT.md>]"
 ---
 
 # /sc:workflow — Implementation Plan Generator
@@ -28,6 +28,8 @@ Exactly one source: an existing file path (`@path` ok) **or** leftover `$ARGUMEN
              [--strategy systematic|agile|enterprise]
              [--depth quick|standard|deep]
              [--handoff none|design|implement]
+             [--remediate none|surgical|regenerate]
+/sc:workflow --revise <package-dir> --review <REPORT.md>        # route for a package reviewed outside workflow
 /sc:workflow <path-or-prompt> --unattended --report-dir <dir>   # worker mode, see Unattended mode
 ```
 
@@ -39,6 +41,8 @@ Exactly one source: an existing file path (`@path` ok) **or** leftover `$ARGUMEN
 | `--strategy` | `systematic` | `systematic` \| `agile` \| `enterprise`. Enterprise + omitted depth → `deep` |
 | `--depth` | `standard` | `quick` \| `standard` \| `deep` |
 | `--handoff` | `none` | `none` / `design` = text; `implement` = Skill invoke |
+| `--remediate` | route of the routing rule, run after Wave 4 | `none` \| `surgical` \| `regenerate`. `none` records the finding counts and the chosen route and changes nothing; `surgical` and `regenerate` force that route and are recorded as forced |
+| `--revise <package-dir>` + `--review <REPORT.md>` | off | Given together: run the route for a package that was reviewed outside workflow, using that review report |
 | `--unattended` | off | Worker mode: no step waits for a person; see Unattended mode |
 | `--report-dir` | none | With `--unattended`, the directory that holds the worker contract |
 
@@ -47,6 +51,7 @@ Banned (`E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`, and t
 ## Behavioral Summary
 
 Command file: parse flags → STOP on empty/banned → Activation. Protocol owns waves. Final generation step (after the gate, before any handoff): advisory `/sc:reflect --mode pre` of the plan against the source; its report path/status is printed and recorded in `return-contract.yaml`.
+After that review, Wave 4R routes the blocking findings (`none`, `surgical`, `regenerate` or `escalate`) and repairs only blocking findings, for at most 2 fix cycles; Medium and Note findings are counted and never repaired. `--revise <package-dir> --review <REPORT.md>` runs the same route for a package reviewed outside workflow. The routing rule and the repair steps are in the protocol (`~/.claude/skills/sc-workflow-protocol/SKILL.md`).
 The protocol runs one codegraph readiness check per run: a fresh index grounds the plan and that pre-check in the real code, otherwise Grep/Read do and the fallback is recorded.
 
 ## Activation
@@ -87,13 +92,14 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 - **Handoff.** A `--handoff implement` is skipped (the implement executor accepts the flag only in a later phase) and recorded in the package contract as `partial` with one `unresolved` line. The `design` handoff is text and unchanged.
 - **Gates.** None else, and no person-mode flag.
 - **Nested invocations.** Under `--unattended` the Wave 4 reflect step receives `--unattended --output <report-dir>/nested/reflect-<n>/` (reflect's own directory flag; workflow's `--output` stays retired; `<n>` counts from 1 and is never reused), still without `--remediate`, and its contract is listed in `artifacts`, also when the call failed. A nested contract is read by the nested-result rule of `~/.claude/WORKER-CONTRACT.md`.
+- **Remediation.** The `--remediate` and `--revise ... --review ...` routes run without a person. The surgical route runs unattended; escalation after 2 fix cycles ends the run `partial`, lists the open blockers in `unresolved`, and the last placed package keeps `review_verdict: FAIL`. Nested reflect calls for re-reviews use the next unused `nested/reflect-<n>/` directory and each one is listed in `artifacts`.
 - **Outward actions.** The command does not stage `.dev/tasks` and leaves that to the coordinator; it pushes and commits nothing.
 
 ## Boundaries
 
-**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`. Ground the plan in the real code through codegraph when the index is fresh.
+**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`. Ground the plan in the real code through codegraph when the index is fresh. Run the bounded remediation after Wave 4: repair only blocking findings (surgical route, at most 2 fix cycles) or build one replacement package (regenerate route), and record the route and finding counts in the package contract.
 
-**Will Not:** mutate product code; edit the plan from reflect findings.
+**Will Not:** mutate product code; edit a plan for a Medium or Note finding; edit a plan outside the surgical route or beyond 2 fix cycles; regenerate more than once per run.
 
 ## Related Commands
 
diff --git a/src/superclaude/commands/workflow.md b/src/superclaude/commands/workflow.md
index 96a9140e1..38a1b1032 100644
--- a/src/superclaude/commands/workflow.md
+++ b/src/superclaude/commands/workflow.md
@@ -4,7 +4,7 @@ description: "Generate a phased implementation plan from a PRD, spec, or feature
 category: orchestration
 complexity: standard
 mcp-servers: [codegraph]
-argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement]"
+argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement] [--remediate none|surgical|regenerate] [--revise <package-dir> --review <REPORT.md>]"
 ---
 
 # /sc:workflow — Implementation Plan Generator
@@ -28,6 +28,8 @@ Exactly one source: an existing file path (`@path` ok) **or** leftover `$ARGUMEN
              [--strategy systematic|agile|enterprise]
              [--depth quick|standard|deep]
              [--handoff none|design|implement]
+             [--remediate none|surgical|regenerate]
+/sc:workflow --revise <package-dir> --review <REPORT.md>        # route for a package reviewed outside workflow
 /sc:workflow <path-or-prompt> --unattended --report-dir <dir>   # worker mode, see Unattended mode
 ```
 
@@ -39,6 +41,8 @@ Exactly one source: an existing file path (`@path` ok) **or** leftover `$ARGUMEN
 | `--strategy` | `systematic` | `systematic` \| `agile` \| `enterprise`. Enterprise + omitted depth → `deep` |
 | `--depth` | `standard` | `quick` \| `standard` \| `deep` |
 | `--handoff` | `none` | `none` / `design` = text; `implement` = Skill invoke |
+| `--remediate` | route of the routing rule, run after Wave 4 | `none` \| `surgical` \| `regenerate`. `none` records the finding counts and the chosen route and changes nothing; `surgical` and `regenerate` force that route and are recorded as forced |
+| `--revise <package-dir>` + `--review <REPORT.md>` | off | Given together: run the route for a package that was reviewed outside workflow, using that review report |
 | `--unattended` | off | Worker mode: no step waits for a person; see Unattended mode |
 | `--report-dir` | none | With `--unattended`, the directory that holds the worker contract |
 
@@ -47,6 +51,7 @@ Banned (`E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`, and t
 ## Behavioral Summary
 
 Command file: parse flags → STOP on empty/banned → Activation. Protocol owns waves. Final generation step (after the gate, before any handoff): advisory `/sc:reflect --mode pre` of the plan against the source; its report path/status is printed and recorded in `return-contract.yaml`.
+After that review, Wave 4R routes the blocking findings (`none`, `surgical`, `regenerate` or `escalate`) and repairs only blocking findings, for at most 2 fix cycles; Medium and Note findings are counted and never repaired. `--revise <package-dir> --review <REPORT.md>` runs the same route for a package reviewed outside workflow. The routing rule and the repair steps are in the protocol (`~/.claude/skills/sc-workflow-protocol/SKILL.md`).
 The protocol runs one codegraph readiness check per run: a fresh index grounds the plan and that pre-check in the real code, otherwise Grep/Read do and the fallback is recorded.
 
 ## Activation
@@ -87,13 +92,14 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 - **Handoff.** A `--handoff implement` is skipped (the implement executor accepts the flag only in a later phase) and recorded in the package contract as `partial` with one `unresolved` line. The `design` handoff is text and unchanged.
 - **Gates.** None else, and no person-mode flag.
 - **Nested invocations.** Under `--unattended` the Wave 4 reflect step receives `--unattended --output <report-dir>/nested/reflect-<n>/` (reflect's own directory flag; workflow's `--output` stays retired; `<n>` counts from 1 and is never reused), still without `--remediate`, and its contract is listed in `artifacts`, also when the call failed. A nested contract is read by the nested-result rule of `~/.claude/WORKER-CONTRACT.md`.
+- **Remediation.** The `--remediate` and `--revise ... --review ...` routes run without a person. The surgical route runs unattended; escalation after 2 fix cycles ends the run `partial`, lists the open blockers in `unresolved`, and the last placed package keeps `review_verdict: FAIL`. Nested reflect calls for re-reviews use the next unused `nested/reflect-<n>/` directory and each one is listed in `artifacts`.
 - **Outward actions.** The command does not stage `.dev/tasks` and leaves that to the coordinator; it pushes and commits nothing.
 
 ## Boundaries
 
-**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`. Ground the plan in the real code through codegraph when the index is fresh.
+**Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`. Ground the plan in the real code through codegraph when the index is fresh. Run the bounded remediation after Wave 4: repair only blocking findings (surgical route, at most 2 fix cycles) or build one replacement package (regenerate route), and record the route and finding counts in the package contract.
 
-**Will Not:** mutate product code; edit the plan from reflect findings.
+**Will Not:** mutate product code; edit a plan for a Medium or Note finding; edit a plan outside the surgical route or beyond 2 fix cycles; regenerate more than once per run.
 
 ## Related Commands
 


Codegraph context: index_state: fresh; checked_at: 2026-11-20T02:48:46Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-624; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-624
call codegraph only when index_state: fresh, never to widen scope
(Q2b dependents not in the diff: none recorded; Grep/Read floor used.)
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
