---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-implementFrOnb1O-20261023-180618
version: "1"
priority: Medium
created_date: "2026-10-23"
---

# Make /sc:workflow the default planner (FR-ONB.1, Part A)

Source: ./source.md
Goal: Every routing surface (the HOW-WE-WORK guide and its copies, core CLAUDE.md, the /sc:recommend skill and CLI prompt, and the user docs) sends planned work with clear requirements, including many-file and multi-session work, to /sc:workflow then /sc:implement, and reserves /task-builder then /task for large spec-driven builds, exactly as FR-ONB.1 of the spec specifies.

## Constraints

- The authoritative wording for every change is the FR-ONB.1 section of /home/coder/workspaces/IronClaude/.dev/releases/backlog/ironclaude-onboarding-deck/spec.md (approved by the user 2026-10-23). Use its quoted sentences verbatim where it quotes them.
- Line numbers in the spec were taken on master. This worktree is based on PR #285 (branch feature/pr-submit-default-monitor-3), so locate each edit by its quoted text, not by line number.
- Do not change the level 6 route (/prd then /tdd then /roadmap, section 3.1 steps 2-11), the push or merge rules, or anything about pr-submit --monitor (owned by PR #285).
- Out of scope: the onboarding deck (FR-ONB.2 to FR-ONB.7), filing issues, docs/user-guide/commands.md:1345 and docs/user-guide/flags.md:112.
- src/superclaude/core/HOW-WE-WORK.md is the source. plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md must end byte-identical to it, and the block between the level-table markers must be byte-identical in src/superclaude/core/CLAUDE.md.
- Edit src/ and plugins/ only, then run make sync-dev. Never stage or commit any .claude/ path. Do not commit or push.
- Keep the guide ASCII-only (tests/core/test_how_we_work_routing_table.py checks this) and in plain English, matching the guide's existing style.
- Installed primitives must not tell an agent to read anything through a src/superclaude/ path (repo CLAUDE.md rule).
- Plan amended by the operator before Task 1 started (HOW-WE-WORK.md 3.10 allows adding missing requirements to a plan before its first step), from the pre-execution review .dev/reflect/pre-implementFrOnb1O-20261023180800/REPORT.md (merged findings M-001 to M-021; M-012 dropped by the evidence validator). Approval of every FR-ONB.1 bullet, including the level 5 re-point, is recorded in the spec's Open Items table (item 1, RESOLVED 2026-10-23).
- Baseline: uv run pytest tests/core/ tests/commands/test_help_command.py tests/commands/test_routing_plugin_parity.py tests/cli/test_how_we_work_install.py tests/skills/test_sc_recommend_routing_contract.py tests/unit/test_cli_install.py passed (148 tests) on this branch before any edit.
- Every edit to src/superclaude/core/HOW-WE-WORK.md happens in Tasks 1-3, before Task 3's sync step. If any later task changes the guide, it must repeat the byte copy to plugins/, the level-table re-copy into core CLAUDE.md, and make sync-dev.
- This branch is stacked on PR #285. Open its PR only after PR #285 merges, then rebase onto master and re-run the Task 7 test gate.
- Level 3 keeps "--depth quick" as written; whether multi-session level-3 work should use a deeper setting is an open question for the user, not part of this plan.

## Phase 1: Guide wording

## Task 1: Rewrite the level table, tie-break and hard limit in section 1 of the guide

In src/superclaude/core/HOW-WE-WORK.md section 1 ("How much process does this job need?"):

- Replace the sentence "If you are unsure between two rows, choose the heavier one." with the spec's tie-break: "If you are unsure between levels 3 and 4, choose level 3. If you are unsure between any other two rows, choose the heavier one."
- Level 3 row "Use this when" cell: replace with "The work is planned and its requirements are clear, including work that touches many files or takes more than one session. This is the default for any planned change." Keep the rest of the row.
- Level 4 row "Use this when" cell: replace with "You are building a whole project or major component from scratch, from a spec complex enough that it nearly warrants a PRD and TDD, and you or your lead chose the extra time and tokens."
- Level 5 row "What you run" cell: re-point "Then build the task file from it: /task-builder ..." to /sc:workflow "<what to build> as recommended in <path to the report>" (level 3), keeping /task-builder only for level-4-sized work (spec FR-ONB.1, Level 5 bullet).
- Hard limit paragraph: keep the trigger (more than 5 edits or more than one source file), replace "level 3 for a few files with clear scope, level 4 for anything larger, longer, or riskier" with "level 3 by default, level 4 only for the large spec-driven builds described in level 4". Keep the edit definition and the /sc:cleanup exception.

Acceptance criteria:
- The level 3 and level 4 "Use this when" cells contain exactly the spec's quoted sentences.
- grep -n "choose the heavier one" src/superclaude/core/HOW-WE-WORK.md returns only the new tie-break line, which also names the level 3 versus 4 exception.
- grep -n "larger, longer, or riskier" src/superclaude/core/HOW-WE-WORK.md returns nothing.
- Level 5's follow-on step names /sc:workflow as the default and /task-builder only for level-4-sized work.
- The level-table markers are unchanged and still enclose the table and the hard limit.

## Task 2: Re-point the workflow sections (2, 3.1 step 1, 3.2, 3.4, 3.6, 3.7, 3.8, 3.11) and add section 3.13

Depends on: Task 1

In src/superclaude/core/HOW-WE-WORK.md, apply each "Routes that currently go to task-builder" bullet of spec FR-ONB.1 that falls in sections 2 and 3:

- Section 2 "strong request" example: rewrite the /task-builder "Add per-tenant rate limits as recommended in ..." example as the /sc:workflow form, and change the matching weak-request cell `/task-builder "add rate limits"` to `/sc:workflow "add rate limits"`.
- 3.3 step 2 heading/wording "A few files with clear scope": reword so it matches the new level 3 (planned change with clear requirements, including many files or more than one session).
- 3.1 step 1 and the 3.6 brainstorm table row: where they say --handoff task builds a task file, say that when no PRD is needed you run /sc:workflow <path to merged-requirements.md>, and keep --handoff task only for level-4-sized work. Leave 3.1 steps 2-11 unchanged.
- 3.2: steps 3-5 become /sc:workflow <spec file> then /sc:implement on the printed plan path, then the 3.11 ship step. Move the current task-file walk-through text of 3.2 steps 3-5 (--spec, reflect_pre, Open Questions, /task, reflect_post) into a new section "### 3.13 Build and run a task file (level 4)" placed after 3.12, keeping its instructions intact. Give 3.13 a one-sentence intro that stands on its own (when to use it: level 4 only), and keep its references to 3.1 ("the note at the end of 3.1", "3.1 step 9") and 3.11 valid.
- 3.4: correct step 1's --fix description and its trigger wording ("larger or riskier than a few files with clear scope") to match src/superclaude/commands/troubleshoot.md (--fix offers a sc:workflow plan you run with /sc:implement; --fix --depth deep builds a task file). In step 3, keep 3b and 3c as distinct routes: 3b is a clear fix that needs a short plan, `/sc:workflow "<fix>" --depth quick`; 3c is a riskier or multi-session fix, `/sc:workflow "Fix the root cause described in <REPORT.md path> ..."` at its default depth; /task-builder only for level-4-sized fixes. Both 3b and 3c then run `/sc:implement` on the printed plan path. Reword the "a few files" wording in step 3 to match.
- 3.7 step 3: large refactors go to /sc:workflow <spec> by default; its cross-reference "(3.2)" becomes "(3.2; for level-4-sized refactors, 3.13)".
- 3.8: "put them in the spec and the task file (3.2)" becomes "put them in the spec and the plan (3.2)".
- 3.11 step 4: replace "offers to plan fixes as a task file" with the actual default from src/superclaude/commands/auggie-review.md (--remediation-offer row): it offers /sc:design then sc:workflow, with /sc:implement run by you; task-builder only with --depth deep.

Acceptance criteria:
- A heading "### 3.13 Build and run a task file (level 4)" exists after 3.12 and contains the walk-through moved from 3.2 (reflect_pre, Open Questions, /task, reflect_post).
- Section 3.2 names /sc:workflow and /sc:implement for building the feature and no longer instructs /task-builder by default.
- 3.4, 3.7, 3.8 and 3.11 step 4 match the bullets above; 3.4 and 3.11 descriptions agree with troubleshoot.md and auggie-review.md.
- 3.1 steps 2-11 (the /prd, /tdd, /roadmap route) are byte-unchanged except for any cross-reference that pointed into moved 3.2 text.
- Section 2's weak and strong rate-limit examples both use /sc:workflow.
- 3.4 step 3 names 3b (--depth quick) and 3c (default depth) as distinct /sc:workflow routes that both end in /sc:implement.
- grep -n "few files" src/superclaude/core/HOW-WE-WORK.md: every remaining hit is listed with a one-line justification in ./artifacts/t2-few-files.log.

## Task 3: Update sections 4 and 5, Other commands and the routing table, then sync the copies

Depends on: Task 2

In src/superclaude/core/HOW-WE-WORK.md:

- Section 4: add the agent rule bullet with its exemption, verbatim from spec FR-ONB.1 ("Never choose /task-builder or /task as the planner on your own ... runs them as one of its own steps.").
- Section 5 mix-up row "/sc:workflow + /sc:implement and /task-builder + /task" and the Other commands /sc:spawn row: reword so /sc:workflow is the default and /task-builder is for the level-4 case.
- Routing table rows:
  - simple-plan intent becomes phrases matching the new level 3 (for example "planned change; clear requirements; many files; more than one session").
  - task-file intent matches the new level 4 without any bare "spec" phrase (for example "whole project built from scratch; major component built from scratch; nearly needs a PRD and TDD"), because /sc:recommend prefers the row whose phrase names an artifact (sc-recommend SKILL.md:58) and a request that names a spec must not land on level 4; its section column points to "1, 3.13".
  - feature-existing: intent gains a spec-naming phrase (for example "spec file exists"); steps become /sc:workflow <spec file> then /sc:implement on the printed plan path; level 3; mandatory_flags set to `-` (the "3: --spec <spec file>" entry is removed; /sc:workflow has no --spec flag).
  - research-first: step 2 uses /sc:workflow "<what to build> as recommended in <report path>" with /task-builder kept for level-4-sized work; step 3 becomes /sc:implement on the printed plan path (/task only after a /task-builder step 2).
  - shape-idea: notes no longer send no-PRD work to --handoff task by default; they point to /sc:workflow on the merged requirements, --handoff task only for level-4-sized work.
  - bug: 3b and 3c both use /sc:workflow (3b with --depth quick, 3c at default depth), /task-builder only for level-4-sized fixes; step 4 reads "only after 3b or 3c"; keep the mandatory-flag label "3b: --depth quick" pointing at step 3b; reword the notes' "a few files with clear scope" clause.
- No routing row may pair /sc:workflow with /task.

Then sync the copies:

- Copy src/superclaude/core/HOW-WE-WORK.md byte-for-byte to plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md.
- In src/superclaude/core/CLAUDE.md: re-copy the block between the level-table markers from the guide, replace the "choose the heavier one" sentence (in "How to choose a workflow") with the new tie-break, and add the agent rule with its exemption as a plain paragraph in "How to choose a workflow", outside the level-table markers, with no new "## " heading between the block and the ~/.claude/HOW-WE-WORK.md pointer paragraph (tests/core/test_claude_md_routing_block.py slices at the first "## " after the block). The file must not contain "make sync-dev".
- Run make sync-dev.

Acceptance criteria:
- cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md reports no difference.
- Routing row feature-existing has level 3 and mandatory_flags `-`; routing row task-file's section column names 3.13 and its intent contains no bare "spec" phrase.
- research-first step 3 and bug step 4 run /sc:implement after a /sc:workflow step; no routing row pairs /sc:workflow with /task.
- For each re-pointed route (3.2, 3.4, 3.7, 3.11, level 5, shape-idea, bug, research-first), the prose section and its routing row name the same commands, recorded one line per route in ./artifacts/t3-consistency.log.
- The agent rule with its exemption appears in HOW-WE-WORK.md section 4 and in src/superclaude/core/CLAUDE.md.
- uv run pytest tests/core/ tests/commands/test_help_command.py tests/commands/test_routing_plugin_parity.py tests/cli/test_how_we_work_install.py passes; output saved to ./artifacts/t3-tests.log.

## Phase 2: /sc:recommend and user docs

## Task 4: Apply the tie rule and hard limit to the /sc:recommend skill and its references

Depends on: Task 3

- src/superclaude/skills/sc-recommend/SKILL.md: in the "Match the goal to one routing row" step, change "take the row with the higher level (the guide's rule: when unsure between two rows, choose the heavier one)" so a tie between a level-3 row and a level-4 row picks the level-3 row and other numeric ties still pick the higher level. Replace both hard-limit sentences ("level 3 ... for a few files with clear scope, level 4 ... for anything larger, longer, or riskier") with the new wording "level 3 by default, level 4 only for the large spec-driven builds described in level 4".
- src/superclaude/skills/sc-recommend/SKILL.md: where a level 1 or 2 match breaks the hard limit and the skill offers "simple-plan (level 3) or task-file (level 4)" as equal choices (and the matching "level 3 or 4" wording earlier in the file), make simple-plan the default and task-file only for level-4-sized builds.
- src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md: same hard-limit replacement, and align its "level 3 or 4" wording the same way.
- Copy src/superclaude/skills/sc-recommend/SKILL.md and src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md byte-for-byte over their plugins/superclaude/skills/sc-recommend/ copies (tests/commands/test_routing_plugin_parity.py compares the whole folder byte-for-byte).
- Run make sync-dev.

Acceptance criteria:
- grep -rn "larger, longer, or riskier" src/superclaude/skills plugins/superclaude/skills returns nothing.
- The tie step in both SKILL.md copies picks level 3 over level 4.
- cmp reports no difference between each edited src file and its plugins/ copy.
- Walking the request "Add CSV export to the invoices list; touches 6 files; spec at docs/specs/x.md" through the SKILL.md match rules against the edited routing table selects a level-3 row; the walk-through is written to ./artifacts/t4-recommend-walk.md.
- uv run pytest tests/skills/test_sc_recommend_routing_contract.py tests/commands/test_routing_plugin_parity.py tests/unit/test_cli_install.py passes; output saved to ./artifacts/t4-tests.log.

## Task 5: Update the /sc:recommend CLI prompt

Depends on: Task 4

In src/superclaude/cli/recommend/prompts.py:

- Replace the hard-limit sentence in the PHASE-1 block ("level 3 (/sc:workflow --depth quick then /sc:implement) for a few files with clear scope, level 4 (/task-builder then /task) for anything larger, longer, or riskier") with the new wording, keeping the command names.
- Reword the task-file-generation key description so plan requests are not steered to /task-builder (for example: a full task file for a large spec-driven build; /task-builder then /task). Keep the key name, because the key list is closed.
- Keep the classifier example "Build a tasklist for this spec at docs/specs/checkout-v2-spec.md" -> task-file-generation byte-for-byte unchanged: it is a verbatim eval request (see the comment above the examples). Change only the key description.

Acceptance criteria:
- grep -n "larger, longer, or riskier" src/superclaude/cli/recommend/prompts.py returns nothing.
- The closed key list and the classifier examples are unchanged.
- grep -n "few files" src/superclaude/cli/recommend/prompts.py returns nothing.
- uv run pytest tests/ -k "recommend" -q passes; output saved to ./artifacts/t5-tests.log.

## Task 6: Align the user docs with the new default planner

Depends on: Task 3

Edit these lines (located by text; numbers are from master) to the new level wording, the corrected --fix route, and the default-planner wording, as listed in the spec FR-ONB.1 "User docs outside the guide" bullet:

- docs/user-guide/commands.md: line 43 (/sc:workflow summary "Short checked plan for a few files (level 3)"), 70 (/sc:troubleshoot "--fix adds a task file you run with /task"), 294 (/sc:pm "multi-file work to /task-builder then /task"), 456 (/sc:roadmap "for the default planning route use /roadmap" becomes "for the default roadmap route"), 506 (/sc:spawn), 551 (/sc:task), 695 (/sc:workflow "A few files with clear scope that fit in one or two sessions (level 3)"), 806 (/sc:implement "more than one session or many files"), 927 (/sc:improve large refactor).
- docs/user-guide/session-management.md: line 125 ("larger work goes through a task file").

Acceptance criteria:
- Each listed line now matches the guide after Tasks 1-3.
- Re-running grep -rnE "task-builder|task file|level 4|few files|one or two sessions|many files|default planning" docs/user-guide/ docs/getting-started/ README.md shows no line that sends multi-file, multi-session or large-refactor planned work to /task-builder by default, calls /roadmap the default planning route, or says --fix adds a task file by default; output saved to ./artifacts/t6-sweep.log.

## Task 7: Add the regression test and changelog entry

Depends on: Task 5, Task 6

- In tests/core/test_how_we_work_routing_table.py add a test that scans every .md and .py file under src/ and plugins/ and fails if any line contains "choose the heavier one" without the level 3 versus 4 exception, or contains "larger, longer, or riskier"; and fails if the guide's level 4 row "Use this when" cell lists "many files" or "more than one session" as a trigger. Put the checks in a helper that takes text, so the failure case can be proven on a text fixture.
- Add a CHANGELOG.md entry describing the default-planner change, following the file's existing format.
- Record the manual follow-up for the user in ./artifacts/t7-manual-check.md: in a fresh Claude session, run `/sc:recommend "Add CSV export to the invoices list; touches 6 files; spec at docs/specs/x.md"` and confirm it recommends /sc:workflow, not /task-builder.

Acceptance criteria:
- The new test passes on the edited files, and the helper fails on a text fixture containing the old tie-break sentence and on one containing "larger, longer, or riskier" (shown in ./artifacts/t7-regression.log). The real guide is never reverted.
- grep -rn "larger, longer, or riskier" src/ plugins/ returns nothing; output saved to ./artifacts/t7-tests.log.
- ./artifacts/t7-manual-check.md exists with the exact command and expected result.
- uv run pytest tests/core/ tests/commands/test_help_command.py tests/commands/test_routing_plugin_parity.py tests/cli/test_how_we_work_install.py tests/skills/test_sc_recommend_routing_contract.py tests/unit/test_cli_install.py passes and make verify-sync passes; output saved to ./artifacts/t7-tests.log.
- grep -rn "choose the heavier one" src/ plugins/ returns only lines that also carry the level 3 versus 4 exception.
