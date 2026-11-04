# Base Selection Report

- Decision D3 (`/sc:pr-submit` as an Orca worker), `/sc:adversarial` Mode A, Step 3. Assembled by the debate-orchestrator (non-advocating), 2026-11-02T16:25:11Z.
- Variant 1 = option (a), coordinator or person only; Variant 2 = option (b), worker with pre-authorization; Variant 3 = option (c), unsupervised orca-cli handoff to a person-owned agent tab. The scored text is each `variant-N-original.md`; `V1:N` etc. are line numbers in those files.
- Inputs: `scoring/qual-pass-1.md` (input order V1, V2, V3), `scoring/qual-pass-2.md` (reverse order V3, V2, V1), `diff-analysis.md` (DA), `invariant-probe.md` (INV), `rounds/`, and `debate-transcript.md` (scoring matrix). Sources re-read for the re-evaluations: `src/superclaude/commands/pr-submit.md` (PRC) 1-91; `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (PRS) 36-85, 264-277; spec (SPEC) 53-56, 66-75, 137, 156, 185, 195-197, 276, 339-348, 391-394; `orca-capabilities.md` (CAPS) 47, 52, 161; `HOW-WE-WORK.md` (HWW) 212-223; `CLAUDE.md:50,65`; `decisions/D4/option-c.md:1-5`; `orca-ide skills get orca-cli` lines 1-8, 25-32, 49-66.

## Quantitative Scoring (50% weight)

Computed by a script over the three variant files (no judgment except where a rule below says a line was checked against its source). Exact counting rules:

- **RC, requirement coverage.** No requirement IDs (FR-/NFR-/R-) exist for D3, so section-level topic matching is used, as the protocol's edge case directs. Topics: the four the D3 options were asked to cover (safety, reliability, day-to-day use, implementation cost) plus the content topics C-001..C-013 of `diff-analysis.md`. C-009 (implementation cost) and C-012 (what the person sees day to day) duplicate two of the four headline topics and are counted once, giving 15 topics. A topic is covered when its keyword appears in the variant (case-insensitive): Safety / Reliability / day-to-day / Implementation cost headings; C-001 `headless`; C-002 `push|outward`; C-003 `HALT`; C-004 `parallel`; C-005 `stays free|other workers' questions`; C-006 `completion signal|worker_done|summary`; C-007 `heartbeat`; C-008 `D4`; C-010 `--resume|run-log`; C-011 `top-level`; C-013 `reversible|later`. The misses agree with DA's own cells (C-006 V1 "Implicit", C-008 V1 "None stated", C-010 V1 "Not discussed", C-013 V2 "Not discussed").
- **IC, internal consistency.** Scorable claims = body sentences (headings and the citation-key line excluded) that carry a citation or a number. Contradictions = DA's internal contradictions: V2 X-001 ("It already fits a worker technically", V2:9, against "either rewrites that boundary or treats the worker's session as 'attended'", V2:13); V3 X-004 ("the coordinator does not create a Task or wait on it", V3:3, and its cited "do not monitor completion", against "the coordinator reads the run-log file later", V3:17). DA lists none for V1.
- **SR, specificity ratio.** Concrete = backticked spans (commands, flags, citations, named files) plus bare numbers outside backticks. Vague = occurrences of: appropriate, as needed, properly, adequate, should consider, might, various, etc., best practice, industry standard, usually, rarely, often, maybe, probably.
- **DC, dependency completeness.** References = (1) every citation token, resolved when its prefix is defined in the variant's own citation key (or the token is a repo path such as `CLAUDE.md:50`); plus (2) every bare spec-item identifier (WC-N, AC-N.N, D4, P4 / Phase 4, "section N"), resolved only when the same bullet carries a locator whose source line is that item (checked against the spec). Option labels (a)/(b)/(c) are the decision's shared vocabulary and are not counted.
- **SC, section coverage.** H2 count over the maximum H2 count (5).

| Metric | Weight | Variant 1 (option a) | Variant 2 (option b) | Variant 3 (option c) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.800 (12/15; misses C-006 completion signal, C-008 D4, C-010 resume) | 0.933 (14/15; misses C-013 reversibility) | 1.000 (15/15) |
| internal_consistency | 0.25 | 1.000 (1 - 0/10) | 0.923 (1 - 1/13; X-001) | 0.909 (1 - 1/11; X-004) |
| specificity_ratio | 0.15 | 0.935 (29 concrete: 23 backticked + 6 numbers; 2 vague: "usually", "rarely", V1:17) | 1.000 (32 concrete: 25 + 7; 0 vague) | 1.000 (25 concrete: 18 + 7; 0 vague) |
| dependency_completeness | 0.15 | 1.000 (20/20: 17/17 citation tokens; 3/3 spec items: Phase 4 → `SPEC:341`, WC-10 → `SPEC:74`, AC-4.3 → `SPEC:276`) | 0.821 (23/28: 19/19 tokens; 4/9 spec items: section 3.2 → `SPEC:137`, AC-4.3 ×2 → `SPEC:276`, P4 → `SPEC:185` resolve; D4 ×3 and WC-6 ×2 do not, since `SPEC:137` / `SPEC:342` are not D4, which is at `SPEC:345`, and no WC-6 locator is given) | 0.786 (11/14: 11/11 tokens; 0/3 spec items: D4 (V3:13), "section 4 / D3" and AC-4.3 (V3:23) carry no locator) |
| section_coverage | 0.15 | 0.800 (4/5) | 1.000 (5/5) | 1.000 (5/5) |
| **quant_score** | | **0.900** | **0.934** | **0.945** |

Arithmetic: V1 = 0.30(0.800) + 0.25(1.000) + 0.15(0.935) + 0.15(1.000) + 0.15(0.800) = 0.9003. V2 = 0.30(0.933) + 0.25(0.923) + 0.15(1.000) + 0.15(0.821) + 0.15(1.000) = 0.9340. V3 = 0.30(1.000) + 0.25(0.909) + 0.15(1.000) + 0.15(0.786) + 0.15(1.000) = 0.9451.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts after position-bias resolution. Where both passes agreed, the evidence is theirs (condensed). Cells marked **[R]** were re-evaluated because the passes disagreed; the reasoning is in "Position-Bias Mitigation". MET = 1, NOT MET = 0.

### Completeness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. Covers the decision's requirements (safety, reliability, day-to-day, cost) | MET | All four H2 sections (V1:7, 12, 16, 20). | MET | All four (V2:12, 16, 20, 23). | MET | All four (V3:10, 15, 19, 22). |
| 2. Edge cases and failure scenarios | MET **[R]** | HALT failure and who acts on it: "Its HALTs (for example `pr_head_mismatch` ...) are written for an operator to act on" (V1:10); held coordinator (V1:18); single-PR case (V1:17). | MET | HALT → blocked contract (V2:18); unverified poll runtime (V2:17); unwatched push (V2:14). | MET | HALT in a visible tab (V3:11); no completion signal and UNVERIFIED prompt path (V3:17). |
| 3. Dependencies and prerequisites | NOT MET | Only the top-level rule (V1:13); no D4 or authorization prerequisite (DA C-008 "None stated"), conceded R2-V1 #13; PR-head checkout conceded R2-V1 #16. | MET | P4 row, AC-4.3, D4 dependency named (V2:24); detail WRONG, scored under Correctness. | MET | Launch mechanism (V3:3), person's instruction (V3:13), argv prompt dependency (V3:17, `CAPS:47`). |
| 4. Success / completion criteria | NOT MET | None; "Reversible later ..." (V1:21) is a switch trigger. | MET | "AC-4.3 must show no single Bash call exceeds 240 s (`SPEC:276`)" (V2:17). | NOT MET | No pass condition for the handoff route; smoke test appears only in R2-V3 and is undefined (INV-008). |
| 5. Out of scope stated | MET | "pr-submit gets no Phase 4 changes" (V1:3); "no pr-submit edits, no AC-4.3 run" (V1:21). | MET **[R]** | "outward actions as D4 decides" (V2:3) explicitly places outward-action authorization outside D3. | MET | "gets no `--unattended` mode"; "does not create a Task or wait on it" (V3:3); "no pr-submit edits, no AC-4.3" (V3:23). |
| **Subtotal** | **3/5** | | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. No factual errors | NOT MET | "contradicts the command's stated design" (V1:8) rests on worker = headless, DA A-001 CONTRADICTED, conceded R2-V1 #4-5; `CAPS:161` overstated for the coordinator (DA incidental 1). | NOT MET | "Depends on D4 (a) or (c) for any push" (V2:24) WRONG (DA spot-check 6; `D4/option-c.md:3`; `SPEC:347`). | NOT MET | `CAPS:52` OVERSTATED (V3:11; DA spot-check 4); `[G] 39` quoted without "and do not monitor completion" (V3:12; DA spot-check 3). |
| 2. Feasible with stated constraints | MET | Runs the existing command unchanged in a top-level session (V1:3, V1:13; `SPEC:341`). | NOT MET | Under its own stated "D4 (c)" a worker never pushes (`D4/option-c.md:3`), and `HWW:223` then says "withhold execution"; conceded R2-V2 #3. | MET **[R]** | `agent launch ... --prompt` exists as cited (DA spot-check 2; orca-cli lines 49-52); the one unproven step is stated by the variant (V3:17). |
| 3. Consistent, accurate terminology | NOT MET | "not headless" and "no person at the keyboard" used as one concept (V1:8); DA A-001. | NOT MET | "Will Not: run headless ... treats the worker's session as 'attended'" (V2:13). | NOT MET **[R]** | "makes an attended, top-level, 'Will Not: run headless' command ... into an unattended worker" (V3:8); DA A-001 names V3; V3 accepted the correction (R1-V3 A-001). |
| 4. No internal contradictions | MET | DA X-001..X-005 list no V1 self-contradiction. | NOT MET | X-001 (V2:9 vs V2:13); conceded R2-V2 #11. | NOT MET | X-004 (V3:3 and `[G] 39` vs V3:17); conceded R1-V3 Concession 1. |
| 5. Claims supported by evidence | NOT MET | "parallel PR monitoring is rarely needed" (V1:17) unsourced; withdrawn R2-V1 #1. | NOT MET | D4 dependency (V2:24) uncited and WRONG. | NOT MET **[R]** | "A HALT waits in a visible tab" (V3:11) is supported only by a startup-readiness line (`CAPS:52`) and is contradicted by `PRS:268` / `PRS:274` (HALTs end the run with `terminal_halted`). |
| **Subtotal** | **2/5** | | **0/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. Logical ordering | MET | Position, key, Safety, Reliability, Day to day, Cost (V1:3-21). | MET | Position, key, Strongest case, then the four (V2:3-24). | MET | Position, key, Why a third option, then the four (V3:3-23). |
| 2. Consistent hierarchy depth | MET | One H1, flat H2s, bullets. | MET | One H1, flat H2s, bullets. | MET | One H1, flat H2s, bullets. |
| 3. Separation of concerns | MET | Each section stays on its label (V1:8-21). | NOT MET | Reliability material (durability, heartbeat fit) sits in "Strongest case" (V2:9) while Reliability argues against it (V2:16-18); DA S-006. | MET | Safety (V3:11-13), Reliability (V3:16-17), Cost (V3:23). |
| 4. Navigation aids / cross-references | MET | Citation key (V1:5); refs to WC-10, AC-4.3. | MET | Citation key (V2:5); refs to WC-6, D4, AC-4.3. | MET | Citation key with guide version 1.4.237 (V3:5); refs to D4, section 4 / D3. |
| 5. Position-file conventions | MET | Baseline shape (DA S-001). | MET | Same shape. | MET | Same shape. |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. Unambiguous language | NOT MET **[R]** | "A run usually opens one PR at the end, so parallel PR monitoring is rarely needed" (V1:17): vague frequency words carry the hinge of `SPEC:343`. | NOT MET | Unresolved either/or (V2:13) and "outward actions as D4 decides" (V2:3). | NOT MET **[R]** | Unresolved either/or on who reads the outcome: "The person reads each tab, or the coordinator reads the run-log file later" (V3:17). |
| 2. Concrete | MET | "35 rather than 36 commands" (V1:21); 600 s (V1:18). | MET | "`--monitor 1` refused" (V2:3); 240 s (V2:17). | MET | Full `agent launch` command line (V3:3). |
| 3. Clear section purpose | MET | One-phrase H2s. | MET | One-phrase H2s. | MET | One-phrase H2s. |
| 4. Terms defined on first use | NOT MET | WC-10, AC-4.3, Phase 4 undefined. | NOT MET | WC-6, D4, AC-4.3, P4 undefined. | NOT MET | D4, AC-4.3, HALT undefined. |
| 5. Actionable decision points | MET | Trigger and action for switching to (b) (V1:21). | MET | Build list (V2:24). | MET | "One sentence in section 4 / D3" (V3:23); launch on the person's instruction (V3:3). |
| **Subtotal** | **3/5** | | **3/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. At least 3 risks with probability and impact | NOT MET | No probabilities anywhere. | NOT MET | Risks named (V2:14, 17, 18), no probability. | NOT MET | Risks named (V3:17), no probability. |
| 2. Mitigation for each risk | NOT MET | Held coordinator (V1:18) unmitigated. | NOT MET | Slower HALT handling (V2:18) unmitigated. | NOT MET | UNVERIFIED prompt path (V3:17) unmitigated in the variant. |
| 3. Failure modes and recovery | NOT MET | Session loss and resume not discussed (DA C-010); conceded R2-V1 #14-15. | MET | HALT → blocked contract and new Task (V2:18); run-log plus `--resume` (V2:9). | MET | Run-log and `--resume` "work as today" (V3:16); person steps in on a HALT (V3:20). |
| 4. External dependencies and their failure | NOT MET | gh, review App, CI preflight absent (DA A-006; INV-009). | MET | Poll-script runtime UNVERIFIED against the 240 s bound (V2:17, `SPEC:394`). | MET | Orca argv prompt path UNVERIFIED (V3:17, `CAPS:47`). |
| 5. Monitoring or validation mechanism | NOT MET | None; "no AC-4.3 run" (V1:21). | MET | AC-4.3 on a scratch fork PR (V2:17, V2:24). | NOT MET | "the coordinator gets no completion signal" (V3:17); visible is not watched (R1-V3 Concession 3). |
| **Subtotal** | **0/5** | | **3/5** | | **2/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. Collection boundaries (empty, single, maximum) | MET | Single-PR versus several-PR case (V1:17); INV-016 ADDRESSED. | NOT MET | Only "several PRs at once" (V2:8). | NOT MET | Only "several PRs" / "one tab per PR" (V3:3, V3:20); no upper bound (INV-015). |
| 2. State interactions across components | MET | Coordinator's waits against other workers' questions (V1:18). | MET | HALT → blocked contract → new Task; run-log ↔ WC-6 (V2:9, 18). | MET | Coordinator holds no Task state; run state in run-log (V3:3, 16, 17). |
| 3. Guard condition gaps | MET **[R]** | Names a missing validation: per-iteration poll runtime UNVERIFIED while the WC-10 heartbeat rule depends on it (V1:14; `SPEC:394` item 12). | MET | What pr-submit's guards do not cover under an unwatched push (V2:14, `PRC:85`). | MET **[R]** | Names the launch as an outward start that needs a guard and supplies one: "the coordinator does it only when the person's instruction names it" (V3:13). |
| 4. Count divergence | NOT MET **[R]** | States per-wait and per-cycle upper bounds (V1:18) but counts one wait per cycle; the loop has three kinds of wait (`PRS:51-54`), so the hold is undercounted (INV-013). No divergence analysis. | MET | Per-iteration versus cumulative bound (V2:9 vs V2:17). | NOT MET | None; duplicate monitors (INV-012) raised only in R1-V3 Concession 5. |
| 5. Interaction effects when components combine | MET **[R]** | pr-submit × unattended mode (V1:8), × the repo's mandatory PR rule (V1:9), × the coordinator's other workers (V1:18). | MET | pr-submit × D4 × WC-10 × WC-6 (V2:9, 18, 24). | MET | Handoff route × top-level rule (V3:8), × the workers' shared argv mechanism (V3:17). |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

### Qualitative Summary

| Dimension | Variant 1 (a) | Variant 2 (b) | Variant 3 (c) |
|---|---|---|---|
| Completeness | 3/5 | 5/5 | 4/5 |
| Correctness | 2/5 | 0/5 | 1/5 |
| Structure | 5/5 | 4/5 | 5/5 |
| Clarity | 3/5 | 3/5 | 3/5 |
| Risk Coverage | 0/5 | 3/5 | 2/5 |
| Invariant & Edge Case Coverage | 4/5 | 4/5 | 3/5 |
| **qual_score** | **17/30 = 0.567** | **19/30 = 0.633** | **18/30 = 0.600** |

For reference, unresolved pass totals were V1 18 / 15, V2 19 / 18, V3 18 / 19 (Pass 1 / Pass 2).

### Edge Case Floor Check

| Variant | Invariant & Edge Case subtotal | Floor (at least 1/5) | Eligible as base |
|---|---|---|---|
| Variant 1 (a) | 4/5 | met | yes |
| Variant 2 (b) | 4/5 | met | yes |
| Variant 3 (c) | 3/5 | met | yes |

No variant is excluded; the floor suspension rule does not apply.

## Position-Bias Mitigation

Completion note (2026-11-02, after the 16:28 UTC dev-environment restart): this section, "Combined Scoring" and "Selected Base" were still `<!-- TODO -->` when the run stopped. They were completed from the verdicts already written above and in `scoring/qual-pass-1.md` (P1) and `scoring/qual-pass-2.md` (P2). No cell was rescored: every Final verdict below is the **[R]** verdict already recorded in the qualitative tables; the reason column restates the evidence those cells cite.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Reason for the final verdict (from the [R] cell) |
|---|---|---|---|---|---|---|
| Completeness 2 (edge cases, failures) | V1 | MET | NOT MET | DISAGREE | MET | P2 treated the HALT line as generic; V1:10 names a failure (`pr_head_mismatch` HALT) and who acts on it, and V1:18 names the held-coordinator edge, which is what the criterion asks. |
| Completeness 5 (out of scope) | V2 | MET | NOT MET | DISAGREE | MET | "outward actions as D4 decides" (V2:3) explicitly places outward-action authorization outside D3, which is a scope exclusion; P2 read only the `--monitor 1` rule. |
| Correctness 2 (feasible) | V3 | MET | NOT MET | DISAGREE | MET | The launch verb and `--prompt` exist as cited (DA spot-check 2); the one unproven step is disclosed by the variant itself (V3:17). INV-017 is a pre-PR gap common to (a) and (c), not an infeasibility of (c)'s own mechanism. |
| Correctness 3 (terminology) | V3 | NOT MET | MET | DISAGREE | NOT MET | V3:8 calls the command "'Will Not: run headless' ... into an unattended worker", the same headless/unattended conflation DA A-001 names for all three; V3 accepted the correction (R1-V3 A-001). |
| Correctness 5 (claims supported) | V3 | NOT MET | MET | DISAGREE | NOT MET | "A HALT waits in a visible tab" (V3:11) rests on a startup-readiness line (`CAPS:52`) and is contradicted by `PRS:268` / `PRS:274` (HALTs end the run with `terminal_halted`). One load-bearing unsupported claim fails the criterion. |
| Clarity 1 (unambiguous) | V1 | MET | NOT MET | DISAGREE | NOT MET | "usually" / "rarely" (V1:17) carry the hinge of `SPEC:343` (whether parallel monitoring is needed); vague frequency words on the deciding point fail the criterion. |
| Clarity 1 (unambiguous) | V3 | NOT MET | MET | DISAGREE | NOT MET | "The person reads each tab, or the coordinator reads the run-log file later" (V3:17) leaves who reads the outcome unresolved. |
| Invariant 3 (guard gaps) | V1 | MET | NOT MET | DISAGREE | MET | V1:14 names a missing validation the heartbeat rule depends on (per-iteration poll runtime UNVERIFIED, `SPEC:394` item 12). Its own missing authorization guard (INV-006) is scored under Completeness 3, not here. |
| Invariant 3 (guard gaps) | V3 | MET | NOT MET | DISAGREE | MET | V3:13 names the launch as an outward start needing a guard and supplies one (only on the person's instruction). |
| Invariant 4 (count divergence) | V1 | NOT MET | MET | DISAGREE | NOT MET | V1:18 states per-wait and per-cycle bounds but counts one wait per cycle; the loop has three kinds of wait (`PRS:51-54`), so the hold is undercounted (INV-013); no divergence analysis. |
| Invariant 5 (interaction effects) | V1 | MET | NOT MET | DISAGREE | MET | V1:8-9, V1:18 combine pr-submit with unattended mode, with the repo's mandatory PR rule (`CLAUDE.md:50`) and with the coordinator's other workers. Missing the D4 coupling (INV-017) does not erase the three named interactions. |

Disagreements re-evaluated: 11 (V1: 5, V2: 1, V3: 5). All other 79 cells agreed between the passes.
Final verdicts changed: 11 of 11 disagreements were settled by re-evaluation; 10 finals match Pass 1 and 1 matches Pass 2 (V1 Clarity 1). Net effect against Pass 1 totals: V1 18 → 17, V2 19 → 19, V3 18 → 18. Against Pass 2 totals: V1 15 → 17, V2 18 → 19, V3 19 → 18.

## Combined Scoring

`variant_score = 0.50 × quant_score + 0.50 × qual_score` (`~/.claude/skills/sc-adversarial-protocol/SKILL.md:1787`; `refs/scoring-protocol.md:188`). Computed from the unrounded inputs above.

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker (points won, `debate-transcript.md:607`) |
|---|---|---|---|---|
| Variant 2 (option b) | 0.4670 | 0.3167 | **0.7837** | 6 (sole 3, shared 3) |
| Variant 3 (option c) | 0.4726 | 0.3000 | **0.7726** | 9 (sole 1, shared 8) |
| Variant 1 (option a) | 0.4501 | 0.2833 | **0.7335** | 12 (sole 5, shared 7); not a top-two variant, so not used |

**Margin**: top two (V2, V3) differ by 0.0111, i.e. 1.1 points on the 0-1 scale (below the 0.05 threshold of `refs/scoring-protocol.md:197`).
**Tiebreaker applied**: Yes, level 1 (debate performance, `SKILL.md:1795-1798`). Variant 3 won 9 diff points against Variant 2's 6; 9 and 6 are not within 5% of each other, so level 2 (correctness count: V2 0/5, V3 1/5) is not reached. Variant 3 is selected.

Note for the reader: Variant 1 had the most debate wins (12) but its combined score is 0.0502 below Variant 2, just outside the 0.05 band, so the tiebreaker never compares it. The selection is a scoring artefact of which file is the merge base; it is not the debate's verdict on the option. The debate's verdict is the unanimous Round 2 position (`debate-transcript.md:665`): (a) is the default, (c) is the person-requested parallel route, (b) is deferred.

## Selected Base: Variant 3 (option c, unsupervised orca-cli handoff)

### Selection Rationale
Variant 3 is selected by the level-1 tiebreaker (9 diff points won against Variant 2's 6) after its combined score (0.7726) fell within 0.05 of Variant 2's (0.7837). It is also the variant whose text already contains the debate's converged shape: it keeps pr-submit out of the worker contract exactly as (a) does ("pr-submit is never a supervised worker (as in (a)) and gets no `--unattended` mode", V3:3) and adds the person-requested parallel route that all three advocates adopted in Round 2 (`debate-transcript.md:557`, `:665`). Its weaknesses, which the merge must repair: correctness 1/5 (overstated `CAPS:52`, the X-004 self-contradiction, the HALT-waits claim against `PRS:268` / `PRS:274`), no success criterion for its route, and no count or boundary coverage (INV-008, INV-012, INV-015).

### Strengths to Preserve from Base
1. pr-submit stays outside the worker contract: no `--unattended` mode, no Phase 4 edits, no AC-4.3 (V3:3, V3:23; matches C-009, S-004).
2. The full handoff launch command and its Orca citation (V3:3; `[CLI]` lines 49-52, DA spot-check 2 CONFIRMED).
3. The launch is an outward start and happens only on the person's instruction (V3:13; INV-019 ADDRESSED once anchored on `HWW:215` / `HWW:221`).
4. Parallel monitoring with pr-submit unchanged (C-004, sole win).
5. Recovery by run-log and `--resume`, unchanged (V3:16; C-010).
6. The disclosed UNVERIFIED argv slash-command step (V3:17; `CAPS:47`).

### Strengths to Incorporate from Non-Base Variants
1. From Variant 1, Position and "How a person works day to day" (V1:3, V1:17): the single-session route as the default, with (c) only when the person asks for several PRs at once (S-003, C-002, A-004, X-005 sole wins; INV-016 ADDRESSED).
2. From Variant 1, Safety (V1:9): monitor 3 pushes without asking (`CLAUDE.md:50`), so the safety difference is visibility and who authorized the start (C-002).
3. From Variant 1, Implementation cost (V1:21): zero build cost and the "35 rather than 36" count (`SPEC:195`), and the reversibility trigger toward (b).
4. From Variant 2, Implementation cost and Reliability (V2:17, V2:24): an explicit pass condition, used here as the model for the (c) smoke test (Completeness 4, only V2 met it).
5. From Variant 2, Strongest case (V2:9): the corrected meaning of "attended" (X-001 to V2, unanimous): attended means in-session and not detached (`PRS:43-45`, `PRS:82-84`), so (b) is deferred, not rejected.
6. From Variant 2, Reliability (V2:18) and the Round 2 rebuttal: the `SPEC:137` row fix ("`ask` or `escalation`" contradicts WC-3, `SPEC:67`; INV-010).
7. From the invariant probe (all four HIGH items, which the convergence gate made mandatory, `debate-transcript.md:655`): the authorization guard for (a) (INV-006), one live monitor per PR (INV-012), the pre-PR commit, rebase and push steps and their D4 coupling (INV-017), and the gate list that makes the route sufficient (INV-023).
