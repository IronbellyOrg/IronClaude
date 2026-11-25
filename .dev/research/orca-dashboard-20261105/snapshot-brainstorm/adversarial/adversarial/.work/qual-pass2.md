# Qualitative Pass 2 (order: V3, V2, V1)

## Variant 3
| Criterion | Claim | Evidence | Verdict |
|-----------|-------|----------|---------|
| CO1 | CO1 is met in V3 | Sec 2 requirements R01-R16 cover decisions, blockers, communication, change, verification, coverage; sec 1 names "Complete five-concept set" A-E; sec 10 recommends Decision Brief with four state screens; sec 11 evaluation tasks E01-E07; all fenced screens measured at most 70 columns | MET |
| CO2 | CO2 is met in V3 | Sec 4 rules: "Future timestamps produce `clock conflict`"; repeated or invalid cursor tokens yield partial coverage; sec 10 empty, busy, stale and complete-but-failing screens | MET |
| CO3 | CO3 is met in V3 | Sec 3 read-only data contract lists sources; sec 12 gates G01-G08 with an "If unresolved" column | MET |
| CO4 | CO4 is met in V3 | Sec 11 "Proposed acceptance": "At least 4 of 5 operators identify all four within 20 seconds" | MET |
| CO5 | CO5 is met in V3 | Sec 12 heading "Explicit limits and out of scope" | MET |
| CR1 | CR1 is met in V3 | Sec 3 restates seed context accurately: messages "capped at 100 with no advertised paging"; completion, terminal existence, liveness and verification kept distinct; no unsupported Orca capability asserted | MET |
| CR2 | CR2 is met in V3 | Sec 12 G01: "Ship only an observed-attention design" if the durable decision source is unresolved, keeping the design feasible under seed constraints | MET |
| CR3 | CR3 is met in V3 | W/M/V markers defined once in sec 4 and reused unchanged in sec 5-10 screens | MET |
| CR4 | CR4 is met in V3 | Stale-state ages are consistent with the as-of time (D1 08:20 to 09:20 = 60m; F1 18m; D2 25m); no conflicting rule statements found across sec 4 and sec 10 | MET |
| CR5 | CR5 is met in V3 | Sec 10 gives the rationale for Decision Brief as default against the other four concepts' tradeoffs | MET |
| ST1 | ST1 is met in V3 | Order: purpose, requirements, contract, rules, concepts 5-9, default 10, evaluation 11, risks/limits/gates 12 | MET |
| ST2 | ST2 is met in V3 | Numbered sections 1-12 with ### subsections under each concept; no orphaned subsection found | MET |
| ST3 | ST3 is met in V3 | Data contract (sec 3) separated from integrity/rendering rules (sec 4) and from concept screens (sec 5-9) | MET |
| ST4 | ST4 is met in V3 | Cross-references such as "specified in section 10" and "definitions from section 4" | MET |
| ST5 | ST5 is met in V3 | Requirement IDs with acceptance conditions (R01-R16), evaluation IDs (E01-E07), gate IDs (G01-G08) | MET |
| CL1 | CL1 is met in V3 | Sec 4 disambiguates: "`Newly observed` is not necessarily newly created" | MET |
| CL2 | CL2 is met in V3 | Each concept has a synthetic ASCII screen with concrete IDs, ages and owners | MET |
| CL3 | CL3 is met in V3 | Each concept section states organizing principle, strengths, tradeoffs and state behavior | MET |
| CL4 | CL4 is met in V3 | Sec 4: "`W` for worker projection, `M` for messages and `V` for the proposed independent verification contribution" | MET |
| CL5 | CL5 is met in V3 | Sec 10/12: "Decision for the next design review: evaluate Decision Brief..."; gates name the unresolved decisions | MET |
| RK1 | RK1 is not met in V3 | Sec 12 risk table columns are Risk / Consequence / Required mitigation; no probability or likelihood column or wording found - searched sections [3, 4, 11, 12] | NOT MET |
| RK2 | RK2 is met in V3 | Sec 12 risk table has a "Required mitigation" entry on every one of its 10 rows | MET |
| RK3 | RK3 is met in V3 | Sec 4: "Recovery compares with the last successful source observation"; failed collection never supplies a zero baseline | MET |
| RK4 | RK4 is met in V3 | Sec 12 gates G01-G08 name external sources with an "If unresolved" failure consequence | MET |
| RK5 | RK5 is met in V3 | Sec 11 "Future contract acceptance cases" and instruction to "assess E01/E06" as detection checks | MET |
| IE1 | IE1 is met in V3 | Sec 10: empty "0 workers"; single "1 worker... Shown 1/1"; overflow "Seven observed actionable bundles under a six-bundle budget" | MET |
| IE2 | IE2 is met in V3 | Sec 4: "A successful empty worker response plus failed message response never produces `all clear`"; inventory, worker and decision coverage kept as separate fields | MET |
| IE3 | IE3 is met in V3 | Sec 4: "Completion means a successful terminal page, not merely receiving fewer rows"; clock-conflict guard | MET |
| IE4 | IE4 is met in V3 | Sec 4 rule 8 separates "observed actionable items, shown, omitted from render and unobserved unknown"; "Even fewer than 100 returned messages do not prove complete" | MET |
| IE5 | IE5 is met in V3 | Sec 4: "Partial observations can establish positive additions, but not absence"; urgency escalation versus oldest-item pin addressed | MET |

## Variant 2
| Criterion | Claim | Evidence | Verdict |
|-----------|-------|----------|---------|
| CO1 | CO1 is met in V2 | Sec 3 requirement groups R-DEC, R-BLK, R-COM, R-CHG, R-VER, R-FLT, R-FMT, R-INT; sec 4 "Five-Question Snapshot Set (5Q)" C1-C5 each with a screen; sec 6 C1 recommended; sec 7 four states; sec 9 evaluation; screens measured at most 80 columns | MET |
| CO2 | CO2 is met in V2 | Sec 8 state-by-concept table; sec 7.4 complete-but-failing with stale revision handling | MET |
| CO3 | CO3 is met in V2 | Sec 12 gates FG-1 to FG-8; sec 12.3 "Close FG-1 and FG-8 first" | MET |
| CO4 | CO4 is met in V2 | Sec 9 ET-1 to ET-10 with targets, MC-1 to MC-8 pass rules, and decision rule 9.3 | MET |
| CO5 | CO5 is met in V2 | Sec 10 "Out of scope for this document" | MET |
| CR1 | CR1 is met in V2 | Fixture arithmetic checks out (2h14m, 3h02m, 3+1+2+1=7) and sec 5 line counts 27/26/24/25/21/13 match the screens; seed facts restated without new capability claims | MET |
| CR2 | CR2 is met in V2 | Sec 1 [E]/[P]/[G] tags mark gated items as proposals, so nothing depends on an unverified source being present | MET |
| CR3 | CR3 is met in V2 | C1-C5, FG-n and R-* identifiers used consistently across sec 3-12 | MET |
| CR4 | CR4 is not met in V2 | Sec 7.3 prints "NEEDS YOU  at least 3 last-known~" but lists only 2 rows with no shown+omitted line, contrary to R-OVF-01 and MC-6; sec 5 says C5 "omits the failing/unverified summary" while the C5 screen shows "UNVERIFIED  1 (T-DEMO-02)" | NOT MET |
| CR5 | CR5 is met in V2 | Sec 6 weighted rationale for C1, ratings explicitly labelled as judgments | MET |
| ST1 | ST1 is met in V2 | Order: tags, shared contract, requirements, concepts, comparison, default, states, evaluation, scope, risks, gates | MET |
| ST2 | ST2 is met in V2 | Numbered subsections 2.2, 2.6, 7.1-7.4, 12.3 nest under their parents; no orphan found | MET |
| ST3 | ST3 is met in V2 | Shared contract (sec 2) separated from requirements (sec 3), concept screens (sec 4) and states (sec 7-8) | MET |
| ST4 | ST4 is met in V2 | Cross-references "see section 8" and R-ID references inside risks and tests | MET |
| ST5 | ST5 is met in V2 | Requirement IDs, test IDs (ET/MC), risk IDs (RK) and gate IDs (FG) follow spec conventions | MET |
| CL1 | CL1 is met in V2 | Sec 2.2 symbols table fixes meaning of each marker; "shown + omitted = observed" stated explicitly | MET |
| CL2 | CL2 is met in V2 | Sec 2.6 synthetic fixture and concrete screens with T-DEMO identifiers | MET |
| CL3 | CL3 is met in V2 | Each section opens with its role (contract, requirements, concepts, states, evaluation, risks) | MET |
| CL4 | CL4 is met in V2 | Sec 1 tag table defines [E]/[P]/[G]; sec 2.2 symbols table defines every marker | MET |
| CL5 | CL5 is met in V2 | Sec 12.3 "Recommended next step" | MET |
| RK1 | RK1 is met in V2 | Sec 11 has a "Likelihood / impact (judgment)" column, e.g. RK-1 "High / High", across RK-1 to RK-15 | MET |
| RK2 | RK2 is met in V2 | Sec 11 gives a mitigation for each of RK-1 to RK-15 | MET |
| RK3 | RK3 is met in V2 | Sec 7.3 "Baseline kept at 08:55Z; 2 samples missed"; R-CHG-04 recovery from last good observation | MET |
| RK4 | RK4 is met in V2 | Sec 12 FG table with an "If open" consequence per external source gate | MET |
| RK5 | RK5 is met in V2 | Sec 9 MC-1 to MC-8 and ET-4 referenced from risks as detection checks | MET |
| IE1 | IE1 is not met in V2 | Empty (7.2) and overflow (7.1, 19 items) are covered; no single-item boundary found - searched sections [2.6, 4, 7, 8, 9] | NOT MET |
| IE2 | IE2 is met in V2 | Sec 8: "a failed source for one band makes only that band stale"; R-FLT-03 | MET |
| IE3 | IE3 is met in V2 | R-INT-01 guard and sec 7 "If any source were PARTIAL... would become" | MET |
| IE4 | IE4 is met in V2 | Sec 2: "shown + omitted = observed"; "N observed*" notation for partial counts | MET |
| IE5 | IE5 is met in V2 | Sec 8 combined-state table and "Common repair applied to all four" | MET |

## Variant 1
| Criterion | Claim | Evidence | Verdict |
|-----------|-------|----------|---------|
| CO1 | CO1 is met in V1 | Sec 3 requirements DEC, BLK, COM, CHG, VER, COV, FMT; sec 5 "The complete set is: A Attention Brief, B Control Board, C Root-Blocker Tree, D Conversation Ledger, E Delta Journal"; sec 11 A recommended; sec 12 four states; sec 14 EV tasks; width "at most 78 columns" | MET |
| CO2 | CO2 is met in V1 | Each concept in sec 6-10 has its own "State handling" paragraph; sec 13 OVF-1 to OVF-8 | MET |
| CO3 | CO3 is met in V1 | Sec 17 gates G1-G8; sec 11.2 data dependency table | MET |
| CO4 | CO4 is met in V1 | Sec 14 EV thresholds, e.g. "Correct in at least 9 of 10 trials; median under 30 s" | MET |
| CO5 | CO5 is met in V1 | Sec 15 "Out of scope" | MET |
| CR1 | CR1 is met in V1 | Board totals and tree "distinct blocked tasks: 6" check out; stale age 47 to 62m correct; seed source limits restated accurately | MET |
| CR2 | CR2 is met in V1 | Sec 2 layer 1 uses only read-only sources and gates unverified ones in sec 17 | MET |
| CR3 | CR3 is met in V1 | Concept letters, OVF/EV/G identifiers and coverage markers used consistently | MET |
| CR4 | CR4 is not met in V1 | Sec 3 COV-3: an empty section reads "`0 observed (partial)`, never `none`", but sec 12.1 prints "answered, unresolved: none observed" under partial coverage; sec 12 says "The bottom status banner is the only line whose wording changes by state" yet the stale banner is placed "(top of body)" | NOT MET |
| CR5 | CR5 is met in V1 | Sec 11.3 rationale for Attention Brief as default | MET |
| ST1 | ST1 is met in V1 | Order: status, architecture, requirements, frame, set, concepts, comparison, states, overflow, evaluation, limits, risks, gates | MET |
| ST2 | ST2 is met in V1 | Numbered sections 1-17 with consistent subsections (e.g. 4.3, 11.2, 11.3, 12.1) | MET |
| ST3 | ST3 is met in V1 | Sec 2 four-layer table separates collection, normalization, ranking and rendering | MET |
| ST4 | ST4 is met in V1 | Sec 1 "Reading Guide"; references such as "see section 12" and "gate G1, section 17" | MET |
| ST5 | ST5 is met in V1 | Requirement, overflow, evaluation, risk and gate IDs follow spec conventions | MET |
| CL1 | CL1 is met in V1 | Sec 4.3 notation: "`1+1*` reads '1 current plus 1 last-good'" | MET |
| CL2 | CL2 is met in V1 | Every concept has a synthetic ASCII screen with concrete keys and ages | MET |
| CL3 | CL3 is met in V1 | Each section has a stated purpose, introduced by the sec 1 Reading Guide | MET |
| CL4 | CL4 is not met in V1 | Sec 5 cites "PagerDuty triggered/acknowledged/resolved separation" and "Dolphie observation/replay separation" without defining either; neither appears in the seed brief | NOT MET |
| CL5 | CL5 is met in V1 | Sec 17 gates and "Open design questions for the debate" | MET |
| RK1 | RK1 is not met in V1 | Sec 16 risk table columns are Risk / Effect / Mitigation; no probability or likelihood found - searched sections [2, 13, 15, 16, 17] | NOT MET |
| RK2 | RK2 is met in V1 | Sec 16 gives a mitigation for each of R-1 to R-11 | MET |
| RK3 | RK3 is met in V1 | Layer 2 gap records; G7 "first report after restart prints `n/a`" | MET |
| RK4 | RK4 is met in V1 | Sec 17 gates with "If it fails" consequence per external source | MET |
| RK5 | RK5 is met in V1 | EV-10 width check; TRAIL "makes collection gaps visible"; golden-text testability | MET |
| IE1 | IE1 is met in V1 | Empty sec 12.1; single "workers ok 1/1pg"; overflow OVF-3 "... and K more keys not printed" | MET |
| IE2 | IE2 is met in V1 | VER-5 res-held explains "workers live 1 with zero running attempts"; current versus last-good split in "`1+1*`" | MET |
| IE3 | IE3 is met in V1 | COV-4 guard; "A `seen>=` age is a lower bound, so such an item may be older than an item ranked above it" | MET |
| IE4 | IE4 is met in V1 | OVF-5 separates paging coverage from overflow; OVF-7 flags when "rows returned equal the cap" | MET |
| IE5 | IE5 is met in V1 | OVF-5 "Both can be non-zero at once"; sec 10 "Change wording can create urgency bias" | MET |

## Summary
| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total /30 |
|---------|--------------|-------------|-----------|---------|------|-----------|-----------|
| V3 | 5 | 5 | 5 | 5 | 4 | 5 | 29 |
| V2 | 5 | 4 | 5 | 5 | 5 | 4 | 28 |
| V1 | 5 | 4 | 5 | 4 | 4 | 5 | 27 |
