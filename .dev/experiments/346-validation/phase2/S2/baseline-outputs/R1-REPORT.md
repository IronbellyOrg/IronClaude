# Reflect pre-execution report — TASK-WF-removeTheAnyIssu-20261101-225635

```yaml
contract_version: 1.8.0
status: success   # run quality; the plan itself fails review on 11 blocking findings (see Summary)
mode: pre
tier_reached: 2
confidence_calibrated: 0.80   # mean of the three reviewer-card calibrations (0.83, 0.77, 0.81); Tier 1 card calibrated 0.67
citations_total: 50
citations_revalidated: 50
citations_dropped: 0      # zero-drop-flag: true (audit marker); 4 citations drifted within +-3 or ambiguous, noted below
citations_inferred: 9
citation_budget_policy: sampled
coverage_degraded: null
```

Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261101-225635/TASK-WF-removeTheAnyIssu-20261101-225635.md`. Spec: `source.md` in the same folder. All paths relative to `/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule`. Advisory: this report does not edit the plan.

## Summary

- Coverage: 10/10 parsed requirements (R-001..R-010) map to tasks (`coverage_pct: 1.00`); union with 6 inferred rows 12/16 (`coverage_pct_union: 0.75`); the 4 unmatched inferred rows are carried by the plan's Constraints section.
- Tier: 2 (rule 4, `S_domains` = 3; rule 6 would also fire, calibrated confidence 0.67 for the Tier 1 card). Reviewers: sonnet/analyzer, glm-5.3 (haiku alias)/qa, opus/refactorer; calibrators opus (`calibrator_diversity: degraded`, all three alias classes are reviewers); executor class unresolved (WARN: anti-self-confirmation guarantee weakened).
- Merge: `sc-adversarial-protocol` Mode A, 2 rounds + invariant probe; 26/26 diff points 3-0; convergence BLOCKED_BY_INVARIANTS (INV-001). Merged verdict: `adversarial/merged-verdict.md` — 11 blocking, 17 minor.
- Verdict for the plan: FAIL on blocking findings. Several task checks cannot pass as written (B-01, B-02, B-05) and the Goal "every review loop runs at most 2 fix cycles" would be false (B-03, B-07..B-10).

## Blocking findings (from adversarial/merged-verdict.md)

- **B-01** `tests/audit/test_severity_floor_unweakened.py:48` pins `BASELINE_BLOCK_SHA` over `rf-qa-qualitative.md`'s Critical Rules block (hashed span `:85-106`); Tasks 3 and 11 edit rule 10 at `src/superclaude/agents/rf-qa-qualitative.md:982`; no task re-pins. Fix: re-pin in Task 3 and Task 11 after `make sync-dev` (or move both rule-10 edits to Task 3); keep `BASELINE_SLICE_SHA`.
- **B-02** `src/superclaude/skills/operational-guide/SKILL.md:1349` and `src/superclaude/skills/readme/SKILL.md:2034` contain "Max fix cycles: 3 ..." and "ALL findings must be resolved"; Task 8's grep matches them but no task edits them, so Task 8 cannot pass; Task 11's regex misses this form and the I16 `| 3 |` cells (`src/superclaude/templates/workflow/01_mdtm_template_generic_task.md:649-653`). Fix: Task 8 edits the severity sentence; Task 11 lowers the counts; one shared cap pattern.
- **B-03** `src/superclaude/cli/prd/models.py:203` `max_research_fix_cycles: int = 3`, used at `src/superclaude/cli/prd/executor.py:957`; no task changes it. Fix: Task 11 lowers it to 2 (scope per A-002).
- **B-04** `src/superclaude/cli/prd/prompts.py:1173` keeps "FAIL: ALL findings must be resolved"; Task 6 edits only `src/superclaude/skills/prd/refs/agent-prompts.md:283`. Fix: add `prompts.py:1173` to Task 6 and the wording to Task 13's scan.
- **B-05** The R-008 check at plan lines 24 and 191 (`grep '^+' | grep -n 'src/superclaude'`) matches `+++ b/src/superclaude/...` headers, so it can never print nothing. Fix: `grep '^+[^+]'`.
- **B-06** Task 4 edits `src/superclaude/templates/documents/skill_template.md:815` and `:824` without S1-S3 (+S5), against R-002 (`source.md:6`) and Constraints line 21; Task 13's S1-S3 list omits the file. Fix: add the block in Task 4 and the path in Task 13.
- **B-07** "phase-gate QA failing 3 fix cycles" (allowed-halt rule) at `src/superclaude/skills/operational-guide/SKILL.md:1371`, `src/superclaude/skills/readme/SKILL.md:2058`, `src/superclaude/skills/roadmap/SKILL.md:2587`, `src/superclaude/skills/task/SKILL.md:120`, `src/superclaude/skills/task/SKILL.md:616`, `src/superclaude/skills/task-builder/SKILL.md:2369`, `src/superclaude/skills/tech-reference/SKILL.md:1327`, `src/superclaude/skills/tech-research/SKILL.md:1643`; in no task; Task 11's regex cannot match. Fix: lower all 8 and widen the shared pattern.
- **B-08** "After 3 failed cycles" at `src/superclaude/skills/task/SKILL.md:368`, `src/superclaude/skills/prd/refs/build-request-template.md:130`, `src/superclaude/skills/tdd/refs/build-request-template.md:125`, `src/superclaude/skills/tech-reference/SKILL.md:512`, `:529`, `:1307` escapes Task 11's regex. Fix: lower all and cover the form.
- **B-09** "Per I16 (2-3 per gate)" at `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md:787` and `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:804` survives. Fix: rewrite to the new cap.
- **B-10** `src/superclaude/rules/core/ib_agent_core.md:633` ("Maximum 5 correction attempts per batch"), `:913` ("after 3 attempts"), `:933` (`MAX_CORRECTION_ATTEMPTS` default 5): an installed QA correction loop above the cap. Fix: lower to 2 (B2 "uncapped loops drop to 2").
- **B-11** `src/superclaude/agents/rf-team-lead.md:462` triggers a FIX pipeline on any issue, against S2; the plan changes only its number. Fix: limit the FIX trigger to blocking findings in the same edit that lowers the cap, then re-pin `tests/audit/test_dnsp_all_agents_fail_bypass.py` and its fixture.

## Minor findings (notes; not fixed in extra rounds)

M-01 cli_portify code cap latent (`src/superclaude/cli/cli_portify/steps/panel_review.py:352`); M-02 run `make sync-dev` before each `tests/audit` run (`tests/audit/test_severity_floor_unweakened.py:39`); M-03 keep the binary-verdict tail in FAIL-line replacements (`src/superclaude/skills/readme/SKILL.md:1007`); M-04 Task 12 precision (`src/superclaude/skills/sc-implement-protocol/refs/ledger.md:157`, `:161`, `refs/retry.md:148`, `:189`); M-05 drop the S3 annotation (`.dev/review-severity-rule/inventory.md:22`); M-06 keep the nfr_conv_9 marker (`tests/audit/test_nfr_conv_9_zero_trust.py:249-253`); M-07 S1-S3 not propagated to shared prompt copies; M-08 plan Goal should cite S4 for /sc:implement; M-09 `docs/guides/tdd-skill-release-guide.md:265` out of scope; M-10 add "at any severity" to Task 13's list (`src/superclaude/skills/tech-reference/SKILL.md:536`); M-11 run `tests/cli/reflect/test_no_nesting_guard.py` and `tests/troubleshoot/backtest/test_backtest_e5.py`; M-12 [INFERRED] no kept-path check; M-13 [INFERRED] no A3-A5 survival check; M-14 single-source anchor (`src/superclaude/output-styles/pragmatic.md:224`); M-15 [INFERRED] twin list; M-16 rule 9 "When in doubt, fail it" (`src/superclaude/agents/rf-qa-qualitative.md:981`); M-17 run `tests/cli/prd` too (`src/superclaude/cli/prd/executor.py:1157`).

## Inferred requirements (Pass 2)

Six INF rows (INF-001..INF-006) are listed with quotes and `source.md` citations in `artifacts/coverage-matrix.yaml`; INF-001 and INF-003 matched tasks by containment; INF-002, INF-004, INF-005, INF-006 are carried by the plan's Constraints section.

## Grounding Gaps

None. Evidence validator re-Read all 50 citations: 0 dropped. Drift notes: B-01 `:85-106` are lines of the test helper `_critical_rules_block()`, not of the agent file (the agent block is near lines 970-983); B-07 `task/SKILL.md:120` reads "(2) a phase-gate QA has failed 3 fix cycles" (same meaning); M-05 annotation is at `inventory.md:23`; M-14 the replaced bullet is `pragmatic.md:225` (224 is the binary-verdict anchor). The validator did not test plan-content claims ("no task edits this", "regex cannot match"); those were checked by the three reviewers and the debate.

## Recommendations

### Recommendation R-001: Regenerate the plan with the 11 blocking fixes

- File: a new `/sc:workflow` package (the plan is never edited from reflect findings).
- Change: fold B-01..B-11 into the tasks named in each fix, plus scope decision A-002 (B1/B2 cover `src/superclaude/cli/` code and prompts).
- Verify: the regenerated plan's own Wave 4 pre-review; under the 2-fix-cycle cap this is fix cycle 1 of the plan review loop.

## Inferred-claim audit

citations_inferred: 9 (M-12, M-13, M-15 and six fix assignments marked [INFERRED] in the merged verdict). Not more than half of citations_total; no WARN.
