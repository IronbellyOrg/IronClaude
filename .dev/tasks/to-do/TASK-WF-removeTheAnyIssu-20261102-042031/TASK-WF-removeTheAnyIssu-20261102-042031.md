---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeTheAnyIssu-20261102-042031
version: "1"
priority: High
created_date: "2026-11-02"
---

# Minor findings never fail a review; review loops capped at 2 fix cycles (regenerated)

Source: ./source.md
Goal: No shipped primitive, CLI default or CLI prompt fails a review on a minor finding or rechecks minors; every review loop outside /sc:implement runs at most 2 fix cycles (3 reviews) and then escalates the open blocking findings to the user; /sc:implement drops its second A2 repair and keeps its own ladder as its at-cap escalation under S4; static tests pin all of it.

## Constraints

- Final user decisions (restart spec `/tmp/t11b-severity-rule-restart-spec.md`): B1 minor findings are noted and work proceeds, with no recheck and no FAIL; B2 the cap is 2 fix cycles = at most 3 reviews, caps of 2 stay, caps of 3 or more and uncapped loops drop to 2; B3 `/sc:implement` option A; `update.sh` is not changed. Evidence: `/home/coder/workspaces/IronClaude/.dev/worktrees/qa-loop-investigation/.dev/qa-loop-investigation/FINDINGS.md` sections 4 and 5.
- This plan replaces package `TASK-WF-removeTheAnyIssu-20261101-225635`; its pre-review merged verdict (`.dev/reflect/pre-removeTheAnyIssu-20261101225845/adversarial/merged-verdict.md`, findings B-01..B-11) is folded in below. Scope decision R-011: the rule and the cap cover `src/superclaude/cli/` defaults and prompt strings too.
- Site lists (repo-relative): severity wording `.dev/review-severity-rule/inventory.md` sections 1, 2, 3.1, 4 and 6; cap numbers `.dev/review-severity-rule/cap-sites.md` (138 IN rows, every row gives the replacement text; it supersedes inventory section 3.2). Line numbers are against `f90877be`; locate each site by its quoted text.
- Canonical text: S1-S5 of inventory section 1, held in `src/superclaude/output-styles/pragmatic.md`. The S1-S3 file set (R-002) is exactly: `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/templates/documents/agent_template_qa.md`, `src/superclaude/templates/documents/skill_template.md`, `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`, `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (these six also carry S5) and the four `src/superclaude/rules/prompts/*_qa_prompt.md` files. Canonical cap text: "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings"; at-cap clause form: "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings".
- CAP_PATTERN (used by every cap task and by the Task 17 test; case-insensitive extended regex): `(max(imum)?|after|up to)[^.|]{0,20}\b[3-9]\b[^.|]{0,12}(fix[- ]?)?(cycles?|rounds?|iterations?|attempts?)|\b[3-9]-(fix-)?cycles?\b|max-[3-9]-cycles|fix cycles?: [3-9]\b|(failing|failed) [3-9] fix cycles|\| [3-9] \||/ [3-9]\b|\[1 / 2 / 3|[2-9]-[3-9] per gate|(max_iterations|max_convergence|max_research_fix_cycles)(: int)? ?= ?[3-9]`. A cap task passes its scan when `git grep -n -i -E "<CAP_PATTERN>" -- <its files>` prints only lines that cap-sites.md marks OUT; the task saves the output with the OUT reason per line to its `./artifacts/` scan file.
- Keep the binary PASS/FAIL verdict, the adversarial stance and the zero-finding Self-Audit bullets of `pragmatic.md`. Shared FAIL-line replacements keep "Only PASS or FAIL — no conditional pass." and each file's own "List each ..." suffix.
- Edit only `src/superclaude/`, `plugins/superclaude/` twins, `tests/` and `CHANGELOG.md`. Never edit or stage `.claude/` (except `.claude/settings.json`, untouched here). `.dev/tasks/` is always staged.
- R-010: `.claude/agents`, `.claude/skills` and `.claude/templates` are absent in this worktree, and many `tests/audit` tests compare `src/` with those mirrors, so every task runs `make sync-dev` before its pytest command.
- R-008: never add a `src/superclaude/...` path to an installed primitive. Every task that edits a primitive checks `git diff -U0 -- <its primitive files> | grep '^+[^+]' | grep -n 'src/superclaude'` prints nothing.
- Minor findings from this plan's own reviewers are noted, not fixed in extra rounds. Kept as notes, not tasks: cli_portify's latent caller (panel_review submits one iteration), rule 9 "When in doubt, fail it" (`rf-qa-qualitative.md:981`), `docs/guides/tdd-skill-release-guide.md:265, 271` (outside scope), S1-S3 not copied into the seven skill prompt-block copies.
- Checks are the tests named per task plus tests that read edited files; `make verify-sync`; `make lint`. Never the full suite and never `tests/cli/eval/` as a directory. Commit, push and `/sc:pr-submit` are done by the operator after this plan.

## Phase 1: Canonical rule

## Task 1: Replace the any-severity bullet in the Pragmatic output style

Covers: R-001, R-007 (pin P1), R-008.

Replace the bullet in `src/superclaude/output-styles/pragmatic.md` that begins "Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict" with S1, S2, S3, S4, S5 of inventory section 1, in that order, without the "(S1)".."(S5)" labels and without the S3 parenthetical annotation. Leave the adversarial-stance, zero-finding Self-Audit and binary-verdict bullets unchanged; the five new bullets follow the binary-verdict bullet directly. Update pin P1 in `tests/skills/test_implement_severity_static.py` (`test_p1_output_style_exempts_implement_severity_model`) to assert the new S2 and S4 text; keep P2-P4.

Acceptance criteria:
- `git grep -n -i -E 'any severity|minor issues still pass' -- src/superclaude/output-styles/pragmatic.md` prints nothing; the file contains S1-S5 verbatim right after "Every review agent MUST produce a binary verdict: PASS or FAIL.", S3 contains the canonical cap text, and the adversarial-stance and zero-finding bullets are unchanged.
- `make sync-dev` then `uv run pytest tests/skills/test_implement_severity_static.py -q` passes (saved to `./artifacts/t1-static.log`).

## Phase 2: QA agents, templates and the pinned rf-team-lead line

## Task 2: Apply the rule to rf-qa and its verdict test

Depends on: Task 1

Covers: R-002, R-007 (nfr_conv_9), R-008, R-010.

Edit `src/superclaude/agents/rf-qa.md` per the inventory section 2.2 rows for `agents/rf-qa.md`: the DNSP references to "any gap regardless of severity = FAIL" (lines 82 and 84, wording only), principle 1 "Zero tolerance" (91), principle 8 NO LENIENCY (98), the research-gate Gap severity items (158-159), the research-gate Verdict bullets (171-172), the Fix Cycle phase re-verification scope (370-391: blocking items only), "Must resolve ALL [N] issues" (464) and rule 10's severity clause (537). Add one "## Review severity rule" section after the Verification Principles holding S1-S3 and S5. Do not change cap numbers, the "max-3-cycles" token or the sha256 on line 82 (Tasks 6 and 12). Update `tests/audit/test_nfr_conv_9_zero_trust.py`: `PASS_BULLET` / `FAIL_BULLET` to the new bullets, the scorer to fail only on CRITICAL or IMPORTANT gap rows, the one-MINOR case to expect PASS (rename fail-named classes and tests such as `TestPartA_OneLowFindingFailsGate`, `test_gate_returns_fail`, and the docstring and assert text at lines 6-12 and 246), and a new one-IMPORTANT case expecting FAIL with fixture `tests/audit/fixtures/nfr_conv_9/one_important_finding.md`; update the prose in `tests/audit/fixtures/nfr_conv_9/one_low_finding.md` (lines 13, 45; keep the "NFR-CONV.9 part (a)" marker) and `tests/audit/fixtures/nfr_conv_9/zero_findings_baseline.md` (lines 9, 35).

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|still must be fixed' -- src/superclaude/agents/rf-qa.md` prints nothing; the file contains S1, S2, S3 and S5; the PASS bullet allows MINOR gaps as notes and the FAIL bullet names only CRITICAL or IMPORTANT gaps.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t2-audit.log`).

## Task 3: Apply the rule to rf-qa-qualitative and rf-analyst and re-pin the Critical Rules hash

Depends on: Task 2

Covers: R-002, R-004 (rule 10 cap), R-007 (BASELINE_BLOCK_SHA), R-008, R-010.

Edit `src/superclaude/agents/rf-qa-qualitative.md` per inventory 2.2: the DNSP reference (83, wording only; sha and "max-3-cycles" stay for Task 6), NO LENIENCY (97), the eight PASS / FAIL pairs (228-229, 279-280, 350-351, 417-418, 488-489, 555-556, 734-735, 772-773), the Fix Cycle phase (777-797: blocking items only), and rule 10 at line 982 in full: both its severity clause and its cap, using cap-sites.md section 1 row `rf-qa-qualitative.md:982`, so the Critical Rules block changes only in this task. Add one "## Review severity rule" section with S1-S3 and S5 after the principles. Edit `src/superclaude/agents/rf-analyst.md` per inventory 2.2: the DNSP API-003-M6 clause on line 74 (wording only), line 93, and lines 148 and 199. Recompute `BASELINE_BLOCK_SHA` in `tests/audit/test_severity_floor_unweakened.py` (line 48) for the new Critical Rules block with a comment citing this change; keep `BASELINE_SLICE_SHA`, the Rule 6 verbatim check and the softening-token check.

Acceptance criteria:
- `git grep -n -i -E 'any severity|issues of any severity|regardless of severity|no severity level is exempt|must still be fixed' -- src/superclaude/agents/rf-qa-qualitative.md src/superclaude/agents/rf-analyst.md` prints nothing; `rf-qa-qualitative.md` contains S1, S2, S3 and S5, eight PASS bullets that allow MINOR issues as notes, and rule 10 reads "Maximum 2 fix cycles" with the at-cap clause form.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t3-audit.log`).

## Task 4: Apply the rule to the QA agent template, the skill template and the shared document templates

Depends on: Task 1

Covers: R-002, R-008, R-010.

Edit per inventory 2.2 and 2.3: `src/superclaude/templates/documents/agent_template_qa.md` (principle lists 95-96, NO LENIENCY 100, S5 under the MINOR definition at 139, verdict 156-157 plus S1-S3, message 262, the severity clause of rule N+3 at 335; caps stay for Task 12); `src/superclaude/templates/documents/skill_template.md` lines 815 and 824 (Gap severity item and FAIL verdict of the shared research-gate prompt block; the FAIL line keeps "Only PASS or FAIL — no conditional pass.") plus S1-S3 and S5 added once inside that prompt block; `src/superclaude/templates/modularization-template-review/analyst-completeness_report_template.md` lines 75 and 159; `src/superclaude/templates/modularization-template-review/synthetic-dnsp-finding.contract` line 52.

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|must still be fixed|ALL findings must be resolved' -- src/superclaude/templates/documents/agent_template_qa.md src/superclaude/templates/documents/skill_template.md src/superclaude/templates/modularization-template-review/analyst-completeness_report_template.md src/superclaude/templates/modularization-template-review/synthetic-dnsp-finding.contract` prints nothing; `agent_template_qa.md` and `skill_template.md` each contain S1, S2, S3 and S5.
- `make sync-dev` then `uv run pytest tests/audit tests/skills/test_task_builder_merge.py -q` passes (saved to `./artifacts/t4-tests.log`).

## Task 5: Apply the rule and the at-cap escalation to the MDTM templates and rf-task-builder

Depends on: Task 1

Covers: R-002, R-003, R-008, R-010.

In `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`: replace line 643's any-severity sentence with S1-S3 and S5 (indented to the I16 block), change line 655 to re-verify blocking items only, and change the I16 "After Max Reached" cells "Unresolved issues become Open Questions" (650, 652) and the lite rule "log as Open Questions and proceed" (803) to "HALT and escalate to the user with the open blocking findings; minor findings stay as notes.". In `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`: the same at 654, 671, 663, 665 and 820, plus the Multi-Agent Verdict Consolidation sentence at 656. In `src/superclaude/agents/rf-task-builder.md`: the "Open Questions" cells at 384 and 386. Numeric cap values stay for Task 12.

Acceptance criteria:
- `git grep -n -i -E 'any severity|become Open Questions|log as Open Questions and proceed' -- src/superclaude/templates/workflow/01_mdtm_template_generic_task.md src/superclaude/templates/workflow/02_mdtm_template_complex_task.md src/superclaude/agents/rf-task-builder.md` prints nothing; both MDTM templates contain S1, S2, S3 and S5.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t5-audit.log`).

## Task 6: Rewrite the pinned rf-team-lead Fix Cycles line and propagate its sha256

Depends on: Task 3

Covers: R-004, R-007 (dnsp test), R-012, R-008, R-010.

Rewrite `src/superclaude/agents/rf-team-lead.md:462` ("**Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings.") so a FIX pipeline runs only for blocking findings (minor findings are recorded as notes), the cap reads "max 2 cycles per phase", and the at-cap sentence still contains "HALT and ask user" plus "with the open blocking findings". Compute the sha256 of the new line exactly as `tests/audit/test_dnsp_all_agents_fail_bypass.py` does (fixture bytes, trailing newline included). In one change: replace `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` with the new sha in `src/superclaude/agents/rf-qa.md:82`, `src/superclaude/agents/rf-qa-qualitative.md:83`, `src/superclaude/agents/rf-analyst.md:74` and `src/superclaude/skills/task-builder/SKILL.md:901`, and change "max-3-cycles" to "max-2-cycles" on those four lines; write the new line to `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt`; update `tests/audit/test_dnsp_all_agents_fail_bypass.py` (lines 14, 32, 77, 395-399, 640) to the new sha, "max 2 cycles per phase" and "max-2-cycles".

Acceptance criteria:
- `git grep -n '51725c0f' -- src tests plugins` prints nothing; the new sha appears in the four primitive lines and the test; `git grep -n -i 'max-3-cycles\|max 3 cycles per phase' -- src tests` prints nothing.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t6-audit.log`).

## Phase 3: Skills, CLI prompt and rule prompts

## Task 7: Apply the rule to the prd and tdd skills and the prd CLI prompt

Depends on: Task 4

Covers: R-002, R-011 (prompt), R-008, R-010.

Edit per inventory 2.4: `src/superclaude/skills/prd/refs/agent-prompts.md` lines 273 and 283 and `src/superclaude/skills/tdd/refs/agent-prompts.md` lines 282 and 291 (same Gap severity and FAIL text as Task 4's `skill_template.md`), `src/superclaude/skills/prd/refs/build-request-template.md` lines 129 and 157, `src/superclaude/skills/tdd/refs/build-request-template.md` lines 124 and 152, and the same Gap severity and FAIL lines in the Python prompt string `src/superclaude/cli/prd/prompts.py` (lines 1164 and 1173, ASCII "--" kept as in that file). Cap numbers stay for Task 13.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|must still be fixed|ALL findings must be resolved|\(CRITICAL, IMPORTANT, or MINOR\)' -- src/superclaude/skills/prd src/superclaude/skills/tdd src/superclaude/cli/prd/prompts.py` prints nothing; the Gap severity and FAIL lines of both `agent-prompts.md` files equal those of `skill_template.md`.
- `make sync-dev` then `uv run pytest tests/cli/prd -q` passes (saved to `./artifacts/t7-prd.log`).

## Task 8: Apply the rule to the tech-reference and tech-research skills

Depends on: Task 4

Covers: R-002, R-008, R-010.

Edit per inventory 2.4: `src/superclaude/skills/tech-reference/SKILL.md` lines 536, 878 and 886; `src/superclaude/skills/tech-research/SKILL.md` lines 567, 886, 894 and 1150. The shared FAIL lines keep "Only PASS or FAIL — no conditional pass.". Cap numbers stay for Task 13.

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|must still be fixed|ALL findings must be resolved|0 minor' -- src/superclaude/skills/tech-reference/SKILL.md src/superclaude/skills/tech-research/SKILL.md` prints nothing; the shared Gap severity and FAIL lines equal those of `skill_template.md`.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t8-tests.log`).

## Task 9: Apply the rule to the readme and operational-guide skills

Depends on: Task 4

Covers: R-002, R-008, R-010.

Edit per inventory 2.4: `src/superclaude/skills/readme/SKILL.md` lines 549, 609, 1007, 1029 and 1038 (the FAIL lines keep "List each with specific remediation."), and the severity sentence "ALL findings must be resolved" inside the summary line 2034 (merged verdict B-02); `src/superclaude/skills/operational-guide/SKILL.md` lines 514 (severity clause only), 982 and 990 (keep "Only PASS or FAIL — no conditional pass. List each finding with specific remediation."), and the same severity sentence inside the summary line 1349. Cap numbers on these lines stay for Task 13.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|must still be fixed|ALL findings must be resolved|Zero leniency' -- src/superclaude/skills/readme/SKILL.md src/superclaude/skills/operational-guide/SKILL.md` prints nothing; the shared Gap severity line equals `skill_template.md`'s.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t9-tests.log`).

## Task 10: Apply the rule and the at-cap escalation to the task and task-builder skills

Depends on: Task 5, Task 6

Covers: R-002, R-003, R-008, R-010.

Edit `src/superclaude/skills/task/SKILL.md` line 347 and `src/superclaude/skills/task-builder/SKILL.md` lines 865, 869-870, 895 (DNSP API-003-M6 clause, wording only) and 1600 per inventory 2.2 and 2.4; change `task-builder/SKILL.md` line 873 ("After 3 rounds, proceed with remaining gaps as Open Questions in the task file") and line 1259 ("After max rounds, proceed with gaps as Open Questions in the task file") to "HALT and escalate to the user with the open blocking findings", leaving their round numbers for Task 14.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|proceed with (remaining )?gaps as Open Questions|\(CRITICAL, IMPORTANT, or MINOR\)' -- src/superclaude/skills/task/SKILL.md src/superclaude/skills/task-builder/SKILL.md` prints nothing.
- `make sync-dev` then `uv run pytest tests/skills/test_task_builder_merge.py tests/audit tests/cli/reflect/test_no_nesting_guard.py tests/troubleshoot/backtest/test_backtest_e5.py -q` passes (saved to `./artifacts/t10-tests.log`).

## Task 11: Apply the rule to the legacy QA rule prompts

Depends on: Task 1

Covers: R-002, R-008, R-010.

Edit per inventory 2.5: principle 1 "Zero tolerance: The batch must be perfect to pass" in `src/superclaude/rules/prompts/automated_qa_workflow_qa_prompt.md` (line 10), `src/superclaude/rules/prompts/doc_code_analyst_qa_prompt.md` (26), `src/superclaude/rules/prompts/documentation_expert_qa_prompt.md` (27) and `src/superclaude/rules/prompts/recruiting_expert_qa_prompt.md` (26), each followed by S1-S3 once; and the two cosmetic FAIL lines at `documentation_expert_qa_prompt.md:307-308`. The "EXACT means EXACT" checks stay.

Acceptance criteria:
- `git grep -n -E 'must be perfect to pass|Poor grammar/spelling/formatting = FAIL|Unclear or confusing writing = FAIL' -- src/superclaude/rules/prompts` prints nothing; each of the four files contains S1, S2 and S3.
- `make sync-dev` then `uv run pytest tests/cli/test_install_user_setup.py -q` passes (saved to `./artifacts/t11-install.log`).

## Phase 4: Review-loop caps

## Task 12: Lower the caps in the agents and templates

Depends on: Task 3, Task 4, Task 5, Task 6

Covers: R-004, R-007 (task_builder_merge comment), R-008, R-010.

Apply every IN row of cap-sites.md sections 1, 13, 14 and 15 except the rows already done (`rf-qa-qualitative.md:982` in Task 3; the DNSP lines and `rf-team-lead.md:462` in Task 6): `src/superclaude/agents/rf-qa.md` (390, 393, 395, 403, 406, 418, 537), `src/superclaude/agents/rf-qa-qualitative.md` (797, 827), `src/superclaude/agents/rf-task-builder.md` (383, 385, 387), `src/superclaude/templates/documents/agent_template_qa.md` (184, 210, 320, 335), `src/superclaude/templates/documents/skill_template.md` (427), the nine `qa-*` templates in `src/superclaude/templates/modularization-template-review/` named in section 14, and the MDTM templates (`01_mdtm_template_generic_task.md` 649, 651, 653, 787; `02_mdtm_template_complex_task.md` 662, 664, 666, 667, 753, 804, 1090, 1119). Update the "3-fix-cycle" comment at `tests/skills/test_task_builder_merge.py:435`.

Acceptance criteria:
- The CAP_PATTERN scan over the files above prints only cap-sites.md OUT lines (confidence-raising rounds and agent counts), each listed with its reason in `./artifacts/t12-cap-scan.txt`; every replaced at-cap clause uses the at-cap clause form.
- `make sync-dev` then `uv run pytest tests/audit tests/skills/test_task_builder_merge.py -q` passes (saved to `./artifacts/t12-tests.log`).

## Task 13: Lower the caps in the operational-guide, readme, roadmap, tech-reference and tech-research skills and the build-request templates

Depends on: Task 7, Task 8, Task 9

Covers: R-004, R-008, R-010.

Apply every IN row of cap-sites.md sections 4, 5, 6, 9, 10 and 11: `src/superclaude/skills/operational-guide/SKILL.md` (including the "Max fix cycles: 3" summary at 1349 and the allowed-halt rule "phase-gate QA failing 3 fix cycles" at 1371), `src/superclaude/skills/readme/SKILL.md` (including 2034 and 2058), `src/superclaude/skills/roadmap/SKILL.md` (including 2587 and the sentinel gate at 554), `src/superclaude/skills/tech-reference/SKILL.md` (including 177, 512, 529, 1307 and 1327), `src/superclaude/skills/tech-research/SKILL.md` (including 1643), `src/superclaude/skills/prd/refs/build-request-template.md` (130) and `src/superclaude/skills/tdd/refs/build-request-template.md` (125).

Acceptance criteria:
- The CAP_PATTERN scan over these seven files prints only cap-sites.md OUT lines, each listed with its reason in `./artifacts/t13-cap-scan.txt`.
- `make sync-dev` then `uv run pytest tests/audit tests/skills -q` passes (saved to `./artifacts/t13-tests.log`).

## Task 14: Lower the caps in the task and task-builder skills

Depends on: Task 10

Covers: R-004, R-008, R-010.

Apply every IN row of cap-sites.md sections 7 and 8: `src/superclaude/skills/task-builder/SKILL.md` (including 204, 872-873, 1275, 1310, 1420, 1471 and the allowed-halt rule at 2369) and `src/superclaude/skills/task/SKILL.md` (including 120, 254, 336, 366, 368, 405, 477 and 616).

Acceptance criteria:
- The CAP_PATTERN scan over the two files prints only cap-sites.md OUT lines (the closed-vocabulary identifier `gap-fill-round-3` is not matched by the pattern), each listed with its reason in `./artifacts/t14-cap-scan.txt`.
- `make sync-dev` then `uv run pytest tests/skills tests/audit tests/cli/reflect/test_no_nesting_guard.py tests/troubleshoot/backtest/test_backtest_e5.py -q` passes (saved to `./artifacts/t14-tests.log`).

## Task 15: Lower the cli-portify convergence cap in code, skill and tests

Depends on: Task 1

Covers: R-004, R-011, R-007 (test_convergence), R-008, R-010.

Apply every IN row of cap-sites.md sections 2 (cli_portify rows) and 12: `src/superclaude/cli/cli_portify/convergence.py` (149 docstring, 165 default), `src/superclaude/cli/cli_portify/steps/panel_review.py:352`, `src/superclaude/cli/cli_portify/commands.py:100-101` (`--max-convergence` default and help text 2; the user may still raise it), `src/superclaude/cli/cli_portify/config.py:53`, `src/superclaude/cli/cli_portify/models.py:583`, `src/superclaude/cli/cli_portify/prompts.py:68`, `src/superclaude/cli/cli_portify/resume.py:136`, `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md` (355, 363, 364, 367, 374, 534) and `src/superclaude/skills/sc-cli-portify-protocol/decisions.yaml` (121, 123). Rewrite `tests/cli_portify/test_convergence.py:78-86` (`test_default_max_iterations_is_3`) for a default of 2 (escalates after the second unresolved iteration).

Acceptance criteria:
- The CAP_PATTERN scan over these ten source files prints only cap-sites.md OUT lines (score means `/ 4`), listed in `./artifacts/t15-cap-scan.txt`.
- `make sync-dev` then `uv run pytest tests/cli_portify -q` passes (saved to `./artifacts/t15-tests.log`); `make lint` passes on the edited Python files.

## Task 16: Lower the prd CLI research fix-cycle cap and the ib_agent_core correction loop

Depends on: Task 7

Covers: R-004, R-011, R-013, R-008, R-010.

Set `max_research_fix_cycles` in `src/superclaude/cli/prd/models.py:203` to 2 (`executor.py:1157` runs `range(max_cycles + 1)`, so 2 gives 2 fix cycles and 3 QA runs). In `src/superclaude/rules/core/ib_agent_core.md`: line 633 "Maximum 5 correction attempts per batch" becomes 2, line 913 "Manual intervention needed after 3 attempts" becomes 2, and line 933 states that the rule requires `MAX_CORRECTION_ATTEMPTS` set to 2 (at most 2 fix cycles, 3 reviews) without claiming the external `automated_qa_workflow.sh` default changed.

Acceptance criteria:
- `git grep -n -E 'max_research_fix_cycles: int = [3-9]' -- src` prints nothing; `git grep -n -E 'Maximum [3-9] correction attempts|after [3-9] attempts' -- src/superclaude/rules/core/ib_agent_core.md` prints nothing.
- `make sync-dev` then `uv run pytest tests/cli/prd tests/unit/test_cli_install.py -q` passes (saved to `./artifacts/t16-tests.log`).

## Task 17: Remove the second A2 repair from the /sc:implement retry ladder (option A)

Depends on: Task 1

Covers: R-005, R-014, R-008, R-010.

Re-read `src/superclaude/skills/sc-implement-protocol/refs/retry.md` and `refs/qa.md` first. In `refs/retry.md` Repair round: item 5 (j is always 1), item 6 (one A2 repair; drop the second-repair sentence), item 12 (resume: no second-repair branch for n = 2; drop "the second-repair conditions" at line 148), and any wording in items 1, 11 and 13 that allows a further A2 repair; in Cost and caps, recompute the "Worst case: 9 reviews instead of 2 (...)" line from the edited rules (repairs stay at most 1 per attempt and 2 per task, so the count may stay 9; say why in the parenthesis) and drop "except the second A2 repair" from the Repairs line. In `refs/qa.md` change the row "A2 with repairs 1 and 2" (line 267) to name the single A2 repair. In `refs/ledger.md` change line 143 ("both repairs are unspent"), Resume row S (`repair-2-<j>.md` → `repair-2-1.md`) and row V (`repair-<n>-<j>.md` → `repair-<n>-1.md`). Keep attempts A3-A5, `halt review=5 reason=ladder-end`, the saved reviewer prompt (`refs/qa.md` Subagent prompt block) and the FINAL contract byte-identical. Copy each edited file byte for byte to `plugins/superclaude/skills/sc-implement-protocol/refs/`. Update `tests/skills/test_implement_severity_static.py` (qa.md row pin at line 278), `tests/skills/test_implement_severity_replay.py` (`route()`'s second-A2 branch, `test_r_a3_late_blockers_local_second_a2_repair`, the replay at lines 244-251), `tests/skills/test_task_workspace_lifecycle.py:582` if the worst-case line changes, and any test found by `git grep -n -E 'second A2|repair-2-2|repairs 1 and 2' -- tests`.

Acceptance criteria:
- `git grep -n -E 'second A2 repair|second-repair conditions|repairs 1 and 2|both repairs are unspent|repair-2-<j>' -- src plugins` prints nothing; `git grep -c -E 'A3|A4|A5' -- src/superclaude/skills/sc-implement-protocol/refs/retry.md` is non-zero and `halt review=5 reason=ladder-end` is still present; `git diff` shows no change inside the `refs/qa.md` Subagent prompt block or the FINAL contract text; `cmp` of each edited src file against its plugin twin is silent.
- `make sync-dev` then `uv run pytest tests/skills/test_implement_severity_static.py tests/skills/test_implement_severity_replay.py tests/skills/test_task_workspace_lifecycle.py -q` plus every test file found by `git grep -l 'sc-implement-protocol' -- tests` pass (saved to `./artifacts/t17-tests.log`).

## Phase 5: Static test and release note

## Task 18: Add the static review-severity test and run the checks

Depends on: Task 2, Task 11, Task 12, Task 13, Task 14, Task 15, Task 16, Task 17

Covers: R-006, R-008, R-010.

Create `tests/skills/test_review_severity_rule.py` with: (a) a scan of every tracked text file under `src/`, `plugins/`, `commands/` and `agents/` (`git ls-files`) that fails on the wordings "any issue of any severity", "issues of any severity", "gaps of any severity", "at any severity", "regardless of severity", "no severity level is exempt", "minor issues still pass", "must still be fixed", "still must be fixed", "must be perfect to pass" and "ALL findings must be resolved" (case-insensitive), with parametrized negative cases on scratch strings; (b) S1-S5 extracted once from `src/superclaude/output-styles/pragmatic.md` as the five bullets after the binary-verdict bullet, each checked by its opening phrase, and one shared helper that the P1 pin in `tests/skills/test_implement_severity_static.py` reuses; (c) S1-S3 (whitespace-normalized) in the ten-file S1-S3 set of Constraints and S5 in its first six; (d) the canonical cap text in `pragmatic.md`; (e) CAP_PATTERN over the 38 cap-sites.md IN files with an allowlist of the cap-sites.md OUT lines (by file and quoted text, not line number), with negative cases on scratch "Max 3 fix cycles", "phase-gate QA failing 3 fix cycles", "after 3 failed cycles", "| research-gate | 3 |" and "Per I16 (2-3 per gate)" strings; (f) no "become Open Questions" / "as Open Questions and proceed" / "proceed with gaps as Open Questions" in the MDTM templates, `rf-task-builder.md` or `task-builder/SKILL.md`; (g) every file under `plugins/superclaude/skills/sc-implement-protocol/` byte-equal to its `src/superclaude/skills/sc-implement-protocol/` twin. Then run `make sync-dev`, `make verify-sync` and `make lint` (install dev deps with `uv pip install -e ".[dev]"` if ruff is missing).

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py -v` passes, including the negative cases (saved to `./artifacts/t18-new-test.log`).
- `uv run pytest tests/audit tests/skills tests/cli/prd tests/cli_portify tests/cli/test_install_user_setup.py tests/cli/reflect/test_no_nesting_guard.py tests/troubleshoot/backtest/test_backtest_e5.py tests/unit/test_cli_install.py -q`, `make verify-sync` and `make lint` pass (saved to `./artifacts/t18-checks.log`); `git diff -U0 -- src/superclaude/agents src/superclaude/skills src/superclaude/templates src/superclaude/rules src/superclaude/output-styles plugins | grep '^+[^+]' | grep -n 'src/superclaude'` prints nothing.

## Task 19: Add the CHANGELOG entry

Depends on: Task 18

Covers: R-009.

Add an entry under `## [Unreleased]` in `CHANGELOG.md`: minor review findings are recorded as notes and never fail a review, are never rechecked and never trigger a fix pass; only blocking findings fail; review loops run at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings instead of becoming Open Questions; the same cap applies to the prd and cli-portify CLI defaults (`--max-convergence` default 2); `/sc:implement` drops its second A2 repair and keeps its own ladder; citing the user decision and the QA-loop findings (`FINDINGS.md` bundle A).

Acceptance criteria:
- `CHANGELOG.md` has the entry under `## [Unreleased]`, naming `pragmatic.md`, the rf-qa agents, the MDTM templates, the 2-fix-cycle cap, the CLI defaults, the `/sc:implement` change and `tests/skills/test_review_severity_rule.py`.
