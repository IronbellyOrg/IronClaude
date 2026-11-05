# Merge Log

## Metadata
- Base: Variant 1 (reviewer-1 analyzer card), per base-selection.md (tiebreaker level 1, debate points won).
- Plan executed: adversarial/refactor-plan.md (12 required plan notes, 6 executor notes, 3 owner questions, 5 not-made items).
- Merged artifact: adversarial/merged-verdict.yaml
- Plan approval: auto-approved (non-interactive run).
- Escalations to the orchestrator: none. Every planned change was applied as written.

## Per-Change Execution Log

| Change | Status | Provenance tag | Placement in merged-verdict.yaml | Summary of what was applied |
|---|---|---|---|---|
| RN-1 | applied | Variant 1 (base), merged per Change RN-1 with Variant 2 (R2 point b), Variant 3 (F4), INV-003 | required_plan_notes[RN-1]; also findings_by_severity.blocking_until_criterion | Fallback order and test cases carried over as written; marked blocking-until-criterion (debate point X-001); risk Medium |
| RN-2 | applied | Variant 1 (base), merged per Change RN-2 with Variant 3 (F4), X-003, INV-002 | required_plan_notes[RN-2] | Lift of Claude --name/-n dropped; name-carried rule and CCSESSION_NAME rule kept; owner report cross-linked to OQ-2; risk Medium |
| RN-3 | applied | Variant 1 (base), merged per Change RN-3 with Variant 3 (F1), INV-006 | required_plan_notes[RN-3] | Early fast-path dispatch (ccsession:597-628) and loop reference (ccsession:648-723) kept verbatim; four hostile-text tests; risk Low |
| RN-4 | applied | Variant 3, merged per Change RN-4 (F2), extended by Variant 1 (F6, F7), Variant 2 (F2), Variant 3 Round 2 | required_plan_notes[RN-4] | Five test changes plus env exclusion lists in test_ccsession_tag.py and test_ccsession_tiers.py; risk Low |
| RN-5 | applied | Variant 1 (base), F2 and F5, required per Variant 3 | required_plan_notes[RN-5] | `IFS= read -r`, raw-line checks, `--` before text that starts with `-`; five tests; risk Medium |
| RN-6 | applied | Variant 3, merged per Change RN-6 (new point), INV-010 | required_plan_notes[RN-6] | Unset of CCSESSION_ASK_TIMEOUT and CCSESSION_NAME before the final exec; risk Low |
| RN-7 | applied | Variant 1 (base), merged per Change RN-7 with A-004, INV-005 | required_plan_notes[RN-7] | Equals forms, trailing --name, value-taking options not counted as a task, unknown options fail safe; risk Medium |
| RN-8 | applied | Variant 2, merged per Change RN-8 (F1) | required_plan_notes[RN-8] | CCSESSION_ASK_TIMEOUT=2 hint test plus default-hint test; risk Low |
| RN-9 | applied | Variant 1 (base), merged per Change RN-9 with Variant 2 (F5), Variant 3 (F8), INV-004 | required_plan_notes[RN-9] | Seconds or random part in the stamp; cut order for the 80-character cap; same-minute test; risk Low |
| RN-10 | applied | Variant 3, merged per Change RN-10 (F3) | required_plan_notes[RN-10] | Executor writes launch-paths.md; no test opens a path outside tmp_path; risk Low |
| RN-11 | applied | Variant 3, merged per Change RN-11 (F5) | required_plan_notes[RN-11] | Hint passed by ccsession-orca only; old default kept; Task 11 handoff states the 30 s default; risk Low |
| RN-12 | applied | Variant 2, merged per Change RN-12 (F3) | required_plan_notes[RN-12] | Task 9 criterion pins the --session-id statement (README.md:266); risk Low |
| EN-1 | applied | Variant 1 (base), V1 F3 | executor_notes[EN-1] | Second paste probe, set -e guard (ccsession:98) |
| EN-2 | applied | Variant 1 (base), V1 F4, INV-011 | executor_notes[EN-2] | python3 raw-byte drain (ccsession:1426), 128 KiB cap |
| EN-3 | applied | Variant 1 (base), V1 F13 | executor_notes[EN-3] | rc capture, INT trap, exact 130 and ICANON check |
| EN-4 | applied | Variant 1 (base), V1 F9 | executor_notes[EN-4] | Pass-through verification note |
| EN-5 | applied | Invariant probe INV-009 | executor_notes[EN-5] | CCSESSION_NAME is name-carried and skips the pull request 355 reopen; document it |
| EN-6 | applied | Variant 3, V3 F6 and F7 | executor_notes[EN-6] | One ordered decision list; `-k orca` expected to fail until Task 5 |
| OQ-1 | applied | Variant 3 (scope_additions keep) | owner_questions[OQ-1] | Print mode and CCSESSION_AUTOSTART=0 stay untagged |
| OQ-2 | applied | Variant 1 (base, F10) with Variant 3 (F4), X-003 | owner_questions[OQ-2] | RN-2 reverses the plan Constraint that lifts Claude --name |
| OQ-3 | applied | Invariant probe INV-001 | owner_questions[OQ-3] | HIGH, addressed as a documented condition (ccsession:1482-1489); Task 9 and Task 11 must say so |

### "Changes NOT Being Made" (recorded in downgraded_or_rejected)
| Item | Status | Disposition |
|---|---|---|
| V1 F1 auto-name half as a blocker | applied (recorded) | downgraded; kept as RN-1's folder-name case only |
| V1 F3, F8, F9, F13 | applied (recorded) | downgraded to executor notes or folded into RN-6 |
| V3 F4 class "authorized" | applied (recorded) | rejected; lift dropped (RN-2) |
| V2 F5 hook-suffix mitigation | applied (recorded) | rejected as a guarantee (ccsession:336-337, 391-398) |
| Change to the plan package itself | applied (recorded) | not made |

### Top-level fields
- merge_method adversarial; base_variant variant-1 (reviewer-1 analyzer); status ready-with-notes; convergence_score 0.8889; unresolved_conflicts 0; fallback_mode false.
- invariant_probe: total 12, unaddressed_high 0, unaddressed_medium INV-002, INV-003, INV-005; unaddressed_low INV-004, INV-006, INV-009, INV-010 (matches invariant-probe.md summary).
- findings_by_severity: blocking-until-criterion 1 (X-001 / RN-1); required plan notes 12 (RN-1 included, 4 Medium and 8 Low); executor notes 6; owner questions 3.

## Post-Merge Validation

### Structural
- YAML parses with PyYAML (`yaml.safe_load`): pass.
- Tab characters in the file: 0.
- Required top-level keys present: merge_method, base_variant, status, convergence_score, unresolved_conflicts, fallback_mode, invariant_probe, required_plan_notes, executor_notes, owner_questions, downgraded_or_rejected, findings_by_severity (plus review_status and standing_rule carried from the plan).
- Entry counts: required_plan_notes 12 (RN-1..RN-12, each with id, title, source_findings, target_tasks, requirement, acceptance_check, provenance), executor_notes 6, owner_questions 3, downgraded_or_rejected 5.

### References
- Every file:line reference in the merged verdict was extracted and searched for in the plan, the variant cards, the debate transcript, base-selection.md and the probe. Found in sources: ccsession:98, ccsession:597-628, ccsession:648-723, ccsession:1426, ccsession:1482-1489, ccsession:336-337 and 391-398, README.md:266. Missing: none.
- No reference was added that the plan did not use. Test and file names (test_ccsession_tag.py, test_ccsession_tiers.py, the named tests) appear in the plan text.
- The acceptance_check text for RN-4 and RN-12 adds only the verification commands named in variant cards V2 F2, V3 F2 and V2 F3.

### Contradictions
- No new contradictions. RN-2 intentionally replaces Task 3 criterion 2 and the Task 7 `--name x` case and is reported through OQ-2; this matches the plan.
- RN-6 resolves the plan's Task 4 contradiction (timeout test sets CCSESSION_ASK_TIMEOUT while the record must not contain it); the verdict states this once.
- EN-5 (CCSESSION_NAME skips the reopen) is consistent with RN-2 (CCSESSION_NAME is name-carried).
- Status ready-with-notes agrees with unresolved_conflicts 0 and with the probe gate (no HIGH item unaddressed).
