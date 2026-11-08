# Refactoring Plan

## Overview
- Base variant: variant-3 (reviewer-3-card.yaml, opus:refactorer). Combined score 0.890 (base-selection.md).
- Incorporating from: variant-1 (reviewer-1-card.yaml, sonnet:analyzer) and variant-2 (reviewer-2-card.md, haiku:qa). Invariant probe items INV-001..INV-013 are fix-scope evidence.
- Total planned changes: 16
- Overall risk: Medium. Two blocking findings carry fix scope that the invariant probe widened (INV-001, INV-004, INV-005), and those three stay unresolved.
- Output target: merged-verdict.yaml in the exact schema of the run brief. It is not a markdown card.

## Ground rules for the merge-executor
- Re-Read every cited line (TF = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`, D = `docs/designs/issue-watcher.md`, R06 = the research/06-gap-fill-decisions.md under the task folder, plus `Makefile` and `.github/workflows/test.yml`). Drop or correct any citation whose text does not exist at that line. If the text has moved, cite the current line.
- Severity is binary: blocking or minor, as the run brief defines it. A deviation that R06 or TF's Open Questions declare is not a defect.
- Findings are ordered most severe first: blocking, then minor.
- Provenance goes in YAML comments.

## Planned Changes

### Change #1: M-001 X-001 remediation after the single commit (blocking, sequencing)
- **Source**: variant-3 R3-001 (base), variant-1 R1-002 (co-source); INV-001, INV-002, INV-003
- **Target**: findings[0]
- **Rationale**: Unanimous VALID-BLOCKING (X-001, 95%). Step 10.6 tells the runner to apply remediations after the single commit, while the POST audit covers only BASE..HEAD and staging excludes source (TF:864, 866, 875; R06:30 DF-07).
- **Integration**: fix = make the Step 10.6 POST reflect report-only. Any Regression or unauthorized Drift HALTs the task and is reported to the owner, with no source edit and no second commit. Per INV-001 and INV-002, a re-gate alone is insufficient and self-approval by a bypass-mode runner is unsafe. Note INV-003: any re-gate must use the PASS-baseline verdict of M-002.
- **Risk**: Medium (the fix choice is unresolved: INV-001)

### Change #2: M-002 X-008 lint/test exit-0 against recorded-not-fixed (blocking, contradiction)
- **Source**: variant-3 R3-002 (base); INV-004, INV-005, INV-006, INV-007
- **Target**: findings[1]
- **Rationale**: Unanimous VALID-BLOCKING (X-008, 95%; A-004 rejected 3/3). TF:699 and 702 say "ensuring exit 0" while pre-existing findings are recorded and not fixed, and TF:735 and 745 require every row PASS.
- **Integration**: fix = (a) add a P1 baseline step that records `make lint`, pinned ruff format and the G-2 test subset; (b) define one PASS-baseline verdict (no new finding against baseline) and reference it at every site: G-2 TF:693 (INV-005), G-4/G-5 TF:699/702, TF:735, TF:745, per-phase G-4 TF:259/390/517, Gate A-D re-runs TF:306/321/433/448/560/575/657/672, Final/M4 re-runs TF:778/793/821/836, Gate C lens TF:530 (INV-004); (c) add the carve-out to the 3.G2, 9.F2, 9.F11 and 9.F16 prompts; (d) record the lint-architecture prerequisite separately so ruff always runs (INV-006); (e) pin the ruff version used for the baseline (INV-007). Re-Read every one of these lines first and keep only those that hold the pattern.
- **Risk**: Medium (the site list is unresolved: INV-004, INV-005)

### Change #3: X-006 cycle stderr fallback untested (minor, coverage_gap)
- **Source**: variant-2 R2-002
- **Target**: findings, minor
- **Rationale**: Unanimous VALID-MINOR. TF:460 names the fallback and the TF:472 test list omits it (D:887, D:722).
- **Integration**: fix = add a stderr-fallback test case to the Step 6.x test item at TF:472. Mention INV-008 (MEDIUM) in a comment.
- **Risk**: Low

### Change #4: X-007 revalidation/revocation cases untested (minor, coverage_gap)
- **Source**: variant-2 R2-001
- **Target**: findings, minor
- **Rationale**: Unanimous VALID-MINOR. TF:460 lists the cases and the TF:475 list omits them (D:879).
- **Integration**: fix = add the cases to the Step 6.7 test list at TF:475. Mention INV-008 and INV-009 in comments.
- **Risk**: Low

### Change #5: X-002 T-2 attempts<3 conjunct dropped in Step 4.1c wording (minor, coverage_gap)
- **Source**: variant-1 R1-001
- **Rationale**: Unanimous VALID-MINOR. T-2 is covered.
- **Integration**: fix = restore the "attempts < 3" conjunct in the TF:336 wording (D:479).
- **Risk**: Low

### Change #6: C-001 withdrawn-commit branch has no audit argument (minor, contradiction)
- **Source**: variant-1 R1-003; INV-010 (MEDIUM warning)
- **Integration**: fix = give the Step 10.6 prompt (TF:860) explicit substitution text for the withdrawn branch (TF:848), and forbid an empty HEAD..HEAD audit.
- **Risk**: Low

### Change #7: C-002 xdist citation names a different supply mechanism (minor, wrong_citation)
- **Source**: variant-1 R1-004
- **Integration**: fix = correct the TF:611 rationale to match test.yml:29.
- **Risk**: Low

### Change #8: C-003 G-10 does not check pyproject.toml/Makefile (minor, gate_weakness)
- **Source**: variant-1 R1-005. Backstopped per INV-014 (ADDRESSED).
- **Integration**: fix = add the two paths to G-10 at TF:723.
- **Risk**: Low

### Change #9: C-004 uncapped per-phase re-run loops (minor, gate_weakness)
- **Source**: variant-3 R3-003; INV-013
- **Integration**: fix = cap the TF:690 loop to match the Final HALT rule (TF:778). Note that it stays minor only if M-002 lands.
- **Risk**: Low

### Change #10: C-005 stale outputs after fix cycles (minor, sequencing)
- **Source**: variant-3 R3-004, broadened by INV-012
- **Integration**: fix = regenerate final-change-set.md (TF:742), final-gate-record.md (TF:735) and ac-trace.md (TF:729) after each post-fix re-run, before M4 (TF:800).
- **Risk**: Low

### Change #11: C-006 record -> predicates import departs from D:239 "types only" (minor, contradiction)
- **Source**: variant-3 R3-005; INV-011. Majority 67%, with v2 dissenting (BLOCKING).
- **Integration**: fix = declare the departure in TF Open Questions and add it to the TF:751 lens and the TF:800 M4 exemption lists.
- **Risk**: Low

### Change #12: C-008 format hit in main.py (minor, contradiction)
- **Source**: variant-3 R3-007
- **Integration**: fix = make TF:502 and TF:520 agree on how a pre-existing format hit is handled (PASS-baseline verdict).
- **Risk**: Low

### Change #13: C-009 Done kept after a staging failure (minor, gate_weakness)
- **Source**: variant-3 R3-008. Majority 67%, with v2 dissenting (BLOCKING). INV-015 ADDRESSED.
- **Integration**: fix = state at TF:875 that a staging failure is logged as a follow-up for the owner.
- **Risk**: Low

### Change #14: coverage_resolution (UNION of S-002)
- **Source**: v1 T rows, v2 AC rows, v3 INF register
- **Integration**: covered: T-2, INF-016. partially_covered: INF-123 (DF-05, declared), INF-155 (DF-05, declared), INF-146, AC-14, AC-6, INF-138 (INV-009).
- **Risk**: Low

### Change #15: dropped_findings
- **Integration**: R3-006, reason "declared deviation DF-46 (R06:180); conceded 3/3 in debate (C-007)". Add any finding whose cited text fails the re-Read.
- **Risk**: Low

### Change #16: header and unresolved
- **Integration**: merge_method adversarial, convergence_score 1.00, reviewers 3, unresolved [INV-001, INV-004, INV-005]. Add a YAML comment recording status BLOCKED_BY_INVARIANTS.
- **Risk**: Low

## Changes NOT Being Made
| Diff Point | Non-Base Approach | Rationale |
|------------|-------------------|-----------|
| C-007 | R3-006 (base's own finding) | Declared deviation DF-46 (R06:180). Dropped 3/3. |
| S-001 | v2 markdown card format | Unanimous YAML, so the output follows the brief's schema |
| S-003 | v2 MEDIUM/HIGH severity labels | Severity is binary per the brief |
| S-004 | v2 "Drift" category label | Mapped to coverage_gap. The deviation taxonomy stays separate |
| C-006, C-009 | v2 BLOCKING severity | Outvoted 2/3. Recorded in debate_outcome |
| X-003, X-004 | Finding status for INF-123/INF-155 | Declared DF-05. Coverage only, not a defect |

## Risk Summary
| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1 | Medium | Fix option disputed (INV-001) | Listed in unresolved |
| #2 | Medium | Site list may be incomplete (INV-004, INV-005) | Listed in unresolved. Re-Read every site |
| #3-#13 | Low | Minor findings | Drop an item if its citation fails the re-Read |
| #14-#16 | Low | Schema fields | Re-validate the schema |

## Review Status
- Approval: auto-approved
- Approved by: auto
- Timestamp: 2026-11-07T20:06:00Z
