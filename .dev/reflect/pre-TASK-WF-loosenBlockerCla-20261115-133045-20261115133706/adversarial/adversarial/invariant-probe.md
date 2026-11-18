# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis

Fault-finder: independent opus agent, not an advocate. Source file: debate/round25-fault-finder.md. "Orchestrator check" says what the orchestrator re-read on disk before keeping or changing the grade. "Merged card" says where the item landed.

| ID | Category | Assumption | Status | Severity | Evidence | Orchestrator check | Merged card |
|----|----------|------------|--------|----------|----------|--------------------|-------------|
| INV-001 | sufficiency_challenge | The B7 fix (rewrite rf-qa-qualitative's 8 label-based FAIL bullets) removes every FAIL-by-label bullet beside a v2 digest | UNADDRESSED | HIGH | src/superclaude/templates/documents/agent_template_qa.md:158 "FAIL - Any CRITICAL or IMPORTANT issue exists"; Task 34 edits only lines 161, 85, 333 (plan:405) | Read agent_template_qa.md:156-161: bullet present 3 lines above the definition at 161. Kept HIGH | F11, origin fault-finder |
| INV-002 | guard_conditions | The stage-2 final-gate sweep is a shadow observer consistent with "the old definition still decides every gate outcome" | UNADDRESSED | HIGH | plan:250 sweep "becomes Blocking at that gate"; plan:261 "old definition still decides"; plan:273 wires the sweep at Gate 5 with no shadow guard; pragmatic.md:230 Medium "never fails a review" | Read plan:250, 261, 273 and pragmatic.md:230. Kept HIGH | F12, origin fault-finder |
| INV-003 | sufficiency_challenge | Task 30's L3 edit at task/SKILL.md:258 applies L3 everywhere the spec puts it | UNADDRESSED | MEDIUM (re-graded from HIGH) | spec:272 lists rf-qa.md:402-415 and task/SKILL.md:258, 372; task/SKILL.md:372 and :409 and rf-qa.md:402 keep a plain HALT | Read spec:272, task/SKILL.md:372, 409, rf-qa.md:402. Spec does not say at which stage L3 applies (spec:947 omits L3), so not a clear wrong result | F15, origin fault-finder, non-blocking |
| INV-004 | interaction_effects | B9's fix gives tech-research exactly one offer per run | UNADDRESSED | MEDIUM | tech-research/SKILL.md:614 "Execution transfers to /task"; plan:261 /task already ends with an offer | Read tech-research/SKILL.md:614-621 | folded into F7 as a fix note |
| INV-005 | interaction_effects | Gate 5 is the last gate before delivery | UNADDRESSED | MEDIUM | tech-research/SKILL.md:415; task/SKILL.md:290 final validation runs after Gate 5 | Read both lines | folded into F3 and F12 as a fix note |
| INV-006 | interaction_effects | B2 can be fixed by registering rule.md or exempting it | UNADDRESSED | MEDIUM | registering breaks plan:150 and plan:230; Task 39 mirrors rule.md into plugins/ (plan:459), where T2 also scans | Read plan:150, 230, 459 | folded into F2 as a fix note |
| INV-007 | sufficiency_challenge | Allow-listing the two code files is enough for the Task 33 scan | UNADDRESSED | MEDIUM | Task 7 copies GR1-GR12 into rule.md (plan:101); spec:651 GR5 contains "highest severity wins"; scale-map row quotes "keep the higher severity" (spec:746) | Read spec:651, 746 and plan:101, 113, 394 | folded into F5 as extra hits |
| INV-008 | interaction_effects | Task 31 can edit the two fixtures alone | UNADDRESSED | MEDIUM | tests/skills/test_review_severity_rule.py:275-283 test_ej requires byte equality with .dev/review-severity-rule/cap-edits.yaml and sweep-edits.yaml (both tracked); plan:372, 376 name only the fixtures | Read the test and git ls-files | F16, origin fault-finder, non-blocking |
| INV-009 | sufficiency_challenge | An owner stop after Phase 1 is enough because Phase 1 writes the stage 0 result | UNADDRESSED | MEDIUM | plan:77 says steps 0a and 0c are not skipped; Grep "0a" finds it only at plan:77; spec:944 defines 0a | Grep run | folded into F4 as a fix note |
| INV-010 | sufficiency_challenge | One deferral sentence covers plan-input item 4 | UNADDRESSED | MEDIUM | plan-input:16 has two populations; Task 4 carries only the stage 0b sample, not "proved real" cases (plan:66) | Read plan-input:16, plan:66 | folded into F9 |
| INV-011 | sufficiency_challenge | Adding per-input row counts to Task 16 gives the measurement plan-input item 3 needs | UNADDRESSED | MEDIUM | no task builds code suppliers for M, C, E inputs; Task 10 only documents "Needs from code" (plan:138); judges are Fixture and Reviewer (plan:180) | Read plan:138, 180, 203 | folded into F10 |
| INV-012 | count_divergence | Task 39 and Task 11 agree on the number of installed-only variants | UNADDRESSED | LOW | plan:464 says "two"; plan:146, 151 name five | Read plan:464, 146, 151 | not carried (LOW) |
| INV-013 | state_variables | N1: Task 30 criterion assumes the task skill holds CANONICAL_CAP_TEXT | ADDRESSED (debate-surfaced, verified) | LOW | task/SKILL.md has no "at most 2 fix cycles"; cap sentences at 258, 372, 409 | Grep run | not carried (LOW); used as evidence in F16 |
| INV-014 | guard_conditions | Every prerequisite is stated in a "Depends on" line | UNADDRESSED | LOW | Tasks 21, 22 miss Task 14 and 16; Task 26 and 34 have no matching dependency line | not re-read | not carried (LOW) |

## Summary

- **Total findings**: 14
- **ADDRESSED**: 1
- **UNADDRESSED**: 13
  - HIGH: 2 (INV-001, INV-002)
  - MEDIUM: 9 (INV-003 to INV-011)
  - LOW: 2 (INV-012, INV-014)

## Gate resolution

Per the invariant probe gate, 2 HIGH UNADDRESSED items would block convergence. They are new defects in the reviewed plan, not gaps in the debate consensus about the two cards. The orchestrator resolves the gate by carrying both into the merged card as findings F11 and F12 with citations verified on disk (origin: fault-finder), which is the acknowledgement action the gate asks for. They are also listed in return-contract.yaml under unaddressed_invariants.
