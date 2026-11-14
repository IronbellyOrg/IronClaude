# Base Selection Report

Scope: Step 3 of /sc:adversarial Mode A (--compare, standard) inside reflect post-execution audit `reflect-post-20261112T192600Z-TASK-RF-sweep-phase1`. Variants: V1 = reviewer 1 (analyzer, sonnet), V2 = reviewer 2 (qa, haiku), V3 = reviewer 3 (refactorer, opus); each card is scored together with its blind calibration. Source requirements for RC = deviation leads DC-1..DC-12 of `../reflection-card-t1.yaml` (no formal FR ids exist for the artifact, so lead-level topic matching per the RC edge case). Scored text = the reviewer card block (the calibration is evidence, not scored content).

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (analyzer/sonnet) | V2 (qa/haiku) | V3 (refactorer/opus) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.417 (5/12) | 0.417 (5/12) | 0.500 (6/12) |
| internal_consistency | 0.25 | 0.846 (1-2/13) | 0.824 (1-3/17) | 0.929 (1-1/14) |
| specificity_ratio | 0.15 | 0.988 (255/258) | 1.000 (216/216) | 0.995 (189/190) |
| dependency_completeness | 0.15 | 0.977 (43/44) | 0.976 (40/41) | 0.961 (49/51) |
| section_coverage | 0.15 | 1.000 (2/2) | 1.000 (2/2) | 1.000 (2/2) |
| **quant_score** | | **0.781** | **0.777** | **0.826** |

### Arithmetic

- **RC (lead matched by `lead_ref`, lead_verdict key, or 3+ word topic match).** V1: DC-1, DC-2, DC-3, DC-9, DC-12 = 5. V2: DC-6, DC-8, DC-10, DC-11, plus DC-1 by topic (R2-F6 "FR-006 class coverage excludes working" = Rule 5 inert) = 5. V3: DC-4, DC-5, DC-7, DC-9, DC-3 by topic (R3-F3 "chunked reads and a kill at 8 MiB"), DC-12 by keyword (R3-F3 "output over 8388608 bytes" vs SPEC "output over 8 MiB") = 6. Union of the three = 12/12; no single variant exceeds 6.
- **IC = 1 - contradictions / scorable claims** (claims = findings + lead_verdicts + objective_checks). V1 13 claims, 2 contradictions: R1-F8 class `necessary` while its reasoning shows DESIGN :346 and :517 agree with the code; R1-F7 class `authorized` while its reasoning says authorization for `freshness_age_s` is not shown. V2 17 claims, 3: R2-F6 `regression` while its own `authorization_source` is the owner approval; R2-F5 `regression` while its reasoning finds "No difference in the FINAL detection value"; objective 7 labelled `fail` while its text says "not an execution deviation". V3 14 claims, 1: R3-F4 `regression` while its reasoning says "Practical risk is low".
- **SR = concrete / (concrete + vague)** over the card block, computed with a coarse regex (file:line citations plus quantity tokens versus the vague word list of the protocol). Concrete 255 / 216 / 189, vague 3 / 0 / 1 (V1 lines 52, 101, 103; V3 line 78). All near 1.0; this metric does not separate the variants.
- **DC = resolved / total internal references.** References = calibrator-checked citations + `lead_ref` values and lead_verdict keys (each resolves to a DC-n of the Tier-1 card) + cross-references to task finding ids. Unresolved: V1 1 (DC-1 cite `:18-19`, quote is at `:13`); V2 1 (the "FIN-F19" cross-reference points at the wrong item); V3 2 (`probes.py:837`, `commands.py:219-221`). V1 (31+12)/(32+12) = 43/44; V2 (33+7)/(33+7+1) = 40/41; V3 (40+9)/(42+9) = 49/51.
- **SC = H2 sections / max.** Each variant file has two H2 sections (Reviewer card, Blind calibration): 2/2 = 1.0. (Top-level YAML keys differ: V2 adds `objective_checks`, V3 adds `checked_clean`; the protocol counts H2 headings, so this is not scored.)
- **quant_score** V1 = 0.125+0.2115+0.1482+0.1466+0.15 = 0.7813; V2 = 0.125+0.2059+0.15+0.1463+0.15 = 0.7772; V3 = 0.15+0.2321+0.1493+0.1441+0.15 = 0.8255.

## Qualitative Scoring (50% weight) - Additive Binary Rubric (30 criteria, CEV)

Each cell is the FINAL verdict (Y = MET, N = NOT MET); `*` = passes disagreed, resolved in the log below. Evidence cell = CLAIM/EVIDENCE per variant (verdict follows the evidence; no evidence means N).

### Completeness

| # | Criterion | V1 | V2 | V3 | Evidence (quote or sections searched) |
|---|---|---|---|---|---|
| 1 | Covers all explicit requirements | N | N | N | RC leads matched 5/12, 5/12, 6/12; no card covers all of DC-1..12 |
| 2 | Edge cases and failure scenarios | Y | Y* | Y | V1 R1-F3 "every row of a Run lacks a valid id"; V2 R2-F4 "full-timeout fake probes"; V3 R3-F2 FIFO "hangs the read-only command" |
| 3 | Dependencies and prerequisites | Y | Y | Y | `grounding_gaps` with `next_evidence`: 3 gaps in each card |
| 4 | Success/completion criteria | N | Y | N | V2 `objective_checks` 1-7 pass/fail; V1 and V3: searched lead_verdicts, findings, gaps, none states a completion test |
| 5 | Out-of-scope stated | Y | Y | Y | V1 "Sections 7.1-7.4 coverage not completed"; V2 "sampled seven objectives and eight requirement rows"; V3 "Read-only reviewer with no git access" |
| **Subtotal** | | **3/5** | **4/5** | **3/5** | |

### Correctness

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | No factual errors / hallucinated claims | N | N* | N | V1 DC-1 cite `:18-19` wrong (quote at `:13`), R1-F7 and R1-F8 overstated; V2 "FIN-F19" points at the wrong item; V3 `probes.py:837` and `commands.py:219-221` failed |
| 2 | Approaches feasible | Y | Y | Y | V1 R1-F4 `subprocess.run` bound 10 s; V2 R2-F5 tail-only gives the same value; V3 0-byte FIFO `st_size` (POSIX) |
| 3 | Terminology consistent | Y | N | Y | V2 labels R2-F6 `regression/blocking` with the owner approval as its own source, objective 7 `fail` for "not an execution deviation"; V1 and V3 use the four classes as defined |
| 4 | No internal contradictions | N | N | N | IC above: 2, 3 and 1 contradictions |
| 5 | Claims supported by evidence | Y | Y | Y | every finding carries `evidence` lists: 8/8, 6/6, 10/10 |
| **Subtotal** | | **3/5** | **2/5** | **3/5** | |

### Structure

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Logical ordering | Y | Y | Y | lead_verdicts, findings, grounding_gaps, inferred_claims in all three |
| 2 | Consistent hierarchy | Y | Y | Y | one top-level YAML level, same finding fields |
| 3 | Separation of concerns | Y | Y | Y | gaps, inferred claims apart from findings; V2 `objective_checks`, V3 `checked_clean` are separate blocks |
| 4 | Navigation aids | Y | Y | Y | `lead_ref` plus finding ids R1-Fn, R2-Fn, R3-Fn (V2: 3 of 6 are `NEW`, 3 carry a DC ref) |
| 5 | Artifact-type conventions | Y | Y | Y | reviewer-card schema: reviewer, persona, model_class, lead_verdicts, findings, self_reported_confidence |
| **Subtotal** | | **5/5** | **5/5** | **5/5** | |

### Clarity

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Unambiguous language | N* | Y | N | vague markers: V1 3 (`:52` "Arguable as regression", `:101` "likely minor", `:103` "slightly beyond"); V2 0; V3 1 (`:78` "slightly different surface") |
| 2 | Concrete, not abstract | Y | Y | Y | file:line citations: 78, 57, 65 |
| 3 | Clear purpose per section | Y | Y | Y | each finding has a one-clause title |
| 4 | Acronyms defined | N | N | N | FR, NFR, SP-15, FIN-F12, OQ, GQ-105, L3 used without definition |
| 5 | Actionable next steps | Y* | Y | Y | every card gives `next_evidence` per gap (concrete grep or command); no card gives a fix per finding |
| **Subtotal** | | **3/5** | **4/5** | **3/5** | |

### Risk Coverage

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | At least 3 risks with probability and impact | Y | Y | Y | severity plus confidence on 8, 6, 10 findings |
| 2 | Mitigation per risk | N | N | N | no card pairs a risk with a mitigation (they sit in the Tier-1 `recommendations`) |
| 3 | Failure modes and recovery | N* | Y | Y | V1 R1-F3 failure mode, no recovery; V2 R2-F2 "specifies follow-up work"; V3 R3-F2 "until the skill's 120 s Bash kill", R3-F9 "falls back to ordinary formatting" |
| 4 | External dependencies | Y | Y | Y | V1 Orca worker-list rows; V2 Orca outage not relayed; V3 `orca worktree ps` scope gap |
| 5 | Detection / validation mechanism | Y | Y | Y | `next_evidence` commands, e.g. V3 "git diff --cached --name-only \| grep ^.claude/" |
| **Subtotal** | | **3/5** | **4/5** | **4/5** | |

### Invariant & Edge Case Coverage

| # | Criterion | V1 | V2 | V3 | Evidence |
|---|---|---|---|---|---|
| 1 | Collection boundaries | Y | Y* | Y | V1 R1-F3 empty `rows`; V2 R2-F5 over-1 MiB ledger; V3 R3-F2 0-byte FIFO, 8 MiB |
| 2 | State interactions across components | Y | N | Y | V1 probes drops the row, `classify.py:690-694` reads only `listing.unscanned`; V3 R3-F5 report sanitizer to JSON `report_path` to skill step 3; V2 compares code with SPEC text only |
| 3 | Guard-condition gaps | Y | N | Y | V1 R1-F3 missing or non-string `dispatchId`; V3 R3-F2 no regular-file check, R3-F1 no fsmonitor override; V2 none |
| 4 | Count divergence / ranges | N* | Y | Y | V2 R2-F5 and V3 R3-F4 first/last 512 KiB range read as tail only; V1 none (R1-F4 is a timing divergence) |
| 5 | Interaction effects | Y | N | Y | V1 inferred claim: first-call rule turns `output over 8 MiB` into `unavailable` (`probes.py:355-357`); V3 R3-F3 `_git` limit with the `worktree not readable` collapse (`:936-937`); V2 none |
| **Subtotal** | | **4/5** | **2/5** | **5/5** | |

**Edge-case floor check**: V1 4/5, V2 2/5, V3 5/5, all at or above 1/5: all three eligible as base (no suspension needed).

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3 | 4 | 3 |
| Correctness | 3 | 2 | 3 |
| Structure | 5 | 5 | 5 |
| Clarity | 3 | 4 | 3 |
| Risk Coverage | 3 | 4 | 4 |
| Invariant & Edge Case | 4 | 2 | 5 |
| **qual_score** | **21/30 = 0.700** | **21/30 = 0.700** | **23/30 = 0.767** |

## Position-Bias Mitigation

Pass 1 in input order (V1, V2, V3), pass 2 in reverse (V3, V2, V1). 7 of 90 verdicts disagreed (the other 83 agreed); each was re-evaluated with both passes' evidence side by side and the re-evaluation is final.

| Criterion | Variant | Pass 1 | Pass 2 | Final | Re-evaluation reason |
|---|---|---|---|---|---|
| Compl. 2 | V2 | Y | N | Y | R2-F4 names the full-timeout scenario and shows it is untested; that addresses a failure scenario even without behaviour analysis |
| Correct. 1 | V2 | Y | N | N | 33/33 citations hold, but the "FIN-F19" cross-reference is wrong (calibrator note); one factual error is enough |
| Clarity 1 | V1 | Y | N | N | three hedges are cited (`:52`, `:101`, `:103`); the criterion allows none |
| Clarity 5 | V1 | N | Y | Y | `next_evidence` on 3 gaps is a concrete next step, the same evidence that gave V2 and V3 a Y |
| Risk 3 | V1 | Y | N | N | R1-F3 gives a failure mode only; the "origin not proved" note is a symptom, not a recovery |
| Invar. 1 | V2 | N | Y | Y | the 1 MiB ledger limit with the first/last 512 KiB split is a max-size boundary |
| Invar. 4 | V1 | N | Y | N | the `last_record_ts` inferred claim is a selection-rule difference, not an off-by-one or range count |

Disagreements re-evaluated: 7. Final verdict differs from pass 1 in 5 (Correct. 1, Clarity 1, Clarity 5, Risk 3, Invar. 1) and from pass 2 in 2 (Compl. 2, Invar. 4). The tables above already use the final verdicts.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points (computed for sensitivity only) |
|---|---|---|---|---|
| V1 (analyzer/sonnet) | 0.3907 | 0.3500 | **0.741** | 4 |
| V2 (qa/haiku) | 0.3886 | 0.3500 | **0.739** | 3 |
| V3 (refactorer/opus) | 0.4128 | 0.3833 | **0.796** | 8 |

**Margin**: V3 over V1 = 0.0554 (5.5 points), above the 5% threshold. **Tiebreaker applied**: No.

Sensitivity (the margin is thin): if V3's keyword match for DC-12 is dropped, V3 RC is 5/12, quant 0.801, final 0.784 and the margin 0.043, inside 5%. The tiebreaker would then decide: debate points = diff points where the variant raised the finding and its original class equals the final class in the Scoring Matrix. V3 8 (C-003, C-006, C-007, C-013, C-014, C-015, C-016, C-017), V1 4 (C-001, C-004, C-005, C-008), V2 3 (C-009, C-010, C-011). V3 wins again, so the selection does not rest on that one match.

## Selected Base: Variant 3 (reviewer 3, refactorer, opus)

### Selection Rationale

V3 has the highest quant score (0.826 against 0.781 and 0.777: widest lead coverage 6/12, fewest internal contradictions, 1) and the highest qual score (23/30; the only 5/5 on Invariant & Edge Case, and 4/5 on Risk Coverage). It carries the largest verified risk surface (10 findings, 42 citations checked, blind-calibrated C 0.73 against 0.65 and 0.63) and no blocking item. Its weaknesses are known and bounded: R3-F4 over-labelled as Regression, R3-F3 contested, and no look at C-001, C-004, C-009..C-012; the other two variants cover exactly those.

### Strengths to Preserve from Base (V3)

1. Unique risk surface: R3-F1 fsmonitor, R3-F2 FIFO, R3-F5 `report_path` sanitizer, R3-F6 and R3-F7 (C-006, C-007, C-015, C-016, C-017).
2. R3-F3 reasoning on SPEC :286 against DESIGN :753 and `tests/sweep/conftest.py:36-41` (the task's stated reason for `subprocess.run` is false): the basis of the contested Regression (C-003).
3. R3-F9 and R3-F10 Authorized findings with verbatim DESIGN :1052, :717 and :680 sources (C-014, C-013).
4. `checked_clean` list (no `src/superclaude/` path, never-as-worker list, `.gitignore`).

### Strengths to Incorporate from Non-Base Variants

1. V1 R1-F1, R1-F2: owner-decision grounding for Rule 5 (C-001 Authorized) plus the residual footnote Drift (FIN-F15); `working: 0` has no caveat.
2. V1 R1-F3: the dropped worker-list row and the origin-guard hole (C-004), the only card with it; carries the INV-001/INV-002 conditional escalation.
3. V1 R1-F5, R1-F6, R1-F7: `_git` reason wording (C-005), extra source row and model fields (C-008); V1's dissent on C-003 (Drift medium) as a carried note.
4. V2 R2-F1, R2-F2, R2-F3: stale banner and Open Questions (C-009), FIN-F7 (C-010), environmental test failures (C-011).
5. V2 R2-F4: NFR-007 "still publish" tests stop at `report.render` (C-012), plus the objective-level qualification (objective 6 not fully satisfied, objective 7 pending).
6. V2 R2-F5 (head never read, misnamed test): kept inside V3's R3-F4 at the lowered class Drift minor (C-002); V1 did not flag it.

