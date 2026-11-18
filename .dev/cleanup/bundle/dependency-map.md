# Dependency map: remove the task and documentation bundle (6.1.0, issue 571 Part B)

Measured 2026-11-18 on branch `clayphi/v61-part-b-map` at `847cccc1a` (head of `origin/integration`; its tree is identical to `origin/master` `3f3b34a26`, the 6.0.0 release commit: `git diff origin/integration origin/master` is empty, confirmed by GeneralIronFlow). Read-only: codegraph (`codegraph_status`, `codegraph_node` on `cli/reflect/runner.py`, `codegraph_callers` on `_apply_remediation`), `git grep` over the whole tree, a full-suite baseline and a full-suite trial removal (section 9). Companion files in this folder: `retention.md` (where every removed item stays retrievable) and `reference-index.md` (every file outside the bundle that names a bundle item, with line numbers, generated).

> **Corrected 2026-11-18 (Clay's decision, relayed by GeneralIronFlow).** Wherever this map says a thing is removed, the following are **kept in 6.1.0** instead: `/sc:task` (`commands/task.md`, the plugin copy, the legacy `commands/sc-task.md`) and `sc-task-protocol`; `/sc:validate-tests` and `sc-validate-tests-protocol`; the suite `task_classification_contract`; and the six agents `rf-analyst`, `rf-assembler`, `rf-task-builder`, `rf-task-executor`, `rf-task-researcher`, `rf-team-lead` (issue 572 decides their future; text that names them stays as it is, so the seven `rf-qa`/`rf-qa-qualitative` lines are not reworded). `/sc:task` was never on Clay's list; the "Ryan's list" line that named it could not be verified. PR 2 is withdrawn (#652 closed), D2 is dropped. Still removed: 9 skills (`prd`, `tdd`, `tech-research`, `tech-reference`, `operational-guide`, `readme`, `task`, `task-builder`, `roadmap`), 1 command (`/sc:tdd`), 1 suite (`workflow_vs_task_builder` with its script and test), the nfr reference, level 4 and the task-file routes. Rows below that still say otherwise are the first scope and are superseded by this note.

Historical records, NOT edited (same rule as 6.0.0): `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries, `.dev/`, `docs/memory/`, `docs/generated/` (CLI pipeline artifacts).

## 0. The bundle, and what the map decides

| Kind | Item | Verdict | Why (evidence) |
|---|---|---|---|
| skill | `task` (MDTM executor, `/task`) | remove | Clay's list |
| skill | `task-builder` (MDTM task-file builder) | remove | Clay's list |
| skill | `tdd`, `tech-research`, `operational-guide`, `roadmap` | remove | Clay's list |
| skill | `prd`, `readme`, `tech-reference` | **remove** | Each has a Stage A that builds a task file with `task-builder` (`prd` and `tdd` spawn the `rf-task-builder` agent directly) and a Stage B that runs `/task`: `prd/SKILL.md:143-168,414-416`, `readme/SKILL.md:172-206,643-656`, `tech-reference/SKILL.md:14,165-199,564-573`. Without `task` and `task-builder` they cannot run, so they go with the bundle. |
| command | `/sc:tdd` (`commands/tdd.md`, activates the `tdd` skill) | remove | Clay's list |
| command | `/sc:task` (`commands/task.md`) and skill `sc-task-protocol` | **keep (corrected)** | Not on Clay's list. A different thing from the MDTM `/task` skill: it classifies a request into a compliance tier (STRICT, STANDARD, LIGHT, EXEMPT). Nothing in `task` or `task-builder` uses it (matrix below), so keeping it blocks no removal. |
| command + skill | `/sc:validate-tests` and `sc-validate-tests-protocol` | **keep (corrected)** | They validate `/sc:task` tier classification and stay with it. |
| agent | `rf-analyst`, `rf-assembler`, `rf-task-builder`, `rf-task-executor`, `rf-task-researcher`, `rf-team-lead` | **keep (corrected): issue 572 decides** | Clay's decision. The first-scope evidence (only `rf-task-builder` in the reflect MDTM route, `sc-reflect-protocol/SKILL.md:847`, `refs/remediation-handoff.md:116-120`, which PR 3 removes) stays valid. Text that names these agents is left unchanged. |
| agent | `rf-qa`, `rf-qa-qualitative` | **keep for now (issue 572 decides)** | `/sc:reflect` uses both as Wave 3B reviewers: `commands/reflect.md:172` (tool grant), `sc-reflect-protocol/SKILL.md:632-633,1466`, `refs/remediation-handoff.md:144`; the eval suite `agent_grounding_drift.yaml:4-37` watches both; `spec-panel.md:262` names rf-qa. Seven lines name removed siblings and are edited (section 4). |

Internal references among the bundle (mentions of the row item inside the column item's files; `grep -rP` over `src/superclaude/skills/<column>`):

| Mentioned item | in `task` | `task-builder` | `tdd` | `prd` | `tech-research` | `tech-reference` | `operational-guide` | `readme` | `roadmap` | `sc-task-protocol`+`commands/task.md` |
|---|---|---|---|---|---|---|---|---|---|---|
| `/task` | 4 | 9 | 15 | 13 | 16 | 13 | 14 | 17 | 19 | 1 |
| `task-builder` | 2 | 33 | 6 | 6 | 9 | 10 | 8 | 8 | 40 | 0 |
| `tdd`, `prd`, `readme`, `operational-guide` | 0 to 1 | 0 to 2 | 0 to 1 | 0 to 1 | 0 to 1 | 0 to 1 | 0 to 10 (own) | 0 to 1 | 0 to 2 | 0 |
| `rf-*` agents (six removed) | 10 | 43 | 28 | 29 | 36 | 31 | 35 | 34 | 25 | 0 |

Reading: the six documentation skills and `roadmap` reference each other almost never (0 to 2 mentions), and all of them lean on `task` and `task-builder` (6 to 40 mentions each). `sc-task-protocol` is independent of the MDTM pair.

Consequence for the order: remove the documentation skills first (leaves), then re-point the routes that offer MDTM (PR 3), then delete `task`, `task-builder` and `roadmap` (PR 4). The `/sc:task` family and the six agents stay (PR 2 withdrawn). See the plan.

## 1. Files deleted (tracked) and mirrors

| Group | Files | Count |
|---|---|---|
| Documentation skills | `src/superclaude/skills/prd/` (SKILL.md + 5 refs), `tdd/` (SKILL.md + 5 refs), `tech-research/SKILL.md`, `tech-reference/SKILL.md`, `operational-guide/SKILL.md`, `readme/SKILL.md` | 15 |
| `/sc:tdd` | `src/superclaude/commands/tdd.md` (no plugin copy; checked with `git ls-files plugins`) | 1 |
| `/sc:task` family (kept, corrected) | `src/superclaude/commands/task.md`, `plugins/superclaude/commands/task.md`, `commands/sc-task.md`, `src/superclaude/skills/sc-task-protocol/`: not deleted | 0 |
| `/sc:validate-tests` family (kept, corrected) | `src/superclaude/commands/validate-tests.md`, `src/superclaude/skills/sc-validate-tests-protocol/`: not deleted | 0 |
| MDTM pair and roadmap | `src/superclaude/skills/task/SKILL.md`, `task-builder/SKILL.md`, `roadmap/SKILL.md` | 3 |
| Agents (kept, corrected) | `src/superclaude/agents/rf-{analyst,assembler,task-builder,task-executor,task-researcher,team-lead}.md`: not deleted; issue 572 decides | 0 |
| Eval | `src/superclaude/cli/eval/suites/workflow_vs_task_builder.yaml`, `scripts/eval_workflow_vs_task_builder.py`, `tests/cli/eval/test_workflow_vs_task_builder_companion.py` (`task_classification_contract.yaml` is kept, corrected) | 3 |
| Docs | `docs/guides/prd-skill-release-guide.md`, `docs/guides/tdd-skill-release-guide.md`, `docs/reference/nfr-conv-2-prose-determinism.md` (about task-builder output) | 3 |
| Tests | see section 9 | about 20 |

Untracked mirror (never staged): `.claude/{skills,commands/sc,agents}/<same names>`; `make sync-dev` copies but does not delete, so delete the stale copies by hand before running tests (done in the trial, section 9). The plugin mirror holds only `commands/task.md` of the bundle.

Not in the tree (nothing to do): root `skills/` and `agents/` hold no bundle item; `plugins/superclaude/skills` holds none.

## 2. Routing guide, level table, worker contract (installed core docs)

| Path:line | Change |
|---|---|
| `src/superclaude/core/HOW-WE-WORK.md:9-24` (level table, rows 4, 5, 6 at 18-20) | PR 1 removes rows 5 (research first, `/tech-research`) and 6 (full specification, `/prd` then `/tdd`); PR 4 removes row 4 (task-file work). The scale ends at level 3. Re-pointing text for research-first: `/sc:analyze` (code), `/sc:research` (web), `/sc:brainstorm` (feasibility), then level 3. |
| `HOW-WE-WORK.md:26,34,43-45,53-95,102,112,139,148,189-194,208,232-235,245,286-290,299,320,340-344,355,363` | Rewrite each mention. Rows `/tech-research`, `/task-builder`, `/tech-reference`, `/prd`, `/tdd`, `/operational-guide`, `/readme`, the "document-built" and "technical-design-document" routes (355, 363), the conditional roadmap steps (79-87), the `/task` resume bullet (232) and the comparison rows (286-290, 299) are deleted; shared sentences (26, 112, 139, 208, 235) lose the MDTM branch. |
| `src/superclaude/core/CLAUDE.md:71-88` (copy of the level table between `<!-- level-table:v1 -->` markers) | Same edits; per the repo rule copy the table from the guide byte for byte after editing (tests check both). |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Byte-identical copy of the guide (checked with `cmp`): copy after every guide edit. |
| `src/superclaude/core/WORKER-CONTRACT.md:304-307,330,334,349` | The unattended worked example (304-307) uses `/sc:tdd "auth"` in the T1 and T2 briefs; line 330 lists the "11 commands converted in P2" and names `task` and `tdd` among them; line 334 repeats "the 11 commands"; the table row at 349 is `/sc:tdd`. Replace the example command with one that stays in the table (`/sc:brainstorm "<topic>" --output <dir>` has the same bare-topic gate, check at implementation), drop `task` and `tdd` from the list (11 becomes 9) and drop the row. There is no `/sc:task` row. Line 44 mentions `.dev/tasks` staging only (false positive, keep). `tests/skills/test_worker_contract.py` pins the list (lines 500-503, 683, 717, 1549, 1620, 1743-1769): edit with it. |

Level numbers used by other text: `cli/recommend/prompts.py:189`, `sc-recommend/SKILL.md:169`, `sc-recommend/refs/delegation-vs-native-heuristics.md:40`, `commands/recommend.md:51` say "Level 4 needs explicit MDTM intent ..."; they change in PR 4 with the guide.

## 3. Protocol skills and commands that offer the bundle (re-point, PR 1, PR 3)

| Path:line | What it says | Change |
|---|---|---|
| `commands/reflect.md:21,63,68,108,146,172-173,224-238,266,290,305-317`; `skills/sc-reflect-protocol/SKILL.md:53-54,90,165,367-393,519-520,632-637,683-689,847,965,998-1003,1461,1504,1834,1874-1876`; `refs/remediation-handoff.md` (15 hits: route table 15-24, BUILD_REQUEST template 116-179, prompt 216-229, state 234-248, errors 300) | `--remediate --depth deep` runs the MDTM route: `task-builder` builds a task file, the user runs `/task`; Wave 1B optionally calls `tech-research` (not under `--unattended`) | PR 3: delete the MDTM route (Step 6.0 handoff write, `remediation_task_path` emission, the BUILD_REQUEST template, the error row); `--remediate` always takes the plan route (`sc:workflow` then `/sc:implement`); `--depth deep` keeps only its review-depth meaning. PR 1: remove the `tech-research` Wave 1B row (685-689). Keep `rf-qa` and `rf-qa-qualitative` rows. `sc:task-protocol` end-of-task hook mentions (reflect.md:21,317; SKILL.md:54,998) go in PR 2. |
| `commands/troubleshoot.md:54,79,103,147-149,205-206,216-217,227`; `skills/sc-troubleshoot-protocol/SKILL.md:138,593-599,617,645-647,670,690`; `refs/remediation-handoff.md:12,42-58,160-246`; `refs/report-template.md:113,171-173`; `refs/hardening-output-contract.md:54`; `refs/effective-input-proof.md:3`; `refs/runtime-entrypoint-verification.md:34`; `refs/diagnosability-audit.md:245` | `--fix --depth deep` selects the MDTM route (Phase A to D around `task-builder` and `/task`) | PR 3: delete the MDTM route; `--fix` always offers the `sc:workflow` plan route; fix the one-line mentions. |
| `commands/brainstorm.md:74,109,137,156,169,188-190`; `skills/sc-brainstorm-protocol/SKILL.md:40,48,108,189-194,344`; `refs/handoff-routing.md:66,197-224`; `docs/user-guide/brainstorm.md` (13 hits) | `--handoff task` invokes `Skill task-builder`; `--research deep` invokes `Skill tech-research` | PR 1: `--research deep` routes to `/sc:research --depth deep` (web) plus `/sc:analyze` (code); PR 3: `--handoff` choices become `none\|design` (a flag value removed: record in the changelog, as 6.0.0 did for `tasklist`); delete the Domain-Template-Mapping table that points at task-builder templates. |
| `skills/sc-crash-recovery/SKILL.md:3,113-116`; `refs/pipelines.md:9,25,36-43,52-89,95`; `refs/investigators.md:24`; `refs/report-template.md:89`; `scripts/bootstrap_scan.sh` (1 MDTM hit) | Pipeline recovery sections for PRD, TDD, research, roadmap and generic MDTM task files, resumed with `/task` or `/sc:task` | PR 1: delete the PRD, TDD, tech-research sections. PR 3: delete the roadmap and generic MDTM sections; keep the `/sc:workflow` section (line 95 already says "never to MDTM `/task`"). Existing task files on disk are left alone. |
| `skills/sc-recommend/SKILL.md:144,169,194,270`; `refs/delegation-vs-native-heuristics.md:27,40,64,98`; `refs/plugin-ecosystem-sources.md:27`; `refs/surface-enumeration.md:51`; plugin copies of all four; `cli/recommend/prompts.py:14-16,189`; `commands/recommend.md:51` | Examples and level text name `/task-builder`, `/task`, `/prd`, `/tech-research`, `/roadmap` | PR 1 and PR 4: replace the examples with surviving commands; line 270 and `plugin-ecosystem-sources.md:27` say "never use `/tech-research` for web search": delete the sentence. `prompts.py:14-16` cites `sc-task-protocol/SKILL.md:56-78` and `commands/task.md:71-93` as the model of the classifier; PR 2 rewrites the docstring (the classifier code stays, it does not read those files). |
| `skills/sc-issue-protocol/refs/chains.md:16,25`; `SKILL.md:189`; `refs/claim.md:82`; `templates/launch-prompt.md:21-23`; `commands/issue.md:97`; `cli/issue_pipeline/brief.py:8` | Chain rows offer the MDTM route and the `task` handoff; prohibition lists say "Do not run `/sc:implement`, `/task`, ..." | PR 3: remove the MDTM chain wording in `chains.md`. **The prohibition lists keep `/task`** (decision D4, section 10): they are deny-lists for an agent at the worktree level, pinned by `tests/skills/test_issue_protocol.py:299,439,591`, `tests/issue_pipeline/test_brief.py:139`, `tests/commands/test_issue_command.py:158`, `tests/skills/test_issue_orca_worktree.py:1105`. |
| `commands/implement.md:98` ("Invoke `/task` or `/sc:task`" in a does-not list); `skills/sc-implement-protocol/SKILL.md:211`; `commands/workflow.md:107`; `skills/sc-workflow-protocol/refs/overlap-routing.md:9`, `refs/00_mdtm_template_simple_task.md:22`, `refs/quality-gates.md` (1), plugin copies | "Not MDTM `/task`" disclaimers | PR 4: reword to say a plan package is not a task file; these files keep working without `/task`. |
| `commands/validate-tests.md`, `skills/sc-validate-tests-protocol/SKILL.md` (9 hits) | Validate `/sc:task` tiers | Deleted with their subject (PR 2, proposed). |
| `skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:54`; `skills/sc-post-release-protocol/refs/fan-out-pattern.md:9` | One MDTM sentence; one prose example ("the `sprint` command, the `roadmap` pipeline"), which names the pipelines removed in 6.0.0, not the `roadmap` skill | PR 3 for the first. The second is not a bundle reference (read in place): no change. |
| `agents/reuse-auditor.md` (2 hits from the second pass) | Names `/tdd` or the tdd skill as a caller | PR 1: reword. |

Skills that match only by false positive (no change): `skills/ccsession-tag/MODEL-TIERS.md` (`$/task` price column), `skills/sc-issue-protocol/scripts/clickup_claim.py` (ClickUp `/task` API path), `cli/sweep/models.py:32` (an example folder `.dev/tdd/auth-1/`), `cli/audit/dead_code.py:48`, `cli/review/telemetry.py:50`.

## 4. Kept agents: no edit (corrected)

All eight `rf-*` agents stay in 6.1.0 (issue 572 decides). The seven lines of `rf-qa.md` (84, 146, 309, 339, 349, 420) and `rf-qa-qualitative.md` (85) that name `rf-analyst`, `rf-team-lead's Fix Cycles rule`, `task-builder` or `tech-research` are **left unchanged**: text that names the agents stays valid, and a line that names a removed skill is part of issue 572's research. `tests/audit/` keeps every case that reads an agent; only the cases that read the `task-builder` skill are deleted in PR 4.

## 5. Hook: launch-level guard (security relevant)

`src/superclaude/hooks/scripts/launch-level-guard.sh:43,45,343-346,409` and the byte-identical `plugins/superclaude/hooks/scripts/launch-level-guard.sh`: the guard blocks an agent at the worktree level from starting implementation until a person types `/sc:implement` or `/task` (`LL_RE_APR`, line 346), classifies a `Skill` call named `implement`, `task` or `cleanup` as IMPL (line 409), and says `/task` in two messages.

Proposed: **no change** in 6.1.0 (decision D4). `/task` can still exist after the removal: the retire step keeps a customized copy, and IronFlow (the copy this release keeps) has its own `task` skill. Dropping `task` from the class list would let an agent at the worktree level start such a skill without being stopped, which is a safety regression; keeping it costs nothing. The 6.0.0 precedent for `improve` and `spawn` does not apply: those never reached the guard through a `Skill` call named after them, while `task` did. Tests: `tests/hooks/test_launch_level_guard.py:84,916-917,934,3698-3824` stay as they are.

The clean-search gate for PRs 3 and 4 therefore allows this script, its plugin mirror, its test, and the four issue-prohibition lists named in section 3.

## 6. Code

| Path:line | Change |
|---|---|
| `src/superclaude/cli/reflect/runner.py:475-476,588-596,769-771,783` (callers by codegraph: `_apply_remediation` is called only by `ReflectRunner.run`, `runner.py:642`) | PR 3: the wrapper always launches `/sc:implement <plan path>`; drop the `/task` verb and the `use_plan = not result.remediation_task_path` branch (769-771); update the comments at 52-55, 464, 475-476, 783. |
| `cli/reflect/commands.py:45`, `config.py` (1 MDTM hit), `models.py:148`, `contract.py:126`, `panel_lint.py:114` | The contract field `remediation_task_path` is a versioned schema field. Keep the field (reader stays tolerant, value is always null from 6.1.0) so old reports still load; fix the comment at `commands.py:45`. No version bump needed for a field that is only no longer written; state it in the PR body. |
| `cli/recommend/prompts.py:14-16,189` | Docstring and level sentence (PR 2, PR 4). |
| `cli/eval/suites/task_classification_contract.yaml` (8 hits), `workflow_vs_task_builder.yaml` (10), `README.md:23-65` (5), `scripts/eval_workflow_vs_task_builder.py` (4), `tests/cli/eval/test_workflow_vs_task_builder_companion.py`, `docs/guides/suites-guide.md:46,55,206-230,372-437` (12) | Delete the two suites with the script and its test; edit the README and the guide (decision D7). `agent_grounding_drift.yaml` names kept agents: no change. The eval harness itself stays (Clay: not yet). `tests/unit/test_cli_install.py:81-82` lists both suite files: edit. |
| `scripts/reflect_consumer_inventory.py:37-43,142-162` and `tests/review/test_reflect_consumer_inventory.py:38-129` | An inventory of which skills consume the reflect contract: remove the rows for `task`, `task-builder`, `sc-task-protocol`, `roadmap` (PR 4, PR 2). |
| `src/superclaude/cli/install_retired_data.py`, `install_retired_files.py:6` | PR 5: regenerate the data with `scripts/gen_retired_install_data.py --tag v5.0.0 --tag v6.0.0` after every removal PR has merged (the 6.0.0 rule). `install_retired_files.py:6` is a docstring that names `/sc:roadmap`; no edit needed. |
| `src/superclaude/cli/install_templates.py` (1 MDTM hit) | Names the workflow templates; templates stay (D5): no change. |

No Python module imports, calls or registers a bundle item: `src/superclaude/cli/main.py` registers no `task`, `tdd` or `prd` group (the `prd` pipeline went in 6.0.0, guarded by `tests/cli/test_cli_registration.py:104`). The bundle is Markdown that the installers copy.

## 7. Rules (installed into every session) and templates

| Path | Finding | Change |
|---|---|---|
| `src/superclaude/rules/core/ib_agent_core.md:216-226,856,880,954` | The always-loaded rule says "ALWAYS recommend `/task` to the user" and points at `.claude/commands/rf/task.md` | PR 4: delete the "Using the `/task` Command" subsection and the three command echoes; the rest of the file describes MDTM conventions and the `/rf:` namespace of IronFlow, which this release does not name as removed items (`/taskbuilder`, `/rf:task`): listed here, out of scope. |
| `rules/core/file_conventions.md`, `DIRECTORY_STRUCTURE.md`, `contextual/context_embedding.md`, `prompts/agent_library.md`, `prompts/*_worker_prompt.md` | Describe MDTM task-file conventions and the `/rf:` namespace | No change (not a removed name; the file format is generic). Follow-up candidate for issue 572. |
| `src/superclaude/templates/documents/` (14 files), `templates/workflow/` (8 MDTM and PRD templates plus `changelog_template.md` and others), `templates/modularization-template-review/` (28 QA and analyst report templates) | 585 hits. Mixed ownership: `changelog_template.md` is used by the release procedure; `skill_template.md` and `agent_template_qa.md` are pinned by `tests/skills/test_review_severity_rule.py:184-185,368` and `test_review_prompt_overrides.py:261`; `tests/unit/test_cli_install.py:312-346` lists all 52 installed templates; the retire step cannot remove an installed template (it covers commands, skills, agents only) | **Keep all templates in 6.1.0** (decision D5) and open a follow-up issue for the ones only the removed skills used. The clean-search gate excludes `src/superclaude/templates/` for this reason. |

## 8. Docs (not historical records)

| Path | Hits | Change |
|---|---|---|
| `docs/user-guide/commands.md` (22) and `flags.md:75-98` | table rows and sections for `/sc:task`, `/sc:tdd`, `/sc:validate-tests`; `--handoff task`; the `--fix --depth deep` sentence; `--resume <task file>` (633); `tests/sc-task/` (656) | PR 1 (`/sc:tdd`), PR 2 (`/sc:task`, `/sc:validate-tests`), PR 3 (flags) |
| `docs/user-guide/brainstorm.md` (13), `codegraph.md:120-122` (2), `session-management.md:12,73` (2) | `task-builder`, `tech-research`, `/sc:task` lines | PR 1, 2, 3 |
| `docs/onboarding/ironclaude-onboarding.html` (27) | The deck is checked against the guide by `tests/docs/test_onboarding_deck.py`: it may name only commands the guide states. When the guide drops `/prd`, `/tdd`, `/tech-research`, `/task-builder`, `/task`, the deck must drop them too (diagram text at lines 304-431, comparison table 559-563, level table 591-593). | PR 1 (levels 5, 6, document routes), PR 4 (level 4) |
| `docs/guides/prd-skill-release-guide.md` (58), `tdd-skill-release-guide.md` (68), `RELEASE-GUIDE-INSTRUCTIONS.md:12` (1), `docs/reference/nfr-conv-2-prose-determinism.md` (26), `docs/reference/README.md:18` | Guides and a reference that exist only for removed skills; `tests/skills/test_spec_panel_review_loop.py:29` lists `tdd-skill-release-guide.md` | Delete the three files, edit the index row and the example sentence (PR 1; PR 4 for the nfr reference) |
| `docs/guides/reflect-cli-tools-guide.md:38,71,334,391,432,476,540` (7), `docs/guides/suites-guide.md` (12) | MDTM route of the reflect wrapper; the two eval suites | PR 3, PR 4 |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (9), `review-severity-rule.md:57,66-67` (3), `session-memory.md:26,78-79` (4), `technical-architecture.md:41` (1) | `/sc:task` is the worked example of a command, `sc-task-protocol` of a skill (lines 289,342,626-643,702,837,1227); rule-copies table lists the bundle's files; the memory store table lists the readers | PR 2 and PR 4: pick a surviving command and skill as the worked example (`/sc:implement`, `sc-implement-protocol`); delete the bundle rows. `technical-architecture.md:41` names `rf-qa.md`: stays. |
| `docs/getting-started/upgrading.md` (4) | 6.0.0 retire-step text | PR 5: add a 6.1.0 section (what is removed, what is kept, what an in-flight MDTM task file does) |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (10) | Review-log rows of a past task (dated 2026-11-10 to 12) | Historical record of a finished task: no edit |
| `docs/docs-product/ops/jev-litellm-gateway-operational-guide.md:17`; `docs/memory/reflect/deviation-patterns-...`; `docs/generated/contributor-knowledge-base/*` (7) | An unrelated document that carries the label `operational-guide`; a memory record; generated artifacts | No change |
| `PROJECT_INDEX.md:75`, `PROJECT_INDEX.json:110` | Lists the bundle skills as "notable" | PR 4: drop the names |
| `commands/sc-help.md:42,117` (legacy root copy naming `/sc:sc:task`), `POST-REFLECT-TASK.md` (61, a finished task file at the repo root that names `rf-task-executor` as assignee), root `CLAUDE.md:98` (false positive) | | Edit `sc-help.md` in PR 2; `POST-REFLECT-TASK.md` is a historical task record, left alone (it is a root-level file: flagged for Clay in the issue) |

## 9. Tests: baseline and trial removal

Baseline on `847cccc1a` (full suite as `.github/workflows/test.yml` runs it: `pytest -n auto --ignore=tests/cli/test_verify_sync_hooks.py`, 24 workers, machine under load from other sessions): **22691 passed, 10 failed, 70 skipped, 1 xpassed** (579 s). The ten failures exist before any edit: `tests/unit/test_ccsession_tag.py` (8, terminal handling), `tests/cli/eval/test_schema_validate.py::test_rejection_does_not_write_to_default_scratch_root`, `tests/hooks/test_launch_level_guard.py::test_speed_large_commands[backslash-lines-64KB]` (a timing test). Every PR gate compares against this list.

Trial removal (all bundle files and mirrors deleted, nothing else edited, then the same run): **148 failed and 101 errors** (22453 passed). Per test file, the cause is a missing file:

| Failures | Test file | Reads | Disposition |
|---:|---|---|---|
| 40 | `tests/skills/test_worker_contract.py` | `commands/task.md`, `commands/tdd.md`, task-builder skill | edit: drop the removed commands from the list of converted commands |
| 39 | `tests/skills/test_task_builder_merge.py` | task-builder skill, `rf-analyst/rf-task-builder/rf-qa*` | delete (PR 4): it tests the removed skill's merge step |
| 32 | `tests/recommend/test_routing_refresh.py` | the guide rows and skills `tdd`, `prd`, `roadmap`, `task-builder` (cases S02, S03, S09, S10, S12, S18-S20, S29) | edit with the guide; frozen record `tests/recommend/fixtures/routing_refresh_cases.json` (11 hits) kept as a record, cases for removed routes marked removed |
| 16 + 12 + 11 + 9 + 9 + 7 + 6 + 5 + 4 + 4 + 4 + 2 | `tests/audit/test_dnsp_*`, `test_inherited_verdict_*`, `test_sequencing_PR06_before_PR04`, `test_synthetic_dnsp_dedup_not_regression`, `test_regression_halt_pass1_fail2`, `test_monotonicity_halt_F_5_5_5`, `test_hidden_input_guard`, `test_dynamic_enumeration_inv_010`, `test_slow_shrink_continues` (13 files) | the task-builder skill (the "four wrapper sites") | corrected: delete only the cases that read the task-builder skill (PR 4); every case that reads `rf-analyst`, `rf-team-lead`, `rf-qa` or `rf-qa-qualitative` stays, with its fixtures |
| 10 | `tests/unit/test_cli_install.py` | pinned baseline lists of installed members: 6 agents, 21 skill files, 2 commands, 2 eval suites, templates | edit the lists |
| 9 | `tests/skills/test_review_severity_rule.py` (+3 `test_review_prompt_overrides.py`) | the skills and refs that carry the review rule | edit the file lists (and the fixtures `tests/skills/fixtures/review_severity_{cap,sweep}_edits.yaml`, 181 hits, which record edits to those files) |
| 6 | `tests/skills/test_codegraph_adoption.py` | `sc-task-protocol/SKILL.md` | none (corrected: `sc-task-protocol` stays) |
| 2 | `tests/core/test_how_we_work_routing_table.py` | `/task-builder is neither a built-in nor a skill` | edit with the guide: more cases fail once the guide text changes (15 pins at lines 295-1030) |
| 2 + 1 + 1 + 1 | `tests/commands/test_impact_command.py:352-376`, `tests/skills/test_sc_recommend_routing_contract.py:31`, `tests/skills/test_primitive_dual_surface_lookup.py:51-56`, `tests/cli/test_install_retired_files.py` | `sc-task-protocol`, `tdd/refs/build-request-template.md`, the task-builder lookup line | edit or delete the case |
| baseline | ccsession (8), schema_validate, `test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files` (1) | | not mine: that last one passed in the baseline run and failed in the trial run, and it also fails when run alone on the clean tree (`pytest tests/cli/test_install_keep.py`: 1 failed, 13 passed), so it is order dependent; the 6.0.0 retire-step map already lists it as failing on integration |

Tests that fail only after text edits (not in the trial): `tests/core/test_how_we_work_routing_table.py` (pins 295, 399, 444-484, 548-552, 591, 618, 723, 839-840, 961, 1030), `tests/docs/test_onboarding_deck.py`, `tests/cli/reflect/{test_fix_loop,test_no_nesting_guard,test_remediation_route_table,test_remediation_source_template}.py` and `conftest.py:149-157`, `tests/commands/test_auggie_review_remediation_chain.py:8,95-97` (a negative test: the MDTM route "must not come back"; stays), `tests/pipeline/test_process.py:126` (a prompt string `/sc:task-unified`, false positive), `tests/hooks/test_launch_level_guard.py` (stays, D4), `tests/skills/test_issue_protocol.py`, `tests/recommend/{test_cache,test_dispatch}.py` (use `/prd` and `/task-builder` as sample cache keys: replace with a surviving command), `tests/troubleshoot/*` (4 files), `tests/skills/test_spec_panel_review_loop.py:29,105,136`.

Expected pass-count change: baseline 22691; the trial lost 238 passes. The real number is fixed per PR: the gate says pass count drops only by the removed tests and records both numbers.

## 10. Decisions applied by default (Clay may overrule before the PR that uses them starts)

| # | Decision | Applied default | Used by |
|---|---|---|---|
| D1 | `prd`, `readme`, `tech-reference` | Removed with the bundle (they cannot run without `task` and `task-builder`) | PR 1 |
| D2 | Dropped (Clay, 2026-11-18): `/sc:task`, `/sc:validate-tests` and their skills stay | none | none |
| D3 | All eight `rf-*` agents | Kept in 6.1.0; issue 572 decides; their text is left unchanged | none |
| D4 | Launch-level guard and the issue prohibition lists keep `task` and `/task` | Kept as deny-list entries | PR 3, 4 |
| D5 | The 52 installed templates | Kept; follow-up issue | none |
| D6 | What replaces levels 5 and 6 | The scale ends at level 3; research-first points at `/sc:analyze`, `/sc:research`, `/sc:brainstorm`; no replacement for full-specification | PR 1, 4 |
| D7 | The eval suite `workflow_vs_task_builder` | Removed with the script and its test; the harness and `task_classification_contract` stay | PR 4 |
| D8 | Flag values removed: `/sc:brainstorm --handoff task`; the MDTM route of `/sc:reflect --remediate --depth deep` and `/sc:troubleshoot --fix --depth deep` (both now take the plan route) | Removed; listed in the changelog as breaking | PR 3 |
| D9 | Version 6.1.0 | Clay's decision 6.3. Recorded: `changelog_maintenance.md` treats a removed command or skill as breaking, which is a major version; 6.0.0 followed that rule | PR 5 |

## 11. Unfinished work handling

A user with a task file under `.dev/tasks/to-do/TASK-*` in progress when 6.1.0 arrives has no `/task` to resume it. `/sc:implement` accepts spec and task inputs but does not invoke `/task` (`sc-implement-protocol/SKILL.md:13,17,211`), and issue 573 notes that existing generated task files are not shown to work unchanged under it. Handling (text only, no new code): the release notes and `docs/getting-started/upgrading.md` say "finish or park MDTM tasks before upgrading, or resume them in IronFlow, which keeps `task`, `task-builder` and the `rf-*` agents"; no task file on disk is touched. IronFlow's project-level copies in its own `.claude/` are not touched by the retire step, which works on `~/.claude/` only.
