2e5e63a66a04e974e424ed3cfe099b68d614eed1
Review one task for spec compliance.

Task brief: ## Task 12: Document the archive folder in `.dev/README.md`

Edit `.dev/README.md`: the Workflow task packages section adds `.dev/tasks/archive/` (superseded packages, never run, deleted only on an explicit owner order), and the bullet "Look in both places" becomes three places (`to-do/` in flight, `done/` finished, `archive/` superseded); mention the surgical and regenerate routes in one sentence each and that `/sc:implement` refuses a plan under `archive/` or one with `review_verdict: FAIL`.

Acceptance criteria:
- The "Look in both places" bullet names all three folders and says a package present in `to-do/` and `archive/` or `done/` is a conflict to resolve by hand.
- `.dev/README.md` contains no sentence that says superseded packages stay in `to-do/`.
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
Start sha: 2e5e63a66a04e974e424ed3cfe099b68d614eed1
Diff against the start snapshot: diff --git a/.dev/README.md b/.dev/README.md
index a8de57665..ddbf70282 100644
--- a/.dev/README.md
+++ b/.dev/README.md
@@ -22,7 +22,7 @@ The enforcement layers that depend on this rule:
 | `releases/` | Release planning, in-flight releases (`current/`), completed work (`archive/`), backlog (`backlog/`), and templates (`templates/`). |
 | `research/` | Free-form research notes, decision memos, and analysis artefacts that inform design decisions. |
 | `resurrection-contracts/` | Recovery contracts (gate definitions) used when an audit needs to re-execute against a known good state. |
-| `tasks/` | MDTM task files — `done/` holds completed tasks; loose `*.md` files are in-flight or staged work. Also holds **workflow task packages** (`to-do/TASK-WF-*/`, `done/TASK-WF-*/`) — see [Workflow task packages](#workflow-task-packages). |
+| `tasks/` | MDTM task files — `done/` holds completed tasks; loose `*.md` files are in-flight or staged work. Also holds **workflow task packages** (`to-do/TASK-WF-*/`, `done/TASK-WF-*/`, `archive/TASK-WF-*/`) — see [Workflow task packages](#workflow-task-packages). |
 | `test-fixtures/` | Static input fixtures used by skill harnesses and evals (e.g. `test-prd-user-auth.md`) plus `results/`. |
 | `test-sprints/` | Sprint CLI smoke-test bundles used to validate the sprint pipeline end-to-end. |
 
@@ -44,7 +44,7 @@ If you find yourself wanting to write to `.claude/skills/<skill>-workspace/` or
 
 ## Workflow task packages
 
-`/sc:workflow` creates one **new** package per generation (it never overwrites one): `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` (UTC; `<subject>` is lower camelCase, max 16 chars, e.g. `authLogin`; `-2`..`-9` suffix on a collision in `to-do/` or `done/`). The tasklist file is named exactly like the package directory plus `.md` (`TASK-WF-authLogin-20261001-063000.md`, collision suffix included). `--output` is retired — there is no destination override.
+`/sc:workflow` creates one **new** package per generation (it never overwrites one): `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` (UTC; `<subject>` is lower camelCase, max 16 chars, e.g. `authLogin`; `-2`..`-9` suffix on a collision in `to-do/`, `done/` or `archive/`). The tasklist file is named exactly like the package directory plus `.md` (`TASK-WF-authLogin-20261001-063000.md`, collision suffix included). `--output` is retired — there is no destination override.
 
 ```text
 .dev/tasks/to-do/TASK-WF-<id>/
@@ -59,5 +59,8 @@ If you find yourself wanting to write to `.claude/skills/<skill>-workspace/` or
 - **Completion.** After every task is complete, `/sc:implement` runs a fresh independent final review (every archive attempt, even for a one-task plan) and then a small helper moves the whole package to `.dev/tasks/done/<id>/`. No commit, PR, merge or release is implied.
 - **Archiving is Linux-only and fail-closed.** It uses `renameat2(RENAME_NOREPLACE)`; on another OS, an unsupported filesystem/kernel, a cross-filesystem move or any existing destination it refuses and leaves the package in `to-do/` — it never falls back to `mv`/copy.
 - **Interrupted archive.** An existing `<package>/.archiving` marker always stops the next run. After you confirm the original run has stopped, clear it explicitly with the helper's `--clear-marker <token>` (the token is in `.archiving/owner`); nothing reclaims it automatically.
-- **Look in both places.** To find work, scan `.dev/tasks/to-do/TASK-WF-*/` (in flight) and `.dev/tasks/done/TASK-WF-*/` (finished). A package present in both is a conflict: stop and resolve it by hand.
+- **Archive of superseded packages.** `.dev/tasks/archive/TASK-WF-*/` holds packages that a newer package replaced. They are never run and are deleted only on an explicit owner order. `/sc:implement` refuses a plan under `archive/` and a plan whose contract says `review_verdict: FAIL` (blocking review findings still open).
+- **Surgical route.** When the final review of `/sc:workflow` finds 1 to 3 blocking findings, the plan is repaired on a copy, the old package moves to `archive/`, and the repaired copy is placed as a new package in `to-do/` and re-reviewed (at most 2 fix cycles).
+- **Regenerate route.** When the review finds more blocking findings than that, the plan is regenerated as a new package (at most once per run) and the old package moves to `archive/`.
+- **Look in three places.** To find work, scan `.dev/tasks/to-do/TASK-WF-*/` (in flight), `.dev/tasks/done/TASK-WF-*/` (finished) and `.dev/tasks/archive/TASK-WF-*/` (superseded). A package present in `to-do/` and in `archive/` or `done/` is a conflict: stop and resolve it by hand.
 - **Preserved legacy runs.** Plans generated before this layout (`workflow-plan/1.1`, `.dev/workflow/<slug>/`) and their path-hashed ledgers under `.dev/implement/` keep working unchanged; they are not migrated.


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
