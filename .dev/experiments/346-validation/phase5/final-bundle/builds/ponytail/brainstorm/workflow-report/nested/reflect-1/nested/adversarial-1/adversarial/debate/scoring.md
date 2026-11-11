## Round 2.5: Invariant Probe

See `invariant-probe.md`: 12 findings, 2 HIGH UNADDRESSED (INV-001, INV-003), which block convergence.

## Round 3

Skipped: depth=standard.

## Shared-assumption responses

| A-NNN | V1 | V2 | V3 | Outcome |
|---|---|---|---|---|
| A-001 owner rulings genuine and binding | QUALIFY (Unattended ruling mechanically forced anyway; T10 ruling uncited in plan) | QUALIFY (msg_7b27 cited plan:26 and checkable; msg_2000 only in orchestrator notes) | QUALIFY (only Unattended ruling cited by id) | Agreed QUALIFY: binding for classification; the plan should cite msg_2000b167e322 at plan:193 |
| A-002 severity judged against literal plan execution; AC is the guard | ACCEPT | QUALIFY (body directives bind too; AC-only omission of a body-incorporated rule is minor) | ACCEPT | Agreed (majority ACCEPT); V2 conceded in Round 2 that plan:55 narrows the incorporated rule, so C-005 falls on the "not delivered" side |
| A-003 inherited spec defects count against the plan | QUALIFY (counts for severity when ACs are unsatisfiable; classify inherited) | ACCEPT (tag spec-inherited; fix both documents) | QUALIFY (same as V1) | Agreed: counts for severity; classified necessary deviation (spec-inherited), never plain drift |

Omissions: none (every advocate answered A-001..A-003).

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L1 | V1 = V3 (flat schema), plus V2 `category` and list evidence | 85% | All three proposed the same merged schema in Round 1 |
| S-002 | L1 | V3 `actively_checked` + V1 `checked_sound` | 80% | Unanimous combination |
| S-003 | L2 | V3 (one finding per cluster) | 85% | V1 conceded R1-F9 bundled two issues |
| C-001 | L3 | V1 | 95% | Unanimous blocking; spec-panel.md:220 vs plan:134, 147; all advocates conceded they missed it |
| C-002 | L2 | V3 fix, V1 severity (minor) | 85% | V3 conceded severity; guard keys on the heading (WORKER-CONTRACT case 2); `--improve` not orphaned (spec-panel.md:35) |
| C-003 | L3 | V1 = V3 (minor) | 90% | V2 conceded; FAIL still forced (plan:101, 114); spec self-inconsistent (src.md:133 vs 183) |
| C-004 | L3 | V1 = V3 (minor) | 75% | Unanimous minor; probe INV-008 argues the wrong-behaviour half is met on failed-audit paths (kept minor, noted) |
| C-005 | L3 | V3 | 85% | Unanimous blocking after Round 2 (V2 conceded); plan has no FR-8/FR-9 string; plan:55, 58 drop the tag; src.md:140, 218, 231 |
| C-006 | L2 | V3 | 85% | Fuller scope (docs/ and .dev/tasks, src.md:174) |
| C-007 | L2 | V1 | 85% | Unique to V1; plan:29 rule vs plan:147 list; plan:182 installs fix_audit.py |
| C-008 | L2 | V3 (recorded, not a finding) | 85% | V1 conceded in Round 2; authorized expansion; plan should cite msg_2000b167e322 |
| C-009 | L2 | V1 | 75% | Unique to V1; INFERRED; label regression (V1, V3) vs drift (V2) |
| C-010 | L3 | V2 (finding), V1/V3 (minor) | 80% | V2 conceded minor; V1's owner-count evidence (plan:101 vs plan:21) makes it top minor, fix required |
| C-011 | L3 | dropped | 90% | V1 conceded; calibrator not-confirmed |
| X-001 | L3 | V1 (minor) | 85% | Resolved with C-002 |
| X-002 | L3 | V1 = V3 (minor) | 90% | Resolved with C-003 |
| X-003 | L3 | V3 (blocking, narrowed) | 85% | Resolved with C-005 |
| X-004 | L3 | V2 = V3 (C-003 drift; C-010 necessary deviation, spec-inherited) | 70% | V1 held "drift (spec-inherited)" for C-010; 2/3 majority |
| X-005 | L3 | V3 (authorized expansion) | 85% | Resolved with C-008 |
| A-001 | L2 | all (QUALIFY) | 80% | Unanimous qualify |
| A-002 | L3 | V1 = V3 (ACCEPT) | 75% | Majority |
| A-003 | L3 | V1 = V3 (QUALIFY) | 75% | Majority; same practical outcome as V2 |

Classification outcomes with a 2/3 majority (dissent recorded): C-007 and C-010 necessary deviation (spec-inherited) (V1: drift (spec-inherited)); C-009 regression (V2: drift).

Taxonomy coverage: L1 2 points, L2 7, L3 13 debated; all levels covered; no forced round.

## Convergence Assessment
- Points resolved: 22 of 22 (unanimous 16, majority 6)
- Alignment: 100%
- Threshold: 80%
- Taxonomy gate: passed (L1, L2, L3 all covered)
- Invariant gate: BLOCKED (INV-001, INV-003 HIGH UNADDRESSED)
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement meets the threshold; convergence is not declared)
- Unresolved points: none among the 22 diff points; INV-001 and INV-003 remain open outside them
