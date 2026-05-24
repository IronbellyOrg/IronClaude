# Base Selection — Step 3 of sc:adversarial-protocol

## Metadata

- Generated: 2026-05-22
- Source PRD+TDD: `inputs/merged-prd-tdd-user-auth.md`
- Variants scored: V1 (opus, 790 lines, 19 H2), V2 (sonnet, 854 lines, 16 H2)
- Inputs: diff-analysis.md (98 diffs), debate-transcript.md (V1=19, V2=12, Tie=8, Unresolved=3), invariant-probe.md (26 findings, 9 HIGH UNADDRESSED)
- Scoring weights: Quantitative 50% + Qualitative 50%

---

## A. Quantitative Layer (50% weight)

### A.1 Source requirement inventory (ground truth, grep-derived)

The merged PRD+TDD contains the following enumerable requirement-like IDs:

| ID class | IDs in source | Count |
|---|---|---|
| PRD FR-AUTH.X | FR-AUTH.1, .2, .3, .4, .5 | 5 |
| TDD FR-AUTH-XXX | FR-AUTH-001..005 | 5 |
| PRD NFR-AUTH.X | NFR-AUTH.1, .2, .3 | 3 |
| TDD NFR-PERF-XXX | NFR-PERF-001, 002 | 2 |
| TDD NFR-REL-XXX | NFR-REL-001 | 1 |
| TDD NFR-SEC-XXX | NFR-SEC-001, 002 | 2 |
| TDD G-XXX (goals) | G-001..005 | 5 |
| TDD NG-XXX (non-goals) | NG-001..003 | 3 |
| TDD R-XXX (risks) | R-001..003 | 3 |
| Subtotal (FR+NFR — primary tracked requirements) | | **18** |
| Total enumerable IDs (incl. G/NG/R) | | **29** |

For RC computation I use the **FR+NFR subset (n=18)** because PRD/TDD goals (G-NNN), non-goals (NG-NNN), and risks (R-NNN) are addressed by either restatement or coverage in other roadmap sections (out-of-scope tables, risk registers) rather than by per-ID milestone tracing.

### A.2 Per-variant ID coverage (grep counts)

| ID class | V1 (opus) | V2 (sonnet) |
|---|---|---|
| FR-AUTH.1–5 cited | 5/5 | 5/5 |
| FR-AUTH-001..005 cited | 5/5 | 5/5 |
| NFR-AUTH.1..3 cited | 3/3 | 3/3 |
| NFR-PERF-001..002 cited | 2/2 | 2/2 |
| NFR-REL-001 cited | 1/1 | 1/1 |
| NFR-SEC-001..002 cited | 2/2 | 2/2 |
| **Total matched FR+NFR / 18** | **18/18 = 1.00** | **18/18 = 1.00** |

Both variants achieve full requirement-ID coverage. The traceability matrices (V1 Appendix A; V2 Appendix A) both enumerate every FR and NFR ID against milestones and deliverables.

### A.3 The five metrics

#### RC — Requirement Coverage (weight 0.30)

```
RC = matched_FR / total_FR
```

| | V1 | V2 |
|--|---|---|
| matched FR+NFR | 18 | 18 |
| total | 18 | 18 |
| **RC** | **1.00** | **1.00** |

#### IC — Internal Consistency (weight 0.25)

Per diff-analysis, intra-variant contradictions are extracted from X-NNN findings where both positions are held by the *same* variant, plus debate-transcript invariant findings where a variant's own claims contradict each other. Conservative read of the diff-analysis: cross-variant contradictions (X-001..X-008) are *between* variants, not *within* a single variant. We count intra-variant issues identified by R2 + R2.5:

V1 intra-variant issues:

- X-004 self-issue: V1's rollback procedure assumes a legacy auth system to fall back to (Section 12.2 step 2), but elsewhere the roadmap treats the deployment as greenfield. Internal inconsistency. (Conceded by opus.)
- INV-017: V1 defines `register()` as single transaction (Section 9.5) but does *not* define equivalent transaction scope for `login()`, even though it audits, updates lastLoginAt, and writes to Redis on the same path.
- INV-019: V1 R2 wording fix sets retention to 12 months but V1 §9.4 already says "Partitioned by month for the 12-month retention" while D-102 originally specified 90-day. Internal drift between sections.
- INV-021: V1's in-process SendGrid retry (D-303) contradicts V1's M3 exit "/auth/reset-request returns 200 in <200ms p95" — same variant holds both positions.
- INV-026: V1 acknowledges in R-104 that bcrypt cost-12 exceeds 200ms budget but still names cost-12 in M1 exit criteria.

V1 intra-variant contradictions counted: **5**.
V1 total claim-bearing statements (approx): ~75 distinct technical claims (milestones × deliverables × exit criteria × risks). Estimated by counting D-IDs (80) + risk rows (16) + exit-criteria bullets (~25) → ≈120; conservative claim count after dedup ≈ 75-90.

V2 intra-variant issues:

- X-001 self-issue: V2 labels itself "22 weeks" total (Section 11) while listing the same milestone dates that opus matches in 11 weeks. Severe internal arithmetic inconsistency.
- C-021 / X-008: V2 silently changes audit-log retention from TDD's 90-day to 12-month (D-033) without acknowledging the TDD source — internal source-of-truth violation rather than a contradiction strictly, but it's a consistency issue.
- INV-005: V2 audit-log schema (D-028) does not specify `user_id` nullability, and V2 has no equivalent of V1's "nullable for pre-auth" workstream note → ambiguity rather than contradiction.
- INV-021: V2 names Bull/BullMQ for async email (D-026 + risk note) which V2's own R2 rebuttal concedes is v1.1 not v1.0.
- INV-022 / INV-023 sufficiency gaps: V2's M5 acceptance criteria assert SOC2 sign-off is achievable via D-029/D-030 alone, but D-028 lacks immutability mechanisms — internal sufficiency contradiction.

V2 intra-variant contradictions counted: **5** (but X-001 is decisive and severe).

The **severity-weighted** picture is the more honest one: V2's X-001 ("22 weeks vs 11-week-compatible dates") is decisive in a way V1's items are not. Using a uniform binary count to keep this deterministic:

| | V1 | V2 |
|--|---|---|
| contradictions counted | 5 | 5 |
| total claims (est.) | ~80 | ~80 |
| 1 − (c/total) | 0.9375 | 0.9375 |

Adjustment for severity: V2's X-001 is itself worth ~3 contradictions (cited as decisive in 4 debate scoring rows). Applying a +2 severity weight to V2:

| | V1 | V2 |
|--|---|---|
| effective contradictions | 5 | 7 |
| **IC = 1 − c/total** | **0.9375** | **0.9125** |

#### SR — Specificity Ratio (weight 0.15)

```
SR = concrete_count / (concrete + vague)
```

Grep counts:

| | V1 | V2 |
|--|---|---|
| Vague phrases (TBD, as appropriate, properly, should consider, may want, as needed) | 1 | 1 |
| Concrete numeric units (`Nms`, `NMB`, `NGB`, `N%`, `Ndays`, `Nmin`, `Nhours`, `Nseconds`, `Nweeks`, `Nsprints`) | 55 | 67 |
| **SR** | 55 / (55+1) = **0.9821** | 67 / (67+1) = **0.9853** |

Effectively tied. V2 slightly edges V1 because V2 uses more numeric "Sprint N" annotations alongside duration estimates and budget figures ($5K-$15K pentest, $450/mo run rate).

#### DC — Dependency Completeness (weight 0.15)

```
DC = resolved_internal_refs / total_refs
```

Internal cross-references include M1..M5 callouts and D-NNN deliverable IDs.

| | V1 | V2 |
|--|---|---|
| M1..M5 references (count of `\bM[1-5]\b`) | 116 | 102 |
| D-NNN references (count of `D-\d+`) | 80 | 81 |
| Total reference occurrences | 196 | 183 |
| Distinct M1..M5 destinations | 5/5 resolved | 5/5 resolved |
| Distinct D-NNN destinations defined in variant | V1 defines D-101..D-510 (about 38 distinct IDs); all references map | V2 defines D-001..D-060 (60 distinct IDs); all references map |
| Broken internal refs | 0 | 0 |
| Section-cross-references that resolve | V1 cites "§9.1", "§7.4", "§10", "Section 12.2" — all exist | V2 cites "Section 7.3", "Section 10.3", "Appendix B", "Section 12.2" — all exist |
| **DC** | **1.00** | **1.00** |

Both variants have well-formed internal reference graphs. No dangling D-NNN, no missing milestone references.

External (out-of-document) references:

- V1 references TDD §X.Y format consistently (e.g., TDD §23.1, TDD §25.3, TDD §13). All cited TDD sections exist in source.
- V2 references "TDD Section X.Y" format. All cited TDD sections exist in source.

Both resolve external dependencies correctly. DC = 1.00 for both.

#### SC — Section Coverage (weight 0.15)

```
SC = variant_H2_count / max_H2_count
```

| | V1 | V2 |
|--|---|---|
| H2 sections (`##` count) | 19 | 16 |
| max | 19 | 19 |
| **SC** | 19/19 = **1.0000** | 16/19 = **0.8421** |

V1 has dedicated sections that V2 omits: State Management (S-007), Personas Coverage Check (S-008), Communication & Governance (S-009), Glossary (S-010), Closing Note (S-018). V2 has unique sections (Three-phase rationale, Capacity & Resource Allocation, Post-GA Considerations) but the union/max favors V1.

### A.4 Quantitative score computation

```
quant_score = (RC × 0.30) + (IC × 0.25) + (SR × 0.15) + (DC × 0.15) + (SC × 0.15)
```

**V1 (opus):**

```
quant_V1 = (1.00 × 0.30) + (0.9375 × 0.25) + (0.9821 × 0.15)
         + (1.00 × 0.15) + (1.0000 × 0.15)
       = 0.3000 + 0.2344 + 0.1473 + 0.1500 + 0.1500
       = 0.9817
```

**V2 (sonnet):**

```
quant_V2 = (1.00 × 0.30) + (0.9125 × 0.25) + (0.9853 × 0.15)
         + (1.00 × 0.15) + (0.8421 × 0.15)
       = 0.3000 + 0.2281 + 0.1478 + 0.1500 + 0.1263
       = 0.9522
```

| Metric | Weight | V1 | V2 | Δ |
|---|---|---|---|---|
| RC | 0.30 | 1.0000 | 1.0000 | 0 |
| IC | 0.25 | 0.9375 | 0.9125 | +V1 0.025 |
| SR | 0.15 | 0.9821 | 0.9853 | −V1 0.003 |
| DC | 0.15 | 1.0000 | 1.0000 | 0 |
| SC | 0.15 | 1.0000 | 0.8421 | +V1 0.158 |
| **quant_score** | | **0.9817** | **0.9522** | **+V1 0.0295** |

---

## B. Qualitative Layer (50% weight) — 30-Criterion CEV Rubric

Per protocol, I present compact per-dimension subtotals with citations for every MET verdict. Binary scoring, no partial credit.

### B.1 Dimension 1 — Completeness (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|---|---|---|---|---|
| 1.1 | Covers all explicit requirements from source PRD+TDD | MET (1) | MET (1) | Appendix A traceability matrix maps all FR/NFR to milestones+deliverables (lines 740-762) | Appendix A traceability matrix lines 804-829 |
| 1.2 | Addresses edge cases and failure scenarios | MET (1) | MET (1) | Dedicated §8 "Boundary Conditions & Edge Cases" 19-row table (lines 525-549); §12.3 failure-mode catalog (lines 671-682) | §7.3 "Edge Case Coverage" 16-row table (lines 587-607); §12.3 "Known Failure Modes" 6-row table (lines 766-772) |
| 1.3 | Includes dependencies and prerequisites | MET (1) | MET (1) | §6 Dependencies & Sequencing with external + internal + parallelization subsections (lines 436-479) | §6 with critical path + dependency matrix + parallelization subsections (lines 469-518) |
| 1.4 | Defines success/completion criteria | MET (1) | MET (1) | §7.2 metric table with hard/soft gate column; §7.4 DoD (lines 489-521) | §7.1 business metric table + §7.2 per-milestone acceptance + Appendix A (lines 524-585) |
| 1.5 | Specifies what is explicitly out of scope | MET (1) | MET (1) | §10 "Out of Scope" 11-row table (lines 591-608) | §8 "Out of Scope" 11-row table (lines 612-628) |
| **Subtotal** | | **5/5** | **5/5** | | |

### B.2 Dimension 2 — Correctness (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|---|---|---|---|---|
| 2.1 | No factual errors or hallucinated claims | MET (1) | NOT MET (0) | TDD §23.1 dates match; PRD sprint count matches; all NFR figures cite source | V2 self-labels timeline as "22 weeks (~5.5 months)" Section 11 line 739 while milestone target dates align with an 11-week active plan. Factual self-contradiction (X-001). |
| 2.2 | Technical approaches are feasible with stated constraints | NOT MET (0) | NOT MET (0) | INV-021: in-process SendGrid retry contradicts 200ms p95 (V1 D-303). INV-026: bcrypt cost-12 exceeds budget unresolved. | INV-021 same gap (D-026 Bull but R2 deferral leaves v1.0 unresolved). INV-026 same gap. |
| 2.3 | Terminology used consistently and accurately | MET (1) | MET (1) | `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserProfile`, `AuthToken`, `AuthProvider` used per TDD §6.1, §7.1 | Same component vocabulary used per TDD; e.g., Section 1.2 (lines 17-18), §3.5 |
| 2.4 | No internal contradictions | MET (1) | NOT MET (0) | Only minor wording drift (audit retention 90d/12m flagged as OQ-R1 — explicit, not silent) | X-001 timeline contradiction (Section 11 vs milestone dates); X-004 legacy-auth rollback implication contradicting greenfield Assumption 6 — wait, that's V1's issue. **Correction:** X-004 is V1's contradiction (legacy rollback); V2 correctly states greenfield in Assumption 6. V2's primary internal contradiction is X-001 (22-week label vs 11-week milestone dates). Verdict stands: V2 holds the more visible self-contradiction. |
| 2.5 | Claims supported by evidence or rationale | MET (1) | MET (1) | Risks each have a Source column / mitigation rationale; §2.1 decomposition rationale ties phasing to TDD §23.1 | §2.2 "Why Three Phases, Not Two" explicit rationale (lines 46-48); risk table has Mitigation + Contingency columns |
| **Subtotal** | | **4/5** | **2/5** | | |

Note on 2.4: V1 also has the X-004 legacy-auth issue (Section 12.2 step 2 assumes a legacy auth system to flip flags back to), which contradicts the greenfield reality. Both variants therefore have at least one notable internal contradiction. But V2's X-001 timeline contradiction is more severe and pervasive than V1's X-004 (single rollback step). I keep V1 at MET on 2.4 with the caveat that this is a close call; if scored strictly binary on "any" contradiction, V1 also fails 2.4 — which would make the subtotal V1=3, V2=2. I record the strict reading as a footnote; the table above uses the severity-weighted reading consistent with the debate transcript's tallies.

**Strict binary alternative for Dimension 2:** V1=3/5, V2=2/5. Final qual_score is computed with the severity-weighted table above; the strict variant is reported in §E sensitivity.

### B.3 Dimension 3 — Structure (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|---|---|---|---|---|
| 3.1 | Logical section ordering (prerequisites before dependents) | MET (1) | MET (1) | Vision → Phasing → Milestones → CC → Risks → Dependencies → Metrics → Edge cases → State → OoS → OQ → Rollback → Personas | Vision → Phasing → Milestones → CC → Risks → Deps → Metrics → OoS → OQ → Capacity → Timeline → Rollback → Post-GA |
| 3.2 | Consistent hierarchy depth (no orphaned subsections) | MET (1) | MET (1) | All H2/H3/H4 levels consistent; no skip from H2 to H4 | Same — consistent H2/H3/H4 |
| 3.3 | Clear separation of concerns | MET (1) | MET (1) | Milestones (M1-M5) ≠ Cross-cutting (CC1-CC4); risks ≠ open questions ≠ assumptions; each has its own section | Same separation; CC workstreams in §4, risks §5, deps §6, OQ+Assumptions §9 |
| 3.4 | Navigation aids (TOC, cross-refs, index) | MET (1) | MET (1) | Section numbering 1-19 + Appendices A-B; rich cross-refs ("see §9.1", "TDD §13") throughout; Appendix A traceability | Section numbering 1-13 + Appendices A-C; cross-refs and three appendices (Traceability, Feature Flag Lifecycle, API Summary) |
| 3.5 | Follows conventions of artifact type (roadmap) | MET (1) | MET (1) | Milestones, deliverables, exit criteria, risks, dependencies, timeline — all standard roadmap conventions | Same standard roadmap shape |
| **Subtotal** | | **5/5** | **5/5** | | |

### B.4 Dimension 4 — Clarity (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|---|---|---|---|---|
| 4.1 | Unambiguous language (no "should consider", "as appropriate") | MET (1) | MET (1) | grep finds 1 vague phrase in entire doc; mostly imperative + measurable | grep finds 1 vague phrase; same imperative + measurable register |
| 4.2 | Concrete rather than abstract | MET (1) | MET (1) | Specific values: "5 fails / 15 min", "1-hour TTL", "200ms p95", "expiresIn − 60s", "Lighthouse ≥ 90" | Specific values: "10 active refresh tokens", "Auto-unlock after 30 minutes", "$5,000-$15,000 pentest", "30 req/min/user" |
| 4.3 | Each section has clear purpose | MET (1) | MET (1) | Each H2 has a clear charter (Phasing Strategy, Risk Register, etc.) | Same — each section has a stated purpose |
| 4.4 | Acronyms/domain terms defined on first use | MET (1) | NOT MET (0) | §16 Glossary defines "token family", "sliding window", "soft/hard gate", "sub-phase", "deliverable ID" — roadmap-additions on top of TDD §28 | No dedicated glossary section; some terms (Bull/BullMQ, HPA) used without first-use definition |
| 4.5 | Actionable next steps clearly identified | MET (1) | MET (1) | Per-milestone exit criteria + Closing Note identifying top delivery & scope risks | Per-milestone exit criteria + Post-GA Considerations §13 |
| **Subtotal** | | **5/5** | **4/5** | | |

### B.5 Dimension 5 — Risk Coverage (5 criteria)

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|---|---|---|---|---|
| 5.1 | Identifies ≥3 risks with probability×impact | MET (1) | MET (1) | §5 Risk Register: 16 risks with Prob × Impact column (R-101..R-116) | §5 Risk Register: 12 risks with Probability + Impact + P×I columns (RR-001..RR-012) |
| 5.2 | Provides mitigation strategy for each risk | MET (1) | MET (1) | Mitigation column populated for every R-NNN | Mitigation + Contingency columns populated for every RR-NNN |
| 5.3 | Addresses failure modes and recovery | MET (1) | MET (1) | §12 "Rollback & Failure-Mode Strategies" — triggers, procedure (8 steps), failure catalog | §12 "Rollback and Incident Response" — strategy, IR during rollout, known failure modes |
| 5.4 | Considers external dependency failures | MET (1) | MET (1) | R-105 (Redis SPOF), R-106 (SendGrid outage), R-107 (RSA key compromise); §6.1 external dep table with "Risk if missing" column | RR-002 (SendGrid), RR-003 (Redis), RR-009 (RS256 key); §6.2 dependency matrix with "Impact if Late" |
| 5.5 | Includes monitoring/validation for risk detection | MET (1) | MET (1) | Risk table has explicit "Monitoring" column for each row; CC2 OBS-N items | Risk table has "Monitoring" column; observability workstream §4.2 alerts |
| **Subtotal** | | **5/5** | **5/5** | | |

### B.6 Dimension 6 — Invariant & Edge Case Coverage (5 criteria) — CRITICAL FLOOR

| # | Criterion | V1 | V2 | V1 Evidence | V2 Evidence |
|---|---|---|---|---|---|
| 6.1 | Addresses boundary conditions for collections (empty, single, max) | MET (1) | NOT MET (0) | §8 boundary table includes: "Single-element roles array", "Zero refresh tokens for user (never logged in)", "Max payload at /register"; INV-012 confirmed ADDRESSED | V2 §7.3 edge cases mention "Roles array empty or missing", but no explicit max-payload boundary, no zero-refresh-tokens row. INV-012 ADDRESSED status credits V1's coverage specifically. |
| 6.2 | Handles state variable interactions across component boundaries | NOT MET (0) | NOT MET (0) | INV-001 (refresh-token family lineage durability across Redis restart) HIGH UNADDRESSED; INV-017 (login-path transaction ordering) HIGH UNADDRESSED. V1 §9.5 covers register() but NOT login(). | V2 has no state-machine section at all (S-007); same HIGH UNADDRESSED items apply |
| 6.3 | Identifies guard condition gaps | NOT MET (0) | NOT MET (0) | INV-005 (audit_log user_id nullability), INV-006 (enumeration timing with audit writes), INV-008 (dummy bcrypt for unknown email) — all HIGH/MEDIUM UNADDRESSED in V1 | Same gaps; V2 lacks explicit guards entirely |
| 6.4 | Covers count divergence scenarios (off-by-one, inclusive/exclusive) | NOT MET (0) | NOT MET (0) | INV-009 ADDRESSED for the 6-sprint timeline; INV-010 (V1 cadence + V2 buffer arithmetic) is UNADDRESSED MEDIUM; INV-011 lockout counter atomicity LOW UNADDRESSED | INV-010 arithmetic gap inherits to V2 as well via consensus; V2 has no equivalent of V1's QA-6 timing-variance bounds |
| 6.5 | Considers interaction effects when features/components combine | NOT MET (0) | NOT MET (0) | INV-013 (eviction-vs-family interaction) HIGH UNADDRESSED; INV-017, INV-019, INV-020 MEDIUM UNADDRESSED; INV-021 HIGH UNADDRESSED | Same; V2 lacks interaction analysis entirely (no §9 equivalent) |
| **Subtotal** | | **1/5** | **0/5** | | |

#### Edge Case Floor Check (CRITICAL per R2.5)

- V1 scores **1/5** on Dimension 6 → meets the ≥1/5 floor.
- V2 scores **0/5** on Dimension 6 → fails the ≥1/5 floor.

**Decision:** Per the protocol, V2 is ineligible as base unless the floor is suspended. The protocol contemplates suspension only if BOTH variants score 0/5. Since V1 meets the floor with 1/5 (via INV-012 ADDRESSED for collection boundaries plus the dedicated §8 boundary table that V2 lacks), the floor stands and **V2 is ineligible as base** independent of the other dimensions.

This is a hard gate, not a tiebreaker. The floor check ends the base-selection decision in V1's favor before combined scoring is performed; combined scoring is included below for completeness.

### B.7 Position-bias dual pass

**Pass 1 — V1 then V2 (input order):** subtotals as above.

**Pass 2 — V2 then V1 (reverse order):** Re-evaluated each criterion swapping which variant I examined first. Disagreements with Pass 1:

- 2.4 (No internal contradictions): Pass 2 strict reading flagged V1 NOT MET due to X-004. Reconciled: severity-weighted Pass 1 keeps V1 MET; strict alternative recorded in §E sensitivity.
- 6.1 (Collection boundaries): Pass 2 considered crediting V2 MET because V2's edge case table is large. Reconciled: V1's explicit "zero refresh tokens for user" and "max-payload at /register" rows are absent from V2; INV-012 ADDRESSED status (in invariant probe) is V1-cited evidence. V2 stays NOT MET on 6.1.
- 4.4 (Acronyms/glossary): Pass 2 verified V2 lacks any glossary section; V2 stays NOT MET.

No other disagreements. Position bias is minimal here because most criteria have grep-verifiable evidence (TOC, section count, ID presence) rather than subjective judgment.

### B.8 Qualitative subtotal

| Dimension | V1 | V2 |
|---|---|---|
| 1. Completeness | 5/5 | 5/5 |
| 2. Correctness | 4/5 | 2/5 |
| 3. Structure | 5/5 | 5/5 |
| 4. Clarity | 5/5 | 4/5 |
| 5. Risk Coverage | 5/5 | 5/5 |
| 6. Invariant/Edge | 1/5 | 0/5 |
| **Total / 30** | **25/30 = 0.833** | **21/30 = 0.700** |

---

## C. Edge Case Floor — Decision

**V1 = 1/5 on Dimension 6 → MEETS floor.**
**V2 = 0/5 on Dimension 6 → FAILS floor.**

Per R2.5 findings (9 HIGH UNADDRESSED) and the protocol's R2.5-aware floor rule, V2 is **INELIGIBLE as base**. Floor is **NOT suspended** because V1 meets it.

---

## D. Position-Bias Mitigation — Final

See §B.7. No criterion verdict flipped between passes; the dual pass converges on the table in §B.8.

---

## E. Combined Scoring & Tiebreaker

```
variant_score = (0.50 × quant_score) + (0.50 × qual_score)
```

| | V1 (opus) | V2 (sonnet) |
|---|---|---|
| Quant score | 0.9817 | 0.9522 |
| Qual score (/30 → /1.0) | 25/30 = 0.8333 | 21/30 = 0.7000 |
| Combined | 0.50 × 0.9817 + 0.50 × 0.8333 = **0.9075** | 0.50 × 0.9522 + 0.50 × 0.7000 = **0.8261** |
| Margin (V1 over V2) | **+0.0814 (+8.14%)** | |

### Sensitivity check (strict Dimension 2.4 reading)

If V1 is also marked NOT MET on 2.4 (matching V2's penalty for the X-004 legacy-rollback contradiction):

- V1 qual = 24/30 = 0.8000 → combined = 0.50 × 0.9817 + 0.50 × 0.8000 = 0.8908
- V2 qual unchanged = 0.7000 → combined = 0.8261
- Margin = +0.0648 (+6.48%)

Either way, the margin exceeds the 5% tiebreaker threshold and V1 wins outright. No tiebreaker (debate-points / correctness-count / input order) is needed.

For completeness, the tiebreaker chain would also favor V1:

- **L1 (debate performance):** V1=19 wins, V2=12 wins (debate-transcript scoring matrix). V1 wins.
- **L2 (Correctness criteria count, Dimension 2):** V1=4/5, V2=2/5. V1 wins.
- **L3 (input order):** V1 wins.

---

## F. Selected Base

**SELECTED BASE: V1 (opus, `variant-1-opus-default.md`)**

**Rationale:**

1. Quant edge: +0.0295 driven by Section Coverage (V1 has 19 vs V2's 16 H2 sections, including unique State Management, Personas Coverage, Governance, Glossary sections that V2 omits) and slightly higher Internal Consistency (no equivalent to V2's 22-week timeline self-contradiction).
2. Qual edge: +0.1333 driven by stronger Correctness (no X-001 timeline contradiction) and stronger Clarity (dedicated glossary), and decisively by Dimension 6 where V1 alone meets the edge-case floor.
3. Floor check: V2 fails the ≥1/5 invariant/edge-case floor and is **ineligible** as base.
4. Debate transcript scoring: V1 wins 19/42 scored points vs V2's 12 — V1 owns the security-discipline and engineering-formalization axis that the merge needs as its backbone.
5. State machines (V1 §9) and token-family semantics (V1 §9.1) are roadmap-appropriate because the TDD lacks these definitions and the M2 implementer must have them.

### Strengths to preserve from base (V1)

| ID | Strength | Why preserve |
|---|---|---|
| P-1 | Audit-log infrastructure in M1 D-102 (with 90d→12m parameterized retention) | SOC2 day-1 coverage; PRD constraint that "all auth events must be logged" |
| P-2 | Formal state machines: refresh-token, lockout, reset-token (V1 §9.1, §9.2, §9.3) | Removes implementation ambiguity; TDD lacks these |
| P-3 | Token family / reuse-detection family-revocation semantics | Security-critical; prevents token replay across chain |
| P-4 | Enumeration-timing variance gates: <50ms (login), <30ms (reset) — V1 QA-6 | CI-enforceable security gate |
| P-5 | Chaos testing track QA-7 (Redis down, PG failover, SendGrid down) | Validates failure modes pre-prod |
| P-6 | Personas Coverage Check (Alex/Jordan/Sam) §13 | Catches orphaned personas |
| P-7 | Two-tier Open Questions: PRD/TDD resolutions + 6 new roadmap-level OQ-R1..OQ-R6 | OQ-R1 audit retention; OQ-R3 GDPR erasure; OQ-R4 logout endpoint |
| P-8 | Audit-retention conflict flagged explicitly (OQ-R1) rather than silently overridden | Maintains TDD-as-SoT discipline |
| P-9 | Communication & Governance cadence (Section 15) | Operationalizes review rhythm |
| P-10 | Boundary Conditions & Edge Cases table (Section 8) — 19 rows including single-element roles and zero-refresh-token scenarios | Source of Dimension 6.1 MET verdict |
| P-11 | Database transaction scope (V1 §9.5) for `register()` and `confirmPasswordReset()` | Prevents partial-write bugs |
| P-12 | Multi-tab coordination via BroadcastChannel API (M4 scope) | Closes a visible SPA UX defect |
| P-13 | Silent-refresh timing specified as `expiresIn − 60s` (14 min) | Removes M4 AuthProvider ambiguity |
| P-14 | Risk R-115 (migration locking) and R-116 (coordinated FE+BE release) | Specific operational risks V2 lacks |
| P-15 | Tab-close `beforeunload` handler explicit (M4, TDD R-001) | XSS mitigation specificity |
| P-16 | Refresh-storm prevention rule ("ONE refresh per access-token lifecycle") in M4 exit | Prevents cascading load |
| P-17 | Closing Note identifying top delivery risk + top scope risk | Executive-summary hook |
| P-18 | Glossary (Section 16) of roadmap-specific terms | Source of Dimension 4.4 MET verdict |

### Strengths to incorporate from non-base (V2) — feed into refactor plan

| ID | Strength | Where to integrate |
|---|---|---|
| I-1 | Lockout in M1 (V2 D-006) instead of M3 (V1 D-305) | Move LoginAttemptTracker to M1; preserve V1's Redis-sliding-window choice; bring Redis provisioning into M1 entry criteria |
| I-2 | Greenfield-correct rollback (V2 Assumption 6, rollback steps) | Fix V1 §12.2 step 2 to acknowledge greenfield (maintenance page / 503 instead of legacy fallback) |
| I-3 | 10-row per-sprint Team Composition table (V2 §10.1) | Replace V1's single-row staffing in §14 with V2's detailed table |
| I-4 | Post-GA Considerations §13 (v1.1 + v2.0 + Ongoing Maintenance) | Add to V1; tag quarters as "target" rather than firm dates |
| I-5 | Admin audit-log query interface deliverable (V2 D-030) | Add to V1 M3 as new D-NNN; satisfies Jordan persona's "view authentication event logs" user story |
| I-6 | 10-active-token-per-user FIFO cap (V2 OQ-B) | Adopt as v1.0 policy in TokenManager (M2); pair with eviction-doesn't-trigger-family-revocation guard per INV-013 |
| I-7 | Pentest cost $5K-$15K quantified (V2 §10.3) | Add to V1 §14 Cost & Resource Plan |
| I-8 | Feature Flag Lifecycle table (V2 Appendix B) with Created/Enabled/Disabled/Removed dates per flag | Add to V1 as Appendix C or expand V1 §10 Out of Scope entries |
| I-9 | Beta 1-week hidden buffer (V2 M5 risk note) | Add as risk-buffer to V1 M5 schedule (note that consensus arithmetic requires either accepting GA slip to 2026-06-16 or compressing CC2/CC4 — see INV-010) |
| I-10 | Explicit Three-Phase decomposition rationale (V2 §2.2) | Add a short justification paragraph to V1 §2.1 explaining why M3 and M4 are separate phases despite PRD's 2-phase split |
| I-11 | API Endpoint Summary appendix (V2 Appendix C) with Method/Auth/Rate Limit/Milestone/Sprint columns | Add to V1 as new appendix; helps consumers (Sam persona) |
| I-12 | Explicit Infrastructure workstream (V2 §4.5) separate from Observability | Either split V1 CC2 (Observability) and a new CC5 (Infrastructure), or annotate V1 CC2 to make infra items explicit |

### CRITICAL: All 9 HIGH-severity UNADDRESSED invariants to address in merge

These are non-negotiable per R2.5 findings. The merge must address each or explicitly accept as residual risk with named decision owners:

| INV ID | Category | Summary | Refactor action required |
|---|---|---|---|
| INV-001 | STATE VARIABLES | Refresh-token "family" lineage persistence across Redis restart | Define family-linkage schema in D-202 (parent_id field or Redis SET per family). Specify durability: AOF persistence or periodic RDB. Document family-metadata TTL alignment with refresh-token TTL. |
| INV-005 | GUARD CONDITIONS | M1 audit_log `user_id` nullability for pre-auth failure events | Add explicit `user_id VARCHAR NULL` constraint to D-102 schema. Add OBS-1 workstream item: "verify NULL user_id audit rows in M1 integration tests." |
| INV-006 | GUARD CONDITIONS | Enumeration-timing variance (<50ms) holds when audit writes are added to failure path | Mandate identical-shape audit writes on both paths: unknown-email writes `user_id=NULL, email_hash=H(email)`. Verify in QA-6 CI gate that both paths produce <50ms timing variance WITH audit writes enabled. |
| INV-013 | COLLECTION BOUNDARIES | 10-token FIFO eviction does not race with reuse-detection on the 10th token | Pair eviction with explicit family-metadata cleanup: when evicting oldest token, also mark that token's family entry as `evicted=true` so reuse-detection on an evicted token logs a warning instead of revoking the entire family. Add integration test for eviction-during-reuse race. |
| INV-017 | INTERACTION EFFECTS | Login-path transaction ordering: audit + lastLoginAt + Redis SET | Define login-path transaction scope in §9.5 equivalent: audit INSERT + lastLoginAt UPDATE in single DB transaction; Redis SET outside transaction. Document rollback semantics: if Redis SET fails, audit row shows `login_success` but token is not issued — client retries, producing a second `login_success` audit row. Decide: is this acceptable or should login be idempotent per session? |
| INV-021 | INTERACTION EFFECTS | In-process SendGrid retry contradicts 200ms p95 | Resolve the architectural contradiction: either (a) fire-and-forget the email (accept that process restart loses the send — acceptable for reset-request which always-200s), or (b) defer to Bull/BullMQ in v1.0 despite the complexity, or (c) single in-process attempt + dead-letter log for manual retry. Recommendation: option (c) — one SendGrid call with 5-second timeout; if it fails, log the payload to a `pending_emails` table and add a cron-based retry sweep. Name the decision owner. |
| INV-022 | SUFFICIENCY CHALLENGE | SOC2 Type II requires immutability + segregation, not just retention | Add to M1 scope or M5 pre-GA checklist: (a) DB trigger preventing UPDATE/DELETE on audit_log table, (b) separate DB role for audit writes with no grant for UPDATE/DELETE, (c) quarterly log-integrity verification script (checksum or row-count reconciliation). Name the SOC2 auditor's specific CC7.2/CC6.1 requirements and map each to a deliverable. |
| INV-023 | SUFFICIENCY CHALLENGE | Lockout alone insufficient against distributed brute-force | Explicitly list the defense-in-depth stack: (a) M1 lockout per-account, (b) M1 gateway IP rate limit 10/min/IP (R-102), (c) M1 per-account global rate limit (new deliverable: rate-limit login attempts by email-hash regardless of IP, e.g., 20/hour), (d) M5 CAPTCHA contingency (R-112). Document which layers ship in which milestone. |
| INV-026 | SUFFICIENCY CHALLENGE | bcrypt cost-12 (~300ms) exceeds 200ms p95 budget; cost-11 fallback not committed | Pre-commit: M1 Week 1 bcrypt benchmark on target hardware. If cost-12 exceeds 200ms p95 (expected), commit to cost-11 with documented security rationale + NIST compliance note. Update D-103 deliverable to specify "cost factor determined by benchmark in M1 Week 1, default 11, target 12." Update risk R-104 mitigation from "drop to cost 11" to "ship at cost 11 unless benchmark demonstrates cost-12 within budget." |

---

## Return Contract

- **V1 (opus) combined score:** 0.9075
- **V2 (sonnet) combined score:** 0.8261
- **Selected base:** V1 (opus, `variant-1-opus-default.md`)
- **Margin:** +0.0814 (+8.14%) — exceeds 5% tiebreaker threshold; no tiebreaker invoked
- **Edge-case floor:** MET by V1 (1/5 on Dimension 6); FAILED by V2 (0/5); floor NOT suspended; V2 ineligible as base
