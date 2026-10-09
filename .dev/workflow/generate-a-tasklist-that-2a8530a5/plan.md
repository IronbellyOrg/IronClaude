---
schema: workflow-plan/1.1
source: .dev/workflow/generate-a-tasklist-that-2a8530a5/source.md
strategy: systematic
depth: standard
slug: generate-a-tasklist-that-2a8530a5
version: "1"
priority: Medium
created_date: "2026-10-09"
---

# Refactor /sc:auggie-review remediation chain to /sc:workflow and /sc:implement

Source: .dev/workflow/generate-a-tasklist-that-2a8530a5/source.md
Goal: No `task-builder`, `/task`, `--type task`, BUILD_REQUEST, or MDTM reference remains in the /sc:auggie-review command, skill, or refs; the remediation chain runs `/sc:design`, `/sc:workflow`, `/sc:reflect --mode pre`, `/sc:implement`, `/sc:reflect --mode post`.

## Constraints

- Edit only under `src/superclaude/`. The `.claude/` mirrors regenerate with `make sync-dev`; never stage `.claude/` paths (only `.claude/settings.json` is tracked).
- Target chain, used verbatim everywhere: Phase A `/sc:design <REVIEW.md path> --type architecture --format spec --output <output_dir>/remediation-spec.md` (unchanged); Phase B `/sc:workflow <output_dir>/remediation-spec.md --handoff none`; Phase C `/sc:reflect --mode pre --spec <output_dir>/remediation-spec.md --tasklist <plan.md>`; Phase D user runs `/sc:implement <plan.md>`; Phase E `/sc:reflect --mode post --diff <output_dir>/remediation.diff --tasklist <plan.md>`.
- Intentional residual hits of "task" are only: the Claude Code subagent `Task` tool (`src/superclaude/agents/auggie-reviewer.md` L14, `src/superclaude/commands/auggie-review.md` L88, `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` L4 and L183) and the external `/sc:reflect` flag `--tasklist`.
- Never pass `--handoff implement` to `/sc:workflow`; Phase D stays user-run and the skill never auto-executes.
- Pinned by `tests/pr_submit/test_static_grep.py`: the `--remediation-offer` table row, `quick` in the `--depth` row, `prism-b` in the `--auggie-model` row, and `--model "${AUGGIE_MODEL:-prism-b}"` in SKILL.md. Do not alter these.
- Line numbers below are from the working tree on 2026-10-09 and shift as earlier tasks edit a file; locate by the quoted text if they drift.
- Non-goals: `src/superclaude/commands/reflect.md` mentions of task-builder and /task (L101, 137, 206, 275, 285), the missing `src/superclaude/hooks/scripts/offer-pr-review.sh` that two pr_submit tests expect, and the frozen `.dev/eval-workspaces/sc-auggie-review/**` artifacts.

## Phase 1: Command file

## Task 1: Update the remediation option row and remove the stray line in the command

In `src/superclaude/commands/auggie-review.md`, rewrite the description cell of the `--remediation-offer` row (L52) so the chain reads `/sc:design` → `/sc:workflow` → `/sc:reflect --mode pre` → `/sc:implement` → `/sc:reflect --mode post`. Delete the stray line `co` at L60 (uncommitted typo under "Behavioral Flow"), restoring the blank line before the list of command-file duties.

Acceptance criteria:
- The row still begins with `| \`--remediation-offer\` | \`true\` |` so the lookup in `tests/pr_submit/test_static_grep.py` (L291) still matches.
- L60 no longer contains `co`; a blank line separates "The command file performs only:" from the duty list.
- The `--remediation-offer` row contains neither `task-builder` nor `--type task`.

## Task 2: Update examples, boundaries, and related commands in the command

Depends on: Task 1

In `src/superclaude/commands/auggie-review.md`: change the example prompt at L101 to "Run /sc:design → /sc:workflow → /sc:reflect chain on these findings?". In the "Deep review with full remediation chain" example (L135–138) replace the four chain comment lines: `/sc:workflow <remediation-spec> --handoff none` producing a phased plan.md; `/sc:reflect --mode pre --spec <spec> --tasklist <plan>` as the plan sanity check; "User sign-off OR re-run /sc:workflow" leading to `/sc:implement <plan.md>`; `/sc:reflect --mode post --diff <diff> --tasklist <plan>` as pre-commit validation. Change the Will bullet at L150 to name `/sc:design` → `/sc:workflow` → `/sc:reflect`. Change the Related Commands bullet at L166 to `/sc:reflect --mode pre|post` (pre-execution and post-execution gates), replace the `task-builder` skill bullet at L167 with a `/sc:workflow` bullet (produces a phased plan.md between `/sc:design` and execution), and add a `/sc:implement` bullet (user-run executor of that plan). Leave the `**Task**` tool line at L88 unchanged.

Acceptance criteria:
- `grep -inE 'task-builder|--type task|MDTM|/task\b' src/superclaude/commands/auggie-review.md` returns no lines.
- The only remaining case-insensitive "task" hits in the file are L88 (`**Task**` tool) and lines containing `--tasklist`.
- Related Commands lists both `/sc:workflow` and `/sc:implement`.

## Phase 2: Protocol skill

## Task 3: Rewrite remediation Phase B through E in the protocol skill

In `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, Wave 5 step 3 and step 4 (L322–331). L324: change "four phases" to "five phases". L327 Phase B: append a "Remediation Context" section (goal, why, files cited in Critical and High findings) to `<output-dir>/remediation-spec.md`, then invoke `/sc:workflow <output-dir>/remediation-spec.md --handoff none`; capture the printed plan path and confirm the `return-contract.yaml` beside it reports `status: success`. L328 Phase C: after `/sc:workflow` returns, invoke `/sc:reflect --mode pre --spec <output-dir>/remediation-spec.md --tasklist <plan.md>`. L329: replace "reflect-analyze" and "tasklist" with "reflect pre-execution" and "plan". L330 Phase D: before handing off, record `base_sha` from `git rev-parse HEAD`; wait for explicit user sign-off; the user runs `/sc:implement <plan.md>` and the skill does NOT auto-execute. L331 Phase E: after the user signals completion, write `<output-dir>/remediation.diff` containing `git diff <base_sha>` plus, for each untracked file from `git ls-files --others --exclude-standard`, `git diff --no-index /dev/null <file>`; then invoke `/sc:reflect --mode post --diff <output-dir>/remediation.diff --tasklist <plan.md>` BEFORE the user commits, blocking on validation failures. Do not touch the `Task` entry in `allowed-tools` (L4) or the `Task` tool mention at L183.

Acceptance criteria:
- Step 3 says "five phases".
- Phases B through E contain the exact commands from the Constraints section and no occurrence of `task-builder`, `BUILD_REQUEST`, `/task`, `--type task`, or "task file".
- Phase E states that `remediation.diff` includes untracked files and that `base_sha` is recorded before Phase D.
- The skill still states it never auto-executes and never passes `--handoff implement`.

## Task 4: Rewrite the remediation wording in Will Do, Will Not Do, and Error Handling

Depends on: Task 3

In `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`: L345 (Will Do) becomes "`/sc:design` → `/sc:workflow` → `/sc:reflect`-pre → `/sc:implement` → `/sc:reflect`-post". L355 (Will Not Do) names `/sc:reflect --mode post` as the final gate before the user commits manually. The Error Handling row at L368 becomes "`/sc:workflow` unavailable | Surface the remediation spec path and stop; do not fail the whole review | None".

Acceptance criteria:
- `grep -inE 'task-builder|Task-builder|--type task|reflect-analyze|reflect-validate|BUILD_REQUEST' src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` returns no lines.
- The only remaining case-insensitive "task" hits in SKILL.md are L4, L183, and lines containing `--tasklist`.
- The `--model "${AUGGIE_MODEL:-prism-b}"` string pinned by `tests/pr_submit/test_static_grep.py` is unchanged.

## Phase 3: Remediation handoff reference

## Task 5: Rewrite the offer prompt and the Phase A rationale

Depends on: Task 4

In `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`: rewrite the verbatim offer prompt Phase B through E entries (L28–36) to: Phase B `/sc:workflow <spec> --handoff none` (produces a phased plan.md with evidence-backed steps); Phase C `/sc:reflect --mode pre --spec <spec> --tasklist <plan.md>` (sanity-checks the plan before execution; flags scope drift, weak verification criteria, missing rollback); Phase D user-driven execution of the plan (the skill does NOT auto-execute; you run `/sc:implement <plan.md>`); Phase E `/sc:reflect --mode post --diff <remediation.diff> --tasklist <plan.md>` (final gate before commit; blocks if validation fails). At L59 change "the task-builder can consume" to "/sc:workflow can consume".

Acceptance criteria:
- The offer prompt block names `/sc:workflow`, `/sc:reflect --mode pre`, `/sc:implement <plan.md>`, and `/sc:reflect --mode post` and contains no `task-builder` or `/task`.
- The offer remains a single free-form message, not an AskUserQuestion form (anti-pattern at the end of the file unchanged).
- L59 mentions `/sc:workflow`, not the task-builder.

## Task 6: Rewrite the Phase B section for /sc:workflow

Depends on: Task 5

In `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`, replace the whole "Phase B — `task-builder` skill" section (L68–100) with "Phase B — `/sc:workflow`". Delete the paragraph claiming the skill is invoked via natural language because it is not a slash command (L70–75, including the `> Skill task-builder` snippet). Delete the BUILD_REQUEST block (GOAL, WHY, WHERE, BUILD_REQUEST file at L80–92) and the `BUILD-REQUEST-REMEDIATION.md` file write (L94). Replace with: before invoking, append a "Remediation Context" section (goal, why, files cited in Critical and High findings) to `<output_dir>/remediation-spec.md` because `/sc:workflow` accepts exactly one source; invoke `/sc:workflow <output_dir>/remediation-spec.md --handoff none` and never `--handoff implement`; explain that `plan.md` lands under `.dev/workflow/<slug>/` (the `--output` flag must stay under `.dev/workflow/`), so capture the plan path from the printed output and confirm `return-contract.yaml` beside it reports `status: success`. On completion, surface the plan path with a one-line summary and proceed to Phase C unless the user says stop.

Acceptance criteria:
- The Phase B heading and body contain no `task-builder`, `BUILD_REQUEST`, `BUILD-REQUEST`, `MDTM`, or "natural language" paragraph.
- The section states the single-source rule, the `.dev/workflow/<slug>/` plan location, and the `status: success` check.
- The section forbids `--handoff implement`.

## Task 7: Rewrite the Phase C section for /sc:reflect --mode pre

Depends on: Task 6

In `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`, rewrite the Phase C section (L102–125). The heading and command become `/sc:reflect --mode pre --spec <output_dir>/remediation-spec.md --tasklist <plan.md>`. Delete the sentence about Serena's `think_about_task_adherence` and `think_about_collected_information` tools (L112, a description of the old v1 reflect) and describe it as the UC-1 pre-execution coverage and gap audit of the plan against the remediation spec. Reword the sanity-check questions (L114–119) to plan terms: are the Acceptance criteria of each plan task strong enough to detect failure, are there scope-drift risks beyond the review findings, is there a rollback or abort path, are dependencies explicit through `Depends on:` lines. Reword L123–124 to "refactor the plan". Change L125 so the refactor loop re-runs `/sc:workflow` with the reflect concerns appended to the spec's Remediation Context section, then re-runs Phase C, capped at 2 refactor cycles.

Acceptance criteria:
- Phase C contains no `--type task`, `--analyze`, `think_about_task_adherence`, `task-builder`, "task file", "tasklist" prose, or "task items".
- The refactor loop re-runs `/sc:workflow` and keeps the 2-cycle cap.
- The only "task" substring left in the section is inside `--tasklist`.

## Task 8: Rewrite Phase D and Phase E sections for /sc:implement and reflect --mode post

Depends on: Task 6

In `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`, rewrite Phase D (L127–142): the surfaced message reads "Plan validated. Ready to execute." with "Run: /sc:implement <plan-path>", note that the executor keeps its progress ledger at `.dev/implement/<slug>/progress.md` and resumes implicitly, keep the rationale and the `remediation_status: in_progress` fallback, and record `base_sha` from `git rev-parse HEAD` before handing off. Rewrite Phase E (L144–164): heading and command become `/sc:reflect --mode post --diff <output_dir>/remediation.diff --tasklist <plan.md>`; describe writing `remediation.diff` as `git diff <base_sha>` plus, for each untracked file listed by `git ls-files --others --exclude-standard`, `git diff --no-index /dev/null <file>`; replace the quoted v1 reflect sentence at L152 with a description of the UC-2 post-execution deviation audit; reword the checks at L156–157 to "were all plan tasks completed" and "do the completed artifacts satisfy each plan task's Acceptance criteria". Do not use `--task-log` unless the executor first confirms in `src/superclaude/skills/sc-reflect-protocol/refs/input-resolution.md` that the `/sc:implement` ledger is an accepted input; default to `--diff` only.

Acceptance criteria:
- Phases D and E contain no `/task`, `--type task`, `--validate`, "task file", or the old quoted v1 sentence.
- Phase E documents how `remediation.diff` is built, including untracked files, and that `base_sha` is recorded in Phase D.
- Phase D names `/sc:implement <plan-path>` and the ledger path, and still says the skill does not auto-execute.

## Task 9: Update resumability state keys and the Phase C anti-pattern wording

Depends on: Task 8

In `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`, update the `remediation-state.json` example (L166–186): rename `task_file_path` to `plan_path`, `task_reflect_analyze_result` to `reflect_pre_result`, `task_reflect_validate_result` to `reflect_post_result`, and add `base_sha` and `diff_path` under `artifacts`. Add one sentence that a state file written by the older key names should be treated as having no Phase B artifact and restarted at Phase B. At L191 change "The reflect-analyze pass" to "The reflect pre-execution pass".

Acceptance criteria:
- `grep -inE 'task_|reflect-analyze|reflect-validate' src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md` returns no lines.
- The JSON example is valid JSON and lists `plan_path`, `reflect_pre_result`, `reflect_post_result`, `base_sha`, and `diff_path`.
- Whole-file check: `grep -inE 'task-builder|BUILD[_-]REQUEST|MDTM|/task\b|--type task' src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md` returns no lines, and every remaining case-insensitive "task" hit is inside `--tasklist`.

## Phase 4: Sync and final gate

## Task 10: Sync mirrors and run the residual and pinning checks

Depends on: Task 9

From the repo root run `make sync-dev` then `make verify-sync` so `.claude/commands/sc/auggie-review.md`, `.claude/skills/sc-auggie-review-protocol/`, and `.claude/agents/auggie-reviewer.md` match `src/superclaude/`. Do not stage any `.claude/` path.

Acceptance criteria:
- `make verify-sync` exits 0.
- `grep -rinE 'task|BUILD[_-]REQUEST|MDTM' src/superclaude/commands/auggie-review.md src/superclaude/agents/auggie-reviewer.md src/superclaude/skills/sc-auggie-review-protocol` returns only the four `Task` tool lines (auggie-reviewer.md L14, auggie-review.md L88, SKILL.md L4 and L183) and lines containing `--tasklist`; there is zero hit for `task-builder`, `/task`, `--type task`, `reflect-analyze`, or `reflect-validate`.
- `uv run pytest tests/pr_submit/test_static_grep.py -v` passes (or fails only on the pre-existing missing `offer-pr-review.sh` source, which is recorded as unchanged in the Constraints non-goals).
- `git status --short` shows no staged path beginning with `.claude/` other than `.claude/settings.json`.
