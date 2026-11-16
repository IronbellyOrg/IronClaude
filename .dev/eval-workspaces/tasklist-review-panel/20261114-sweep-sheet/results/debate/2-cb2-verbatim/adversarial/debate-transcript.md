# Adversarial Debate Transcript: CB-2 reword (DESIGN.md DD-7 / 15.1 row 3)

The full round texts are in `debate/` (kept unchanged). This file assembles them: who said what, what moved, and the scored outcome. Where a statement below was later found wrong, `work/corrections.md` says so.

## Metadata
- Depth: standard (Round 1, Round 2, Round 2.5; no Round 3 at this depth)
- Rounds completed: 1, 2, 2.5
- Advocates (3, the maximum): V1 Haiku defender, V2 Sonnet prosecutor, V3 Sonnet architect. Fault-finder for Round 2.5: one Sonnet agent (not an advocate). No Opus anywhere.
- Orchestrator: the main Sonnet session (no `debate-orchestrator` or `merge-executor` agent, so no Opus)
- Convergence threshold: 0.80 (default). Convergence achieved: 18 of 18 diff points (1.00); see the assessment below for why this number is treated with care.
- Focus areas: all
- Files: variants `variant-1-haiku-defender.md`, `variant-2-sonnet-prosecutor.md`, `variant-3-sonnet-architect.md`; `diff-analysis.md`; `debate/round1-V*.md`, `debate/round2-V*.md`, `debate/orchestrator-note-round2.md`, `debate/invariant-probe.md`; `work/evidence-pack.md`, `work/corrections.md`.

## Step 0: position papers (the variants)
| Advocate | Position on "is the default blocking" | Replacement or addition proposed |
|---|---|---|
| V1 Haiku defender | NO | none; keep verbatim and the heading count |
| V2 Sonnet prosecutor | YES (BD-1: the count has no rule or action; the decision is due before the data), "NO if proof of a biased result is required" | CB-2 text unchanged; add a 5 Z0 + 5 K pilot on HO-6 and a report rule; contingent reword moving the PROBLEM-row duty to an SS-only part |
| V3 Sonnet architect | NO (option d recommended; (c) per-arm variant and (b) one reworded text cost more) | keep verbatim; add a count rule with an exact upper bound, "never harmless", and a Stage 1 limit |

## Round 1: statements (parallel)
- **V1** kept NO. Steelmanned V2 (a post-run count cannot inform a pre-freeze decision) and V3. Conceded: shared text is not shared runs; wider reporting and a "not evidence of harmlessness" caveat are improvements, not prerequisites; the "small harm" estimate is UNVERIFIED. Rejected CORR-4 as written (the spike is planned, not run; reuse of first-block Z0 runs is allowed) which proved right and stronger than V1 knew (the spike is after the freeze).
- **V2 flipped to NO.** Conceded its own evidence 4 (no `config/freeze.json`, so no re-run cost before the freeze), that BD-1 weakens because the owner decides before the freeze, and that the debate-1 analogy fails for blocking because no gate reads the count (CORR-3). Kept: the rule is a real wording gap; the count sees one spelling.
- **V3** kept NO with option (d). Retracted "favours SS" (C-007). Corrected the spike: it comes after the freeze, about 15 reports, shows only gross rates (chance of seeing one heading in 15 reports: 0.26 at 2%, 0.54 at 5%, 0.79 at 10%).
- Corrections CORR-1 to CORR-3 CONFIRMED by all three; CORR-4 rejected or partly confirmed and then revised (corrections item 4).

## Round 2: rebuttals (sequential V1, V2, V3), routes R-A to R-I
The orchestrator note (`debate/orchestrator-note-round2.md`) set six routes nobody had examined; V2 added R-G to R-I.

| Route | V1 | V2 | V3 | Orchestrator reading |
|---|---|---|---|---|
| R-A time baseline (a phantom ledger lengthens Z0, loosens D1's 1.35 x Z0 cap) | non-blocking note | non-blocking note (D1 uses the same-day Z0 as run, MR 492) | not ruled in round 2; probe INV-011 raises the spike's item share `c` | non-blocking note; the count cannot see delay without a heading |
| R-B K checklist plus the clause | non-blocking note | not a defect (`k-lead.txt` has no verdict wording) | not a defect (no evidence either way; `k_paragraph` also appends eight card definitions) | not a defect on the evidence; direction unknowable |
| R-C forward reference (CB-2 before the ledger rule) | not a defect | not a defect (V2 corrected V1's reason: Z0 and K get no ledger rule at all) | agrees with V2 | not a defect |
| R-D the printed line could be read as "harmless" | non-blocking note | non-blocking note | closed by the recommended wording (a) | non-blocking note: `render_report` prints only "n of N" and makes no claim |
| R-E post-hoc owner discretion ("owner decision if above 0") | non-blocking note, "strongest remaining counter-argument" | non-blocking note, "closest to blocking"; stopped by committed gates, per-run brief hashes, and no registered quantity needing a reading | non-blocking note; V3 judged V2's reasons (1) and (2) thin: `prereg()` commits gates, not an action rule for the count | non-blocking note (see VERDICT.md, route R-E) |
| R-F what a PASS leaves behind | not a defect | not a defect | not a defect | not a defect |
| R-G CB-3 and CB-5 also refer to parts Z0 lacks | n/a | non-blocking note | non-blocking note; CB-5 is dangling in Z0 only (corrections item 7) | non-blocking note; supports verbatim, a CB-2-only reword would not make Z0 clean |
| R-H clause-free Z0 never run | n/a | non-blocking note | not a defect: premise fails (corrections item 8) | not a defect |
| R-I clause-caused format failure scored zero in Z0 (DD-8), skipped by the count | n/a | non-blocking note | non-blocking note | non-blocking note, size UNVERIFIED |

Final answers at the end of Round 2: V1 NO, V2 NO, V3 NO. V3's shared-blind-spot check listed three ways the NO could be wrong (NO rests on absence of evidence; "measured" overclaims for a one-spelling count; K's "no ledger" as a broken requirement) and settled each from the files (not settled / wording gap / no conflict).

## Round 2.5: invariant probe (`debate/invariant-probe.md`)
12 findings: 4 ADDRESSED (INV-004, 005, 007, 010), 8 UNADDRESSED. HIGH UNADDRESSED: none. Two findings changed the record: INV-001 (Stage 2 Z0 reports are 177, not 531; corrections item 1) and INV-002 (a re-freeze after 14.6 is not edits only; corrections item 5). INV-012 (sufficiency): the sentence "verbatim plus the heading count makes the experiment fair, measurable and not misleading" holds for "no stated requirement or gate breaks" and cannot be proved for "fair"; the fair wording is "not shown to be unfair".

## Scoring matrix (per diff point; the winner is the variant whose position is superior by majority of the three Round 1 tables, confidence is the mean of the three)
| Diff point | Winner | Confidence | Evidence summary |
|---|---|---|---|
| S-001 | V3 | 80% | options table; no bearing on the verdict (V2) |
| C-001 | default (NO), V1 and V3 | 75% | REQ-05 and REQ-23 kept, no gate reads the count; V2 later agreed |
| C-002 | V3 | 65% | a reading rule is useful (option d) but its absence is not blocking (V2, V3); V1 held that diagnostics need not control decisions |
| C-003 | all agree | 91% | no change to `briefs/cb2.txt` |
| C-004 | V3 | 68% | cheaper than a new pilot, but the spike is after the freeze (corrections item 4) |
| C-005 | V3 | 78% | wider match plus an exact bound; applied by hand, analysis code is out of scope |
| C-006 | none | 81% | all size figures UNVERIFIED |
| C-007 | V1 | 73% | direction unknown |
| C-008 | V3 | 70% | most complete cost table (V1 preferred V2's) |
| C-009 | V3 | 82% | "none seen in N reports (upper bound x%)", never "harmless" |
| X-001 | V1, V3 (V2's claim is false) | 90% | `config/freeze.json` does not exist |
| X-002 | V3 | 88% | text shared, runs separate (RL DR-12) |
| X-003 | V1 | 83% | K is Z0 plus a paragraph; "no ledger" describes machinery |
| A-001 | QUALIFY | 83% | accept only as UNVERIFIED |
| A-002 | ACCEPT | 87% | no gate reads the count (V1 qualified: report-only must not imply harmlessness) |
| A-003 | REJECT | 73% | no registered quantity gates a claim here (V3 qualified) |
| A-004 | ACCEPT | 90% | other forms of harm are seen by no option |
| A-005 | ACCEPT | 92% | only CB-2 says every PROBLEM row gets a findings line |

## Convergence assessment
- Points resolved: 18 of 18 (every point reached at least two of three advocates, counting "all agree" and "none" as agreement). Alignment: 100%. Threshold: 80%. Taxonomy: L1 (S-001, C-009), L2 and L3 all covered; no forced round. Invariant gate: no HIGH UNADDRESSED item, so the gate does not block.
- Status: CONVERGED, with two cautions. (1) A perfect score is weak evidence: V2 changed sides after two corrections, and the three advocates share one blind spot they could not test, namely that no real-model run of Z0 or K with the clause exists (A-001). (2) The agreement is on the verdict; the advocates did not agree on whether the recommended hardening text is needed (V1: improvement, not prerequisite; V3: recommended; V2: smallest edit if the owner wants it closed).
- Unresolved points: none by the rule above. Open and unmeasured: the size and direction of the clause's effect on found fraction, time and format failures.
