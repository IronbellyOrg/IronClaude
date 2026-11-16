# Invariant Probe Results

## Round 2.5: fault-finder analysis (opus class, general-purpose agent, read-only)

The fault-finder returned 12 findings. Its own first summary count was wrong and it corrected it: 7 ADDRESSED (all LOW), 5 UNADDRESSED (1 HIGH, 1 MEDIUM, 3 LOW). The column "After Round 3" records the grade after the extra resolution round (`debate/round3-invariant-resolution.md`); the probe's own severity is kept in the Severity column.

| ID | Category | Assumption | Status | Severity | Evidence | After Round 3 |
|----|----------|------------|--------|----------|----------|---------------|
| INV-001 | sufficiency_challenge | Task 1 removes every old-rule bullet from the four digest templates | UNADDRESSED | HIGH | merged-requirements.md:815 "replaces S1, S2 and S5 (where present) with the digest and pointer line"; `agent_template_qa.md:140` holds S5 ("CRITICAL and IMPORTANT findings are blocking") 21 lines above S1 at :161; plan line 37 names lines 85, 157, 158, 161 and 333 and "the definition bullets near line 161" and never S5; no acceptance line, T1 or strict T2 greps for S5 (orchestrator re-checked the four S5 lines: agent_template_qa.md:140, skill_template.md:831, 01_mdtm_template_generic_task.md:647, 02_mdtm_template_complex_task.md:658) | MEDIUM (advocates: blocking, MEDIUM, minor; majority non-blocking, median MEDIUM) |
| INV-002 | interaction_effects | Task 4's one added Unattended line is consistent with the rest of the section | UNADDRESSED | MEDIUM | spec-panel.md:461 "`artifacts` lists `<report-dir>/improved-spec.md` when the Improve step ran ... and it is `[]` otherwise"; stage 2 plan line 102 lists the ledger in `artifacts` when tracked; plan line 89 adds the ledger write and leaves the Contract bullet alone | MEDIUM (advocates: MEDIUM, minor, MEDIUM) |
| INV-003 | interaction_effects | The new Task 4 text passes the three spec-panel tests | ADDRESSED | LOW | test_spec_panel_review_loop (:83-91, :157-159), test_review_loop_extension (:120-127), test_worker_contract (:916-926); plan line 100 runs all three | LOW |
| INV-004 | state_variables | No cap-edit or sweep-edit fixture row has its new text on a line Tasks 1 to 3 replace | ADDRESSED | LOW | nearest row tech-reference:514 is on a separate line; stage 3 dispatch by registry state (S3:192) | LOW |
| INV-005 | guard_conditions | Task 2's brief rewording keeps the brief regex working | ADDRESSED | LOW | test_review_prompt_overrides.py:70 reads each brief with `- {label}: "([^"]+)"`; plan line 64 runs it | LOW |
| INV-006 | guard_conditions | P4:108 "reword or record a named exemption" are interchangeable | UNADDRESSED | LOW | an exempted literal still fails the `grep -rn ... src/superclaude plugins/superclaude` that must print nothing (P4:115) | LOW |
| INV-007 | guard_conditions | P4:113 covers a `doctor.py` reword | ADDRESSED (debate C-009) | LOW | non-strict T2 already fails an unregistered fence literal (S1:223), so the branch is likely moot; C-009 stays as a missing test | LOW (see C-009 MEDIUM) |
| INV-008 | count_divergence | "each edited file names the rule once" (P4:25) | UNADDRESSED | LOW | in `agent_template_qa.md` the digest pointer and the L1 merge line both name `refs/rule.md`; no acceptance line counts it | LOW |
| INV-009 | count_divergence | Pinned counts match the tree | ADDRESSED | LOW | HALT 2, 5, 6; cap counts 5, 6, 1, 2; "follow-up candidates" 3 lines; old sentence in 11 files; merge-rule hits on the 6 named lines | LOW |
| INV-010 | collection_boundaries | P4:48's parenthetical list is the whole surviving allow-list | UNADDRESSED | LOW | S3:214 also keeps `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py`; "every entry" covers them | LOW |
| INV-011 | sufficiency_challenge | "No merge-rule phrase left" | ADDRESSED | LOW | `task/SKILL.md:252`, `:361` and `sc-auggie-review-protocol/SKILL.md:228` still match and pass through the `exempt-by-retirement` and `allowed` rows (P4:22) | LOW |
| INV-012 | collection_boundaries | Zero hits in the settling greps | ADDRESSED | LOW | P4:111 already requires "says so" | LOW |

Not found by the probe: no test outside the plan's run list (P4:113) pins a stage 4 file's replaced text (it grepped `tests/` for every edited file name and phrase).

## Summary

- **Total findings**: 12
- **ADDRESSED**: 7
- **UNADDRESSED**: 5
  - HIGH: 1 (INV-001, lowered to MEDIUM after Round 3)
  - MEDIUM: 1 (INV-002)
  - LOW: 3 (INV-006, INV-008, INV-010)

Gate: CONVERGENCE was BLOCKED by 1 HIGH-severity UNADDRESSED invariant (INV-001) until the Round 3 resolution round (`debate/round3-invariant-resolution.md`) debated it with all three advocates; it is now addressed and graded MEDIUM. Not checked by the probe: the stage 3 rewrite of `test_review_severity_rule.py` does not exist yet, so whether its v2 branch asserts that S5 is gone is unknown.
