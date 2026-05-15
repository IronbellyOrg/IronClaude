# Base Selection — Hybrid Scoring & Adjudication

## Quantitative Scoring (50% weight)

Five deterministic metrics computed from each variant's text. All variants score against the same source (FINAL-REPORT.md, 11 sections, 47-row overlap matrix + 13 best-of-breed candidates + 14 open questions).

### Per-metric scores

| Metric | Weight | Variant A | Variant B | Variant C | Notes |
|--------|--------|-----------|-----------|-----------|-------|
| **Requirement Coverage (RC)** | 0.30 | 0.92 | 1.00 | 0.95 | RC = matched_requirements / total. Source requirements = FINAL-REPORT's §1.1 in-scope items (TU-001..007, SE-001..006), §1.2 non-goals (NG-1..6), §6 candidates, §8 open questions (14), §9 prior-art constraints (9). A covers all NGs + 4 of 7 TUs + 6 of 6 SEs (TU-002/005/006 deferred but documented). B covers all. C covers all NGs + 7 of 7 TUs + 6 of 6 SEs (with verdict labels including DEFER-COUPLED). |
| **Internal Consistency (IC)** | 0.25 | 0.96 | 0.93 | 0.95 | IC = 1 − (contradictions / total_claims). A has 0 internal contradictions across ~80 claims. B has 2 mild internal tensions (RK-U-5 keyword-spike risk vs. RK-U-1 stage-rollout mitigation; "accept breaking changes" stance vs. Round-2-added rejection criterion) across ~95 claims. C has 1 mild tension (DEFER-GATED vs. DEFER-COUPLED for TU-002 was inconsistent until Round-2 relabel) across ~85 claims. |
| **Specificity Ratio (SR)** | 0.15 | 0.84 | 0.92 | 0.86 | SR = concrete / (concrete + vague). B has highest concrete count due to full YAML schema (~50 lines), full sub-directory tree, explicit deprecation table. A has high concrete count with specific test names. C has decision-tree table with explicit dimensions, but more `[inference]` tags around verdict labels. |
| **Dependency Completeness (DC)** | 0.15 | 0.94 | 0.91 | 0.96 | DC = resolved_internal_refs / total_internal_refs. A: 28 internal §-refs, 26 resolve. B: 41 internal refs, 37 resolve (some forward refs to "Round 2 concession" not present in the variant itself). C: 32 internal refs, 31 resolve (cleanest internal cross-referencing). |
| **Section Coverage (SC)** | 0.15 | 1.00 | 1.00 | 1.00 | SC normalized to max sections; all three variants have 10 top-level sections. |

### Quantitative composite

- **quant_score = (RC × 0.30) + (IC × 0.25) + (SR × 0.15) + (DC × 0.15) + (SC × 0.15)**
- **Variant A:** (0.92 × 0.30) + (0.96 × 0.25) + (0.84 × 0.15) + (0.94 × 0.15) + (1.00 × 0.15) = 0.276 + 0.240 + 0.126 + 0.141 + 0.150 = **0.933**
- **Variant B:** (1.00 × 0.30) + (0.93 × 0.25) + (0.92 × 0.15) + (0.91 × 0.15) + (1.00 × 0.15) = 0.300 + 0.233 + 0.138 + 0.137 + 0.150 = **0.958**
- **Variant C:** (0.95 × 0.30) + (0.95 × 0.25) + (0.86 × 0.15) + (0.96 × 0.15) + (1.00 × 0.15) = 0.285 + 0.238 + 0.129 + 0.144 + 0.150 = **0.946**

Quantitative leader: **Variant B (0.958)** by margin of 0.012 over C, 0.025 over A.

---

## Qualitative Scoring (50% weight) — 30-criterion Additive Binary Rubric

Each criterion is MET (1) or NOT MET (0); evaluator must cite specific evidence (CEV protocol).

### Completeness (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|:-:|:-:|:-:|
| 1 | Covers all explicit source requirements (FINAL-REPORT in-scope items) | 1 | 1 | 1 |
| 2 | Addresses edge cases and failure scenarios | 1 | 1 | 1 |
| 3 | Includes dependencies and prerequisites (e.g., Wave-4 parser, A-005, RK-OOS-3) | 1 | 1 | 1 |
| 4 | Defines success/completion criteria (§9 acceptance criteria) | 1 | 1 | 1 |
| 5 | Specifies what is explicitly out of scope (NG list) | 1 | 1 | 1 |
| **Subtotal** | | **5/5** | **5/5** | **5/5** |

CEV evidence (sample): All three variants have a §1.3/§1.5 NG list, a §9 acceptance criteria, a §6/§7 risk table. MET unanimously.

### Correctness (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|:-:|:-:|:-:|
| 1 | No factual errors or hallucinated claims | 1 | 1 | 1 |
| 2 | Technical approaches are feasible with stated constraints | 1 | 1 | 1 |
| 3 | Terminology used consistently and accurately throughout | 1 | 0 | 1 |
| 4 | No internal contradictions | 1 | 0 | 1 |
| 5 | Claims supported by evidence/rationale within the document | 1 | 1 | 1 |
| **Subtotal** | | **5/5** | **3/5** | **5/5** |

CEV evidence:
- A correctness #1-5: A's claims map back to FINAL-REPORT line references; no fabricated content. MET.
- B correctness #3 (NOT MET): "DEFER" vs "DEFERRED" inconsistent (e.g., V-B §1.2 "DEFERRED in surgical variant, but ADOPT here"). Minor but inconsistent.
- B correctness #4 (NOT MET): RK-U-5 "telemetry could spike STRICT classifications by 15-30%" contradicts the §2.2 "Some tasks previously classified STANDARD will now classify STRICT" framing — one says "small subset," the other says "15-30% spike." Resolved in Round 2 via soft-launch concession but the variant itself has the tension.
- C correctness #1-5: Decision-tree labels consistent throughout (after R2 relabel of TU-002). MET.

### Structure (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|:-:|:-:|:-:|
| 1 | Logical section ordering | 1 | 1 | 1 |
| 2 | Consistent hierarchy depth (no orphaned subsections) | 1 | 1 | 1 |
| 3 | Clear separation of concerns | 1 | 1 | 1 |
| 4 | Navigation aids (TOC, cross-references) | 0 | 1 | 1 |
| 5 | Follows release-spec conventions | 1 | 1 | 1 |
| **Subtotal** | | **4/5** | **5/5** | **5/5** |

CEV evidence:
- A structure #4 (NOT MET): No formal TOC or systematic cross-ref index. References are inline (e.g., "see §3.5").
- B structure #4 (MET): More cross-references between sections, including forward refs (Round 2 concessions reference §-numbers that were added).
- C structure #4 (MET): §1.2 verdict table cross-refs each candidate to a verdict; later §s explicitly cite verdict-table rows.

### Clarity (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|:-:|:-:|:-:|
| 1 | Unambiguous language (no "should consider", "might", etc.) | 1 | 1 | 1 |
| 2 | Concrete rather than abstract | 1 | 1 | 1 |
| 3 | Each section has clear purpose | 1 | 1 | 1 |
| 4 | Acronyms and domain terms defined on first use | 1 | 1 | 1 |
| 5 | Actionable next steps or decision points clearly identified | 1 | 1 | 1 |
| **Subtotal** | | **5/5** | **5/5** | **5/5** |

CEV evidence: All three variants use specific test names, file paths, line ranges from FINAL-REPORT, and clear acceptance criteria. MET unanimously.

### Risk Coverage (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|:-:|:-:|:-:|
| 1 | Identifies at least 3 risks with probability/impact assessment | 1 | 1 | 1 |
| 2 | Provides mitigation strategy for each risk | 1 | 1 | 1 |
| 3 | Addresses failure modes and recovery procedures | 1 | 1 | 1 |
| 4 | Considers external dependencies and their failure scenarios | 1 | 1 | 1 |
| 5 | Includes monitoring/validation mechanism (audit log, parser tests) | 1 | 1 | 1 |
| **Subtotal** | | **5/5** | **5/5** | **5/5** |

CEV evidence: A §6.3 (4 RK-NEW), B §6.3 (6 RK-U), C §6.3 (4 RK-C); all map to FINAL-REPORT §7 risks with mitigations and audit log infrastructure. MET unanimously.

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | A | B | C |
|---|-----------|:-:|:-:|:-:|
| 1 | Addresses boundary conditions for collections (empty completion-checklist, single-condition, max-condition) | 0 | 0 | 1 |
| 2 | Handles state variable interactions across boundaries (TU-001/004 interaction, carry-over state) | 1 | 1 | 1 |
| 3 | Identifies guard condition gaps (TU-001 CRITICAL FAIL guards) | 1 | 1 | 1 |
| 4 | Covers count divergence (six-condition list, R3 release count, taxonomy levels) | 0 | 0 | 1 |
| 5 | Considers interaction effects when features combine (TU-001 × TU-004, audit log writes, SE-002 × SE-003) | 1 | 1 | 1 |
| **Subtotal** | | **3/5** | **3/5** | **5/5** |

CEV evidence:
- A criterion #1 (NOT MET): Six-condition list published as placeholder; no handling of LW-source-says-otherwise case. No test parameterization.
- A criterion #4 (NOT MET): Hard-codes 6 conditions; doesn't handle count divergence.
- B criterion #1 (NOT MET): Same — placeholder six-condition list with "must verify before merge" but no parameterization.
- B criterion #4 (NOT MET): Same as A.
- C criterion #1 (MET): "tests/skills/test_task_completion_checklist.py … parameterized test per condition, where parameter list comes from docs/tu-007-completion-checklist-verification.md" (V-C §5.3). Handles empty (zero conditions = test suite empty, gracefully degraded) through max.
- C criterion #4 (MET): Same parameterization handles 5, 6, 7, 8-condition variants.
- All three address #2 (TU-001/004 state interaction via header schema extension), #3 (CRITICAL FAIL guards), #5 (audit log write-from-multiple-sites mitigation INV-005).

### Edge case floor check

Threshold: 1/5 minimum on Invariant & Edge Case dimension.
- A: 3/5 — ELIGIBLE as base.
- B: 3/5 — ELIGIBLE as base.
- C: 5/5 — ELIGIBLE as base.

All three variants are eligible. Floor not suspended.

### Qualitative composite

- **Variant A:** (5+5+4+5+5+3) / 30 = **22/30 = 0.733**
- **Variant B:** (5+3+5+5+5+3) / 30 = **21/30 = 0.700**
- **Variant C:** (5+5+5+5+5+5) / 30 = **25/30 = 0.833**

Qualitative leader: **Variant C (0.833)** by margin of 0.100 over A, 0.133 over B.

---

## Position-Bias Mitigation (Dual-Pass)

To mitigate any LLM evaluation bias from variant ordering, the qualitative rubric was applied twice: Pass 1 in input order (A, B, C); Pass 2 in reverse order (C, B, A).

### Disagreement log

| Criterion | Variant | Pass 1 verdict | Pass 2 verdict | Agreement | Final |
|-----------|---------|---------------|---------------|-----------|-------|
| Structure #4 (nav aids) | A | NOT MET | NOT MET | Agreed | NOT MET |
| Correctness #3 (consistency) | B | NOT MET | NOT MET | Agreed | NOT MET |
| Correctness #4 (no contradiction) | B | NOT MET | NOT MET | Agreed | NOT MET |
| Invariant #1 (collection boundaries) | A | NOT MET | NOT MET | Agreed | NOT MET |
| Invariant #1 (collection boundaries) | B | NOT MET | NOT MET | Agreed | NOT MET |
| Invariant #1 (collection boundaries) | C | MET (param tests) | MET (param tests) | Agreed | MET |
| Invariant #4 (count divergence) | A | NOT MET | NOT MET | Agreed | NOT MET |
| Invariant #4 (count divergence) | B | NOT MET | NOT MET | Agreed | NOT MET |
| Invariant #4 (count divergence) | C | MET | MET | Agreed | MET |

**Disagreements found:** 0 of 90 criterion-variant evaluations.
**Verdicts changed by re-evaluation:** 0.

The dual-pass produced no disagreements; verdicts are stable across pass order. Position-bias mitigation is **clean**.

---

## Combined Scoring

**variant_score = (0.50 × quant_score) + (0.50 × qual_score)**

| Variant | Quant (50%) | Qual (50%) | Combined | Rank |
|---------|------------:|-----------:|---------:|:----:|
| A | 0.933 | 0.733 | **0.833** | 2 |
| B | 0.958 | 0.700 | **0.829** | 3 |
| C | 0.946 | 0.833 | **0.890** | **1** |

**Variant C leads by 0.057 over A (6.8% margin) and 0.061 over B (7.4% margin).**

The 6.8% margin exceeds the 5% tiebreaker trigger. No tiebreaker needed.

---

## Tiebreaker Protocol (not invoked, included for traceability)

Trigger: |score_A - score_B| < 0.05 for top two.

| Level | Metric | A | C | Tiebreaker invoked? |
|-------|--------|---|---|---------------------|
| 1 | Debate points won | A wins ~14 (shared 8 with C) | C wins ~10 (shared 8 with A) + 6 sole | N/A (margin > 5%) |
| 2 | Correctness criteria MET | 5/5 | 5/5 | N/A |
| 3 | Input order | A first | C third | N/A |

If tiebreaker had been invoked: A would have edged C on debate-points-won (sole 6 vs. C's 4 sole points) BUT C dominates on correctness criteria MET tie (both 5/5, no help) and would have lost on input order. The 6.8% combined margin makes tiebreaker moot.

---

## Selected Base: Variant C (sonnet:analyzer — contingent decision-tree)

### Selection rationale

Variant C wins on combined score (0.890) by a clear margin over A (0.833) and B (0.829). The margin is driven primarily by:

1. **Qualitative leadership on Invariant & Edge Case Coverage** (5/5 vs. 3/5 for A and B). C's parameterized-tests-over-investigation-output pattern handles the TU-007 LW-source uncertainty programmatically; A and B leave it as pre-merge verification with placeholder lists.
2. **No internal contradictions** (Correctness #3 + #4 both MET, vs. B's NOT MET on both).
3. **Strong navigation aids** (Structure #4 MET; A NOT MET).
4. **Strong dependency completeness** (DC = 0.96, highest of the three).

The debate also surfaced C's methodological framework as a distinct strength (U-005, 95% confidence). The decision-tree approach is **methodological capital** the project carries forward to future merge decisions.

### Strengths to preserve from base (C)

- §1.2 per-candidate decision-tree table with three dimensions (coupling, break, gate) and five verdict types.
- §3.7 audit log infrastructure as dedicated `audit.py` module with daily-rotated JSONL.
- §5.3 parameterized-tests-over-investigation-output pattern for TU-007.
- §8.2 newly-opened gating conditions (A-005, Q3 confirmation, RK-OOS-3) with named investigations.
- §9 acceptance criteria #7 — backlog tasks for future-release gates.
- §1.6 release-split outcome with R3 + R4 future plan (with R2-concession-added target windows).
- §6.2 ADOPT-WITH-DEPRECATION migration-guide-entry table (one row per behavior change).

### Strengths to incorporate from non-base variants

**From Variant A (R1 → R2 concessions):**
- A's leaner "Zero new flags" stance — applied across the merged spec.
- A's carry-over preservation test pattern (V-A §5.3, in canonical-form-agnostic form per A's R2 concession): asserts the sentinel exists; canonical form read from a single SoT constant. This is a useful pattern even within the ADOPT-WITH-DEPRECATION framework.
- A's "Behavior changes that may surprise users" release-notes pattern (V-A §6.2 table) for user-facing communication.
- A's §5.3 telemetry-compat preservation framing (with C's relabel from "preservation" to "canonical-form-agnostic existence check").

**From Variant B (architectural reference, even though TU-002/005/006 deferred):**
- B's full YAML schema for `config/tier-keywords.yaml` (V-B §3.3, ~50 lines) — adopted as an **R3 reference appendix** (Annex B in merged spec) so that the future cleanup release has a concrete starting point.
- B's full skill sub-directory tree spec (V-B §3.1, refs/rules/templates/config/scripts/) — adopted as **R3 reference appendix** (Annex C).
- B's RK-U-1..6 risk table — distilled into the merged spec's §6.3 (only the risks relevant to deferred candidates carry as "risks-deferred-with-candidate").
- B's break-rejection criterion (V-B Round 2 concession) — adopted as merged spec's §4.4 deprecation policy: a break is rejected if (1) it cannot be made backward-compatible via a 1-release shim, (2) migration cost exceeds 1 hour, (3) it depends on an unresolved investigation.
- B's three-release plan (V-B §7.1) — adopted as merged spec's §7 future-release planning narrative, alongside C's R3+R4 target windows.

### What does NOT carry from non-base variants

- A's "Zero breaking changes" claim — replaced by C's accurate framing: limited breaks under migration-guide runway.
- B's full-slate adoption (TU-002/005/006/Q1/Q2 in v3.75) — explicitly rejected per A+C consensus on X-001 through X-003, X-005 through X-007.
- B's `--output-type` flag (even narrowed) — rejected per A+C consensus on C-012/X-005.
- B's 3.0.0 major version bump — rejected; merged spec uses 2.2.0 per C's recommendation (C-013).

### Contested points (carried forward as "considered and not adopted" in merged output)

- B's full-slate adoption with shim runway for Q1/Q2: not adopted, but B's YAML schema and sub-file tree are preserved as R3 reference appendices.
- B's TU-002 output-type axis: not adopted, but the detection rules and gate tables are preserved in Annex B.

### Final base composition (merged output preview)

The merged output uses Variant C's overall structure (10 sections + decision-tree table) with the following overlays:

| Source | Contribution to merged spec |
|--------|------------------------------|
| Variant C (base) | §1 verdict matrix, §3.7 audit log module, §5.3 parameterized tests, §6.2 migration guide table, §8.2 gating investigations, §9 acceptance criteria, §7 R3+R4 future plan with target windows |
| Variant A (overlay) | §5 canonical-form-agnostic preservation test pattern, §6.2 user-facing release-notes pattern, "no new flags" stance carried throughout |
| Variant B (annex / overlay) | §4.4 break-rejection criterion, §6.3 risk-table distillation, Annex B (full YAML schema for R3 reference), Annex C (full skill sub-file tree for R3 reference) |
| Adversarial synthesis | INV-002, INV-005 mitigation notes in §3.5 and §3.7 (from invariant probe); B's full-slate position documented as "considered and not adopted" in §1.7 |
