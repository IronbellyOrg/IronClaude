# Base Selection Report

Variants: Variant A = Proposal A (`variant-1-original.md`), Variant B = Proposal B (`variant-2-original.md`). Both are default model, default persona advocates' source positions; Mode A. Quantitative layer: `quant-score.py` / `quant-score-output.json` (deterministic; `uv run python`). Qualitative layer: two independent position-bias passes (`score-pass1.md`: A then B; `score-pass2.md`: B then A) and one re-evaluation (`score-reeval.md`).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (Proposal A) | Variant B (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 0.7692 (10/13; matched 10 of 13 requirements (ids 6, phrases 4)) | 1.0000 (13/13; matched 13 of 13 requirements (ids 9, phrases 4)) |
| internal_consistency | 0.25 | 0.9906 (105/106; total_claims=106 (units with a file:line citation or a standalone number, vague-phrase units excluded); intra-variant contradictions=1 ['X-007'] from ) | 1.0000 (62/62; total_claims=62 (units with a file:line citation or a standalone number, vague-phrase units excluded); intra-variant contradictions=0 [] from diff-ana) |
| specificity_ratio | 0.15 | 1.0000 (142/142; concrete units=142 (number, file:line, path, code identifier or named id), vague units=0; a unit can count in both) | 1.0000 (110/110; concrete units=110 (number, file:line, path, code identifier or named id), vague units=0; a unit can count in both) |
| dependency_completeness | 0.15 | 1.0000 (13/13; internal references=13, resolved=13, external excluded=14; heading numbers present=['0', '1', '2', '3', '3.1', '3.2', '3.3', '3.4', '3.5', '4', '4.1',) | 1.0000 (9/9; internal references=9, resolved=9, external excluded=10; heading numbers present=['1', '2', '3', '3.1', '3.2', '3.3', '3.4', '4', '5', '6', '7', '8', ) |
| section_coverage | 0.15 | 1.0000 (9/9; H2 count 9 / max H2 count 9) | 1.0000 (9/9; H2 count 9 / max H2 count 9) |
| **quant_score** | | **0.9284** | **1.0000** |

Notes: RC uses the ids and phrases of row C-11 (CO-30, CO-31, FX-8, FX-20, INV-G, INV-J, INV-N, INV-K, GQ-181 plus four decided-fact phrases); Variant A names INV-G but not INV-J, INV-N, INV-K (descriptive invariant names instead), which is the whole RC gap (10/13 against 13/13). IC counts one intra-variant contradiction for A (X-007, templates 8 versus 9) and none for B. SR is 1.0 for both (no vague-phrase unit in either). The quantitative layer favours Variant B.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Final verdicts after position-bias mitigation. Evidence is the passes' CEV evidence (where the passes agree the evidence shown is Pass 1's; the full CEV text of every criterion is in `score-pass1.md` and `score-pass2.md`).

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| 1. Covers all explicit requirements | MET | Decided facts A:6, C-01..C-03 section 0, two eight-lens sets A:35 (CO-32), owner Q2/Q3/Q5 A:152, invariants section 4, measurement section 5, PR/rf-qa section 6, objection section 7. | NOT MET | Two different 'eight lens' sets and owner question Q5 not addressed; searched B for 'eight', 'CO-32', 'Q5': only B:30/B:32 mention the /task gate's eight lens names. |
| 2. Addresses edge cases/failures | MET | M3 A:117 truth table 'including the 95 boundary, UNCHECKED above zero, and TOTAL equal to UNVERIFIABLE'; failure scenarios in 4.2 table A:102-107. | MET | Failure scenarios: INV-J 'the pins fail loudly' B:78, INV-K 'caught by verify-sync' B:79; edge case 'fallback if no document type has a usable seeded-defect set' B:109. |
| 3. Includes dependencies/prerequisites | MET | Section 8 'Open items this proposal depends on' A:147-153: C-01 T-a, C-02 Q/INV-011/INV-003, C-03 INV-003, owner Q2/Q5. | MET | B:59 'Dependencies on them: C-01 (...), C-02 (...), C-03 (...)'; ordered prerequisites (a)-(f) for the later gate replacement B:96. |
| 4. Defines success/completion criteria | MET | A:123 'shown RIGHT if ... arm 1 is not worse than arm 0 on recall and wrong blockers, mutates nothing ...; shown WRONG if ...'. | MET | B:84 rule fixed before audit: zero writes outside own report supports, one write to a reviewed output file shows B-3 wrong; M-B3 static check B:88. |
| 5. Specifies out-of-scope items | MET | A:22 'The first change does not touch the seven skills' spawn lines, the rf-qa and rf-qa-qualitative agent files, ... pr_submit, or anything under cli/reflect'; A:39 unchanged list. | MET | B:21 'Untouched in the first change: rf-qa.md, rf-qa-qualitative.md, rf-analyst.md; task/SKILL.md ...; pr_submit/; everything under cli/reflect/'; B:15 'does not need' list. |
| **Subtotal** | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| 6. No factual errors or hallucinated claims | NOT MET | Code-contradicted, conceded: A:115 lists 9 templates, Glob finds 8 (X-007); 'the one place'/'every lens reviewer of every phase gate' (X-001); M1 mode check guards ignored control (X-004). | NOT MET | Code-contradicted, conceded: B:16 'schema change over all 8 packaged templates and their validate tests' (X-002); B:28 new agent 'must be installed' per test_cli_install.py (A-006). |
| 7. Approaches feasible with stated constraints | MET | Constraints stated and respected: panel 1..8 vs floors, 'One template therefore covers the two lowest tiers' A:80; one ledger per document A:81; Half 2 doc-only A:139; X-003 Half 1 needs no panel code. | NOT MET | Doc-gate module B:20 has no host while B:21/B:88 keep all skills byte-identical; A-R1 weakness 3; B conceded 'not literally touches no existing file' and 'module leaves the first change' (B-R2). |
| 8. Terminology consistent and accurate | MET | A:35 'the three meanings of lens in this repo (v2 finding field, swarm LensEntry, /task QA dimension) stay separate'; severity mapping stated A:36. | MET | B:63 'Definitions are those of synth-06-conflict-log.md 6.12.0 (INV-A to INV-N)'; clause labels B-1..B-3 defined B:10 and reused consistently B:28-49, B:84-90. |
| 9. No internal contradictions | NOT MET | A:28 counts 8 packaged templates ('default ... the seven reflect-* / live7 files') but A:115 lists 'default, live7, the seven reflect files' (9) (diff X-007, intra-variant). | MET | No contradiction found in sections 1-9: B-3 (B:10) is conditional on M-B1 (B:84, B:105); 'No new core feature' B:15 and the new module profile B:20 are different layers. |
| 10. Claims supported by evidence or rationale | MET | Claim/evidence/tag table E1-E9 with file:line citations and CODE-VERIFIED/UNVERIFIED tags (A:45-55). | MET | Inline file:line evidence with tags, e.g. B:37 'fix_authorization: false occurs 93 times in 8 files ... [CODE-VERIFIED]'; separate 'What I did not verify' list B:111-118. |
| **Subtotal** | **3/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| 11. Logical section ordering | MET | Section 0 consistency check precedes position (1) and design (2); debate S-001 adopted A's order. | MET | Position, design, evidence, consistency, invariants, measurement, effect, objection, not-verified; every later section builds on clauses B-1..B-3 defined in section 1 (B:10). |
| 12. Consistent hierarchy depth | MET | H2 sections 0-8; H3 only under section 3 (3.1-3.5) and section 4 (4.1-4.2); no orphan subsection. | MET | H2 sections 1-9; H3 only under section 3 (3.1-3.4); no orphan subsection. |
| 13. Clear separation of concerns | NOT MET | Position decomposition (Half 1/Half 2) appears only inside the objection answer A:139 (diff S-002, debate outcome B 93%); section 8 mixes dependencies with not-verified items (S-001). | MET | Evidence keyed per clause ('3.1 B-3', '3.2 B-1', '3.3 B-2'); measurements name the clause decided (B:84, B:86); separate not-verified section B:111 (debate S-002 outcome B). |
| 14. Navigation aids present | MET | Numbered sections with cross-references: '(section 0)', 'the oracle (section 5)' A:137, evidence ids E1-E4 cited from section 7. | MET | Cross-references: 'the falsifier M-B1 in section 6' B:77, 'the cost is stated in section 7' B:107, '(section 3.1 item 6)' B:105. |
| 15. Follows artifact-type conventions | MET | Status line A:3/A:155, slot and conflict header A:5-6, tag legend A:7, position, evidence, invariants, measurement, objection and answer. | MET | Status line B:3/B:120, slot and conflict header with HEAD B:5, tag legend B:6, position, evidence, invariants keyed to the row's INV ids, measurement, objection. |
| **Subtotal** | **4/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| 16. Unambiguous language | MET | Grep: no 'might', 'should consider', 'as appropriate'; the 'may' hits are a gate-text quote (A:38) or tagged uncertainty (A:107 [UNVERIFIED], A:151). | MET | P1 (MET): Grep: no 'might', 'should consider', 'as appropriate'; hits are a gate-text quote (B:29), a tagged untested question (B:53) and a quote in the objection (B:102). / P2 (NOT MET): Core target left open: 'for example PRD, TDD, technical reference or README' and B-2's 'weaker alternative ... a skill's spawn sites' (B:10); B:116 leaves the document type undecided. / re-evaluation: score-reeval.md |
| 17. Concrete rather than abstract | MET | A:28 '_SLOT_KEYS (panel.py:46) gains an optional lens'; slot ids tmpl, consist, evid, compl A:35; planted defects per lens A:121. | MET | B:88 'git diff --stat ... shows no edits to src/superclaude/agents/rf-qa*.md ...; uv run pytest tests/skills/test_review_severity_rule.py ... -q passes'. |
| 18. Each section has a clear purpose | MET | Headings state purpose: 'The test or measurement that would show position A right or wrong', 'The strongest objection and the answer'; section 1 '(one paragraph)'. | MET | Headings state purpose ('The position in one paragraph', 'What I did not verify'); evidence subsections name the clause they support. |
| 19. Acronyms and terms defined on first use | NOT MET | Undefined on first use: 'owner question Q3 / GQ-181' A:22, 'MDTM task' A:102, 'the E2 harness' A:69, 'S1-S3 severity text' A:64; T-a used at A:15 before description. | NOT MET | r13, GQ-n (B:6) and T-a/T-b (B:53) defined, but 'M5 of r13 section 8', '(M9)', '(R3)' B:15, 'MDTM task' B:31 and 'S1-S3 cap text' B:10 used undefined. |
| 20. Actionable next steps / decision points | MET | A:111 'Built first, before any /task text changes' with ordered M1-M5; decision points listed in section 8 A:147-153. | MET | M-B1 'run before the first change' with fixed rule B:84; prerequisites (a)-(f) incl. '(b) the owner answers GQ-181 (Q3) and Q2' B:96. |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| 21. At least 3 risks with probability and impact | NOT MET | 4.2 table gives 'Severity (this proposal's own view)' A:100 (impact only); no probability per risk; searched sections 4.2 and 7. | NOT MET | Four endangered items with severity only (INV-G HIGH, INV-J HIGH, INV-K MEDIUM, INV-H MEDIUM, B:77-80); no probability per risk; searched sections 5 and 8. |
| 22. Mitigation for each risk | MET | Each 4.2 risk handled: oracle first + selectable branch A:102; pins caught by tests A:103; partitioning A:141; count UNVERIFIABLE A:105; read next A:106. | MET | INV-G via falsifier M-B1 B:77; INV-J copy verbatim, pins fail loudly B:71/B:78; INV-K caught by verify-sync B:79; INV-H no document text in telemetry B:80. |
| 23. Failure modes and recovery | MET | A:102 prose steps 6-9 'must remain as a selectable branch until the oracle result is in'; code gates stay on Half 1 until T-a fires A:139. | MET | B:22 'rf-qa remaining the authority until a replay says otherwise'; B:105 'If M-B1 finds a write ... I would move the hardening in'; fallback B:109. |
| 24. External dependencies and failure scenarios | MET | A:69 'The E2 harness ... leaves Bash open ... report-only by prompt is not a safety property'; C-02 --resolution fallback avoided A:17; no C-07 dependency A:82. | MET | B:115 whether the Agent tool's mode argument or frontmatter decides, 'If the frontmatter decides, B-3's cost estimate stands'; transcripts' location and retention UNVERIFIED B:84. |
| 25. Monitoring or validation mechanism | MET | A:121 'a tree-hash check that no reviewer changed any file'; static guards and golden checks M1-M2 A:113-115. | MET | M-B3 mechanical scope check with git diff --stat and named suites B:88; M-B1 transcript audit B:84. |
| **Subtotal** | **4/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| 26. Collection boundaries (empty, single, max) | MET | A:80 'total reviewers must be 1..8', slot count 1..4, one fixed slot vs floors 6/8/10/12; M3 TOTAL equal to UNVERIFIABLE A:117; lens over its bound rejected A:115. | MET | B:42 'review merge --doc is one file ...; the /task gate reviews a phase output of one to many files with partitioning above six files ... and section ranges above 3000 lines'. |
| 27. State variable interactions across boundaries | MET | A:90 reviewer dict gains lens only when its slot has one, so reflect resolution is byte-identical; A:106 coordinator must read next, not only the exit code. | MET | B:55 'an exit-code-only caller runs an empty reviser when brief_ids is empty and verify_ids is not; next is only in ledger verdict JSON'; persistence shift B:29. |
| 28. Guard condition gaps | MET | A:70 'No other agent modifies files during this step' is a convention until lenses lose Write; tool-engagement minimum not computable A:29; undefined formula case A:117. | MET | B:28 'Report-only is a prompt parameter on a write-capable agent'; confidence gate unpinned B:32; step 10 assumes the agent writes its report B:29. |
| 29. Count divergence (off-by-one, ranges) | MET | M3 'including the 95 boundary' and eligibility 'confidence at least 95 and UNCHECKED zero' A:29/A:117; gate floor 6 vs C-03 min(2, requested) A:18. | MET | B:55 'min(Q, requested) can be 0' (C-02 INV-001); agent-count floors vs C-03 floor of 2 B:57; census 175 vs slice figure 185 [UNVERIFIED] B:96. |
| 30. Interaction effects when components combine | MET | A:105 read-only reviewers plus confidence formula: Bash items become UNVERIFIABLE, lower the denominator and 'can hide a lost check inside a high percentage'. | MET | B:106 doing it with the C-01 T-a and C-03 INV-003 decisions 'couples four open questions in one change to the highest-traffic path'. |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 4/5 |
| Correctness | 3/5 | 3/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.8333** | **25/30 = 0.8333** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case Coverage | Eligible as base (floor 1/5) |
|---|---|---|
| A | 5/5 | Yes |
| B | 5/5 | Yes |

Floor suspension not needed.

## Position-Bias Mitigation

Pass 1 evaluated A then B; Pass 2 evaluated B then A; independent agents, neither read the other's file.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| 1 | A | MET | MET | AGREE | MET |
| 2 | A | MET | MET | AGREE | MET |
| 3 | A | MET | MET | AGREE | MET |
| 4 | A | MET | MET | AGREE | MET |
| 5 | A | MET | MET | AGREE | MET |
| 6 | A | NOT MET | NOT MET | AGREE | NOT MET |
| 7 | A | MET | MET | AGREE | MET |
| 8 | A | MET | MET | AGREE | MET |
| 9 | A | NOT MET | NOT MET | AGREE | NOT MET |
| 10 | A | MET | MET | AGREE | MET |
| 11 | A | MET | MET | AGREE | MET |
| 12 | A | MET | MET | AGREE | MET |
| 13 | A | NOT MET | NOT MET | AGREE | NOT MET |
| 14 | A | MET | MET | AGREE | MET |
| 15 | A | MET | MET | AGREE | MET |
| 16 | A | MET | MET | AGREE | MET |
| 17 | A | MET | MET | AGREE | MET |
| 18 | A | MET | MET | AGREE | MET |
| 19 | A | NOT MET | NOT MET | AGREE | NOT MET |
| 20 | A | MET | MET | AGREE | MET |
| 21 | A | NOT MET | NOT MET | AGREE | NOT MET |
| 22 | A | MET | MET | AGREE | MET |
| 23 | A | MET | MET | AGREE | MET |
| 24 | A | MET | MET | AGREE | MET |
| 25 | A | MET | MET | AGREE | MET |
| 26 | A | MET | MET | AGREE | MET |
| 27 | A | MET | MET | AGREE | MET |
| 28 | A | MET | MET | AGREE | MET |
| 29 | A | MET | MET | AGREE | MET |
| 30 | A | MET | MET | AGREE | MET |
| 1 | B | NOT MET | NOT MET | AGREE | NOT MET |
| 2 | B | MET | MET | AGREE | MET |
| 3 | B | MET | MET | AGREE | MET |
| 4 | B | MET | MET | AGREE | MET |
| 5 | B | MET | MET | AGREE | MET |
| 6 | B | NOT MET | NOT MET | AGREE | NOT MET |
| 7 | B | NOT MET | NOT MET | AGREE | NOT MET |
| 8 | B | MET | MET | AGREE | MET |
| 9 | B | MET | MET | AGREE | MET |
| 10 | B | MET | MET | AGREE | MET |
| 11 | B | MET | MET | AGREE | MET |
| 12 | B | MET | MET | AGREE | MET |
| 13 | B | MET | MET | AGREE | MET |
| 14 | B | MET | MET | AGREE | MET |
| 15 | B | MET | MET | AGREE | MET |
| 16 | B | MET | NOT MET | DISAGREE | MET |
| 17 | B | MET | MET | AGREE | MET |
| 18 | B | MET | MET | AGREE | MET |
| 19 | B | NOT MET | NOT MET | AGREE | NOT MET |
| 20 | B | MET | MET | AGREE | MET |
| 21 | B | NOT MET | NOT MET | AGREE | NOT MET |
| 22 | B | MET | MET | AGREE | MET |
| 23 | B | MET | MET | AGREE | MET |
| 24 | B | MET | MET | AGREE | MET |
| 25 | B | MET | MET | AGREE | MET |
| 26 | B | MET | MET | AGREE | MET |
| 27 | B | MET | MET | AGREE | MET |
| 28 | B | MET | MET | AGREE | MET |
| 29 | B | MET | MET | AGREE | MET |
| 30 | B | MET | MET | AGREE | MET |

Disagreements re-evaluated: 1 of 60 criterion-variant pairs (Variant B, Clarity criterion 1 / n=16).
Final verdicts changed by the re-evaluation relative to a pass: 1 (Pass 2's NOT MET became MET; Pass 1's MET was upheld).
## Combined Scoring

variant_score = 0.50 x quant_score + 0.50 x qual_score.

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker (points won in Step 2) |
|---------|---------------|--------------|-----------------|-------------------------------------------|
| A (Proposal A) | 0.4642 (0.9284) | 0.4167 (25/30 = 0.8333) | **0.8809** | 3 of 30 won outright (X-002, X-006, A-006) |
| B (Proposal B) | 0.5000 (1.0000) | 0.4167 (25/30 = 0.8333) | **0.9167** | 9 of 30 won outright (S-002, S-004, C-003, C-004, C-011, X-001, X-003, X-004, X-007) |

The other 18 points were won by neither variant: both advocates ended on a named hybrid (the hybrid column of the scoring matrix in `debate-transcript.md`).

**Margin**: 3.58% (below the 5% threshold). The qualitative layer is a dead heat (25/30 each, different dimension profile); the whole margin comes from the quantitative layer (RC 10/13 for A against 13/13 for B, and IC 0.9906 against 1.0 because of the intra-variant templates count X-007).
**Tiebreaker applied**: Yes, level 1 (debate performance): Variant B won 9 diff points outright against 3 for Variant A. It confirms the score order; level 2 (correctness criteria met) is not reached: A 3/5 and B 3/5 (identical).

## Selected Base: Variant B (Proposal B; `variant-2-original.md`)

### Selection Rationale
- Combined score B 0.9167 against A 0.8809, margin 3.58%, tiebreaker level 1 (debate performance, 9 points won against 3) confirms B. Both variants clear the edge-case floor (5/5 each).
- The layers differ in kind: the quantitative layer favours B (RC and IC), the qualitative layer ties (25/30 each). A's Correctness losses are code-checked: the packaged-templates count (A:28 says 8, A:115 lists 9; X-007) and the "one place / every lens reviewer of every phase gate" overreach (X-001, conceded by Advocate A). B's Correctness losses are also code-checked and conceded: "schema change over all 8 packaged templates and their validate tests" (X-002) and the install-list claim (A-006); in addition B's document-gate module has no host skill (B conceded in Round 1).
- The debate itself moved both positions to a hybrid. Advocate A conceded that the first change must not wire a panel engine, must not add the per-slot `lens` key, the checklist completion predicate or a floor parameter, and must put owner question Q3 to the owner (C-003, C-004, C-011, S-002, S-004 to B). Advocate B conceded that its clause B-3 is refuted by its own M-B1 rule (the Gate C overwrite, N1) and that the document-gate module leaves the first change (C-001, C-002, C-005, C-006 to hybrid). Base B is chosen because 9 points were won outright by B against 3 by A, and the shape the debate converged on (no engine change, a measurement before any gate edit, a mechanical scope check, the audit with write classes) is closer to B's clause-and-falsifier structure than to A's single pipeline.
- Round 2.5 left 6 HIGH UNADDRESSED invariants (INV-002, INV-009, INV-012, INV-015, INV-016, INV-017); they bear on the executor-persistence and arm-1a parts that come from Variant A, not on B's base structure.

### Strengths to Preserve from Base (Variant B)
1. The three separable clauses B-1, B-2, B-3, each tied to its own measurement (S-002, B 93%); the synth-06 invariant ids INV-A..INV-N (S-004).
2. No panel engine, no per-slot `lens` key, no checklist completion predicate and no floor parameter in the first change; the prose floors stay (C-003, C-004, C-011).
3. The code-checked facts: the report-only gate pattern is replicated in 8 skill files (93 `fix_authorization: false` markers; X-001); Half 1 also rewrites persistence and step 10 (X-003); the spawn `mode` argument is ignored and the tools allowlist is the control (X-004); 8 packaged templates (X-007).
4. M-B1 (transcript audit with a decision rule fixed before the audit), M-B3 (mechanical scope check with unedited pinned suites), M-B4 (anchor probe for C-01 trigger T-a), and the ordered prerequisites (a)-(f) for a later `/task` gate replacement.
5. The "What I did not verify" separate section (S-001 hybrid).

### Strengths to Incorporate from Non-Base Variant (Variant A)
1. The lens-level first deliverable: one read-only lens-reviewer agent definition with a `reflect-reviewer`-pattern allowlist, separate from the single write-capable fix agent, plus the Half 1 / Half 2 separation (U-001; C-001, C-006, C-007 hybrids).
2. The replay oracle design: arm 0 (current lens agents) versus arm 1a (read-only agent, same lens text, prose consolidation) on seeded single documents with clean twins, tree-hash no-mutation check, UNVERIFIABLE share, pre-registered repeat count and variance bound (C-005, C-010, A-005; U-003, U-006).
3. The static guard design: the allowlist is a subset of a named read-only set (spawn and message tools are mutators), with a negative fixture (A-002; Advocate A's finding that `_MUTATORS` at `tests/cli/reflect/test_reviewer_readonly_tools.py:30` omits `Agent` and `SendMessage`).
4. The conditional standard-lens switch at `/task` steps 3-4 with executor-side persistence to the dispatched path and sha256, and a rewritten step 10 (C-002, C-008, A-003), with the wording splits recorded (step-8 verification pair; exclusion scope; probe form).
5. Finding N1 (a report-only lens overwrote another lens's report in a real Gate C run) and the Bash-use split between standard and executing lenses (N3), as evidence that refutes B-3 as first written and bounds the switch.
6. Consistency check against C-01/C-02/C-03 placed first (S-001 hybrid) and the claim/evidence/tag table inside each clause (S-003 hybrid).
