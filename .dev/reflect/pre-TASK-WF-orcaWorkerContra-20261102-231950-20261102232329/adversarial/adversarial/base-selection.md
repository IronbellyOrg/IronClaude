# Base Selection Report

## Quantitative Scoring (50% weight)
Generated 2026-11-03T00:39:08Z by the debate-orchestrator. Variants: A = `variant-1-original.md` (analyzer), B = `variant-2-original.md` (qa), C = `variant-3-original.md` (refactorer). Cite keys as in `debate-transcript.md` (`A:N`, `B:N`, `C:N`, `TL:N`, `SRC:N`, `R1-A:N`, `R2-B:N`, `diff:N`). Formulas: `refs/scoring-protocol.md` A.1-A.4. All counts below came from one read-only grep script run on the three variant files on 2026-11-03; every line cite was opened.

| Metric | Weight | Variant A (analyzer) | Variant B (qa) | Variant C (refactorer) |
|--------|--------|-------------------|-------------------|-----|
| requirement_coverage | 0.30 | 0.593 (16/27) | 0.667 (18/27) | 0.630 (17/27) |
| internal_consistency | 0.25 | 0.966 (1 contradiction / 29 claims) | 0.968 (1 / 31) | 0.957 (2 / 46) |
| specificity_ratio | 0.15 | 0.980 (96 concrete / 98) | 0.985 (129 / 131) | 0.954 (124 / 130) |
| dependency_completeness | 0.15 | 1.000 (5/5 refs resolve) | 1.000 (6/6) | 1.000 (3/3) |
| section_coverage | 0.15 | 0.909 (10/11 top-level keys) | 1.000 (11/11) | 0.909 (10/11) |
| **quant_score** | | **0.852** | **0.890** | **0.857** |

Computation: quant = RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15.
- A: 0.1778 + 0.2414 + 0.1469 + 0.1500 + 0.1364 = 0.8525
- B: 0.2000 + 0.2419 + 0.1477 + 0.1500 + 0.1500 = 0.8896
- C: 0.1889 + 0.2391 + 0.1431 + 0.1500 + 0.1364 = 0.8575

### Requirement coverage detail

Source requirements (the spec has no FR-/NFR- ids, so the P0 acceptance checks and the requirement ids are the universe): 14 P0 acceptance checks, AC-C1 to AC-C6 (SRC:244-276) and AC-0.1 to AC-0.7 plus AC-0.9 (SRC:298-305; the spec has no AC-0.8, B:229), and 13 requirement ids, WC-1 to WC-13 (SRC:69-81). Total 27. Match rule: case-insensitive whole-word grep of the id in the card (so `WC-1` does not match `WC-10`, and `ac-0.4-smoke.md` counts as AC-0.4).

| Card | Matched | Not matched |
|---|---|---|
| A | AC-C1, AC-C2, AC-C4, AC-C5, AC-C6, AC-0.1, AC-0.2, AC-0.4, AC-0.5, AC-0.6, AC-0.7, AC-0.9, WC-1, WC-9, WC-10, WC-13 (16) | AC-C3, AC-0.3, WC-2 to WC-8, WC-11, WC-12 (11) |
| B | AC-C1 to AC-C6, AC-0.1, AC-0.4, AC-0.6, AC-0.7, AC-0.9, WC-3, WC-4, WC-5, WC-7, WC-9, WC-10, WC-13 (18) | AC-0.2, AC-0.3, AC-0.5, WC-1, WC-2, WC-6, WC-8, WC-11, WC-12 (9) |
| C | AC-C1 to AC-C5, AC-0.4, AC-0.6, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9, WC-10, WC-12, WC-13 (17) | AC-C6, AC-0.1, AC-0.2, AC-0.3, AC-0.5, AC-0.7, AC-0.9, WC-1, WC-8, WC-11 (10) |

No card names AC-0.3, WC-8 or WC-11.

### Internal consistency detail

Scorable claims = 3 per finding (claim, severity, class) + 1 per agreement, disagreement or matrix-omission bullet. A: 8×3 + 3 + 2 = 29. B: 6×3 + 5 + 2 + 6 = 31. C: 14×3 + 2 + 2 = 46.

Contradictions found:
- A (1): F1 says "Task 4's acceptance criterion cannot pass at the point Task 4 runs" (A:11), then "or the order depends on task numbering, which the plan does not state" (A:16-17).
- B (1): R2-2 is minor because TL:122 delegates to spec 7.2 (B:46-49), while R2-1, from the same delegated step, is blocking (B:10-23); this is X-003 (diff:59).
- C (2): R3-F2 is graded blocking (C:28) and the card's calibration says "no (downgrade to minor)" (C:285); R3-F1 says "The step order and the acceptance criterion cannot both be met" (C:15-16, repeated C:280) and the calibration says "'AC cannot pass' overstated, artifact can be written after the commit" (C:285).

### Specificity detail

Line-based count over body text, excluding metadata lines, evidence path lines and bare key lines. Concrete = a line with a number, a backtick, a quoted string or a file name. Vague = a line with appropriate, as needed, properly, adequate, should consider, might, various, etc., best practices, may, could or possibly. Vague lines: A:82, A:104; B:50, B:125; C:34, C:70, C:189, C:237, C:279, C:280.

### Dependency completeness detail

Internal references are card-local finding ids used outside their own entry. A: F1, F3, F8, F1, F7 (A:178, :181, :183, :189, :193), all defined. B: R2-3, R2-1, R2-2, R2-4, R2-2, R2-4 (B:191, :192, :193, :196, :202, :209), all defined. C: R3-F9, R3-F13, R3-F1 (C:249, :252, :263), all defined. References to the T1 card, the coverage matrix and repo files are external and excluded.

### Section coverage detail

Top-level keys (the cards are YAML, so a top-level key is a section). A: reviewer, persona, model_class, verdict, self_confidence, findings, agreements_with_t1_card, disagreements_with_t1_card, self_audit, calibration (A:1-6, :175, :184, :194, :206) = 10. B: the same ten plus `matrix_omissions` (B:155) = 11. C: the same ten as A (C:1-6, :244, :253, :266, :281) = 10. Max = 11.

## Qualitative Scoring (50% weight) — Additive Binary Rubric
Each cell is one Claim-Evidence-Verdict record: the CLAIM is the criterion for that variant, the EVIDENCE is the cited line (or the sections searched), and the VERDICT is MET (1) or NOT MET (0). A MET verdict without a cite defaults to NOT MET (`refs/scoring-protocol.md` A.2). Verdicts shown are final, after the dual pass and re-evaluation (next section).

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Covers all explicit requirements | NOT MET | A concedes no finding on rule substance, U-007, U-008, U-009, U-010 or U-011 (R1-A:46) | NOT MET | B concedes the narrowest coverage of the three (R1-B:45) | NOT MET | C misses A's U-002 and F2 (R1-C:11, R1-C:50); no card catches A-008 (diff:102) |
| Addresses edge cases/failures | MET | F3: a QA retry after the commit halts `head-moved` (A:58-61) | MET | R2-2: the AC-0.6 "no" branch (B:42-52) | MET | R3-F8: a leftover scratch skill breaks verify-sync (C:140-141) |
| Includes dependencies/prerequisites | MET | F1 traces the Depends-on closure of Tasks 4 and 7 (A:11-20) | MET | R2-4 lists the Depends-on gaps (B:84-92) | MET | R3-F4 and R3-F5 (C:69-71, C:86-89) |
| Defines success/completion criteria | MET | F7: one P0 report that "states pass or fail" (A:151-153) | MET | R2-4: final task that re-runs the common checks (B:107-110) | MET | R3-F11: `p0-phase-report.md` with "one PASS or FAIL line per check" (C:201-203) |
| Specifies out-of-scope items | MET | "The P0-only deferral is legitimate under source.md:216 and :238" (A:200-201) | MET | "P0-only scope is an authorized limit, not drift" (B:188-190) | MET | "P0 edits no command files, so item 8 does not apply in P0" (C:256-257) |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| No factual errors or hallucinated claims | NOT MET | F8(a) quotes "at any depth setting" as Task 8 text; it is WC-13 text (A:210; SRC:81) | NOT MET | R2-3 cites TL:17 for text at TL:20 (B:243) | NOT MET | "the four `guard refused:` texts" (C:166); SRC:60 gives three |
| Technical approaches feasible | MET | F5's tmp_path monkeypatch (A:112-113) and F2's three-texts wording (A:52-53) can both be done | NOT MET | The Tier-2 run (B:33-34) is Agent-tool time that SRC:291 excludes, and the vacuous fallback (B:35-37) is what SRC:291 forbids (R2-B:17-18) | NOT MET | R3-F9 asks the test to pin a case-3 string the spec never defines (C:166; SRC:60; R1-C:50) |
| Terminology consistent and accurate | NOT MET | `regression` for F1 (A:9) and `none` for F6 (A:116), both conceded (R1-A:45, :48) | MET | drift and none used as the debate later agreed (R1-C:52 accepts B's `none`) | NOT MET | `regression` for R3-F6 (C:102) and `drift` for a stale cite (C:206), both conceded (R1-C:52-53) |
| No internal contradictions | NOT MET | A:11 against A:16-17 | NOT MET | B:10-23 against B:46-49 (X-003) | NOT MET | C:28 and C:15-16 against C:285 |
| Claims supported by evidence | MET | every finding has an evidence list, e.g. A:21-28 | MET | e.g. B:24-30 | MET | e.g. C:18-21 |
| **Subtotal** | **2/5** | | **2/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Logical section ordering | MET | blocking F1 first (A:7-8) | MET | blocking R2-1 first (B:7-8) | MET | blocking R3-F1, R3-F2 first (C:7-8, C:27-28) |
| Consistent hierarchy depth | MET | every finding has id, severity, class, claim, evidence, recommendation (A:7-32) | MET | same shape (B:7-37) | MET | same shape (C:7-26) |
| Clear separation of concerns | NOT MET | F8 bundles three unrelated issues (A:157-164); F7 bundles four (A:137-143; diff:20) | MET | phase-end checks split into R2-3 and R2-4 (B:63-110) | MET | finest split of the three (diff:20) |
| Navigation aids | MET | cross-references such as "(F1)" (A:178) | MET | "(my R2-3)" (B:191) | MET | "See R3-F13" (C:252) |
| Follows artifact conventions | MET | reviewer-card keys present (A:1-6, :194, :206) | MET | (B:1-6, :210, :238) | MET | (C:1-6, :266, :281) |
| **Subtotal** | **4/5** | | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Unambiguous language | MET | no "should consider", "might" or "as appropriate"; "may" (A:82, :104) describes a defect, not an instruction | MET | B:125 "properly enumerated" is a verified judgment, not a hedge | MET | "could" (C:34, :70, :237) states failure paths, not hedged instructions |
| Concrete rather than abstract | MET | names tasks and lines to change (A:30-32) | MET | names the artifact and the re-run (B:60-62) | MET | lists exact paths (C:77-81) |
| Each section has a clear purpose | MET | each finding opens with one claim sentence (A:11) | MET | (B:11-13) | MET | "Task 7 contradicts itself." (C:11) |
| Terms defined on first use | NOT MET | "D5" (A:159) and "T1" (A:164) undefined | NOT MET | "TL:122" (B:14) uses an undefined cite key | NOT MET | "SA-5" (C:123) undefined |
| Actionable next steps | MET | a recommendation on every finding (A:29-32) | MET | (B:31-37) | MET | (C:22-26) |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| At least 3 risks with probability and impact | NOT MET | severity gives impact only; no likelihood on any finding (searched A:7-174) | NOT MET | one likelihood statement only, "Residual risk is low" (B:93-94) | NOT MET | none (searched C:6-243) |
| Mitigation for each risk | MET | 8 of 8 findings carry a recommendation (A:29, :51, :71, :92, :111, :130, :150, :171) | MET | 6 of 6 (B:31, :59, :77, :106, :134, :152) | MET | 14 of 14 (e.g. C:22, :41, :60, :76) |
| Failure modes and recovery | MET | head-moved halt "needs a person's Ruling" (A:59-60) | MET | fallback to `--source terminal` (B:60-62) | MET | re-run AC-C1, AC-C2 after Task 6 (C:150-152) |
| External dependencies and failures | MET | Orca install layout unverified (A:202-204) | MET | Orca transcript may not name tool calls (B:49-52) | MET | `--report-dir` unknown to every command until P1 (C:172-176) |
| Monitoring or validation mechanism | MET | record `git ls-remote` before and after (A:172-173) | MET | record AC-C5 as run with an empty edit set (B:78-79) | MET | PASS or FAIL line per check (C:201-203) |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Collection boundaries (empty, single, max) | MET | empty AC-0.9 class: "no hit can carry that mark" (A:118-120) | MET | empty edit set makes AC-C5 vacuous (B:68-70) | MET | "At P0 nothing is refused" (C:220-221) |
| State interactions across components | MET | HEAD against `q0-head` (A:58-60) | MET | AC-C3 comparison against the HOW-WE-WORK.md edit (B:89-91) | MET | KNOWN_CORE_FILES against `list_core_files()` (C:86-89) |
| Guard condition gaps | MET | three guard texts, not four (A:37-43) | MET | unguarded AC-0.6 branch (B:45-52) | MET | `--only` drops a staged `.dev/tasks` (C:67-69) |
| Count divergence | MET | three against four texts (A:37-40) | MET | lines 13-25 against 13-27 (B:143-144) | MET | 13-25 against 13-27 (C:208-209) |
| Interaction effects | MET | commit against the retry ladder (A:58-61) | MET | dependency graph against common checks (B:84-92) | MET | Task 1's AC against Task 2's content (C:48-53) |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Completeness | 4/5 | 4/5 | 4/5 |
| Correctness | 2/5 | 2/5 | 1/5 |
| Structure | 4/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 | 4/5 |
| Invariant & Edge Case | 5/5 | 5/5 | 5/5 |
| **qual_score** | **23/30 = 0.767** | **24/30 = 0.800** | **23/30 = 0.767** |

### Edge Case Floor Check

Floor: at least 1/5 on Invariant & Edge Case Coverage (`refs/scoring-protocol.md` A.2).

| Variant | Score | Eligible as base |
|---|---|---|
| A | 5/5 | yes |
| B | 5/5 | yes |
| C | 5/5 | yes |

The floor is not suspended. No variant is excluded.

## Position-Bias Mitigation
Pass 1 scored the variants in input order (A, B, C). Pass 2 scored them in reverse order (C, B, A), as an independent pass. Both passes were done by the orchestrator. Of 90 criterion-variant pairs, 84 agreed. The 6 disagreements were re-evaluated with both passes' evidence side by side, and the re-evaluation verdict is final (`refs/scoring-protocol.md` A.5).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Completeness 1: covers all explicit requirements | A | MET (self-audit maps every P0 row, A:198-201) | NOT MET (A's own coverage concessions, R1-A:46) | DISAGREE | NOT MET: mapping rows is not covering them; the debate shows six real gaps |
| Completeness 5: out-of-scope items | C | NOT MET (no P1-P4 deferral sentence) | MET (C:256-257 excludes item 8 from P0) | DISAGREE | MET: C:256-257 is an explicit out-of-scope statement |
| Correctness 2: feasible approaches | C | MET (most recommendations are one-line edits) | NOT MET (R3-F9 pins an undefined string, C:166) | DISAGREE | NOT MET: one recommendation forces the executor to invent spec text (SRC:60; R1-C:50) |
| Structure 3: separation of concerns | A | NOT MET (F8 bundles three issues, A:157-164) | MET (top-level blocks are cleanly separate) | DISAGREE | NOT MET: the criterion applies to the findings, and F7 and F8 mix unrelated defects (diff:20) |
| Clarity 1: unambiguous language | B | MET (none of the named phrases) | NOT MET ("properly", B:125) | DISAGREE | MET: B:125 is a verified judgment about the plan, not a hedged instruction |
| Clarity 1: unambiguous language | C | MET (none of the named phrases) | NOT MET (six "could"/"may" lines) | DISAGREE | MET: the "could" lines (C:34, :70, :237) describe failure paths, which a risk finding must do |

Pass totals: Pass 1 gave A 23, B 24, C 24. Pass 2 gave A 23, B 23, C 23. Final: A 23, B 24, C 23.

Disagreements re-evaluated: 6
Final verdicts changed relative to Pass 1: 3 (A Completeness 1, C Completeness 5, C Correctness 2)

## Combined Scoring
| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (analyzer) | 0.4262 | 0.3833 | **0.810** | 5 of 26 points won (19.2%) |
| B (qa) | 0.4448 | 0.4000 | **0.845** | 6 of 26 points won (23.1%) |
| C (refactorer) | 0.4287 | 0.3833 | **0.812** | 13 of 26 points won (50.0%) |

**Margin**: B 0.845 against C 0.812 = 0.033 (3.3%), below the 5% threshold. A is 0.035 below B, also within 5%, but the tiebreaker compares the top two.
**Tiebreaker applied**: Yes, level 1 (debate performance; `refs/scoring-protocol.md` A.4). Points won come from the Step 2 scoring matrix (`debate-transcript.md`, "Debate points won"): C 13, B 6. C's 50.0% against B's 23.1% is not within 5%, so level 1 decides and levels 2-3 are not needed.
**Result**: Variant C is selected.

## Selected Base: Variant C (default model:refactorer)
### Selection Rationale

B has the highest combined score (0.845) on the strength of its section count (`matrix_omissions`) and its higher requirement coverage. But it leads C by only 3.3%, so the tiebreaker applies, and C won 13 of 26 debate points against B's 6. The debate outcome also fits C as the merge base for a finding list. The single blocking finding the debate settled on is built on C's R3-F1 (R2-C:95, R2-B:99, R2-A:101). The merged list follows C's split (R3-F5 as the dependency residual, R3-F14 apart from the cadence run; R2-A:104, R2-B:105, R2-C:100). Most surviving minors are C-only findings (U-007 to U-011; R2-C:73). C's weaknesses are wrong text, not wrong structure: the "four texts" in R3-F9 (C:166), two class labels (C:102, C:206) and two severities that its own calibrator overturned (C:285). Each one is a local replacement.

### Strengths to Preserve from Base

1. R3-F1 (C:7-26): the Task 7 order conflict, the core of the one adjudicated blocking finding. Keep it, re-based on the "Then ... run it" against "commit last" clash (R2-C:49).
2. R3-F4's explicit P0 path list with `.dev/tasks` named in the `--only` pathspec (C:77-81; U-008).
3. R3-F3 (C:47-62): the TL:21/TL:42 file-wide rule against Task 2's content, graded should-fix (top) after the debate (R2-C:96).
4. R3-F5 (C:85-99): the red `tests/cli` window from Task 1 to Task 3, the surviving form of C-001 (R2-C:100).
5. The C-only minors: R3-F6 (C:100-116), R3-F7 (C:117-132), R3-F10 (C:168-184), R3-F13's `gh api` patterns (C:229-230), R3-F14 (C:231-243).
6. R3-F11's closing task and file name `artifacts/p0-phase-report.md` (C:200-203).
7. C's calibration notes (C:285), every one of which the debate adopted.

### Strengths to Incorporate from Non-Base Variants

1. From Variant A, F3 (A:54-74): the `head-moved` halt after the commit (retry.md:41, :44), merged into the Task 7 finding as its consequence (R2-A:101).
2. From Variant A, F2 (A:33-53): three exact refusal texts plus the case-3 prefix, replacing C's "four" in R3-F9 and added as its own should-fix (X-004; R2-C:98).
3. From Variant A, F6 (A:130-133): state that WC-9's no-git-state claim covers only classified hits; merge into R3-F13 with class drift (R2-A:14).
4. From Variant A, F8 parts (b) and (c) (A:161-164, A:172-174): the `git ls-remote` check and the person-opened coordinator line; part (a) dropped (R2-A:15).
5. From Variant A, the `necessary` class for the commit itself (A:56; R2-C:101).
6. From Variant B, R2-5's phrase list (B:134-138), replacing R3-F9's examples (R2-B:104).
7. From Variant B, R2-6's class `none` for the stale cite (B:141), replacing R3-F12's `drift` (R1-C:52).
8. From Variant B, R2-3's AC-C5 record (B:77-79) and R2-4's phase-end re-run of the AC-C3 comparison (B:107-110), merged into R3-F11 (R2-B:103).
9. From Variant B, the L3 staging point behind A-008 (B:179-182): a recorded closing `git add .dev/tasks` in R3-F11 (R2-B:92).
10. From Variant B, R2-1's tie to the plan Goal at TL:15 (B:19-20), added to the cadence finding's evidence.
