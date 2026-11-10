---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeTheAnyIssu-20261101-225635
version: "1"
priority: High
created_date: "2026-11-01"
---

# Minor findings never fail a review; review loops capped at 2 fix cycles

Source: ./source.md
Goal: No shipped primitive fails a review on a minor finding or rechecks minors, every review loop runs at most 2 fix cycles (3 reviews) and then escalates open blocking findings to the user instead of passing them, `/sc:implement` drops its second A2 repair, and static tests pin all of it.

## Constraints

- Final user decisions (restart spec `/tmp/t11b-severity-rule-restart-spec.md`): B1 minor findings are noted and work proceeds, with no recheck and no FAIL; B2 the cap is 2 fix cycles = at most 3 reviews, existing "Max 2" values stay, "Max 3" and uncapped loops drop to 2; B3 `/sc:implement` option A; `update.sh` is not changed. Evidence: `/home/coder/workspaces/IronClaude/.dev/worktrees/qa-loop-investigation/.dev/qa-loop-investigation/FINDINGS.md` sections 4 and 5 (bundle A).
- The site list, file:line and replacement wording for every edit is the repo-relative file `.dev/review-severity-rule/inventory.md` (sections 1-6). Line numbers are against commit `f90877be`; locate each site by its quoted text.
- Canonical rule text: sentences S1-S5 in inventory section 1, held in `src/superclaude/output-styles/pragmatic.md`. Every edited QA agent, template and rule prompt carries S1-S3 word for word (whitespace and indentation may differ); files with a CRITICAL / IMPORTANT / MINOR scale also carry S5. Canonical cap text, reused wherever a cap is stated in prose: "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings".
- Keep the binary PASS/FAIL verdict, the adversarial stance and the zero-finding Self-Audit bullets of `src/superclaude/output-styles/pragmatic.md`.
- Edit only `src/superclaude/`, `plugins/superclaude/` twins, `tests/` and `CHANGELOG.md`. Never edit or stage `.claude/` (except `.claude/settings.json`, which this plan does not touch); run `make sync-dev` after source edits. `.dev/tasks/` is always staged.
- R-008: never write a `src/superclaude/...` path into an installed primitive (commands, skills, agents, core, hooks, templates, rules, output styles); use `~/.claude/...` installed paths. Every task that edits a primitive checks this with `git diff -U0 -- <edited files> | grep '^+' | grep -n 'src/superclaude'` printing nothing.
- Minor findings from this plan's own reviewers are noted, not fixed in extra rounds.
- R-010: checks are the tests named per task plus the tests that read edited files; `make verify-sync`; `make lint`. Never the full suite and never `tests/cli/eval/` as a directory.
- Commit, push and `/sc:pr-submit` are done by the operator after this plan, not as plan tasks.

## Phase 1: Canonical rule

## Task 1: Replace the any-severity bullet in the Pragmatic output style

Covers: R-001, R-007 (pin P1), R-008.

Replace the bullet in `src/superclaude/output-styles/pragmatic.md` that begins "Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict" (line 225 at `f90877be`) with the five bullets S1, S2, S3, S4, S5 of inventory section 1, in that order, without the trailing "(S1)" style labels. Leave the adversarial-stance, zero-finding Self-Audit and binary-verdict bullets unchanged. The SubagentStart hook (`src/superclaude/hooks/scripts/pragmatic-subagent.js`) reads the installed style file and needs no change. Update pin P1 in `tests/skills/test_implement_severity_static.py` (`test_p1_output_style_exempts_implement_severity_model`, which pins the old bullet) to assert the new S2 and S4 text; keep P2-P4 unchanged.

Acceptance criteria:
- `git grep -n -i -E 'any severity|minor issues still pass' -- src/superclaude/output-styles/pragmatic.md` prints nothing; the file contains S1-S5 verbatim, S3 containing "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings", and still contains "Every review agent MUST produce a binary verdict: PASS or FAIL.", "Treat a review that surfaces zero issues as suspect" and "Every review agent MUST begin its review from an adversarial position".
- `uv run pytest tests/skills/test_implement_severity_static.py -q` passes (saved to `./artifacts/t1-static.log`).

## Phase 2: QA agents and templates

## Task 2: Apply the rule to rf-qa and its verdict test

Depends on: Task 1

Covers: R-002, R-007 (nfr_conv_9 test and fixtures), R-008.

Edit `src/superclaude/agents/rf-qa.md` per the inventory section 2.2 rows for `agents/rf-qa.md`: the DNSP references to "any gap regardless of severity = FAIL" (lines 82 and 84), principle 1 "Zero tolerance" (91), principle 8 NO LENIENCY (98), the research-gate Gap severity items (158-159), the research-gate Verdict bullets (171-172), the Fix Cycle phase re-verification scope (370-391: re-verify previously failed blocking items only), the SendMessage content "Must resolve ALL [N] issues" (464) and rule 10's "ALL findings regardless of severity must be resolved." (537). Add one "## Review severity rule" section after the Verification Principles holding S1-S3 and S5. Leave cap numbers, the "max-3-cycles" token and the sha256 mention for Task 11. Update `tests/audit/test_nfr_conv_9_zero_trust.py`: the `PASS_BULLET` / `FAIL_BULLET` constants to the new research-gate bullets, the verdict scorer to fail only on CRITICAL or IMPORTANT gap rows, the one-MINOR-gap case to expect PASS, plus a new one-IMPORTANT-gap case expecting FAIL (new fixture `tests/audit/fixtures/nfr_conv_9/one_important_finding.md`); update the prose quoting the old rule in `tests/audit/fixtures/nfr_conv_9/one_low_finding.md` (lines 13, 45) and `tests/audit/fixtures/nfr_conv_9/zero_findings_baseline.md` (lines 9, 35).

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|still must be fixed' -- src/superclaude/agents/rf-qa.md` prints nothing; the file contains S1, S2, S3 and S5; the research-gate PASS bullet allows MINOR gaps as notes and the FAIL bullet names only CRITICAL or IMPORTANT gaps.
- `uv run pytest tests/audit -q` passes (saved to `./artifacts/t2-audit.log`).

## Task 3: Apply the rule to rf-qa-qualitative and rf-analyst

Depends on: Task 2

Covers: R-002, R-008.

Edit `src/superclaude/agents/rf-qa-qualitative.md` per inventory 2.2: the DNSP reference (83), NO LENIENCY (97), the eight PASS / FAIL verdict pairs (228-229, 279-280, 350-351, 417-418, 488-489, 555-556, 734-735, 772-773), the Fix Cycle phase (777-797: blocking items only) and rule 10 (982), plus one "## Review severity rule" section with S1-S3 and S5 after the principles. Edit `src/superclaude/agents/rf-analyst.md` per inventory 2.2: the DNSP API-003-M6 clause at line 74 ("treated as a real finding for the existing "any gap regardless of severity = FAIL" gating rule"), line 93, and lines 148 and 199 ("must still be fixed"). Cap numbers, "max-3-cycles" tokens and sha256 mentions stay for Task 11.

Acceptance criteria:
- `git grep -n -i -E 'any severity|issues of any severity|regardless of severity|no severity level is exempt|must still be fixed' -- src/superclaude/agents/rf-qa-qualitative.md src/superclaude/agents/rf-analyst.md` prints nothing.
- `rf-qa-qualitative.md` contains S1, S2, S3 and S5 and eight PASS bullets that allow MINOR issues as notes; `uv run pytest tests/audit -q` passes (saved to `./artifacts/t3-audit.log`).

## Task 4: Apply the rule to the QA agent template, shared document templates and the DNSP contract

Depends on: Task 1

Covers: R-002, R-008.

Edit per inventory 2.2 and 2.3: `src/superclaude/templates/documents/agent_template_qa.md` (principle lists 95-96, NO LENIENCY 100, S5 under the MINOR definition at 139, verdict 156-157 plus S1-S3, message 262, the severity clause of rule N+3 at 335; its cap numbers stay for Task 11); `src/superclaude/templates/modularization-template-review/analyst-completeness_report_template.md` lines 75 and 159; `src/superclaude/templates/documents/skill_template.md` lines 815 and 824 (the shared research-gate prompt block's Gap severity item and FAIL verdict); `src/superclaude/templates/modularization-template-review/synthetic-dnsp-finding.contract` line 52 (pre-review finding C3).

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|must still be fixed|ALL findings must be resolved' -- src/superclaude/templates/documents/agent_template_qa.md src/superclaude/templates/documents/skill_template.md src/superclaude/templates/modularization-template-review/analyst-completeness_report_template.md src/superclaude/templates/modularization-template-review/synthetic-dnsp-finding.contract` prints nothing.
- `agent_template_qa.md` contains S1, S2, S3 and S5; `uv run pytest tests/audit tests/skills/test_task_builder_merge.py -q` passes (saved to `./artifacts/t4-tests.log`).

## Task 5: Apply the rule and the at-cap escalation to the MDTM templates and rf-task-builder

Depends on: Task 1

Covers: R-002, R-003, R-008.

In `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`: replace line 643's any-severity sentence with S1-S3 and S5 (indented to the I16 block), change line 655 to re-verify blocking items only (inventory 2.3), and change the I16 "After Max Reached" cells "Unresolved issues become Open Questions" (650, 652) and the lite rule "log as Open Questions and proceed" (803) to the inventory 3.1 replacement "HALT and escalate to the user with the open blocking findings; minor findings stay as notes.". In `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`: the same at 654, 671, 663, 665 and 820, plus the Multi-Agent Verdict Consolidation sentence at 656. In `src/superclaude/agents/rf-task-builder.md`: the "Open Questions" cells at 384 and 386. Numeric "Max Fix Cycles" values stay for Task 11.

Acceptance criteria:
- `git grep -n -i -E 'any severity|become Open Questions|log as Open Questions and proceed' -- src/superclaude/templates/workflow/01_mdtm_template_generic_task.md src/superclaude/templates/workflow/02_mdtm_template_complex_task.md src/superclaude/agents/rf-task-builder.md` prints nothing.
- Both MDTM templates contain S1, S2, S3 and S5; `uv run pytest tests/audit -q` passes (saved to `./artifacts/t5-audit.log`).

## Phase 3: Skills and rule prompts

## Task 6: Apply the rule to the prd and tdd skills

Depends on: Task 4

Covers: R-002, R-008.

Edit per inventory 2.4: `src/superclaude/skills/prd/refs/agent-prompts.md` lines 273 and 283 and `src/superclaude/skills/tdd/refs/agent-prompts.md` lines 282 and 291 (the shared prompt block, same replacement text as Task 4's `skill_template.md`), `src/superclaude/skills/prd/refs/build-request-template.md` lines 129 and 157, `src/superclaude/skills/tdd/refs/build-request-template.md` lines 124 and 152. Cap numbers stay for Task 11.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|must still be fixed|ALL findings must be resolved|\(CRITICAL, IMPORTANT, or MINOR\)' -- src/superclaude/skills/prd src/superclaude/skills/tdd` prints nothing.
- The Gap severity and FAIL lines in both `agent-prompts.md` files equal those in `src/superclaude/templates/documents/skill_template.md`; `uv run pytest tests/cli/prd/test_prompts.py -q` passes (saved to `./artifacts/t6-prd.log`).

## Task 7: Apply the rule to the tech-reference and tech-research skills

Depends on: Task 4

Covers: R-002, R-008.

Edit per inventory 2.4: `src/superclaude/skills/tech-reference/SKILL.md` lines 536, 878 and 886; `src/superclaude/skills/tech-research/SKILL.md` lines 567, 886, 894 and 1150. Cap numbers stay for Task 11.

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|must still be fixed|ALL findings must be resolved|0 minor' -- src/superclaude/skills/tech-reference/SKILL.md src/superclaude/skills/tech-research/SKILL.md` prints nothing.
- The shared prompt block lines equal those in `skill_template.md`; `uv run pytest tests/skills -q -k 'tech'` passes or selects no test (saved to `./artifacts/t7-tests.log`).

## Task 8: Apply the rule to the readme and operational-guide skills

Depends on: Task 4

Covers: R-002, R-008.

Edit per inventory 2.4: `src/superclaude/skills/readme/SKILL.md` lines 549, 609, 1007, 1029 and 1038; `src/superclaude/skills/operational-guide/SKILL.md` lines 514 (severity clause only), 982 and 990. Cap numbers stay for Task 11.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|must still be fixed|ALL findings must be resolved|Zero leniency' -- src/superclaude/skills/readme/SKILL.md src/superclaude/skills/operational-guide/SKILL.md` prints nothing.
- The shared prompt block lines equal those in `skill_template.md`; `uv run pytest tests/skills -q -k 'readme or operational'` passes or selects no test (saved to `./artifacts/t8-tests.log`).

## Task 9: Apply the rule and the at-cap escalation to the task and task-builder skills

Depends on: Task 5

Covers: R-002, R-003, R-008.

Edit `src/superclaude/skills/task/SKILL.md` line 347 and `src/superclaude/skills/task-builder/SKILL.md` lines 865, 869-870, 895 (the DNSP API-003-M6 clause, pre-review finding C2) and 1600 per inventory 2.2 and 2.4; change `task-builder/SKILL.md` line 873 ("After 3 rounds, proceed with remaining gaps as Open Questions in the task file") and line 1259 ("After max rounds, proceed with gaps as Open Questions in the task file") to the inventory 3.1 replacement, leaving the round numbers for Task 11.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|proceed with (remaining )?gaps as Open Questions|\(CRITICAL, IMPORTANT, or MINOR\)' -- src/superclaude/skills/task/SKILL.md src/superclaude/skills/task-builder/SKILL.md` prints nothing.
- `uv run pytest tests/skills/test_task_builder_merge.py tests/audit -q` passes (saved to `./artifacts/t9-tests.log`).

## Task 10: Apply the rule to the legacy QA rule prompts

Depends on: Task 1

Covers: R-002, R-008.

Edit per inventory 2.5: principle 1 "Zero tolerance: The batch must be perfect to pass" in `src/superclaude/rules/prompts/automated_qa_workflow_qa_prompt.md` (line 10), `src/superclaude/rules/prompts/doc_code_analyst_qa_prompt.md` (26), `src/superclaude/rules/prompts/documentation_expert_qa_prompt.md` (27) and `src/superclaude/rules/prompts/recruiting_expert_qa_prompt.md` (26), each followed by S1-S3 once; and the two cosmetic FAIL lines at `documentation_expert_qa_prompt.md:307-308`. The "EXACT means EXACT" checks stay.

Acceptance criteria:
- `git grep -n -E 'must be perfect to pass|Poor grammar/spelling/formatting = FAIL|Unclear or confusing writing = FAIL' -- src/superclaude/rules/prompts` prints nothing.
- Each of the four files contains S1, S2 and S3; `uv run pytest tests/cli/test_install_user_setup.py -q` passes (saved to `./artifacts/t10-install.log`).

## Phase 4: Review-loop caps

## Task 11: Lower every 3-cycle review-loop cap to 2 fix cycles

Depends on: Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Covers: R-004, R-007 (dnsp and task_builder_merge tests), R-008.

Apply inventory section 3.2 (CAP = 2 fix cycles, 3 reviews): every "Max 3 fix cycles" / "max 3 cycles" / "3 max per gate" / "[1 / 2 / 3 / N/A]" / "/ 3" / "3-fix-cycle" / "3-cycle" / "max-3-cycles" in a review-fix loop becomes 2 (`[1 / 2 / N/A]`, `/ 2`, `2-fix-cycle`, `2-cycle`, `max-2-cycles`), and every "After 3 cycles, HALT ..." becomes an at-cap clause using the canonical cap text. Files, each with the lines listed in inventory 3.2 including its "Additional 3-cycle sites" paragraph: `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/agents/rf-analyst.md`, `src/superclaude/agents/rf-team-lead.md` (line 462 becomes "max 2 cycles per phase"), `src/superclaude/agents/rf-task-builder.md`; `src/superclaude/templates/documents/agent_template_qa.md`, `src/superclaude/templates/documents/skill_template.md`, `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`, `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`; the modularization templates `qa-consolidated-findings_template.md`, `qa-cross-source-contradictions_template.md`, `qa-fix-summary_template.md`, `qa-research-depth_report_template.md`, `qa-research-evidence_report_template.md`, `qa-research-gap_report_template.md`, `qa-source-fidelity_template.md`, `qa-task-validation-b2_report_template.md`, `qa-task-validation-structure_report_template.md` under `src/superclaude/templates/modularization-template-review/`; `src/superclaude/skills/prd/refs/build-request-template.md`, `src/superclaude/skills/tdd/refs/build-request-template.md`; `SKILL.md` of `src/superclaude/skills/` `operational-guide`, `readme`, `roadmap`, `task`, `task-builder`, `tech-reference`, `tech-research`; `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md` (`max_iterations = 2`, `iteration < 2`, `iteration >= 2`, "2 iterations exhausted") and `src/superclaude/skills/sc-cli-portify-protocol/decisions.yaml` (ADR-SM01). Keep the excluded loops listed at the end of inventory 3.2 and the kept sites (`sc-roadmap-protocol`, `/sc:pr-submit`, `update.sh`). Compute the sha256 of the new `rf-team-lead.md` Fix Cycles line and put it in place of `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` in `rf-qa.md:82`, `rf-qa-qualitative.md:83`, `rf-analyst.md:74` and `task-builder/SKILL.md:901`; update `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt` to the new line bytes and `tests/audit/test_dnsp_all_agents_fail_bypass.py` (lines 14, 32, 77, 395-399, 640) to "max 2 cycles per phase", "max-2-cycles" and the new sha256; update the comment and any cap assertion at `tests/skills/test_task_builder_merge.py:435`.

Acceptance criteria:
- A case-insensitive `git grep -n -E` for `(max(imum)?|after) 3 (fix )?(cycles|rounds|iterations)`, `3-fix-cycle`, `3-cycle`, `max-3-cycles`, `max_iterations = 3`, `\[1 / 2 / 3` and `/ 3\b` over the files listed in this task prints only lines of the excluded loops named in inventory 3.2 (confidence-raising rounds, research and builder retries), each listed with its reason in `./artifacts/t11-cap-scan.txt`.
- The new sha256 appears in all four primitive files and the test file, `51725c0f` appears nowhere under `src/` or `tests/`, and `uv run pytest tests/audit tests/skills/test_task_builder_merge.py tests/skills/test_primitive_dual_surface_lookup.py tests/cli/prd/test_prompts.py -q` passes (saved to `./artifacts/t11-tests.log`).

## Task 12: Remove the second A2 repair from the /sc:implement retry ladder (option A)

Depends on: Task 1

Covers: R-005, R-008.

Re-read `src/superclaude/skills/sc-implement-protocol/refs/retry.md` and `refs/qa.md` first. In `refs/retry.md` Repair round: item 5 (valid names: j is always 1), item 6 (A2 timing: one A2 repair; drop the second-repair sentence), item 12 (resume: for n = 2 no second-repair branch), and any wording in items 1, 11 and 13 that allows a further A2 repair; in Cost and caps, recompute the "Worst case: 9 reviews instead of 2 (...)" line from the edited rules and drop "except the second A2 repair" from the Repairs line. In `refs/qa.md` change the row "A2 with repairs 1 and 2" (line 267) to name the single A2 repair. In `refs/ledger.md` change line 143 ("both repairs are unspent") and Resume rows S (`repair-2-<j>.md` → `repair-2-1.md`) and V to the single A2 repair. Keep attempts A3-A5, `halt review=5 reason=ladder-end`, the saved reviewer prompt (`refs/qa.md` Subagent prompt block) and the FINAL contract byte-identical. Copy each edited file byte for byte to `plugins/superclaude/skills/sc-implement-protocol/refs/`. Update `tests/skills/test_implement_severity_static.py` (the qa.md row pin at line 278), `tests/skills/test_implement_severity_replay.py` (`route()`'s second-A2 branch, `test_r_a3_late_blockers_local_second_a2_repair`, and the replay at lines 244-251 that expects two A2 repairs) and `tests/skills/test_task_workspace_lifecycle.py:582` (worst-case line pin), plus any test found by `git grep -n -E 'second A2|repair-2-2|repairs 1 and 2' -- tests`.

Acceptance criteria:
- `git grep -n -E 'second A2 repair|repairs 1 and 2|both repairs are unspent' -- src plugins` prints nothing; `git diff` shows no change inside the `refs/qa.md` Subagent prompt block or the FINAL contract text; `cmp` of each edited src file against its `plugins/superclaude/` twin is silent.
- `uv run pytest tests/skills/test_implement_severity_static.py tests/skills/test_implement_severity_replay.py tests/skills/test_task_workspace_lifecycle.py -q` plus every test file found by `git grep -l 'sc-implement-protocol' -- tests` pass (saved to `./artifacts/t12-tests.log`).

## Phase 5: Static test and release note

## Task 13: Add the static review-severity test and run the checks

Depends on: Task 10, Task 11, Task 12

Covers: R-006, R-008, R-010.

Create `tests/skills/test_review_severity_rule.py` with: a scan of every tracked text file under `src/`, `plugins/`, `commands/` and `agents/` (via `git ls-files`) that fails on the wordings "any issue of any severity", "issues of any severity", "gaps of any severity", "regardless of severity", "no severity level is exempt", "minor issues still pass", "must still be fixed", "still must be fixed" and "must be perfect to pass" (case-insensitive), with a parametrized negative case that feeds a scratch string to the scan function; S1-S5 present verbatim in `src/superclaude/output-styles/pragmatic.md`, read once from that file as the single source (the test extracts the five bullets and compares other files against them); S1-S3 present (whitespace-normalized) in `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/templates/documents/agent_template_qa.md`, both MDTM templates and the four `src/superclaude/rules/prompts/*_qa_prompt.md` files, and S5 in the first five; the canonical cap text present in `pragmatic.md`; no fix-cycle cap of 3 or more in the Task 11 files outside the inventory 3.2 exclusions, with a negative case on a scratch "Max 3 fix cycles" string; no "become Open Questions" / "as Open Questions and proceed" / "proceed with gaps as Open Questions" at-cap rule in the MDTM templates, `rf-task-builder.md` or `task-builder/SKILL.md`; every file edited by this plan that has a same-path twin under `plugins/superclaude/` is byte-equal to it. Then run `make sync-dev`, `make verify-sync` and `make lint` (install dev deps with `uv pip install -e ".[dev]"` if ruff is missing).

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py -v` passes, including the negative cases (saved to `./artifacts/t13-new-test.log`).
- `uv run pytest tests/audit tests/skills tests/cli/prd/test_prompts.py tests/cli/test_install_user_setup.py -q`, `make verify-sync` and `make lint` pass (saved to `./artifacts/t13-checks.log`); `git diff -U0 -- src plugins | grep '^+' | grep -n 'src/superclaude'` prints nothing.

## Task 14: Add the CHANGELOG entry

Depends on: Task 13

Covers: R-009.

Add an entry under `## [Unreleased]` in `CHANGELOG.md`: minor review findings are recorded as notes and never fail a review, are never rechecked and never trigger a fix pass; only blocking findings fail; review loops run at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings instead of turning them into Open Questions; `/sc:implement` drops the second A2 repair; citing the user decision and the QA-loop findings (`FINDINGS.md` bundle A).

Acceptance criteria:
- `CHANGELOG.md` has the entry under `## [Unreleased]`, naming `pragmatic.md`, the rf-qa agents, the MDTM templates, the 2-fix-cycle cap, the `/sc:implement` change and `tests/skills/test_review_severity_rule.py`.
