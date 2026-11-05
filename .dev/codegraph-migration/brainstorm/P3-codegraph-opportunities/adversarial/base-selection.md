# Base Selection Report: P3 codegraph opportunities

## Metadata
- Generated: 2026-10-29T17:27:48Z
- Variants: A = `variant-1-opus-architect.md` (opus:architect), B = `variant-2-sonnet-analyzer.md` (sonnet:analyzer), C = `variant-3-haiku-backend.md` (haiku:backend)
- Source requirements: `../seed-brief.md` Success Criteria and Constraints. It has no FR IDs, so requirement coverage uses section-level topic matching.
- Ground truth for correctness checks: `../../../research/codegraph-evaluation.md` (EVAL), plus the EVAL fact checks in `diff-analysis.md` (X-015, X-017 to X-021)
- Debate status carried in: BLOCKED_BY_INVARIANTS (INV-001). At depth standard there is no Round 3, so the base is **force-selected by score**, and INV-001 is carried into the merge as an accepted risk with a blocking experiment (see `refactor-plan.md`).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (opus:architect) | Variant B (sonnet:analyzer) | Variant C (haiku:backend) |
|---|---|---|---|---|
| requirement_coverage (RC) | 0.30 | 1.000 (21/21 topics) | 0.952 (20/21; no scope statement) | 1.000 (21/21) |
| internal_consistency (IC) | 0.25 | 0.957 (3 contradictions / 70 claims) | 1.000 (0 / 63) | 0.967 (2 / 60) |
| specificity_ratio (SR) | 0.15 | 0.905 (152/168 lines) | 0.929 (130/140) | 0.857 (126/147) |
| dependency_completeness (DC) | 0.15 | 1.000 (180/180) | 0.994 (165/166) | 1.000 (134/134) |
| section_coverage (SC) | 0.15 | 1.000 (9/9 H2) | 1.000 (9/9) | 1.000 (9/9) |
| **quant_score** | | **0.975** | **0.974** | **0.970** |

### Computation notes

**RC: topic matching.** The 21 topics come from the seed brief. Success Criteria are split into 6 topics: SC-1 per-idea target/value/effort/risk; SC-2 single ranked list; SC-3 explicit drops with reasons; SC-4 3-5 candidates with callers; SC-5 EVAL traceability (claims sourced or marked UNVERIFIED); SC-6 blockers called out (listing env, per-worktree `init`, freshness). Constraints add 6 more: K-1 planning-only scope (guidance, allowlists, contracts and new primitives, not CLI code or the installer); K-2 installed-path and dual-surface rule; K-3 fail-open with a named fallback and a degraded value; K-4 re-Read before cite; K-5 read-only agents need listed `mcp__codegraph__*` names; K-6 no `prompt-hook` and no SQLite reliance. The last 9 topics are the vectors V-1 to V-9 (token cost; citation accuracy; impact before edits; review scoping covering auggie-review, pr-submit and reflect; test selection via `affected`; troubleshoot Tier 1; planning covering workflow, implement and tasklist; reflection/audit covering reflect, cleanup-audit and reuse-auditor; onboarding covering index-repo, explain and load). A topic counts as matched when the variant addresses it by keyword or section. An explicit drop of a vector's primitive counts as coverage.

| Topic | A | B | C |
|---|---|---|---|
| SC-1..SC-4 | §3 table columns, §4, §5 D-01..D-12, §6 C-1..C-4 | §3 columns Eff/Risk/Value, §4, §5, §6 N-1..N-3 | §3 columns, §4, §5 bullets, §6 C-1..C-4 |
| SC-5 | line 13 "Every codegraph capability below is taken from EVAL; anything else is marked UNVERIFIED" | Notation: "UNVERIFIED means EVAL did not measure it" | line 4 "no capability is claimed outside it" |
| SC-6 | §2.2 B1, B2, B3 | §2.2 B1, B2, B3 | §2 prerequisites 1-3 |
| K-1 | line 13 "Not in scope: the installer phase, IronClaude Python CLI code, and the 1:1 Serena SYM/REF swaps" | **not matched**: no scope statement (searched Notation, §1, §2) | line 4 "Planning only" |
| K-2 | FR-01, §6 header | FR-20, §6 header | NFR-03, §6 footer |
| K-3 | FR-03 | FR-02 | FR-01, NFR-01 |
| K-4 | FR-04, INV-2 | FR-06 | FR-03 |
| K-5 | §2.1 Class D | §2.1 row 3, FR-11 | §2 row 2 |
| K-6 | D-02, D-05 | D-04, D-12 | §5 bullets 5 and 8 |
| V-1..V-9 | all 9 via the §3 Vector column (tasklist via D-03) | all 9 via the §4 coverage check | all 9 via the §1 coverage table |

**IC: contradictions per scorable claim.** Scorable claims are ideas, drops, FRs, NFRs, invariants and risk or edge-case bullets. That gives A 19+12+16+8+4+11 = 70, B 10+12+21+9+11 = 63, and C 13+12+10+7+10+8 = 60. Contradictions found:
- A (3): (1) the stale-index edge case "try one `sync`" against NFR-07 "Apart from C-4 `init`/`sync`, codegraph use writes nothing". (2) I-12 "zero graph callers is extra evidence for DELETE" against the empty-results edge case "never infer 'unused' from it" (A conceded this, R1 Conc 5). (3) NFR-08 "Removing the codegraph registration … makes every consumer degrade" against §2.1, where Class B and C default to the CLI, which does not need the registration (A conceded this, R2 NE2).
- B (0): FR-01 "once per run" and §8 "re-run `status` immediately before the queries … not once per session" are about different subjects (a run-level probe versus a per-batch re-check). The diff-analysis flags no B self-contradiction. This was confirmed in position-bias re-evaluation item 2 below.
- C (2): the X-002 self-contradiction counted as two opposing pairs. §1 says "no allowlist change", §2 says "adding `Bash(codegraph *)` patterns", and FR-10 says "no bare `Bash(codegraph *)`".

**SR.** Every non-heading, non-blank, non-separator, non-front-matter line counts as a substantive statement. A line is concrete when it contains a number, a backticked identifier or an `§` citation. Counted mechanically with awk. A secondary count of hedge words ("should", "might", "could", "likely", "roughly", "best-effort", "opportunistic", "nicety", "appropriate") found A 3, B 1 and C 3 lines. No variant uses the protocol's own vague list ("as needed", "properly", "adequate", "best practices").

**DC.** Internal ID references were counted with grep: `I-NN`, `D-NN`, `C-N`/`N-N`, `FR-NN`, `NFR-NN`, `B<n>`, `Q-n` and `INV-n`. External references were excluded: `INV §n`, EVAL §, implement `Q1`-`Q6` steps, and the external task id "W4 step 6". B has one unresolved reference: "Spike instead (OQ-5)" in D-08, because B's §9 numbers its questions `1.`-`8.` and defines no `OQ-` IDs. All other references resolve.

**SC.** Each variant has 9 H2 sections, and the maximum is 9.

## Qualitative Scoring (50% weight): Additive Binary Rubric

Each cell is a compressed Claim-Evidence-Verdict record. The claim is "criterion N is met / not met in Variant X". The evidence is a quote or section reference. The verdict is MET (1) or NOT MET (0). When no evidence could be cited, the verdict defaults to NOT MET. The verdicts below are final, after the position-bias re-evaluation.

### Completeness

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1 Covers all explicit requirements | MET | All 21 RC topics. 4 candidates with callers (§6) | MET | All 9 vectors in the §4 coverage check. 3 candidates with callers | MET | §1 nine-vector table. 4 candidates with a "Called by" column |
| 2 Edge cases and failures | MET | §8 edge cases: stale, uninitialized, nested, empty, ambiguous, hub, Markdown repos | MET | §8: stale, nested, empty, ambiguous, caller-count semantics, format drift | MET | §8 edge-case table, 8 rows |
| 3 Dependencies and prerequisites | MET | §2.2 B1-B7 with owners | MET | §2.2 B1-B8 with owner and stance | MET | §2 "Prerequisites and owners" 1-5 |
| 4 Success and completion criteria | MET | FR-01..16, each with a "Test:" | MET | FR-01 "Test: …"; NFR-08 numeric backtest thresholds | MET | FR-01..10, each with a "Test:" |
| 5 Explicit out-of-scope items | MET | line 13 "Not in scope: …" plus D-01..D-12 | MET | D-01..D-12 exclusion table; D-12 "Memory/NUDGE/ACT jobs (INV §4) are not graph jobs" | MET | line 4 scope plus 12 §5 drop bullets |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Correctness

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1 No factual errors | NOT MET | I-17 and NFR-02: "`codegraph status` (~300 ms, EVAL §5.5)", but §5.5 timed only `query`/`callers` (X-017). The empty-results list is sourced to EVAL §4 beyond its support (R1-A Conc 7) | NOT MET | §1 "23 callers reported … the rest were test functions": EVAL shows 20 of 23 (X-021). D-05 "Grep sees every static reference the graph sees" is not in EVAL (X-020). I-04 "a broken caller can never surface today" (corrected in R2-B #7) | NOT MET | §2 `mcp__codegraph__search` names would not match `codegraph_*` (X-018). I-02 CLI `symbolsOnly` (X-019). I-02 "≤2k-token Tier-1 budget (Wave 1.5 :256)" cites the wrong wave (X-015) |
| 2 Feasible under the constraints | NOT MET | I-06/FR-07 put `changed-area ∪ affected` straight into VG-1, though EVAL never ran `affected`, and any non-zero gate blocks the push (`sc-pr-submit-protocol/SKILL.md:203-206`, R2-A B-6) | MET | CLI-first artifacts work without B1 (§2.1). Per-subcommand patterns fit the enumerated allowlists. Gate changes are staged (FR-12, FR-13) | NOT MET | FR-05 "`tests` is exactly the parsed `affected --json` list" can narrow VG-1. I-02 rests on MCP-only node file mode through the CLI |
| 3 Consistent terminology | MET | One state field `index_state` and one closed `graph:{…}` vocabulary used everywhere (FR-03, C-1 output) | NOT MET | N-1 output `codegraph_state` and `degraded: codegraph:<state>`, but N-2 `graph_state`, FR-14 `graph:<state>`, FR-18 `graph_state` | NOT MET | `graph: available/unavailable` plus free-form keys: `test-scope:codegraph_stale`, `grounding:codegraph_uninitialized`, `neighbour-search:codegraph_unlisted`, `dropped: ambiguous` |
| 4 No internal contradictions | NOT MET | IC: 3 (sync vs NFR-07; I-12 vs empty-results rule; NFR-08 vs CLI default) | MET | IC: 0 (see re-evaluation 2) | NOT MET | IC: 2 (X-002) |
| 5 Load-bearing claims supported | MET | Top-5 ranked items cite EVAL §3/§5.5 and primitive lines (`:286`, `:218`, `:206-207`) | MET | Every rank carries an M/P/A class and an EVAL cite; unmeasured benefits are labelled UNVERIFIED | NOT MET | #2-ranked I-09 and §1: `affected` is "the clearest net win … deterministic, replayable", but EVAL never ran `affected` (A-008; R1-C Conc 3) |
| **Subtotal** | **2/5** | | **3/5** | | **0/5** | |

### Structure

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1 Logical ordering | MET | Summary → access → ideas → ranking → drops → candidates → requirements → risks → questions (S-002) | MET | Same nine | MET | Same nine |
| 2 Consistent hierarchy | MET | §2.1/§2.2 H3; no orphans | MET | §2.1/§2.2, §6 N-1..N-3 H3 | MET | Flat H2 with tables; no orphaned H3 |
| 3 Separation of concerns | MET | Blockers (§2.2) separate from ideas (§3) and requirements (§7) | MET | Same | MET | Contract block (§2) separate from ideas and requirements |
| 4 Navigation aids | MET | ID cross-references (I-, D-, C-, FR-) throughout | MET | ID cross-references; §4 coverage check | MET | ID cross-references; §1 coverage map |
| 5 Follows artifact conventions | MET | YAML front matter; ID'd drops, FRs and NFRs with tests | MET | YAML front matter; ID'd drops, FRs and NFRs | NOT MET | No front matter (S-001); drops are unnumbered bullets that cannot be cross-referenced (S-008, all three advocates) |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Clarity

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1 Unambiguous language | MET | Hedge words appear only inside §9 questions | MET | 1 hedge line; values stated with classes | NOT MET | "Neutral-to-positive", "Modest" (§1 table), "additions are opportunistic", "user-facing nicety" (§4 #10) |
| 2 Concrete | MET | SR 0.905 | MET | SR 0.929 | MET | SR 0.857 |
| 3 Section purpose clear | MET | Each section opens with a method or scale line | MET | Notation; "Method." lines | MET | Persona/scope line; "Method:" line |
| 4 Terms defined on first use | NOT MET | "INV §4", "SYM/REF" used at line 13 without defining INV | MET | Notation defines EVAL, INV and the M/P/A classes | NOT MET | "INV §1/§4", "6 LB SYM rows", "MEM/ACT jobs" used undefined |
| 5 Actionable next steps | MET | Layer 0 order; Q-1..Q-8 with owners (Q-5) | MET | §4 sequencing; §9 questions with default answers and owners | MET | §4 sequencing note; §9 owner questions |
| **Subtotal** | **4/5** | | **5/5** | | **3/5** | |

### Risk Coverage

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1 ≥3 risks with probability and impact | MET | Risk L/M with reason per idea; §2.2 "Effect if unfixed" | MET | Risk L/M/H per idea plus evidence class (confidence) | NOT MET | Risk column is prose with no level, except I-01 "Low" |
| 2 Mitigation per risk | MET | §8 edge cases each name a response | MET | §8 bullets each name an FR | MET | §8 table "Contract response" |
| 3 Failure modes and recovery | MET | INV-1 fail-open; rollback bullet | MET | FR-02; NFR-07; rollback bullet | MET | NFR-01; NFR-05 rollback |
| 4 External dependencies | MET | Single-maintainer upstream; telemetry B5; installer B1 | MET | B1 installer; B8 version pin; upstream drift | MET | Prerequisites 1-5 with owners |
| 5 Monitoring and validation | MET | NFR-03 containment count; `graph:version_mismatch` | MET | NFR-04 golden fixtures; NFR-08 backtest; NFR-07 per-primitive tests | MET | NFR-06 observability; FR-06 mutation grep |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Invariant & Edge Case Coverage

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| 1 Collection boundaries | MET | Empty results (`graph:empty`); hub symbols `truncated`; `limit ≤ 20` | MET | FR-07 empty ≠ absence; FR-08 shown/total; FR-10 40 rows / 6 KB | MET | Empty ≠ zero refs; "Showing 20 of 23" row; docs-only `tests: []` |
| 2 State across components | MET | `index_state` shared by the probe and all consumers; INV-3 freshness gate | MET | FR-03 `index_root == worktree_root`; FR-05 stale → leads | MET | Stale count skews reflect severity (§8) |
| 3 Guard gaps | MET | `graph:ambiguous`; `version_mismatch` | MET | NFR-04 `parse_failed`; `ambiguous[]` | MET | `dropped: ambiguous`; `unverified` drop |
| 4 Count divergence | MET | FR-08 `caller_functions` vs call sites; "Showing 20 of 23" | MET | "Caller-count semantics" bullet: per caller symbol vs per call site | MET | I-05 risk: callers vs call sites; `total_count` |
| 5 Feature interaction effects | MET | B7: node file mode × freshness hook; telemetry × CLI path | MET | Allowlist × `install`; BASH policy interplay; QA scope creep | MET | §5: node file mode × freshness matcher; CLI vs MCP latency row |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | A | B | C |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 2/5 | 3/5 | 0/5 |
| Structure | 5/5 | 5/5 | 4/5 |
| Clarity | 4/5 | 5/5 | 3/5 |
| Risk Coverage | 5/5 | 5/5 | 4/5 |
| Invariant & Edge Case | 5/5 | 5/5 | 5/5 |
| **qual_score** | **26/30 = 0.867** | **28/30 = 0.933** | **21/30 = 0.700** |

## Edge-Case Floor Check

| Variant | Invariant & Edge Case score | Floor (≥1/5) | Eligible as base |
|---|---|---|---|
| A | 5/5 | pass | yes |
| B | 5/5 | pass | yes |
| C | 5/5 | pass | yes |

## Position-Bias Mitigation

Pass 1 evaluated the variants in input order (A, B, C). Pass 2 evaluated them in reverse order (C, B, A). Only the disagreements are listed. Each one was re-evaluated with both passes' evidence side by side, and the re-evaluation verdict is final.

| # | Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Resolution |
|---|---|---|---|---|---|---|---|
| 1 | Completeness-5 | B | NOT MET | MET | DISAGREE | MET | Pass 1 looked for a scope sentence. The criterion asks for out-of-scope *items*, and D-01..D-12 is an explicit exclusion list. The missing scope sentence is already charged once, in RC (K-1) |
| 2 | Correctness-4 | B | MET | NOT MET | DISAGREE | MET | Pass 2 counted the FR-01 / §8 tension (A-006). The two statements are about different subjects (run probe vs per-batch re-check). B's own R2 #3 says "not literally contradictory", and the diff-analysis lists no B self-contradiction. IC for B is set to 0 contradictions to match |
| 3 | Correctness-5 | C | MET | NOT MET | DISAGREE | NOT MET | Pass 1 counted C's 18 EVAL references. Pass 2 applied the load-bearing standard: C's #2 ranked claim about `affected` has no EVAL support, and C conceded it (R1-C Conc 3) |
| 4 | Correctness-5 | A | NOT MET | MET | DISAGREE | MET | Pass 1 charged A Conc 7 (empty-results sourcing) and the withdrawn "safe by construction". Under the same load-bearing standard used for C, A's top-5 ranked claims cite EVAL and primitive lines. The sourcing error is already charged under Correctness-1 |
| 5 | Structure-5 | C | MET | NOT MET | DISAGREE | NOT MET | Pass 2 compared C against A and B: unnumbered drops and no front matter break the convention all three advocates endorsed (S-008 A+B unanimous) |
| 6 | Risk-1 | C | MET | NOT MET | DISAGREE | NOT MET | Pass 1 accepted prose risks. Pass 2 required a level, and only I-01 has one |
| 7 | Clarity-4 | A | MET | NOT MET | DISAGREE | NOT MET | Pass 2 read A line 13 after B's Notation block, which defines INV. A uses "INV §4" undefined |

- Disagreements re-evaluated: 7
- Final verdicts that differ from Pass 1: 6 (#1, #3, #4, #5, #6, #7). Final verdicts that differ from Pass 2: 1 (#2)

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker (scoring-matrix points won) |
|---|---|---|---|---|
| A (opus:architect) | 0.488 | 0.433 | **0.921** | 35 of 59 = 59.3% |
| B (sonnet:analyzer) | 0.487 | 0.467 | **0.954** | 48 of 59 = 81.4% |
| C (haiku:backend) | 0.485 | 0.350 | **0.835** | 10 of 59 = 16.9% |

- **Margin**: B − A = 0.033 (3.3%), **below** the 5% threshold
- **Tiebreaker applied**: Yes. Level 1 is debate performance, meaning points won in the `debate-transcript.md` Scoring Matrix, with combination winners credited to each member. B 81.4% vs A 59.3% is a 22.1-point gap, more than 5%, so B is selected at level 1. Levels 2 (correctness count: B 3 vs A 2) and 3 (input order) were not needed. Both would also have picked B.
- Points with no variant winner (S-002, S-011, X-020 "none"; C-029, C-031, X-021 split; the 5 shared A-points) are excluded from the tiebreaker denominator.

## Selected Base: Variant B (sonnet:analyzer)

### Selection Rationale

B has the highest combined score (0.954). It also wins the tiebreaker clearly. It is part of the winning approach on 48 of 59 decided debate points, and on almost every L3 gate-safety point: C-004, C-007, C-013, C-017, C-018, C-030, X-002, X-008 and X-013. Its quantitative lead over A is negligible (0.974 vs 0.975). Its qualitative lead comes from Correctness (3 vs 2) and Clarity (5 vs 4). The specific Correctness advantage is that B's access model and gate staging are feasible today without the B1 listing env and without changing a push gate on the unrun `affected` command. A conceded both points (R1-A Conc 1-2; R2-A B-6). B's weaknesses are fact-level overstatements: X-021, X-020 and "can never surface today". B conceded all three in Round 2, and the merge can fix them with local edits. A's architectural surplus (capability map, `/sc:graph`, telemetry, language scope) is additive and can be grafted onto B. C's surplus (contract sequence text, asymmetric cleanup rule, edge-case table) is additive too.

The selection is forced by score despite BLOCKED_BY_INVARIANTS. INV-001 sits under B's FR-01/FR-05 freshness design, and the consensus adopted that design. Choosing A or C would not remove INV-001, because all three variants rely on `codegraph status` for freshness. The merge must therefore carry INV-001 as a blocking prerequisite experiment.

### Strengths to Preserve from Base (B)

1. M/P/A evidence classes and the `V × C ÷ E` score (S-005, S-007, C-024).
2. CLI-first access with orchestrator-computed artifacts passed to agents by path, and no `mcp__codegraph__*` in agent `tools:` in v1 (C-002, X-001, X-003).
3. Per-subcommand allowlists, never `Bash(codegraph *)` (C-004, X-002; FR-04).
4. The parity hazard and prod-only distinct-caller counting through the runtime-surface table (U-009; C-017, X-013; FR-09).
5. The span-bounded call-site resolver (`resolve-callsite.sh`, I-02) as the executable core of the citation contract (C-009).
6. Staged `affected`: advisory delta, then backtest, then union, never removing tests (U-010; C-013, X-008; FR-13, NFR-08).
7. The provenance check `index_root == realpath(toplevel)`, golden fixtures and the `parse_failed` degrade (U-012, U-013; C-006).
8. The asymmetric-evidence rule FR-07, artifact caps (FR-10: 40 rows, 6 KB) and the 2K-token context cap (NFR-06).
9. No new reflect contract field, only `degraded_components` entries (C-018).
10. evidence-validator unchanged (C-010, X-004), no new hooks (C-022, X-007) and the routing block (I-03).

### Strengths to Incorporate from Non-Base Variants

1. From A §6 C-1 and FR-03: the capability map (capability → CLI form → MCP tool `mcp__codegraph__codegraph_*` → fallback → tested version) and the closed `graph:*` vocabulary (C-005 A+B+C, C-006 A+B, X-018 A).
2. From A I-02 and FR-04: typed row `resolution: def-line|call-site-verified|unresolved`, plus A's R2 NE6 binding `(file, startLine == def_line)` (C-009).
3. From A §6 C-4: the `/sc:graph` user-typed lifecycle owner with the nested-worktree refusal, minus `sync` (C-023, X-005; INV-022).
4. From A §2.2 B5 and §1: the telemetry blocker and the language-scope limit (U-002, U-003; C-032).
5. From A §4: the Layer 0 prerequisite layer (S-007, C-024).
6. From A I-05 and I-10: pre-edit impact as a warning and Q3 input, and pre-fix impact in remediation chains (C-011, U-006).
7. From A I-13, I-14, I-16: an informational workflow step, explain one-hop and a load status line (X-011, C-021, X-016).
8. From A FR-05, NFR-03, NFR-04, FR-16: the explore grep ban, the containment count, mirror parity and the release-level switch (C-008, X-014, C-031, C-033).
9. From A §6 C-2 and C-3: `/sc:impact` modes and caps, and the `selected ⊇ heuristic` invariant (C-028, C-013).
10. From C §2: the PROBE→CALL→VERIFY→DEGRADE text as the seam skill body (C-005), and the drop-never-repair rule (C-009).
11. From C I-07: the asymmetric cleanup-audit rule (C-019, X-012).
12. From C §1 and §8: the nine-vector coverage table and the edge-case table (S-003, S-010).
13. From C FR-06 and R2-C NE1/NE4/NE5: the mutation-exclusion grep extended to script bodies, the pytest exit-5 collect-only pre-pass, and the zero baseline for containment (C-031, C-013).
14. From C §8 and C-3: the docs-only-diff rule and the `source:` provenance field for test scope (U-022; C-013).
15. From C §5: the `sync` drop, private per-skill scripts, `sc-recommend` routes, cleanup-audit test runs and the `/sc:load` rewrite drop (C-026).
