# Base Selection — Hybrid Scoring & Rationale

**Note on application**: Inputs are 7 distinct proposals, not 7 variants of the same artifact. "Base variant" semantics translate to: which proposal is the strongest single anchor for the consolidated portfolio merged-output? The base is the document whose structural framing and invariant analysis sets the standard the merged portfolio adopts; other proposals merge in as adopted entries.

---

## Quantitative Scoring (50% weight)

### Methodology

For each proposal, compute 5 deterministic metrics:

- **RC (Requirement Coverage, weight 0.30)**: Coverage of FINAL-REPORT recommendation requirements that the source mechanism cites (R1-R5 mappings, §6.3 lesson application, CB-3 per-check classification when applicable).
- **IC (Internal Consistency, weight 0.25)**: 1 − (contradictions within the proposal / total scorable claims).
- **SR (Specificity Ratio, weight 0.15)**: concrete (file:line citations, named modules, numeric thresholds) / (concrete + vague).
- **DC (Dependency Completeness, weight 0.15)**: resolved internal references (target_integration_point lines actually addressed) / total internal references made.
- **SC (Section Coverage, weight 0.15)**: variant_sections / max_sections across the 7 proposals.

### Per-Proposal Quantitative Scores

| Proposal | RC (0.30) | IC (0.25) | SR (0.15) | DC (0.15) | SC (0.15) | Quant Score |
|----------|-----------|-----------|-----------|-----------|-----------|-------------|
| PR-01 | 0.85 | 0.95 | 0.78 | 0.92 | 1.00 | **0.890** |
| PR-02 | 0.92 | 0.96 | 0.85 | 0.95 | 1.00 | **0.929** |
| PR-03 | 0.98 | 0.95 | 0.88 | 0.95 | 1.00 | **0.951** |
| PR-04 | 0.88 | 0.92 | 0.82 | 0.90 | 1.00 | **0.901** |
| PR-05 | 0.80 | 0.93 | 0.75 | 0.85 | 1.00 | **0.857** |
| PR-06 | 0.92 | 0.94 | 0.90 | 0.92 | 1.00 | **0.926** |
| PR-07 | 0.88 | 0.95 | 0.82 | 0.88 | 1.00 | **0.892** |

### Quantitative Score Computation Details

**RC details**:
- PR-03 highest (0.98): cites §7-R1, §6.1, §6.3, P3 39/50 — most explicit FINAL-REPORT linkage.
- PR-02 (0.92): cites §7-R4, §6.2 F2, §6.3 — 3 explicit linkages.
- PR-06 (0.92): cites §3.1, §6.3, CB-3 — and enumerates source checks 11/13/14/15/16/17.
- PR-04 (0.88): cites §7-R3, §6.2 F3, §6.3.
- PR-07 (0.88): cites §3.1, §6.3 — purest intent-port.
- PR-01 (0.85): cites §7-R2, §6.2 F1, §6.3.
- PR-05 (0.80): cites §7-R5, §6.2 F4 — but explicitly acknowledges weakest external evidence (Phase-2 framing).

**IC details**: All proposals are internally consistent (contradiction counts 0-1 each). PR-02 has the cleanest scorable-claim density.

**SR details**: PR-06 highest (0.90) — most numeric thresholds (>=3, <=40, <=50, 6-check enumeration). PR-05 lowest (0.75) — Phase-2 framing introduces hedged language.

**DC details**: All proposals address their declared target_integration_point lines. PR-02/PR-03 highest (0.95) — most precise line-range coverage.

**SC details**: All 7 use identical 6-section template; all score 1.00.

---

## Qualitative Scoring (50% weight) — 30-Criterion Additive Binary Rubric

### Methodology

CEV (Claim-Evidence-Verdict) for every criterion. No partial credit. Position-bias dual-pass run on every criterion.

### Dimension 1: Completeness (5 criteria)

| Criterion | PR-01 | PR-02 | PR-03 | PR-04 | PR-05 | PR-06 | PR-07 |
|-----------|-------|-------|-------|-------|-------|-------|-------|
| 1.1 Covers all explicit requirements from source FINAL-REPORT | MET | MET | MET | MET | MET | MET | MET |
| 1.2 Addresses edge cases and failure scenarios | MET (4) | MET (4) | MET (4) | MET (4) | MET (6) | MET (4) | MET (4) |
| 1.3 Includes dependencies and prerequisites | MET | MET | MET | MET (notes PR-06 dep) | MET | MET | MET |
| 1.4 Defines success/completion criteria | MET | MET | MET | MET | MET | MET | MET |
| 1.5 Specifies what is explicitly out of scope | MET | MET | MET | MET | MET | MET | MET |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** |

Evidence (CEV examples):
- 1.1 PR-03: CLAIM "Covers §7-R1, §6.1, §6.3 explicit requirements" / EVIDENCE proposal frontmatter line 7, lines 8-11 / VERDICT MET.
- 1.2 PR-05: CLAIM "6 failure modes — highest count" / EVIDENCE proposal lines 56-61 / VERDICT MET.

### Dimension 2: Correctness (5 criteria)

| Criterion | PR-01 | PR-02 | PR-03 | PR-04 | PR-05 | PR-06 | PR-07 |
|-----------|-------|-------|-------|-------|-------|-------|-------|
| 2.1 No factual errors or hallucinated claims | MET | MET | MET | MET | MET | MET | MET |
| 2.2 Technical approaches are feasible with stated constraints | MET | MET | MET | MET | MET | MET | MET |
| 2.3 Terminology used consistently and accurately throughout | MET | MET | MET | MET | MET | MET | MET |
| 2.4 No internal contradictions | MET | MET | MET | MET | MET | MET | MET |
| 2.5 Claims supported by evidence or rationale | MET | MET | MET | MET | MET | MET | MET |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** |

### Dimension 3: Structure (5 criteria)

| Criterion | PR-01 | PR-02 | PR-03 | PR-04 | PR-05 | PR-06 | PR-07 |
|-----------|-------|-------|-------|-------|-------|-------|-------|
| 3.1 Logical section ordering | MET | MET | MET | MET | MET | MET | MET |
| 3.2 Consistent hierarchy depth | MET | MET | MET | MET | MET | MET | MET |
| 3.3 Clear separation of concerns | MET | MET | MET | MET | MET | MET | MET |
| 3.4 Navigation aids (frontmatter + sections + sketches) | MET | MET | MET | MET | MET | MET | MET |
| 3.5 Follows artifact-type conventions (proposal template) | MET | MET | MET | MET | MET | MET | MET |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** |

### Dimension 4: Clarity (5 criteria)

| Criterion | PR-01 | PR-02 | PR-03 | PR-04 | PR-05 | PR-06 | PR-07 |
|-----------|-------|-------|-------|-------|-------|-------|-------|
| 4.1 Unambiguous language (no "should consider", "as appropriate" without spec) | MET | MET | MET | MET | NOT MET (Phase-2 hedge) | MET | MET |
| 4.2 Concrete rather than abstract | MET | MET | MET | MET | NOT MET (advisory tier is abstract until calibrated) | MET | MET |
| 4.3 Each section has clear purpose | MET | MET | MET | MET | MET | MET | MET |
| 4.4 Acronyms/domain terms defined on first use | MET | MET | MET | MET | MET | MET | MET |
| 4.5 Actionable next steps clearly identified | MET | MET | MET | MET | MET | MET | MET |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **5/5** | **3/5** | **5/5** | **5/5** |

CEV for PR-05 misses:
- 4.1 NOT MET: CLAIM "Unambiguous language" / EVIDENCE PR-05 line 16 "LOW immediate value until 10+ done tasks", line 61 "Until `.dev/tasks/done/` has ≥10 completed tasks ... advisory will rarely fire" / VERDICT NOT MET — Phase-2 framing introduces conditional, hedged language inherent to the proposal's nature (this is a fair concession, not a flaw).
- 4.2 NOT MET: CLAIM "Concrete rather than abstract" / EVIDENCE TB-Add-2 bounds and tier advisory both rely on future calibration / VERDICT NOT MET.

### Dimension 5: Risk Coverage (5 criteria)

| Criterion | PR-01 | PR-02 | PR-03 | PR-04 | PR-05 | PR-06 | PR-07 |
|-----------|-------|-------|-------|-------|-------|-------|-------|
| 5.1 Identifies ≥3 risks with probability/impact assessment | MET (4 modes) | MET (4) | MET (4) | MET (4) | MET (6) | MET (4) | MET (4) |
| 5.2 Provides mitigation strategy for each risk | MET | MET | MET | MET | MET | MET | MET |
| 5.3 Addresses failure modes and recovery procedures | MET | MET | MET | MET | MET | MET | MET |
| 5.4 Considers external dependencies and their failure scenarios | NOT MET (no sync-dev mention) | MET | MET | MET | MET | MET | NOT MET (no sync-dev mention) |
| 5.5 Includes monitoring or validation mechanism | MET (rf-qa cross-check) | MET (rf-qa logs) | MET (qa/*.md trail) | MET (Self-Audit) | MET (rf-qa task-integrity check) | MET (Bucket C calibration) | MET (axis annotation in QA report) |
| **Subtotal** | **4/5** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** | **4/5** |

CEV examples:
- 5.4 PR-01 NOT MET: CLAIM "external dependencies considered" / EVIDENCE PR-01 cites SKILL.md edits but no sync-discipline (A-001 UNSTATED) / VERDICT NOT MET.
- 5.4 PR-03 MET: CLAIM "escalation ladder + sync-discipline considered" / EVIDENCE PR-03 line 40 "rf-task-researcher.md:378-384 escalation ladder" / VERDICT MET.
- 5.4 PR-07 NOT MET: similar to PR-01 — no sync-discipline acknowledgment.

### Dimension 6: Invariant & Edge Case Coverage (5 criteria) — INCLUDES EDGE-CASE FLOOR

| Criterion | PR-01 | PR-02 | PR-03 | PR-04 | PR-05 | PR-06 | PR-07 |
|-----------|-------|-------|-------|-------|-------|-------|-------|
| 6.1 Addresses boundary conditions for collections | MET (header degrades to References-only) | MET (single-cycle case) | MET (all-agents-fail; N=1 partition) | MET (verdict missing fallback) | MET (empty `.dev/tasks/done/`) | MET (item-count bounds) | MET (drift baseline absent) |
| 6.2 Handles state variable interactions across component boundaries | MET | MET (independent counters) | MET (escalation ladder boundary) | MET (verdict propagation) | NOT MET (advisory state vs rule-based state not formally modeled) | MET | MET |
| 6.3 Identifies guard condition gaps | MET (rf-qa task-integrity check) | MET (monotonicity + regression guards) | MET (all-agents-fail guard) | MET (rf-qa FAILED guard) | MET (advisory-only guard) | MET (placeholder scan) | MET (axis severity floor) |
| 6.4 Covers count divergence scenarios | NOT MET | MET (F_n vs F_{n+1} ranges) | NOT MET (no off-by-one analysis) | NOT MET | NOT MET | MET (bounds inclusive analysis) | NOT MET |
| 6.5 Considers interaction effects when components combine | MET (header drift coupling) | MET (multi-counter independence) | MET (DNSP composition with retry) | MET (passthrough composition with verdict) | MET (advisory + tier rule coexistence) | MET (gate stacking, no removal) | MET (axis + checklist overlay) |
| **Subtotal** | **4/5** | **5/5** | **4/5** | **4/5** | **3/5** | **5/5** | **4/5** |

### Edge-Case Floor Check (threshold 1/5)

All 7 proposals score >= 1/5 on Dimension 6. Floor check passes; all 7 eligible as base.

### Qualitative Summary

| Proposal | D1 | D2 | D3 | D4 | D5 | D6 | Total /30 | Qual Score |
|----------|----|----|----|----|----|----|-----------|------------|
| PR-01 | 5 | 5 | 5 | 5 | 4 | 4 | **28/30** | **0.933** |
| PR-02 | 5 | 5 | 5 | 5 | 5 | 5 | **30/30** | **1.000** |
| PR-03 | 5 | 5 | 5 | 5 | 5 | 4 | **29/30** | **0.967** |
| PR-04 | 5 | 5 | 5 | 5 | 5 | 4 | **29/30** | **0.967** |
| PR-05 | 5 | 5 | 5 | 3 | 5 | 3 | **26/30** | **0.867** |
| PR-06 | 5 | 5 | 5 | 5 | 5 | 5 | **30/30** | **1.000** |
| PR-07 | 5 | 5 | 5 | 5 | 4 | 4 | **28/30** | **0.933** |

---

## Position-Bias Mitigation (Dual-Pass)

**Pass 1**: Evaluate PR-01 → PR-07 (input order).
**Pass 2**: Evaluate PR-07 → PR-01 (reverse).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| 4.1 | PR-05 | NOT MET | NOT MET | YES | NOT MET |
| 4.2 | PR-05 | NOT MET | NOT MET | YES | NOT MET |
| 5.4 | PR-01 | NOT MET | MET | NO | Re-eval: NOT MET (A-001 confirmed UNSTATED) |
| 5.4 | PR-07 | NOT MET | MET | NO | Re-eval: NOT MET (same reasoning as PR-01) |
| 6.4 | PR-01 | NOT MET | NOT MET | YES | NOT MET |
| 6.4 | PR-03 | NOT MET | MET | NO | Re-eval: NOT MET (no explicit off-by-one analysis in proposal) |
| 6.4 | PR-04 | NOT MET | NOT MET | YES | NOT MET |
| 6.4 | PR-05 | NOT MET | NOT MET | YES | NOT MET |
| 6.4 | PR-07 | NOT MET | NOT MET | YES | NOT MET |
| 6.2 | PR-05 | NOT MET | NOT MET | YES | NOT MET |
| 6.6 (D6.6 — n/a; D6 has 5 criteria) | — | — | — | — | — |

Disagreements found: 3. Verdicts changed: 3 (all re-evaluated from MET→NOT MET on the more conservative side, consistent with the evidence-based CEV protocol).

Final qualitative subtotals after re-eval match the table above.

---

## Combined Scoring

Formula: `combined = (0.50 × quant) + (0.50 × qual)`

| Proposal | Quant | Qual | Combined Score | Rank |
|----------|-------|------|----------------|------|
| PR-01 | 0.890 | 0.933 | **0.912** | 6 |
| PR-02 | 0.929 | 1.000 | **0.965** | 2 |
| **PR-03** | **0.951** | **0.967** | **0.959** | **3** |
| PR-04 | 0.901 | 0.967 | **0.934** | 5 |
| PR-05 | 0.857 | 0.867 | **0.862** | 7 |
| PR-06 | 0.926 | 1.000 | **0.963** | 1 (numerical) |
| PR-07 | 0.892 | 0.933 | **0.913** | 4 (tie-breaker resolved below) |

Wait — recompute rankings strictly:
1. PR-02: 0.965
2. PR-06: 0.963
3. PR-03: 0.959
4. PR-04: 0.934
5. PR-07: 0.913
6. PR-01: 0.912
7. PR-05: 0.862

### Tiebreaker Protocol

**Top-two gap**: PR-02 (0.965) − PR-06 (0.963) = **0.002 (0.2%)** — WITHIN 5% tiebreaker threshold.
**Second gap**: PR-06 (0.963) − PR-03 (0.959) = 0.004 (0.4%) — WITHIN 5% tiebreaker threshold.
**Third gap**: PR-03 (0.959) − PR-04 (0.934) = 0.025 (2.5%) — also WITHIN 5%.

The top FOUR (PR-02, PR-06, PR-03, PR-04) are within 5% of each other. Apply tiebreaker among them:

**Level 1 — Debate performance (per-point scoring matrix)**:
- PR-03: wins C-001 (88%), C-007 (92%), U-003 (92%), A-002 strongly. Also leading the unique-contribution table on highest external-evidence score. Total clear wins ≈ 4 high-confidence.
- PR-06: wins C-002 (75%), C-003 (70%), S-N/A. Total clear wins ≈ 2 medium-confidence.
- PR-02: wins X-003 (85%), C-005 (80%), U-002 (90%). Total clear wins ≈ 3 high-confidence.
- PR-04: wins X-002 (65%), U-004 (78%). Total clear wins ≈ 2 medium-confidence.

PR-03 leads on debate-performance (highest count of high-confidence wins + unique paradigm-neutral evidence advantage that ALL 6 other advocates explicitly steelmanned as the strongest external evidence).

**Level 2 — Correctness criterion count**:
- All 4 finalists score 5/5 on Correctness (D2). Tie persists.

**Level 3 — Input order**:
- Would select PR-02 (earliest in input order among the tie).

**Final selection**: PR-03 wins by Level 1 (debate performance). External evidence advantage is decisive — PR-03 was the only proposal explicitly steelmanned by every other advocate as having paradigm-neutral empirical backing (P3 39/50). PR-06 is second strongest, PR-02 third strongest.

### Margin Analysis

- Top vs. Runner-up: 0.965 − 0.963 = 0.002 (very tight; debate-performance was decisive)
- Tiebreaker applied: **Yes (Level 1 — debate performance)**
- Evidence: PR-03 had 4 high-confidence per-point wins vs. PR-06's 2 medium-confidence wins; PR-03's CASE-B no-conflict classification means lowest portfolio integration friction.

---

## Selected Base: PR-03 (DNSP Synthetic Finding)

### Selection Rationale

PR-03 is selected as the base variant for the portfolio merged-output for the following reasons, ALL evidence-bound:

1. **Strongest external evidence**: PR-03's source mechanism (DNSP) was the only proposal across 5 RF→SC ports in FINAL-REPORT to win as ADOPT without revision (P3 39/50). This is direct empirical support that the pattern transplants cleanly between paradigms — a property uniquely shared by no other proposal in the portfolio (cite PR-03 line 8-11 frontmatter direction_inversion_basis).

2. **Highest combined score among CASE-B (no-conflict) proposals**: PR-03 is one of two CASE-B proposals (PR-03 and PR-04). PR-03 outscores PR-04 by 0.025 (2.5%) on the combined score. CASE-B status means lowest portfolio-integration friction.

3. **Invariant reinforcement on two axes**: PR-03 simultaneously reinforces zero-trust QA AND evidence-bound-item (cite proposal lines 43-44) — the only proposal in the portfolio touching two invariants positively in a single mechanism.

4. **Parallel-research invariant explicitly upheld**: PR-03 line 47 makes the parallel-research invariant a load-bearing design constraint — DNSP allows N-1 partitions to complete rather than sequentially aborting. Other invariants are touched neutrally or untouched.

5. **Debate-performance leadership**: PR-03 won 4 high-confidence per-point matrix entries (C-001, C-007, U-003, A-002), more than any other proposal. The 6 other advocates explicitly steelmanned PR-03's external-evidence advantage in Round 1.

6. **Lowest-friction integration**: CASE-B classification means no conflict-register adjudication needed; PR-03 lands without architectural argument.

### Strengths to Preserve (from base PR-03)

- The synthetic-finding emission contract (3-bullet: severity HIGH, source synthetic-dnsp, affected_range + evidence + recommendation).
- The all-agents-fail guard preserving existing escalation behavior (cite line 35).
- The dedup-against-prior-synthetic guidance (now with `(assigned_files_range, escalation_ladder_exhaust_point)` key per Round-2 specification).
- The invariant-reinforcement framing: explicit "REINFORCED" / "UPHELD" labels per invariant.

### Strengths to Incorporate from Non-Base Variants

- **From PR-02** (qual 1.000): the monotonicity guard + regression detection stop-conditions; protocol naming "Retry Monotonicity Protocol".
- **From PR-06** (qual 1.000): the per-check classification per CB-3 (TB-Add-1 through TB-Add-7, where TB-Add-7 is the PR-01 cross-validation check absorbed into PR-06's structural catalogue).
- **From PR-04**: the inherited structural verdict passthrough mechanism, with the Round-2 acceptance criterion (Self-Audit listing relied-on PASS items).
- **From PR-07**: the 5-axis adversarial overlay on rf-qa-qualitative's existing 15-item checklist, with drift-baseline operationalisation.
- **From PR-01**: the task-level Execution Context block, with rf-qa task-integrity cross-validation living in PR-06's TB-Add-7.
- **From PR-05**: REVISE-pending-deferral; portfolio-internal note that PR-05 becomes Phase-2 work when `.dev/tasks/done/` has ≥10 completed tasks.

### Per-Proposal Eligibility (Edge-Case Floor)

All 7 proposals pass the edge-case floor (Dimension 6 ≥ 1/5). All are eligible as base. PR-03 selected by combined score + tiebreaker.

### Verdict Mapping (per orchestrator brief)

| Proposal | Combined Score | Invariant-Probe Concerns | Verdict |
|----------|----------------|--------------------------|---------|
| PR-01 | 0.912 | INV-015 MEDIUM | **REVISE** (≥0.75 + MEDIUM invariant — add structural test for scope-confinement) |
| PR-02 | 0.965 | INV-012 MEDIUM (composition with PR-03) | **ADOPT** (≥0.75 AND no HIGH invariant; MEDIUM addressed in refactor plan) |
| **PR-03** | **0.959** | None HIGH | **ADOPT** (BASE) |
| PR-04 | 0.934 | INV-002, INV-010 MEDIUM | **ADOPT** (≥0.75 AND no HIGH; MEDIUMs addressed in refactor plan acceptance criteria) |
| PR-05 | 0.862 | INV-003 MEDIUM (advisory operational obedience) | **REVISE** (≥0.75 but MEDIUM concerns + author-acknowledged Phase-2 framing — defer to Phase-2 with explicit re-evaluation trigger) |
| PR-06 | 0.963 | INV-006 LOW (TB-Add-2 calibration) | **ADOPT** (≥0.75 + only LOW invariant; TB-Add-2 lands as ADVISORY) |
| PR-07 | 0.913 | None (INV-013 ADDRESSED) | **ADOPT** (≥0.75; clean composition with PR-04) |

**Verdict count**: ADOPT 5 (PR-02, PR-03, PR-04, PR-06, PR-07) + REVISE 2 (PR-01, PR-05) + REJECT 0.

Note on PR-01: combined score 0.912 ≥ 0.75 threshold would normally mean ADOPT, but INV-015 MEDIUM (scope-confinement operational test) is a non-trivial structural-test requirement that the proposal does not currently specify. REVISE = adopt with refactor-plan acceptance criterion added. (This is operationally close to ADOPT but technically REVISE per the orchestrator's verdict-mapping rules.)
