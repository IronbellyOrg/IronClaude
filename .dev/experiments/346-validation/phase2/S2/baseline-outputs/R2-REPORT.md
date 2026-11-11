# Reflect pre-execution report — TASK-WF-removeTheAnyIssu-20261102-042031 (review 2 of 3)

```yaml
contract_version: 1.8.0
status: partial            # STOP input_drift at the Wave 5 pre-synthesis guard
mode: pre
tier_reached: 2
confidence_calibrated: 0.81  # Tier 1 card; reviewer cards not calibrated (run stopped before Wave 3C)
citations_total: 0           # evidence-validator not run (stopped before Wave 5)
citations_revalidated: 0
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: null
input_drift_detected: true
```

Plan: `.dev/tasks/to-do/TASK-WF-removeTheAnyIssu-20261102-042031/TASK-WF-removeTheAnyIssu-20261102-042031.md`. Advisory; the plan is not edited from these findings.

## Why the run stopped

`.dev/review-severity-rule/inventory.md` (an input in `artifacts/input-snapshot.yaml`) changed on purpose during Wave 3: the coordinator answered a new question (cli-portify default = 1 iteration, inventory section 4 item 3a). Per SKILL.md §4.0 Step 0.4 a changed input tree stops the run with `status: partial` (old tree `9348ca52…`, new tree `c20ea1fb…`; only `inventory.md` differs). Waves 3C (per-card calibration), 4 (adversarial merge) and 5 (evidence validator) did not run. The findings below come from the Tier 1 card (calibrated 0.81), the Wave 1B coverage matrix and three Tier 2 reviewer cards (sonnet, glm-5.3, opus), each of which Read its cited lines; none was re-read by the evidence validator.

## Blocking findings (to fold into fix cycle 2)

- **P2-B1** Task 5 cannot pass and R-003 is unmet: the lite at-cap sentence "unresolved issues become Open Questions" at `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md:938` and `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:1090` is in no task (T1-F1, confirmed by calibrator and coverage).
- **P2-B2** Open-Questions at-cap rules at `src/superclaude/skills/task-builder/SKILL.md:1420` ("as an Open Question ... and proceed") and `src/superclaude/skills/roadmap/SKILL.md:569` are in no task; the `rf-task-builder.md:384/386` cells have no check (coverage).
- **P2-B3** CAP_PATTERN cannot detect 11 IN lines (`tech-reference/SKILL.md:177`, `roadmap/SKILL.md:554`, `cli_portify/commands.py:100-101`, `sc-cli-portify-protocol/SKILL.md:355/363/364/374/534`, `decisions.yaml:123`, `ib_agent_core.md:933`), `range(1, 4)` at `convergence.py:150`, "correction loops", and leftover 3s on lines it does match; cap-sites rows are not literal enough for a per-row check (coverage, R1-F7, R3-03). Fix: give every IN row literal `old` / `new` substrings and check each row (old count 0, new count >= 1).
- **P2-B4** Task 18(d) checks the canonical cap text only in `pragmatic.md`; R-006 requires it in the at-cap IN files (coverage).
- **P2-B5** cli-portify semantics: one iteration = 2 review passes + 2 fix passes (`sc-cli-portify-protocol/SKILL.md:283-336`), so the plan's default 2 = 4 fix passes; the coordinator decided default 1 (inventory 4.3a). Task 15, cap-sites section 12 note, `tests/cli_portify/test_convergence.py:78-86` and the CHANGELOG line must use 1 (R1-F1, F2-1).
- **P2-B6** `src/superclaude/rules/core/ib_agent_core.md:574` "Maximum 5 correction loops per batch" is in no task or check (R1-F2).
- **P2-B7** Task 12's whole-line replacements for `rf-qa.md:537` and `agent_template_qa.md:335` drop the blocking-findings sentence Tasks 2/4 add; no check sees it (R3-01, R1-F6). Fix: do those cap edits inside Tasks 2 and 4 (as Task 3 does for `rf-qa-qualitative.md:982`).

## Minor findings (notes)

`test_nfr_conv_9_zero_trust.py:432` assert not named in Task 2; `task-builder/SKILL.md:901` has no "max-3-cycles" token and dnsp test method `test_fix_cycles_line_contains_max_3_cycles_token` (`:395`) keeps the old name; Task 17 never checks ledger row V (`ledger.md:157`); Task 10 never checks `task-builder:870`; Task 15 "ten" files vs nine; Goal should state /sc:implement's worst case stays its own count; no check that OUT sites stay unchanged; Tasks 1/7 skip some readers until Tasks 13/18; Tasks 2/3 rewrite blocks containing cap lines 390/797; section 18 OUT rows skip middle lines; Tasks 2-5/11 must copy S1-S5 from `pragmatic.md` (no labels) and Task 18(c) should reject labels; Task 18(c) should strip a leading "- "; Tasks 4/5 should depend on Task 3 (or tasks run in number order); `rf-task-executor.md:226` "retry up to 5 times" sample output unclassified; FAIL-line tails "Only PASS or FAIL — no conditional pass." and "List each ..." have no check.

## Recommendation R-001: fix cycle 2 (the last one)

Regenerate the plan once more with P2-B1..P2-B7 folded in and a per-row literal cap check; its pre-review is review 3 of 3. If blocking findings remain after it, stop and escalate them to the user (rule S3).
