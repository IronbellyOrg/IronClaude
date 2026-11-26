# Merge Execution Log

## Metadata
- Base: Variant 2 (sonnet:analyzer), chosen by the tiebreaker (score margin 0.0482 < 0.05; V2 won or shared 35 of 41 diff points, V1 19, V3 5)
- Executor: merge-executor agent in three sequential parts (A `a60ee21c34af9f337`: header, sections 1-2, 3 opening, 3.0; B `a6f5f070702866664`: 3.1 and 3.2; C `a429dc41dcdb25351`: sections 4-6, closing note, provenance summary, effort correction in 3.1(h) and 3.2(h)); fixes of cycle 1 applied by the orchestrator with the Edit tool
- Changes applied: 16 of 16 planned (changes 1-16 of `refactor-plan.md`), plus one fix cycle that closed 7 blocking review findings
- Status: success
- Output: `../merged-spec.md` (1,248 lines, six numbered sections plus "Not checked and unverified" and "Provenance summary"; 49 provenance comments)
- Timestamp: 2026-11-14T00:17:00Z

## Changes Applied

| # | Change | Status | Where in `merged-spec.md` | Provenance tag | Validation |
|---|--------|--------|---------------------------|----------------|------------|
| 1 | Frame and conventions (labels HO-1..HO-6, SS/RL/Z0/K, no GT labels) | Applied (part A) | top, lines 1-22 | Base (original, modified) V2 header + V1 conventions | Structural ✅ References ✅ Contradictions ✅ |
| 2 | Section 1 Theories (V2 base, V1 numbers, rejected rival, theory map) | Applied (A) | `## 1.` | Base + Variant 1 section 1 | ✅ ✅ ✅ |
| 3 | Section 2 Defect classes and generality (HO label key, X1-X7, limits) | Applied (A) | `## 2.` | Base + Variant 1 section 2 | ✅ ✅ ✅ |
| 4 | Section 3.0 shared scaffolding (H1-H4 with +0.14, CB-1..5, cards, `ledger-v1`, checks and promotion, telemetry, fallback and guard rows, reach stages, optional verifier, no messaging) | Applied (A) | `### 3.0`, 3.0.1-3.0.10 | V1 3.0, V2 shared changes, V3 3.3, INV-001..014 | ✅ ✅ ✅ (one defect fixed in cycle 1: 3.0.7 flags) |
| 5 | 3.1(a) Redesign 1 mechanism, extractors E1-E7, templates, sheet wording | Applied (B) | `### 3.1 (a)` | V2 Redesign 1, V1 3.1(a), V3 determinism | ✅ ✅ ✅ (cap fix in cycle 1) |
| 6 | 3.1(b)-(i) roles, time, matrix, breadth, gain, overhead, effort, failure modes | Applied (B), effort corrected (C) | `### 3.1 (b)-(i)` | Appendix A2, A4-A8; V1/V2 failure rows | ✅ ✅ ✅ |
| 7 | 3.2 Redesign 2 (a)-(i), lens table, recipes, ledger rule | Applied (B) | `### 3.2` | V2 Redesign 2, V1 recipes and search forms | ✅ ✅ ✅ (duplicate-class wording fixed in cycle 1) |
| 8 | Section 3 opening: distinctness, three-row table, what is NOT a redesign | Applied (A) | `## 3.` first paragraphs | V2 section 3 intro + debate Q1, Q5 | ✅ ✅ ✅ |
| 9 | Section 4 comparison table and 4.1 answers to the five open questions | Applied (C) | `## 4.` | V1/V2 section 4, Appendix A | ✅ ✅ ✅ (token percent fixed in cycle 1) |
| 10 | Section 5 validation experiment (arms, 326 runs, gates G0, D1-D7) | Applied (C) | `## 5.` | V2 section 5 + V1 gates + V3 bootstrap | ✅ ✅ ✅ (D5 and power note fixed in cycle 1) |
| 11 | Section 6 requirements REQ-01..REQ-46 with tests | Applied (C) | `## 6.` | V1/V2/V3 + INV resolutions | ✅ ✅ ✅ (REQ-12, 25, 45 fixed in cycle 1) |
| 12 | Closing note and provenance summary | Applied (C) | last two `##` sections | V1/V2/V3 closings | ✅ ✅ ✅ |
| 13 | Failure-mode union with probability and recovery columns | Applied (B) | 3.1(i), 3.2(i) | V1/V2/V3 (i) rows | ✅ ✅ ✅ |
| 14 | Anti-overfitting rules AO-1..AO-8 | Applied (A) | 3.0.3, referenced in (e) | V1 AO1-AO8, V2 AO-1..AO-8, V3 | ✅ ✅ ✅ |
| 15 | Guard rows (gateway, judge, missing source, empty sheet, one class, two reviewers) | Applied (A) | 3.0.7 | INV-008, 012, 013 | ✅ ✅ ✅ |
| 16 | Provenance annotations | Applied (A, B, C) | 49 `<!-- Source: ... -->` comments | skill provenance rules | ✅ |

Executor-reported deviations from the plan (all small, none a strategic change): arm names taken from the brief (`RS` not used); the linking of a ledger row to a findings line was specified through the `probe` key or the quote lying inside the anchor (3.0.5); the ledger-check failure after the run was added to 3.0.7; eight question templates written (C3 from V1); ember item cap set to 8 so the caps sum to 24 (A4 said about 9); A5 per-row sums differ from the Appendix totals by rounding (0.93-2.75 vs 0.92-2.73; 0.64-2.48 vs 0.63-2.47) and a note was added; the plan's A8 effort subtotal was mis-added (450-600 + 90 + 250-400 = 790-1,090) and was corrected in the document; the A2 cell for b = 122 was written in full; V2's claim that Redesign 2 has more slack was corrected (expected b + 28 against b + 29; worst case b + 34).

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ✅ `#` title, `## 1.`-`## 6.` plus two unnumbered `##` closing sections, `###`/`####` below; no level gaps found by the reviewers
- Section ordering: ✅ theories, classes, redesigns (3.0 shared first), comparison, validation, requirements, closing note
- Document flow: ✅ exactly two redesigns; the verifier, a second ember session, a rubric edit and the 60-item list are named as not redesigns (section 3 opening and 3.0.9)
- Mechanical checks by the orchestrator: 0 em or en dashes; 0 uses of "Redesign A/B", GT labels or H1-H6 hold-out labels; 46 distinct REQ ids; ground-truth lint (`scoring/lint-groundtruth-output.txt`): 1 shingle hit in 1,230, "with the plan s", a tokenization artifact of "with the plan's" (accepted)

### Internal References
- REQ references: every REQ id cited exists (REQ-01..REQ-46 defined in section 6); INV-001..INV-014 each resolved in the text (map in `merge-review.md` and `merge-review-2.md`)
- Open reference issue recorded as follow-up (M-10): "A4"/"A7" and the step label "S1" are ambiguous

### Contradiction Re-Scan
- Review 1 (`merge-review.md`): FAIL, 7 blocking, 11 medium, 13 minor. Blocking: B-1 ember cap and fallback; B-2 token percent; B-3 gate D5 spec clause; B-4 power note item count; B-5 REQ-45 wording; B-6 duplicated classes per panel; B-7 REQ-12 versus 3.0.7
- Fix cycle 1 (orchestrator, Edit tool): B-1 (3.1(b) row, S4 step tables, fallback sentence with ember raised to 12 in the fallback only), B-2 (+23% to +40% in 3.2(g) and section 4), B-3 (D5 spec clause removed; spec generality rests on HO-5 and REQ-37 fixtures), B-4 (36-40 items), B-5 (REQ-45), B-6 (R1 sentence, lens caption, failure row, REQ-25), B-7 (REQ-12 split into fallback=true and check_skipped=true; 3.0.7, S5 and R3 aligned)
- Review 2 (`merge-review-2.md`): PASS, 0 blocking, 3 medium, 5 minor; every recomputed number matched
- New contradictions introduced by the merge: 0 open blocking

## Follow-up candidates (Medium; recorded only, not fixed, per the review rules)

From review 1: M-1 D2 threshold (+0.12 absolute) sits above the central planned gain (+0.095 and +0.075); M-2 Stage 2 entry rule and "passes" undefined; M-3 ember re-ask has no working mechanism because the launcher uses `--no-session-persistence`; M-4 promotion leaves `category` and `id` scheme unspecified; M-5 ledger wording does not tell models to JSON-escape quotes; M-6 recipe R-C2 asks for more row-steps than its 6-row budget; M-7 pre-pass search scope differs between S1, E3 and E4; M-8 two word-level hints ("found" in set-word lists; "changelogs" in recipes) that a 4-word lint cannot catch; M-9 REQ-40 names a prompting share that the reports do not give; M-10 label clashes (S1 step versus item id) and references to appendix numbers ("A4", "A7") of the plan; M-11 "retried reviewer scored as zero" conflicts with the launcher's retry loop, which exists to recover a missing block.
From review 2: M-12 the fallback cap raise (ember 12) is stated only in 3.1(c), not in S3, REQ-20 or REQ-32, and the fallback routing is unstated; M-13 the "consistent" threshold reads unevenly (Redesign 2 I4 up to 0.63 not expected, Redesign 1 I7 up to 0.62 expected); M-14 spec generality for Redesign 2 rests on HO-5 alone after the D5 fix.

## Summary
- Total changes planned: 16
- Successfully applied: 16
- Failed: 0
- Skipped: 0
- Blocking review findings: 7 found, 7 fixed in one cycle (review 1 FAIL, review 2 PASS; cap of 2 fix cycles not reached)
- Post-merge validation: PASS
