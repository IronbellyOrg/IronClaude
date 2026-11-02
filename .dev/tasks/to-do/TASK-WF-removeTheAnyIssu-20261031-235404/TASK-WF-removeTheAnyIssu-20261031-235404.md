---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeTheAnyIssu-20261031-235404
version: "1"
priority: High
created_date: "2026-10-31"
---

# Minor findings never fail a review; review loops capped at 2 rounds

Source: ./source.md
Goal: No shipped primitive fails a review on a minor finding or rechecks minors, every review loop stops at the cap and escalates open blocking findings to the user instead of passing them, and static tests pin the new rule.

## Constraints

- User decision (2026-10-31, verbatim): "Any severity fail rule: after review fails on minor, note them and proceed, do not recheck do not fail. Remove any severity rule. Limit review loops to 2."
- The site list, file:line and replacement wording for every edit is `.dev/review-severity-rule/inventory.md` (sections 1-6). Line numbers there are against commit `f90877be`; locate each site by its quoted text.
- Canonical rule text: sentences S1-S4 and the mapping sentence S5 in `.dev/review-severity-rule/inventory.md` section 1. Every edited QA agent, template and rule prompt carries S1-S3 word for word (whitespace and indentation may differ); files with a CRITICAL / IMPORTANT / MINOR scale also carry S5.
- Keep the binary PASS/FAIL verdict, the adversarial stance and the zero-finding Self-Audit (`src/superclaude/output-styles/pragmatic.md` lines 221, 222 and 224 at `f90877be`).
- Edit only `src/superclaude/`, `plugins/superclaude/` twins, `tests/` and `CHANGELOG.md`. Never edit or stage `.claude/` (except `.claude/settings.json`, which this plan does not touch); run `make sync-dev` after source edits.
- Never write a `src/superclaude/...` path into an installed primitive (commands, skills, agents, core, hooks, templates, rules, output styles); use `~/.claude/...` installed paths.
- Do not change any "Max N fix cycles" number (inventory section 3.2) or the `/sc:implement` retry ladder before the coordinator's answer; those are Tasks 14 and 15 only.
- Minor findings from this plan's own reviewers are noted, not fixed in extra rounds.
- Checks: the new and edited tests plus the tests that read edited files (named per task); `make verify-sync`; `make lint`. Never the full suite and never `tests/cli/eval/` as a directory.

## Phase 1: Canonical rule

## Task 1: Replace the any-severity bullet in the Pragmatic output style

Replace the bullet at `src/superclaude/output-styles/pragmatic.md:225` ("Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict, except inside a protocol that defines its own severity model, ...; a "minor issues still pass" allowance is PROHIBITED.") with the four bullets S1, S2, S3, S4 of inventory section 1, in that order. Leave the adversarial-stance, zero-finding Self-Audit and binary-verdict bullets unchanged. The SubagentStart hook (`src/superclaude/hooks/scripts/pragmatic-subagent.js`) reads the installed style file, so it needs no change.

Acceptance criteria:
- `git grep -n -i 'any severity' -- src/superclaude/output-styles/pragmatic.md` prints nothing, and `minor issues still pass` is absent from the file.
- The file contains S1, S2, S3 and S4 verbatim, and still contains "Every review agent MUST produce a binary verdict: PASS or FAIL.", "Treat a review that surfaces zero issues as suspect" and "Every review agent MUST begin its review from an adversarial position".

## Phase 2: QA agents and templates

## Task 2: Apply the rule to rf-qa

Depends on: Task 1

Edit `src/superclaude/agents/rf-qa.md` per inventory section 2.2 rows for `agents/rf-qa.md`: the DNSP references to "any gap regardless of severity = FAIL" (lines 82 and 84), principle 1 "Zero tolerance" (91), principle 8 NO LENIENCY (98), the research-gate Gap severity item (158-159), the research-gate Verdict bullets (171-172), the Fix Cycle phase re-verification scope (370-391: re-verify previously failed blocking items only), the SendMessage content "Must resolve ALL [N] issues" (464) and rule 10's "ALL findings regardless of severity must be resolved." (537). Add one "## Review severity rule" section after the Verification Principles holding S1-S3 and S5. Do not change any cap number (lines 82, 390, 393-406, 418, 537 keep their 3s for Task 14). The DNSP `rf-team-lead's Fix Cycles rule` text and its sha256 mention stay byte-identical.

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|still must be fixed' -- src/superclaude/agents/rf-qa.md` prints nothing.
- The file contains S1, S2, S3 and S5; the research-gate PASS bullet allows MINOR gaps as notes and the FAIL bullet names only CRITICAL or IMPORTANT gaps.
- "Maximum 3 fix cycles" still appears at the same two places (cap untouched), and `uv run pytest tests/audit -q` shows no failure other than the rf-qa verdict pins in `tests/audit/test_nfr_conv_9_zero_trust.py` that Task 12 updates (output saved to `./artifacts/t2-audit.log`).

## Task 3: Apply the rule to rf-qa-qualitative and rf-analyst

Depends on: Task 2

Edit `src/superclaude/agents/rf-qa-qualitative.md` per inventory 2.2: DNSP reference (83), NO LENIENCY (97), the eight PASS / FAIL verdict pairs (228-229, 279-280, 350-351, 417-418, 488-489, 555-556, 734-735, 772-773), the Fix Cycle phase (777-797: blocking items only; drop "ALL findings regardless of severity must be resolved.") and rule 10 (982), plus one "## Review severity rule" section with S1-S3 and S5 after the principles. Edit `src/superclaude/agents/rf-analyst.md` lines 93 (the "any gap regardless of severity = FAIL" reference), 148 and 199 ("must still be fixed") per inventory 2.2. Cap numbers stay.

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|must still be fixed' -- src/superclaude/agents/rf-qa-qualitative.md src/superclaude/agents/rf-analyst.md` prints nothing.
- `rf-qa-qualitative.md` contains S1, S2, S3 and S5 and has eight PASS bullets that allow MINOR issues as notes; `uv run pytest tests/audit -q` has no new failure beyond those named in Task 2 (saved to `./artifacts/t3-audit.log`).

## Task 4: Apply the rule to the QA agent template and shared document templates

Depends on: Task 1

Edit per inventory 2.3: `src/superclaude/templates/documents/agent_template_qa.md` (principle lists 95-96, NO LENIENCY 100, S5 under the MINOR definition at 139, verdict 156-157 plus S1-S3, message 262, rule N+3's severity clause at 335; its "Maximum 3" stays for Task 14); `src/superclaude/templates/modularization-template-review/analyst-completeness_report_template.md` lines 75 and 159; `src/superclaude/templates/documents/skill_template.md` lines 815 and 824 (the shared research-gate prompt block's Gap severity item and FAIL verdict).

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|must still be fixed|ALL findings must be resolved' -- src/superclaude/templates/documents/agent_template_qa.md src/superclaude/templates/documents/skill_template.md src/superclaude/templates/modularization-template-review/analyst-completeness_report_template.md` prints nothing.
- `agent_template_qa.md` contains S1, S2, S3 and S5.

## Task 5: Apply the rule and the at-cap escalation to the MDTM templates and rf-task-builder

Depends on: Task 1

In `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`: replace line 643's any-severity sentence with S1-S3 and S5 (indented to the I16 block), change line 655 to re-verify blocking items only (inventory 2.3), change the I16 "After Max Reached" cells "Unresolved issues become Open Questions" (650, 652) and the lite rule "log as Open Questions and proceed" (803) to the inventory 3.1 replacement. In `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`: the same at 654, 671, 663, 665 and 820, plus the Multi-Agent Verdict Consolidation sentence at 656. In `src/superclaude/agents/rf-task-builder.md`: the "Open Questions" cells at 384 and 386. Do not change any "Max Fix Cycles" number.

Acceptance criteria:
- `git grep -n -i -E 'any severity|become Open Questions|log as Open Questions and proceed' -- src/superclaude/templates/workflow/01_mdtm_template_generic_task.md src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` prints nothing, and `rf-task-builder.md` has no `| Open Questions |` cell.
- Both MDTM templates contain S1, S2, S3 and S5; the numeric "Max Fix Cycles" columns are unchanged from `f90877be` (`git diff` shows no digit change in those rows).

## Phase 3: Skills and rule prompts

## Task 6: Apply the rule to the prd and tdd skills

Depends on: Task 4

Edit per inventory 2.4: `src/superclaude/skills/prd/refs/agent-prompts.md` lines 273 and 283, `src/superclaude/skills/tdd/refs/agent-prompts.md` lines 282 and 291 (shared prompt block, same replacement text as Task 4's `skill_template.md`), `src/superclaude/skills/prd/refs/build-request-template.md` lines 129 and 157, `src/superclaude/skills/tdd/refs/build-request-template.md` lines 124 and 152. Cap numbers (prd 130, 149; tdd 125, 144) stay.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|must still be fixed|ALL findings must be resolved|\(CRITICAL, IMPORTANT, or MINOR\)' -- src/superclaude/skills/prd src/superclaude/skills/tdd` prints nothing.
- The Gap severity and FAIL lines in both `agent-prompts.md` files are byte-identical to those in `src/superclaude/templates/documents/skill_template.md`; `uv run pytest tests/cli/prd/test_prompts.py -q` passes (saved to `./artifacts/t6-prd.log`).

## Task 7: Apply the rule to the tech-reference and tech-research skills

Depends on: Task 4

Edit per inventory 2.4: `src/superclaude/skills/tech-reference/SKILL.md` lines 536, 878, 886; `src/superclaude/skills/tech-research/SKILL.md` lines 567, 886, 894, 1150. Cap numbers stay.

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|must still be fixed|ALL findings must be resolved|0 minor' -- src/superclaude/skills/tech-reference/SKILL.md src/superclaude/skills/tech-research/SKILL.md` prints nothing.
- The shared prompt block lines match `skill_template.md` byte for byte.

## Task 8: Apply the rule to the readme and operational-guide skills

Depends on: Task 4

Edit per inventory 2.4: `src/superclaude/skills/readme/SKILL.md` lines 549, 609, 1007, 1029, 1038; `src/superclaude/skills/operational-guide/SKILL.md` lines 514, 982, 990. Cap numbers stay.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|must still be fixed|ALL findings must be resolved|Zero leniency' -- src/superclaude/skills/readme/SKILL.md src/superclaude/skills/operational-guide/SKILL.md` prints nothing.
- The shared prompt block lines match `skill_template.md` byte for byte.

## Task 9: Apply the rule and the at-cap escalation to the task and task-builder skills

Depends on: Task 5

Edit `src/superclaude/skills/task/SKILL.md` line 347 and `src/superclaude/skills/task-builder/SKILL.md` lines 865, 870 and 1600 per inventory 2.4; change `task-builder/SKILL.md` lines 873 ("After 3 rounds, proceed with remaining gaps as Open Questions in the task file") and 1259 ("After max rounds, proceed with gaps as Open Questions in the task file") to the inventory 3.1 replacement, keeping their round numbers for Task 14.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|proceed with (remaining )?gaps as Open Questions|\(CRITICAL, IMPORTANT, or MINOR\)' -- src/superclaude/skills/task/SKILL.md src/superclaude/skills/task-builder/SKILL.md` prints nothing.
- `uv run pytest tests/skills/test_task_builder_merge.py -q` passes (saved to `./artifacts/t9-merge.log`).

## Task 10: Apply the rule to the legacy QA rule prompts

Depends on: Task 1

Edit per inventory 2.5: principle 1 "Zero tolerance: The batch must be perfect to pass" in `src/superclaude/rules/prompts/automated_qa_workflow_qa_prompt.md` (line 10), `src/superclaude/rules/prompts/doc_code_analyst_qa_prompt.md` (26), `src/superclaude/rules/prompts/documentation_expert_qa_prompt.md` (27) and `src/superclaude/rules/prompts/recruiting_expert_qa_prompt.md` (26), each followed by S1-S3 once; and the two cosmetic FAIL lines at `documentation_expert_qa_prompt.md:307-308`. The "EXACT means EXACT" checks stay.

Acceptance criteria:
- `git grep -n -E 'must be perfect to pass|Poor grammar/spelling/formatting = FAIL|Unclear or confusing writing = FAIL' -- src/superclaude/rules/prompts` prints nothing.
- Each of the four files contains S1, S2 and S3; `uv run pytest tests/cli/test_install_user_setup.py -q` passes (saved to `./artifacts/t10-install.log`).

## Phase 4: Tests and release note

## Task 11: Add the static review-severity test

Depends on: Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10

Create `tests/skills/test_review_severity_rule.py` with: (a) a scan of every tracked text file under `src/`, `plugins/`, `commands/` and `agents/` that fails on the wordings "any issue of any severity", "issues of any severity", "gaps of any severity", "regardless of severity", "no severity level is exempt", "minor issues still pass", "must still be fixed" and "must be perfect to pass" (case-insensitive); (b) S1-S4 present verbatim in `src/superclaude/output-styles/pragmatic.md`; (c) S1-S3 present (whitespace-normalized) in `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/templates/documents/agent_template_qa.md`, both MDTM templates and the four `src/superclaude/rules/prompts/*_qa_prompt.md` files, and S5 in the first five; (d) no "become Open Questions" / "as Open Questions and proceed" at-cap rule in the MDTM templates, `rf-task-builder.md` or `task-builder/SKILL.md`; (e) every tracked file under `plugins/superclaude/` that has a same-path twin under `src/superclaude/` is byte-equal to it. The test reads the canonical sentences from `pragmatic.md` once and compares the other files against them, so the wording has one source.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py -v` passes (saved to `./artifacts/t11-new-test.log`).
- Reintroducing "Any issue of any severity (CRITICAL, IMPORTANT, or MINOR) results in FAIL." into a scratch copy is detected by the scan function (a parametrized negative case inside the test file, not an edit to a shipped file).

## Task 12: Update tests that pinned the old wording

Depends on: Task 2, Task 11

Update `tests/skills/test_implement_severity_static.py` pin P1 (`test_p1_output_style_exempts_implement_severity_model`, which reads the old `pragmatic.md:225` bullet) to assert the new S2 and S4 text instead; keep P2-P4 unchanged. Update `tests/audit/test_nfr_conv_9_zero_trust.py`: the `PASS_BULLET` / `FAIL_BULLET` constants to the new rf-qa research-gate bullets, `_score_rf_qa_verdict` to fail only on CRITICAL or IMPORTANT gap rows, the one-MINOR-gap case to expect PASS, and add a one-IMPORTANT-gap case expecting FAIL (new fixture `tests/audit/fixtures/nfr_conv_9/one_important_finding.md`). Update the prose in `tests/audit/fixtures/nfr_conv_9/one_low_finding.md` and `tests/audit/fixtures/nfr_conv_9/zero_findings_baseline.md` (lines 9 and 35) that quotes the old rule.

Acceptance criteria:
- `uv run pytest tests/audit tests/skills/test_implement_severity_static.py tests/skills/test_review_severity_rule.py tests/skills/test_task_builder_merge.py tests/skills/test_primitive_dual_surface_lookup.py tests/cli/test_install_user_setup.py tests/cli/prd/test_prompts.py -q` passes (saved to `./artifacts/t12-tests.log`).
- `make verify-sync` and `make lint` pass after `make sync-dev` (saved to `./artifacts/t12-sync-lint.log`).

## Task 13: Add the CHANGELOG entry

Depends on: Task 12

Add an entry under `## [Unreleased]` in `CHANGELOG.md`: minor review findings are recorded as notes and never fail a review or trigger a fix pass; only blocking findings fail; at-cap blocking findings halt and escalate instead of becoming Open Questions; citing the user decision of 2026-10-31 and the QA-loop findings. Add the cap and `/sc:implement` lines only after Tasks 14 and 15 land.

Acceptance criteria:
- `CHANGELOG.md` has the entry under `## [Unreleased]`, naming `pragmatic.md`, the rf-qa agents, the MDTM templates and `tests/skills/test_review_severity_rule.py`.

## Phase 5: Pending decisions (apply after the coordinator's answers)

## Task 14: Apply the 2-round cap number

Depends on: Task 13

Before starting, read the coordinator's answer on what counts as a round (`orca orchestration check`). With CAP = 1 fix cycle (a round is one review pass) or CAP = 2 fix cycles (a round is one fix cycle), lower every number above CAP in the sites of inventory section 3.2 to CAP and make every at-cap clause "HALT and escalate to the user with the open blocking findings": `src/superclaude/agents/rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, `rf-team-lead.md`, `rf-task-builder.md`; `src/superclaude/templates/documents/agent_template_qa.md`, `skill_template.md`; both MDTM templates (I16 and I22 tables and prose); the ten `src/superclaude/templates/modularization-template-review/*` "/ 3" fields; `src/superclaude/skills/{prd,tdd}/refs/build-request-template.md`; `src/superclaude/skills/{operational-guide,readme,roadmap,task,task-builder,tech-reference,tech-research}/SKILL.md`; `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` and `refs/validation.md`; `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md` and `decisions.yaml`; and, only if the coordinator says the cap covers it, `src/superclaude/commands/pr-submit.md`, `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md` and its FSM. Update `tests/audit/test_dnsp_all_agents_fail_bypass.py` and `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt` to the new `rf-team-lead.md` line and sha256, and extend `tests/skills/test_review_severity_rule.py` with a scan that fails on any fix-cycle cap above CAP. Add the cap line to the CHANGELOG entry.

Acceptance criteria:
- The extended scan in `tests/skills/test_review_severity_rule.py` passes and fails on a scratch "Max 3 fix cycles" string; the Task 12 test command, `make verify-sync` and `make lint` pass (saved to `./artifacts/t14-tests.log`).
- No site of inventory 3.2 keeps a number above CAP, except the excluded loops listed at the end of inventory 3.2.

## Task 15: Apply the /sc:implement ladder decision

Depends on: Task 14

Before starting, read the coordinator's answer (option A, B or C of inventory section 4 decision 2). B: no change; record it in the CHANGELOG entry. A: in `src/superclaude/skills/sc-implement-protocol/refs/retry.md` remove the attempt-2 repairs (Repair round items 5, 6 and 12 and the "Cost and caps" worst case at line 189), so a blocker still open after the A2 review goes straight to the adviser route; align `refs/qa.md` (Interruption table row "A2 with repairs 1 and 2", the A2 row of the audit table) and `refs/ledger.md` (Resume rows that name the second A2 repair); copy each edited file byte for byte to `plugins/superclaude/skills/sc-implement-protocol/refs/`; update the implement tests that pin the second A2 repair (`tests/skills/test_implement_severity_static.py::test_retry_repair_round_rules` and any test found by `git grep -n 'second A2 repair\|repair-2-2' -- tests`). C: escalate to the coordinator before editing, because it removes the `halt review=5 reason=ladder-end` contract. Do not change the closed reviewer template (`refs/qa.md` Subagent prompt block) or the FINAL contract.

Acceptance criteria:
- For A: `git grep -n 'second A2 repair' -- src plugins` prints nothing, src and plugin twins are byte-equal, and `uv run pytest tests/skills/test_implement_severity_static.py tests/skills/test_review_severity_rule.py -q` plus every test found by `git grep -l 'sc-implement-protocol' -- tests` pass (saved to `./artifacts/t15-tests.log`).
- For B: the CHANGELOG entry states that `/sc:implement` keeps its own ladder as its at-cap escalation; `make verify-sync` and `make lint` pass.
