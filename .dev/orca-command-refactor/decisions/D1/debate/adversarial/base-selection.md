# Base Selection Report

Decision D1 (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:328-331`), /sc:adversarial Mode A, depth standard, Step 3. Assembled 2026-11-02T16:23Z by the debate orchestrator (not an advocate). Variants: V1 = `variant-1-original.md` (option a, explicit `--unattended` flag); V2 = `variant-2-original.md` (option b, detect Orca); V3 = `variant-3-original.md` (option c, flag plus worker-session guard). The original variant texts are scored; Round corrections do not earn credit here (they feed the refactoring plan instead).

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (option a) | V2 (option b) | V3 (option c) |
|---|---|---|---|---|
| requirement_coverage (RC) | 0.30 | 0.824 (14/17) | 0.882 (15/17) | 0.824 (14/17) |
| internal_consistency (IC) | 0.25 | 0.800 (1 - 2/10) | 0.800 (1 - 2/10) | 0.750 (1 - 2/8) |
| specificity_ratio (SR) | 0.15 | 0.900 (9/10) | 1.000 (10/10) | 1.000 (8/8) |
| dependency_completeness (DC) | 0.15 | 1.000 (32/32) | 1.000 (24/24) | 0.964 (27/28) |
| section_coverage (SC) | 0.15 | 0.800 (4/5) | 1.000 (5/5) | 1.000 (5/5) |
| **quant_score** | | **0.852** | **0.915** | **0.879** |

Computation details (all counts are reproducible from the variant files and `diff-analysis.md`):

- **RC, requirement coverage.** The source (`SPEC:328-331`) has no requirement IDs (no FR-/NFR-/R- patterns), so the protocol's edge case applies: topic coverage. The required topics are the decision's four (safety for people, reliability/testability, day-to-day use, implementation cost) plus the 13 C-NNN topics of the diff analysis, 17 in all. A decision topic is covered when the variant has a section for it; all three have all four (V1:7/12/17/21, V2:12/16/21/24, V3:10/15/19/22). A C-topic is covered unless the variant's cell in the diff analysis's content table says "Not addressed", "Not used" or "Not discussed".
  - V1 misses C-010 (Orca's worker definition, "Not used"), C-011 (coordinator-only commands) and C-012 (headless precedent): 4 + 10 = 14.
  - V2 misses C-011 and C-013 (phase gating): 4 + 11 = 15. V2's C-002 cell ("Mentions loss of outward defaults only as a side effect", V2:13) counts as covered.
  - V3 misses C-002 (outward defaults, "Not discussed beyond 'same as (a)'"), C-012 and C-013: 4 + 10 = 14.
- **IC, internal consistency.** Scorable claims = the claim bullets and paragraphs counted by the diff analysis's similarity check (V1 10, V2 10, V3 8; position lines excluded). Contradictions = rows of the diff analysis's contradiction table that are internal to the variant or set it against a fixed spec constraint (the protocol's "requirement-constraint conflict"); cross-variant disagreements (X-001, X-007) are not internal.
  - V1: X-003 (V1:13 vs V1:22), X-004 (V1:23 vs V1:14) = 2.
  - V2: X-002 (V2:9 vs V2:17), X-006 (V2:10 vs `SPEC:57`) = 2. V2's offer of the environment route (V2:3) against its rejection (V2:13) is recorded by the diff analysis as structural (S-002, S-003), not as an X-row, so it is not counted here; it is scored in the qualitative layer (Correctness 4).
  - V3: X-003 (V3:16 vs V3:17), X-005 (V3:3, V3:23 vs `SPEC:181`, `SPEC:191`, `SPEC:197`) = 2.
- **SR, specificity ratio.** Same statement units as IC. A statement is concrete when it contains at least one concrete indicator (a citation, a number, or a named entity such as `ORCA_TERMINAL_HANDLE`, `WORKER-CONTRACT.md`, AC-n, WC-n). A grep of the protocol's vague indicators ("appropriate", "as needed", "properly", "adequate", "should consider", "might", "various", "etc.", "best practices", "industry standard") found 0 occurrences in all three variants. The only statement without a concrete indicator is V1:23 ("Changing later is cheap ..."), so V1 = 9/10. Note: the vague-word formula (concrete / (concrete + vague)) gives 1.000 for all three; the statement-level form from the metric table is used because it is the only one that separates the variants. Using 1.000 for V1 would raise its quant score to 0.867 and does not change the selection (see Combined Scoring).
- **DC, dependency completeness.** External references (`SPEC:N`, `CAPS:N`, `[G] N` line targets, file paths) are excluded as the protocol requires. Internal references are (1) uses of the citation keys, which resolve when the key is defined in the variant's own citation-key line (V1 defines `SPEC`, `CAPS`; V2 and V3 also define `[G]`), and (2) term references to contract IDs or sections (SA-n, WC-n, AC-n, non-goal n, item n, section n, "7.2", option (x)), which resolve when the same line carries a citation to where the term is defined. Title lines are excluded.
  - V1: 23 key uses + 9 term references (V1:8, 9×2, 10, 13×2, 14, 18, 19), all resolved = 32/32.
  - V2: 19 key uses + 5 term references (V2:13×2, 18×2, 25), all resolved = 24/24.
  - V3: 17 key uses + 11 term references (V3:3×2, 8×6, 11, 13, 16); V3:16 ("one extra 7.2 run") carries no citation = 27/28.
  - DC checks only that a reference resolves, not that the cited line says what is claimed. Content errors in citations (V2's `CAPS:47` OVERSTATED and AC-C1 WRONG; V3's `[G]` 78-82 range OVERSTATED) are scored in the qualitative layer (Correctness 1 and 5).
- **SC, section coverage.** H2 headings: V1 4, V2 5, V3 5; max 5.
- quant_score = RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15. V1: 0.2471 + 0.2000 + 0.1350 + 0.1500 + 0.1200 = 0.8521. V2: 0.2647 + 0.2000 + 0.1500 + 0.1500 + 0.1500 = 0.9147. V3: 0.2471 + 0.1875 + 0.1500 + 0.1446 + 0.1500 = 0.8792.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Source: two independent scoring passes, `scoring/qual-pass-1.md` (order V1, V2, V3) and `scoring/qual-pass-2.md` (order V3, V2, V1), on the protocol's 6 dimensions and 30 criteria with Claim-Evidence-Verdict cells. The tables below give the **final** verdict per criterion: the agreed verdict where both passes agree, and the orchestrator's re-evaluated verdict where they disagree (marked †; reasons in Position-Bias Mitigation). Evidence is abbreviated; the full CEV text is in the two pass files. Keys: `Vn:N` = line N of the variant; `DA:N` = `diff-analysis.md`; `R1-Vn:N`, `R2-Vn:N` = round files; `SPEC:N`, `CAPS:N` as in the variants.

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. Covers all explicit requirements | MET | Safety, Reliability, Day to day, Cost sections (V1:7-21) | MET | Same four sections (V2:12-24) | MET | Same four sections (V3:10-22) |
| 2. Edge cases / failure scenarios | MET | Quoted-argument case (V1:8); misfire (V1:9); own forgotten-flag stall as "Known weakness" (V1:19) | MET † | Failures of its own routes: person's `/sc:cleanup --interactive` losing prompts (V2:13); invisible wrong guess (V2:17); print signal not firing (V2:19) | NOT MET † | Names only failures of (a) that it fixes (V3:12) and the coordinator-only case (V3:13); no failure scenario of its own guard; missed the flagless P0 and `/sc:load` briefs (DA:52, X-005; conceded R1-V3:42) |
| 3. Dependencies / prerequisites | MET | Phase gating (V1:15); brief template (V1:18); shared parse rule (V1:22) | MET † | Per-command detection text (V2:25); model recognition of prose (V2:14); SA-2 and non-goal 1 conflict (V2:18). The wrong AC-C1 prerequisite (DA:97) is scored under Correctness | MET † | Worker session that received the preamble and the WC-6 retry (V3:3); one rule in `WORKER-CONTRACT.md` (V3:17, V3:23) |
| 4. Success / completion criteria | MET | AC-1.1 and 7.2 checks (V1:13); AC-2.8 (V1:8) | NOT MET | None; "Not mechanically testable" (V2:17) | MET | 7.2 run with the flag omitted, with pass conditions (V3:16) |
| 5. Out of scope stated | NOT MET | None found in V1:3-23 | NOT MET | None found in V2:3-25 | NOT MET | None found in V3:3-23; scope limits appear only in rounds (R2-V3:33) |
| **Subtotal** | **4/5** | | **3/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. No factual errors or invented claims | NOT MET | V1:23 "add detection later" conflicts with SA-2 (DA:51), conceded wrong (R1-V1:40); "Deterministic" overstated (R1-V1:39) | NOT MET | `CAPS:47` OVERSTATED (DA:96); AC-C1 exception WRONG (DA:97); both withdrawn (R1-V2:37-38) | NOT MET | `[G]` 78-82 range OVERSTATED for identity (DA:100; conceded R2-V3 #5); "Deterministic" overstated (R1-V3:44) |
| 2. Feasible with stated constraints | MET | Fits SA-2, non-goal 1 and the phase plan (V1:14-15; `SPEC:54`, `SPEC:187-197`) | NOT MET | Breaks SA-2 and non-goal 1 (V2:18), conceded both need amending (R2-V2 #4) | NOT MET | Guard as written refuses the spec's own flagless briefs (V3:3, V3:23; DA:52), conceded (R1-V3:42) |
| 3. Terminology consistent | MET | "standalone token", "brief", "coordinator", "person" used in one sense (V1:3-19) | MET | "environment route" vs "preamble" kept distinct (V2:13-14) | MET | "worker session" defined (V3:3) and used consistently (V3:8, 17, 23) |
| 4. No internal contradictions | NOT MET | V1:13 vs V1:22 (X-003); V1:23 vs V1:14 (X-004) | NOT MET | V2:9 vs V2:17 (X-002); V2:3 vs V2:13 | NOT MET | V3:16 vs V3:17 (X-003) |
| 5. Claims supported by evidence | MET | Every Safety and Reliability bullet cited, citations confirmed (V1:8-15; DA:92) | NOT MET † | Three decision-relevant claims rest on support that fails: "shorter briefs" (V2:10 vs `SPEC:57`, X-006), preamble on the same line (`CAPS:47`, DA:96), AC-C1 exception (DA:97) | MET | `CAPS:73` failure signal (V3:12, DA:95 CONFIRMED); `CAPS:52` stall; `SPEC:70` WC-6; `SPEC:151` section 4 |
| **Subtotal** | **3/5** | | **1/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. Logical section ordering | MET | Position, key, then Safety to Cost (V1:3-21) | MET | Position, key, Strongest case, then Safety to Cost (V2:3-24) | MET | Position, key, Why a third option, then Safety to Cost (V3:3-22) |
| 2. Consistent hierarchy depth | MET | One H1, flat H2 (V1:1, 7, 12, 17, 21) | MET | One H1, flat H2 (V2:1, 7-24) | MET | One H1, flat H2 (V3:1, 7-22) |
| 3. Separation of concerns | MET | Each section holds its own topic (V1:8-23) | NOT MET | Testability in Safety (V2:14); constraint argument in Reliability (V2:18); Day to day restates a risk (DA:24) | MET | Critique isolated in "Why a third option" (V3:8); other sections on topic |
| 4. Navigation aids / cross-references | MET | Citation key (V1:5); AC/WC/SA cross-references | MET | Citation key with `[G]` (V2:5) | MET | Citation key (V3:5); "exactly as in option (a)" (V3:3) |
| 5. Follows position-file conventions | MET | One position (V1:3) | NOT MET | Two routes, never picks one (V2:3; DA:20) | MET | One position (V3:3) |
| **Subtotal** | **5/5** | | **3/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. Unambiguous language | MET | Firm wording, no hedge words (V1:1-23) | NOT MET | "either through `ORCA_TERMINAL_HANDLE` or through the worker preamble" (V2:3) | NOT MET | "one live check in P0 or P1" (V3:23), the root of X-005 |
| 2. Concrete rather than abstract | MET | `/sc:troubleshoot "the worker ignores --unattended"` (V1:8) | MET | `/sc:cleanup --interactive` scenario (V2:13) | MET | `worker_done --outcome failed` with reason `brief lacks --unattended` (V3:3) |
| 3. Each section has a clear purpose | MET | Each H2 summarizable (V1:7-21) | MET | Each H2 summarizable (V2:7-24) | MET | Each H2 summarizable (V3:7-22) |
| 4. Terms defined on first use | NOT MET | "brief", "7.2", SA-2 undefined (V1:3, 13, 14) | NOT MET | "brief", AC-C1, "outward defaults" undefined | NOT MET | WC-6, SA-2, "7.2 run" undefined |
| 5. Actionable next steps | MET | What to build (V1:22) | NOT MET | No route chosen, no steps (V2:3, V2:25) | MET | One sentence plus one live check (V3:23), pass conditions (V3:16) |
| **Subtotal** | **4/5** | | **2/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. ≥3 risks with probability and impact | NOT MET | Impact only (V1:9, 10, 19) | NOT MET | Impact only (V2:13, 17, 18) | NOT MET | Impact only (V3:8, 13) |
| 2. Mitigation per risk | MET | Misfire → flag immune (V1:9); forgotten flag → template and 7.2 proof (V1:19) | NOT MET | Misfire, wrong guess, SA-2 conflict stated with no mitigation (V2:13-18) | MET | Forgotten flag and coordinator-only → guard (V3:3, 13); person's tab → no command reads environment (V3:11) |
| 3. Failure modes and recovery | NOT MET | Stall caught "only after the fact" (V1:19); no recovery step | NOT MET | No recovery (V2:17) | MET | "The coordinator then fixes the brief in a new Task (WC-6, `SPEC:70`)" (V3:3) |
| 4. External dependencies and their failure | MET | `ORCA_TERMINAL_HANDLE` misfire, healthy-stall report (V1:9, 19) | MET | Environment misfire, print-mode signal (V2:13, 19) | MET | Orca's only guaranteed failure signal (V3:12, `CAPS:73`) |
| 5. Monitoring / validation mechanism | MET | AC-1.1, 7.2, AC-2.8 (V1:8, 13, 19) | NOT MET | "Not mechanically testable" (V2:17) | MET | 7.2 flag-omitted run (V3:16) |
| **Subtotal** | **3/5** | | **1/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. Collection boundaries | NOT MET | No empty/single/multi-command brief case (V1:3-23) | NOT MET | None (V2:3-25) | NOT MET | None; the empty P0 flag-accepting set was missed (X-005) |
| 2. State interactions across component boundaries | MET | Phase-conversion state × flag (V1:15); environment kept out of commands (V1:9) | NOT MET | Keeps the environment route despite showing the cross-terminal state misfires (V2:3 vs V2:13) | NOT MET † | The one cross-component interaction V3 adds, guard × the command's phase state, is handled wrongly as written (V3:3, V3:23; DA:52, DA:78; conceded R1-V3:42); the commands-read-no-state property is (a)'s, stated only as "Same as (a)" (V3:11) |
| 3. Guard condition gaps | MET | Quoted-argument guard (V1:8); forgotten-flag gap (V1:19) | MET | Environment variable does not separate worker from non-worker terminal (V2:13) | MET | Coordinator-only ban is prose only (V3:13, `SPEC:151`) |
| 4. Count divergence | NOT MET | None (V1:3-23) | NOT MET | "35 commands" is a count claim, not a divergence case (V2:10) | NOT MET | None (V3:3-23) |
| 5. Interaction effects when components combine | MET | Flag × WC-9 outward defaults (V1:10); flag × phase gating (V1:15) | MET † | Launch mode × reflect's headless rule (V2:19); detection × SA-2 (V2:18) | MET † | Guard × WC-6 retry (V3:3); guard × section 4 (V3:13) |
| **Subtotal** | **3/5** | | **2/5** | | **2/5** | |

### Qualitative Summary

| Dimension | V1 (option a) | V2 (option b) | V3 (option c) |
|---|---|---|---|
| Completeness | 4/5 | 3/5 | 3/5 |
| Correctness | 3/5 | 1/5 | 2/5 |
| Structure | 5/5 | 3/5 | 5/5 |
| Clarity | 4/5 | 2/5 | 3/5 |
| Risk Coverage | 3/5 | 1/5 | 4/5 |
| Invariant & Edge Case Coverage | 3/5 | 2/5 | 2/5 |
| **qual_score** | **22/30 = 0.733** | **12/30 = 0.400** | **19/30 = 0.633** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case subtotal | Floor (≥1/5) | Eligible as base |
|---|---|---|---|
| V1 | 3/5 | passes | yes |
| V2 | 2/5 | passes | yes |
| V3 | 2/5 | passes | yes |

The floor is not suspended (no variant scores 0/5).

## Position-Bias Mitigation

Pass 1 (`qual-pass-1.md`) scored in input order V1, V2, V3; Pass 2 (`qual-pass-2.md`) in reverse order V3, V2, V1. Neither pass read the other. Pass totals: V1 22 / 22, V2 12 / 10, V3 20 / 18. Of 90 criterion-variant pairs, 82 agree and 8 disagree. Every V1 verdict agrees.

Re-evaluation standard, applied the same way to every disagreement:
- Criteria that ask whether something is **present** (Completeness 2 and 3, Invariant 5) are MET when the variant text gives specific evidence for its **own** proposed mechanism. A case that the debate later showed was missed is not counted again here when a correctness or feasibility criterion already records it, so one defect is not scored in many cells.
- Criteria that ask whether something is **correct or validly supported** (Correctness 5, Invariant 2) are decided by the conceded defects, because those defects are exactly what the criterion measures.
- Pass 2's own "consistency rule" (`qual-pass-2.md:9`) is not part of the protocol rubric; it was weighed as one input, not followed automatically.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation (evidence from both passes plus the source text) |
|---|---|---|---|---|---|---|
| Completeness 2 (edge cases / failures) | V2 | MET | NOT MET | DISAGREE | **MET** | P1 cites V2:13, V2:17, V2:19; P2 cites the missed Agent-tool boundary (R2-V2:18). V2:13-14 and V2:17 name failure scenarios of V2's own two routes with their consequences. The missed subagent case is already recorded in Correctness 2 (feasibility). |
| Completeness 2 (edge cases / failures) | V3 | MET | NOT MET | DISAGREE | **NOT MET** | P1 cites V3:3, V3:12, V3:13; P2 cites X-005 and R1-V3:42. Re-reading V3:3-23: every failure V3 names is a failure of option (a) that the guard fixes, or the coordinator-only case it adds. V3 names no failure scenario of its own guard, and its central edge case (legitimate flagless briefs, `SPEC:191`, `SPEC:197`) is absent. DA:19 records "no self-critique"; its advocate added guard-misfire risk only in R1-V3:46. Under the own-mechanism standard this is not met; V1 (V1:19) and V2 (V2:13, V2:17) meet it. |
| Completeness 3 (dependencies) | V2 | MET | NOT MET | DISAGREE | **MET** | P1 cites V2:25, V2:14; P2 cites the WRONG AC-C1 prerequisite (DA:97). V2 also states per-command detection text (V2:25), dependence on model recognition (V2:14) and the SA-2 / non-goal 1 conflict (V2:18). The wrong AC-C1 claim is already penalized in Correctness 1 and 5. |
| Completeness 3 (dependencies) | V3 | MET | NOT MET | DISAGREE | **MET** | P1 cites V3:3 (worker session, WC-6, `SPEC:61`, `SPEC:70`) and V3:17/23; P2 cites the missing ship-after-P0 prerequisite and the template delivery path (R2-V3 #3). V3 does state its dependencies; the phase-timing miss is penalized in Correctness 2 and Clarity 1, and the delivery-path gap is a gap in a stated dependency, not an absent one. |
| Correctness 5 (claims supported) | V2 | NOT MET | MET | DISAGREE | **NOT MET** | P1 cites X-006 and DA:96-97; P2 cites the confirmed citations at V2:8, V2:9, V2:19. Three of V2's decision-relevant claims rest on support that fails on re-reading: "shorter briefs and no new flag on 35 commands" (V2:10) is contradicted by `SPEC:57`; the preamble-on-the-same-line claim (V2:14) is not in `CAPS:47`; the AC-C1 exception (V2:25) does not follow from `SPEC:205-212`. V1 and V3 each have at most one weakly supported claim, outside their main rationale. |
| Invariant 2 (state interactions) | V3 | NOT MET | MET | DISAGREE | **NOT MET** | P1 cites X-005 and A-005 (DA:52, DA:78); P2 cites V3:3, V3:8, V3:11. The criterion asks whether interactions are **handled**. The interaction V3 introduces beyond (a), its worker-session guard against each command's phase state (`SPEC:187-195`), is handled wrongly as written (V3:3 refuses every flagless brief; V3:23 "P0 or P1"), conceded at R1-V3:42. The property that commands read no state is inherited from (a) (V3:11 "Same as (a)"). |
| Invariant 5 (interaction effects) | V2 | MET | NOT MET | DISAGREE | **MET** | P1 cites V2:19; P2 cites the missed Agent-tool interaction (R2-V2:18). The criterion asks whether interaction effects are **considered**; V2:18 (detection × SA-2) and V2:19 (Orca launch mode × reflect's headless rule) do so specifically. The missed case is recorded in Correctness 2. |
| Invariant 5 (interaction effects) | V3 | MET | NOT MET | DISAGREE | **MET** | P1 cites V3:3 and V3:13; P2 cites the missed guard × phase-plan interaction. V3 considers guard × WC-6 retry (V3:3) and guard × section 4 (V3:13). The missed guard × phase interaction is recorded in Invariant 2 and Correctness 2. |

Disagreements re-evaluated: 8
Final verdicts matching Pass 1: 7; matching Pass 2: 1 (V3 Completeness 2)
Final verdicts changed: 1 relative to Pass 1 (V3 Completeness 2, MET → NOT MET); 7 relative to Pass 2
Effect on totals: V1 22 (unchanged), V2 12 (Pass 1 12, Pass 2 10), V3 19 (Pass 1 20, Pass 2 18)

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker (points won of 31) |
|---|---|---|---|---|
| V1 (option a) | 0.852 × 0.5 = 0.426 | 0.733 × 0.5 = 0.367 | **0.793** | 3 (9.7%): S-002, C-007, X-006 |
| V3 (option c) | 0.879 × 0.5 = 0.440 | 0.633 × 0.5 = 0.317 | **0.756** | 12 (38.7%): S-004, S-006, C-003, C-004, C-006, C-010, C-011, X-002, X-004, X-005, X-007, A-009 |
| V2 (option b) | 0.915 × 0.5 = 0.457 | 0.400 × 0.5 = 0.200 | **0.657** | 1 (3.2%): C-012 |

**Margin**: top two are V1 (0.7927) and V3 (0.7563); difference 0.036, which is below the 0.05 threshold.
**Tiebreaker applied**: Yes, level 1 (debate performance). V3 won 12 diff points in the Step 2 scoring matrix and V1 won 3 (`debate-transcript.md`, Scoring Matrix). The difference (38.7% vs 9.7%) is far outside 5%, so level 1 decides and levels 2 (correctness count: V1 3, V3 2) and 3 (input order) are not reached.

Sensitivity:
- With the vague-word form of SR (1.000 for all), V1 scores 0.800 and the margin is 0.044: still a tie, same outcome.
- With Pass 1's verdicts alone, V3 scores 0.773 (margin 0.020): tie, same outcome.
- With Pass 2's verdicts alone, V3 scores 0.740 (margin 0.053): just outside the tie band, and V1 would be selected on score. The selection therefore rests on the re-evaluated verdicts plus the debate tiebreaker, not on a clear score lead. This matters little for the outcome: V3's command side is V1's ("exactly as in option (a)", V3:3), and deleting the guard returns exactly (a) (R2-V3 #13), so the refactoring plan produces the same merged position from either base. V3 needs fewer changes to reach it.

## Selected Base: Variant 3 (option c, flag plus worker-session guard)

### Selection Rationale
- **Tiebreaker.** V1 leads on the combined score by 0.036, inside the 0.05 tie band. The protocol's level-1 tiebreaker is debate performance, and V3 won 12 of 31 diff points against V1's 3. V3 won every high-severity point about the forgotten-flag stall (C-004 98%, X-002 98%, X-007 96%), coordinator-only commands (C-011 97%), and where the Orca-aware check belongs (S-004 95%, X-004 95%).
- **The debate converged on V3's position.** All three advocates' Round 2 recommendation is option (c) as corrected in R1-V3:16-21 with the Round 2 amendments (R2-V1:76, R2-V2:86, R2-V3:79). The invariant probe confirms this consensus (`invariant-probe.md`, "Emerging consensus").
- **V3 is V1 plus one mechanism.** Its command side is option (a) unchanged (V3:3, V3:11), so V1's command-side strengths carry over without restructuring, while V1 as base would need the whole guard added.
- **Why V3 scored below V1 qualitatively.** Its original guard wording (V3:3 "no standalone `--unattended` ... it does not run it", V3:23 "P0 or P1") refused the spec's own flagless briefs (X-005), which cost it Correctness 2, Clarity 1 and Invariant 2, and it offered no self-critique (Completeness 2). These are fixable defects, already fixed in the debate (R1-V3:16-21, R2-V3 #11), and the refactoring plan applies the fixes.
- **Why not V2.** Lowest combined score (0.657), lowest qualitative score (12/30), and withdrawn by its own advocate (R2-V2:86). Its unique contributions survive as inputs to (c).
- Edge case floor: V3 is eligible (2/5).

### Strengths to Preserve from Base
1. Commands switch only on the standalone `--unattended` token, read no environment and no conversation, and so keep SA-1 and SA-2 (V3:3, V3:11; `SPEC:55`, `SPEC:169`, `SPEC:170`). Scoring matrix C-001, C-005 (equal V1/V3, 97% / 96%).
2. The Orca-aware check lives in the worker session, which already has Orca duties (WC-3, WC-5, WC-7, WC-12 at `SPEC:67-76`) and which SA-2 does not govern (V3:8). S-004, X-004.
3. A forgotten flag becomes an immediate `worker_done --outcome failed` with a reason, the only failure signal Orca guarantees (V3:12; `CAPS:73`), instead of a stall Orca reports as healthy (`CAPS:52`). C-004, X-002, X-007.
4. The guard refuses the six coordinator-only commands, which today only section 4's prose forbids (V3:13; `SPEC:150-160`). C-011.
5. Recovery path: the coordinator fixes the brief in a new Task (V3:3; WC-6, `SPEC:70`). Risk Coverage 3, MET only for V3.
6. A concrete live check with pass conditions (V3:16). C-003.
7. Cheap reversal: removing the guard sentence returns exactly option (a) (V3:23; R2-V3 #13).

### Strengths to Incorporate from Non-Base Variants and the Debate
From Variant 1 (option a):
1. WC-9 link: outward defaults turn off only under the flag, so a person working in Orca keeps auggie-review's posting default (V1:10; `SPEC:73`, `SPEC:169`; U-002, C-002).
2. Phase gating stated explicitly: a command accepts the flag only once its gates are converted (V1:15; `SPEC:187-195`; U-003, C-013).
3. The quoted-argument example `/sc:troubleshoot "the worker ignores --unattended"` and its live check AC-2.8 (V1:8; `SPEC:269`).
4. Honest wording that the parse is a model applying a rule, not code (V1:22; U-001), replacing V3's "Deterministic" (X-003).
5. A named "known weakness" section (V1:19; S-002), adapted to state the guard's own residual gaps.

From Variant 2 (option b):
6. Orca's role table as the guard's trigger: a session with a live preamble carrying Task and Dispatch IDs is a dispatched worker (`[G]` 38, 41; `CAPS:148`; `SPEC:53`; U-004, C-010), replacing V3's overstated `[G]` 78-82 range.
7. The reflect `claude --print` precedent does not fire for an Orca worker, so an explicit switch is needed (V2:19; `SPEC:391`; U-006, C-012).
8. `ORCA_TERMINAL_HANDLE` marks any live Orca terminal by design (`CAPS:149`, `CAPS:151`; R2-V2 New evidence 2), which closes the environment route without relying on the unverified `worker-list` reading (A-001).

From the debate's concessions and refinements:
9. Key the guard to the command's `## Unattended mode` section, which AC-1.1 already ties to the phase table, so it is inert in P0 and never refuses `/sc:load` (R1-V3:16-21; `SPEC:191`, `SPEC:197`, `SPEC:257`; X-005, A-005).
10. Make the check symmetric: refuse when the flag and the section disagree in either direction (R2-V1:35, New evidence 3; R2-V3 #11).
11. Ship the guard in P1, not P0 (R1-V3:21; R2-V3 New evidence 1).
12. Put the guard sentence in the brief template as well as in `WORKER-CONTRACT.md`, because nothing loads the contract file automatically (R2-V1 #5; R2-V2 critique 2; R2-V3 #3).
13. Amend `SPEC:79` to "where the command accepts it at this phase" (R1-V1 A-005; R2-V1 #10).
14. The flag crosses the Agent-tool subagent boundary and the preamble does not (R2-V1 New evidence 1; R2-V2 New evidence 1; `SPEC:145`; `TL:1618`, `TL:1623`).
15. Guard scope: top-level commands only; nested Agent-tool fan-out relies on AC-2.1 (R2-V3 New evidence 2; `SPEC:263`).
16. Three checks: a static assertion in `test_worker_contract.py`, AC-1.2 plus one P1 flag-omitted run, and the discriminating P2 bare-topic tdd run (R2-V3 New evidence 1, R2-V3:86-89).
17. A brief written without the template falls back to (a), never worse (R2-V3 #3; INV-019).
