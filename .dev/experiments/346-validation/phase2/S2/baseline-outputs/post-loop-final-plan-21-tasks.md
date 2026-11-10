---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeTheAnyIssu-20261102-053741
version: "1"
priority: High
created_date: "2026-11-02"
---

# Minor findings never fail a review; review loops capped at 2 fix cycles (final plan)

Source: ./source.md
Goal: No shipped primitive, CLI default or CLI prompt fails a review on a minor finding or rechecks minors; every review loop outside /sc:implement runs at most 2 fix cycles (3 reviews) and then escalates the open blocking findings to the user instead of passing them; /sc:implement drops its second A2 repair and keeps its own ladder (A3-A5, halt at review 5) as its at-cap escalation under S4, so its worst case stays its own count; static tests pin all of it.

## Constraints

- Final user decisions (restart spec `/tmp/t11b-severity-rule-restart-spec.md`): B1 minor findings are noted and work proceeds, with no recheck and no FAIL; at the cap, open blocking findings are escalated to the user, never passed; B2 the cap is 2 fix cycles = at most 3 reviews; B3 `/sc:implement` option A; `update.sh` is not changed; cli-portify default 1 iteration (coordinator, inventory section 4 item 3a). Evidence: `/home/coder/workspaces/IronClaude/.dev/worktrees/qa-loop-investigation/.dev/qa-loop-investigation/FINDINGS.md` sections 4 and 5.
- Amendment, user decision 2026-11-02 08:41 UTC (coordinator message msg_9d0fe67f82c7, reply to the review-cap escalation): the 10 open blocking findings of pre-review 3 (`.dev/reflect/pre-removeTheAnyIssu-20261102054021/REPORT.md`, B3-01..B3-10) are added to this plan and it is implemented with no fourth plan review. Safeguards: (1) one fixed, recorded site sweep, `.dev/review-severity-rule/site-sweep.md` (pattern list, every hit, and for each hit its task or the reason it is not a rule of this kind); its literal edits for sites outside the earlier lists are `.dev/review-severity-rule/sweep-edits.yaml` (Task 19); (2) the static test of Task 20 fails if any swept wording survives as a rule; (3) acceptance checks use text anchors, not line numbers (B3-09). Per-task QA and the FINAL review stay as they are, each under the 2-fix-cycle cap. This amendment was made by hand on the user's instruction; it is the one exception to never editing a generated plan from reflect findings.
- This plan replaces packages `TASK-WF-removeTheAnyIssu-20261101-225635` and `TASK-WF-removeTheAnyIssu-20261102-042031`; their pre-review findings (B-01..B-11, P2-B1..P2-B7) are folded in.
- Site lists (repo-relative): severity wording `.dev/review-severity-rule/inventory.md` sections 1, 2, 4 and 6; every cap and at-cap edit `.dev/review-severity-rule/cap-edits.yaml` (161 rows with literal `old` and `new`, grouped `agents`, `templates`, `skills-a`, `skills-b`, `portify`, `prd-core`; a row with `occurrences` > 1 is applied to every occurrence). Severity line numbers are against `f90877be`; locate each site by its quoted text.
- CAP_CHECK for a group G (run from the repo root): `uv run python -I -c 'import sys,yaml,pathlib; rows=[r for r in yaml.safe_load(open(".dev/review-severity-rule/cap-edits.yaml"))["rows"] if r["group"]==sys.argv[1]]; bad=[r["id"] for r in rows if r["old"] in pathlib.Path(r["file"]).read_text() or r["new"] not in pathlib.Path(r["file"]).read_text()]; print(len(rows), "rows; failing:", bad); sys.exit(1 if bad else 0)' G`. It exits 0 only when every row of the group has its `old` absent and its `new` present.
- Severity tasks never change any `old` fragment of cap-edits.yaml; cap tasks change only those fragments. Copies of S1-S5 are taken from `src/superclaude/output-styles/pragmatic.md` after Task 1 (no "(S1)".."(S5)" labels, no S3 annotation). The S1-S3 file set is exactly `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/templates/documents/agent_template_qa.md`, `src/superclaude/templates/documents/skill_template.md`, `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`, `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (these six also carry S5) and the four `src/superclaude/rules/prompts/*_qa_prompt.md` files. Shared FAIL-line replacements keep "Only PASS or FAIL — no conditional pass." and each file's own "List each ..." suffix.
- Tasks run in number order. `.claude/agents`, `.claude/skills` and `.claude/templates` are absent in this worktree and many `tests/audit` tests compare `src/` with those mirrors, so every task runs `make sync-dev` before its pytest command.
- R-008: never add a `src/superclaude/...` path to an installed primitive; every task that edits a primitive checks `git diff -U0 -- <its primitive files> | grep '^+[^+]' | grep -n 'src/superclaude'` prints nothing.
- Edit only `src/superclaude/`, `plugins/superclaude/` twins, `tests/` and `CHANGELOG.md`. Never edit or stage `.claude/` (except `.claude/settings.json`, untouched here). `.dev/tasks/` is always staged.
- Minor findings from this plan's own reviewers are noted, not fixed in extra rounds (pre-review 3 minors M3-01..M3-12 stay notes). Kept as notes, not tasks: rule 9 "When in doubt, fail it" (`rf-qa-qualitative.md:981`), `docs/guides/tdd-skill-release-guide.md:265, 271` (outside scope), S1-S3 not copied into the seven skill prompt-block copies, no check that OUT sites stay unchanged beyond Task 20(f).
- SWEEP_CHECK for a group G: the CAP_CHECK command with `cap-edits.yaml` replaced by `sweep-edits.yaml`.
- Checks are the tests named per task plus tests that read edited files; `make verify-sync`; `make lint`. Never the full suite and never `tests/cli/eval/` as a directory. Commit, push and `/sc:pr-submit` are done by the operator after this plan.

## Phase 1: Canonical rule

## Task 1: Replace the any-severity bullet in the Pragmatic output style

Covers: R-001, R-007 (pin P1), R-008.

Replace the bullet in `src/superclaude/output-styles/pragmatic.md` that begins "Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict" with S1, S2, S3, S4, S5 of inventory section 1, in that order, directly after the binary-verdict bullet, without the "(S1)".."(S5)" labels and without the S3 annotation. Leave the adversarial-stance, zero-finding Self-Audit and binary-verdict bullets unchanged. Update pin P1 in `tests/skills/test_implement_severity_static.py` (`test_p1_output_style_exempts_implement_severity_model`) to assert the new S2 and S4 text; keep P2-P4.

Acceptance criteria:
- `git grep -n -i -E 'any severity|minor issues still pass|\(S[1-5]' -- src/superclaude/output-styles/pragmatic.md` prints nothing; the five bullets after "Every review agent MUST produce a binary verdict: PASS or FAIL." are S1-S5 verbatim, and S3 contains "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings".
- `make sync-dev` then `uv run pytest tests/skills/test_implement_severity_static.py tests/audit -q` passes (saved to `./artifacts/t1-tests.log`).

## Phase 2: QA agents, templates and the pinned rf-team-lead line (severity)

## Task 2: Apply the rule to rf-qa and its verdict test

Depends on: Task 1

Covers: R-002, R-007 (nfr_conv_9), R-008, R-010.

Edit `src/superclaude/agents/rf-qa.md` per the inventory section 2.2 rows for `agents/rf-qa.md`: the DNSP references to "any gap regardless of severity = FAIL" (lines 82 and 84, wording only), principle 1 "Zero tolerance" (91), principle 8 NO LENIENCY (98), the research-gate Gap severity items (158-159), the research-gate Verdict bullets (171-172), the Fix Cycle phase re-verification scope (370-389: blocking items only; leave line 390's cap sentence to Task 12), "Must resolve ALL [N] issues" (464) and rule 10's severity sentence (537: "ALL findings regardless of severity must be resolved." becomes "All blocking findings must be resolved; minor findings are recorded as notes."; its cap fragment is Task 12's). Add one "## Review severity rule" section after the Verification Principles holding S1-S3 and S5. Update `tests/audit/test_nfr_conv_9_zero_trust.py`: `PASS_BULLET` / `FAIL_BULLET` to the new bullets, the scorer to fail only on CRITICAL or IMPORTANT gap rows, the one-MINOR case (including the assert at line 432) to expect PASS, rename fail-named classes and tests (such as `TestPartA_OneLowFindingFailsGate`, `test_gate_returns_fail`) and the docstring and messages at lines 6-12 and 246, and add a one-IMPORTANT case expecting FAIL with fixture `tests/audit/fixtures/nfr_conv_9/one_important_finding.md`; update the prose in `tests/audit/fixtures/nfr_conv_9/one_low_finding.md` (lines 13, 45; keep "NFR-CONV.9 part (a)") and `tests/audit/fixtures/nfr_conv_9/zero_findings_baseline.md` (lines 9, 35). B3-05: `tests/audit/test_invariant_preservation_NFR_6_through_10.py` imports the same scorer and expects one LOW finding to FAIL (its `== "FAIL"` assertion for the one-low case and the NFR-CONV.9 invariant built on it): change it to expect PASS for one LOW finding, keep its other invariants, and run `git grep -l -E 'nfr_conv_9|one_low_finding' -- tests` to update any other importer the same way.

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|still must be fixed' -- src/superclaude/agents/rf-qa.md` prints nothing; the file contains S1, S2, S3 and S5; the rule-10 line (it begins `10. **Maximum`) holds "All blocking findings must be resolved"; the PASS bullet allows MINOR gaps as notes and the FAIL bullet names only CRITICAL or IMPORTANT gaps.
- `git grep -n -E 'one_low|one LOW' -- tests/audit/test_invariant_preservation_NFR_6_through_10.py` shows the one-LOW case expecting PASS.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t2-audit.log`).

## Task 3: Apply the rule to rf-qa-qualitative and rf-analyst; rewrite rule 10 and re-pin the Critical Rules hash

Depends on: Task 2

Covers: R-002, R-004 (row C-003), R-007 (BASELINE_BLOCK_SHA), R-008, R-010.

Edit `src/superclaude/agents/rf-qa-qualitative.md` per inventory 2.2: the DNSP reference (83, wording only; sha and "max-3-cycles" stay for Task 6), NO LENIENCY (97), the eight PASS / FAIL pairs (228-229, 279-280, 350-351, 417-418, 488-489, 555-556, 734-735, 772-773), the Fix Cycle phase (777-796 and the severity sentence of 797, blocking items only; the cap fragment of 797 is row C-001 for Task 12), and rule 10 at line 982 in full: its severity sentence becomes "All blocking findings must be resolved; minor findings are recorded as notes." and its cap fragment is changed by row C-003 of cap-edits.yaml, so the Critical Rules block changes only in this task. Add one "## Review severity rule" section with S1-S3 and S5 after the principles (outside the Critical Rules block). Edit `src/superclaude/agents/rf-analyst.md` per inventory 2.2: the DNSP API-003-M6 clause on line 74 (wording only), line 93, and lines 148 and 199. Recompute `BASELINE_BLOCK_SHA` in `tests/audit/test_severity_floor_unweakened.py` (line 48) with a comment citing this change; keep `BASELINE_SLICE_SHA`, the Rule 6 verbatim check and the softening-token check.

Acceptance criteria:
- `git grep -n -i -E 'any severity|issues of any severity|regardless of severity|no severity level is exempt|must still be fixed' -- src/superclaude/agents/rf-qa-qualitative.md src/superclaude/agents/rf-analyst.md` prints nothing; `rf-qa-qualitative.md` contains S1, S2, S3 and S5 and eight PASS bullets that allow MINOR issues as notes; row C-003 holds (its `old` absent, its `new` present).
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t3-audit.log`).

## Task 4: Apply the rule to the QA agent template, the skill template and the shared document templates

Depends on: Task 3

Covers: R-002, R-008, R-010.

Edit per inventory 2.2 and 2.3: `src/superclaude/templates/documents/agent_template_qa.md` (principle lists 95-96, NO LENIENCY 100, S5 under the MINOR definition at 139, verdict 156-157 plus S1-S3, message 262, and rule N+3's severity sentence at 335 becoming "All blocking findings must be resolved; minor findings are recorded as notes."; cap fragments are Task 13's); `src/superclaude/templates/documents/skill_template.md` lines 815 and 824 (Gap severity item and FAIL verdict of the shared research-gate prompt block; the FAIL line keeps "Only PASS or FAIL — no conditional pass.") plus S1-S3 and S5 added once inside that prompt block; `src/superclaude/templates/modularization-template-review/analyst-completeness_report_template.md` lines 75 and 159; `src/superclaude/templates/modularization-template-review/synthetic-dnsp-finding.contract` line 52.

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|must still be fixed|ALL findings must be resolved' -- src/superclaude/templates/documents/agent_template_qa.md src/superclaude/templates/documents/skill_template.md src/superclaude/templates/modularization-template-review/analyst-completeness_report_template.md src/superclaude/templates/modularization-template-review/synthetic-dnsp-finding.contract` prints nothing; `agent_template_qa.md` and `skill_template.md` each contain S1, S2, S3 and S5; the research-gate FAIL line of `skill_template.md` (it begins `- FAIL:`, inside the Research Gate prompt block) still contains "Only PASS or FAIL — no conditional pass.".
- `make sync-dev` then `uv run pytest tests/audit tests/skills/test_task_builder_merge.py -q` passes (saved to `./artifacts/t4-tests.log`).

## Task 5: Apply the rule to the MDTM templates

Depends on: Task 4

Covers: R-002, R-008, R-010.

In `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`: replace line 643's any-severity sentence with S1-S3 and S5 (indented to the I16 block) and change line 655 to re-verify blocking items only. In `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`: the same at 654 and 671, plus the Multi-Agent Verdict Consolidation sentence at 656 (FAIL only on a blocking issue; minor issues carried as notes). The at-cap "Open Questions" cells and sentences in both templates are cap-edits.yaml rows for Task 13.

Acceptance criteria:
- `git grep -n -i 'any severity' -- src/superclaude/templates/workflow/01_mdtm_template_generic_task.md src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` prints nothing; both templates contain S1, S2, S3 and S5; in each template the I16 sentence that begins "Each fix cycle MUST re-verify" re-verifies blocking items only and says minor findings are not rechecked.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t5-audit.log`).

## Task 6: Rewrite the pinned rf-team-lead Fix Cycles line and propagate its sha256

Depends on: Task 3

Covers: R-004, R-007 (dnsp test), R-012, R-008, R-010.

Rewrite the line of `src/superclaude/agents/rf-team-lead.md` that begins "- **Fix Cycles**: " (line 462 at HEAD) so that it keeps that prefix, its FIX trigger reads exactly "If a phase pipeline returns blocking findings, invoke another pipeline with a FIX request" followed by "(minor findings are recorded as notes)", reads "max 2 cycles per phase", and keeps "HALT and ask user" with "the open blocking findings". Compute the sha256 of the new line exactly as `tests/audit/test_dnsp_all_agents_fail_bypass.py` does (fixture bytes, trailing newline included). In one change: put the new sha in place of `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` on the four sha lines `src/superclaude/agents/rf-qa.md:82`, `src/superclaude/agents/rf-qa-qualitative.md:83`, `src/superclaude/agents/rf-analyst.md:74` and `src/superclaude/skills/task-builder/SKILL.md:901`; change "max-3-cycles" to "max-2-cycles" on the three token lines (rf-qa:82, rf-qa-qualitative:83, rf-analyst:74); write the new line to `tests/audit/fixtures/rf-team-lead-fix-cycles-rule.txt`; update `tests/audit/test_dnsp_all_agents_fail_bypass.py` (lines 14, 32, 77, 395-399, 640) to the new sha, "max 2 cycles per phase" and "max-2-cycles", and rename `test_fix_cycles_line_contains_max_3_cycles_token` to `..._max_2_cycles_token`.

Acceptance criteria:
- `git grep -n '51725c0f' -- src tests plugins` and `git grep -n -i -E 'max-3-cycles|max 3 cycles per phase' -- src tests` print nothing; the new sha appears on the four sha lines and in the test; `git grep -n -F -- '- **Fix Cycles**: If a phase pipeline returns blocking findings, invoke another pipeline with a FIX request' -- src/superclaude/agents/rf-team-lead.md` prints one line, and that line contains "max 2 cycles per phase"; `git grep -n -F 'If a phase pipeline returns issues' -- src` prints nothing.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t6-audit.log`).

## Phase 3: Skills, CLI prompt and rule prompts (severity)

## Task 7: Apply the rule to the prd and tdd skills and the prd CLI prompt

Depends on: Task 4

Covers: R-002, R-011 (prompt), R-008, R-010.

Edit per inventory 2.4: `src/superclaude/skills/prd/refs/agent-prompts.md` lines 273 and 283 and `src/superclaude/skills/tdd/refs/agent-prompts.md` lines 282 and 291 (same Gap severity and FAIL text as Task 4's `skill_template.md`), `src/superclaude/skills/prd/refs/build-request-template.md` lines 129 and 157, `src/superclaude/skills/tdd/refs/build-request-template.md` lines 124 and 152, and the same Gap severity and FAIL lines in the Python prompt string `src/superclaude/cli/prd/prompts.py` (lines 1164 and 1173; keep that file's ASCII "--").

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|must still be fixed|ALL findings must be resolved|\(CRITICAL, IMPORTANT, or MINOR\)' -- src/superclaude/skills/prd src/superclaude/skills/tdd src/superclaude/cli/prd/prompts.py` prints nothing; the Gap severity and FAIL lines of both `agent-prompts.md` files equal those of `skill_template.md`.
- `make sync-dev` then `uv run pytest tests/cli/prd tests/audit -q` passes (saved to `./artifacts/t7-tests.log`).

## Task 8: Apply the rule to the tech-reference and tech-research skills

Depends on: Task 4

Covers: R-002, R-008, R-010.

Edit per inventory 2.4: `src/superclaude/skills/tech-reference/SKILL.md` lines 536, 878 and 886; `src/superclaude/skills/tech-research/SKILL.md` lines 567, 886, 894 and 1150. The shared FAIL lines keep "Only PASS or FAIL — no conditional pass.".

Acceptance criteria:
- `git grep -n -i -E 'any severity|regardless of severity|no severity level is exempt|must still be fixed|ALL findings must be resolved|0 minor' -- src/superclaude/skills/tech-reference/SKILL.md src/superclaude/skills/tech-research/SKILL.md` prints nothing; the shared Gap severity and FAIL lines equal those of `skill_template.md`.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t8-tests.log`).

## Task 9: Apply the rule to the readme and operational-guide skills

Depends on: Task 4

Covers: R-002, R-008, R-010.

Edit per inventory 2.4: `src/superclaude/skills/readme/SKILL.md` lines 549, 609, 1007, 1029 and 1038 (FAIL lines keep "List each with specific remediation."), and the severity sentence "ALL findings must be resolved" inside the summary line 2034; `src/superclaude/skills/operational-guide/SKILL.md` lines 514 (severity clause only), 982 and 990 (keep "Only PASS or FAIL — no conditional pass. List each finding with specific remediation."), and the same severity sentence inside line 1349.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|must still be fixed|ALL findings must be resolved|Zero leniency' -- src/superclaude/skills/readme/SKILL.md src/superclaude/skills/operational-guide/SKILL.md` prints nothing; the shared Gap severity line equals `skill_template.md`'s.
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t9-tests.log`).

## Task 10: Apply the rule to the task and task-builder skills

Depends on: Task 6

Covers: R-002, R-008, R-010.

Edit `src/superclaude/skills/task/SKILL.md` line 347 and `src/superclaude/skills/task-builder/SKILL.md` lines 865, 869-870 (MINOR issues stay notes and are not sent to gap-fill), 895 (DNSP API-003-M6 clause, wording only) and 1600 per inventory 2.2 and 2.4. The Open Questions at-cap rules in these files are cap-edits.yaml rows for Task 15.

Acceptance criteria:
- `git grep -n -i -E 'regardless of severity|\(CRITICAL, IMPORTANT, or MINOR\)|CRITICAL, IMPORTANT, and MINOR issues' -- src/superclaude/skills/task/SKILL.md src/superclaude/skills/task-builder/SKILL.md` prints nothing.
- `make sync-dev` then `uv run pytest tests/skills/test_task_builder_merge.py tests/audit tests/cli/reflect/test_no_nesting_guard.py tests/troubleshoot/backtest/test_backtest_e5.py -q` passes (saved to `./artifacts/t10-tests.log`).

## Task 11: Apply the rule to the legacy QA rule prompts

Depends on: Task 1

Covers: R-002, R-008, R-010.

Edit per inventory 2.5: principle 1 "Zero tolerance: The batch must be perfect to pass" in `src/superclaude/rules/prompts/automated_qa_workflow_qa_prompt.md` (line 10), `src/superclaude/rules/prompts/doc_code_analyst_qa_prompt.md` (26), `src/superclaude/rules/prompts/documentation_expert_qa_prompt.md` (27) and `src/superclaude/rules/prompts/recruiting_expert_qa_prompt.md` (26), each followed by S1-S3 once; and the two cosmetic FAIL lines at `documentation_expert_qa_prompt.md:307-308`. The "EXACT means EXACT" checks stay.

Acceptance criteria:
- `git grep -n -E 'must be perfect to pass|Poor grammar/spelling/formatting = FAIL|Unclear or confusing writing = FAIL' -- src/superclaude/rules/prompts` prints nothing; each of the four files contains S1, S2 and S3.
- `make sync-dev` then `uv run pytest tests/cli/test_install_user_setup.py tests/unit/test_cli_install.py -q` passes (saved to `./artifacts/t11-install.log`).

## Phase 4: Review-loop caps and at-cap rules (cap-edits.yaml)

## Task 12: Apply the cap-edits rows of group `agents`

Depends on: Task 6

Covers: R-004, R-003, R-007 (task_builder_merge comment), R-008, R-010, R-015.

Apply every row of group `agents` in `.dev/review-severity-rule/cap-edits.yaml` (17 rows; C-003 is already applied by Task 3): `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/agents/rf-task-builder.md` (cap and Open Questions cells), `src/superclaude/agents/rf-task-executor.md:226`. Update the "3-fix-cycle" comment at `tests/skills/test_task_builder_merge.py:435`.

Acceptance criteria:
- CAP_CHECK `agents` exits 0 (output saved to `./artifacts/t12-capcheck.txt`); the rule-10 line of `rf-qa.md` (it begins `10. **Maximum`) still holds "All blocking findings must be resolved".
- `make sync-dev` then `uv run pytest tests/audit tests/skills/test_task_builder_merge.py -q` passes (saved to `./artifacts/t12-tests.log`).

## Task 13: Apply the cap-edits rows of group `templates`

Depends on: Task 5

Covers: R-004, R-003, R-008, R-010, R-015.

Apply every row of group `templates` (37 rows): `src/superclaude/templates/documents/agent_template_qa.md`, `src/superclaude/templates/documents/skill_template.md`, the nine `qa-*` templates in `src/superclaude/templates/modularization-template-review/`, and both MDTM templates (cap cells, "2-3 per gate" rows, Open Questions at-cap cells and sentences including 01:938, 01:1232 and 02:1090).

Acceptance criteria:
- CAP_CHECK `templates` exits 0 (saved to `./artifacts/t13-capcheck.txt`); `git grep -n -i -E 'become Open Questions|as Open Questions and proceed' -- src/superclaude/templates/workflow` prints nothing; the rule N+3 line of `agent_template_qa.md` (it begins `N+3. **Maximum`) still holds "All blocking findings must be resolved".
- `make sync-dev` then `uv run pytest tests/audit -q` passes (saved to `./artifacts/t13-tests.log`).

## Task 14: Apply the cap-edits rows of group `skills-a`

Depends on: Task 7, Task 8, Task 9

Covers: R-004, R-003, R-008, R-010, R-015.

Apply every row of group `skills-a` (51 rows): `src/superclaude/skills/operational-guide/SKILL.md`, `src/superclaude/skills/readme/SKILL.md` (rows C-071 and C-072 cover two identical lines each), `src/superclaude/skills/roadmap/SKILL.md` (including the Open Questions rules at 569 and 2608), `src/superclaude/skills/tech-reference/SKILL.md`, `src/superclaude/skills/tech-research/SKILL.md`, `src/superclaude/skills/prd/refs/build-request-template.md`, `src/superclaude/skills/tdd/refs/build-request-template.md`.

Acceptance criteria:
- CAP_CHECK `skills-a` exits 0 (saved to `./artifacts/t14-capcheck.txt`).
- `make sync-dev` then `uv run pytest tests/audit tests/skills -q` passes (saved to `./artifacts/t14-tests.log`).

## Task 15: Apply the cap-edits rows of group `skills-b`

Depends on: Task 10

Covers: R-004, R-003, R-008, R-010, R-015.

Apply every row of group `skills-b` (31 rows): `src/superclaude/skills/task/SKILL.md` and `src/superclaude/skills/task-builder/SKILL.md`, including the Open Questions at-cap rules (873, 1259, 1310, 1420, 1471, 1620, 1660) and the DM-005 token rename `retry-into-max-cycle-then-Open-Questions` -> `retry-into-max-cycle-then-halt-escalate` (row C-157, five occurrences).

Acceptance criteria:
- CAP_CHECK `skills-b` exits 0 (saved to `./artifacts/t15-capcheck.txt`); `git grep -n -i 'Open Question' -- src/superclaude/skills/task-builder/SKILL.md` shows no rule that proceeds with open findings as Open Questions (any remaining hit is listed with its reason in the same file).
- `make sync-dev` then `uv run pytest tests/skills tests/audit tests/cli/reflect/test_no_nesting_guard.py tests/troubleshoot/backtest/test_backtest_e5.py -q` passes (saved to `./artifacts/t15-tests.log`).

## Task 16: Apply the cap-edits rows of group `portify` (cli-portify default 1)

Depends on: Task 1

Covers: R-004, R-011, R-007 (test_convergence), R-008, R-010, R-015.

Apply every row of group `portify` (20 rows): `src/superclaude/cli/cli_portify/convergence.py` (default and docstring, including `range(1, 4)`), `steps/panel_review.py`, `commands.py` (`--max-convergence` default 1; help text says the default follows the 2-fix-cycle cap and the user may raise it), `config.py`, `models.py`, `prompts.py`, `resume.py`, `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md`, `src/superclaude/skills/sc-cli-portify-protocol/decisions.yaml`, and the default test in `tests/cli_portify/test_convergence.py` (row C-143: a default engine escalates after the first unresolved iteration).

Acceptance criteria:
- CAP_CHECK `portify` exits 0 (saved to `./artifacts/t16-capcheck.txt`).
- `make sync-dev` then `uv run pytest tests/cli_portify -q` passes and `make lint` passes (saved to `./artifacts/t16-tests.log`).

## Task 17: Apply the cap-edits rows of group `prd-core`

Depends on: Task 7

Covers: R-004, R-011, R-013, R-008, R-010, R-015.

Apply every row of group `prd-core` (5 rows): `src/superclaude/cli/prd/models.py:203` (`max_research_fix_cycles` 2; `executor.py:1157` runs `range(max_cycles + 1)`, so 2 gives 2 fix cycles and 3 QA runs) and `src/superclaude/rules/core/ib_agent_core.md` (574, 633, 913, 933; doc-only, the external `automated_qa_workflow.sh` is not in this repository).

Acceptance criteria:
- CAP_CHECK `prd-core` exits 0 (saved to `./artifacts/t17-capcheck.txt`).
- `make sync-dev` then `uv run pytest tests/cli/prd tests/unit/test_cli_install.py -q` passes (saved to `./artifacts/t17-tests.log`).

## Task 18: Remove the second A2 repair from the /sc:implement retry ladder (option A)

Depends on: Task 1

Covers: R-005, R-014, R-008, R-010.

Re-read `src/superclaude/skills/sc-implement-protocol/refs/retry.md` and `refs/qa.md` first. In `refs/retry.md` Repair round: item 5 (j is always 1), item 6 (one A2 repair; drop the second-repair sentence), item 12 (no second-repair branch for n = 2; drop "the second-repair conditions" at line 148), and any wording in items 1, 11 and 13 that allows a further A2 repair; in Cost and caps, recompute the "Worst case: 9 reviews instead of 2 (...)" line (repairs stay at most 1 per attempt and 2 per task, so the count may stay 9; say why in the parenthesis) and drop "except the second A2 repair" from the Repairs line. In `refs/qa.md` change the row "A2 with repairs 1 and 2" (line 267) to the single A2 repair. In `refs/ledger.md` change line 143 ("both repairs are unspent"), Resume row S (`repair-2-<j>.md` -> `repair-2-1.md`) and row V (`repair-<n>-<j>.md` -> `repair-<n>-1.md`). Keep attempts A3-A5, `halt review=5 reason=ladder-end`, the saved reviewer prompt (`refs/qa.md` Subagent prompt block) and the FINAL contract byte-identical. Copy each edited file byte for byte to `plugins/superclaude/skills/sc-implement-protocol/refs/`. Update `tests/skills/test_implement_severity_static.py` (qa.md row pin at line 278), `tests/skills/test_implement_severity_replay.py` (`route()`'s second-A2 branch, `test_r_a3_late_blockers_local_second_a2_repair`, the replay at lines 244-251), `tests/skills/test_task_workspace_lifecycle.py:582` if the worst-case line changes, and any test found by `git grep -n -E 'second A2|repair-2-2|repairs 1 and 2' -- tests`.

Acceptance criteria:
- `git grep -n -E 'second A2 repair|second-repair conditions|repairs 1 and 2|both repairs are unspent|repair-2-<j>|repair-<n>-<j>' -- src plugins` prints nothing; `refs/retry.md` still names A3, A4 and A5 and contains `halt review=5 reason=ladder-end`; `refs/ledger.md` row V names `repair-<n>-1.md`; `git diff` shows no change inside the `refs/qa.md` Subagent prompt block or the FINAL contract text; `cmp` of each edited src file against its plugin twin is silent.
- `make sync-dev` then `uv run pytest tests/skills/test_implement_severity_static.py tests/skills/test_implement_severity_replay.py tests/skills/test_task_workspace_lifecycle.py -q` plus every test file found by `git grep -l 'sc-implement-protocol' -- tests` pass (saved to `./artifacts/t18-tests.log`).

## Phase 5: Site-sweep edits, static test and release note

## Task 19: Apply the site-sweep rows (pre-review 3 findings B3-01, B3-02, B3-03, B3-04, B3-07, B3-08, B3-10)

Depends on: Task 2, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15, Task 17

Covers: R-002, R-003, R-008, R-010.

Apply every row of `.dev/review-severity-rule/sweep-edits.yaml` (literal `old` -> `new`, same contract as cap-edits.yaml; groups `fixloop`, `verdict`, `halt`, `template-qa`, `reflect-gate`, `tasklist`, `zero-tolerance`). What the rows do: a fix agent receives, applies and re-verifies blocking findings only and a loop repeats only on new blocking findings (B3-03, B3-08); the shared "FAIL: Issues found" verdict and its copies, including the prd CLI prompts, fail only on blocking issues (B3-07); rf-qa's strictly-fewer-issues halt counts blocking issues only (B3-01); the QA agent template's Fix Cycle rechecks blocking items only (B3-02); task-builder's post-execution reflect gate halts and escalates open Regression or Drift deviations instead of logging them to Open Questions (B3-04); sc-tasklist-protocol keeps Low findings as notes and halts and escalates open blocking findings at its cap instead of shipping them "logged for human review" (B3-10); the QA rule prompts and `ib_agent_core.md` say zero tolerance for blocking errors. Every hit of the site sweep (`.dev/review-severity-rule/site-sweep.md`) that names this task is covered by a row. If a row's `old` is no longer found because an earlier task changed the same words, stop and fix the row against the live text, recording the change in the row's comment.

Acceptance criteria:
- SWEEP_CHECK exits 0 for each of the seven groups (saved to `./artifacts/t19-sweepcheck.txt`).
- `uv run python -I .dev/review-severity-rule/sweep/fixloop_scan.py` prints only the three pm-agent example lines (`agents/sc-pm-agent.md`, `src/superclaude/agents/pm-agent.md`, `plugins/superclaude/agents/pm-agent.md`, "Adds prevention checklist if issues found"); `git grep -n -i -E 'FAIL: Issues found|strictly fewer issues|logged for human review|zero-tolerance policy for errors' -- src plugins commands agents skills` prints nothing.
- `make sync-dev` then `uv run pytest tests/audit tests/skills tests/cli/prd -q` passes (saved to `./artifacts/t19-tests.log`).

## Task 20: Add the static review-severity test and run the checks

Depends on: Task 2, Task 11, Task 12, Task 13, Task 14, Task 15, Task 16, Task 17, Task 18, Task 19

Covers: R-006, R-008, R-010.

Copy `.dev/review-severity-rule/cap-edits.yaml` to `tests/skills/fixtures/review_severity_cap_edits.yaml` and `.dev/review-severity-rule/sweep-edits.yaml` to `tests/skills/fixtures/review_severity_sweep_edits.yaml`, and create `tests/skills/test_review_severity_rule.py` with: (a) a scan of every tracked text file under `src/`, `plugins/`, `commands/` and `agents/` (`git ls-files`) that fails on "any issue of any severity", "issues of any severity", "gaps of any severity", "at any severity", "regardless of severity", "no severity level is exempt", "minor issues still pass", "must still be fixed", "still must be fixed", "must be perfect to pass", "ALL findings must be resolved" and "CRITICAL, IMPORTANT, and MINOR issues" (case-insensitive), with parametrized negative cases on scratch strings; (b) S1-S5 extracted once from `src/superclaude/output-styles/pragmatic.md` as the five bullets after the binary-verdict bullet, each checked by its opening phrase, through one helper that the P1 pin in `tests/skills/test_implement_severity_static.py` also uses; (c) S1-S3 (leading "- " stripped, whitespace-normalized) in the ten-file S1-S3 set of Constraints and S5 in its first six, and no "(S1)".."(S5)" label or "contains the canonical cap text" annotation in those files; (d) the canonical cap text in `pragmatic.md`, and the at-cap clause form present in each file that has a cap-edits row whose `new` contains it; (e) every fixture row holds (its `old` absent and its `new` present in its file); (f) the regression pattern `(max(imum)?|after|up to) [3-9] (fix|fix-verify|correction) (cycles?|loops?|attempts?)|(failing|failed) [3-9] fix cycles|max-[3-9]-cycles?|\b[3-9]-(fix-)?cycles?\b|fix cycles?: [3-9]\b|after [3-9] failed cycles` (case-insensitive) finds nothing in tracked `src/` and `plugins/` text outside `sc-implement-protocol` except the two allowlisted sc-cli-eval lines ("Max 3 fix loops" in `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md` and "max 3 fix loops" in its `refs/create-pipeline.md`), with negative cases on scratch "Max 3 fix cycles", "phase-gate QA failing 3 fix cycles", "after 3 failed cycles" and "max-3-cycles"; (g) "Only PASS or FAIL — no conditional pass." still present in `skill_template.md`, the prd, tdd, tech-reference and tech-research prompt blocks and `operational-guide/SKILL.md`, and "List each with specific remediation." in `readme/SKILL.md`; (h) every file under `plugins/superclaude/skills/sc-implement-protocol/` byte-equal to its `src/superclaude/skills/sc-implement-protocol/` twin; (i) the site-sweep wordings: a scan of the same tracked files (`src/`, `plugins/`, `commands/`, `agents/`, `skills/`) that fails on "FAIL: Issues found", "strictly fewer issues", "logged for human review", "zero-tolerance policy for errors", "issues of any severity" and the fix-loop patterns F1-F6 of `.dev/review-severity-rule/sweep/fixloop_scan.py` (copied into the test as `FIX_LOOP_PATTERNS`; a line containing "blocking" is in scope), with an allowlist that holds only the three pm-agent example lines, each with its reason, and parametrized negative cases on scratch strings ("If findings exist, spawn ONE rf-qa agent", "If verification finds new issues, repeat", "FAIL: Issues found (list with specific fixes)", "logged for human review"); (j) every row of the sweep-edits fixture holds; (k) a "zero tolerance" phrase in those files is allowed only on a line that also names fabrication, forgery, hallucination, verification or verify, accuracy, dismissal, incremental writing, blocking, or the template comment about the VERBATIM "Zero tolerance" closing line (the site-sweep reasons), with a negative case on "Zero tolerance: The batch must be perfect to pass". Then run `make sync-dev`, `make verify-sync` and `make lint` (install dev deps with `uv pip install -e ".[dev]"` if ruff is missing).

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py -v` passes, including the negative cases (saved to `./artifacts/t20-new-test.log`).
- `uv run pytest tests/audit tests/skills tests/cli/prd tests/cli_portify tests/cli/test_install_user_setup.py tests/unit/test_cli_install.py tests/cli/reflect/test_no_nesting_guard.py tests/troubleshoot/backtest/test_backtest_e5.py -q`, `make verify-sync` and `make lint` pass (saved to `./artifacts/t20-checks.log`); `git grep -l 'sc-tasklist-protocol' -- tests` files also pass; `git diff -U0 -- src/superclaude/agents src/superclaude/skills src/superclaude/templates src/superclaude/rules src/superclaude/output-styles plugins | grep '^+[^+]' | grep -n 'src/superclaude'` prints nothing.

## Task 21: Add the CHANGELOG entry

Depends on: Task 20

Covers: R-009.

Add an entry under `## [Unreleased]` in `CHANGELOG.md`: minor review findings are recorded as notes and never fail a review, are never rechecked and never trigger a fix pass; only blocking findings fail; review loops run at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings instead of becoming Open Questions; the prd CLI research fix cycles default to 2 and cli-portify's convergence defaults to 1 iteration (`--max-convergence` can raise it); `/sc:implement` drops its second A2 repair and keeps its own ladder; fix agents, the synthesis QA verdict and sc:tasklist's patch loop handle blocking findings only; citing the user decision and the QA-loop findings (`FINDINGS.md` bundle A).

Acceptance criteria:
- `CHANGELOG.md` has the entry under `## [Unreleased]`, naming `pragmatic.md`, the rf-qa agents, the MDTM templates, the 2-fix-cycle cap, the CLI defaults, the `/sc:implement` change and `tests/skills/test_review_severity_rule.py`.
