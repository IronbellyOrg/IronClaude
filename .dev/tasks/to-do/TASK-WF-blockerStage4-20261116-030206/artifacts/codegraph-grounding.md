# Codegraph grounding for TASK-WF-blockerStage4-20261116-030206

## Run state

- index_state: fresh
- checked_at: 2026-11-16T03:03:44Z (`codegraph_status`: 3570 files, "Changes since index: 0 added, 0 modified, 0 removed")
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- access: mcp
- degraded tokens: none
- note: the index covers Python, YAML, JavaScript and TypeScript, not Markdown. The skill, agent, template, rule-prompt and command files this plan edits were resolved with Grep and Read from the base grounding of `TASK-WF-loosenBlockerRev-20261115-210254` (read 2026-11-15) plus a `test -e` check today; no symbol lookup beyond that was repeated for this package.

## Resolved symbols

- Four digest templates under `src/superclaude/templates/` (`documents/agent_template_qa.md` merge rule near 85, `skill_template.md` near 828, two MDTM templates near 644 and 655) and `agent_template_analysis.md` (merge-rule text only); four rule prompts near lines 11, 27, 28, 27; the builder and researcher skills (`tech-reference`, `readme`, `tdd/refs/build-request-template.md`, `operational-guide`); `commands/spec-panel.md` and its plugin twin. Line numbers are from the base grounding and Task 1 of the base plan; every task re-reads before editing.
- `plugins/superclaude/skills/` holds 4 entries today (`confidence-check`, `sc-implement-protocol`, `sc-recommend`, `sc-workflow-protocol`); the mirror folder is new.
- Existing paths named in the plan (`test -e` today): 16. Paths named that do not exist yet: 6: `plugins/superclaude/skills/sc-review-severity/`, `plugins/superclaude/skills/sc-review-severity/refs/rule.md`, `src/superclaude/skills/sc-review-severity/`, `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, `tests/skills/test_review_severity_plugin_parity.py`, `tests/skills/test_review_severity_registry.py`.

## Dependents

- Plugin twins (hand-kept, differ from source): `plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`.
- Installed-only spec-panel variants in `~/.claude/commands/sc/` (`spec-panel-armb.md`, `-diffgate.md`, `-ledger.md`, `-ponytail.md`, `-stoprule.md`) are outside the scan and stay `installed-only`.
- `make verify-sync` covers `src/` to `.claude/`; the plugin mirror is checked by the new parity test.

## Pre-check

Checked 2026-11-16 with `test -e` over the 22 distinct `src/`, `tests/`, `plugins/` paths the plan names in backticks: 16 exist and 6 do not. Every absent path is a file or folder this package creates or one an earlier package creates (the stage 1 modules and tests, the skill folder `sc-review-severity`, the stage 2 `test_review_brief_rests_on.py`); the first task of each of stages 2, 3 and 4 checks the earlier package's evidence by package id before anything else runs. No named existing path is missing.
Plan edits made during this pre-check. The protocol says the pre-check never edits the plan; this run did edit it after the generator wrote it and before the gate and the reflect call, to remove wording the gate rules reject: the literal task-folder prefix in the Constraints line for the spec, and leftover cross-package task numbers (a Phase or Task number of the old 46-task plan, replaced by the stage 3 package's name). No reflect finding drove these edits.
Not checked: the quoted line numbers in task bodies (they come from the 2026-11-15 grounding and each task re-reads before editing); that the old 46-task plan's task text is unchanged since extraction (it is the base text, extracted once on 2026-11-16).

## Revision 2 (2026-11-16)

Re-checked against the live files in the worktree on 2026-11-16 (Markdown carriers are not in the codegraph index, so Grep, `git grep` and Read were used; `codegraph_status` was not repeated because no symbol lookup was needed).

Existence (`test -e` over 38 paths named in the revised plan): 29 exist (all 5 templates, the 5 rule prompts, the 4 builder and researcher skill files, `src/superclaude/commands/spec-panel.md` and the two plugin twins, `rf-qa-qualitative.md`, `doctor.py`, 9 existing test files, `OPEN-QUESTIONS.md`, `~/.claude/WORKER-CONTRACT.md`); 9 do not exist yet and are created by earlier stages: `src/superclaude/skills/sc-review-severity/` with `refs/rule.md`, `refs/registry.yaml`, `refs/scale-map.md`, `refs/follow-up-ledger.md` (stage 1), `tests/skills/test_review_severity_registry.py` and `tests/skills/test_review_merge_rule_scan.py` (stages 1 and 3), `tests/skills/test_review_brief_rests_on.py` (stage 2). The plugin paths of the old plan (`plugins/superclaude/skills/sc-review-severity/...`, `tests/skills/test_review_severity_plugin_parity.py`) are no longer named.

Facts re-read (commands):
- `git grep -l "Grade every review finding as blocking or minor" -- src plugins` prints exactly the 11 digest carriers (none under `plugins/`); `git grep -n "review-severity:digest" -- src plugins` prints nothing today.
- `git grep -n "follow-up candidates" -- src plugins` hits 3 in `src/superclaude/commands/spec-panel.md`, 3 in the plugin twin, 3 in each `document_review_loop_prompts.md` and 1 in `pragmatic.md` (stage 3). `git grep -n "follow-up candidates\|once per loop" -- tests` hits `tests/skills/test_review_severity_mapping.py` (Grading literal, Verdict literals, the output-style cadence pin) and one unrelated fixture.
- `cmp` of the two `document_review_loop_prompts.md` copies prints nothing (byte-identical); `tests/skills/test_review_brief_placement.py` asserts the byte copy.
- The plugin `commands/spec-panel.md` has no `## Unattended mode` heading (`grep -n "^## "`); the source has it near line 455. `tests/skills/test_worker_contract.py` forbids `src/superclaude/` and `nested/` in that section.
- Cap sentence counts (`grep -ci`): tech-reference 5, readme 6, tdd 1 (lower-case "after"), operational-guide 2. HALT-line counts: `agent_template_qa.md` 2, 01 template 5, 02 template 6. Each of the 8 digest carriers holds the cap phrase once today.
- Merge-rule lines match the plan: 6 lines in the four skills (tech-reference 510 and 513, readme 542 and 547, tdd 122, operational-guide 511), plus `agent_template_qa.md:85` and `agent_template_analysis.md:466`.
- Label list near `agent_template_qa.md:333` holds "Contradictions are always IMPORTANT or CRITICAL" in an example comment; `rf-qa-qualitative.md:990` holds Rule 6 today (stage 3 rewrites it).
- `git diff --name-only HEAD -- src/superclaude/skills/task src/superclaude/skills/task-builder src/superclaude/agents/rf-task-builder.md` prints nothing.

Findings:
- G1 applied (summary check reduced; window result read from the stage ledger go cell; checks run before the first edit).
- G2 applied (pins named, mapping test added to the run lines, FR-8 line named; conditional on stage 3 settled by a grep first).
- G3 applied (final pinning run in Task 5; plugin byte copy moved into Task 2).
- G4 not needed (decision 4: no plugin mirror; plugin spec-panel gets no Unattended section).
- G5 applied (acceptance by content plus one source-only test).
- G6 applied (checks before the first edit).
- G7 applied. G8 applied (case-insensitive counts verified above). G9 applied. G10 applied.
- G11 and G12 not applied: the plugin mirror, parity test and plugin `canonical` row are removed by decision 4.
- G13 applied (settling `git grep` before the strict switch; both print nothing or only registered files today).
- G14 applied for (a), (c), (d); (b) is moot (no plugin copy of `scale-map.md`).
- Decision 1 applied (old Task 4 dropped; `rf-task-builder.md` and `task-builder/SKILL.md` not edited; `test_task_builder_merge.py` not run).
- Not verified: whether stage 3's Task 8 moves the spec-panel literals in the mapping test (its text names none), so Task 4 settles that with a grep at run time; the exact wording of Rule 6 after stage 3 (Task 1 reads it then).

## Revision 3 (2026-11-16)

Re-checked against the live files (the code graph is not used for markdown carriers; checks are `test -e`, `grep` and `awk`):
- `test -e` prints "exists" for `tests/unit/test_cli_doctor.py`, `tests/cli/test_install_retired_mcp.py`, `tests/skills/test_worker_contract.py`, `tests/audit/test_severity_floor_unweakened.py`, `src/superclaude/agents/rf-qa-qualitative.md` and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`. `tests/skills/test_review_severity_registry.py` does not exist yet (stage 1 Task 15 creates it), so the switch name is read at run time.
- `grep -rc "CRITICAL and IMPORTANT findings are blocking" src/superclaude/templates` is 1 in exactly four files: `agent_template_qa.md` (line 140), `skill_template.md` (831), `01_mdtm_template_generic_task.md` (647), `02_mdtm_template_complex_task.md` (658). `grep -rn` of the phrase over `tests` prints nothing (no test pins it).
- `agent_template_qa.md`: line 100 is `N+1. **NO LENIENCY**` (holds "claim is blocking" once and "it FAILS. Grade what you find"), line 339 is `N+2. **Report honestly**` ("When in doubt, fail it"); lines 95, 96 and 102 name the principle only. Other "in doubt" hits are gate choice (`01_...` line 907, `02_...` line 1059) and default tier (`skill_template.md` line 125) and stay.
- Rule prompts: `NO LENIENCY` at line 20 (`automated_qa_workflow_qa_prompt.md`, with the "close enough" clause), 36 (`doc_code_analyst`), 37 (`documentation_expert`), 36 (`recruiting_expert`, no clause); "When in doubt, fail the item" at 147, 261, 295 (none in `recruiting_expert_qa_prompt.md`); `BE STRICT` "almost right or close enough" bullet at 151, 265, 299 (none in recruiting). `grep -c -iE 'close enough|probably what was intended|almost right'` today is 2, 1, 1, 0 and `grep -c -F "When in doubt, fail"` is 1, 1, 1, 0. The mechanical rule "If an expected item is NOT marked [x], it MUST be marked as FAIL" is in all four files and stays. `grep -rn` over `tests` for these phrases prints nothing; the fixture rows for the rule prompts pin only the "zero-tolerance policy" lines.
- `awk '/^## Critical Rules/{f=1} f && /^6\. \*\*/{print NR": "$0; exit}' src/superclaude/agents/rf-qa-qualitative.md` prints one line (`990: 6. **Contradictions are always IMPORTANT or CRITICAL** ...`); stage 3 rewrites it.
- `managed-workspace.md` line 59 holds `FINAL: <pass|issues> evidence=<ev-list> state=<sha256>`; `issues` leaves the package in to-do (archive-blocked).
- `src/superclaude/commands/spec-panel.md` `## Unattended mode`: the Contract bullet holds the only line with `` `artifacts` `` in that section; `tests/skills/test_worker_contract.py` `_artifacts_clause` (line 1298) reads the rest of that line, `_check_f1_clause` (line 1911) requires "paths git ignores are left out (WC-4)" and rejects "git add" and "git refuses", the spec-panel expectation (line 616) requires "improved-spec.md", and `_check_unattended_section` forbids `nested/` and `src/superclaude/`.
- Stage 1 Task 15 says only "strict mode is a switch, off in this phase" (no name). The spec's stage 4 row says "T2 becomes strict (no legacy definition sentence in `src/` or `plugins/`)".
- `git diff --name-only HEAD -- src/superclaude/skills/task src/superclaude/skills/task-builder src/superclaude/agents/rf-task-builder.md` prints nothing.

Findings: H1, H3, H4, H5 applied; H2 applied as a recorded exclusion (the cap sentences are pinned by the cap-edit fixtures, stage 2 owns the tech-research file); F2 (H6), F3 (H7), F7 (H12) applied; F5 (H11) is a stage 3 plan defect, not applicable here; H13 (a) applied in passing, H8, H9, H10 and H13 (b), (c) not applied (minor, outside this cycle's list). The stage 3 doubt-line item applied to Tasks 1 and 2 (recruiting prompt has no doubt bullet, so that line is dropped; the `BE STRICT` bullet is an addition found in the live files).

## Revision 4 (2026-11-16, cuts debate)

Plan trimmed from 6 tasks to 4 (one per phase) per `cuts-debate/final-cuts.md` section (b). Markdown carriers are not in the code graph; checks are `test -e`, `grep`, `awk` and `sed -n` on the live tree.

Existence (`test -e` over 29 paths named in the trimmed plan): 28 exist (the five templates, the four rule prompts, the four skill files, `src/superclaude/commands/spec-panel.md` and its plugin twin, `src/superclaude/agents/rf-qa-qualitative.md`, `sc-implement-protocol/refs/qa.md`, and 12 test files including `test_review_severity_mapping.py`, `test_review_severity_rule.py`, `test_primitive_dual_surface_lookup.py`, `tests/audit/test_severity_floor_unweakened.py`). 1 does not exist yet: `tests/skills/test_review_merge_rule_scan.py` (the stage 3 reverse-scan test; the plan says to use the name stage 3 gives it if it differs).

Facts re-read:
- `tests/skills/test_review_severity_rule.py`: `S_OPENINGS` maps S1 to the "Grade every review finding" bullet, S2 to "Minor findings never fail", S3 to "A review loop (review, fix, re-review) runs at most 2 fix cycles" (the cap bullet), S4 to "A protocol that defines its own severity model", S5 to the CRITICAL / IMPORTANT / MINOR bullet; `S1_S3_FILES` has the ten entries and `S5_FILES = S1_S3_FILES[:6]`. So the cap bullet arrives with the stage 3 copy and its count is 1 in each carrier today (`grep -c` over the eight carriers prints 1) and HALT counts are 2, 5, 6 for `agent_template_qa.md`, `01_...` and `02_...` (K1).
- Live doubt lines: `NO LENIENCY` at `automated_qa_workflow_qa_prompt.md:20` (with the "close enough" clause), `doc_code_analyst_qa_prompt.md:36`, `documentation_expert_qa_prompt.md:37`, `recruiting_expert_qa_prompt.md:36` (the last three say only "Do not give workers the benefit of the doubt"); "When in doubt, fail the item" at 147, 261, 295 and the BE STRICT "almost right" bullet at 151, 265, 299 (none in the recruiting prompt); `agent_template_qa.md:100` and `:339`; label list `agent_template_qa.md:333`.
- K6 sibling lines read: `automated_qa_workflow_qa_prompt.md:125` and `doc_code_analyst_qa_prompt.md:206` ("No benefit of doubt: If you cannot verify something exists/works, it FAILS", a checklist-item rule), `skill_template.md:824` (FAIL bullet already worded "any blocking (Critical or Important) finding") and `:834` ("Zero tolerance - if you can't verify it, it fails.", described at `:841` as verbatim across all skills). All kept with a reason in the Constraints.
- Merge-rule hits: `grep -rniE "highest severity|more severe|higher severity"` over `templates`, `rules/prompts` and the four skills hits only `agent_template_qa.md:85`, `agent_template_analysis.md:466`, `tech-reference/SKILL.md:510, 513`, `readme/SKILL.md:542, 547`, `tdd/refs/build-request-template.md:122`, `operational-guide/SKILL.md:511`. `skill_template.md` and the two MDTM templates hold no such sentence; the MDTM Findings Consolidation steps (`01_...:936`, `02_...:1088`) say "with severity (CRITICAL/IMPORTANT/MINOR) and originating lens", and `skill_template.md` has no step that merges reviewer reports. The plan treats the L1 clause as an addition at those two steps and records the `skill_template.md` note (a divergence from final-cuts wording, which names `skill_template.md`).
- Spec-panel: `src/superclaude/commands/spec-panel.md` lines 259, 260, 332 hold the Grading, Verdict and FR-8 text and line 372 the dimensional-mismatch sentence; the plugin twin holds the Grading, Verdict and FR-8 lines at 257, 258, 330. `tests/skills/test_review_severity_mapping.py:72` holds "asks the user once per loop" (Verdict test, source and plugin) and `:128` the output-style pin owned by stage 3.
- Rule 6 `awk` over `rf-qa-qualitative.md` prints one line today (`990: 6. **Contradictions are always IMPORTANT or CRITICAL** ...`); stage 3 may rewrite it, so Task 1 reads it then (K4).
- `git status --short src plugins tests` prints nothing at the time of this revision (no carrier edited yet).

Findings: K1, K2, K3, K4, K6 applied; K5, K7 recorded in the Constraints; K8, K10, K11 moot (strict switch, allow-list and scale map cut); K9 recorded (plugin parity undecided). Not done: the reachability of the four rule prompts (owed item (e)1) is only turned into a recorded grep inside Task 1 (`stage4-task1-notes.md`).
