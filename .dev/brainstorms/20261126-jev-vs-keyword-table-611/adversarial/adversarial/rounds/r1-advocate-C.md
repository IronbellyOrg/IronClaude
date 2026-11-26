## 1. Position summary

C offers the strongest audit-trail foundation: it states what evidence establishes ordering and justifies the decision. Merge A’s bias controls and B’s verification structure into C.

## 2. Steelman of A, then of B

**A:** A best protects measurement validity. Independent label bases, contamination splits, blinded table application, paired breakdowns, explicit error denominators, and attempted-call latency make results interpretable (A FR-003–005, FR-010–011, FR-018–020; C-001, C-003, U-001–004). T-01–T-10 give concrete verification targets.

**B:** B best serves later operators. Corpus validation, an ordered gate, append-only runs, deterministic scoring, and preserved rescoring outputs support independent review (B FR-002–004, FR-014, FR-018; NFR-008–011; S-003, U-006–007). T-04 and T-10 make secrecy controls observable.

## 3. Strengths claimed for C

1. **Gate scope:** C blocks comparison as well as live calls until owner inputs and the complete rule exist, matching the seed’s stronger constraint (C run gate; C-004).
2. **Chronology:** The first-request event references the exact pre-run manifest. Retained originals and identified amendments let reviewers establish ordering without trusting retrospective narrative (C FR-003, FR-009; U-008).
3. **Interpretation:** Owner quotations remain beside their confirmed interpretation; unclear units and contradictions block execution. Definitions must explain why they answer the build decision (C run gate; C-010).
4. **Honest records:** Candidates differ from final answers, unattempted cases from errors, and unmeasured local timing from zero. Issue text and resulting references are retained (C FR-007–010; U-009).
5. **Bounded spending:** Unbounded pricing or outstanding liability stops sending; estimates cannot masquerade as safeguards (C Cost cap; C-007).

## 4. Weaknesses identified in A and B

1. B allows table application before owner inputs; A’s hard gate addresses network access rather than all comparison. C preserves the seed’s required ordering (B gate step 4; A section 4; C-004, U-005).
2. A FR-024 ends at coordinator delivery, while the seed requires issue updates. C FR-010 includes retained publication evidence; A needs an explicit downstream completion obligation.
3. B freezes labels without requiring output blindness or non-keyword label bases. C FR-002 improves blindness, though A FR-003–005 remains strongest (C-001, U-001).
4. A fixes error scoring while asking owner acceptance. B permits alternative-rule rescoring without expressly separating exploratory conclusions from the original verdict. C requires separate replacement evidence after invalidation (X-002, U-007; A open questions; B FR-018; C run gate).

## 5. Concessions about C

C lacks numbered NFRs/tests and FR-to-test links (S-001, S-003). Its risk paragraph is harder to scan (S-002); the diff incorrectly calls A’s risk bullets a table. C lacks A’s contamination split and explicit denominator/latency defaults. Adopt A’s no-retry scored run. X-002 overstates C: pre-run policy need not exclude a spec-fixed policy.

## 6. SCORING TABLE

S-001 | B | 90 | Numbered requirements aid references.
S-002 | B | 90 | Risk table pairs causes and controls.
S-003 | B | 98 | T-01–T-13 link requirements and checks.
C-001 | A | 98 | FR-003 requires non-keyword label bases.
C-002 | MERGE | 90 | A’s enums; C’s inconclusive rationale.
C-003 | A | 95 | FR-019 separates attempted/successful latency.
C-004 | C | 99 | Blocks comparison; persists gate evidence.
C-005 | MERGE | 90 | Freeze explicit denominator pre-run.
C-006 | A | 95 | No retries preserves one-request design.
C-007 | C | 96 | Bounds liability and uncertainty.
C-008 | MERGE | 95 | C’s minimization; B’s redaction tests.
C-009 | C | 85 | Naming remains legitimately open.
C-010 | C | 96 | Ambiguous interpretations block execution.
X-001 | A | 95 | Scored retries weaken one-request design.
X-002 | MERGE | 94 | Resolve policy; remove apparent contradiction.
A-001 | MERGE | 95 | Provenance requirements cannot establish availability.
A-002 | C | 94 | FR-005 requires authorized service verification.
A-003 | MERGE | 90 | Difficult labels need review.
A-004 | C | 88 | FR-010 requires limitations.
A-005 | B | 95 | Explicit offline invocation and checks.
U-001 | incorporate yes | Exposes contamination.
U-002 | incorporate yes | Shows paired effects.
U-003 | incorporate yes | Makes invalidity explicit.
U-004 | incorporate yes | Preserves blinded reasoning.
U-005 | incorporate yes | After owner gate only.
U-006 | incorporate yes | Checks corpus completeness.
U-007 | incorporate yes | Mark rescoring exploratory.
U-008 | incorporate yes | Establishes evidence ordering.
U-009 | incorporate yes | Preserves publication evidence.

## 7. SHARED ASSUMPTIONS

A-001 QUALIFY — Verify public corpus availability before freeze.
A-002 QUALIFY — Validate actual response fields at authorized execution.
A-003 QUALIFY — Require instructions and difficult-case review.
A-004 QUALIFY — Limit conclusions to measured network conditions.
A-005 REJECT — Require recorded offline verification, not presumed collection.
