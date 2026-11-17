# Score Pass 1: slot X-13 process-redesign-modules (order: Variant A, then Variant B)

Scorer: scorer-pass1 (forward order). Algorithm: `/home/coder/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (6 dimensions, 30 criteria, CEV, qual_score = met/30).
Variants scored as written: A = `variant-1-original.md` (Proposal A, Sweep-Sheet-shaped), B = `variant-2-original.md` (Proposal B, Recipe-Ledger-shaped). The hybrid the advocates later converged on is not scored. The debate is used only as evidence about which claims of each variant are right, wrong, overstated or missing.
Line refs "A:n" and "B:n" are line numbers in the variant files. Code facts I re-read myself (read-only): `ledger.py:3-4`, `ledger.py:172-179`, `ledger.py:464-470`, `panel.py:46`, `agents/reflect-reviewer.md:5,8`, and `ls src/superclaude/cli/swarm/recipes` (exists).

## Quantitative layer (from `quant-score.py` / `quant-score-output.json`)

| Metric | Weight | A | B |
|---|---|---|---|
| RC requirement coverage | 0.30 | 1.0000 (12/12) | 1.0000 (12/12) |
| IC internal consistency | 0.25 | 0.8148 (5 contradictions / 27 claim lines) | 0.8065 (6 / 31) |
| SR specificity | 0.15 | 1.0000 (72 concrete lines, 0 vague terms) | 1.0000 (65 concrete lines, 0 vague terms) |
| DC dependency completeness | 0.15 | 1.0000 (7/7) | 1.0000 (23/23) |
| SC section coverage | 0.15 | 0.8889 (8 H2 / max 9) | 1.0000 (9 H2) |
| **quant_score** | | **0.937037** | **0.951613** |

Debate-verified contradictions counted (full table with line refs and verifying evidence is in `quant-score.py`; the IC value moves only through this table):
- A: A-X1 `observed` "existing mechanism" for a no-finding item is hollow (A:20 vs A:110); A-X2 `ledger.py:3-4` is a status rule, not "no component edits a reviewer finding" (A:43); A-X3 precheck item-evidence flags built on `_check`, which reaches only v2 citations (A:18, A:69); A-X4 `probe` key on v1 never reaches the ledger and no host runs the module check (A:20, A:89); A-X5 "degrades by construction" leftover has no value beyond arm K (A:12, A:113).
- B: B-X1 no brief renderer exists (B:35, B:93); B-X2 `ledger.py:468` does not list a PROBLEM row without a finding (B:43); B-X3 sidecar key is the card stem, not `<slot_id>-<i>` (B:34, B:36); B-X4 no merge hook or profile layer for the overlay (B:38, B:118); B-X5 row block after findings block vs brief line 33 while the brief is called untouched (B:36, B:43, B:79); B-X6 `recipes` collides with existing `cli/swarm/recipes/` (B:34).
- Not counted (cosmetic): B:62 cites `skills/task/SKILL.md:224`, true claim at line 225.

Deviations from the stated definitions are listed in the script header (external `section N` references excluded; `E<n>` counted only in B, which has E-rows; `3.0` treated as a decimal; `Status:` and table-separator lines excluded from SR lines). SR is 1.0 for both because neither variant contains any of the protocol's vague terms (verified by grep), so SR does not separate them. The script ran twice with byte-identical JSON.

## Qualitative layer, Pass 1

### Completeness

| # | Var | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|
| C1 | A | Covers all explicit requirements from the source input | A:12 core shape; A:43 GQ-130; A:40 GQ-131; A:52 CO-24; A:55 GQ-135/G0/D1-D7; sections 2, 4, 5, 6, 7, 8 cover design, invariants, test, C-01..C-03, PR/rf-qa, objection; RC 12/12 | MET |
| C1 | B | same | B:11 position; B:34 GQ-131; B:43 CO-24; B:65 E14 (G0, D1-D7, GQ-135); B §2 table, §3, §5, §6, §7, §8; RC 12/12 | MET |
| C2 | A | Addresses edge cases and failure scenarios | A:68-73 five endangered items (byte identity, snapshot boundary, determinism, false positives, class constants); A:78 "a failing M1 is a live possibility" | MET |
| C2 | B | same | B:82-87 INV-G (shell the agent lacks), INV-I (demotion false negatives), INV-C v1 weaker, INV-H file level; B:118 compliance and exactness failure | MET |
| C3 | A | Includes dependencies and prerequisites | A:88 "depends on three of its outcomes" of C-01; A:77 "none exists yet"; A:105 "no extractor exists for any class at HEAD" | MET |
| C3 | B | same | B:24 "Depends on it" (C-02 floor, C-03 union); B:101 pre-registered by X-14's rule; B:84 C-08 transcript adapter not yet existing | MET |
| C4 | A | Defines success or completion criteria | A:78 "A is right for that class if recall reaches a floor registered before the run and beats random"; A:83 design-level wrong condition | MET |
| C4 | B | same | B:103 "B is wrong if the unrecoverable rate is above ... 10 percent"; B:104 RL must beat K by 0.04 | MET |
| C5 | A | Specifies what is out of scope | A:19 "Does not add: a per-row verdict block, demotion, promotion, a lens-to-model binding ..."; A:12 CB-2 not adopted into the core | MET |
| C5 | B | same | B §9 "What this proposal does not claim"; B:11 "A third option ... is not argued here" | MET |

Subtotal: A 5/5, B 5/5.

### Correctness

| # | Var | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|
| K1 | A | No factual errors or hallucinated claims | Debate-verified errors: A:20 "existing mechanism" for `observed` of a no-finding item (A's own advocate conceded: nothing writes `observed` but the orchestrator, `findings_v2.py:6`, `SKILL.md:345`); A:20/A:89 `probe` key on v1 (`ledger.py:172-179` copies only round, reviewer_id, fid, blocking); A:18/A:69 precheck item-evidence flags (A withdrew part (c) in round 2) | NOT MET |
| K1 | B | same | Debate-verified errors: B:35 "brief renderer" does not exist (B conceded); B:43 `ledger.py:468` lists ledger rows only (B: "My R1 citation `ledger.py:468` was wrong"); B:34 reviewer ids vs sidecar key (`cluster_cmd.py:146`, conceded); B:34 `recipes` name collision with `cli/swarm/recipes/` (conceded) | NOT MET |
| K2 | A | Technical approaches are feasible with stated constraints | Spec-review module on v1 has no host for the sheet writer or the item check (A:89 "the module's own advisory check must validate it" names no place; A concession 5, A-003 "Neither" in the debate matrix); A:18 flags in `precheck.json` endanger the byte-identity pins A itself names (A:69) | NOT MET |
| K2 | B | same | Overlay and `rowcheck` switch need a `merge_cmd.py:71-118` hook and a `ledger.py` change that INV-D protects (B conceded; B dropped overlay, profile value, slot key in round 2); brief renderer absent (B:35); demotion by flag alone is invalid in v2 when `reflect_category` is set (`findings_v2.py:161-162`, A weakness 3, never rebutted) | NOT MET |
| K3 | A | Terminology used consistently and accurately | Uses "sheet", "item", "card", "sidecar" consistently; A:12 and A:34 sidecar key `reviewer-<N>` matches `SKILL.md:345` and `cluster_cmd.py:146`; no block named "ledger" (A:93) | MET |
| K3 | B | same | B:34 and B:36 conflate reviewer ids `<slot_id>-<i>` (`panel.py:668`) with the sidecar key, which is the card stem (`cluster_cmd.py:146`); B:38 "profile" `rowcheck` names a layer that no code owns (debate: C-03 INV-003 unspecified); inaccurate terms, conceded | NOT MET |
| K4 | A | No internal contradictions (cross-validated with IC) | IC finds 5 debate-verified contradictions: A:20 vs A:110 (`observed` mechanism vs "a declaration"); A:43 quote of `ledger.py:3-4` ("status") vs the claim built on it; A:18 "additive" flags vs A:69 byte-identity endangered and `_check` v2-only | NOT MET |
| K4 | B | same | IC finds 6 debate-verified contradictions: B:36/B:43/B:79 row block after the findings block while the brief file is "untouched" (brief line 33 "end the report with the findings block"); B:118 "no behaviour in the core that a profile does not switch on" vs no host (`merge_cmd.py:71-118`); B:35 renderer | NOT MET |
| K5 | A | Claims supported by evidence or rationale within the document | Every claim is tagged; but the central GQ-130 rationale rests on `ledger.py:3-4` read as a no-edit rule (A:43; both advocates agree it is a status rule) and A:12/A:113 "degrades by construction" was withdrawn as value-free | NOT MET |
| K5 | B | same | Tagged table E1-E16, but B:43 CB-2 route rests on `ledger.py:468` (wrong list, conceded) and B:118 containment of demotion omits the round-2 recomputation `ledger.py:210-218` (B conceded demotion is unstable across rounds) | NOT MET |

Subtotal: A 1/5, B 0/5.

### Structure

| # | Var | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|
| S1 | A | Logical section ordering (prerequisites before dependents) | Order: position, design consequence, evidence, invariants, test, consistency, PR/rf-qa, objection; inline pointers (A:12 "section 5", A:20 inline C-01 reliance) keep forward references readable | MET |
| S1 | B | same | Consistency with C-01..C-03 (B §2) placed before the design (B §3); evidence E1-E16, invariants, tests, effect, objection, non-claims follow | MET |
| S2 | A | Consistent hierarchy depth, no orphaned subsections | 8 H2 sections; 3.1-3.6 only under section 3; no orphan levels | MET |
| S2 | B | same | 9 H2 sections; no subsection levels; evidence as one table | MET |
| S3 | A | Clear separation of concerns between sections | Section 3 "Evidence" carries design decisions: A:43 "Position A's answer to GQ-130 is therefore 'no demote or promote in the core'", A:52 "Position A removes the conflict by not adopting CB-2", A:40 GQ-131 answer; section 2 "Design consequence" does not hold them | NOT MET |
| S3 | B | same | Design decisions sit in §3 (core items 1-7, module bullets incl. CO-24 at B:43); §4 is a claim table only (claim, evidence, tag) | MET |
| S4 | A | Navigation aids present | Numbered subsections 3.1-3.6, "(section 5)", "(see 3.5)", tag legend at A:8 | MET |
| S4 | B | same | E1-E16 ids cross-referenced ("section 4, E5", B:19), tag legend at B:7, section refs | MET |
| S5 | A | Follows conventions of the artifact type | Proposal header with slot, status, code state, tag legend; required sections all present; "Status: Complete" at A:119 | MET |
| S5 | B | same | Same conventions (B:1-7, "Status: Complete" at B:3); extra §9 non-claims | MET |

Subtotal: A 4/5, B 5/5.

### Clarity

| # | Var | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|
| L1 | A | Unambiguous language (no "should consider", "might", "as appropriate") | grep of all protocol vague terms over the file: 0 hits | MET |
| L1 | B | same | grep: 0 hits | MET |
| L2 | A | Concrete rather than abstract | 72 concrete lines; file:line cites throughout (A:33-36); thresholds "at least 0.8 on at least 3 unused plans" (A:78) | MET |
| L2 | B | same | 65 concrete lines; test list T-B1..T-B7 (B:93-99); "0.12 x 14 = 1.68 items" (B:65) | MET |
| L3 | A | Each section has a clear purpose or one-sentence summary | Sections 1-8 each summarizable (position; core design; evidence; invariants; measurement; C-01..C-03; PR/rf-qa; objection) | MET |
| L3 | B | same | Sections 1-9 each summarizable | MET |
| L4 | A | Acronyms and domain terms defined on first use | Used without expansion: "G0 and D1-D7" (A:55), "INV-003" and "C-06" (A:88), "E1, E2, E5, E7" (A:25), "REQ-23" (A:61); defined: CB-2, MR2, arm K, M1-M5 | NOT MET |
| L4 | B | same | Used without expansion: "INV-J (S1 to S5, Medium non-blocking)" and "INV-N (mirror pins)" (B:79), "C-08" and "X-14" (B:84, B:101), "G0 and D1 to D7" (B:65); defined: tags, `r10`, `MR2`, arms Z0/K/RL/SS (B:104) | NOT MET |
| L5 | A | Actionable next steps or decision points clearly identified | M1-M5 ordered steps (A:77-83); decision unit stated: "The unit of commitment is an extractor, not the design" (A:113) | MET |
| L5 | B | same | M-B1..M-B3 (B:103-105); decision rule "the cheaper form wins" (B:104); "the answer is the switch and M-B3" (B:118) | MET |

Subtotal: A 4/5, B 4/5.

### Risk Coverage

| # | Var | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|
| R1 | A | At least 3 risks with probability and impact | A:70 snapshot boundary, 92.5 percent of recorded flags `not-in-snapshot`; A:78 blind pick hits a true line 6 to 10 percent so M1 failing is "a live possibility", impact "ships as a card ... with no extractor"; A:72 false-positive crowd-out planning values -0.90 to -0.10 of 14 | MET |
| R1 | B | same | B:118 exactness 0.914 x 0.914 = 0.835 per row, impact "can turn a real blocker into PASS"; B:103 compliance "above 10 percent" precondition, impact `rows_missing`; B:59 E8 11 of 13 sidecars with a row id assigned more than once. Weaker than A on probability but three have a rate and a consequence | MET |
| R2 | A | Mitigation strategy for each identified risk | A:68 labels the endangered list "named, not resolved here"; the false-positive item (A:72) has only measurement M4, no mitigation | NOT MET |
| R2 | B | same | B:82 labels the list "Endangered or left open"; INV-C v1 weaker check is accepted as "a cost of the C-01 outcome" (B:19, B:86) with no mitigation | NOT MET |
| R3 | A | Failure modes and recovery procedures | A:83 and A:113: if no extractor passes M1, ship the card loader and sidecar entry point; a failing class "ships as a card ... with no extractor" (A:78) | MET |
| R3 | B | same | B:85 containment (off by default, never CRITICAL, own flag, `check_skipped`); B:104 kill rule when RL does not beat K; B:36 missing block counted as `rows_missing` | MET |
| R4 | A | External dependencies and their failure scenarios | A:88 "if that outcome were reversed, `probe`, `class` and `src` would have to be registered keys in the v1 parser" | MET |
| R4 | B | same | B:24 depends on C-02 floor and C-03 union; B:84 `ran` unverifiable until the C-08 transcript adapter exists; B:87 telemetry convention only | MET |
| R5 | A | Monitoring or validation mechanism for risk detection | M1-M5 (A:77-82): byte-identity over two runs, runtime against the kill limit, found-at-any and found-at-blocking reported separately | MET |
| R5 | B | same | T-B1..T-B7 (B:93-99) incl. T-B6 telemetry leak test; M-B1..M-B3 (B:103-105) | MET |

Subtotal: A 4/5, B 4/5.

### Invariant & Edge Case Coverage

| # | Var | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|
| I1 | A | Boundary conditions for collections (empty, single, maximum) | A:61 "With no cards declared, the sheet step produces nothing"; A:33 "an empty block is complete only when the assigned rows are non-empty and all observed (`findings_v2.py:292`)"; A:78 "at-most-12 selection" | MET |
| I1 | B | same | B:36 "an empty findings block is complete only when every assigned row is observed (`findings_v2.py:291-298`)"; B:35 "A slot with no `recipes` gets a byte-identical brief" (no maximum bound stated) | MET |
| I2 | A | State variable interactions across component boundaries | A:17 sidecar written as `panel/coverage.json` and read by `cluster --coverage` and `verify-citations --coverage`; A:92 sheets exist on first review only, re-review quorum rows have no sheet | MET |
| I2 | B | same | B:36 `observed` computed in the v2 parser, advisory in v1; B:22 recipes first review only vs `prior` lines; B:36 sidecar feeds `cluster` and `verify-citations` | MET |
| I3 | A | Guard condition gaps (missing validation, unguarded type assumptions) | A:89 "on v1 the item link is an unvalidated key; the module's own advisory check must validate it against the sheet, because the core would not"; A:36 unknown keys parse in both engines | MET |
| I3 | B | same | B:36 "In the v1 parser there is no coverage rule"; B:37 a `quote_other` printed tool line "cannot be checked by a file read", so `check_skipped`; B:21 demotion never on CRITICAL | MET |
| I4 | A | Count divergence scenarios | A:98 reviewer lost after assignment leaves items unexamined, `observed` shows it, and it does not feed C-03's `min(2, requested)` floor; A:55 D2 arithmetic 0.12 x 14 = 1.68 vs +1.33 items | MET |
| I4 | B | same | B:36 assigned rows vs observed rows (`rows_missing`, `block_ok` false when the block is skipped); B:65 D2 1.68 items vs +1.33 and +1.05; no line-base off-by-one scenario in either variant | MET |
| I5 | A | Interaction effects when features combine | A:97 promotion or demotion would change the input C-03's union runs over (INV-006); A:98 replica assignment is not a quorum | MET |
| I5 | B | same | B:24 demotion lowers one flag but the union keeps another reviewer's flag (`ledger.py:187`); B:21 demotion bounded by the C-02 CRITICAL floor | MET |

Subtotal: A 5/5, B 5/5.

## Qualitative summary

| Dimension | A | B |
|---|---|---|
| Completeness | 5/5 | 5/5 |
| Correctness | 1/5 | 0/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **Total met** | **23/30** | **23/30** |
| **qual_score** | **0.7667** | **0.7667** |

Edge Case Floor (>= 1/5 on Invariant & Edge Case Coverage): A 5/5 eligible, B 5/5 eligible.

Informational pass-1 combination (final combination waits for pass 2): A = 0.5 x 0.937037 + 0.5 x 0.7667 = 0.8519; B = 0.5 x 0.951613 + 0.5 x 0.7667 = 0.8592; margin 0.0073, inside the 5 percent tiebreaker band, so debate performance decides at the combine step.

Scoring notes for the combiner:
- Correctness is where the two differ: A has the one MET (terminology, `reviewer-<N>` sidecar key is accurate); B conflates reviewer-id spaces. Both lose K1, K2, K4, K5 on debate-verified errors. B's verified errors are more numerous (6 vs 5), and B's own concessions cover the overlay, renderer, slot key and CB-2 route, the pieces its position was built on; A's verified errors sit mostly in the item-answer carrier and the precheck flags.
- Structure favours B on separation of concerns (A:43, A:52 put design answers in the evidence section).
- Neither variant's text mentions line-base (inclusive/exclusive) off-by-one; I4 is MET on the assigned/observed/requested count scenarios only.

```yaml
pass: 1
order: [A, B]
completeness.1: {A: MET, B: MET}
completeness.2: {A: MET, B: MET}
completeness.3: {A: MET, B: MET}
completeness.4: {A: MET, B: MET}
completeness.5: {A: MET, B: MET}
correctness.1: {A: NOT MET, B: NOT MET}
correctness.2: {A: NOT MET, B: NOT MET}
correctness.3: {A: MET, B: NOT MET}
correctness.4: {A: NOT MET, B: NOT MET}
correctness.5: {A: NOT MET, B: NOT MET}
structure.1: {A: MET, B: MET}
structure.2: {A: MET, B: MET}
structure.3: {A: NOT MET, B: MET}
structure.4: {A: MET, B: MET}
structure.5: {A: MET, B: MET}
clarity.1: {A: MET, B: MET}
clarity.2: {A: MET, B: MET}
clarity.3: {A: MET, B: MET}
clarity.4: {A: NOT MET, B: NOT MET}
clarity.5: {A: MET, B: MET}
risk.1: {A: MET, B: MET}
risk.2: {A: NOT MET, B: NOT MET}
risk.3: {A: MET, B: MET}
risk.4: {A: MET, B: MET}
risk.5: {A: MET, B: MET}
invariant.1: {A: MET, B: MET}
invariant.2: {A: MET, B: MET}
invariant.3: {A: MET, B: MET}
invariant.4: {A: MET, B: MET}
invariant.5: {A: MET, B: MET}
totals: {A: 23, B: 23}
qual_score: {A: 0.7667, B: 0.7667}
edge_case_floor: {A: eligible, B: eligible}
quant_score: {A: 0.937037, B: 0.951613}
```

Status: Complete
