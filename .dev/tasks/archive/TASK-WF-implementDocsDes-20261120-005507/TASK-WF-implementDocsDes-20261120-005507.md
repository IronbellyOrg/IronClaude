---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementDocsDes-20261120-005507
version: "1"
priority: Medium
created_date: "2026-11-20"
---

# Implement surgical remediation of a reviewed workflow package (issue 624)

Source: ./source.md
Goal: After Wave 4 of /sc:workflow, a plan with 1 to 3 blocking review findings is repaired on a copy, the old package is archived, the repaired copy is placed as a new package and re-reviewed (at most 2 fix cycles); larger finding sets are regenerated at most once per run; a plan that still has blockers carries `review_verdict: FAIL` and /sc:implement refuses it; /sc:reflect reports `finding_counts` in contract 1.9.0; superseded packages leave `to-do/` and the seven existing ones are migrated.

## Constraints

- The design is `docs/designs/surgical-remediation.md`. Where it disagrees with `.dev/issues/624/accuracy-check.md` or `.dev/issues/624/analysis/analyze-sc-workflow-protocol.md`, those two files win: the reflect bump has consumers, the workflow package contract stays at `contract_version: "1.1"`, and seven packages (not four) are migrated. Anchor edits by text, not by the line numbers of the design (they moved).
- Edit only `src/superclaude/` sources, `tests/`, `scripts/`, `plugins/superclaude/` copies of files that already exist there, `.dev/README.md` and the data migration. Never hand-edit the dev copies under the project `.claude/` folder; after each task that changes a primitive run `make sync-dev` and then `make verify-sync`.
- Installed primitives never point at a `src/superclaude/...` path. In every edited skill, command or core doc, name other primitives by their installed path (`~/.claude/skills/<name>/SKILL.md`) and name the project `.claude/` copy second.
- Where a file in `plugins/superclaude/skills/` mirrors an edited file (the workflow and implement protocols), keep the mirror byte-identical to the `src/` file (`diff -rq` shows no difference).
- Decision made by this plan because the design leaves it open: `finding_counts.label_high` counts the Deviations-table label HIGH on the legacy reviewer path, and counts findings-v2 severity CRITICAL on the shadow-panel path (the panel has no HIGH label). `blocking`, `medium` and `note` count the grades `Blocking (...)`, `Medium:` and `Note:` (or the panel's `blocking` flag).
- The workflow package contract adds only additive fields under `contract_version: "1.1"`: `remediation_route`, `supersedes`, `superseded_by`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`. `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` and `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` keep accepting only "1.1".
- Only blocking findings are ever repaired. No fix pass touches text for a Medium or Note finding.
- Out of scope: the wording of the review severity rule, reviewer models, `/sc:design`, `/sc:brainstorm`, `/sc:spec-panel`'s own loop, deleting archived packages, and `src/superclaude/rules/prompts/document_review_loop_prompts.md` (reused as written).
- Reflect's own `--remediate` plan route keeps calling `sc:workflow`; `src/superclaude/cli/reflect/runner.py` gets no code change (its fail-closed handling of a non-zero apply already covers a refused package).

## Phase 1: Reflect reports finding counts (contract 1.9.0)

## Task 1: Add `finding_counts` and bump the reflect contract text to 1.9.0

Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md`: the section 9.1 heading (`### 9.1 Stable contract (contract_version: 1.8.0)`) and its field list gain `finding_counts: {blocking, label_high, medium, note}` (computed from the merged findings after the evidence validator, in both pre and post modes); the section 9.4 sentence `Contract version is v1.8.0`, the grader row `return-contract.yaml contract_version == "1.8.0"` and the two sentences that say the contract "stays 1.8.0" (the panel publish step and the three-engine-keys sentence) move to 1.9.0. Keep the historical "1.8.0" remark on `remediation_plan_path` (the field was added in 1.8.0). Edit `src/superclaude/skills/sc-reflect-protocol/refs/report-template.md` (`contract_version: 1.8.0` in the example) and `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md` (the `contract_version == "1.8.0"` row) to 1.9.0. Edit `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` to state how a panel reviewer's findings map to `label_high` (CRITICAL) and to the other three counts. Edit `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` only for the 1.8.0 pin on `remediation_plan_path` if it names the current version rather than the introducing version (Task 10 owns its other changes).

Acceptance criteria:
- `finding_counts` appears once in the section 9.1 field list with the four keys, and `grep -n '1\.8\.0' src/superclaude/skills/sc-reflect-protocol/SKILL.md` leaves only lines that say a field was introduced in 1.8.0.
- `report-template.md` and `grader-extensions.md` say 1.9.0 and contain no current-version 1.8.0 pin.
- `reviewer-spec.md` states the CRITICAL-to-`label_high` mapping and the panel `blocking` flag mapping in plain words.

## Task 2: Move the reflect contract checkers, scripts and tests to 1.9.0

Depends on: Task 1

Edit `src/superclaude/cli/reflect/panel_lint.py`: rename the field tuple `STABLE_FIELDS_1_8_0` to `STABLE_FIELDS_1_9_0` and add `finding_counts` to it, set `CONTRACT_VERSION = "1.9.0"`, and update the L1, L2, L3 and B-bump failure messages and the module docstring that name 1.8.0 (its users are `scripts/reflect_shadow_exit.py` and `tests/cli/reflect/test_panel_contract_lint.py`). Edit `scripts/reflect_shadow_exit.py` and `scripts/reflect_verdict_replay.py` (`VERSION = "1.8.0"`) so a recorded 1.8.0 or 1.9.0 contract is counted and no other version is. Edit `tests/cli/reflect/test_panel_contract_lint.py`, `tests/cli/reflect/test_shadow_skill_contract.py` (both pin the heading `### 9.1 Stable contract (contract_version: 1.8.0)`), `tests/cli/reflect/test_shadow_exit_script.py`, `tests/cli/reflect/test_verdict_replay_script.py`, `tests/review/test_reflect_consumer_inventory.py` and the fixtures `tests/cli/reflect/fixtures/panel_lint_legacy/return-contract.yaml`, `tests/cli/reflect/fixtures/autofixable_drift_both.yaml` and `tests/cli/reflect/fixtures/autofixable_drift_plan.yaml` wherever they pin the current version. `src/superclaude/cli/reflect/contract.py` (checks the major version only) and `src/superclaude/cli/reflect/models.py` need no change; `scripts/reflect_consumer_inventory.py` only reports and changes only if its test requires it.

Acceptance criteria:
- A 1.9.0 contract carrying `finding_counts` passes `lint_panel_contract` (checks L1, L2 and the B bump rule); a contract with an unknown top-level key or version 1.8.0 still fails as before for the right reason (new cases in `tests/cli/reflect/test_panel_contract_lint.py`).
- `uv run pytest tests/cli/reflect tests/review/test_reflect_consumer_inventory.py -q` passes.
- `src/superclaude/cli/reflect/contract.py` parses a fixture 1.9.0 contract that has `finding_counts` without error (one new assertion in an existing test under `tests/cli/reflect/`).

## Phase 2: Routing and package-swap script

## Task 3: Create the routing rule as a tested script

Create `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` with a pure function `route(blocking, label_high, medium, regenerated_already=False, forced=None)` and a `route` command-line subcommand that prints one JSON object `{"route": ..., "forced": ...}`. Rows in order, first match wins: blocking equals 0 gives `none`; blocking at most 3 and label_high at most 5 and medium at most 9 gives `surgical`; otherwise `regenerate`; a `regenerate` result when `regenerated_already` is true gives `escalate`. `forced` (`none`, `surgical` or `regenerate`) overrides and is recorded as forced. Reject negative or non-integer counts with a non-zero exit. Create `tests/skills/test_workflow_remediation.py` (style of `tests/skills/test_workflow_archive.py`, which loads a script by file path) with the route tests.

Acceptance criteria:
- Parametrized tests cover the boundaries blocking 3/4, label_high 5/6, medium 9/10, blocking 0 with label_high 20 and medium 30 (route `none`), a forced route, and the second regenerate (`escalate`).
- `uv run pytest tests/skills/test_workflow_remediation.py -q` passes.

## Task 4: Add the package copy, archive, place and restore operations

Depends on: Task 3

Extend `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py` with these subcommands, all taking `--root <checkout>`: `prepare --package <dir>` makes a private directory with `mktemp -d /tmp/sc-workflow-revise.XXXXXXXX` semantics, copies the plan `<id>.md` and `source.md` into it and prints the directory and the sha256 of the original plan; `archive --package <dir> --superseded-by <new-id>` moves the package from `.dev/tasks/to-do/<old-id>/` to `.dev/tasks/archive/<old-id>/` and records a `SUPERSEDED` line naming the new id in the moved package's `return-contract.yaml` `unresolved` list (writing a minimal contract with `status: partial` first when Wave 5 has not written one); `place --old-id <id> --copy-dir <dir> --route surgical|regenerate --finding-counts <json> --fix-cycles <n>` creates `.dev/tasks/to-do/<new-id>/` with a plain exclusive `mkdir` under the id rule of `src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md` (collision also with `.dev/tasks/archive/<id>`), writes `<new-id>.md` with `slug` set to `<new-id>`, `source.md`, and a `return-contract.yaml` at `contract_version: "1.1"` with `supersedes`, `remediation_route`, `finding_counts` and `fix_cycles`; `restore --old-id <id>` moves the archived package back to `to-do/` after a failed placement. Every move uses `rename_noreplace` from `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py`, loaded by file path from the sibling skill directory (`<this skill>/../sc-implement-protocol/scripts/archive_workspace.py`); if that file is missing the command fails closed with a named error and moves nothing. On a platform without `renameat2` it fails closed and moves nothing. Add tests to `tests/skills/test_workflow_remediation.py`.

Acceptance criteria:
- An end-to-end test in a temporary checkout runs prepare, edits the copy, archive, place and checks: the old plan file is byte-identical (same sha256) in `archive/`, the new contract names `supersedes` and `remediation_route: surgical`, and `to-do/` no longer holds the old package.
- Tests show that an id existing in `archive/` makes `place` pick a suffixed id (or fail after `-9`), that an existing archive destination is never overwritten, that a failed `place` followed by `restore` leaves the old package back in `to-do/`, and that a missing sibling helper moves nothing.
- `uv run pytest tests/skills/test_workflow_remediation.py -q` passes.

## Phase 3: Workflow protocol and command

## Task 5: Write the route reference `refs/remediation.md`

Depends on: Task 4

Create `src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` from sections 3, 4 and 6 of `docs/designs/surgical-remediation.md`, corrected by the Constraints: the routing rule table and counting rules (B, H and M from the reflect `finding_counts`), the surgical route as five steps in the owner order (duplicate, edit, archive the original after the Wave 3 gate on the copy, place the new package, re-review) with each step calling the matching `remediate.py` subcommand of Task 4 by the installed path `~/.claude/skills/sc-workflow-protocol/scripts/remediate.py`; the reviser brief (fresh context, Edit tool only, one finding per call, fixmap-v1 block, reuse `~/.claude/rules/prompts/document_review_loop_prompts.md` and name the project copy second); the re-review brief (agent type `reflect-reviewer`, archived original as baseline, `diff -w`, prior blockers decided resolved/open/regressed); the 2-fix-cycle cap with `review_verdict: FAIL` and `open_blockers` on escalation; the regenerate route (new source with blockers to fix and counted findings to avoid, archive only after the new plan passes Wave 3, regenerate at most once per run); the failed-placement undo with `restore`; and the standing archive rule (a replaced package always moves to `archive/` in the same change, with a `SUPERSEDED` line).

Acceptance criteria:
- The file names every `remediate.py` subcommand it uses and each exists in Task 4's script.
- `grep -n 'src/superclaude' src/superclaude/skills/sc-workflow-protocol/refs/remediation.md` prints nothing.
- Every threshold (3, 5, 9) and the cap of 2 fix cycles match the design and `route()`.

## Task 6: Add Wave 4R to the workflow skill

Depends on: Task 5

Edit `src/superclaude/skills/sc-workflow-protocol/SKILL.md`: add `## Wave 4R — Remediate` between Wave 4 and Wave 5 that loads `refs/remediation.md`, reads `finding_counts` from the Wave 4 reflect contract, runs `remediate.py route`, and follows the chosen route; replace the sentence "Advisory and read-only: never edit, delete, or regenerate `<id>.md` from findings, and never change the workflow `status` because of them." in Wave 4 with the bounded rule (the plan is changed only by Wave 4R, only for blocking findings, only on a copy); keep "never overwrite an existing package"; update `## Will / Will Not` (the old "modify the plan from reflect findings" ban becomes "edit a plan in place"); add the Wave 4R file operations (`mktemp`, copy and move through `remediate.py` only). Mirror the file to `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md` and the new ref and script to the same mirror folder if the mirror carries refs and scripts for this skill.

Acceptance criteria:
- Wave 4R sits between the Wave 4 and Wave 5 headings and says the route runs after Wave 4 by default.
- The Wave 4 text no longer contains "never edit, delete, or regenerate" and the Will Not list no longer contradicts Wave 4R.
- `diff -rq` between `src/superclaude/skills/sc-workflow-protocol` and `plugins/superclaude/skills/sc-workflow-protocol` shows no difference; `make sync-dev` then `make verify-sync` is clean.

## Task 7: Update the workflow parse and contract refs

Depends on: Task 5

Edit `src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md`: the "never reuses" sentence of Package identity stays but notes that Wave 4R places a new package and never edits an old one; step 4 (exclusive creation) also tests `.dev/tasks/archive/<id>`; the Bash rule allows exactly the `remediate.py` subcommands, the private `mktemp -d /tmp/sc-workflow-revise.XXXXXXXX` directory and the copy and move they perform, in addition to the package `mkdir` and the single `rm`; add `--remediate none|surgical|regenerate` and `--revise <package-dir> --review <REPORT.md>` to the enums and STOP table (`E-BAD-FLAG` for another value, a `--revise` without `--review` and the reverse). Edit `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`: keep `contract_version: "1.1"`, add the additive fields `remediation_route`, `supersedes`, `superseded_by`, `finding_counts`, `fix_cycles`, `review_verdict` and `open_blockers` with their values and when each is written, and say `reflect_status` records the re-review verdict and scope ("changed lines plus prior blockers") for a replaced package. Update the mirror copies under `plugins/superclaude/skills/sc-workflow-protocol/refs/`.

Acceptance criteria:
- `return-contract.md` still contains `contract_version: "1.1"` and lists all seven new fields.
- `input-parse.md` lists `archive/` in the collision check and both new flags in its enums.
- `diff -rq` against the plugin mirror shows no difference.

## Task 8: Add the flags and Unattended rules to the workflow command

Depends on: Task 6, Task 7

Edit `src/superclaude/commands/workflow.md`: Usage and Options table gain `--remediate none|surgical|regenerate` (default: the route of the routing rule runs after Wave 4; `none` records counts and the chosen route and changes nothing; the other two force a route and are recorded as forced) and `--revise <package-dir> --review <REPORT.md>` (run the route for a package reviewed outside workflow); Behavioral Summary and Boundaries (Will, Will Not) describe the bounded remediation instead of "never edit the plan"; the Unattended section says the surgical route runs without a person, escalation after 2 fix cycles ends the run `partial` with the open blockers in `unresolved` and the last placed package keeps `review_verdict: FAIL`, and nested reflect calls for re-reviews use the next `nested/reflect-<n>/` directory and are listed in `artifacts`. Keep the existing `--unattended` rules and the `E-LEGACY` list unchanged.

Acceptance criteria:
- `grep -n -e '--remediate' -e '--revise' src/superclaude/commands/workflow.md` shows the two flags in Usage, Options and the Unattended section.
- The Boundaries text no longer says plans are never edited from findings.
- `make sync-dev` then `make verify-sync` is clean.

## Phase 4: Implement refusal, reflect hand-off and routing guide

## Task 9: Make /sc:implement refuse a plan with `review_verdict: FAIL`

Edit `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`: in the Detection list (check 2, the sibling contract) add that a contract carrying `review_verdict: FAIL` is refused before any write with STOP `E-MANAGED-REVIEW-FAIL` that prints the `open_blockers` ids from that contract; keep `contract_version: "1.1"`, keep the rule that a plan outside `to-do/` and `done/` (an `archive/` plan included) is refused, and add `E-MANAGED-REVIEW-FAIL` to any STOP list in `src/superclaude/skills/sc-implement-protocol/SKILL.md` that enumerates the managed STOPs. Mirror both files to `plugins/superclaude/skills/sc-implement-protocol/`. Add tests to `tests/skills/test_workflow_remediation.py` that read the markdown and assert the refusal wording, the `E-MANAGED-REVIEW-FAIL` code, the unchanged "1.1" pin in `managed-workspace.md` and in `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py`, and that location resolution still knows only `to-do/` and `done/`.

Acceptance criteria:
- The refusal is described before the ledger step and names `open_blockers`.
- The new static tests pass: `uv run pytest tests/skills/test_workflow_remediation.py tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_task_workspace_smoke.py -q`.
- `diff -rq` between the two implement-protocol folders shows no difference.

## Task 10: Point reflect's plan route at Wave 4R

Depends on: Task 6

Edit `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`: Phase B (the paragraph that says findings never edit the tasklist and a refactor re-runs Phase A as a new package) points at workflow's Wave 4R so one routing rule applies; Phase A step 4 reads the contract of the package workflow reports as final (its `plan_path`), follows `superseded_by` when the contract it read names one, and never emits an archived or `review_verdict: FAIL` plan as `remediation_plan_path` (it emits `null` and surfaces the open blockers); the rule that the plan route archives the package it replaces is stated; the headless-wrapper paragraph says the wrapper runs `/sc:implement` on the final placed package and that a refusal is a non-zero apply that the wrapper already handles fail-closed. `src/superclaude/cli/reflect/runner.py` is read to confirm the claim and is not edited.

Acceptance criteria:
- Phase B and Phase A step 4 name Wave 4R, `superseded_by` and `review_verdict: FAIL`.
- `src/superclaude/cli/reflect/runner.py` is unchanged (`git diff --stat` shows no entry for it).
- `grep -n 'src/superclaude' src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` prints only the existing `runner.py` pointer, if any.

## Task 11: Add the archive rule to the routing guide and its copies

Edit the level 3 row of `src/superclaude/core/HOW-WE-WORK.md` so it says a replaced plan moves to `.dev/tasks/archive/` and a plan that still has blockers is refused by `/sc:implement`; then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and re-run the level-table copy into the block between the `level-table:v1` start marker and the `/level-table` end marker in `src/superclaude/core/CLAUDE.md`, as the project instructions require. Never add the guide as an `@` import.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing.
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py tests/recommend/test_routing_refresh.py -q` passes.

## Task 12: Document the archive folder in `.dev/README.md`

Edit `.dev/README.md`: the Workflow task packages section adds `.dev/tasks/archive/` (superseded packages, never run, deleted only on an explicit owner order), and the bullet "Look in both places" becomes three places (`to-do/` in flight, `done/` finished, `archive/` superseded); mention the surgical and regenerate routes in one sentence each and that `/sc:implement` refuses a plan under `archive/` or one with `review_verdict: FAIL`.

Acceptance criteria:
- The "Look in both places" bullet names all three folders and says a package present in `to-do/` and `archive/` or `done/` is a conflict to resolve by hand.
- `.dev/README.md` contains no sentence that says superseded packages stay in `to-do/`.

## Phase 5: Migrate the superseded packages

## Task 13: Move the seven superseded packages out of `to-do/`

Depends on: Task 4, Task 9, Task 12

Move exactly these seven packages from `.dev/tasks/to-do/` to `.dev/tasks/archive/` using `remediate.py archive` (no `mv`): `TASK-WF-designSpec-20261107-072120`, `TASK-WF-designSpec-20261107-074040`, `TASK-WF-p3Requirements-20261107-065757`, `TASK-WF-removeTheAnyIssu-20261031-235404`, `TASK-WF-removeTheAnyIssu-20261101-225338`, `TASK-WF-removeTheAnyIssu-20261101-225635` and `TASK-WF-removeTheAnyIssu-20261102-042031`. Each moved contract keeps its existing `SUPERSEDED` line and gains the replacement id where its text names one (the p3Requirements contract names `TASK-WF-p3Requirements-20261107-070713`). Do not move `TASK-WF-blockerStage4-20261116-030206` (its own contract carries no SUPERSEDED line; its replacement `TASK-WF-blockerStage4-20261117-170451` says it is superseded) or `TASK-WF-specScRecommendR-20261024-055620` (an intake with no plan); print both as open owner decisions in the task result. Write the list of moved ids and the two open decisions to `./artifacts/migration.md`. Run `git add .dev/tasks` afterwards (staging only).

Acceptance criteria:
- `ls .dev/tasks/to-do` shows none of the seven ids and `ls .dev/tasks/archive` shows all seven, each with its plan, `source.md` and `return-contract.yaml` intact.
- `grep -il 'SUPERSEDED' .dev/tasks/to-do/*/return-contract.yaml` lists only the two packages named above as open owner decisions.
- `./artifacts/migration.md` names the seven moves and the two open decisions.
- `make verify-sync` and `uv run pytest tests/skills tests/core tests/cli/reflect -q` pass.
