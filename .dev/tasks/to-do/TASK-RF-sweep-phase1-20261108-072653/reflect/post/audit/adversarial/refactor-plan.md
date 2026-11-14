# Refactoring Plan: Merge into Base (Variant 3)

## Overview
- Base: Variant 3 (reviewer 3, refactorer, opus; final score 0.796, see `base-selection.md`)
- Incorporating strengths from: Variant 1 (analyzer/sonnet), Variant 2 (qa/haiku)
- Planned changes: 13 (4 corrections of base weaknesses, 6 incorporations from V1 and V2, 2 base findings kept as they are, 1 verdict-level carry-over)
- Risk level: Low overall (a classification merge; no code or repository file changes; every change is a field in the merged verdict)
- Output shape: the merged verdict is a YAML `findings:` list, one finding per surviving diff point (17 findings, F-01..F-17), fields `id, title, class, severity, lead_ref, evidence, authorization_source, reasoning, confidence, notes`. Numbered by class order: Regression first, then Drift medium, then the rest (Drift minor, Authorized, Necessary), each group in descending debate confidence from the Scoring Matrix in `debate-transcript.md`. S-002 holds: no finding is blocking.

### Finding id map (which finding carries which diff point)

| Finding | Diff point | Class / severity | Source card finding(s) | Carried notes |
|---|---|---|---|---|
| F-01 | C-003 / X-003 | Regression medium (contested) | V3 R3-F3, V1 R1-F4 | dissent note; INV-005 |
| F-02 | C-012 / X-005 | Drift medium | V2 R2-F4 | INV-012 (tests whose names claim more than they assert) |
| F-03 | C-009 | Drift medium | V2 R2-F1 | none |
| F-04 | C-004 | Drift medium | V1 R1-F3 | INV-001/INV-002 conditional escalation; INV-008 |
| F-05 | C-002 / X-002 | Drift minor | V3 R3-F4, V2 R2-F5 | head not read, misnamed test; INV-007 |
| F-06 | C-005 (carries DC-12) | Drift minor | V1 R1-F5, V3 R3-F3 (mention) | none |
| F-07 | C-008 | Drift minor | V1 R1-F6/R1-F7, V3 R3-F8 | split: constants and `freshness_age_s` Drift; `mtime` and `agent_wait_since` Necessary |
| F-08 | C-016 | Drift minor | V3 R3-F6 | none |
| F-09 | C-017 | Drift minor | V3 R3-F7 | none |
| F-10 | C-006 | Drift minor, hardening follow-up | V3 R3-F1 | V1 view: medium |
| F-11 | C-007 | Drift minor, hardening follow-up | V3 R3-F2 | V1 view: medium; SPEC :291 untimed disk reads |
| F-12 | C-015 | Drift minor | V3 R3-F5 | V1 view: medium |
| F-13 | C-001 / X-001 | Authorized minor | V1 R1-F1, R1-F2, V2 R2-F6 | residual footnote Drift minor (FIN-F15); agent-wait feed Necessary |
| F-14 | C-014 | Authorized minor | V3 R3-F9 | none |
| F-15 | C-010 | Authorized medium | V2 R2-F2 | none |
| F-16 | C-013 / X-004 | Authorized minor | V3 R3-F10 | T1 lead DC-5 said Necessary; not adopted |
| F-17 | C-011 | Necessary medium | V2 R2-F3 | environmental causes re-confirmed |

C-018 has no finding (dropped as aligned). Severity of the Authorized and Necessary rows is the calibrator-supported one (R3-F9 minor, R2-F2 medium, R3-F10 minor, R2-F3 medium; R1-F1 minor with V2/V3 impact noted as medium).

## Planned Changes

### Change 1: Keep the C-003 Regression, add the dissent note (from Variant 1) - F-01
- **Source**: V3 R3-F3 (base); V1 R1-F4 and both blind calibrations (Drift medium) for the dissent; INV-005 from `invariant-probe.md`.
- **Target**: Base R3-F3 (modify). Class stays Regression, severity medium.
- **Rationale**: Scoring Matrix C-003, 62%, 2 of 3 (V2, V3 Regression; V1 and both calibrators Drift). Round 1 orchestrator check: the autouse guard patches `Popen` and `os.system` as well as `subprocess.run` (`tests/sweep/conftest.py:36-41`), so the task's reason for `subprocess.run` (task :1452) is false; Round 2 V1 conceded the departure is unforced and unapproved. Observable difference: runaway child gives `unavailable` "timeout after N s" instead of `call_failed` "output over 8 MiB" (INV-003 shows it fails closed).
- **Integration point**: finding `notes`: "contested: V1 and both blind calibrators class this Drift medium (no acceptance fixture fails, SPEC :297 fixtures pass); fallback if the narrow A-002 rule is adopted". Add INV-005 as a note (first call turns any `call_failed` into `unavailable`, `probes.py:355-357`).
- **Risk**: Medium - the class is a judgment call; the note makes the dissent visible so a reader can overrule it.

### Change 2: Lower R3-F4 from Regression to Drift minor (from Variants 1 and 2) - F-05
- **Source**: V2 R2-F5 (calibrated Drift low), V3 R3-F4, V1 and V2 Round 2 concessions, V3 Round 2 withdrawal.
- **Target**: Base R3-F4 (replace class and severity).
- **Rationale**: Scoring Matrix C-002, 85%: tail-only search has the same output (SPEC :295, DESIGN :62); all three advocates settled on Drift minor. Both blind calibrators placed it at Drift low.
- **Integration point**: one finding covering the unread head (`probes.py:563-565`) and the misnamed test `test_ledger_over_the_limit_is_read_as_head_and_tail` (asserts a tail-derived boolean, `test_probes_allowlist.py:1320-1331`); INV-007 note (the first line of the tail is always dropped, `probes.py:565`, pinned by `test_probes_allowlist.py:1336-1346`).
- **Risk**: Low - three-way agreement.

### Change 3: Lower the hardening findings to Drift minor follow-ups - F-10, F-11, F-12
- **Source**: V3 R3-F1, R3-F2, R3-F5 (base); V3 Round 2 self-correction.
- **Target**: Base R3-F1, R3-F2, R3-F5 (severity medium to minor).
- **Rationale**: C-006 and C-007 at 66%: already filed as `[Low]` follow-up (task :3066) and MINOR notes in `qa-readonly-safety-report.md:13-14`, `:55-56`; `-c core.fsmonitor=false` changes the pinned NFR-002 argv (`design-base.md:343`) so it needs an owner note; SPEC :291 itself says disk reads are untimed. C-015 at 62%: the path is tool-chosen under `<root>/.dev/sweeps/`.
- **Integration point**: severity field plus note "V1 view: medium" on F-10, F-11, F-12; F-10 keeps the docstring and CHANGELOG contradiction text; F-11 states the sibling reader checks `is_file` (fix cite to the tab-map reader; the `probes.py:837` citation failed calibration).
- **Risk**: Low - severity only, wording unchanged.

### Change 4: Split C-008 by field (from Variant 1 calibration) - F-07
- **Source**: V1 R1-F6 (extra source row, Drift minor), V1 R1-F7 as calibrated (constants and `freshness_age_s` Drift; `mtime` and `agent_wait_since` Necessary), V3 R3-F8.
- **Target**: Base R3-F8 (restructure, one finding with a split note).
- **Rationale**: Scoring Matrix C-008, 80%, V1 and V3 agree. FINAL-GATE :19 only approves marking unused fields reserved; FIN-F10 records the additions.
- **Integration point**: class Drift minor; note lists which fields are Necessary. V1's `authorized` label for R1-F7 is not carried.
- **Risk**: Low.

### Change 5: Add the Rule 5 finding with its footnote residual (from Variant 1) - F-13
- **Source**: V1 R1-F1, R1-F2; V2 R2-F6 (the same fact, calibrated Authorized medium).
- **Target**: Base, new finding (V3 did not examine C-001).
- **Rationale**: Scoring Matrix C-001 / X-001, 88%; `FINAL-GATE-halt-resolution-decision.md:17-19` edits DESIGN :491 and :760 and records "All 3 approved"; DESIGN section 13 stays at 10 rows (:840). Round 2: V1, V2, V3 all end on Authorized.
- **Integration point**: authorization_source = that decision file; note "SPEC FR-006 (:100) never amended"; residual footnote Drift minor (FIN-F15, `report.py:42-45` names only stalled and fenced, `working: 0` has no caveat); sub-note: the agent-wait feed of Rule 4(a) is Necessary (inline `probes.py:432-434`, `1.0a-facts.md:35`).
- **Risk**: Low - V2's regression label is explicitly rejected (see table below).

### Change 6: Add the dropped-worker-row finding (from Variant 1) - F-04
- **Source**: V1 R1-F3 (unique U-001), `invariant-probe.md` INV-001, INV-002, INV-008.
- **Target**: Base, new finding.
- **Rationale**: Scoring Matrix C-004, 80%. `probes.py:1105-1119` keeps a row only for a non-empty string id; `classify.py:690-694` reads only `orca worker-list {run}`; the all-rows-dropped case ends in `person_started=True` (`classify.py:759-762`). Orchestrator ruling: Drift medium, not a bug in FR-010's enumerated rule.
- **Integration point**: note the conditional escalation: if real Orca emits worker rows without `dispatchId` (queued or undispatched), it becomes a wrong-class bug; `tests/sweep/fixtures/captured-worker-list.json` has 5 rows, all with `dispatchId`, others UNVERIFIED; no test covers it. INV-008 note: `len(workers) >= 100 or hasMore` counts dict entries after filtering (`probes.py:1042-1046`).
- **Risk**: Medium - largest uncertainty in the merge; escalation condition is stated.

### Change 7: Add the `_git` reason-wording finding (from Variant 1) - F-06
- **Source**: V1 R1-F5; V3 R3-F3 mention; T1 lead DC-12.
- **Target**: Base, new finding (absorbs DC-12; no separate finding).
- **Rationale**: Scoring Matrix C-005, 82%: `probes.py:316` says bytes, SPEC :286 says `8 MiB`; the string is pinned at `test_probes_allowlist.py:1454` and collapsed to `worktree not readable` at `probes.py:936-937` (DESIGN :513).
- **Integration point**: Drift minor; mention `_orca` prints MiB (`:271-273`).
- **Risk**: Low.

### Change 8: Add the stale-text finding (from Variant 2) - F-03
- **Source**: V2 R2-F1 (unique U-003).
- **Target**: Base, new finding.
- **Rationale**: Scoring Matrix C-009, 85%; DESIGN :5 and :7 still say WC-16 approval is required and "NOT a clean pass"; task :3037-3043 keep OQ-2..OQ-8 PENDING although decision records exist. Round 2 V2: reconcile before documentary completion, not a runtime-promotion veto.
- **Integration point**: Drift medium; recommendation text from the Tier-1 card (set OQ-2..OQ-8 RESOLVED, update the DESIGN header).
- **Risk**: Low.

### Change 9: Add the NFR-007 publication-test finding at Drift medium (from Variant 2) - F-02
- **Source**: V2 R2-F4 (calibrated Drift medium); INV-012.
- **Target**: Base, new finding.
- **Rationale**: Scoring Matrix C-012 / X-005, 88%: `test_probes_allowlist.py:1144-1147` and `:1169` stop at `report.render` (orchestrator re-read); SPEC :136 and DESIGN :760 claim publication. V2 conceded blocking in Round 2; nothing shows publication fails.
- **Integration point**: Drift medium; fix the "FIN-F19" cross-reference (calibrator: wrong item); INV-012 note that `test_fr010_full_page_uncaptured_continuation` passes `truncated=True` directly (`test_classify.py:947`).
- **Risk**: Low.

### Change 10: Add the FIN-F7 limitation and the environmental test failures (from Variant 2) - F-15, F-17
- **Source**: V2 R2-F2 (Authorized), R2-F3 (Necessary).
- **Target**: Base, two new findings.
- **Rationale**: Scoring Matrix C-010 85% (`FINAL-GATE-FIN-F7-ruling.md:17`), C-011 85% (missing `ruff` in `.venv`, a timing test under load; passes alone, re-confirmed by the orchestrator).
- **Integration point**: R2-F2 note "the owner's words are the executor's own recommended reply pasted back"; R2-F3 note "qualified completion, not a pass of the full suite".
- **Risk**: Low.

### Change 11: Keep V3's own Authorized findings unchanged - F-14, F-16
- **Source**: V3 R3-F9, R3-F10 (base).
- **Target**: Base R3-F9, R3-F10 (retain).
- **Rationale**: C-014 85% (DESIGN :1052), C-013 80% (copies DESIGN :717 and :680 verbatim; the T1 lead's Necessary label is not adopted).
- **Integration point**: none beyond renumbering. **Risk**: Low.

### Change 12: Keep V3's R3-F6 and R3-F7 unchanged - F-08, F-09
- **Source**: V3 R3-F6, R3-F7 (base). Scoring Matrix C-016, C-017 78%. Weak cite `commands.py:219-221` replaced by the `_PublishError` second-line cite (`commands.py:137-143`). **Risk**: Low.

### Change 13: Carry the objective-level qualification and shared-assumption rulings in the verdict summary
- **Source**: V2 objective_checks and Round 2 concession; A-001, A-002, A-004 rulings.
- **Target**: Base, verdict header (new `notes`).
- **Rationale**: V2 conceded objective 3 is a qualified pass, objective 6 is not fully satisfied (literal all-green unmet, publication coverage incomplete), objective 7 is pending (an audit cannot classify its own unfinished gate). A-001 QUALIFY 85%, A-002 QUALIFY 82%, A-004 ACCEPT 85%.
- **Integration point**: a three-line objective summary and one line per assumption ruling. **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base / Base Approach | Rationale for Keeping the Decided Outcome |
|---|---|---|
| C-012 / X-005 | V2 R2-F4 `regression`, `blocking` | Calibrated Drift medium; V2 conceded in Round 2; no behaviour failure shown (88%) |
| C-002 / X-002 | V2 R2-F5 `regression`, `blocking` | Calibrated Drift low; DESIGN :62 also says tail-only, so no output difference; V2 conceded (85%) |
| C-001 / X-001 | V2 R2-F6 `regression`, `blocking` | Its own `authorization_source` is the owner approval (`FINAL-GATE-halt-resolution-decision.md:18`); calibrated Authorized medium; V2 conceded (88%) |
| C-002 | V3 R3-F4 `regression` | V3 withdrew in Round 2; practical risk stated as low; same result as tail-only |
| C-003 | V1/calibrator `drift` medium as the class | Not adopted as the class (2 of 3 majority, 62%); carried as a dissent note on F-01 |
| C-018 | V1 R1-F8 `necessary` / `total_is_lower_bound` always True | Aligned: DESIGN :346 with :517 (remote hosts never scanned) asks for it; V1 conceded; no finding (85%) |
| DC-12 | separate finding for the `_git` wording | Folded into F-06 (C-005); one diff point, one finding |
| C-008 | V1 R1-F7 `authorized` for the whole field set | Calibrated overstated: FINAL-GATE :19 only approves reserved marking; only `mtime` and `agent_wait_since` are Necessary |
| C-006, C-007, C-015 | V1 Round 1 Drift medium | Hardening follow-ups already filed; V3 lowered; severity minor (66%, 66%, 62%); V1 view carried as a note |
| C-013 | T1 lead DC-5 `necessary_deviation` | Both texts copy DESIGN :717 and :680 verbatim; Authorized minor (80%) |
| V2 objectives | objective 3 `fail`, objective 6 `fail`, objective 7 `fail` | Conceded in Round 2; replaced by qualified pass, not fully satisfied, pending (Change 13) |
| INV-013 | Rule 5 inert x output-style exception x exempt reply interaction | Not probed (UNVERIFIED); no evidence to classify; left out of the findings |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | Contested class stands without the dissent being seen | Remove the Regression label, use Drift medium (the calibrators' class) |
| 2 | Low | Over-label stays | Restore V3 label (not recommended) |
| 3 | Low | Hardening gaps rated too low | Restore medium for F-10, F-11, F-12 |
| 4 | Low | Constants mislabelled | Re-split the note |
| 5 | Low | Rule 5 gap reads as unauthorized | Cite the decision file in `authorization_source` |
| 6 | Medium | Real Orca emits id-less rows: the guard fails open | Escalate F-04 to a wrong-class bug, per the stated condition |
| 7-10 | Low | Additive findings; a wrong class is a one-field edit | Delete the finding |
| 11-12 | Low | None (unchanged) | n/a |
| 13 | Low | Summary text only | Delete the notes |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-12
