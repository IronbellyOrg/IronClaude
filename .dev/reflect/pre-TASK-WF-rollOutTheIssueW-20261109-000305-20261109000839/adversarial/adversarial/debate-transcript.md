# Adversarial Debate Transcript

## Metadata
- Depth: standard (2 rounds; Round 3 not applicable)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant A = reviewer-1 card, sonnet advocate; Variant B = reviewer-2 card, sonnet advocate)
- Round 1 files: round-1-advocate-A.md, round-1-advocate-B.md
- Round 2 files: round-2-rebuttal-A.md, round-2-rebuttal-B.md
- Invariant probe: invariant-probe.md

## Round 1: Advocate Statements

Full statements: round-1-advocate-A.md, round-1-advocate-B.md (summarized here).

### Variant A Advocate (sonnet:analyzer-advocate)
**Position**: A is the sounder card on correctness and verifiability; B has the higher-impact Task 5 findings. Best merge keeps both.

**Steelman of Variant B**: B read the consuming test code for the riskiest task (Task 5). QA-03 (`raw` vs `payload`, gh_api_user_include.json:4, test_github.py:563), QA-02 (plan:108 vs plan:110), QA-04 (test_github.py:566-567 hardcoded Date) and F2 (plan:29 vs plan:118) would all change what an implementer does.

**Key strengths claimed**:
1. F1 fails deterministically today: issue-watcher.md:163 backticks `failed`, `unknown`, `abandoned`; none is a REASON_TABLE key; plan:59 adds `once`.
2. All A anchors re-checked (setup.md:5, :202, :224, :282, :637; audit.py:57, :64, :87); self_audit records them.
3. F4 is a true stale-map defect (setup.md:5 stops at section 15; plan:92-100 never touches line 5).
4. Smaller calibration gap (0.14 vs 0.23).

**Weaknesses identified in Variant B**:
1. QA-02 bundles 3 claims under `high`; part is a source tension (source.md:22 "every" vs :24 "about 12+").
2. F2 is hardening, not a defect, by B's own wording.
3. QA-03 scope misstated: plan:110 covers stderr layouts; the real gap is the two `raw` fixtures plus `orca_launch_unknown`.
4. 0.95 vs 0.72 is the larger overreach; no self_audit.

**Concessions**:
- QA-03 and QA-04 are real and outrank F3-F5. F3 is overstated (plan:96 implies 2). F5 is minor. A misses Tasks 1, 3 and 5.

### Variant B Advocate (sonnet:qa-advocate)
**Position**: B reaches Task 5 (the only test- and fixture-editing task) and three of its four findings are verified defects; A has one plan-breaking finding (F1) and three housekeeping items.

**Steelman of Variant A**: F1 is the most mechanically provable defect in either card (plan:65 vs issue-watcher.md:163 vs plan:59). A's self_audit is real negative evidence; its calibration gap is smaller; F4 and F5 are cheap real runbook fixes.

**Key strengths claimed**:
1. QA-03 verified: a literal Task 5 leaves `raw` guessed while labelling the file `_assumed_shape: false`.
2. QA-04 verified: test_github.py:566-568 hardcodes the guessed values; plan:112 and plan:120 give Task 5 no sanctioned fix.
3. QA-02 grounded: plan:15 goal says the 19 fixtures "are replaced" while plan:117/:119 pass with some still guessed.
4. F2 is a real hole in the secret check (plan:29 vs plan:118).

**Weaknesses identified in Variant A**:
1. F1 is a one-line AC tweak on an agent-run doc check.
2. F3 is padding (plan:96 already implies 2).
3. F4, F5 are housekeeping.
4. A never touches Task 5 or Task 1.
5. A's self_audit covers only its own chosen surface.

**Concessions**:
- QA-02 should be medium and bundles 3 claims; source.md:7 has no "every"; plan:78 tolerance for unprovokable errors is partly defensible.
- B has no self_audit and mixed IDs; B confirms one T1 finding to A's two; did not re-verify coverage-matrix.md:14.

### Round 1 per-point positions

| Point | A advocate | B advocate | Agree? |
|---|---|---|---|
| S-001 | A | A | yes |
| S-002 | TIE | A | no |
| S-003 | B | B | yes |
| C-001 | TIE | B | no |
| C-002 | A | TIE | no |
| C-003 | TIE | B | no |
| C-004 | A | A | yes |
| A-001 | TIE (QUALIFY) | TIE (QUALIFY) | yes |
| A-002 | TIE (QUALIFY) | TIE (QUALIFY) | yes |
| A-003 | TIE (ACCEPT) | TIE (ACCEPT) | yes |
| A-004 | TIE (QUALIFY) | TIE (QUALIFY) | yes |

Round 1 agreement: 7 of 11.

## Round 2: Rebuttals

Full sequential rebuttals: round-2-rebuttal-A.md, then round-2-rebuttal-B.md.

A concedes B's Task 5 coverage advantage and retracts its source-ambiguity argument: an effort estimate does not weaken the every-fixture requirement. A withdraws F3 as a defect and F5 as more than navigation advice. B retracts its claim that A never reviewed Task 1 and its claim that Task 5 forbids expected-value edits. Both preserve F1 as an acceptance blocker, F4 as a low-severity map omission, F2 as a verification gap rather than an established leak, QA-02 as medium, QA-03 narrowly on the consumed raw field, and QA-04 on capture-dependent expected values. Neither claims any proposed repair alone makes the test suite pass.

| Point | A final | B final | Agreement |
|---|---|---|---|
| S-001 | A | A | yes |
| S-002 | A | A | yes |
| S-003 | B | B | yes |
| C-001 | B | B | yes |
| C-002 | A | A | yes |
| C-003 | B | B | yes |
| C-004 | A | A | yes |
| A-001 | TIE (plan gaps, not source defects) | TIE | yes |
| A-002 | TIE (snapshot citations) | TIE | yes |
| A-003 | TIE (owner boundary preserved) | TIE | yes |
| A-004 | TIE (Task 3 unreviewed) | TIE | yes |

Raw Round 2 agreement: 11/11. Invariant probe remains a separate convergence gate.

## Round 2.5: Invariant Probe

Independent probe: invariant-probe.md. Eleven rows across all six categories: nine ADDRESSED, two UNADDRESSED. No HIGH-severity UNADDRESSED row remains, so convergence is not blocked. The MEDIUM residuals are Task 3's unreviewed builder/preservation coverage (INV-009) and a conditional CRLF capture/test-adapter interaction (INV-011). Both must remain visible in the merge as limitations, not be converted into an observed parser defect. The probe explicitly enumerates downstream gates and rejects any claim that raw/expected-value repairs alone guarantee passing tests.

## Round 3: Final Arguments (if applicable)

Not applicable: depth is standard.

## Scoring Matrix

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| S-001 | A | .95 | A's checked-negative self_audit, both Round 2 tables |
| S-002 | A | .90 | Consistent F IDs; presentation advantage only |
| S-003 | B | .85 | Raw/Date consumer consequences, QA-02 downgraded |
| C-001 | B | .90 | Task 5 review; A did check Task 1 uniqueness |
| C-002 | A | .90 | F1 impossible literal acceptance; F3 withdrawn |
| C-003 | B | .90 | Raw destination and hardcoded assertion path |
| C-004 | A | .95 | Calibrated gaps .14 versus .23 |
| A-001 | TIE | .90 | Effort estimate does not weaken source obligation |
| A-002 | TIE | .90 | Snapshot citations; section-name preservation rule |
| A-003 | TIE | .95 | Owner-only execution and false configuration retained |
| A-004 | TIE | .85 | Task 3 common blind spot, INV-009 |

Confidence here rates the comparison, not implementation readiness. Finding confidence remains constrained by the .74/.72 independent calibrations.

## Convergence Assessment

Round 1: 7/11 = .6364. Round 2: 11/11 = 1.0000, exceeding .80. Both final tables agree on every defined point; A wins four, B three, four are ties. Invariant gate: zero HIGH UNADDRESSED; two MEDIUM residuals retained as warnings. There are zero unresolved winner disagreements. No Round 3 at standard depth. Agreement establishes a shared review disposition, not that the plan has been repaired, fully reviewed, implemented or tested.
