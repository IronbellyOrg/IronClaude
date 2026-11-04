# Base Selection Report

## Metadata
- Decision: D5, should Orca's nesting depth be raised (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:350-354`)
- Variant 1 = `variant-1-original.md` (option a, keep depth 1); Variant 2 = `variant-2-original.md` (option b, raise depth)
- Scored by the debate-orchestrator, 2026-11-02T16:23:15Z. Inputs: the two variant files, `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `scoring/qual-pass-1.md` (input order), `scoring/qual-pass-2.md` (reverse order).
- Variants are scored as written. Debate concessions count against the conceding variant, as both scoring passes applied.
- Citation key: `V1:N` / `V2:N` = variant line; `DA` = `diff-analysis.md`; `P1` / `P2` = `scoring/qual-pass-1.md` / `scoring/qual-pass-2.md`; `R1-V1` ... `R2-V2` = round files; `INV-NNN` = `invariant-probe.md`; `SPEC:N` / `CAPS:N` as in the variants.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (option a) | Variant 2 (option b) |
|---|---|---|---|
| requirement_coverage (RC) | 0.30 | 0.933 (14 / 15 topics) | 0.933 (14 / 15 topics) |
| internal_consistency (IC) | 0.25 | 1.000 (0 contradictions / 23 claims) | 0.913 (2 contradictions / 23 claims) |
| specificity_ratio (SR) | 0.15 | 0.917 (11 concrete / (11 + 1 vague)) | 1.000 (12 concrete / (12 + 0 vague)) |
| dependency_completeness (DC) | 0.15 | 0.889 (8 / 9 references resolved) | 0.750 (6 / 8 references resolved) |
| section_coverage (SC) | 0.15 | 0.800 (4 / 5 H2 sections) | 1.000 (5 / 5 H2 sections) |
| **quant_score** | | **0.921** (0.92083) | **0.921** (0.92076) |

Arithmetic: V1 = 0.30 x 0.9333 + 0.25 x 1.000 + 0.15 x 0.9167 + 0.15 x 0.8889 + 0.15 x 0.800 = 0.2800 + 0.2500 + 0.1375 + 0.1333 + 0.1200 = 0.92083. V2 = 0.30 x 0.9333 + 0.25 x 0.9130 + 0.15 x 1.000 + 0.15 x 0.750 + 0.15 x 1.000 = 0.2800 + 0.2283 + 0.1500 + 0.1125 + 0.1500 = 0.92076. The quantitative layer does not separate the variants (difference 0.00007).

### Computation details
**RC: topic coverage, not requirement IDs.** The source decision (`SPEC:350-354`) carries no FR/NFR/R requirement IDs, so the protocol's edge case applies: section-level topic matching. Topic set (15, fixed before matching): the four decision areas both variants were asked to cover (safety, reliability, day-to-day use, implementation cost) plus the eleven C-NNN topics in `diff-analysis.md` (C-001 to C-011). C-007 and C-009 overlap the cost and day-to-day areas; they are kept as listed so the set is reproducible. A topic counts as covered when the variant has a statement on it; coverage per topic follows the diff analysis rows.
- Variant 1 misses C-004 (heartbeat gaps; DA C-004 "Not addressed"). 14 / 15.
- Variant 2 misses C-008 (reversibility; DA C-008 "does not discuss reversing it"). 14 / 15.

**IC: claims and contradictions.** Scorable claims are specific, falsifiable statements in the body; proposals ("the spec can revisit it if ...") are not counted. Variant 1: 23 claims (V1:3 three, V1:8 five, V1:9 three, V1:12 four, V1:13 four (R2-R5), V1:16 two, V1:19 two), 0 contradictions (DA X-003: "Consistent"). Variant 2: 23 claims (V2:3 two, V2:8 six, V2:9 one, V2:10 one, V2:13 three, V2:16 five, V2:19 two, V2:22 three), 2 contradicting claim pairs, both from DA X-003: V2:8 "Depth 2 would give each sub-unit its own Task and Dispatch" against V2:16 "Depth alone does not make the rejected design work", and V2:8 against V2:22 "No phase of the spec uses it". V2:13 "Removes Orca's fence" contradicts the sources (`CAPS:99-100`), not another V2 claim, so it is scored under qualitative Correctness, not IC.

**SR: concrete versus vague statements.** Unit: one sentence in the position line or a bullet; headings, the title and the citation-key line excluded. Concrete: contains a number, named entity, file or setting name, rule ID or line citation. Vague: contains a listed vague indicator. A sentence with neither ("No change.", "No phase of the spec uses it.") is excluded from both counts. Vague-word search over both files (`appropriate|as needed|properly|adequate|should consider|might|various|etc.|best practices|industry standard`) matched once: V1:19 "inadequate" (the revisit condition names no measure of inadequacy). Concrete sentences: V1 = 11 (V1:3 one, V1:8 two, V1:9 two, V1:12 two, V1:13 one, V1:16 one, V1:19 two); V2 = 12 (V2:3 one, V2:8 three, V2:9 one, V2:10 one, V2:13 two, V2:16 two, V2:19 one, V2:22 one).

**DC: internal references.** References counted: identifier-style terms a reader must resolve (citation-key prefixes, rule and requirement IDs, phase IDs). Resolved when the variant itself defines or glosses the term. Section numbers that point into another document (V2:3 "section 1.3") are external and excluded, per the protocol's edge case.
- Variant 1 (9): `SPEC:N` and `CAPS:N` (defined at V1:5), WC-8 and SA-2 (glossed together, "commands never call Orca", V1:12), R2, R3, R4, R5 (each glossed, V1:13) = 8 resolved; P0 (V1:19, "P0 smoke runs") not defined = unresolved.
- Variant 2 (8): `SPEC:N` and `CAPS:N` (V2:5), WC-10 (glossed as "a heartbeat gap the spec has to accept", V2:8), R2, R3, R4 (glossed, V2:16) = 6 resolved; SA-2 and "non-goal 1" (V2:22) not glossed = 2 unresolved.

**SC: H2 sections.** `grep -c '^## '`: Variant 1 = 4, Variant 2 = 5 (V2 adds "Strongest case for it"). Maximum 5.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts after position-bias resolution. Where Pass 1 and Pass 2 agreed, the shared CEV evidence is summarized; full CLAIM/EVIDENCE/VERDICT text is in `P1` and `P2`. The two rows the passes disagreed on are marked **[re-evaluated]** and resolved in "Position-Bias Mitigation" below. MET = 1, NOT MET = 0; a MET verdict always carries a citation.

### Completeness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|---|---|---|---|---|
| 1. Covers all explicit requirements | MET | All four areas have cited bullets: "## Safety" (V1:7), "## Reliability" (V1:11), "## How a person works day to day" (V1:15), "## Implementation cost" (V1:18). P1, P2 agree. | MET | Same four areas at V2:12, 15, 18, 21, plus "Strongest case" (V2:7). P1, P2 agree. |
| 2. Edge cases and failure scenarios | MET | Malformed value "falls back to the default rather than disabling the fence"; "a new Run does not reset depth" (V1:8; `CAPS:100-101`); R2-R5 failures (V1:13). | MET | R2, R3, R4 failure modes and the unverified enforcement call sites (V2:16; `CAPS:103`). |
| 3. Dependencies and prerequisites | MET | Records depend on coordinator Task splitting (V1:12, `SPEC:42`); setting location `orca-data.json:1` (V1:9). The unstated root-coordinator precondition (INV-001) is noted, but one stated dependency meets the criterion. | MET | "using it means rewriting commands to call Orca, against SA-2 and non-goal 1" (V2:22). |
| 4. Success / completion criteria | MET | "the spec can revisit it if P0 smoke runs (`SPEC:181`) show coordinator-side splitting is inadequate" (V1:19). Its unworkability (R2-V1 item 3) is scored under Risk 5. | NOT MET | No condition for choosing (b): DA S-003; conceded in R2-V2 item 14. |
| 5. Out-of-scope items | NOT MET | No evidence found; searched V1:1-19 for "scope", "out of scope", "non-goal". | NOT MET | No evidence found; V2:22's "non-goal 1" is a constraint on (b), not a scope boundary. |
| **Subtotal** | **4/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|---|---|---|---|---|
| 1. No factual errors | MET | DA spot-check rows 1-3 CONFIRMED (`CAPS:97`, `orca-data.json:1`/`CAPS:98`, `CAPS:100`); row 4 (`CAPS:155`) OVERSTATED for a dropped caveat, but V1:12's literal claim matches the source's first sentence. 0 WRONG. | NOT MET | "Removes Orca's fence against runaway fan-out" (V2:13) is contradicted by `CAPS:99-100` (DA A-001 CONTRADICTED; R1-V2 A-001 "was wrong"). |
| 2. Feasible with stated constraints | MET | It is the current state and the spec's recommendation (V1:9; `SPEC:352`); cost "Zero" (V1:19). | NOT MET | By its own text the use needs commands to call Orca, "against SA-2 and non-goal 1" (V2:22; `SPEC:170`, `SPEC:314`); withdrawn in R2-V2. |
| 3. Consistent terminology | MET | "depth", "fence", "Tasks", "Agent-tool subagents" keep one meaning (V1:3-19). | MET | "Nested worker depth", "Depth 2", "Task and Dispatch" keep one meaning (V2:3-22). |
| 4. No internal contradictions | MET | DA X-003 "Consistent"; IC = 1.000. | NOT MET | V2:8 against V2:16 and V2:22 (DA X-003); IC = 0.913; conceded R1-V2 concession 2. |
| 5. Claims supported by evidence | MET | Every bullet carries a `SPEC:`/`CAPS:` or profile-file citation (V1:8-19); 3 of 4 spot-checked V1 citations CONFIRMED. | NOT MET | V2:13 cites `CAPS:100`, which says "rather than disabling the fence"; V2:9 cites `CAPS:158`, which routes fan-out to the coordinator (DA spot-check 5 OVERSTATED). |
| **Subtotal** | **5/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|---|---|---|---|---|
| 1. Logical ordering | MET | Position, key, then Safety, Reliability, Day to day, Cost (V1:3-19). | MET | Position, key, Strongest case, then the same four (V2:3-22). |
| 2. Consistent hierarchy | MET | `#` at V1:1, `##` at V1:7, 11, 15, 18. | MET | `#` at V2:1, `##` at V2:7, 12, 15, 18, 21. |
| 3. Separation of concerns | MET | Fence and scope under Safety (V1:8-9); spec need and R2-R5 under Reliability (V1:12-13); cost and revisit under Cost (V1:19). | NOT MET **[re-evaluated]** | Cost is split across two sections with different framings: "The change itself is one setting" (V2:10, under "Strongest case") versus "The setting is trivial; using it means rewriting commands" (V2:22, under "Implementation cost"); "Strongest case" also mixes records (V2:8), policy (V2:9) and cost (V2:10). |
| 4. Navigation aids / cross-references | MET | Citation key (V1:5); WC-8, SA-2, R2-R5 IDs (V1:12-13). | MET | Citation key (V2:5); WC-10, SA-2, R2-R4 IDs (V2:8, 16). |
| 5. Artifact-type conventions | MET | Title, "Position:" line, key, one H2 per decision area (V1:1-18). | MET | Same template (V2:1-21; DA S-005). |
| **Subtotal** | **5/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|---|---|---|---|---|
| 1. Unambiguous language | MET | "Position: workers may not start workers." (V1:3); "No change." (V1:16); "Zero." (V1:19). | NOT MET | V2:3 argues for a raise whose use "the design section 1.3 rejects", while V2:22 says "No phase of the spec uses it" (DA S-002, X-003). |
| 2. Concrete | MET | `"nestedWorkerMaxDepth":1` and its file (V1:9); "N troubleshoot workers then one adversarial merge" (V1:16). | MET | "troubleshoot Tier 2 at '+4-15 min'" (V2:8); "one setting in the desktop app" (V2:10). |
| 3. Clear section purpose | MET | Purpose-named headings (V1:7, 11, 15, 18). | MET | Purpose-named headings (V2:7, 12, 15, 18, 21). |
| 4. Terms defined on first use | NOT MET **[re-evaluated]** | "P0 smoke runs (`SPEC:181`)" (V1:19) is never glossed (DC lists P0 as the one unresolved reference); "Tasks" (V1:3) and "Agent-tool subagents" (V1:3) are not defined. | NOT MET | "against SA-2 and non-goal 1" (V2:22) unglossed; "Task and Dispatch" (V2:8) undefined. |
| 5. Actionable next steps / decision points | MET | "the spec can revisit it if P0 smoke runs (`SPEC:181`) show coordinator-side splitting is inadequate" (V1:19). | NOT MET | No decision condition (DA S-003; R2-V2 item 14). |
| **Subtotal** | **4/5** | | **2/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|---|---|---|---|---|
| 1. At least 3 risks with probability and impact | NOT MET | No evidence found; searched V1:1-19 for "probability", "likely", "impact", "risk". | NOT MET | No evidence found; searched V2:1-22. |
| 2. Mitigation per risk | NOT MET | Only the "coordinator splitting inadequate" risk has a mitigation (V1:19); machine-wide scope (V1:9) and the unverified refusal (INV-004) have none. | NOT MET | No mitigations for the fence (V2:13), call sites (V2:16) or operator load (V2:19). |
| 3. Failure modes and recovery | MET | Malformed value falls back to 1 (V1:8, `CAPS:100`); recovery "one desktop setting" after evidence (V1:19). | NOT MET | R2-R4 failures without recovery; reversal not discussed (DA C-008). |
| 4. External dependencies and their failure | MET | "standalone use breaks without Orca (R2)" (V1:13); setting lives in the Orca profile (V1:9). | MET | Orca calls "fail in other projects without Orca (R2)"; call sites UNVERIFIED (V2:16). |
| 5. Monitoring / validation mechanism | NOT MET | The one mechanism, P0 smoke runs (V1:19), cannot exercise the case: conceded in R2-V1 item 3; INV-010. | NOT MET | No evidence found; searched V2:1-22 for "monitor", "check", "verify", "P0", "test". |
| **Subtotal** | **2/5** | | **1/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|---|---|---|---|---|
| 1. Collection boundaries | NOT MET | Multi-profile case (INV-009) and fan-out width (INV-007) not addressed. | NOT MET | "More workers and Tasks per run" (V2:19) gives no bound; multi-profile case absent (INV-009). |
| 2. State interactions across components | MET | "a new Run does not reset depth" (V1:8); raise applies "to every Orca run on the machine" (V1:9). | MET | "applies to every run on this machine, not only IronClaude workers" (V2:13); WC-10 gap (V2:8). |
| 3. Guard condition gaps | NOT MET | Treats the refusal as the fence (V1:8) without noting the untraced call sites (`CAPS:103`); INV-004, INV-005, INV-017 HIGH UNADDRESSED. | MET | "Which call sites enforce the depth check is UNVERIFIED (`CAPS:103`)" (V2:16; DA U-007). |
| 4. Count divergence | NOT MET | No width, generation or off-by-one analysis (INV-007, INV-008 credit only the rounds). | NOT MET | Same; "Depth 2" (V2:8) without stating which depths a maximum of 2 admits. |
| 5. Interaction effects | MET | "a second orchestrator competes with the coordinator (R5)" (V1:13; `SPEC:40`). | MET | "Depth alone does not make the rejected design work" with R2-R4 (V2:16); effect on other runs (V2:13). |
| **Subtotal** | **2/5** | | **3/5** | |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|---|---|---|
| Completeness | 4/5 | 3/5 |
| Correctness | 5/5 | 1/5 |
| Structure | 5/5 | 4/5 |
| Clarity | 4/5 | 2/5 |
| Risk Coverage | 2/5 | 1/5 |
| Invariant & Edge Case Coverage | 2/5 | 3/5 |
| **qual_score** | **22/30 = 0.733** | **14/30 = 0.467** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case subtotal | Floor (at least 1/5) | Eligible as base |
|---|---|---|---|
| Variant 1 | 2/5 | Met | Yes |
| Variant 2 | 3/5 | Met | Yes |

Floor not suspended (neither variant scores 0/5). Variant 2 is the stronger variant on this one dimension, through its V2:16 flag of the unverified call sites; that flag is carried into the merge (Strengths to Incorporate, item 3).

## Position-Bias Mitigation
Pass 1 (`P1`) evaluated Variant 1 then Variant 2; Pass 2 (`P2`) evaluated Variant 2 then Variant 1. Each pass states it did not read the other. Pass totals: P1 V1 23/30, V2 14/30; P2 V1 22/30, V2 15/30. M = MET, N = NOT MET.

| # | Criterion | V1 P1 | V1 P2 | V1 Final | V2 P1 | V2 P2 | V2 Final |
|---|---|---|---|---|---|---|---|
| Co1 | Covers requirements | M | M | M | M | M | M |
| Co2 | Edge cases / failures | M | M | M | M | M | M |
| Co3 | Dependencies | M | M | M | M | M | M |
| Co4 | Success criteria | M | M | M | N | N | N |
| Co5 | Out of scope | N | N | N | N | N | N |
| Cr1 | No factual errors | M | M | M | N | N | N |
| Cr2 | Feasible | M | M | M | N | N | N |
| Cr3 | Terminology | M | M | M | M | M | M |
| Cr4 | No contradictions | M | M | M | N | N | N |
| Cr5 | Claims supported | M | M | M | N | N | N |
| St1 | Ordering | M | M | M | M | M | M |
| St2 | Hierarchy | M | M | M | M | M | M |
| St3 | Separation of concerns | M | M | M | N | **M** | **N (re-eval)** |
| St4 | Navigation | M | M | M | M | M | M |
| St5 | Conventions | M | M | M | M | M | M |
| Cl1 | Unambiguous | M | M | M | N | N | N |
| Cl2 | Concrete | M | M | M | M | M | M |
| Cl3 | Section purpose | M | M | M | M | M | M |
| Cl4 | Terms defined | M | **N** | **N (re-eval)** | N | N | N |
| Cl5 | Decision points | M | M | M | N | N | N |
| Ri1 | 3 risks with probability | N | N | N | N | N | N |
| Ri2 | Mitigation per risk | N | N | N | N | N | N |
| Ri3 | Failure and recovery | M | M | M | N | N | N |
| Ri4 | External dependencies | M | M | M | M | M | M |
| Ri5 | Monitoring / validation | N | N | N | N | N | N |
| In1 | Collection boundaries | N | N | N | N | N | N |
| In2 | State interactions | M | M | M | M | M | M |
| In3 | Guard gaps | N | N | N | M | M | M |
| In4 | Count divergence | N | N | N | N | N | N |
| In5 | Interaction effects | M | M | M | M | M | M |

### Disagreement re-evaluation (final verdicts)

**St3, Variant 2 (separation of concerns).**
- Pass 1 evidence and verdict: NOT MET; "The change itself is one setting" under "Strongest case" (V2:10) against "The setting is trivial; using it means rewriting commands" under Implementation cost (V2:22); the "Strongest case" section mixes reliability (V2:8), policy (V2:9) and cost (V2:10).
- Pass 2 evidence and verdict: MET; "Safety holds fence and scope (V2:13); Reliability holds R2-R4 and enforcement (V2:16); Cost holds the rewrite cost (V2:22)."
- Source re-read: V2:10 reads "**The change itself is one setting** in the desktop app (`CAPS:99`)." and V2:22 reads "The setting is trivial; using it means rewriting commands to call Orca ... No phase of the spec uses it." Pass 2's evidence covers only the four standard sections and does not address the "Strongest case" section. One concern, implementation cost, is stated in two sections with opposite weight (a strength at V2:10, the real cost at V2:22), and DA C-007 records that the two framings had to be reconciled by the analyst.
- **Final: NOT MET.** Pass 1's evidence is specific and Pass 2's does not answer it.

**Cl4, Variant 1 (terms defined on first use).**
- Pass 1 evidence and verdict: MET; depth 1 defined by quote (V1:8), WC-8/SA-2 glossed as "commands never call Orca" (V1:12), R2-R5 glossed (V1:13), citation key (V1:5).
- Pass 2 evidence and verdict: NOT MET; "P0 smoke runs (`SPEC:181`)" (V1:19) with no gloss of P0 or smoke run; "Tasks" (V1:3) not defined.
- Source re-read: V1:19 "the spec can revisit it if P0 smoke runs (`SPEC:181`) show coordinator-side splitting is inadequate" gives no gloss of P0; it is the term the revisit trigger depends on. Both passes marked Variant 2 NOT MET on this criterion for unglossed IDs (SA-2, non-goal 1) and "Task and Dispatch"; applying the same standard, V1's unglossed "P0" and "Tasks" fail it too. Pass 1's evidence is true for the terms it lists but does not cover P0.
- **Final: NOT MET.** Same standard as Variant 2; the quantitative DC metric independently finds P0 as V1's one unresolved reference.

### Log
- Criterion-variant pairs compared: 60
- Disagreements found: 2 (St3 / Variant 2; Cl4 / Variant 1)
- Disagreements re-evaluated: 2
- Final verdicts changed relative to Pass 1: 1 (Cl4 / Variant 1, MET to NOT MET)
- Final verdicts changed relative to Pass 2: 1 (St3 / Variant 2, MET to NOT MET)
- Net effect: Variant 1 22/30 (Pass 1 had 23); Variant 2 14/30 (Pass 2 had 15). Neither disagreement changes the ranking: Variant 1 leads in both passes (by 9 and by 7 criteria).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---|---|---|---|---|
| Variant 1 (option a) | 0.92083 x 0.50 = 0.4604 | 0.7333 x 0.50 = 0.3667 | **0.827** | not needed (12 of 21 points won) |
| Variant 2 (option b) | 0.92076 x 0.50 = 0.4604 | 0.4667 x 0.50 = 0.2333 | **0.694** | not needed (3 of 21 points won) |

**Margin**: 0.133 (13.3 percentage points), above the 0.05 tiebreaker threshold.
**Tiebreaker applied**: No. For the record, every tiebreaker level would also pick Variant 1: debate points won 12 to 3 (level 1), Correctness MET 5 to 1 (level 2), input order (level 3).

The whole margin comes from the qualitative layer (raw difference 0.267 on qual, 0.00007 on quant). Sensitivity: if both disputed criteria had gone the other way (Cl4 MET for V1, St3 MET for V2), the scores would be 0.844 and 0.710, margin 0.133; the selection does not depend on the re-evaluation.

## Debate cross-check
The Step 2 scoring matrix agrees with the rubric: Variant 1 won 12 diff points, Variant 2 won 3, 5 were equal and 1 (C-003) is unresolved (`debate-transcript.md`, Scoring Matrix). Both advocates end Round 2 recommending option (a), and the Variant 2 advocate withdrew (b) (R2-V2 Overall recommendation). Convergence is 95.2% but the status is BLOCKED_BY_INVARIANTS (INV-001, INV-004, INV-005, INV-017). The block concerns the reasons and preconditions stated for (a), not the choice between (a) and (b); it is carried into `refactor-plan.md` as mandatory changes or accepted-risk entries.

## Selected Base: Variant 1 (option a, keep depth 1)

### Selection Rationale
Variant 1 scores 0.827 against 0.694, a 0.133 margin with no tiebreaker. The quantitative layer is a dead heat (0.921 each): Variant 2's fuller section set and zero vague wording offset Variant 1's consistency and better-resolved references. The qualitative layer decides it, mainly on Correctness (5/5 against 1/5): Variant 2's headline claims were contradicted by its own sources or by itself, "Removes Orca's fence" (V2:13 against `CAPS:99-100`), "Orca's provenance rule prefers it" (V2:9 against `CAPS:158`), and the per-sub-unit benefit (V2:8) against "No phase of the spec uses it" (V2:22), and its advocate conceded all three (R1-V2 concessions 1-2, A-001). Variant 1 is the spec's current recommendation (`SPEC:352`), costs nothing, is internally consistent, and won 12 of the 21 diff points to Variant 2's 3. Both advocates end the debate recommending option (a).

The base is not clean. Variant 1 loses on guard gaps: it treats the depth-1 refusal as a proven fence (V1:8) although its call sites were never traced (`CAPS:103`), and it never states that it needs a root coordinator. Those gaps are the four HIGH UNADDRESSED invariants (INV-001, INV-004, INV-005, INV-017) that block convergence, and they must be fixed in the merge.

### Strengths to Preserve from Base
1. **The recommendation and its spec anchor**: keep depth 1; fan-out stays inside a command or is split into Tasks by the coordinator (V1:3; `SPEC:352`, `SPEC:42`). Debate: S-002, C-003 (plannable fan-out), X-001.
2. **Machine-wide scope argument**: the value lives in the profile file (`orca-data.json:1`, `"nestedWorkerMaxDepth":1`, `CAPS:98`) and a raise affects every Orca run on the machine (V1:9). Debate: C-002, A-003 (only IronClaude briefs could carry a restraint under (b)). Needs the per-profile precision of INV-009.
3. **Depth fixes only R1; R2-R5 remain**, with R5 (second orchestrator) as the reason that also defeats the scoped worker-session route (V1:13; `SPEC:37-40`). Debate: S-004, C-005, A-002.
4. **Orca's own refusal advice and malformed-value fallback** as evidence that depth 1 is a deliberate default (V1:8; `CAPS:99-100`). Debate: DA U-003, C-001.
5. **Zero cost and an evidence-gated revisit** (V1:19). Debate: S-003, C-007, C-008. The trigger itself must be replaced (R2-V1 item 3).
6. **Day-to-day: no change** for the person (V1:16). Debate: C-009.

### Strengths to Incorporate from Non-Base Variants
From Variant 2:
1. **State what option (a) gives up** (V2:7-8; DA U-005): Orca Task, Dispatch, liveness and retry records are not available for fan-out that stays inside one command run, and the WC-10 heartbeat gap stays accepted. Debate: S-001 (V2, 95%), X-002 (V2, 94%), conceded R1-V1 concession 3 and R2-V1 item 11.
2. **Locate (b)'s real cost** (V2:22; DA U-006): the setting is trivial; using it needs either commands calling Orca (forbidden by SA-2, non-goal 1) or a new composite brief type with contract text and tests. Debate: C-007; R2-V1 NE1; R2-V2 item 8.
3. **Flag the unverified enforcement** (V2:16; DA U-007): which call sites enforce the depth check, and whether a depth-1 worker may `task-create`, are UNVERIFIED (`CAPS:103`, `SPEC:387`). This fills the base's Invariant criterion 3 gap and anchors INV-004 / INV-017.
4. **Operator load of (b)** (V2:19; DA U-008): more workers, Tasks and terminals owing a release decision (`CAPS:107`, `CAPS:113`).

From the debate's concessions and refinements:
5. **"Widens, does not remove"** (DA A-001, C-001; R1-V1 concession 1; R1-V2 A-001): the refusal fires at any configured maximum (`CAPS:99`) and bad values fall back to 1 (`CAPS:100`); a raise to 2 admits one more generation. Add INV-007's precision: depth bounds generations, not width; at depth 1 Orca puts no cap on how many workers the coordinator starts.
6. **`check --wait` is a liveness signal** (C-004, V2 94%; `CAPS:64`): V1's R1 "heartbeat gap moves to the parent" was withdrawn (R2-V1 item 6); D5 does not change the WC-10 gap either way (INV-016).
7. **The scoped form (b) would take** (R1-V2 Position summary; R2-V1 and R2-V2 Overall recommendations): depth exactly 2, used only by a worker's top-level session, only when the brief says `Sub-workers: allowed, max N`, with no command changes. Its residual costs: R5 (`SPEC:40`), the shared Run inbox (`CAPS:59`, `CAPS:92`; R2-V2 NE1), the full coordinator loop in the parent (`CAPS:92`, `CAPS:107`, `CAPS:113`, `CAPS:116`; R2-V1 NE2), and no use under the one-command brief (`SPEC:79`; R2-V2 item 6).
8. **A revisit trigger that can fire** (R2-V1 item 3; R2-V2 NE2; INV-010, INV-011): both conditions together, a defined composite brief type, and a real coordinator run recording a split knowable only at run time whose extra round trip was material; plus a place in the run notes to record such a split.
9. **Checks before any raise** (R2-V2 Overall recommendation item 4): trace the refusal call sites and `task-create` at depth 1 (read-only), and establish which mailbox receives a depth-2 worker's messages.
10. **Correct the spec text around D5** (R2-V2 NE3; INV-012): `SPEC:350` and `SPEC:353` describe (b) as commands starting workers and as breaking the fence; `SPEC:36` (R1) says the designs exclude each other "unless the user raises the depth setting"; `SPEC:27` (E4) drops the `CAPS:155` UNVERIFIED caveat; `SPEC:315` (non-goal 2) inherits the same framing.

From the invariant probe (not from either variant, required by the HIGH gate): the root-coordinator precondition (INV-001), a worker-session ban on Orca fan-out verbs (INV-005, INV-013), a read-only P0 trace of the refusal (INV-004), a coordinator rule to start only Tasks it created (INV-014), a P0 read of the live depth value (INV-002), and dropping the "mechanical backstop" claim unless the trace confirms it (INV-017). These are planned in `refactor-plan.md`.
