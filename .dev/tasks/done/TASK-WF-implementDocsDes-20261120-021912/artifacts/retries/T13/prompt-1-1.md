ceef5ccf9191770f3786f9fd3a668a1360f9b75e
Review one task for spec compliance.

Task brief: ## Task 13: Move the seven superseded packages out of `to-do/`

Depends on: Task 4, Task 9, Task 12

Move exactly these seven packages from `.dev/tasks/to-do/` to `.dev/tasks/archive/` using `remediate.py archive` (no `mv`), `--superseded-by none` for every package except the one that names a replacement: `TASK-WF-designSpec-20261107-072120`, `TASK-WF-designSpec-20261107-074040`, `TASK-WF-p3Requirements-20261107-065757`, `TASK-WF-removeTheAnyIssu-20261031-235404`, `TASK-WF-removeTheAnyIssu-20261101-225338`, `TASK-WF-removeTheAnyIssu-20261101-225635` and `TASK-WF-removeTheAnyIssu-20261102-042031`. Each moved contract keeps its existing `SUPERSEDED` line and gets no second one; the p3Requirements package is archived with `--superseded-by TASK-WF-p3Requirements-20261107-070713` (the id its contract names), the other six with `--superseded-by none` because their contracts name no existing replacement id. Do not move `TASK-WF-blockerStage4-20261116-030206` (it has no `return-contract.yaml` at all; its replacement `TASK-WF-blockerStage4-20261117-170451` says it is superseded) or `TASK-WF-specScRecommendR-20261024-055620` (an intake with no plan); print both as open owner decisions in the task result. Write the list of moved ids and the two open decisions to `./artifacts/migration.md`. Run `git add .dev/tasks` afterwards (staging only).

Acceptance criteria:
- `ls .dev/tasks/to-do` shows none of the seven ids and `ls .dev/tasks/archive` shows all seven, each with its plan, `source.md` and `return-contract.yaml` intact.
- `grep -il 'SUPERSEDED' .dev/tasks/to-do/*/return-contract.yaml` lists exactly `TASK-WF-blockerStage4-20261117-170451` (its contract says the older plan is superseded) and `TASK-WF-specScRecommendR-20261024-055620`, which are the two open owner decisions.
- `./artifacts/migration.md` names the seven moves and the two open decisions.
- `make verify-sync` and `uv run pytest tests/skills tests/core tests/cli/reflect -q` pass.
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
Start sha: ceef5ccf9191770f3786f9fd3a668a1360f9b75e
Diff against the start snapshot: 

Codegraph context: index_state: fresh; checked_at: 2026-11-20T02:48:46Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-624; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-624
call codegraph only when index_state: fresh, never to widen scope
(Q2b dependents not in the diff: none recorded; Grep/Read floor used.)

Codegraph-free summary of the .dev/tasks moves (git diff --cached -M --name-status, other packages only; the unified diff above excludes .dev/tasks):
R100	.dev/tasks/to-do/TASK-WF-designSpec-20261107-072120/TASK-WF-designSpec-20261107-072120.md	.dev/tasks/archive/TASK-WF-designSpec-20261107-072120/TASK-WF-designSpec-20261107-072120.md
A	.dev/tasks/archive/TASK-WF-designSpec-20261107-072120/artifacts/archive-undo.txt
R100	.dev/tasks/to-do/TASK-WF-designSpec-20261107-072120/return-contract.yaml	.dev/tasks/archive/TASK-WF-designSpec-20261107-072120/return-contract.yaml
R100	.dev/tasks/to-do/TASK-WF-designSpec-20261107-072120/source.md	.dev/tasks/archive/TASK-WF-designSpec-20261107-072120/source.md
R100	.dev/tasks/to-do/TASK-WF-designSpec-20261107-074040/TASK-WF-designSpec-20261107-074040.md	.dev/tasks/archive/TASK-WF-designSpec-20261107-074040/TASK-WF-designSpec-20261107-074040.md
A	.dev/tasks/archive/TASK-WF-designSpec-20261107-074040/artifacts/archive-undo.txt
R100	.dev/tasks/to-do/TASK-WF-designSpec-20261107-074040/return-contract.yaml	.dev/tasks/archive/TASK-WF-designSpec-20261107-074040/return-contract.yaml
R100	.dev/tasks/to-do/TASK-WF-designSpec-20261107-074040/source.md	.dev/tasks/archive/TASK-WF-designSpec-20261107-074040/source.md
R100	.dev/tasks/to-do/TASK-WF-p3Requirements-20261107-065757/TASK-WF-p3Requirements-20261107-065757.md	.dev/tasks/archive/TASK-WF-p3Requirements-20261107-065757/TASK-WF-p3Requirements-20261107-065757.md
A	.dev/tasks/archive/TASK-WF-p3Requirements-20261107-065757/artifacts/archive-undo.txt
R092	.dev/tasks/to-do/TASK-WF-p3Requirements-20261107-065757/return-contract.yaml	.dev/tasks/archive/TASK-WF-p3Requirements-20261107-065757/return-contract.yaml
R100	.dev/tasks/to-do/TASK-WF-p3Requirements-20261107-065757/source.md	.dev/tasks/archive/TASK-WF-p3Requirements-20261107-065757/source.md
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261031-235404/TASK-WF-removeTheAnyIssu-20261031-235404.md	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261031-235404/TASK-WF-removeTheAnyIssu-20261031-235404.md
A	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261031-235404/artifacts/archive-undo.txt
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261031-235404/return-contract.yaml	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261031-235404/return-contract.yaml
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261031-235404/source.md	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261031-235404/source.md
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225338/TASK-WF-removeTheAnyIssu-20261101-225338.md	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261101-225338/TASK-WF-removeTheAnyIssu-20261101-225338.md
A	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261101-225338/artifacts/archive-undo.txt
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225338/return-contract.yaml	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261101-225338/return-contract.yaml
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225338/source.md	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261101-225338/source.md
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225635/TASK-WF-removeTheAnyIssu-20261101-225635.md	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261101-225635/TASK-WF-removeTheAnyIssu-20261101-225635.md
A	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261101-225635/artifacts/archive-undo.txt
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225635/return-contract.yaml	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261101-225635/return-contract.yaml
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225635/source.md	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261101-225635/source.md
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-042031/TASK-WF-removeTheAnyIssu-20261102-042031.md	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261102-042031/TASK-WF-removeTheAnyIssu-20261102-042031.md
A	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261102-042031/artifacts/archive-undo.txt
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-042031/return-contract.yaml	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261102-042031/return-contract.yaml
R100	.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-042031/source.md	.dev/tasks/archive/TASK-WF-removeTheAnyIssu-20261102-042031/source.md

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
