# Base Selection Report

Two independent passes scored the three variants in opposite order (pass 1: Variant 1, 2, 3 with a sonnet judge; pass 2: Variant 3, 2, 1 with an opus judge). Pass files: `scoring-pass-1.md`, `scoring-pass-2.md`. Variant 1 = opus:architect, Variant 2 = sonnet:refactorer, Variant 3 = haiku:qa. Source requirements: AC-1..AC-8 of issue #394 and SC-1..SC-5 of the seed brief (13 items).

## Quantitative Scoring (50% weight)

Each metric is the mean of the two passes, except RC for Variant 2, which is set to 1.000 (pass 2 gave 0.923 because its speed budget is not numeric; the requirement is addressed by a measured speed test, see C1 below).

| Metric | Weight | Variant 1 (opus:architect) | Variant 2 (sonnet:refactorer) | Variant 3 (haiku:qa) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 1.000 (13/13 in both passes) | 1.000 (13/13 pass 1; 12/13 pass 2, overridden) | 1.000 (13/13 in both passes) |
| internal_consistency | 0.25 | 0.9815 (0.982, 0.981) | 0.9835 (0.980, 0.987) | 0.9410 (0.946, 0.936) |
| specificity_ratio | 0.15 | 0.9745 (0.967, 0.982) | 0.9665 (0.966, 0.967) | 0.9865 (0.981, 0.992) |
| dependency_completeness | 0.15 | 0.9850 (0.990, 0.980) | 0.9895 (1.000, 0.979) | 0.9355 (0.964, 0.907) |
| section_coverage | 0.15 | 1.000 (16/16) | 1.000 (16/16) | 1.000 (16/16) |
| **quant_score** | | **0.9893** | **0.9893** | **0.9736** |

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Verdicts are final (agreed by both passes, or resolved below). Evidence is the pass-1 judge's note, or the resolution text where the passes disagreed.

### Completeness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence | Variant 3 | Evidence |
|---|---|---|---|---|---|---|
| C1 Covers all explicit requirements | MET | section 13 maps AC-1 to AC-8 to sections and test groups  | MET | Final: speed is evaluated by a measured test (median of 20 runs); the number is vague but the r | MET | section 13 maps AC-1 to AC-8 to T-* test ids  |
| C2 Addresses edge cases and failures | MET | section 10 failure table, degraded binding for missing or stale record  | MET | section 10 table covers jq missing, bad JSON, unreadable state, timeout  | MET | section 10 table, T-FO fail-open cases, T-SUB-4 no match  |
| C3 Includes dependencies and prerequisites | MET | section 3 files, claim interface R1/R2/R3, section 14 step 7 handoff  | MET | C1 to C3 claim interface, claim script refuses launch without jq  | MET | section 3 interface R1 to R4 owed by claim feature, install list  |
| C4 Defines success and completion criteria | MET | section 14 step 8, full and submit stay off real issues until OB-H3  | MET | section 14 step 5, OB-H2 and OB-H3 pass before any real full launch  | MET | section 16 closing line makes OB-H2 mandatory; section 13 AC map  |
| C5 Specifies out-of-scope items | MET | section 2 T3 out of scope; O-1 leaves source edits to #322  | MET | section 1 item 6 Cut list; T3 not designed against  | MET | section 2 Not covered list; section 3 claim interface is requests only  |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence | Variant 3 | Evidence |
|---|---|---|---|---|---|---|
| K1 No factual errors or hallucinated claims | NOT MET | section 3 says Makefile holds `_FRESHNESS_SCRIPTS`; it lives only in install_hooks.py  | MET | `_FRESHNESS_SCRIPTS` and `hooks.json` alternation matcher both match the repository  | NOT MET | wrong Makefile claim, unregistered `manual` marker, V4 and V11 misapplied (X-004, X-006)  |
| K2 Technical approach feasible within constraints | MET | bash builtins fast paths, ERR/EXIT traps, one subprocess only for governed pushes  | MET | one jq call, string replacement, git call bounded by 1 s timeout  | NOT MET | always-on cwd fallback and tamper block in every session break the ordinary-session constraint  |
| K3 Terminology consistent and accurate | NOT MET | R1 to R8 residual ids reused as claim interface R1, R2 (section 14)  | NOT MET | T1 names both the honest-agent threat and the tamper message  | MET | W, WA, F, FS and MSG-* ids used consistently; MSG-STATE reuse minor  |
| K4 No internal contradictions | NOT MET | fast path 1 (empty store) exits before degraded binding of a marked prompt  | NOT MET | fast path tests only `sessions/`, so first launch never reaches binding  | NOT MET | X-005 tamper block everywhere, X-007 push HEAD from master allowed  |
| K5 Claims supported by evidence or rationale | MET | every decision has a Why or Rejected line with V-tagged facts  | MET | each position states rationale and rejects options, e.g. section 8 awk cost  | NOT MET | Final: it cites V4 and V8, but the cited facts do not support its fail-open and fallback claims |
| **Subtotal** | **2/5** | | **3/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence | Variant 3 | Evidence |
|---|---|---|---|---|---|---|
| T1 Logical section ordering | MET | 16 sections run position, threats, identity, table, approval, tests, order  | MET | same 16-section order, decisions D1 to D7 in seed order  | MET | same order; section 14 builds a provably harmless skeleton first  |
| T2 Consistent hierarchy | MET | H1 title, 16 H2 sections, bold sub-labels used uniformly  | MET | 16 H2 sections used uniformly, though no H1 title  | MET | H1 plus 16 H2 sections; section 12 uses prose per AC  |
| T3 Clear separation of concerns | MET | ll_classify_shell, ll_decide, ll_message separate classify, policy, wording  | MET | one section per decision; messages and tests in their own sections  | MET | table, approval, Bash, tools, fail-closed, messages in separate sections  |
| T4 Navigation aids (ids, cross-references) | MET | section 13 AC map, LL-* ids, U/OB/O/R ids, decision grid  | MET | section 13 map, message ids W1 to F3, OB-H and N ids  | MET | section 13 map, T-* and MSG-* ids; T-WR-gh-repo dangling  |
| T5 Follows design-spec conventions | MET | summary, threat model, components, interfaces, tests, open decisions  | MET | Final: all 16 required headings and the spec conventions are present; a missing title is cosmet | MET | same elements with title and persona line  |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence | Variant 3 | Evidence |
|---|---|---|---|---|---|---|
| L1 Unambiguous language | MET | closed class list and ordered message precedence leave little room  | NOT MET | Final: speed budget "a few milliseconds" and "three times the budget" have no number | NOT MET | Final: "never blocked" (section 1) contradicts "blocked in every session" (section 4) |
| L2 Concrete rather than abstract | MET | literal word lists, delimiters, millisecond budgets in sections 8 and 10  | MET | regexes, token lists, timeouts in section 8  | MET | literal JSON payload per case in section 12  |
| L3 Each section has a clear purpose | MET | headings name the decision, e.g. "Session identity (D1)"  | MET | headings name the decision, e.g. "Bash and git wrappers (D4)"  | MET | headings name the decision, e.g. "Fail-closed rules and speed (D6)"  |
| L4 Terms defined on first use | NOT MET | Final: "seed A2", "A12", "WC-13", "FR-23" used without definition (applied equally to all three | NOT MET | "governed" used in section 4, defined only in section 10  | NOT MET | Final: "A12", "A7", "WC-13" used without definition (applied equally to all three variants) |
| L5 Actionable next steps or decision points | MET | section 14 eight ordered steps; section 15 nine decisions with recommendations  | MET | section 14 five steps; section 15 seven decisions with defaults  | MET | section 14 six steps; section 15 six decisions with defaults  |
| **Subtotal** | **4/5** | | **3/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence | Variant 3 | Evidence |
|---|---|---|---|---|---|---|
| R1 At least 3 risks with probability and impact | NOT MET | R1 to R8 have reasons, no probability or impact rating  | NOT MET | ten cuts listed; only "likeliest workaround" hints at probability  | NOT MET | six residual bullets, no probability or impact rating  |
| R2 Mitigation for each risk | MET | each R row has "Why accepted"; section 16 gives a tolerance per unknown  | MET | cut table states what stays open; section 16 tolerance per item  | MET | each bullet gives its reason; section 16 tolerance per unknown  |
| R3 Failure modes and recovery | MET | section 10 table; LL-BROKEN and LL-TAMPER name a release step  | MET | F1 to F3 messages say release as in T1, or claim again  | MET | section 10 table; release by `rm` of the active file (R4)  |
| R4 External dependency failures | MET | jq missing, symbolic-ref timeout, hook timeout, missing record (section 10)  | MET | jq missing, invalid JSON, 1 s git timeout, hook timeout (section 10)  | MET | jq missing row; U8 harness failure voids binding (section 16)  |
| R5 Monitoring or validation mechanism | MET | OB-H1 to OB-H3 observed checks, LL-STATE note on degraded state  | MET | OB-H1 to OB-H5 including live wording check and real-machine timing  | MET | OB-H1 to OB-H3 plus T-FO and T-SPD regression guards  |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence | Variant 3 | Evidence |
|---|---|---|---|---|---|---|
| E1 Collection boundaries | MET | empty store fast path, other-sessions speed test, missing Monitor field  | MET | no sessions at all, empty state file, 100 KB command test  | MET | empty `tool_input` and unknown tool cases, 256 KB stdin cap  |
| E2 State-variable interactions | MET | approval kept in a separate file; degraded session still accepts approval  | MET | `.ok` written only at worktree level; prompts with `agent_id` ignored  | MET | approval lives in active JSON; invalid file resets `approved` to false  |
| E3 Guard-condition gaps | MET | bare push on main, detached HEAD, symbolic-ref failure all LL-PROTECTED  | MET | symbolic-ref printing master, main or nothing, plus `--all` and `--mirror`  | NOT MET | `git push origin HEAD` and `--all` pass at full with submit (X-007)  |
| E4 Count divergence | MET | stale record "over 30 minutes"; nonce binds at most one session  | MET | nonce regex `{32}`, single-use `mv`, 100 KB command speed test  | NOT MET | Final: four-word lookahead and 256 KB cap have no overflow behaviour or boundary test |
| E5 Interaction effects | MET | several-class precedence order; wrapper plus protected push in tests  | MET | `test_wrappers_at_every_level`; `\/` token form; store name split in source  | MET | Final: tests that after approval at W, git commit still exits 2 (an interaction case) |
| **Subtotal** | **5/5** | | **5/5** | | **3/5** | |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 2/5 | 3/5 | 1/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 3/5 | 3/5 |
| Risk Coverage | 4/5 | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 | 3/5 |
| **qual_score** | **25/30 = 0.8333** | **25/30 = 0.8333** | **21/30 = 0.7000** |

### Edge Case Floor Check (minimum 1/5)

| Variant | Score | Eligible as base |
|---|---|---|
| Variant 1 | 5/5 | yes |
| Variant 2 | 5/5 | yes |
| Variant 3 | 3/5 | yes |

## Position-Bias Mitigation

Pass 1 total: Variant 1 26, Variant 2 26, Variant 3 21. Pass 2 total: Variant 1 25, Variant 2 23, Variant 3 24. Of 90 criterion-variant pairs, 81 agreed and 9 disagreed. The orchestrator re-evaluated each disagreement against both passes' evidence (the re-evaluation is the final verdict).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| C1 Covers all requirements | 2 | MET | NOT MET | DISAGREE | MET (a measured speed test exists; the budget number is vague, scored under L1) |
| K5 Claims supported | 3 | NOT MET | MET | DISAGREE | NOT MET (cited V4 and V8 do not support its claims) |
| T5 Spec conventions | 2 | MET | NOT MET | DISAGREE | MET (missing title is cosmetic; the required structure is there) |
| L1 Unambiguous language | 3 | NOT MET | MET | DISAGREE | NOT MET (self-contradiction on "blocked in every session") |
| L1 Unambiguous language | 2 | MET | NOT MET | DISAGREE | NOT MET ("a few milliseconds" has no number) |
| L4 Terms defined | 3 | MET | NOT MET | DISAGREE | NOT MET (ids from other documents, applied equally to all three) |
| L4 Terms defined | 1 | MET | NOT MET | DISAGREE | NOT MET (same standard) |
| E4 Count divergence | 3 | NOT MET | MET | DISAGREE | NOT MET (lookahead window and size cap have no boundary test) |
| E5 Interaction effects | 3 | NOT MET | MET | DISAGREE | MET (tests approval against commit) |

Disagreements re-evaluated: 9. Final verdicts that differ from pass 1: 4 (L1 for Variant 2, L4 for Variants 1 and 3, E5 for Variant 3). Final verdicts that differ from pass 2: 5 (C1 and T5 for Variant 2; K5, L1 and E4 for Variant 3).
Method note: criterion-level evidence and the claim counts behind IC, SR and DC are each judge's own sample, so the metrics are approximate. Ranking sensitivity: pass 1 alone ranks Variant 2 first by 0.0003; pass 2 alone ranks Variant 1 first and Variant 3 above Variant 2. Only the combined result is used.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker (points won) |
|---|---|---|---|---|
| 1 (opus:architect) | 0.4947 | 0.4167 | **0.9113** | 7 (C-008, C-012, S-001, X-001, X-003, X-008, X-009) |
| 2 (sonnet:refactorer) | 0.4947 | 0.4167 | **0.9113** | 4 (C-003, C-006, X-004, X-010) |
| 3 (haiku:qa) | 0.4868 | 0.3500 | **0.8368** | 1 (C-017) |

Points won = points where the majority of the three final Round 2 tables name that variant as superior; the other 24 points were won by a merge of positions (see `convergence-tally.md`).

**Margin**: Variant 1 over Variant 2 is 0.0000 (below the 5% threshold); Variant 3 trails by 7.45 points.
**Tiebreaker applied**: Yes, level 1 (debate performance). Variant 1 won 7 points against 4 for Variant 2, which is not within 5%, so level 2 is not needed. For the record, level 2 (correctness criteria met) would have favoured Variant 2, 3 against 2.

## Selected Base: Variant 1 (opus:architect)

### Selection Rationale
Variant 1 ties Variant 2 on score and wins the debate tiebreaker by 7 points to 4. It is the strictest on failure (a marker always governs; trap-based exit 2), covers the most routes (MCP names, `/merge` URLs, remote and repo checks, Monitor), and keeps a closed list of action classes with a literal policy table and message table that tests can walk. Its two score losses are minor (a wrong Makefile claim, reused ids R1 to R3). Variant 3 trails because three of its errors break acceptance criteria AC-4, AC-5 and AC-6 (X-004, X-006, X-007).

### Strengths to Preserve from Base
1. "A marker always governs": a launch marker with a missing, stale or unreadable record still binds at `worktree` (U-001, X-001).
2. Closed action-class list with literal policy and message blocks, walked by grid-completeness tests (U-002).
3. Push-target and repo checks at `full --submit`, MCP and `/merge` URL coverage (U-003, U-004).
4. ERR and EXIT traps mapping unexpected ends to exit 2 (C-015).
5. Measured speed budget with 30 runs (C-017 base part).

### Strengths to Incorporate from Non-Base Variants
1. From Variant 2: one-word state files, empty `.ok` approval file written only at `worktree` (C-003, C-006); no always-on cwd fallback (X-004); two-part store name and `\/` token forms (U-005); ignore approval prompts that carry `agent_id` (U-006); smaller claim interface and `gh <group> create` below submit (U-007); correct `_FRESHNESS_SCRIPTS` location (X-010); flat, small script (S-004).
2. From Variant 3: binding cross-check against the record's worktree path, softened to a prefix match (U-008); relative speed guard and p95 budgets (U-009, C-017); `gh pr ready` never allowed, documented over-match asserted as blocked (U-010); literal JSON payload tests (C-019).
3. From the invariant probe (`invariant-probe.md`): the concrete fix for every UNADDRESSED finding (INV-001 to INV-040), each verified or tested by the fault-finder; five of them re-run by the orchestrator (skill names, env alias, configured push refspec, `--attr-source`, sweep timing).
4. From the Round 2 final tables: the merged rule for each of the 36 diff points (evidence cells of `round-2-advocate-1..3.md`, section 5).
