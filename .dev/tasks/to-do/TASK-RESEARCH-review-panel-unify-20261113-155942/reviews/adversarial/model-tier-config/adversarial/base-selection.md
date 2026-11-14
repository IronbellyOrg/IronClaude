# Base Selection Report

Variants: Variant A = `variant-1-original.md` (proposal-a: central panel targets anthropic-only, class launch). Variant B = `variant-2-original.md` (proposal-b: central panel targets the gateway, launch adapters, dated tier data). Source input for requirement coverage: the C03 block of `synth-04-options-conflicts.md` (lines 164-226), no formal requirement IDs, so section-level topic matching with ten derived requirements Q1-Q10 (listed under RC).

## Quantitative Scoring (50% weight)

Computed with `uv run python` over the two variant files (deterministic; same input gives the same score). Contradiction counts for IC are the intra-variant contradictions CONFIRMED in the debate (A: 0; B: 3 = X-001, X-002, X-003, each conceded in whole or part by the B advocate).

| Metric | Weight | Variant A (anthropic-only, class launch) | Variant B (gateway, adapters, dated data) |
|--------|--------|-------------------|-------------------|
| requirement_coverage | 0.30 | 1.000 (10 of 10 requirements referenced) | 1.000 (10 of 10 requirements referenced) |
| internal_consistency | 0.25 | 1.000 (1 - 0/94 scorable claims) | 0.972 (1 - 3/107 scorable claims) |
| specificity_ratio | 0.15 | 1.000 (92 concrete lines, 0 vague-indicator lines) | 1.000 (105 concrete lines, 0 vague-indicator lines) |
| dependency_completeness | 0.15 | 1.000 (22 EV ids defined, 57 EV tokens and R1-R10 all resolve) | 1.000 (27 evidence rows, R1-R9, P1-P7; 9 row references all resolve) |
| section_coverage | 0.15 | 1.000 (7 H2 of max 7) | 1.000 (7 H2 of max 7) |
| **quant_score** | | **1.000** | **0.993** |

Notes on the quantitative layer:
- RC requirement list and keyword rules: Q1 reflect templates cannot resolve in gateway ("launch None is not one of"); Q2 haiku slot served by `gpt-6.1-sol`; Q3 empty `fallbacks`; Q4 `muse-ember`; Q5 `glm-5.3` + `Qwen3.8-max` + "exclud"; Q6 `O-2` + re-probe/`G-33`; Q7 "adapter"; Q8 `D12`; Q9 dated/provenance; Q10 anthropic-only + reflect. Both variants match all ten. A match means the topic is referenced, not that the requirement is met in substance (A declines Q7 and Q9, B answers them); substance is scored in the qualitative layer (CP1).
- SR follows the protocol formula `concrete / (concrete + vague)`; no vague-indicator line occurs in either file, so it saturates at 1.000 for both. The alternative reading (concrete lines over all substantive lines) gives A 0.920 and B 0.882 and was NOT used.
- RC, SR, DC and SC do not discriminate between these two variants; only IC does (0.028 on the IC weight of 0.25, so 0.007 of quant_score).

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Two independent evaluator agents (general-purpose) scored all 30 criteria for both variants: Pass 1 in input order (A then B), Pass 2 in reverse order (B then A), launched in parallel. Evidence shown is from Pass 1 unless a criterion was re-evaluated. Judged against the proposal documents as written; the debate and probe files were used for fact checking only.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|-----------|-----------|----------------|-----------|----------------|
| CP1 Covers all explicit requirements (Q1-Q10) | NOT MET | Q7, Q8, Q9 are declined: record-only cell, "no gateway dispatch to protect" removes D12 detection, "nothing dated enters" the tier file; Q5 gets evidence only (EV-18) | MET | Design items 1-6 and Risks give a response to Q1-Q10, including adapters, D12 `check_required_env`, `provenance`, ember, anthropic-only kept (Q5 is the thinnest: a dated note) |
| CP2 Addresses edge cases/failures | MET | Risks R1-R10 (A3 collapse, null launch, resume Conflict test 5, no failover R3) | MET | R1-R9, plus the Rollback paragraph and R3 fail-closed reflect case |
| CP3 Includes dependencies/prerequisites | MET | Cost: "Shared with C08 and C09"; Core item 1 relies on the C09 dispatcher; Wave 0 prerequisite | MET | Cost table "Gate" column (B-1 needs owner accepting R1; B-3 needs Coder first); B-4 under C09 |
| CP4 Defines success/completion criteria | MET | "Test coverage needed": new tests 1-7 and the `uv run pytest` run set | MET | "Test coverage needed": new-tests table (completeness, backward-compat, `verify` V1-V4, D12) |
| CP5 Specifies out-of-scope items | MET | "Out of C03" (R7), R9 "Out of scope here", "What this argument does not show" | MET | "Not in this proposal's test scope: the dispatcher...", B-4 counted under C09, P7 "What B does not claim" |
| **Subtotal** | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|-----------|-----------|----------------|-----------|----------------|
| CR1 No factual errors or hallucinated claims | NOT MET | Correctness step 2: "forgetting `--env` yields a panel that can run" (falsified by INV-013, loop has no `launch` reader); reflect "Dispatch passes `model`..." vs `SKILL.md:342` (INV-009) | NOT MET | R3 "Certain for that combination" contradicted by its own row 4 (X-001); "Default environment is the gateway" (X-002) |
| CR2 Technical approaches feasible with stated constraints | MET | Core item 2 `select_env` flip plus the class path (EV-5 docs quote, 15/15 runs EV-7); needs only today's Agent call | NOT MET | R1: `cli-model:` entries run only under an undelivered C09 dispatcher (L); V3 rests on the unverified alias-first-model rule (P7) |
| ^ CR2 Variant B disagreement | P1 NOT MET / P2 MET -> **NOT MET** | Re-evaluation (both passes cited): the headline target for non-reflect consumers, gateway `cli-model:` launch, is not feasible within the stated constraints: R3 says in-session Agent calls cannot pass a raw gateway id and R1 says the dispatcher is not part of B; the B advocate conceded this in Round 2. The additive pieces (grammar, provenance, `check_required_env`) are feasible but the criterion is about the approach as proposed. | | |
| CR3 Terminology consistent and accurate | MET | "class", "launch", "cell", "binding" used consistently; anthropic-only label vs served model is explicitly separated (weakest point) | NOT MET | "default environment" means gateway in the consumer table but `select_env` keeps anthropic-only when `T3Model01` is unset (X-002); "supported" applied to `cli-model` with no executor |
| ^ CR3 Variant B disagreement | P1 NOT MET / P2 MET -> **NOT MET** | Re-evaluation: "default environment" is used for the gateway in the consumer table while the CLI keeps anthropic-only as the fallback (X-002, conceded as "loose" by the B advocate); one core term used inconsistently counts against "consistently throughout". | | |
| CR4 No internal contradictions | MET | No intra-A contradiction was confirmed by the debate (it confirmed 3 in B) | NOT MET | X-001 (R3 vs row 4), X-002 (gateway default vs `select_env`), X-003 (R1 vs "removes the one property that is false") |
| CR5 Claims supported by evidence/rationale | MET | Every claim carries [CODE-VERIFIED]/[RUN]/[OBSERVED-RUNTIME] tags and an EV-n reference in the correctness argument | MET | Evidence rows carry research file, code location and tag; P7 and R1 mark unverified items |
| **Subtotal** | **4/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|-----------|-----------|----------------|-----------|----------------|
| ST1 Logical section ordering | MET | Design, How it works, Evidence, Correctness, Risks, Tests, Cost | MET | Same order; Evidence A-E before the correctness argument P1-P7 |
| ST2 Consistent hierarchy depth | MET | `##` sections with `###` only under Design, How it works and Tests | MET | `##` sections with `###` under Design, How it works, Evidence (A-E), Tests |
| ST3 Separation of concerns | MET | Consumers table separate from data flow, contract fields and CLI surface | MET | Core and consumers split; contract fields and CLI surface separate |
| ST4 Navigation aids / cross-references | MET | Evidence ids EV-1..22 cross-referenced from the correctness argument and risks | MET | Evidence row numbers, P1-P7, R1-R9, V1-V4 and B-1..B-4 cross-referenced |
| ST5 Follows artifact-type conventions | MET | Design, evidence, correctness, risk table, tests, cost table | MET | Design, evidence, correctness, risk table, tests, cost with stages |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|-----------|-----------|----------------|-----------|----------------|
| CL1 Unambiguous language | MET | Definite statements; the only hedged cells are likelihoods ("Possible", "Unknown") in R2 and R8 | MET | Definite statements; only conditionals such as "If the owner wants a hard boundary..." (R5) |
| ^ CL1 Variant B disagreement | P1 MET / P2 NOT MET -> **MET** | Re-evaluation: a grep of the variant for hedge words (appropriate, as needed, should consider, might, various) finds none; the conditionals the second pass cited ("ember only with owner confirmation ... or declared out of scope", "advisory by default; exit 1 when a check is fail") are explicit either/or decisions with a trigger, not vague language. | | |
| CL2 Concrete rather than abstract | MET | Exact file:line, commands and expected output (EV-1/EV-2 printed errors) | MET | Exact grammar `<adapter>:<argument>`, V1-V4 check definitions, 12 ids |
| CL3 Clear purpose per section | MET | Each section is summarisable in one sentence (Position, Design, Evidence groups 1-6) | MET | The "One sentence." line plus section-level purposes |
| CL4 Acronyms/terms defined on first use | NOT MET | C03, C04, C08, C09, C15, C17, C18, E3, O-2, D4, SC-4 and G-33 used without definition (only tags and CR/RR are defined) | NOT MET | C08, C09, C17, C20, D4, D12, G-33, E2, E3 and O-2 used without definition |
| CL5 Actionable next steps/decision points | NOT MET | No ordered next steps or gates; R8 "Possible" and the "Stage 5 decide" notes are not marked as decisions | MET | Stages B-1..B-4 with Gate column; "Owner accepts risk R1"; "Do not ship the gateway entries before the owner accepts that gap" |
| **Subtotal** | **3/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|-----------|-----------|----------------|-----------|----------------|
| RK1 >=3 risks with probability and impact | MET | Table has "Likelihood and impact" for R1-R10 (R1 "5 of 15 combination runs; Medium") | MET | Table has "Likelihood / impact" for R1-R9 (R1 "High likelihood; Medium impact") |
| RK2 Mitigation for each risk | NOT MET | R7 mitigation is "Out of C03. Record as an open item"; R9 mitigation is "Out of scope here" (no mitigating action) | MET | Every row has a mitigation (R1 staging and `verify` "declared only", R4 Coder-first PR, R5 schema bump option) |
| RK3 Failure modes and recovery | MET | R3 mark partial plus one re-dispatch; R8 flip back by one line; D4 legacy path | MET | Rollback paragraph; R3 D4 legacy rotation; "Fail closed" P4 |
| RK4 External dependencies and failures | MET | R2 external docs family-alias rule; R10 one gateway on one day; EV-14 gateway list moved | MET | R2 alias routing and Coder config; R4 `ccsession-models.json` fetched live from master; R9 external evidence |
| RK5 Monitoring/validation mechanism | MET | Launch-versus-observed check; Wave 0 distinct-model count; swap fixture test 6 | MET | `panel verify` V1-V4, `provenance` age, version-coupling test |
| **Subtotal** | **4/5** | | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence (CEV) | Variant B | Evidence (CEV) |
|-----------|-----------|----------------|-----------|----------------|
| IE1 Collection boundary conditions | MET | EV-4 empty `fallbacks`; R6 "sonnet + 3x haiku" duplicates on one bound model; new test 1 over all templates | NOT MET | Only evidence row 5 notes empty `fallbacks`; no design response for single-model or duplicate-slot panels (the packaged-data completeness test covers only an empty `launch` map) |
| IE2 State variable interactions across components | MET | `launch_binding` in the manifest payload hash, a different binding raises `Conflict` (test 5), Wave 0 canonical, `select_env` env var | MET | P1 resolver stays pure while the env reads go to the command layer; `tiers_as_of` kept out of the frozen golden |
| IE3 Guard condition gaps | MET | New test 4: `launch` null, outside the class set, or `fable` is a dispatch error; EV-2 reflect fail-closed | MET | `parse_launch` rejects an unknown adapter and an empty argument; V1 completeness; V2/D12 unset-slot check |
| ^ IE3 Variant A disagreement | P1 MET / P2 NOT MET -> **MET** | Re-evaluation: A names several guard gaps with evidence: a null launch in the gateway (EV-1), a missing class falling to the frontmatter default (A3 collapse, EV-12), a Fable value where the profile forbids it, reflect failing closed (EV-2). It does not note that `validate_tiers` accepts any launch string for non-reflect templates (INV-003) and leaves explicit `--env gateway` slot checks to C09; those are gaps in its coverage and are scored under CR1 and the invariant probe, not as a missing identification. | | |
| IE4 Count divergence scenarios | MET | R4 and test 7 class ceiling of 3; Wave 0 counts distinct bound models; `reviewers_requested` and `reviewers_resolved` in the payload (INV-005 and INV-006 show gaps) | NOT MET | No mention of requested vs resolved reviewers, `N_eff`, the 3-reviewer cap, or class count vs distinct served models |
| IE5 Interaction effects when components combine | MET | R5 and the loop-prompt pin `test_review_rules_text.py:21`; EV-22 goldens; reflect keeps explicit `--env anthropic-only`; resume `Conflict` (misses INV-009 and INV-013) | MET | P2 and R6 goldens; C6 pin and needle tests; reflect stays anthropic-only while others default to gateway |
| **Subtotal** | **5/5** | | **3/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 5/5 |
| Correctness | 4/5 | 1/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 3/5 | 4/5 |
| Risk Coverage | 4/5 | 5/5 |
| Invariant & Edge Case Coverage | 5/5 | 3/5 |
| **qual_score** | **25/30 = 0.8333** | **23/30 = 0.7667** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case Coverage | Floor (>=1/5) |
|---|---|---|
| A | 5/5 | eligible |
| B | 3/5 | eligible |

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| CR2 Technical approaches feasible with stated constraints | B | NOT MET | MET | DISAGREE | NOT MET (re-evaluated) |
| CR3 Terminology consistent and accurate | B | NOT MET | MET | DISAGREE | NOT MET (re-evaluated) |
| CL1 Unambiguous language | B | MET | NOT MET | DISAGREE | MET (re-evaluated) |
| IE3 Guard condition gaps | A | MET | NOT MET | DISAGREE | MET (re-evaluated) |

Criterion-variant verdicts compared: 60. Agreed: 56. Disagreements re-evaluated: 4. Final verdicts changed relative to Pass 1: 0 (all four re-evaluations coincide with Pass 1); relative to Pass 2: 4.
Pass totals before re-evaluation: Pass 1 A 25/30, B 23/30; Pass 2 A 24/30, B 24/30.

Anchoring check (orchestrator): because every re-evaluation landed on the Pass 1 verdict, the selection was re-run under the opposite assumption (all four disagreements resolved to the Pass 2 verdict). Result: A 24/30, B 24/30, qual 0.800 each; combined A 0.900, B 0.897; margin 0.3%, inside the 5% tiebreaker band, and the tiebreaker (debate points, A 10 vs B 0) still selects Variant A. The selection does not depend on the re-evaluation outcomes.

## Combined Scoring

variant_score = 0.50 x quant_score + 0.50 x qual_score

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker (points won, S/C/X) |
|---------|---------------|--------------|-----------------|-------------------|
| A (proposal-a, anthropic-only, class launch) | 0.5000 | 0.4167 (25/30) | **0.9167** | 10 won (S-005, C-002, C-007, C-008, C-010, C-011, C-013, C-015, X-001, X-002) |
| B (proposal-b, gateway, adapters, dated data) | 0.4965 | 0.3833 (23/30) | **0.8798** | 0 won outright (7 points MERGE, 4 NEITHER, 4 unresolved) |

**Margin**: 3.68% (below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance): Variant A won 10 diff points in Step 2, Variant B won none outright. Level 2 and 3 not needed.

Scoring caveats (stated so the margin is not over-read):
- The quantitative layer is saturated (four of five metrics are 1.000 for both), so it contributes almost nothing to the margin (0.0035 of final score).
- The margin comes from the qualitative layer: Correctness (A 4/5, B 1/5) and Invariant & Edge Case (A 5/5, B 3/5) favour A; Completeness, Clarity, Risk Coverage (CP 5/5 vs 4/5, CL 4/5 vs 3/5, RK 5/5 vs 4/5) favour B. B is the better-organised proposal against the written C03 requirements; A is the more correct and the more executable one.
- Score differences are small and the selection is defended by the debate result as much as by the numbers (see the anchoring check above: with Pass 2 verdicts the totals tie at 24/24 and the debate tiebreaker still selects A).
- Neither variant is accepted as written: the invariant probe found two HIGH problems in the consensus built on A's core (INV-009, INV-013) and the debate left 4 points unresolved. Selection of A as base means A's skeleton is the one that the merge repairs and extends; it does not certify A's PR 1 as sufficient.

## Selected Base: Variant A (proposal-a: central panel targets anthropic-only, launching by class name; synth-04 Option A)

### Selection Rationale

1. Score: A 0.9167 against B 0.8798 (3.7% margin); inside the tiebreaker band, where debate performance decides: A 10 points won, B 0.
2. Executability: A's launch route is the only one an in-session orchestrator can use today (platform docs quote verified by both advocates; class path 15 of 15 combination runs reached `published`); B's gateway entries describe a route no code executes (B's own R1, conceded in Round 1 and again in Round 2).
3. Correctness: B has three confirmed internal contradictions (X-001, X-002, X-003, CR4 NOT MET); R3 "Certain" is refuted by B's own evidence row 4; A's confirmed weaknesses are overclaims about sufficiency (INV-013) and an unnoticed collision with shadow mode (INV-009), found by the fault-finder, not self-contradictions.
4. Scope and risk: XS-S and Medium against L and High (C-013, B conceded); no tier-file byte change keeps both goldens valid.
5. Where B is better and the merge must take it: a drift guard for the tier file (the repo checklist omits it), the grammar decision, a pre-run alias and slot check, completeness and backward-compatibility tests, staged delivery, a clearer owner-decision gate (CL5), a mitigation for every risk (RK2).

### Strengths to Preserve from Base (A)
1. One supported launch contract: class name on the Agent call; gateway models reached by class-to-model binding in the operator environment (EV-5, EV-8, EV-9).
2. `select_env` flip (single production caller) so an omitted `--env` cannot silently yield a no-launch panel; gateway stays reachable by `--env gateway`.
3. `launch_binding` as an extra key of the `resolved` payload with no manifest schema change; D4 fallback for a consumer that selects gateway.
4. Tier file bytes unchanged in PR 1; both goldens stay valid.
5. Test plan items 1, 2, 3, 7 and the two flipped tests; candid "what this argument does not show" and "items I did not check".

### Strengths to Incorporate from Non-Base Variant (B)
1. Launch grammar `<adapter>:<argument>`, bare string means `agent-class` (U-011), decided now; a closed `parse_launch` accepting only `agent-class` (timing disputed: PR 2 or the dispatcher PR). Gateway `cli-model` entries wait for the dispatcher (agreed, C-002, C-003).
2. Minimal provenance (`tiers_as_of`, `ccsession_models_version`), the version-coupling test and a fourth checklist file in `MODEL-TIERS.md` (U-014); drop the unenforceable free-text `evidence[]`/`gateway_observed_on` fields (B conceded).
3. Env-slot drift check as a set comparison (live `T<N>Model0N` against tier-file aliases, `tier0` and `muse-ember` reported), command layer only (U-013, C-006; timing disputed).
4. `panel verify` V1, V2, V4; V3 route check warn-only, never "ok", with a parent-model input (U-012, C-005, C-009).
5. Packaged-data completeness test and old-versus-new backward-compatibility test, landed with the pieces they guard (U-015, U-016, C-012).
6. Staged delivery with a gate per stage and the owner-decision gate on the gateway entries (U-018, S-007).
