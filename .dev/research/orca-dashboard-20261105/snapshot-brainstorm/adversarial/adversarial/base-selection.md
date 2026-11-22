# Base Selection Report

Variants: V1 = variant-1-opus-architect.md (opus:architect), V2 = variant-2-sonnet-analyzer.md (sonnet:analyzer), V3 = variant-3-haiku-backend.md (haiku:backend). Scoring per refs/scoring-protocol.md (A.1-A.5): 6 qualitative dimensions, 30 binary criteria.

## Quantitative Scoring (50% weight)

Computed deterministically by `.work/quant.py` (rules fixed in its docstring before the run; rerun once after fixing a parser defect that missed V3 table-cell ID definitions such as `| E01 Find ...`).

| Metric | Weight | V1 (opus:architect) | V2 (sonnet:analyzer) | V3 (haiku:backend) |
|--------|--------|---------------------|----------------------|--------------------|
| requirement_coverage | 0.30 | 1.000 (26/26 seed topics) | 1.000 (26/26) | 1.000 (26/26) |
| internal_consistency | 0.25 | 0.985 (3 contradictions X-005, X-006, X-010 / 199 claims) | 0.988 (3: X-007, X-008, X-009 / 257) | 1.000 (0 / 78) |
| specificity_ratio | 0.15 | 0.995 (186 concrete / 1 vague) | 1.000 (235 / 0) | 1.000 (62 / 0) |
| dependency_completeness | 0.15 | 1.000 (146/146 refs resolve) | 1.000 (162/162) | 1.000 (44/44) |
| section_coverage | 0.15 | 1.000 (17/17 H2) | 0.706 (12/17) | 0.706 (12/17) |
| **quant_score** | | **0.995** | **0.953** | **0.956** |

Limitation: the seed brief has no requirement IDs, so RC uses section-level keyword topic matching (protocol edge case). Keyword presence does not prove a requirement is satisfied, so RC does not discriminate here; requirement satisfaction is judged by qualitative criterion CO1. Evidence cells below write a literal table pipe as `/`.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| CO1 | MET | §5 "The complete set is: A Attention Brief, B Control Board, C Root-Blocker Tree, D Conversation Ledger, E Delta Journal."; §1 "every screen in this document is plain ASCII and at most 78 columns"; §12 four states; §14 EV-1..EV-10; §15 limits | MET | §4 "Set name: the Five-Question Snapshot Set (5Q)", C1-C5; §6 default C1; §7 four states; §9 ET-1..10 and MC-1 "Every line 80 columns or fewer; only printable ASCII"; §10 limits | MET | §1 "Complete five-concept set: A. Decision Brief; B. Run Ledger; C. Blocker Paths; D. Conversation Handoffs; E. Change Journal."; §10 default plus four states; §11 E01-E07; §12 limits |
| CO2 | MET | §12.3 "host-DEMO-2 unreachable since 09:12Z: its workers are unknown, not 0"; §3 CHG-2 "A failed or partial collection never supplies a zero baseline" | MET | §7.3 "FLEET       ? (unknown; unknown is not zero and not healthy)"; §8 risk per concept per state | MET | §3 "Repeated tokens, invalid tokens, page errors or a collection deadline produce partial coverage." |
| CO3 | MET | §11.2 data dependency table, "C / Complete task dependency graph / UNROOTED list only"; §17 G1 "Is there a complete, non-consuming source that enumerates durable pending decisions" | MET | §5 "Gate load / Low: needs FG-1 only for the count label / ... / High: dependency graph"; §12 FG-3 "Is a task dependency graph readable, and how complete is it?" | MET | §7 "most demanding data prerequisite"; §12 G01 "This is the central feasibility gate" |
| CO4 | MET | §14 EV-1 "Correct in at least 9 of 10 trials; median under 30 s"; EV-10 "Zero wrapped lines" | MET | §9 ET-1 "C1 at least 90% correct, median 15 s or less"; §9.3 decision rule | MET | §11 E01 "At least 4 of 5 operators identify all four within 20 seconds" |
| CO5 | MET | §15 "Out of scope: Scheduling, posting automation..." | MET | §10 "Out of scope for this document. - Scheduling or posting..." | MET | §12 limits "No API endpoint, durable decision store, overflow archive... is assumed to exist" |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| CR1 | MET | §1 "Status: design proposal only. Nothing in this document was implemented"; §14 "Status: proposed protocol only"; no runtime claims found in §11-§17 | MET | §9 "None of these tasks has been run"; §1 tags [E]/[P]/[G] separate evidence from proposal; no runtime claims found | MET | §11 "No tests, collector calls, performance measurements or operator trials were performed for this design artifact." |
| CR2 | MET | §17 G1 "If it fails / Keep `>=N` and 'oldest observed' permanently": each capability has a degraded path within the read-only constraints | MET | §6 "It degrades gracefully. If the dependency graph is missing, the 'holds' ..." | MET | §10 "does not depend on a complete dependency graph or thread history to remain useful" |
| CR3 | MET | §3 IDs DEC/BLK/COM/CHG/VER/COV/FMT reused verbatim in §12 "(CHG-2)", "(COV-2)", "(VER-3)" | MET | R-ROW, R-OVF, R-INT IDs defined in §2-§3 and reused verbatim in §5, §7, §8 ("R-INT-05") | MET | §10 "W, M and V use the definitions from section 4"; §11 "define fixture-based checks for R01-R16" |
| CR4 | NOT MET | §3 "'Must' applies to every concept unless a concept section says otherwise" and DEC-2 "Each decision row carries: ... impact and at least one evidence reference", yet the §7.2 B row `A DECIDE  D-DEMO-0042 47m "Approve schema v7 or keep v6..."  w-07` has neither impact nor evidence, and §7.3 does not exempt it | NOT MET | §3 R-DEC-03 "Each decision row must meet R-ROW (id, question, requester, owner, age, impact, evidence reference)" vs §5 "C4 rows have no impact and no message reference, and C2 and C3 omit the message reference on some rows" | MET | Checked §1 fixture against §3: "Cursor exhaustion alone does not prove a point-in-time census" agrees with §10 "decision census unknown"; no contradiction found in §1-§12 |
| CR5 | MET | §2 "Why this shape is the maintainable choice"; §11.1 "Ratings are design judgments..." with per-row reasons | MET | §3 Basis column "seed brief (SB) or REPORT.md section (RP n)", e.g. R-VER-04 "/ RP 3 /"; §6 numbered rationale | MET | §10 "It puts the oldest blocking question in a fixed location, keeps unanswered context across quiet periods"; each concept has Strengths/Tradeoffs |
| **Subtotal** | **4/5** | | **4/5** | | **5/5** | |

### Structure (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| ST1 | MET | Order: §1 scope, §2 model, §3 requirements, §4 frame, §5-§10 concepts, §11 default, §12 states, §13 overflow, §14 evaluation, §15-§17 limits/risks/gates | MET | §1 purpose, §2 contract, §3 requirements, §4 concepts, §5 comparison, §6 default, §7-§8 states, §9 evaluation, §10 limits, §11 risks, §12 gates and next step | MET | §1 purpose, §2 requirements, §3 contract, §4 rules, §5-§9 concepts, §10 default/states, §11 evaluation, §12 risks/limits/gates |
| ST2 | MET | Numbered sections with child subsections (§11.1-§11.3; §12.1-§12.4); no orphaned single subsection found | MET | §2.1-§2.6 and §7.1-§7.4 numbered children; no orphaned subsection found | MET | §10 four state subsections; §11 "Operator tasks" and "Future contract acceptance cases"; no orphan found |
| ST3 | MET | §2 four layers, "1. Collector adapters ... 2. Observation store", each with a "Must never" column | MET | §2 "Shared Report Contract" kept apart from §3 requirements and §4 concept renderings | MET | §3 observation contract kept apart from §4 integrity rules and §5-§9 renderings |
| ST4 | MET | §1 Reading Guide; cross-refs "(gate G1, section 17)", "Evaluation (section 14)" | MET | Cross-refs "(section 12) (FG-1)", "section 5 lists the check"; §11 Requirement column links risks to requirement IDs | MET | Cross-refs §5 "specified in section 10"; §10 "W, M and V use the definitions from section 4" (no TOC, but cross-references present) |
| ST5 | MET | §1 "Status: design proposal only"; requirement IDs with "Must" language (§3); tradeoffs (§11), risks (§16), gates (§17) | MET | Requirement tables with Basis (§3), comparison (§5), risks with likelihood (§11), open gates (§12) | MET | §2 R01-R16 with acceptance conditions; §12 risks, limits, gates G01-G08 |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| CL1 | MET | §13 OVF-5 "Overflow is 'observed but not printed'; paging coverage is 'not observed because the source was capped or not fully paged'" | MET | §7.2 "NOT AN ALL-CLEAR FOR: hosts not reported, transitions between samples..." | MET | §4 rule 8 "Footer distinguishes `observed actionable items`, `shown`, `omitted from render` and `unobserved unknown`" |
| CL2 | MET | §12 banner "NO ATTENTION ITEMS OBSERVED. This is not an all-clear: coverage partial."; §7.2 "`1+1*` reads '1 current plus 1 last-good'" | MET | §7.1 "+16 more observed, not shown (shown 3 + omitted 16 = 19*)" | MET | §4 rule 7 "no more than six actionable item bundles and a target of 44 lines" |
| CL3 | MET | §1 Reading Guide states each section's role; §17 "Gates are checks that must pass before a capability is promised" | MET | §1 Purpose/Scope; §4 each concept tied to one question, e.g. C3 "Which single answer unblocks the most work?" | MET | §1 "These organize the entire report by priority, run ownership, dependency, dialogue and change respectively" |
| CL4 | NOT MET | ANSI (FMT-1), UTC (COV-1) and API (§17 G1 "a cursor or event API") are used without definition; searched §1-§4, §17 | NOT MET | (re-evaluated, final) Defined: s.1 tag table "[E] / Stated in the seed brief..."; s.2.2 "`*` / Partial: lower bound". Undefined: s.10 item 10 "Terminal ANSI colour is an optional export"; s.12 FG-1 "A read-only API or event source with paging"; no expansion of ANSI or API anywhere | NOT MET | (re-evaluated, final) Defined: s.4 "use `W` for worker projection, `M` for messages and `V` for the proposed independent verification contribution". Undefined: "no ANSI, tabs, control sequences" (render rule 10); "This is a logical contract for a future adapter, not a new API endpoint specification"; "No API endpoint, durable decision store..." (s.12); "80 ASCII columns". A file-wide search found no expansion of API or ANSI. |
| CL5 | MET | §11.3 "Recommended default: Concept A"; §17 G1-G8 with "If it fails" actions plus open questions | MET | §12.3 "Close FG-1 and FG-8 first... Then run the mechanical checks MC-1..MC-8" | MET | Closing "Decision for the next design review: evaluate Decision Brief with the synthetic tasks, while verifying G01..." |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| RK1 | NOT MET | §16 header "/ ID / Risk / Effect / Mitigation in this design /" gives impact (Effect) only, no probability for R-1..R-11; searched §16, §17 | MET | §11 header "/ ID / Risk / Likelihood / impact (judgment) / Mitigation / Requirement /", RK-1 "High / High", 15 risks | NOT MET | §12 risks header "/ Risk / Consequence / Required mitigation /" gives consequence only, no probability; searched §12 |
| RK2 | MET | §16 every row has "Mitigation in this design", e.g. R-8 "Shared frame and single derivation layer (section 2)" | MET | §11 Mitigation column filled for RK-1..RK-15 | MET | §12 "Required mitigation" column for every risk row |
| RK3 | MET | §2 store "an explicit gap record for each failed or partial collection"; §12.3 "the change section prints `n/a` rather than zero (CHG-2)" | MET | §7.3 "SINCE       NO VALID COMPARISON. Baseline kept at 08:55Z; 2 samples missed." | MET | §11 "A collection interruption cannot advance a source's last-success pointer. A rendering interruption cannot publish a half report" |
| RK4 | MET | §17 G1 needs a "complete, non-consuming source"; on failure "Keep `>=N` and 'oldest observed' permanently"; §11.2 lists the fallback per data dependency | MET | §12 FG-3 "/ 'holds ?'; C3 not offered /"; FG-2 "Verification lines show `?` or 'claim only'" | MET | §12 G03 "Show completion claims and verification unavailable; do not invent check results or ready totals." |
| RK5 | MET | §14 EV-2 "Names the capped or partial source"; EV-10 "mechanical check, no participant needed" | MET | §9 MC-1..MC-8 mechanical checks; §12.1 "A gate must be closed by verifying a source (not by assuming one)" | MET | §11 "Before implementation approval, define fixture-based checks for R01-R16"; "Any false all-clear in E02-E04 is a design blocker" |
| **Subtotal** | **4/5** | | **5/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| IE1 | MET | Empty: §12 "Empty, partial coverage"; single: §12.3 "the body is shrunk to one full row"; overflow: §13 OVF-3 "... and K more keys not printed" | NOT MET | Empty: s.7.2 "Empty / healthy (nothing observed)" with "NEEDS YOU   none observed". Overflow: s.7.1 "+16 more observed, not shown (shown 3 + omitted 16 = 19*)" and s.2.5 R-OVF. Single: only s.4.1 "UNVERIFIED (claimed done, no independent check seen)  1: T-DEMO-02", which sits inside the busy fixture; s.7 defines four states (busy/overflow, empty, stale, reported-complete) and none is a one-item state. | MET | Empty: §10 "Shown 0/0 observed actionable items"; single: §10 "Shown 1/1 observed actionable items"; overflow: §11 "Seven observed actionable bundles under a six-bundle budget account for one omitted bundle" |
| IE2 | MET | §12.4 "`res-held 1` reports a settled attempt that still owns a live terminal, which explains `workers live 1` with zero running attempts (VER-1, VER-5)" | MET | §7.4 "NOT AN ALL-CLEAR: 2 tasks reported done are not verified done." (assignment source vs verification source) | MET | §10 "Terminal exists; process liveness unknown; neither proves ready."; §2 R13 "workspace parentage does not become a dependency" |
| IE3 | MET | §3 COV-3 "an empty section reads `0 observed (partial)`, never `none`"; concept D state handling "never prints 'inbox zero' while any message source is capped" | MET | §3 R-VER-04 "A task reported complete with no independent verification must read 'unverified', counted apart from failing" | MET | §4 rule 1 "Future timestamps produce `clock conflict`, never negative waiting time"; §10 "If no successful history exists, print `No last-known records available`" |
| IE4 | MET | §3 BLK-3 "A task blocked by two roots is counted once in the fleet total and marked `shared`"; §7.2 "Totals that mix current and last-good values are never added together" | MET | §2.5 "Totals shown must equal shown rows plus omitted rows"; §2 "the group only shows the shared dependents once" | MET | §4 rule 6 "A task blocked by two questions contributes once to fleet impact"; §11 "Duplicate worker records do not inflate counts" |
| IE5 | MET | §13 OVF-5 "Paging coverage is distinct from overflow... Both can be non-zero at once" | MET | §8 Busy row "CHANGED block capped first, CARRIED block capped second; both print shown + omitted = observed" | MET | §11 "A successful empty worker response plus failed message response never produces `all clear`."; §7 "multi-parent tasks must repeat with `also under <ID>` and count once" |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

Full Claim/Evidence/Verdict rows: `.work/qual-pass1.md` (order V1, V2, V3), `.work/qual-pass2.md` (order V3, V2, V1), `.work/qual-reeval.md` (disagreements).

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 4/5 | 4/5 | 5/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 5/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 4/5 | 5/5 |
| **qual_score** | **27/30 = 0.900** | **27/30 = 0.900** | **28/30 = 0.933** |

## Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (>= 1/5) | Eligible as base |
|---------|-----------------------------|----------------|------------------|
| V1 | 5/5 | Pass | Yes |
| V2 | 4/5 | Pass | Yes |
| V3 | 5/5 | Pass | Yes |

Floor not suspended (no variant scored 0/5).

## Position-Bias Mitigation

Pass 1 order V1, V2, V3 (`.work/qual-pass1.md`); pass 2 order V3, V2, V1 (`.work/qual-pass2.md`); separate independent evaluators. 87 of 90 verdicts agreed.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| CL4 | V2 | NOT MET | MET | DISAGREE | NOT MET (pass 2 checked only invented symbols; ANSI and API undefined, same standard as V1) |
| IE1 | V2 | MET | NOT MET | DISAGREE | NOT MET (single-item case appears only as incidental fixture data; no one-item state or rule) |
| CL4 | V3 | NOT MET | MET | DISAGREE | NOT MET (API and ANSI undefined, same standard as V1) |

Disagreements re-evaluated: 3 (independent third evaluator, `.work/qual-reeval.md`)
Final verdicts changed: 3 relative to pass 2 (V2 total 28 -> 27, V3 total 29 -> 28); 1 relative to pass 1 (V2 IE1).

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (opus:architect) | 0.4975 | 0.4500 | **0.9475** | 11 diff points won |
| V2 (sonnet:analyzer) | 0.4765 | 0.4500 | **0.9265** | 12 diff points won |
| V3 (haiku:backend) | 0.4780 | 0.4667 | **0.9447** | 21 diff points won |

**Margin**: 0.28% (V1 0.9475 vs V3 0.9447; V2 is 2.1% behind V1)
**Tiebreaker applied**: Yes. The top two are within 5%, so scoring-protocol A.4 level 1 applies: the variant that won more debate diff points is selected. V3 won 21 of 46 points, V1 won 11 (Round 2 tally, `.work/consensus-round2.txt`; 2 points unresolved). Levels 2 and 3 were not needed.

## Selected Base: Variant 3 (haiku:backend)

### Selection Rationale

V1 has the highest raw combined score, but its lead over V3 (0.0028) is inside the 0.05 tie band, so the protocol tiebreaker decides. V3 won 21 debate points against V1's 11, mostly on observation and data integrity (C-005, C-006, C-007, C-009, C-012, C-013, C-014, C-017, X-002..X-005, X-008..X-010, A-001, A-002, A-004). V3 also has the only qualitative Correctness score of 5/5 and zero internal contradictions (internal_consistency 1.000).

Recorded neutrally: in Round 2 all three advocates, including V3's, recommended V1's architecture and frame as the skeleton of the merge, and V3 conceded that its five concepts are not visibly distinct (C-002, Round 2 CR-1) and that it has no frame or printed legend (S-004, S-011, CR-3). The orchestrator does not override the protocol result. Instead, the refactor plan imports V1's layer model, frame, legend, DEC-1 ordering and distinct concept structures into the V3 base, so the debate outcome is honored without changing the selected base. This makes the merge a large restructure (see refactor-plan.md risk level).

### Strengths to Preserve from Base

- Observation envelope with separate collection time and evidence time; a successful fetch of an old record is not fresh (V3 s.3 Observation envelope).
- Census honesty: a page below the message cap is not a complete history; `decision census unknown` stays independent of worker coverage (V3 s.3 Source capabilities; X-003, C-006).
- Integrity rules 1-10: age bounds and `clock conflict` (rule 1), oldest pointer kept on any override (rule 2), last-known unresolved instead of inferred resolution (rule 3), per-source and per-scope baselines with positive-only partial additions (rules 4-5), overlap note and union counts (rule 6), whole-bundle omission and four-way accounting (rules 7-9), wrapping, escaping and marked redaction (rule 10) (V3 s.4).
- Age-ranked root blockers with `dependency conflict` for cycles (V3 s.7; X-002, C-007).
- Scope-qualified empty state that never becomes a fleet-wide all-clear (V3 s.10; X-004, C-012), with the host line qualified per Round 2 CR-10.
- Full last-known bundles under a not-confirmed-current banner in the stale state (V3 s.10; C-013).
- Distinct unavailable / stale / mismatched / failed verification labels with revision provenance (V3 s.3, s.10; C-014).
- Observable acceptance condition per requirement (V3 s.2; S-003 unresolved) and future contract acceptance cases (V3 s.11).
- Consistent DEMO-marked synthetic identifiers (V3 s.1, s.5-10; C-020, X-008, X-010).
- Acting human kept distinct from requesting worker; missing owner stays unknown (V3 s.3 Logical records; A-002).

### Strengths to Incorporate from Non-Base Variants

From V1 (opus:architect):
- Four-layer model with owns / must-never boundaries (V1 s.2; S-002) and a Layer column on every requirement (V1 s.3; S-003 input).
- Document organization: architecture, requirements, frame, one section per concept, comparison, states, overflow, evaluation, limits, risks, gates (V1 s.1-17; S-001).
- Shared report frame contract: header, footer, fields, notation, printed legend, stable identity rule (V1 s.4.1-4.4; S-004, S-011, S-012).
- DEC-1 decisions-first and DEC-3 mandatory OLDEST line in every concept (V1 s.3.1, s.4.2; C-004, X-001, X-006, X-007).
- Five structurally distinct concepts: queue, tree, ladder, journal (V1 s.6, s.8, s.9, s.10; C-002), with C and E repaired under DEC-1.
- y/n/? transport and resolution ladder (V1 s.9.1; C-015).
- VANISHED as an explicit delta kind, with the capped-read qualifier (V1 CHG-3, DEC-6; C-010).
- Comparison ratings and data-dependency table (V1 s.11.1-11.2; S-008).
- Never-print-all-clear in the default (V1 COV-4, as narrowed by X-004).

From V2 (sonnet:analyzer):
- Responsibility axis: C2 Ball-Holder Board as the second concept (V2 s.4.2; C-001), without naming the relay as owner (V2 Round 2 CR-8).
- Synthetic fixture table shared by every screen (V2 s.2.6; S-005).
- 19-decision overflow screen with printed arithmetic (V2 s.7.1; S-007) and the hard line budget (V2 R-FMT-03, R-OVF-01; C-016).
- ANSWERED, NOT RESOLVED band (V2 s.4.1, s.6; C-011) and WATCH row (V2 s.2.4, s.4.1; C-008).
- Hybrid default with one test-gated switch rule (V2 s.6, s.9.3; C-003).
- Concept x state matrix (V2 s.8; S-006).
- Evaluation: reader tasks, mechanical checks, decision rule (V2 s.9.1-9.3; S-009, C-018).
- Gate table with closing evidence and FG-8 Cannot-ship (V2 s.12.1; S-010, C-019).
