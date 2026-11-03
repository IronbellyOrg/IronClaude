# Base Selection Report

Variants: A = `variant-1-original.md` (reviewer 1, analyzer, PASS), B = `variant-2-original.md` (reviewer 2, qa, PASS), C = `variant-3-original.md` (reviewer 3, refactorer, FAIL). All three are reviewer cards on the same plan.

Citation keys: `VA:N`, `VB:N`, `VC:N` are variant-card lines; `SP:N` is `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md`; `DT` is `debate-transcript.md` in this directory; `R1a:N` and similar are the round files; `TL:N` is the plan; `brief-2:N` is `../../reviewer-briefs/reviewer-2.md`. Every cited line was opened for this step. The card is the unit scored: what the reviewer wrote plus its calibration block, because both are in the variant file.

Debate context carried in: the merged verdict is FAIL with one adjudicated blocker (R3-F1, from C), and convergence is 100% but BLOCKED_BY_INVARIANTS (DT, "Convergence Assessment" and "Invariant-Probe Gate"). Base selection scores card quality; it does not re-decide the verdict.

## Quantitative Scoring (50% weight)
All five metrics were computed from the card text by fixed rules (SP:9), with the counts taken by grep in one read-only batch run for this step.

| Metric | Weight | Variant A (analyzer) | Variant B (qa) | Variant C (refactorer) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.950 (19/20) | 0.700 (14/20) | 0.600 (12/20) |
| internal_consistency | 0.25 | 0.960 (1 contradiction / 25 claims) | 0.923 (1 / 13) | 0.959 (2 / 49) |
| specificity_ratio | 0.15 | 1.000 (74 concrete / 0 vague) | 1.000 (60 / 0) | 0.992 (127 / 1) |
| dependency_completeness | 0.15 | 1.000 (15/15 references resolve) | 1.000 (8/8) | 1.000 (21/21) |
| section_coverage | 0.15 | 0.889 (8/9 top-level blocks) | 1.000 (9/9) | 0.889 (8/9) |
| **quant_score** | | **0.958** | **0.891** | **0.852** |

Computation details:

- **requirement_coverage.** The cards cite no FR or NFR ids, so section-level topic matching applies (SP:39). The common scope is the static P0 scope stated in the briefs, "AC-0.1, AC-0.2, AC-0.3, AC-0.7, AC-0.9, AC-C1 to AC-C6" (brief-2:77), which is 11 checks, plus the plan's 9 units: the Constraints block (TL:17) and Tasks 1-8 (TL:31, 50, 65, 78, 100, 121, 135, 143). That gives 20 units. A check counts when the reviewer's own text names it, ranges included. A plan unit counts when a finding's `tasks:` field holds it, or, for the Constraints, when a finding claim names them.
  - A: 11 checks (VA:113 names AC-0.1, 0.2, 0.3, 0.7, 0.9 and "AC-C1 to AC-C6"); units Tasks 1-6 and 8 (VA:10, 29, 50, 70, 89) plus the Constraints (VA:76-77). Task 7 appears only in the self-audit. 19/20.
  - B: 11 checks (VB:75 "AC-0.1/0.2/0.3/0.7/0.9, AC-C1..C6"); units Constraints, Task 8 and Task 3 (VB:10, 27, 45). 14/20.
  - C: 4 checks in the reviewer's own text (AC-0.9 VC:99, AC-0.2 VC:116, AC-C4 VC:183, AC-C2 VC:191); units Tasks 1-6 and 8 (VC:10, 32, 51, 74, 94, 114, 131, 145, 159, 173, 188) plus the Constraints (VC:12). 12/20.
- **internal_consistency.** Scorable claims are the findings plus their evidence entries (plus B's two matrix spans) (SP:46). A contradiction is a statement in the card that another line of the same card says is wrong (SP:48-52).
  - A: 5 findings + 20 evidence lines = 25. VA:100 cites `test_impact_command.py:308`; VA:130 says the plugin copy is at line 309. 1 contradiction.
  - B: 3 findings + 8 evidence lines + 2 spans = 13. VB:67 says the spec has 452 lines; VB:100 says 451. 1 contradiction.
  - C: 11 findings + 38 evidence lines = 49. VC:123 cites test line 290 for the heading slice, and VC:227 says the quote is not at that line; VC:50 classes R3-F3 as drift, and VC:226 calls that classification loose. 2 contradictions.
- **specificity_ratio.** Concrete statements are non-blank lines carrying a number, line reference or threshold; the `reviewer:` and `self_confidence:` metadata lines are excluded (SP:71). Vague statements are lines with a term from the protocol's vague list (SP:67-70). Only C has one, "might" (VC:211). A's "probably" (VA:37) is not on the list.
- **dependency_completeness.** Internal references are finding ids used outside their own definition (calibration `severity_holds` keys, calibration notes, self-audit mentions). Every one resolves to a defined finding (A: VA:7, 26, 47, 67, 86; B: VB:7, 24, 42; C: VC:7 to VC:185). External file paths are excluded (SP:87).
- **section_coverage.** The cards are YAML, so a top-level key stands in for an H2 section (SP:94). A and C have 8 (`reviewer` to `calibration`); B adds `matrix_omissions` (VB:58) for 9.

Formula (SP:24): A = 0.30×0.950 + 0.25×0.960 + 0.15×1.000 + 0.15×1.000 + 0.15×0.889 = 0.958. B = 0.210 + 0.231 + 0.150 + 0.150 + 0.150 = 0.891. C = 0.180 + 0.240 + 0.149 + 0.150 + 0.133 = 0.852.

## Qualitative Scoring (50% weight) — Additive Binary Rubric
30 binary criteria in 6 dimensions (SP:106-154), each judged under Claim-Evidence-Verdict (SP:162-173): a MET needs a cited line, and anything without one is NOT MET. The tables show the **final** verdict after the dual pass; the pass-by-pass record and the re-evaluations are in "Position-Bias Mitigation". In each cell the claim is "criterion N is met / not met in Variant X", the evidence is the citation, and the verdict is MET (1) or NOT MET (0).

### Completeness (5 criteria)
| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1. Covers all explicit requirements | MET | Maps every static outcome to a task AC (VA:112-113) and checks Task 7's inputs (VA:110-112) | MET | Walks every in-scope requirement against a task AC (VB:74-78) | NOT MET | Names only 4 of the 11 checks (VC:99, 116, 183, 191); its calibrator lists Task 7 and the AC-0.1 install call as unchecked (VC:229) |
| 2. Edge cases and failure scenarios | MET | Unmet-AC halt route (VA:35-37); verify-sync failure case (VA:116-118) | MET | Halt-path inventory (VB:82-84) | MET | Ladder-end or dispute halt (VC:14-17); FINAL archive block (VC:57-59) |
| 3. Dependencies and prerequisites | MET | KNOWN_CORE_FILES set-equality and install manifest (VA:107-109) | MET | Pytest targets exist; Depends-on satisfied by source order (VB:68-74) | MET | Task ordering and the Tasks 1-2, 3, 5 dependencies (VC:204-206) |
| 4. Success or completion criteria | MET | Its pass basis: "Every spec-required static outcome ... maps to a task with a runnable acceptance criterion" (VA:112-113) | MET | States why no blocker exists (VB:80-84) | MET | States the blocking rule it applied (VC:208-211) |
| 5. Out-of-scope items | MET | Two-part split authorized by spec line 238 (VA:114) | MET | Deferrals authorized by source.md:238 (VB:79) | MET | No defect in the static-versus-live split (VC:213-214) |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Correctness (5 criteria)
| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1. No factual errors | NOT MET | "two tests that pin plugin core copies" (VA:95) was not confirmed (VA:130) and was later corrected to one test (R1a:47) | NOT MET | "no task instruction breaches the plan's own Constraints" (VB:81-82) is false against TL:21 and TL:90 (conceded, R1b:35); "452-line spec" (VB:67) is 451 (R2b:23) | NOT MET | "matches hits in agents" (VC:97-98) was withdrawn as false matches (R2c:19); line-290 citation is wrong (VC:227) |
| 2. Approaches feasible | MET | Each fix is a one- or two-line plan edit (VA:23-25, 44-46, 64-66, 83-85, 102-104) | MET | VB:23, VB:41, VB:57 | MET | One-sentence reword for the blocker (VC:25-28) |
| 3. Terminology consistent | MET | Severity and class words used as defined throughout (VA:8-9, 27-28, 48-49, 68-69, 87-88); its calibrator flags no class misuse (VA:126-136) | MET | VB:8-9, 25-26, 43-44; class clarity 0.90 (VB:90) | NOT MET | R3-F3 is labelled drift though it is a conflict inside the plan (VC:50, VC:226); C conceded (R2c:13) |
| 4. No internal contradictions (checked against IC) | NOT MET | IC 0.960: VA:100 against VA:130 | NOT MET | IC 0.923: VB:67 against VB:100 | NOT MET | IC 0.959: VC:123 against VC:227; VC:50 against VC:226 |
| 5. Claims supported by evidence | MET | Every finding carries evidence lines, verified byte for byte (VA:126) | MET | Each finding verified (VB:94-97) | MET | All spot-checked citations match (VC:222) |
| **Subtotal** | **3/5** | | **3/5** | | **2/5** | |

### Structure (5 criteria)
| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1. Logical ordering | MET | Should-fix findings before the minor one (VA:8, 27, 48, 68, 87) | MET | Should-fix, then minor (VB:8, 25, 43) | MET | Blocking, then should-fix, then minor (VC:8, 30, 49, 72, 92, 113, 129) |
| 2. Consistent hierarchy | MET | Every finding has the same seven keys (VA:7-25) | MET | Same (VB:7-23) | MET | Same (VC:7-28) |
| 3. Separation of concerns | MET | findings, self_audit, calibration are separate blocks (VA:6, 105, 119) | MET | Plus a separate matrix_omissions block (VB:6, 58, 65, 87) | MET | VC:6, 201, 215 |
| 4. Navigation aids | MET | Finding ids cross-referenced in severity_holds (VA:124) | MET | VB:92 | MET | VC:220 |
| 5. Artifact-type conventions | MET | Same top-level keys as the other cards (VA:1-6, 105, 119) | MET | The extra matrix_omissions block answers the brief's instruction to audit the coverage matrix (brief-2:68) | MET | VC:1-6, 201, 215 |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Clarity (5 criteria)
| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1. Unambiguous language | MET | No term from the criterion's list occurs (grep); "probably" (VA:37) is a stated likelihood | MET | No listed term occurs (grep found none) | NOT MET | "a lenient reviewer might read" (VC:211), against "ends the run" (VC:15-17); the debate flagged the mismatch (R1b:28) |
| 2. Concrete | MET | Literal replacement text (VA:24-25, VA:84-85) | MET | VB:23 | MET | VC:26-28 |
| 3. Clear purpose per section | MET | claim / evidence / recommendation per finding (VA:11-25) | MET | VB:11-23 | MET | VC:11-28 |
| 4. Terms defined on first use | NOT MET | "QA", "FINAL review", "AC" used without definition (VA:36, VA:77) | NOT MET | "E-NO-AC, E-HALT-QA" undefined (VB:83) | NOT MET | "ladder-end halt", "dispute halt", `cmp` undefined (VC:16-17, VC:57) |
| 5. Actionable next steps | MET | A recommendation on every finding (VA:23, 44, 64, 83, 102) | MET | VB:23, 41, 57 | MET | A recommendation on every finding (VC:25 to VC:198) |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

### Risk Coverage (5 criteria)
| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1. At least 3 risks with likelihood and impact | MET | Likely saved files, impact a halt (VA:35-37); "unlikely to block", impact false phase text (VA:57-58); "nothing would catch it", impact shipped `src/` paths (VA:76-77) | NOT MET | Three risks with impact (VB:15-17, VB:34-36, VB:52-53), but no likelihood beyond "nothing blocks" | MET | Halt conditional on a literal reviewer (VC:15-17, VC:211); "will silently go stale" (VC:78-79); "Each failure costs a repair round" (VC:120) |
| 2. Mitigation for each risk | MET | A fix per finding (VA:23-104) | MET | VB:23, 41, 57 | MET | A fix per finding (VC:25-198) |
| 3. Failure modes and recovery | MET | Halt route and its fix (VA:36, VA:45-46) | MET | Halt paths listed (VB:82-84) | MET | Halt paths (VC:16-17) and an alternative repair (VC:69-70) |
| 4. External dependencies | MET | Checked `/opt/Orca` and the profile file (VA:110-112) | NOT MET | "I did not run anything" (VB:85-86); Task 7's environment unexamined (VB:99) | NOT MET | Orca environment and the install signature unchecked (VC:229) |
| 5. Monitoring or validation mechanism | MET | Saved evidence file per check (VA:45-46) | MET | "results the P0 live plan must cite" list (VB:41) | MET | Byte-identity test (VC:88-90); flag check test (VC:154-155) |
| **Subtotal** | **5/5** | | **3/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)
| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1. Collection boundaries | MET | Fan-in caps "at most 10" and "at least 2" (VA:12-15) | NOT MET | No collection-boundary item; searched VB:7-64 | MET | Empty per-phase set for `## Unattended mode` (VC:133-141) |
| 2. State across component boundaries | MET | Evidence artifacts across Tasks 1, 3, 4 and 8 (VA:31-35) | MET | Static report to live-plan handoff (VB:29-34) | MET | A Task 5 edit breaks Task 3's `cmp` (VC:55-59) |
| 3. Guard condition gaps | MET | No gate catches `src/` paths in an installed file (VA:76-77) | NOT MET | Looked for guard breaches and reported none (VB:80-84) | MET | Constraint against the Task 4 write (VC:12-17); no sync guard for a copy (VC:76-79) |
| 4. Count divergence | MET | 11 checks against fewer saved evidence files (VA:31-35) | MET | AC numbering skips AC-0.8 (VB:12-14) | MET | 40 `gh pr` hits, about 121 sites, line-number keys that break (VC:97-101) |
| 5. Interaction effects | MET | The D3 decision interacting with Task 6's phase slot (VA:52-56) | MET | Task 3's decision interacting with AC-C1's by-name exclusion (VB:50-52) | MET | Paraphrase plus plugin copy plus Task 5 edit (VC:53-59) |
| **Subtotal** | **5/5** | | **3/5** | | **5/5** | |

### Qualitative Summary
| Dimension | Variant A | Variant B | Variant C |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 4/5 |
| Correctness | 3/5 | 3/5 | 2/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 3/5 |
| Risk Coverage | 5/5 | 3/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 3/5 | 5/5 |
| **qual_score** | **27/30 = 0.900** | **23/30 = 0.767** | **23/30 = 0.767** |

### Edge Case Floor Check
Rule (SP:156): a variant scoring below 1/5 on Invariant & Edge Case Coverage cannot be the base.

| Variant | Score | Eligible |
|---|---|---|
| A | 5/5 | yes |
| B | 3/5 | yes |
| C | 5/5 | yes |

The floor is not suspended, because no variant scores 0/5.

## Position-Bias Mitigation
Pass 1 judged the cards in input order (A, B, C); Pass 2 judged them independently in reverse order (C, B, A) (SP:209-210). Where the passes disagreed, the criterion was judged again with both passes' evidence side by side, and that verdict is final (SP:214-215).

Full record per dimension (criteria 1-5, M = MET, N = NOT MET):

| Dimension | Variant | Pass 1 | Pass 2 | Final |
|---|---|---|---|---|
| Completeness | A | M M M N M | M M M M M | M M M M M |
| Completeness | B | M M M M M | N M M M M | M M M M M |
| Completeness | C | N M M M M | N M M M M | N M M M M |
| Correctness | A | N M M N M | N M M N M | N M M N M |
| Correctness | B | N M M N M | N M M N M | N M M N M |
| Correctness | C | N M N N M | N M M N M | N M N N M |
| Structure | A, B, C | M M M M M | M M M M M | M M M M M |
| Clarity | A | M M M N M | M M M N M | M M M N M |
| Clarity | B | M M M N M | M M M N M | M M M N M |
| Clarity | C | N M M N M | M M M N M | N M M N M |
| Risk Coverage | A | M M M M M | M M M M M | M M M M M |
| Risk Coverage | B | M M M N M | N M M N M | N M M N M |
| Risk Coverage | C | M M M N M | M M M N M | M M M N M |
| Invariant & Edge | A | M M M M M | M M M N M | M M M M M |
| Invariant & Edge | B | N M N M M | N M N M M | N M N M M |
| Invariant & Edge | C | M M M M M | M M M M M | M M M M M |

Pass totals: Pass 1 A 26, B 24, C 23; Pass 2 A 26, B 22, C 25; final A 27, B 23, C 23.

Disagreements and their re-evaluation:

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation reason |
|---|---|---|---|---|---|---|
| Completeness 4 (completion criteria) | A | NOT MET | MET | DISAGREE | MET | Pass 1 looked only at VA:112's "no blocking defect". Pass 2 found the stated basis right beside it: every static outcome maps to a task with a runnable AC (VA:112-113). That is a completion criterion. |
| Completeness 1 (explicit requirements) | B | MET | NOT MET | DISAGREE | MET | Pass 2 marked B down for the unexamined Task 7 environment (VB:99). That gap is a dependency question, scored under Risk 4. B's walk does map every in-scope requirement, AC-0.7 included, to a task AC (VB:74-78). |
| Correctness 3 (terminology) | C | NOT MET | MET | DISAGREE | NOT MET | Pass 2 saw severity words used consistently. But the deviation-class word "drift" is misapplied to R3-F3 (VC:50, VC:226), and C conceded it (R2c:13). Class terms are part of the focus area "deviation-classification". |
| Clarity 1 (unambiguous language) | C | NOT MET | MET | DISAGREE | NOT MET | Pass 2 read "might" (VC:211) as a stated likelihood. The criterion lists "might" by name, and C's card also says a strict reviewer "ends the run" (VC:15-17), so the card gives two readings of its own blocker (R1b:28). |
| Risk 1 (likelihood and impact) | B | MET | NOT MET | DISAGREE | NOT MET | Pass 1 counted "nothing blocks" as a likelihood. On comparison, VB:17-18 and VB:52-53 state impact (none) but never how likely the risk is; R2-2's "If the live-plan writer does not carry them" (VB:34-35) is a condition, not a likelihood. |
| Invariant 4 (count divergence) | A | MET | NOT MET | DISAGREE | MET | Pass 2 looked only at R1-F1's wording issue. R1-F2 is a count divergence: 11 required evidence lines against fewer saved files (VA:31-35). |

- Disagreements re-evaluated: 6 (of 90 criterion-variant pairs)
- Final verdicts that differ from Pass 1: 2 (Completeness 4 for A; Risk 1 for B)
- Final verdicts that differ from Pass 2: 4

## Combined Scoring
Formula (SP:188): variant_score = 0.50 × quant_score + 0.50 × qual_score.

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate diff points won (DT, Scoring Matrix) |
|---|---|---|---|---|
| A (analyzer) | 0.479 | 0.450 | **0.929** | 4 of 21 |
| B (qa) | 0.445 | 0.383 | **0.829** | 1 of 21 |
| C (refactorer) | 0.426 | 0.383 | **0.809** | 12 of 21 |

**Margin**: A over B = 0.929 − 0.829 = 0.100 (10.0 points), above the 0.05 threshold (SP:197).
**Tiebreaker applied**: No. The debate column is shown for transparency only; it would decide only if the top two were within 0.05 (SP:199).

Sensitivity check: A stays first under Pass 1 alone (qual 26/30, final 0.913) and under Pass 2 alone (26/30, final 0.913). C would pass B only under Pass 2 alone (C 0.843, B 0.812). No ordering change reaches A.

## Selected Base: Variant A (reviewer 1, analyzer)

### Selection Rationale
Variant A has the highest quantitative score (0.958) and the highest qualitative score (27/30). It leads on requirement coverage (19/20 against 14/20 and 12/20) because it is the only card that both maps all eleven static checks (VA:112-113) and files findings across Tasks 1-6 and 8. It is also the only card that met every Risk Coverage criterion, mainly because it alone checked the external Orca environment (VA:110-112). The advocates themselves proposed A's findings as the anchor of the merged should-fix list (R1a:7), and A's unique R1-F4 is the top should-fix in every Round 2 table (R2a:68, R2b:82, R2c:73).

A's weakness is decisive for the verdict but not for the base: its PASS lost the debate 3-0 (DT, X-001 and S-001), and it missed R3-F1. A base is the card the merge builds on, not the verdict it ends with. The refactor plan therefore replaces A's verdict with FAIL and adds C's blocker. C won the most diff points (12), but the debate column is a tiebreaker only, and the margin is 10 points.

### Strengths to Preserve from Base
1. R1-F4, the installed-path finding: the only check against the repo rule that installed primitives must not point at `src/superclaude/` paths (VA:67-85); unanimous should-fix, fix first (R2a:68, R2b:82, R2c:73).
2. R1-F1's concrete instance: TL:112 says "at most 10" "(as written in section 2.3)", but SRC:122 does not (VA:7-25); it leads the merged C-003 finding (R1c:43).
3. R1-F2, the Task 8 evidence-file gap (VA:26-46); unanimous should-fix (R2a:72, R2b:86, R2c:77).
4. R1-F5's deciding evidence, `scripts/build_superclaude_plugin.py:75` (VA:86-104); it absorbs B's R2-3 (R2b:15).
5. R1-F3's spec grounding on D3 (a) for the Task 6 phase slot (VA:47-66), which C called the stronger grounding (R1c:47).
6. The self-audit's environment checks: Task 7's `/opt/Orca` paths and profile value (VA:110-112), kept as a note (R2a:83, R2b:94, R2c:88).
7. The calibration block (VA:119-136), as the record behind A's calibrated confidence of 0.86.

### Base weaknesses to repair (from debate losses)

1. Verdict PASS and "I found no blocking defect" (VA:4, VA:112): replaced by FAIL with R3-F1 (lost X-001 and S-001).
2. "two tests that pin plugin core copies" (VA:95) and the `:308` citation (VA:100): corrected to one test at line 309 (R1a:47, R2a:19).
3. The routing-guide test risk judged "not a finding" (VA:110-111): replaced by R3-F6 at should-fix (R2a:21).

### Strengths to Incorporate from Non-Base Variants
1. From Variant C: the FAIL verdict and R3-F1 as the one adjudicated blocker, with its one-sentence fix (VC:4, VC:7-28; DT X-002, 90%).
2. From Variant C: the method of grading severity from the executor's rules (VC:14-16, VC:23-24; DT S-006, 95%).
3. From Variant C: R3-F5's read-only hits and path-verb-text keying, merged into the Task 6 finding (VC:91-110; DT C-001, 65%, B dissenting with blocking).
4. From Variant C: R3-F2 (VC:29-47), R3-F4 (VC:71-90) and R3-F6 with corrected citations (VC:111-127), all should-fix.
5. From Variant C: R3-F3's mechanism, merged under A's R1-F1 instance (VC:48-70; DT C-003).
6. From Variant C: the minor findings R3-F7, R3-F8, R3-F9 and R3-F11 (VC:128-169, VC:185-200), and R3-F10 merged into B's R2-2 (VC:170-184).
7. From Variant B: R2-1, the phantom AC-0.8, at minor (VB:7-23; R2b:17) and R2-2, the live-plan handoff (VB:24-41).
8. From Variant B: the halt-path inventory as the frame for the verdict rationale (VB:80-84; R1b:19).
9. From Variant B: matrix_omissions as an appendix note (VB:58-64; DT S-005) and the empty grounding hunk H4 as an evidence-gap note (VB:47-50; R2b:15).
10. From the Round 2.5 probe (no variant): INV-001, INV-002, INV-010 and INV-014 as unadjudicated items, and INV-005 and INV-007 as run conditions (INV:5, 6, 9, 11, 14, 18 of `invariant-probe.md`; see `refactor-plan.md`).
