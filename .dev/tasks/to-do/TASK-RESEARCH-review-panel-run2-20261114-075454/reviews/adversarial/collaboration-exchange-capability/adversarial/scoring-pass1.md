# Scoring Pass 1 (input order: Variant A = Proposal A, then Variant B = Proposal B), slot C-12

Scorer: c12 pass 1. Variants scored as written (variant-1-original.md, variant-2-original.md). The debate is used only as evidence of which claims are right or wrong. Round 2 concessions are not credited unless the original text has them. Staleness rule applied: pinned E2 tip 6c0984326cbb; facts from c44c98a77 on are [POST-BASELINE]; e2f2ac268 is not held against either variant.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A | Variant B |
|--------|--------|-----------|-----------|
| requirement_coverage | 0.30 | 1.0000 (15/15) | 0.9333 (14/15) |
| internal_consistency | 0.25 | 0.9620 (3 contradictions / 79 claims) | 0.9718 (2 contradictions / 71 claims) |
| specificity_ratio | 0.15 | 0.9620 (76 concrete / 79) | 0.9718 (69 concrete / 71) |
| dependency_completeness | 0.15 | 0.9091 (20/22 resolved) | 0.8421 (16/19 resolved) |
| section_coverage | 0.15 | 1.0000 (9 H2 / max 9) | 1.0000 (9 H2 / max 9) |
| **quant_score** | | **0.9712** | **0.9450** |

Arithmetic. A: 0.30 + 0.2405 + 0.1443 + 0.1364 + 0.15 = 0.9712. B: 0.28 + 0.2430 + 0.1458 + 0.1263 + 0.15 = 0.9450.

### RC detail (15 source items: 8 brief elements + 7 C-12 evidence facts)

| # | Item | A (section) | B (section) |
|---|------|-------------|-------------|
| 1 | position statement | yes (1) | yes (1) |
| 2 | design consequence, core and modules | yes (3.1-3.4) | yes (2) |
| 3 | evidence | yes (4) | yes (3 A-F) |
| 4 | consistency with C-01..C-03 | yes (2 table) | yes (4) |
| 5 | invariants preserved/endangered | yes (5) | yes (5) |
| 6 | test or measurement | yes (6, 7 items) | yes (6, 8 items) |
| 7 | effect on PR review and rf-qa | yes (7) | yes (7) |
| 8 | strongest objection and answer | yes (8) | yes (8) |
| 9 | E2: kit may beat every exchange design | yes (E1, 4.1) | yes (3.D) |
| 10 | r5 kit +59% elapsed on sonnet | yes (4.2) | yes (3.D) |
| 11 | act rates range 0 to 1.0 across probes | yes (E6: luna 4/5 and 5/5, r4 0, ember 0/4, r5 1/5 and 3/5) | NO: gives no act-rate figures; section 4 only says act-rate measurement needs the served model; 3.F gives k and delivered counts instead |
| 12 | only single smoke rows (pinned tip) | yes (4.2 stale-note, E8, E9) | yes (0 stale list) |
| 13 | lib/ absent r2-r5 (pinned tip) | yes (E3) | yes (0, 3.D) |
| 14 | hooks only in main-thread claude -p | yes (E5, 4.4) | yes (3.B heading, 3.C) |
| 15 | reflect-reviewer has no Bash | yes (3.3, E10) | yes (2.6, 3.C) |

### IC detail

Method: scorable claims = every row of an evidence, consistency, invariant, module or test table, every numbered claim or item, and every bullet or paragraph that states a falsifiable fact. A: sections 0 (5) + 1 (1) + 2 (4) + 3 (16) + 4 (24) + 5 (12) + 6 (7) + 7 (3) + 8 (7) = 79. B: sections 0 (6) + 1 (4 numbered) + 2 (8) + 3 (22) + 4 (3) + 5 (11) + 6 (8) + 7 (3) + 8 (6) = 71.

Contradictions, A (3):
1. 4.2 "no exchange arm has a matching control row" vs its own 4.3 "collaboration against the same-harness baseline" counted rows (debate-established; A conceded the wording).
2. 3.3 says H1 and the kit reach the tasklist and reflect module "through the reflect brief; no call-site change" vs section 2 and section 5 "no change to src/superclaude/cli/reflect" (the brief is built in `cli/reflect/ensemble.py`; probe INV-005, HIGH).
3. 6.4 pins the off state to "brief bytes equal today's brief" vs 3.1 item 1 (H1 ships unconditionally and changes the brief; probe INV-004, 6.4 vs 6.5 baselines).

Contradictions, B (2):
1. 2.2 "registered ... in `hooks.json`" vs 2.2/2.4 "arguments baked into per-reviewer `--settings`" and "off state emits no `--settings`" (X-006; B conceded it).
2. 1 (4) "with the switch off the cost is zero by construction" vs 2.2 "one installed hook script" copied to every user's `~/.claude/hooks/` (A-002, B conceded "partly false for B as I first wrote it").

Not counted: A's H2 re-ask inside `parse_block` (INV-009) is an unreconciled dependency that A names itself in section 2, not a contradiction.

### SR detail

Method: classify the same claim set as IC. Concrete = number, named file/line, named entity or threshold. Vague = no such anchor, or an unanchored hedge.
A: 76 concrete, 3 vague (5 "UV only; fork-only PR target; .dev/tasks/ staged | Unaffected"; 7 "What would change this" bullet; 8 "Residual risk" paragraph).
B: 69 concrete, 2 vague (1 claim (3) "the transport is where the open runtime questions become answerable"; 7 third bullet "Both consumers get ... a recorded place for a per-model capability fact").

### DC detail

Internal references only (section refs, E-rows, test or measurement numbers, defined terms). External ids (C-06, X-13, CL-x, r09, MR:917, R-21, INV-nnn of other slots) are excluded.
A: 22 references, 20 resolve. Unresolved: "slot B" in 6.1 (no such slot is defined in A; means position B) and "A1" first used in 4.2 and never defined (A2 is defined in 1). Resolved: "see 3.4" (1), "3.1 item 2" (2, 8), "3.4" (3.3, 5), "3.3" (3.1), "section 6" (3.4, 4.3, 8), E8 and E10 (4.4), "claim E2 in 4.1", "the 4.2 means", "measurement 1/2" (6.7, 7), "3.2" (7), "3.1 item 1" (8), H1..H4 (defined in 1), INV-A..INV-L (labelled inline in 5).
B: 19 references, 16 resolve. Unresolved: "H1/H2" in 1 (B never defines them; A defines them), "EL2/HL2" in 3.F (never defined), "k" in 2.1, 3.F and 6.7 (never defined). Resolved: "section 3.B", "sections 1 to 3.E", "section 3.F" (0), "section 0" (3.D), "B above" and "S0 lines above" (3.C), "section 2.5" (4), "section 2.3" (5), "section 3.C" (5), "open, section 5" (7), "test 1" (8), "section 3.D" (8), "B's claim (3)" (6.7), "A above" (3.C), F-families (glossed in 1), INV-L/G/H (labelled in 5).

### SC detail

`grep -c '^## '`: A 9 (0 to 8), B 9 (0 to 8). SC = 1.0 for both.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

### Variant A

#### Completeness (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| Covers all explicit requirements | MET | RC 15/15: sections 1-8 plus E1, 4.2, E3, E5, E6, 3.3 cover all 7 evidence facts |
| Edge cases and failure scenarios | MET | 4.3 `k` 0 in 15 of 18 role values and time-cap exception; E9 hang guard; section 5 endangered rows with mitigations |
| Dependencies and prerequisites | MET | Section 2 dependency column (C-01 INV-003, C-02, C-03 INV-006/007); 3.1 item 2 re-ask needs served-model check CL-C09 |
| Success/completion criteria | MET | 6.1 "wrong if an exchange arm beats A2 ... right if none does"; 6.4-6.6 pass/fail tests |
| Out of scope | MET | 3.2 "What the core does not build now" (hook library, board, seal, registry, `--settings`, alarms) |
| **Subtotal** | **5/5** | |

#### Correctness (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| No factual errors | NOT MET | 4.4 "`--resume` on gateway ids is not evidenced" is stale at the pinned tip (X-002, B won 82%); 8 "tens to about 150 ms" overstated (X-004); 4.2 "no matching control row" overstated |
| Feasible with stated constraints | NOT MET | 3.3 H1 reaches reflect "no call-site change" while `ensemble.py:601-630` builds the brief (INV-005 HIGH); 3.1 item 2 re-ask cannot live inside a pure `parse_block` (INV-009 HIGH) |
| Terminology consistent and accurate | MET | 1 disambiguates "Unconditional" ("not gated on an exchange decision", kit per profile); tags and legend in 0 used uniformly |
| No internal contradictions | NOT MET | IC found 3 (4.2 vs 4.3; 3.3 vs 2/5; 6.4 vs 3.1 item 1) |
| Claims supported by evidence | MET | 4.1 table E1-E12 with tag and source per row; 4.2 recomputed ratios shown |
| **Subtotal** | **2/5** | |

#### Structure (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| Logical ordering | MET | 0 legend, 1 position, 2 consistency, 3 design, 4 evidence, 5 invariants, 6 test, 7 effect, 8 objection |
| Consistent hierarchy depth | MET | H3 only under 3 and 4 (3.1-3.4, 4.1-4.4); other sections flat; no orphans |
| Separation of concerns | MET | Evidence in 4, invariants in 5, tests in 6, effects in 7; 0 holds tag legend |
| Navigation aids | MET | Cross-references "see 3.4", "3.1 item 2", E1-E12 row labels, "measurement 1/2" |
| Artifact-type conventions | MET | All 8 brief elements present plus Status header and footer |
| **Subtotal** | **5/5** | |

#### Clarity (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| Unambiguous language | MET | Hedge words only in quotes of MR or evidence caveats ("may beat" is quoted from `MR:917`); decisions stated as rules (3.4, 6.2) |
| Concrete, not abstract | MET | Named keys `kit: on|off`, `exchange: off`; file:line cites; thresholds n >= 4, hold-out >= 4 |
| Section purpose statement | MET | Each H2 states its purpose in its first sentence; 1 is a one-paragraph summary |
| Terms defined on first use | MET | H1-H4 defined in 1, el2/sl2 in 4.2, `k` in 4.3, F1 in 4.4. Minor gap: "A1" never defined |
| Actionable next steps | MET | 6.1-6.7 measurements; 7 "What would change this"; 3.4 "subject to cost measurement" |
| **Subtotal** | **5/5** | |

#### Risk Coverage (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| At least 3 risks with likelihood and impact | MET | 5 endangered rows (INV-G HIGH, INV-L/A, INV-K, cost +59% pinned and +10 to +35%) with measured magnitudes in E6, E8, E9, 4.2 |
| Mitigation for each risk | MET | 5: lint test for read-only lanes, `kit: off` for reflect, `verify-sync` coverage; cost risk gated in 3.4 and 6.2 |
| Failure modes and recovery | MET | 8 answer (5): if the kit fails only the catalogue is lost; `exchange` other values refused; retrofit path in 3.2 |
| External dependencies and failures | MET | Section 2 residue (C-01 INV-003, C-03 INV-006/007), 4.4 runtime facts (subagent delivery, `--resume`, hook cost) |
| Monitoring/validation mechanism | MET | 6.4 off-state equality, 6.5 brief lint, 6.2 per-module cost record, catalogue hash in the run record |
| **Subtotal** | **5/5** | |

#### Invariant & Edge Case Coverage (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| Collection boundaries | MET | 3.1 item 2 anchor over 200 and claim over 300 (88 of 92 dropped lines); n = 2 vs 4 rows; `k` 0 cells |
| State across boundaries | MET | 2 and 3.2: `origin` means three things (E2, ledger, diffgate), so another key name; sidecar vs in-line tag |
| Guard condition gaps | MET | 3.1 item 6 any other `exchange` value refused at validation; 5/6.5 lint on no-Bash lanes; E4 `agent_id` skip gap in r2 |
| Count divergence | MET | 4.3 last bullet: static `def test_` counts 103, 163, 89, 90, 82 vs self-reported 138, 358, 89, 106, 108 |
| Interaction effects | MET | 2: peer finding is not an independent vote; hang-killed receiver trips C-03 quorum; 3.4 kit vs pinned reflect bytes; X-13 class-card single source |
| **Subtotal** | **5/5** | |

### Variant B

#### Completeness (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| Covers all explicit requirements | NOT MET | RC 14/15: act-rate range (item 11) absent; no act-rate figures anywhere in sections 3 or 6 |
| Edge cases and failure scenarios | MET | 6.4 fault injection (corrupt board line, missing transcript, lock timeout); 3.F `k` 0 and late-delivery cases; 5 untrusted anchor |
| Dependencies and prerequisites | MET | 2.3 depends on C-07; 4 depends on C-08 for act rates; 8 concession "if C-07 yields no launcher" |
| Success/completion criteria | MET | 6.1 "B is wrong if this cannot hold"; 6.7 "fewer than half of the cells" decision rule; 6.2 pins unmodified |
| Out of scope | MET | 1 "B's boundary: harness-authored kinds only ... F4 and F7 are not in the core"; 2.5-2.7 no change to contract, reflect, loop |
| **Subtotal** | **4/5** | |

#### Correctness (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| No factual errors | NOT MET | 2.2 "registered ... in `hooks.json`" is wrong (X-006: a `hooks.json` entry fires in every session); 1 (4) "cost is zero by construction" is falsified by the installed script and sync list (A-002) |
| Feasible with stated constraints | NOT MET | 2.2 global registration conflicts with the stated inert off state and baked per-session args; `--settings` appears nowhere in `src/superclaude/**/*.py`; the shared H1/H2 carry the same INV-005/009 issues |
| Terminology consistent and accurate | NOT MET | "registered" in 2.2 vs "baked into `--settings`" in 2.2/2.4; "H1/H2" used in 1 without any definition in B |
| No internal contradictions | NOT MET | IC found 2 (2.2 vs 2.4; 1 (4) vs 2.2) |
| Claims supported by evidence | MET | 3.A-3.F cite file:line with tags; 3.B recorded S0/S2 lines with hook_ms_p95 values |
| **Subtotal** | **1/5** | |

#### Structure (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| Logical ordering | MET | 1 position, 2 design, 3 evidence, 4 consistency, 5 invariants, 6 test, 7 effect, 8 objection (the brief's own order) |
| Consistent hierarchy depth | MET | H3 A-F only under 3; other sections are flat lists; no orphans |
| Separation of concerns | MET | 3.F isolates [POST-BASELINE] updates from decisive 3.A-3.E; 5 splits preserved and endangered |
| Navigation aids | MET | "(section 3.D)", "(section 2.3)", "(test 1)", lettered sub-sections A-F |
| Artifact-type conventions | MET | All 8 brief elements present plus Status header and footer |
| **Subtotal** | **5/5** | |

#### Clarity (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| Unambiguous language | MET | Rules stated as decisions; hedges limited to labelled [UNVERIFIED] caveats |
| Concrete, not abstract | MET | Named files and lines (`hook-posttool.sh:14-15`), 600-byte cap, forbidden-key list, 0.1 s budget |
| Section purpose statement | MET | Each H2 opens with its purpose; 1 gives a four-claim summary |
| Terms defined on first use | NOT MET | "H1/H2" (1), "EL2/HL2" (3.F), "k" (2.1, 3.F, 6.7), "S0/S2" (3.B) never defined; A1/A2 defined only in 6.7 |
| Actionable next steps | MET | 6.1-6.8 tests and measurements; 8 concession states the shrink path |
| **Subtotal** | **4/5** | |

#### Risk Coverage (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| At least 3 risks with likelihood and impact | MET | 5 endangered rows (blindness relaxation, Bash launcher, untrusted anchors, INV-H, time budget 60 to 100 ms per call); 3.F `k` 0 and delivered 0 as likelihood; 6.7 "fewer than half the cells" |
| Mitigation for each risk | NOT MET | 5 Bash-launcher risk is passed to C-07 with no mitigation; 5 untrusted text "B does not claim it is closed"; delivery to a read-only reviewer left [UNVERIFIED] |
| Failure modes and recovery | MET | 6.4 fault injection; seal fails closed while review fails open; 8 concession fallback to validator, sidecar and F1 prompt |
| External dependencies and failures | MET | C-07 launcher, C-08 served model, `--no-session-persistence` pins, gateway-id evidence 3.B |
| Monitoring/validation mechanism | MET | 6.5 hook p95 over 30 calls in `hook_latency_drift.yaml`; 6.8 echo and independence alarms; `collab` record counts |
| **Subtotal** | **4/5** | |

#### Invariant & Edge Case Coverage (5)

| Criterion | Verdict | Evidence |
|---|---|---|
| Collection boundaries | MET | 2.1 600-byte cap; 5 anchor 12 to 200 characters; 6.6 two parallel calls |
| State across boundaries | MET | 2.5 in-line `origin` accepted by both parsers then dropped before the ledger, so a sidecar keyed by reviewer id and finding id |
| Guard condition gaps | MET | 3.A r2 hook has no `agent_id` branch (`grep -c` 0); 2.1 forbidden verdict keys; 6.6 replay with an `agent_id` call |
| Count divergence | MET | 5 "36 `def test_` functions and no parametrize" (count verified against the C-03 figure); 3.A `flock -w 4` vs untimed `flock 9`; 0 vs later `/lib/` counts |
| Interaction effects | MET | 4 exchange vs C-02 quorum (counts over own-origin lines only); 2.3 persistence vs `--no-session-persistence` pins; INV-H vs board anchors |
| **Subtotal** | **5/5** | |

## Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 4/5 |
| Correctness | 2/5 | 1/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 4/5 |
| Risk Coverage | 5/5 | 4/5 |
| Invariant & Edge Case | 5/5 | 5/5 |
| **qual_score** | **27/30 = 0.9000** | **23/30 = 0.7667** |

Edge Case Floor: A 5/5 (eligible), B 5/5 (eligible).

Observations. Both papers are weakest on Correctness, for different reasons: A's defects are two stale or overstated facts (`--resume`, hook latency) plus the shared-core feasibility gaps the probe found (INV-005, INV-009); B's defects are the `hooks.json` wording, the "zero cost by construction" claim and undefined terms. A wins Completeness (all 15 source items, including the act-rate range), Clarity and Risk on specific citations; B's unique strengths (validator and untrusted-anchor analysis, fault injection) do not change a binary verdict but are the content a merge should keep.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A | 0.4856 | 0.4500 | **0.9356** | not needed (A 12 points) |
| B | 0.4725 | 0.3833 | **0.8559** | not needed (B 5 points) |

**Margin**: 7.97% (above the 5% threshold). **Tiebreaker applied**: No. For the record: level 1 (debate tally A 12, B 5, Merge 2, Tie 2, Unresolved 1) and level 2 (correctness count A 2 vs B 1) would both favour A.

Pass-1 leader: Variant A (input-order pass). Position-bias reconciliation against pass 2 is left to the lead.

RESULT_PASS1: quant_A=0.9712 quant_B=0.9450 qual_A=27/30 qual_B=23/30 combined_A=0.9356 combined_B=0.8559 floor_A=5/5 floor_B=5/5
A: MMMMMNNMNMMMMMMMMMMMMMMMMMMMMM
B: NMMMMNNNNMMMMMMMMMNMMNMMMMMMMM
