<!-- /sc:issue feature template (complex) -->

> **Corrected 2026-11-18 (Clay's decision, relayed by GeneralIronFlow).** `/sc:task`, `sc-task-protocol`, `/sc:validate-tests`, `sc-validate-tests-protocol` and the suite `task_classification_contract` are **kept**: `/sc:task` was never on Clay's list, and the earlier line that it came from "Ryan's list" could not be verified. The six agents `rf-analyst`, `rf-assembler`, `rf-task-builder`, `rf-task-executor`, `rf-task-researcher` and `rf-team-lead` are **kept in 6.1.0**; their future is issue 572's research. PR 2 is withdrawn (#652 closed) and decision D2 is dropped. Removed in 6.1.0: 9 skills, 1 command and 1 eval suite.

## Feature Summary

Remove the task and documentation bundle from IronClaude in release 6.1.0 (Part B of #571, Clay's decision 6.3): 9 skills, 1 command and 1 eval suite go (the `/sc:task` family and the six `rf-*` agents stay); every route that offered the task-file (MDTM) route points at `/sc:workflow` then `/sc:implement`; an upgrade of an installed 6.0.0 removes the shipped files. Four pull requests into `integration` (PR 1, 3, 4, 5; PR 2 is withdrawn), never master. This issue is the map, the retention record, the plan and the decisions for Clay.

## Problem Statement

#571 asks for a dependency map of the bundle before anything is removed. The map shows the bundle is a closed group: the six documentation skills (`prd`, `tdd`, `tech-research`, `tech-reference`, `operational-guide`, `readme`) and `roadmap` each have a Stage A that builds a task file with `task-builder` (`prd` and `tdd` spawn the `rf-task-builder` agent directly) and a Stage B that runs `/task` (for example `prd/SKILL.md:143-168,414-416`, `readme/SKILL.md:172-206,643-656`, `tech-reference/SKILL.md:14,165-199,564-573`). Removing only the skills Clay named would leave `prd`, `readme` and `tech-reference` unable to run, and the routing guide, reflect, troubleshoot, brainstorm, crash-recovery and recommend text still offering routes that no longer exist.

## User Story

As the maintainer preparing 6.1.0, I want the bundle removed in reviewable pull requests with every reference re-pointed, so that IronClaude names only what it still ships and an upgraded install drops the removed files.

## Proposed Solution

All paths and line numbers are in the map: [dependency-map.md](https://github.com/IronbellyOrg/IronClaude/blob/clayphi/v61-part-b-map/.dev/cleanup/bundle/dependency-map.md). Companion files: [retention.md](https://github.com/IronbellyOrg/IronClaude/blob/clayphi/v61-part-b-map/.dev/cleanup/bundle/retention.md), [reference-index.md](https://github.com/IronbellyOrg/IronClaude/blob/clayphi/v61-part-b-map/.dev/cleanup/bundle/reference-index.md) (every file outside the bundle that names a bundle item, with line numbers), and the plan [TASK-WF-planThe610Remova-20261118-170805](https://github.com/IronbellyOrg/IronClaude/blob/clayphi/v61-part-b-map/.dev/tasks/to-do/TASK-WF-planThe610Remova-20261118-170805/TASK-WF-planThe610Remova-20261118-170805.md) (19 tasks in 5 phases). Branch with the files: `clayphi/v61-part-b-map` (no pull request).

### What each item is, and the verdict

| Kind | Item | Verdict | Why |
|---|---|---|---|
| skill | `task`, `task-builder`, `tdd`, `tech-research`, `operational-guide`, `roadmap` | remove | Clay's list |
| skill | `prd`, `readme`, `tech-reference` | remove | cannot run without `task` and `task-builder` (Stage A and B above) |
| command | `/sc:tdd` | remove | Clay's list |
| command + skill | `/sc:task` and `sc-task-protocol` | **keep** (corrected) | never on Clay's list (the "Ryan's list" line is unverified); a separate thing from the MDTM `/task` (compliance tiers); nothing in `task` or `task-builder` uses it, so keeping it blocks nothing |
| command + skill | `/sc:validate-tests` and `sc-validate-tests-protocol` | **keep** (corrected) | they validate `/sc:task` tiers and stay with it |
| agent | `rf-analyst`, `rf-assembler`, `rf-task-builder`, `rf-task-executor`, `rf-task-researcher`, `rf-team-lead` | **kept, issue 572 decides** (corrected) | Clay: their future is issue 572's research; any text that names them stays valid |
| agent | `rf-qa`, `rf-qa-qualitative` | keep (issue 572 decides) | `/sc:reflect` uses both as Wave 3B reviewers (`commands/reflect.md:172`, `sc-reflect-protocol/SKILL.md:632-633`); the eval suite `agent_grounding_drift` watches them; their text is left unchanged |
| eval | suite `workflow_vs_task_builder` with `scripts/eval_workflow_vs_task_builder.py` | remove | it compares against `/task-builder`; the eval harness itself stays |
| eval | suite `task_classification_contract` | **keep** (corrected) | it tests `/sc:task`, which stays |

### Every removal, one per line (for Clay)

Skills (9): `src/superclaude/skills/prd/`; `src/superclaude/skills/tdd/`; `src/superclaude/skills/tech-research/`; `src/superclaude/skills/tech-reference/`; `src/superclaude/skills/operational-guide/`; `src/superclaude/skills/readme/`; `src/superclaude/skills/task/`; `src/superclaude/skills/task-builder/`; `src/superclaude/skills/roadmap/`.

- remove skill `prd` (6 files)
- remove skill `tdd` (6 files)
- remove skill `tech-research`
- remove skill `tech-reference`
- remove skill `operational-guide`
- remove skill `readme`
- remove skill `task`
- remove skill `task-builder`
- remove skill `roadmap`
- remove command `/sc:tdd` (`commands/tdd.md`)
- remove eval suite `workflow_vs_task_builder.yaml` with `scripts/eval_workflow_vs_task_builder.py` and its companion test
- kept (corrected, not removed): `/sc:task`, `sc-task-protocol`, `/sc:validate-tests`, `sc-validate-tests-protocol`, suite `task_classification_contract`, and the six agents `rf-analyst`, `rf-assembler`, `rf-task-builder`, `rf-task-executor`, `rf-task-researcher`, `rf-team-lead`
- remove docs `docs/guides/prd-skill-release-guide.md`, `docs/guides/tdd-skill-release-guide.md`, `docs/reference/nfr-conv-2-prose-determinism.md`
- remove behavior: `/sc:brainstorm --handoff task`; the MDTM route of `/sc:reflect --remediate --depth deep` and `/sc:troubleshoot --fix --depth deep` (both now take the plan route); levels 4, 5 and 6 of the routing guide (the scale ends at level 3)

### Retention: where every removed item stays retrievable

Three copies compared (read only; nothing was edited in IronFlow or the fork): IronClaude `integration` `847cccc1a` (tree identical to master `3f3b34a26`), the snapshot fork `ironbelly/IronClaudeV5` (master `d4d1662a8`, 2026-11-14), and IronFlow (`/home/coder/workspaces/IronFlow`, `.claude/skills|commands/sc|agents`). All 10 removed items exist in all three. The fork equals IronClaude for the removed items except the task-builder skill, changed after the snapshot (#582, #632). IronClaude is newer in every item by date (IronClaude 2026-11-08 to 11-17, IronFlow 2026-06-23 to 10-19). IronFlow's copy of the main file is an older untouched IronClaude version in 6 items and has IronFlow-only edits in the other 4 (marked "own edits"), so for those neither copy contains the other. Full table, the commit list and how to retrieve: [retention.md](https://github.com/IronbellyOrg/IronClaude/blob/clayphi/v61-part-b-map/.dev/cleanup/bundle/retention.md).

**The `v6.0.0` tag (`3f3b34a26`) holds the latest version of every removed item**, newer than the fork snapshot and than IronFlow (all 10 items exist at that tag, checked with `git cat-file -e`). Restore a file with `git show v6.0.0:<path>` or `git checkout v6.0.0 -- <path>`, for example `git checkout v6.0.0 -- src/superclaude/skills/task-builder`.

| Item | IronClaude last | IronFlow last | IronFlow copy | IronClaude-only commits (count newer than that version) |
|---|---|---|---|---|
| skill task | 2026-11-09 | 2026-10-19 | own edits (5 lines vs IC@17bab85b9 2026-07-05) | 6 |
| skill task-builder | 2026-11-17 | 2026-10-19 | own edits (63 lines vs IC@17bab85b9 2026-07-05) | 10 |
| skill tdd | 2026-11-12 | 2026-06-23 | own edits (461 lines vs IC@a9cf7ee3e 2026-04-02) | 8 |
| skill tech-research | 2026-11-12 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 6 |
| skill operational-guide | 2026-11-09 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 3 |
| skill roadmap | 2026-11-09 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 3 |
| skill prd | 2026-11-08 | 2026-06-23 | own edits (471 lines vs IC@a9cf7ee3e 2026-04-02) | 6 |
| skill readme | 2026-11-09 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 3 |
| skill tech-reference | 2026-11-12 | 2026-06-23 | identical to IC@17bab85b9 (2026-07-05) | 6 |
| command tdd | 2026-11-12 | 2026-06-23 | identical to IC@021f715cd (2026-05-27) | 4 |

IronClaude-only changes for Clay to port to IronFlow if wanted (themes; commit subjects in retention.md): the review rule (`80f934de5`, `f90aca51a`, `b681ace43`, `64e8eacf2`, `002eaa8b7`), unattended mode (`2327fbd37`), tool grants and names (`ed6074c47`, `077f9dd38`, `156f28292`), codegraph in place of the old memory servers (`2f10a0e1e`, `75d0d1e2c`, `3ae238b17`, `046a03ab4`), path and routing hygiene (`3fcb54175`, `5c6a7d919`, `051f39fea`, `c6009cd3f`), reflect integration (`2323f7cbb`, `5495ba286`), the `prd` and `tdd` `refs/` packs (`f787fef94`, `763e0c58c`, `09e2ccc0d`, `234355941`, `2219545cc`; IronFlow has no `refs/` folders) and `af5fb69eb` (6.0.0 cleanup). For the four "own edits" items (task, task-builder, tdd, prd) the commit list is an upper bound. Not claimed to be in IronFlow: every IronFlow copy differs from IronClaude's.

### The PR split (order is fixed; each merges into `integration` before the next starts; PR 2 is withdrawn)

| PR | Removes | Edits outside (main files) | Tests |
|---|---|---|---|
| 1 documentation skills | `prd`, `tdd`, `tech-research`, `tech-reference`, `operational-guide`, `readme`, `/sc:tdd`, two release guides (15 + 1 + 2 files) | routing guide rows 5 and 6 and 40 other lines, its plugin copy, `core/CLAUDE.md` level table, `WORKER-CONTRACT.md` (example, list, row), onboarding deck, brainstorm `--research deep`, reflect Wave 1B, crash-recovery PRD/TDD/research sections, recommend refs and fixtures | `test_review_severity_rule`, `test_review_prompt_overrides` file lists, recommend tests, install baseline lists, worker contract |
| 2 withdrawn (Clay, 2026-11-18) | nothing: `/sc:task`, `sc-task-protocol`, `/sc:validate-tests` + skill and suite `task_classification_contract` stay; #652 closed | none | none |
| 3 re-point the MDTM routes | nothing deleted | reflect command, protocol and handoff ref; reflect wrapper `runner.py:583-596,769-783` always `/sc:implement`; troubleshoot (command, skill, 7 refs); brainstorm `--handoff` becomes `none\|design`; issue chains; crash-recovery; recommend | `tests/cli/reflect/*`, `tests/troubleshoot/*` |
| 4 delete the MDTM pair and roadmap | `task`, `task-builder`, `roadmap`, suite `workflow_vs_task_builder` with script and test, nfr reference | level 4 of the guide, recommend text, `rules/core/ib_agent_core.md` (`/task` section), deck, project index | delete `test_task_builder_merge.py` and the audit cases that read the task-builder skill; the cases that read the `rf-*` agents stay |
| 5 retire step, version, changelog | nothing | `install_retired_data.py` regenerated with `--tag v5.0.0 --tag v6.0.0`, version 6.1.0 in `pyproject.toml` and `__init__.py`, `CHANGELOG.md`, `docs/releases/v6.1.0.md`, `docs/getting-started/upgrading.md` | retire-step tests gain the 6.1.0 names and an upgrade from the `v6.0.0` tag |

Routes that point at `/task` today are re-pointed in PR 3: reflect and troubleshoot (`--remediate` and `--fix` always offer the `sc:workflow` plan that the user runs with `/sc:implement`), brainstorm (`--handoff task` removed), recommend (examples and level text, PRs 1 and 4), crash-recovery (PRD, TDD, research, roadmap and MDTM sections removed; its `/sc:workflow` section stays), issue chains (MDTM wording removed). PR 3 stacks on PR 1; PR 2 is withdrawn.

### Gates (every PR)

Full suite as `.github/workflows/test.yml` runs it. Baseline on `847cccc1a`: **22691 passed, 10 failed, 70 skipped, 1 xpassed** (the 10: eight in `tests/unit/test_ccsession_tag.py`, `tests/cli/eval/test_schema_validate.py::test_rejection_does_not_write_to_default_scratch_root`, `tests/hooks/test_launch_level_guard.py::test_speed_large_commands[backslash-lines-64KB]`; `tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files` is order dependent). 0 new failures; the pass count drops only by the removed tests, both numbers in the PR body; `make lint`; `uv run ruff format --check src/ tests/`; `make sync-dev` then `make verify-sync`; `git diff --check`; `superclaude install` into a throwaway HOME then `superclaude doctor`; a clean search for the removed names (excluding `.dev/`, the historical records, `src/superclaude/templates/` and the allow-list below). Then `/sc:pr-submit --monitor 3 --repo IronbellyOrg/IronClaude` with base `integration`; each PR stops when green, both reviewers finished and no thread open.

A trial removal (all bundle files of the first scope deleted, nothing else edited; measured before the scope change) already ran the full suite: 148 failed and 101 errors in 27 test files, each from a missing file (table in map section 9), 238 fewer passes. More tests fail only after the text edits (routing-table pins, onboarding deck, reflect wrapper tests); they are in the plan.

## Acceptance Criteria

- [ ] PRs 1, 3, 4 and 5 are merged into `integration`; each shows 0 new test failures against the baseline above, a pass-count drop equal to its removed tests, and a clean search for its removed names
- [ ] None of the 9 skills, 1 command or 1 eval suite above exists in `src/superclaude/`, `plugins/superclaude/` or the legacy root `commands/` folder; `/sc:task`, `sc-task-protocol`, `/sc:validate-tests`, `sc-validate-tests-protocol`, the suite `task_classification_contract` and all eight `rf-*` agents still exist
- [ ] `HOW-WE-WORK.md`, its plugin copy, `WORKER-CONTRACT.md` and `core/CLAUDE.md` describe only what is still installed; the level scale ends at level 3
- [ ] `/sc:reflect --remediate`, `/sc:troubleshoot --fix` and `superclaude reflect run --fix` take only the plan route (`/sc:workflow` then `/sc:implement`); `/sc:brainstorm --handoff` accepts `none|design`
- [ ] An upgrade of an installed 6.0.0 (throwaway HOME, `superclaude update` then `superclaude doctor`) leaves none of the removed commands or skills installed, keeps an edited copy with the printed reason, and leaves the `/sc:task` family and every `rf-*` agent installed
- [ ] Version 6.1.0 in `pyproject.toml` and `src/superclaude/__init__.py`; `CHANGELOG.md` and `docs/releases/v6.1.0.md` list every removal above with its replacement or "none"
- [ ] Clay has the list of IronClaude-only changes to port to IronFlow (retention.md); IronFlow was not edited

## Out of Scope

IronFlow edits; the release PR from `integration` to master, the tag and the gate G1 to G9 (GeneralIronFlow and Clay); issue 572's decision on all eight `rf-*` agents; the 52 installed templates (decision D5; they name removed skills in 585 lines but are shared and pinned by tests); the MDTM conventions and `/rf:` namespace text in `src/superclaude/rules/` other than `ib_agent_core.md`; the eval harness itself; the historical records (`docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, `CHANGELOG.md` past entries, `.dev/`, `docs/memory/`, `docs/generated/`, root `POST-REFLECT-TASK.md`).

## Components Affected (from `/sc:analyze`)

Read-only pass with codegraph and `git grep` at `847cccc1a`; 221 files outside the bundle name a bundle item (164 without template and fixture files) (index in reference-index.md). Main areas: `src/superclaude/core/{HOW-WE-WORK,CLAUDE,WORKER-CONTRACT}.md` and the plugin copy of the guide; `src/superclaude/commands/{reflect,troubleshoot,brainstorm,recommend,implement,workflow}.md`; skills `sc-reflect-protocol`, `sc-troubleshoot-protocol`, `sc-brainstorm-protocol`, `sc-crash-recovery`, `sc-recommend`, `sc-issue-protocol`, `sc-implement-protocol`, `sc-workflow-protocol`; `src/superclaude/cli/reflect/{runner,commands,config,models,contract,panel_lint}.py` (`_apply_remediation` has one caller, `run`, by codegraph); `src/superclaude/cli/recommend/prompts.py`; `src/superclaude/cli/eval/suites/`; `src/superclaude/rules/core/ib_agent_core.md`; `src/superclaude/hooks/scripts/launch-level-guard.sh` (kept, see D4); `src/superclaude/cli/install_retired_{data,files}.py`; `docs/` (user guide, developer guide, onboarding deck); about 30 test files. No Python module imports a bundle item; the bundle is Markdown that the installers copy.

## Related Issues/PRs

#571 (parent; Part B and the flow), #572 (rf agents; decides the future of all eight `rf-*` agents), #573 (source findings on these skills; used as input: the `rf-task-builder` direct dependency of `prd` and `tdd`, and that `/sc:implement` is not a drop-in executor for existing task files), the 6.0.0 removals merged into `integration` (#615 to #640).

## Success Metrics

After 6.1.0: a search of the shipped sources (excluding the allow-list and historical records) finds none of the removed names; the throwaway-HOME upgrade check passes; `/sc:help` lists no removed command; the suite baseline is 22691 minus the removed tests with the same 10 known failures.

## Architecture Impact

No code module changes except the reflect wrapper (it always launches `/sc:implement <plan>`; the contract field `remediation_task_path` stays in the schema, never written) and the generated retire data. The routing level scale shrinks from six levels to three. The retire step (6.0.0) is reused unchanged; its data is regenerated from both tags.

## Dependencies

Clay's answers to the decisions below (defaults apply if no answer). Order: PR 1, 3, 4, then 5 after all merge (PR 2 withdrawn). `integration` already contains master (tree identical, confirmed by GeneralIronFlow).

### Decisions applied by default (Clay may overrule before the PR that uses them starts)

| # | Decision | Default | PR |
|---|---|---|---|
| D1 | `prd`, `readme`, `tech-reference` | removed with the bundle | 1 |
| D2 | dropped (Clay, 2026-11-18): `/sc:task`, `/sc:validate-tests` and their skills stay | none | none |
| D3 | all eight `rf-*` agents | kept in 6.1.0; issue 572 decides | none |
| D4 | launch-level guard and the issue prohibition lists keep `task` and `/task` as deny-list entries | kept: a customized copy kept by the retire step, or IronFlow's own `task` skill, can still be started by an agent; dropping `task` from the guard's class list (`launch-level-guard.sh:409`) would let it start without the worktree-level stop | 3, 4 |
| D5 | the 52 installed templates | kept; follow-up issue | none |
| D6 | what replaces levels 5 and 6 | scale ends at level 3; research-first points at `/sc:analyze`, `/sc:research`, `/sc:brainstorm` | 1, 4 |
| D7 | the eval suite `workflow_vs_task_builder` | removed; the harness and `task_classification_contract` stay | 4 |
| D8 | removed flag value and routes | `/sc:brainstorm --handoff task`; the MDTM route of reflect and troubleshoot; listed as breaking | 3 |
| D9 | version | 6.1.0 (decision 6.3). `changelog_maintenance.md` treats a removed command or skill as breaking, which is a major version; 6.0.0 followed that | 5 |

The clean-search allow-list (D4): `launch-level-guard.sh` and its plugin mirror, `tests/hooks/test_launch_level_guard.py`, and the issue prohibition lists (`commands/issue.md:97`, `sc-issue-protocol/SKILL.md:189`, `templates/launch-prompt.md`, `cli/issue_pipeline/brief.py:8` with their tests).

## Testing Strategy

Per PR: the gate above. The upgrade test for the retire step installs the `v6.0.0` tag into a throwaway HOME (the real `~/.claude` is never touched), runs `superclaude update`, then `doctor` and `install --list`. The reflect wrapper tests assert the apply prompt starts with `/sc:implement` for every depth.

## Documentation Needs

`docs/user-guide/{commands,flags,brainstorm,codegraph,session-management}.md`, `docs/developer-guide/` examples, `docs/guides/{reflect-cli-tools-guide,suites-guide}.md`, the onboarding deck (checked against the guide by a test), `docs/getting-started/upgrading.md` (a 6.1.0 section), `docs/releases/v6.1.0.md`, `CHANGELOG.md`.

## Alternatives Considered

One large PR (fewer rebases, but a 70-file deletion plus about 160 edits that the two reviewers cannot review well). Removing only Clay's named items (leaves `prd`, `readme` and `tech-reference` unable to run). Removing any `rf-*` agent now (that is #572's decision). Removing the 52 templates now (mixed ownership; the retire step cannot remove an installed template).

## Impact Analysis (Blast Radius, Integration Impact)

- Blast Radius: every user who runs `/task`, `/task-builder`, `/tdd`, `/prd`, `/readme`, `/tech-research`, `/tech-reference`, `/operational-guide` or `/roadmap`; in-flight MDTM task files under `.dev/tasks/to-do/TASK-*` cannot be resumed with `/task` after the upgrade (`/sc:implement` accepts spec and task inputs but does not invoke `/task`; #573). Handling is text only: the release notes and upgrading doc say finish or park them, or resume in IronFlow.
- Integration Impact: reflect, troubleshoot, brainstorm, recommend, crash-recovery, issue, implement and workflow text; the reflect command-line wrapper; the onboarding deck; the install retire data; plugin copies; the Coder pin (outside this repo).

## Risks & Mitigation

- Tests that pin the removed text fail only after edits: the plan lists them, the trial removal found 27 files, the gate compares against the baseline.
- Launch-level guard: removing `task` from it would be a safety regression: kept (D4).
- Retire step removes a file a user still relies on: it removes only byte-identical shipped files (the 6.0.0 rule) and keeps edited copies with the printed reason.
- The `rf-*` agents name `task-builder` and `tech-research` in a few places (`rf-qa` lines 84, 309, 339, 349 and the same in `rf-qa-qualitative`): left unchanged for issue 572; `tests/audit/` cases that read the task-builder skill are deleted, the ones that read the agents stay.
- A reviewer asks for the templates to go: answered by D5 and the follow-up issue.
- The advisory `/sc:reflect --mode pre` of the plan was not run (reflect's reviewers are sub-agents; this session works without them). The plan passed the workflow gate and a path pre-check.

## Effort Estimate (hours) and Complexity

- Effort Estimate (hours): 25 (PR 1: 6, PR 3: 7, PR 4: 6, PR 5: 3, plus monitoring; PR 2 withdrawn)
- Complexity: complex (about 30 files deleted, about 150 edited, about 20 test files known to break, several pinned routing tables)

<!-- sc:issue:create template=issue-feature-complex -->

