# Base Selection: reviewer-card variants (sc:adversarial step 3, Mode A, depth standard, sc:reflect UC-1 run 4)

- Written: 2026-11-10 by the merge executor (steps 3 to 5). Status: complete.
- Inputs: `variant-1-original.md` (V1, reviewer 1, analyzer, calibrated C 0.68), `variant-2-original.md` (V2, reviewer 2, qa, calibrated C 0.86), `variant-3-original.md` (V3, reviewer 3, refactorer, calibrated C 0.86), `debate/consensus.md` (CONS), `invariant-probe.md`, the three `../reviewer-cards/reviewer-N-card-calibrated.yaml` files, and the real files the cards cite.
- Machine part: the quantitative layer, the debate-point count and the combination were computed by a throw-away script (`/tmp/adv-r4-score/score_r4.py`, run with `uv run --no-project python -I`, not kept in the repository). Its full output is `scores.json` in this folder. The qualitative verdicts are my own judgments; the script only adds them up.
- Reference only, not a variant: `../reflection-card-t1.yaml` (Tier 1 card).

## What this score does and does not mean

The three cards are not three versions of one document. Each reviewer audited a different slice of the plan: V1 the Phase 7 items around 7.10, 7.20, 7.30 and 7.34; V2 the decision consumers of the optional OQ-17/OQ-18 branch (7.17, 7.24) and the ten closures; V3 items 13.1, 11.4, 13.18/13.22, the 14.x fixers and the reflect artifacts. So the score ranks how well each card meets the reviewer contract (`../reviewer-briefs/common.md` "Return format (your final message, exact)") and how well its claims survived the debate. It does not rank which slice of the plan is more defective, and a low score does not make a card's findings less true: V1 scores lowest, yet five of the nine merged findings come from V1. The base variant only supplies the frame of the merged verdict (per-finding claim, evidence, fix, verifier, f_closure) and the findings it already holds. Severities, scope and the finding list come from CONS and the invariant probe, not from the base.

The quantitative layer saturates: IC, SR and SC are 1.0 for all three cards, so only RC and DC discriminate. The qualitative layer and the debate carry most of the information.

## Quantitative Scoring (50% weight)

ADAPT: the scored artifacts are reviewer cards, not roadmaps, so each metric is adapted as follows. Every figure is computed mechanically by the script from the card text and the cited files.

- RC (requirement coverage, 0.30): share of the 9 elements the brief's exact return format requires: (1) header `reviewer: <n> persona: <name> model: <name>`; (2) every finding has id, severity and tag; (3) every claim is one sentence (counted as no sentence end followed by a capital letter inside the claim); (4) every finding has at least one `ref` plus `quote`; (5) every finding has a `fix`; (6) every verifier states an expected value (`expect`, `must`, `prints`, `returns`, a number); (7) `f_closure` has F-01..F-10 each with an allowed verdict (`fixed`, `partial`, `not fixed`, `fixed with new defect`); (8) `self_audit`; (9) `confidence`.
- IC (internal consistency, 0.25): 1 - (citations the blind calibrator found wrong + internal contradictions) / citations the calibrator checked. Calibrators: V1 0 of 42, V2 0 of 31, V3 0 of 30 failed (`reviewer-N-card-calibrated.yaml` lines 10-11). I read each card in full looking for a claim that contradicts the same card's f_closure or self_audit and found none in any card.
- SR (specificity, 0.15): concrete tokens (TL/DESIGN/ADD/STYLE/BASE line refs, ids such as R1-F3 or INV-005, item numbers, numbers of two or more digits, code spans) / (concrete + vague words: appropriate, as needed, properly, adequate, should consider, might, various, etc., arguably, best practices, perhaps, probably, somewhat). The provenance comment lines at the top of each variant file are excluded.
- DC (dependency completeness, 0.15): (evidence quotes that are verbatim substrings of their cited line in the real file + internal references that resolve) / (all evidence quotes + all internal references). Internal references are the card's own R<n>-F<m> ids (must be defined in the card) and F-01..F-10 (must be 1 to 10). References to other documents' ids (R4-F5, a qa/r4 finding) are external and excluded, as the protocol says.
- SC (section coverage, 0.15): top-level keys of the card (`reviewer`, `findings`, `f_closure`, `self_audit`, `confidence`) / the maximum across cards.

| Metric | Weight | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|---|---|---|---|---|
| RC | 0.30 | 0.778 (7 of 9: claims not one sentence, 5 of 5; f_closure F-02 and F-10 "not checked") | 1.000 (9 of 9) | 0.889 (8 of 9: claims not one sentence, 3 of 3) |
| IC | 0.25 | 1.000 (0 failed of 42; 0 contradictions) | 1.000 (0 of 31; 0) | 1.000 (0 of 30; 0) |
| SR | 0.15 | 1.000 (169 concrete, 0 vague) | 1.000 (105, 0) | 1.000 (133, 0) |
| DC | 0.15 | 1.000 (15 of 15 quotes, 27 of 27 internal refs) | 1.000 (10 of 10, 12 of 12) | 1.000 adjusted (11 of 11, 18 of 18); 0.862 against the files today (7 of 11 quotes) |
| SC | 0.15 | 1.000 (5 keys) | 1.000 (5) | 1.000 (5) |
| **quant_score** | | **0.933** | **1.000** | **0.967** |

DC for V3, honestly stated: four of V3's eleven quotes cite `coverage-matrix.yaml` lines 1, 165, 256 and 258, and the matrix was rebuilt at 05:56:15, after V3 read it (`audit.log` step `1B.refresh`; diff-analysis X-006 and A-008 CONTRADICTED). Those four quotes no longer match today's file. V3's blind calibrator verified them before the rebuild ("matrix line 1 says 'run 3', line 256 shows INF-A06 as status: partial", `reviewer-3-card-calibrated.yaml` line 13), so the score counts them as resolved at read time (DC 1.000). With today's file DC is 0.862, V3's quant falls to 0.946 and its combined score to 0.873; the base does not change.

## Qualitative Scoring (50% weight): Additive Binary Rubric (30 criteria)

Claim-Evidence-Verdict per criterion. Evidence is quoted from the card or cited to the debate record. A MET verdict without a citable passage defaults to NOT MET. "RESOLVED" marks a criterion where the two passes disagreed; the final verdict and its reason are given (see Position-Bias Mitigation). Criterion codes: C completeness, K correctness, S structure, L clarity, R risk coverage, E invariant and edge-case coverage, numbered 1 to 5 in the protocol order (`refs/scoring-protocol.md` A.2).

### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| C1 all explicit requirements of the brief (ten closures plus new defects) | NOT MET: "F-02: not checked - item 13.1 is outside my slice." and "F-10: not checked"; two of the ten required closures are absent. | MET: all ten closures judged (F-01 partial, F-02..F-10 fixed) plus two findings. | MET: all ten closures judged plus three findings. |
| C2 edge cases and failure scenarios | MET: "I traced the 7.10 lifecycle through first run with authorization, first run without, failed check after the edit, and resume." | MET: verifier "Walk no-optional, resolved-refusal and resolved-approval cases". | MET: R3-F3 "a DESIGN change made in Phase 13 would not be caught". |
| C3 dependencies and prerequisites | MET: R1-F5 "the only route is then a HALT, because ticked 7.10 is not retried and the style fixer 11.14 cannot run first". | MET: R2-F2 "despite 7.17 requiring the approved count, approved argv and a re-capture". | MET: R3-F3 "The 14.x hashes are taken only when those items start". |
| C4 success or completion criteria | MET: R1-F2 verifier "`grep -c '^## Execution authorization (verbatim)' <step-7.10 file>` must print 1". | MET: R2-F1 verifier "each completed case must satisfy Verification and Completion together". | MET: R3-F1 verifier "grep -n 'status: partial' on the run-4 coverage-matrix.yaml prints only line 225". |
| C5 out of scope stated | MET: self_audit "I did not check: the 7.17 text for how OQ-17 and OQ-18 are written, beyond the glob names". | MET: "Limits: no shell, tests, live captures, hash recomputation, installed activation or model-behaviour checks were performed." | MET: "What I could not check: I could not run diff". |
| **Subtotal** | **4/5** | **5/5** | **5/5** |

### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| K1 no factual errors | NOT MET: R1-F1 verifier "Today 7.20 returns PASS (it matches the R2 section)" was conceded as overstated by V1's own advocate (CONS section 2, row R1-F1, R1v1:58) and rejected by all three (CONS X-005). | MET: both findings verified on their cited lines (diff-analysis Adjudication A: "both are real"); calibrator 0 of 31 citations failed; the debate kept both at HIGH-conditional unanimously or 2 of 3 (CONS M-01, M-02). | NOT MET (RESOLVED): R3-F2 "Item 13.1 says ticked item 5.2 produced the DESIGN R2 bullet" misreads TL:2265, which says "item 5.2 aligned it with master's 5-minute sweep bound"; V3's own advocate withdrew it (R1v3:29 "WITHDRAWN as a defect") and the calibrator called it overstated. |
| K2 fixes feasible within the stated constraints | NOT MET: R1-F1 fix "Have the owner (or the supplier of that message) save the message to a named file" needs an owner action the plan does not create; rejected by all three (invariant-probe INV-R4-027). | NOT MET (RESOLVED): R2-F2 fix "Apply the same qualification to the reused R5 review inputs" edits ticked items 6.5 to 6.22, whose completed bodies the second revision freezes (BUILD-REQUEST line 18 "completed body (137)"); invariant-probe INV-R4-012 UNADDRESSED. | MET: R3-F3 first option "record the same four-file sha256sum ... before the spawn and re-check it after, as 14.25 does" fits labels 13.18/13.22, which are inside the 85; the frozen-hash alternative was withdrawn but the first option stands alone. |
| K3 terminology consistent | MET: TL, ADD, STYLE, Branch 1/2 used the same way throughout. | MET: "TL denotes the task file ... DESIGN denotes docs/designs/orchestrator-mode.md"; terms stable. | MET: TL/ADD/BASE and the F-ids used consistently. |
| K4 no internal contradictions | MET: no claim contradicts its own f_closure (F-04 "fixed with new defects" matches R1-F1, F2, F4). | MET: F-01 "partial" matches R2-F1 and R2-F2. | MET: F-03 "fixed" is explained ("not blocking because no check greps the ADD:19 literal"). |
| K5 claims supported by evidence | MET: 15 of 15 quotes resolve on their cited lines. | MET: 10 of 10 quotes resolve. | MET: 11 of 11 quotes resolved when read (7 still match today; see DC). |
| **Subtotal** | **3/5** | **4/5** | **4/5** |

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| S1 logical ordering | MET: header, findings, f_closure, self_audit, confidence (the brief's order). | MET: same order. | MET: same order. |
| S2 consistent hierarchy | MET: every finding has the same fields. | MET: every finding has the same fields (ref and quote on two lines, same mapping). | MET: every finding has the same fields. |
| S3 separation of concerns | MET: findings, closures and limits are separate. | MET: separate. | MET: separate. |
| S4 navigation aids | MET: ids R1-F1..F5 cross-referenced from f_closure ("see R1-F3 (baseline file overwrite)"). | MET: ids R2-F1/F2 and alias definitions in self_audit. | MET: ids R3-F1..F3, cross-reference "(R3-F3)" in self_audit. |
| S5 follows the artifact convention (the brief's "exact" return format) | NOT MET (RESOLVED): 5 of 5 claims run to several sentences, and "not checked" is not one of the allowed f_closure verdicts. | MET: one-sentence claims; every closure uses an allowed verdict. | NOT MET (RESOLVED): 3 of 3 claims run to several sentences ("The run-4 coverage matrix is a byte copy of run 3, so ... The edited item 7.10 now carries ... The gate is still not falsely passed"). |
| **Subtotal** | **4/5** | **5/5** | **4/5** |

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| L1 unambiguous language | NOT MET: R1-F5 "If 11.4 pins the style source for "without fabricated success", a literal 7.10 can fail it"; R1-F3 "A stub-first write by the agent can erase the baseline". | MET: directive fixes, e.g. "Make 7.24 check the approved post-7.17 allowlist and capture contract". | NOT MET: R3-F1 "INF-A06 should flip to covered and union coverage should rise from 0.985 to about 0.990"; R3-F2 "fix: Optional." |
| L2 concrete | MET: exact greps and file names in every fix. | MET: named items, counts and cases. | MET: exact greps, line numbers and hashes. |
| L3 each section has one purpose | MET | MET | MET |
| L4 acronyms and terms defined on first use | NOT MET: TL, ADD, STYLE, OQ, HALT, R2 used undefined (the shorthand comes from the brief). | NOT MET: TL and DESIGN are defined only at the end, in self_audit; OQ, R5, HALT undefined. | NOT MET: TL, ADD, BASE, INF-A06, R4-F5 used undefined. |
| L5 actionable next steps | MET: one fix and one verifier per finding. | MET: same. | MET: same. |
| **Subtotal** | **3/5** | **4/5** | **3/5** |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| R1 at least 3 risks with probability and impact | NOT MET: severities give impact, but no finding states a probability. | NOT MET: two findings only, and none states a probability. | NOT MET: three findings, no probability stated. |
| R2 mitigation per risk | MET: a fix per finding. | MET: a fix per finding. | MET: a fix per finding. |
| R3 failure modes and recovery | MET: R1-F5 failure leads to "a HALT"; R1-F2 retry and resume path. | MET (RESOLVED): R2-F1 names the failure mode ("cannot satisfy its literal completion checks") and the recovery route ("needs a bounded authorization extension"). | MET: R3-F3 failure "would not be caught", recovery by a hash guard. |
| R4 external dependencies and their failure | MET: R1-F1 "The "later dated owner message" branch has no on-disk source to compare against". | MET: owner approval and refusal walked as separate cases (R2-F1 verifier). | MET (RESOLVED): R3-F3 rests on the behaviour of spawned docs-gate fix agents that "may edit "the docs"" (tag [INFERRED]). |
| R5 monitoring or validation mechanism | MET: a verifier per finding. | MET | MET |
| **Subtotal** | **4/5** | **4/5** | **4/5** |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|---|---|---|---|
| E1 collection boundaries (empty, single, maximum) | MET: one section versus two on a resume (R1-F2); "OQ-17/OQ-18 handled as SKIP when absent" (f_closure F-01). | MET: "Eight prerequisite records alone ... Plus one or both resolved optional records ... An unmatched prerequisite glob produces no matching filenames and count 0". | NOT MET: counts given are totals ("BASE has 59 matching old lines", six sha256sum hits); no empty, single or maximum case is analysed. |
| E2 state interactions across components | MET: Blocked status and an existing section across 7.10, 7.20 and a resume. | MET: the 7.17 resume state (RESOLVED, halt cleared) against its Verification. | MET: a Phase 13 DESIGN edit against the start-time hashes of 14.x. |
| E3 guard gaps | MET: R1-F1, R1-F3, R1-F4. | MET: R2-F2 unconditional guard. | MET: R3-F3 no sha256 guard. |
| E4 count divergence | MET: "expect 1" against a second section; "expect 6". | MET: ten templates against the approved count. | MET: "(0 today; the only hits now are lines 1363, 1391, 2614, 2642, 2705, 2733)". |
| E5 interaction effects | MET: R1-F5 chain (omitted clause, 11.4 pin, F-05 route, 11.14 order). | MET: the approved 7.17 branch combined with the 7.24 lens. | MET: 13.18 fixer scope combined with the timing of the 14.x hashes. |
| **Subtotal** | **5/5** | **5/5** | **4/5** |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4/5 | 5/5 | 5/5 |
| Correctness | 3/5 | 4/5 | 4/5 |
| Structure | 4/5 | 5/5 | 4/5 |
| Clarity | 3/5 | 4/5 | 3/5 |
| Risk Coverage | 4/5 | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 | 4/5 |
| **qual_score** | **23/30 = 0.767** | **27/30 = 0.900** | **24/30 = 0.800** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case Coverage | Eligible as base (needs at least 1/5) |
|---|---|---|
| V1 | 5/5 | yes |
| V2 | 5/5 | yes |
| V3 | 4/5 | yes |

The floor is not suspended: every variant meets it.

## Position-Bias Mitigation

Pass 1 judged the cards in input order (V1, V2, V3); pass 2 judged them in reverse order (V3, V2, V1), criterion by criterion. Limitation: both passes were made by me, in one context, so this is a weaker control than two independent judges; it catches criteria where my verdict depended on which card I had just read, not my own systematic leanings.

| Variant | Pass 1 (MET of 30) | Pass 2 (MET of 30) | Final |
|---|---|---|---|
| V1 | 24 | 23 | 23 |
| V2 | 28 | 26 | 27 |
| V3 | 24 | 25 | 24 |

Disagreements: 6 of 90 criterion-variant pairs. Each was re-evaluated with both passes' evidence side by side; the re-evaluation is final. Final verdicts that differ from pass 1: 4 (K1 V3, K2 V2 and S5 V1 changed to NOT MET; R4 V3 changed to MET). Final verdicts that differ from pass 2: 2 (S5 V3 and R3 V2).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final and reason |
|---|---|---|---|---|---|
| K1 | V3 | MET | NOT MET | disagree, re-evaluated | NOT MET. Pass 1 accepted R3-F2 as a history-only remark; pass 2 applied the rule used for V1 (a claim its own advocate withdrew as untrue fails K1). The rule must be the same for both cards. |
| K2 | V2 | MET | NOT MET | disagree, re-evaluated | NOT MET. Pass 1 judged only the main 7.24 fix; pass 2 judged every part of each fix. The R5 sub-fix is part of R2-F2's fix and breaks the frozen completed bodies, the same class of defect as V1's owner-file fix. |
| S5 | V1 | MET | NOT MET | disagree, re-evaluated | NOT MET. The brief says "exact"; multi-sentence claims and a "not checked" closure verdict are outside it. |
| S5 | V3 | NOT MET | MET | disagree, re-evaluated | NOT MET. Same rule as V1: three multi-sentence claims. |
| R3 | V2 | MET | NOT MET | disagree, re-evaluated | MET. Pass 2 objected that V2 does not trace the runtime halt (CONS section 4.1 did that). The criterion asks for a failure mode and a recovery procedure; V2 names both (the literal checks cannot be satisfied; a bounded authorization extension repairs it). |
| R4 | V3 | NOT MET | MET | disagree, re-evaluated | MET. Pass 1 treated the docs-gate fix agents as internal to the plan. They are spawned agents whose edits the plan cannot control, the same kind of dependency V1's R1-F3 rests on, so the same rule gives MET. |

A pass-order effect is visible: the first card read in each pass was given the benefit of the doubt on S5 (V1 in pass 1, V3 in pass 2). The re-evaluations removed it.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | Final score | Debate points won (S, C, X, A) | Debate points won (U, O) |
|---|---|---|---|---|---|
| V1 (analyzer) | 0.933 -> 0.467 | 0.767 -> 0.383 | **0.850** | 2 | 3 |
| V2 (qa) | 1.000 -> 0.500 | 0.900 -> 0.450 | **0.950** | 9 | 4 |
| V3 (refactorer) | 0.967 -> 0.483 | 0.800 -> 0.400 | **0.883** | 7 | 5 |

Debate points are counted from the Winner column of CONS section 3: a row counts for a variant when its winner cell starts with that variant (V1: C-003, X-003; V2: S-001, S-003, C-001, C-005, C-006, X-001, X-004, A-002, A-007; V3: S-004, C-002, C-004, X-002, X-006, X-007, A-008).

- Ranking: V2 0.950, V3 0.883, V1 0.850.
- Margin between first and second: 6.7 percentage points, above the 5-point threshold.
- Tiebreaker applied: No. (Had it been needed, level 1 would also pick V2: 9 points won against V3's 7.)
- Sensitivity: with V3's DC taken against today's matrix (0.862), V3 scores 0.873; the ranking is unchanged.

## Selected Base: Variant 2 (reviewer 2, qa; recorded model gpt-6.1-sol in the haiku-class slot, the agent reported "ChatGPT (exact model identifier unavailable)"; calibrated C 0.86)

### Selection Rationale

V2 has the highest combined score (0.950) by a margin of 6.7 points, so no tiebreaker was needed. It is the only card that meets the brief's return format exactly (RC 9 of 9), it judged all ten closures, and it holds the only two findings that make a correct run fail if the optional OQ-17/OQ-18 branch fires (R2-F1 and R2-F2 became M-01 and M-02, both HIGH-conditional in CONS). It won the most debate points (9), including the highest-impact rows C-001, X-001, X-004, U-007 and U-008. Its weaknesses are real and are repaired from the other sources: it raised nothing below HIGH, one part of its R2-F2 fix is infeasible (the R5 sub-fix, INV-R4-012), and its 7.24 fix wording covers only part of the breach (INV-R4-011).

### Strengths to Preserve from Base

1. The per-finding frame: one-sentence claim, `ref` plus verbatim `quote` evidence, smallest fix, verifier with an expected value; and the full ten-line f_closure.
2. R2-F1 (7.17 Verification against its own resume) and its case walk (no optional record, resolved refusal, resolved approval; a still-PENDING record must block completion).
3. R2-F2 (7.24 lens against an approved allowlist change), with "Keep rejection of every unapproved addition."
4. The origin statement "The two reported contradictions predate R2" (CONS C-006, X-004) and the scope statement "Item 7.17 is outside the present 85-label edit surface" (CONS C-005).

### Strengths to Incorporate from Non-Base Variants and the Debate Record

1. From V1: R1-F3 (sha256 baseline shares the fix-log path) as M-03 MEDIUM; R1-F4 (re-run lists omit the authorization check) as M-04; R1-F2 (7.10 resume rule) as M-05; R1-F5 (omitted ADD:17 and ADD:19 clauses) as M-06; R1-F1 (7.20 record check, two-way authority text) as M-07; V1's F-07 "partial" closure and its F-04 residual list.
2. From V3: R3-F3 (13.18/13.22 without a DESIGN hash guard) as M-08; its character-level F-02 closure and the F-06 count check.
3. From the diff analysis: O-001 (folded into M-01) and O-002 (stale DESIGN line numbers, M-09).
4. From the invariant probe: the fix corrections that the debate did not make (INV-R4-003, 009, 011, 015, 020, 021, 022, 026), carried into the fix text or notes of the matching finding.
5. From the Tier 1 card (reference only): the overlaps L1, L2, L3, L6 and L8 as corroboration, and its F-01..F-10 verifier runs for the f_closure block.

