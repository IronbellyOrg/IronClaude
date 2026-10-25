# Remove the `--depth deep` MDTM route from the /sc:auggie-review remediation chain

Issue: IronbellyOrg/IronClaude#263. Supersedes the stale plan on branch `docs/auggie-review-workflow-implement-plan` (written against commit cbdbb826; the default plan route has since landed).

Goal: `/sc:auggie-review` has ONE remediation route for every `--depth`: `/sc:design` -> `sc:workflow` (with its built-in `/sc:reflect --mode pre`) -> user-run `/sc:implement` -> `/sc:reflect --mode post`. No `task-builder`, `/task`, `BUILD_REQUEST`, MDTM, `--type task`, `--analyze` or `--validate` reference remains in the auggie-review command, protocol skill, or refs.

## Constraints

- Edit only under `src/superclaude/`. Run `make sync-dev` afterward. Never stage any `.claude/` path (only `.claude/settings.json` is tracked).
- Do NOT change the plan route text that already exists (the `remediation-workflow-source.md` build, `--depth standard --handoff none`, never `--handoff implement`, never `--output`, the `.dev/tasks/to-do/<id>/<id>.md` package, `baseline_ref`, the `--task-log` Phase E command). Only remove the deep/MDTM branches and the words that exist to distinguish routes.
- `--depth deep` itself stays a valid review depth. Only its remediation route changes: deep now uses the same chain as `quick` and `standard`.
- Keep verbatim: the `--remediation-offer` table row start (`| \`--remediation-offer\` | \`true\` |`), `quick` in the `--depth` row, `prism-b` in the `--auggie-model` row, and `--model "${AUGGIE_MODEL:-prism-b}"` in SKILL.md (pinned by `tests/pr_submit/test_static_grep.py`).
- Intentional residual hits of "task": the Claude Code subagent `Task` tool (`src/superclaude/agents/auggie-reviewer.md` line 14, `src/superclaude/commands/auggie-review.md` the `**Task**` line, `SKILL.md` line 4 `allowed-tools` and the `Task` mention near line 193), the `--task-log` and `--tasklist` flags, and "per-task" acceptance wording about plan tasks.
- Out of scope, do not touch: `src/superclaude/commands/troubleshoot.md`, `src/superclaude/core/HOW-WE-WORK.md` and its plugin mirror, `src/superclaude/commands/reflect.md`, the `task-builder` skill itself, frozen `.dev/eval-workspaces/**`.
- Locate edits by quoted text, not line numbers; lines shift as earlier tasks edit a file.

## Phase 1: Command file

## Task 1: Single-route remediation in `src/superclaude/commands/auggie-review.md`

Edit these spots:
- The `--remediation-offer` table row: remove the sentence "With `--depth deep`, `task-builder` -> `/task` (and `/sc:reflect --type task --analyze|--validate`) replaces the workflow/implement pair". Keep the chain text before it.
- Heading "### Default remediation chain (plan route)": rename to "### Remediation chain". Leave its body as is.
- Delete the whole section "### Deep review with MDTM remediation chain" and its code block.
- Will bullet "Offer the `/sc:design` -> `sc:workflow` -> `/sc:reflect` -> `/sc:implement` remediation chain after the report posts (`task-builder` -> `/task` only when `--depth deep`), gated on user confirmation": remove the parenthetical.
- Related Commands, the `/sc:reflect` bullet: remove "; `--type task --analyze|--validate` on the MDTM route" and the "Plan route:" label (it is the only route).
- Related Commands: delete the "`task-builder` skill" bullet.

Acceptance criteria:
- `grep -inE 'task-builder|mdtm|/task\b|--type task|--analyze|--validate|plan route|BUILD[_-]REQUEST' src/superclaude/commands/auggie-review.md` returns no lines.
- The `--remediation-offer` row still starts with `| \`--remediation-offer\` | \`true\` |`.
- The only case-insensitive "task" hits left are the `**Task**` tool line and lines containing `workflow` tasklist wording such as "tasklist package".

## Phase 2: Protocol skill

## Task 2: Single-route remediation in `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`

Depends on: Task 1

Edit these spots:
- Wave 5 step 3: change "name the route (plan, or mdtm when `--depth deep` was requested), and ask one yes/no question" to "and ask one yes/no question".
- Wave 5 step 4: change the lead-in so it no longer selects a route from `--depth` (one route for every depth; keep the pointer to `refs/remediation-handoff.md`).
- Phase B: drop the "plan route ->" label and delete "; MDTM route -> invoke the `task-builder` skill with a BUILD_REQUEST citing the remediation spec (file path passed as input)".
- Phase C: drop the label and delete "; MDTM route -> `/sc:reflect --type task --analyze` against the new task file".
- Phase D: drop "(plan route) or `/task <path>` (MDTM route)"; keep `/sc:implement <pkg>/<id>.md` and "the skill does NOT auto-execute".
- Phase E: drop "(plan route; ...)" label wording but keep the `<pkg-now>` explanation and the full `/sc:reflect --mode post ...` command; delete "or `/sc:reflect --type task --validate` (MDTM route)".
- Will Do bullet: remove "; with `--depth deep`, `task-builder` -> `/task` replaces the workflow/implement pair".
- Will Not Do bullet: "`/sc:reflect --type task --validate` is the final gate" becomes "`/sc:reflect --mode post` is the final gate".
- Error Handling row "Task-builder skill not available": replace with "`sc:workflow` unavailable | Surface the remediation spec path and stop; do not fail the whole review | None".

Acceptance criteria:
- `grep -inE 'task-builder|mdtm|/task\b|--type task|--analyze|--validate|BUILD[_-]REQUEST' src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` returns no lines.
- The text still says "five phases", still forbids `--handoff implement`, and still says the skill does not auto-execute.
- `--model "${AUGGIE_MODEL:-prism-b}"` is unchanged.

## Phase 3: Remediation handoff reference

## Task 3: Collapse routing and offer text in `refs/remediation-handoff.md`

Depends on: Task 2

In `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`:
- Replace the "Route selection" section (table keyed on `--depth`) with a short paragraph: every review depth, including `deep`, uses the same chain (`sc:workflow-protocol` on the remediation spec produces `.dev/tasks/to-do/<id>/<id>.md` and runs `/sc:reflect --mode pre` itself; the user runs `/sc:implement`). Keep the sentence that explains why `sc:workflow` sits between the spec and `sc:implement` (a design spec is prose and would collapse to one task). Retitle the section so it is not about route selection.
- In the verbatim offer prompt: remove every `[plan route]` / `[mdtm route]` label and the two-line mdtm alternatives (`task-builder`, `--type task --analyze`, `/task <path>`, `--type task --validate`); delete the line "Route for this review: <plan | mdtm> ...". Keep the five phases, the `/sc:implement <pkg>/<id>.md` command, and the closing reply instructions.
- Phase A rationale: "`sc:workflow` / the task-builder can consume" becomes "`sc:workflow` can consume".

Acceptance criteria:
- The offer prompt block has no route labels and no `mdtm`, `task-builder`, `/task`, `--analyze`, or `--validate`.
- The file no longer contains a table with a `deep` row pointing at MDTM.
- The offer is still a single free-form message (anti-pattern note about AskUserQuestion unchanged).

## Task 4: Delete the MDTM branch of Phases B, C, D, E in `refs/remediation-handoff.md`

Depends on: Task 3

- Retitle "## Phase B (plan route) - `sc:workflow`" to "## Phase B - `sc:workflow`". Delete the entire "## Phase B (mdtm route, `--depth deep`) - `task-builder` skill" section (natural-language paragraph, `> Skill task-builder` snippet, BUILD_REQUEST block, BUILD-REQUEST file write, completion bullets).
- Phase C: delete the "**MDTM route:**" block (the `/sc:reflect --type task --analyze` command, the Serena `think_about_task_adherence` quote, and the "pre-execution sanity check" prose). Remove the "**Plan route (consume, do not re-run):**" label but keep its content. Keep the sanity-check questions only if reworded to plan terms (are acceptance criteria strong enough to detect failure, scope-drift risk, rollback/abort path, explicit dependencies); rename "reflect-analyze" to "the pre-execution review" and the refactor bullet must re-run Phase B (not `task-builder`), same 2-cycle cap. Remove "The rest of this phase ... applies to both routes."
- Phase D: surface text keeps `/sc:implement <pkg>/<id>.md`; delete the `/task <task-file-path>` line and the "(plan route; a TASK-WF package never goes to /task)" aside. Replace "the task file" wording with "the tasklist".
- Phase E: keep the `/sc:reflect --mode post ...` command and its `<pkg-now>`/`baseline_ref` explanation; drop "on the plan route" and delete the "or `/sc:reflect --type task --validate` on the MDTM route" alternative and the quoted v1 `--validate` sentence. Reword the checks to "were all tasklist tasks completed" and "do the completed artifacts satisfy each task's acceptance criteria".

Acceptance criteria:
- `grep -inE 'task-builder|BUILD[_-]REQUEST|MDTM|/task\b|--type task|--analyze|--validate|think_about_task|reflect-analyze|reflect-validate|task file' src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md` returns no lines, except the `task_file_path` line in the Resumability JSON and the `reflect-analyze` wording in the Anti-patterns list, which Task 5 owns (plan correction made during execution: Task 5 runs after Task 4, so the whole-file grep can only be clean after Task 5).
- There is exactly one Phase B section.
- The Phase B refactor loop still caps at 2 cycles and the plan-route text about `remediation-workflow-source.md`, `--handoff none`, and `return-contract.yaml` is unchanged.

## Task 5: Resumability keys and anti-pattern wording in `refs/remediation-handoff.md`

Depends on: Task 4

- In the `remediation-state.json` example: remove `task_file_path`; rename `task_reflect_analyze_result` to `reflect_pre_result` and `task_reflect_validate_result` to `reflect_post_result`; drop the "(plan route; ...)" qualifier on `plan_path` (keep the absolute-path hint). Add one sentence: a state file with the older key names (`task_file_path`, `task_reflect_*`) is treated as having no Phase B artifact and the chain restarts at Phase B.
- Anti-patterns: "The reflect-analyze pass is cheap" becomes "The pre-execution review is cheap".

Acceptance criteria:
- The JSON example parses (`python -c` with `json.loads` on the extracted block, or a manual check) and lists `plan_path`, `reflect_pre_result`, `reflect_post_result`.
- `grep -inE 'task_file_path|task_reflect|reflect-analyze|reflect-validate' src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md` matches only the one sentence that names the old keys.

## Phase 4: Sync and final gate

## Task 6: Sync mirrors, residual check, tests

Depends on: Task 5

From the repo root run `uv run` for Python and `make` for sync:
1. `make sync-dev` then `make verify-sync` (must exit 0). Do not stage `.claude/`.
2. `grep -rinE 'task-builder|BUILD[_-]REQUEST|MDTM|/task\b|--type task|--analyze|--validate|reflect-analyze|reflect-validate' src/superclaude/commands/auggie-review.md src/superclaude/agents/auggie-reviewer.md src/superclaude/skills/sc-auggie-review-protocol` must return no lines except the single old-key sentence from Task 5.
3. `uv run pytest tests/pr_submit tests/commands/test_auggie_review_revagent.py tests/core/test_how_we_work_routing_table.py tests/cli/reflect/test_remediation_route_table.py tests/cli/reflect/test_remediation_source_template.py -q`. Any failure must be reported by test name with its reason, never hidden. The known pre-existing failure is the missing `src/superclaude/hooks/scripts/offer-pr-review.sh` that two pr_submit tests expect; any other failure must be shown to be unrelated to the edited files, or fixed if the edit caused it.
4. `git status --short` shows no staged path beginning with `.claude/` other than `.claude/settings.json`.

Acceptance criteria:
- `make verify-sync` exits 0.
- The residual grep is clean as described.
- The listed pytest files pass, or every failure is named with evidence that it is unrelated to the edited files.
