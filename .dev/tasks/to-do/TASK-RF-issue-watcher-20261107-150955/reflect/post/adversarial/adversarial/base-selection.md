# Base Selection Report

## Metadata

| Field | Value |
|---|---|
| Date | 2026-11-08 |
| Pipeline step | sc:adversarial Steps 3 and 4 (scoring, base selection) |
| Mode / depth / focus | Mode A / standard / correctness, coverage, deviation classification |
| Variants (input order) | V1 analyzer (sonnet), V2 qa (haiku), V3 refactorer (opus): the three reflect-reviewer deviation cards for diff `e8db2fe6..26f551f4` |
| Scoring protocol | `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (30 criteria, lines 108-154) |
| Formula | quant = RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15; final = 0.5×quant + 0.5×qual |
| Debate result | Converged, 56 / 67 = 0.836 (`scoring-matrix.md`) |
| judge_class_collision | **true**: the judge is a model of the same family as the variant authors and advocates, and one judge instance ran both qualitative passes |
| Spot checks | 9 citations per variant re-read by the judge (minimum 6) |

## Quantitative Scoring (50% weight)

RC = requirement coverage (debated plus single-source points a variant raises, out of the 69 coverage units used for every variant); IC = internal consistency; SR = structural rigor; DC = citation accuracy from the calibrator counts; SC = section completeness (H2 sections present against the five a deviation card requires). RC is rounded to two decimals before weighting.

| Variant | RC (0.30) | IC (0.25) | SR (0.15) | DC (0.15) | SC (0.15) | quant |
|---|---|---|---|---|---|---|
| V1 | 0.46 (32/69) | 0.95 | 0.92 | 0.931 (27/29) | 1.00 (5 H2) | **0.803** |
| V2 | 0.17 (12/69) | 1.00 | 0.94 | 0.955 (21/22) | 0.80 (4 H2) | **0.705** |
| V3 | 0.20 (14/69) | 0.98 | 0.98 | 0.971 (34/35) | 1.00 (5 H2) | **0.748** |

Judge spot checks (separate from DC; 9 per variant):

| Variant | Correct | Wrong |
|---|---|---|
| V1 | `cli.py:35`, `audit.py:55-57`, `record.py:421-431`, `predicates.py:205-209`, `launch.py:326-334`, `runner.py:15`, `cycle.py:685-690` (7) | `cycle.py:335-337` (real 1060-1062), `cycle.py:308` (real 693-694 and 1033-1034) (2) |
| V2 | design :647, `cycle.py:1048`, `cycle.py:1060`, task :188, `test_cli.py:1070`, `test_cycle.py:4694`, `test_cycle.py:4154`, `research/06-gap-fill-decisions.md:28`, task :332 (9) | none; outside the sample, `p9-g2-summary.md:8` is one line off (real :9) |
| V3 | design :114, setup :53, setup :432, `cycle.py:693-694`, `record.py:310-315`, `cycle.py:1271` / `:1279-1280`, `audit.py:393-402`, `record.py:421-431` (8) | `src/superclaude/main.py:563-565` (real `src/superclaude/cli/main.py:563-565`) (1) |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Each cell is claim-evidence-verdict: the verdict (MET / NOT MET) followed by the evidence the judge read in the variant card. One point per MET criterion.

### Completeness

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Covers all requirements | NOT MET: classes no item as Regression although several contradict stated criteria (X-001, X-007) | MET: every unit in its 13-unit slice is classified or listed adherent (V2:27-30) | NOT MET: V3:63 says the slice was checked "not clause by clause" |
| 2 Edge cases | MET: 13 gaps including C-016, C-018, C-022 | MET: late-launch window and skip sites | MET: gaps C-017, C-035, C-036, C-037 |
| 3 Dependencies | MET: module-boundary rows (C-005, C-006, C-010) | MET: rows 4 and 5 tie to DF-05 and the boundary test | MET: rows 8-11 and the `_ORCA_CLIS` read |
| 4 Success criteria | NOT MET: no verdict, no pass condition | MET: verdict FAIL with DONE / NEXT table (V2:8-13) | MET: adherent checks state what "matches" means (V3:34-47) |
| 5 Out of scope | MET: not-read list V1:51-57 | MET: V2:55 states no tests were run | MET: "Could not fully verify" V3:62-66 |
| **Score** | **3** | **5** | **4** |

### Correctness

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 No factual errors | NOT MET: `cycle.py:335-337` and `cycle.py:308` are wrong lines | MET: 21 / 22 exact; the one off-by-one line is a citation-format slip | NOT MET: `src/superclaude/main.py` path does not exist |
| 2 Feasible | MET: findings describe real code paths | MET: V2:53 fix is compatible with both durable-before-launch and the cutoff | MET: "do not consolidate `_fsync_dir`" respects design :237 |
| 3 Terminology consistent | NOT MET: row 6 "Drift (alternative reading: NFR-014 regression)" | NOT MET: row 2 is Drift MEDIUM labelled "Blocking"; only a Regression blocks | NOT MET: rows 8 and 10 call design-permitted structure Necessary |
| 4 No contradictions | NOT MET: header V1:7 "1 MEDIUM, 11 LOW" against two MEDIUM rows | MET: no internal contradiction found | NOT MET: row 1 Drift (`cycle_crashed`) against row 7 Necessary (`cycle_complete`) for the same kind of unlisted reason |
| 5 Claims supported | NOT MET: V1:32 "This is an estimate"; row 2 "arguably contradicted" | MET: each row has an absolute citation | MET: 34 / 35 citations match |
| **Score** | **1** | **4** | **2** |

### Structure

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Ordering | MET: rows by severity | MET: verdict first, rows by severity | MET: rows, adherent, gaps in order |
| 2 Hierarchy | MET: H2 per section | MET: H2 per section | MET: H2 per section |
| 3 Separation | MET: findings and gaps apart | MET: findings and notes apart | MET: findings, adherent and gaps apart |
| 4 Navigation aids | MET: tables with ids | MET: DONE / NEXT table, numbered rows | MET: numbered rows and runbook list |
| 5 Artifact conventions | MET: all required sections | NOT MET: no correctness-gaps table | MET: all required sections |
| **Score** | **5** | **4** | **5** |

### Clarity

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Unambiguous | NOT MET: row 6 carries two classifications | MET: one class per row | MET: one class per row |
| 2 Concrete | MET: file:line per row | MET: file:line per row | MET: file:line per row |
| 3 Section purpose | MET: headings match content | MET: headings match content | MET: headings match content |
| 4 Acronyms defined | NOT MET: DF and AC ids used without gloss | MET (disputed, see bias table): ids are glossed by quoted text at first use | NOT MET: DF, PRE-11 and R-003 never defined |
| 5 Actionable next steps | NOT MET: no recommendations | MET: V2:53 names the fix and the test | NOT MET: no actions |
| **Score** | **2** | **5** | **3** |

### Risk

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 At least 3 risks with probability and impact | MET: 12 rows with severity and the time windows at V1:49-50 | NOT MET: 5 rows, no probability stated | NOT MET: severities without probability or window |
| 2 Mitigation for each | NOT MET: no remediation column | MET: V2:53 and per-row remedies | NOT MET: no actions |
| 3 Failure modes and recovery | MET: at-most-once notes | MET: pending-state crash path | MET: C-018 lost record |
| 4 External dependencies | MET: Orca and gh notes | MET: DF-05 gh dependency | MET: `find_orca` relative PATH (`launch.py:184`), gh pinned to the fork (`github.py:37`) |
| 5 Monitoring and validation | NOT MET: no verifier named | MET: names the test to add (V2:53) | MET: parity-test gap and audit-check gap (C-037) |
| **Score** | **3** | **4** | **3** |

### Invariant and Edge Case

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| 1 Collection boundaries | MET: reason-count rows | MET: 59 versus 57 | MET: reason table rows 1 and 7 |
| 2 State across components | MET: pending / consumed notes | MET: save then launch ordering | MET: `launch_cwd` across record and cycle (C-036) |
| 3 Guard gaps | MET: X-008 leading dash | MET: missing cutoff guard after save | MET: `retry` drop guard |
| 4 Count divergence | MET: six-per-day cap note | MET: C-030 cap test | MET: 13 runbook counts |
| 5 Interaction effects | MET: disabled-mid-cycle window | MET: save crossing 120 s | MET: dangling symlink across `disabled` / `status` |
| **Score** | **5** | **5** | **5** |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3 | 5 | 4 |
| Correctness | 1 | 4 | 2 |
| Structure | 5 | 4 | 5 |
| Clarity | 2 | 5 | 3 |
| Risk | 3 | 4 | 3 |
| Invariant and Edge Case | 5 | 5 | 5 |
| **Total / 30** | **19** | **27** | **22** |
| **qual** | **0.633** | **0.900** | **0.733** |

## Position-Bias Mitigation

Pass 1 scored in input order (V1, V2, V3); pass 2 in reverse (V3, V2, V1). Each disagreement was re-evaluated against the card text.

| Variant / criterion | Pass 1 | Pass 2 | Final | Re-evaluation |
|---|---|---|---|---|
| V3 Completeness-1 | MET | NOT MET | NOT MET | V3:63 admits the slice was not checked clause by clause |
| V1 Risk-1 | NOT MET | MET | MET | 12 severity-graded rows plus time windows at V1:49-50 |
| V2 Clarity-4 | MET | NOT MET | MET | Each id is accompanied by the quoted criterion text at first use |
| V3 Risk-5 | NOT MET | MET | MET | Parity-test and audit-check gaps are validation proposals |
| V2 Correctness-2 | NOT MET | MET | MET | V2:53 text is compatible with a restore-and-skip fix |

Disagreements: 5. Final verdicts that changed from pass 1: 4.

**Disclosure (shortcut):** one judge instance ran both passes in the same context; the reverse pass was not an independent instance. This is why `judge_class_collision: true` is recorded in Metadata.

## Edge Case Floor Check

Floor: at least 1 / 5 on Invariant and Edge Case.

| Variant | Invariant score | Eligible |
|---|---|---|
| V1 | 5 / 5 | yes |
| V2 | 5 / 5 | yes |
| V3 | 5 / 5 | yes |

## Combined Scoring

| Variant | quant | qual | final = 0.5×quant + 0.5×qual | Rank |
|---|---|---|---|---|
| V2 | 0.705 | 0.900 | **0.803** (0.8025) | 1 |
| V3 | 0.748 | 0.733 | **0.741** (0.7405) | 2 |
| V1 | 0.803 | 0.633 | **0.718** | 3 |

**Margin and tiebreaker:** V2 leads V3 by 0.062, which is not under 0.05, so no tiebreaker is applied (order would have been: debate result, then correctness count, then input order).

## Selected Base

**BASE: V2 (qa, haiku).**

**Rationale:** V2 has the highest final score (0.803) and the highest correctness count (4 / 5). It is the only card that finds the one blocking Regression (late launch after the 120 s cutoff, X-007), quotes the criterion it contradicts (design :647, AC-19), gives a verdict, and names a fix and a verifier (V2:53). Its 9 / 9 spot checks were exact. Its weakness is coverage (12 of 69 units), which the merge fills from V3 and V1.

**Strengths to preserve (from V2):**

- The late-launch finding with the cutoff criterion quoted.
- The binary verdict and DONE / NEXT table (V2:8-13).
- The recommended action at V2:53: keep durable-before-launch ordering and the `budget_exhausted` outcome; add a test whose pending-state save crosses the cutoff.
- Absolute file:line citations.
- The skip-site analysis against task :188.

**Strengths to incorporate:**

- From V3: the adherent list (V3:34-47); the 13 runbook claims (V3:48-61); gaps C-017, C-035, C-036, C-037; the "do not consolidate `_fsync_dir`" advice; the parity-test gap.
- From V1: the 13 gaps, in particular C-016, C-017, C-018, C-019, C-022, C-024 and C-026; the at-most-once notes.

**Not carried over:** V2's HIGH severity and the "Blocking" label on its Drift row 2; V1's "Regression 0" and its two wrong line ranges; V3's wrong `main.py` path. See `refactor-plan.md`, "Changes NOT Being Made".
