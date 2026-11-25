# Qualitative Pass 1 (order: V1, V2, V3)

## Variant V1
| Criterion | Claim | Evidence | Verdict |
|-----------|-------|----------|---------|
| CO1 | CO1 is met in V1 | §5 "The complete set is: A Attention Brief, B Control Board, C Root-Blocker Tree, D Conversation Ledger, E Delta Journal."; §1 "every screen in this document is plain ASCII and at most 78 columns"; §12 four states; §14 EV-1..EV-10; §15 limits | MET |
| CO2 | CO2 is met in V1 | §12.3 "host-DEMO-2 unreachable since 09:12Z: its workers are unknown, not 0"; §3 CHG-2 "A failed or partial collection never supplies a zero baseline" | MET |
| CO3 | CO3 is met in V1 | §11.2 data dependency table, "C \| Complete task dependency graph \| UNROOTED list only"; §17 G1 "Is there a complete, non-consuming source that enumerates durable pending decisions" | MET |
| CO4 | CO4 is met in V1 | §14 EV-1 "Correct in at least 9 of 10 trials; median under 30 s"; EV-10 "Zero wrapped lines" | MET |
| CO5 | CO5 is met in V1 | §15 "Out of scope: Scheduling, posting automation..." | MET |
| CR1 | CR1 is met in V1 | §1 "Status: design proposal only. Nothing in this document was implemented"; §14 "Status: proposed protocol only"; no runtime claims found in §11-§17 | MET |
| CR2 | CR2 is met in V1 | §17 G1 "If it fails \| Keep `>=N` and 'oldest observed' permanently" - each capability has a degraded path within the read-only constraints | MET |
| CR3 | CR3 is met in V1 | §3 IDs DEC/BLK/COM/CHG/VER/COV/FMT reused verbatim in §12 "(CHG-2)", "(COV-2)", "(VER-3)" | MET |
| CR4 | CR4 is not met in V1 | §3 "'Must' applies to every concept unless a concept section says otherwise" and DEC-2 "Each decision row carries: ... impact and at least one evidence reference", yet the §7.2 B row `A DECIDE  D-DEMO-0042 47m "Approve schema v7 or keep v6..."  w-07` has neither impact nor evidence, and §7.3 does not exempt it | NOT MET |
| CR5 | CR5 is met in V1 | §2 "Why this shape is the maintainable choice"; §11.1 "Ratings are design judgments..." with per-row reasons | MET |
| ST1 | ST1 is met in V1 | Order: §1 scope, §2 model, §3 requirements, §4 frame, §5-§10 concepts, §11 default, §12 states, §13 overflow, §14 evaluation, §15-§17 limits/risks/gates | MET |
| ST2 | ST2 is met in V1 | Numbered sections with child subsections (§11.1-§11.3; §12.1-§12.4); no orphaned single subsection found | MET |
| ST3 | ST3 is met in V1 | §2 four layers, "1. Collector adapters ... 2. Observation store", each with a "Must never" column | MET |
| ST4 | ST4 is met in V1 | §1 Reading Guide; cross-refs "(gate G1, section 17)", "Evaluation (section 14)" | MET |
| ST5 | ST5 is met in V1 | §1 "Status: design proposal only"; requirement IDs with "Must" language (§3); tradeoffs (§11), risks (§16), gates (§17) | MET |
| CL1 | CL1 is met in V1 | §13 OVF-5 "Overflow is 'observed but not printed'; paging coverage is 'not observed because the source was capped or not fully paged'" | MET |
| CL2 | CL2 is met in V1 | §12 banner "NO ATTENTION ITEMS OBSERVED. This is not an all-clear: coverage partial."; §7.2 "`1+1*` reads '1 current plus 1 last-good'" | MET |
| CL3 | CL3 is met in V1 | §1 Reading Guide states each section's role; §17 "Gates are checks that must pass before a capability is promised" | MET |
| CL4 | CL4 is not met in V1 | ANSI (FMT-1), UTC (COV-1) and API (§17 G1 "a cursor or event API") are used without definition; searched §1-§4, §17 | NOT MET |
| CL5 | CL5 is met in V1 | §11.3 "Recommended default: Concept A"; §17 G1-G8 with "If it fails" actions plus open questions | MET |
| RK1 | RK1 is not met in V1 | §16 header "\| ID \| Risk \| Effect \| Mitigation in this design \|" gives impact (Effect) only, with no probability or likelihood for any of R-1..R-11; searched §16, §17 | NOT MET |
| RK2 | RK2 is met in V1 | §16 every row has "Mitigation in this design", e.g. R-8 "Shared frame and single derivation layer (section 2)" | MET |
| RK3 | RK3 is met in V1 | §2 store "an explicit gap record for each failed or partial collection"; §12.3 "the change section prints `n/a` rather than zero (CHG-2)" | MET |
| RK4 | RK4 is met in V1 | §17 G1 needs a "complete, non-consuming source"; on failure "Keep `>=N` and 'oldest observed' permanently"; §11.2 lists the fallback per data dependency | MET |
| RK5 | RK5 is met in V1 | §14 EV-2 "Names the capped or partial source"; EV-10 "mechanical check, no participant needed" | MET |
| IE1 | IE1 is met in V1 | Empty: §12 "Empty, partial coverage"; single: §12.3 "the body is shrunk to one full row"; overflow: §13 OVF-3 "... and K more keys not printed" | MET |
| IE2 | IE2 is met in V1 | §12.4 "`res-held 1` reports a settled attempt that still owns a live terminal, which explains `workers live 1` with zero running attempts (VER-1, VER-5)" | MET |
| IE3 | IE3 is met in V1 | §3 COV-3 "an empty section reads `0 observed (partial)`, never `none`"; concept D state handling "never prints 'inbox zero' while any message source is capped" | MET |
| IE4 | IE4 is met in V1 | §3 BLK-3 "A task blocked by two roots is counted once in the fleet total and marked `shared`"; §7.2 "Totals that mix current and last-good values are never added together" | MET |
| IE5 | IE5 is met in V1 | §13 OVF-5 "Paging coverage is distinct from overflow... Both can be non-zero at once" | MET |

## Variant V2
| Criterion | Claim | Evidence | Verdict |
|-----------|-------|----------|---------|
| CO1 | CO1 is met in V2 | §4 "Set name: the Five-Question Snapshot Set (5Q)", C1-C5; §6 default C1; §7 four states; §9 ET-1..10 and MC-1 "Every line 80 columns or fewer; only printable ASCII"; §10 limits | MET |
| CO2 | CO2 is met in V2 | §7.3 "FLEET       ? (unknown; unknown is not zero and not healthy)"; §8 risk per concept per state | MET |
| CO3 | CO3 is met in V2 | §5 "Gate load \| Low: needs FG-1 only for the count label \| ... \| High: dependency graph"; §12 FG-3 "Is a task dependency graph readable, and how complete is it?" | MET |
| CO4 | CO4 is met in V2 | §9 ET-1 "C1 at least 90% correct, median 15 s or less"; §9.3 decision rule | MET |
| CO5 | CO5 is met in V2 | §10 "Out of scope for this document. - Scheduling or posting..." | MET |
| CR1 | CR1 is met in V2 | §9 "None of these tasks has been run"; §1 tags [E]/[P]/[G] separate evidence from proposal; no runtime claims found | MET |
| CR2 | CR2 is met in V2 | §6 "It degrades gracefully. If the dependency graph is missing, the 'holds' ..." | MET |
| CR3 | CR3 is met in V2 | R-ROW, R-OVF, R-INT IDs defined in §2-§3 and reused verbatim in §5, §7, §8 ("R-INT-05") | MET |
| CR4 | CR4 is not met in V2 | §3 R-DEC-03 "Each decision row must meet R-ROW (id, question, requester, owner, age, impact, evidence reference)" vs §5 "C4 rows have no impact and no message reference, and C2 and C3 omit the message reference on some rows" | NOT MET |
| CR5 | CR5 is met in V2 | §3 Basis column "seed brief (SB) or REPORT.md section (RP n)", e.g. R-VER-04 "\| RP 3 \|"; §6 numbered rationale | MET |
| ST1 | ST1 is met in V2 | §1 purpose, §2 contract, §3 requirements, §4 concepts, §5 comparison, §6 default, §7-§8 states, §9 evaluation, §10 limits, §11 risks, §12 gates and next step | MET |
| ST2 | ST2 is met in V2 | §2.1-§2.6 and §7.1-§7.4 numbered children; no orphaned subsection found | MET |
| ST3 | ST3 is met in V2 | §2 "Shared Report Contract" kept apart from §3 requirements and §4 concept renderings | MET |
| ST4 | ST4 is met in V2 | Cross-refs "(section 12) (FG-1)", "section 5 lists the check"; §11 Requirement column links risks to requirement IDs | MET |
| ST5 | ST5 is met in V2 | Requirement tables with Basis (§3), comparison (§5), risks with likelihood (§11), open gates (§12) | MET |
| CL1 | CL1 is met in V2 | §7.2 "NOT AN ALL-CLEAR FOR: hosts not reported, transitions between samples..." | MET |
| CL2 | CL2 is met in V2 | §7.1 "+16 more observed, not shown (shown 3 + omitted 16 = 19*)" | MET |
| CL3 | CL3 is met in V2 | §1 Purpose/Scope; §4 each concept tied to one question, e.g. C3 "Which single answer unblocks the most work?" | MET |
| CL4 | CL4 is not met in V2 | SB/RP and [E]/[P]/[G] are defined, but §10 item 10 "Terminal ANSI colour" and FG-1 "API" are never defined; searched §1-§3, §10, §12 | NOT MET |
| CL5 | CL5 is met in V2 | §12.3 "Close FG-1 and FG-8 first... Then run the mechanical checks MC-1..MC-8" | MET |
| RK1 | RK1 is met in V2 | §11 header "\| ID \| Risk \| Likelihood / impact (judgment) \| Mitigation \| Requirement \|", RK-1 "High / High", 15 risks | MET |
| RK2 | RK2 is met in V2 | §11 Mitigation column filled for RK-1..RK-15 | MET |
| RK3 | RK3 is met in V2 | §7.3 "SINCE       NO VALID COMPARISON. Baseline kept at 08:55Z; 2 samples missed." | MET |
| RK4 | RK4 is met in V2 | §12 FG-3 "\| 'holds ?'; C3 not offered \|"; FG-2 "Verification lines show `?` or 'claim only'" | MET |
| RK5 | RK5 is met in V2 | §9 MC-1..MC-8 mechanical checks; §12.1 "A gate must be closed by verifying a source (not by assuming one)" | MET |
| IE1 | IE1 is met in V2 | Empty: §7.2 "Empty / healthy (nothing observed)"; single: §4 C1 "UNVERIFIED (claimed done, no independent check seen)  1: T-DEMO-02"; overflow: §7.1 "shown 3 + omitted 16 = 19*" | MET |
| IE2 | IE2 is met in V2 | §7.4 "NOT AN ALL-CLEAR: 2 tasks reported done are not verified done." (assignment source vs verification source) | MET |
| IE3 | IE3 is met in V2 | §3 R-VER-04 "A task reported complete with no independent verification must read 'unverified', counted apart from failing" | MET |
| IE4 | IE4 is met in V2 | §2.5 "Totals shown must equal shown rows plus omitted rows"; §2 "the group only shows the shared dependents once" | MET |
| IE5 | IE5 is met in V2 | §8 Busy row "CHANGED block capped first, CARRIED block capped second; both print shown + omitted = observed" | MET |

## Variant V3
| Criterion | Claim | Evidence | Verdict |
|-----------|-------|----------|---------|
| CO1 | CO1 is met in V3 | §1 "Complete five-concept set: A. Decision Brief; B. Run Ledger; C. Blocker Paths; D. Conversation Handoffs; E. Change Journal."; §10 default plus four states; §11 E01-E07; §12 limits | MET |
| CO2 | CO2 is met in V3 | §3 "Repeated tokens, invalid tokens, page errors or a collection deadline produce partial coverage." | MET |
| CO3 | CO3 is met in V3 | §7 "most demanding data prerequisite"; §12 G01 "This is the central feasibility gate" | MET |
| CO4 | CO4 is met in V3 | §11 E01 "At least 4 of 5 operators identify all four within 20 seconds" | MET |
| CO5 | CO5 is met in V3 | §12 limits "No API endpoint, durable decision store, overflow archive... is assumed to exist" | MET |
| CR1 | CR1 is met in V3 | §11 "No tests, collector calls, performance measurements or operator trials were performed for this design artifact." | MET |
| CR2 | CR2 is met in V3 | §10 "does not depend on a complete dependency graph or thread history to remain useful" | MET |
| CR3 | CR3 is met in V3 | §10 "W, M and V use the definitions from section 4"; §11 "define fixture-based checks for R01-R16" | MET |
| CR4 | CR4 is met in V3 | Checked §1 fixture against §3: "Cursor exhaustion alone does not prove a point-in-time census" agrees with §10 "decision census unknown"; no contradiction found in §1-§12 | MET |
| CR5 | CR5 is met in V3 | §10 "It puts the oldest blocking question in a fixed location, keeps unanswered context across quiet periods"; each concept has Strengths/Tradeoffs | MET |
| ST1 | ST1 is met in V3 | §1 purpose, §2 requirements, §3 contract, §4 rules, §5-§9 concepts, §10 default/states, §11 evaluation, §12 risks/limits/gates | MET |
| ST2 | ST2 is met in V3 | §10 four state subsections; §11 "Operator tasks" and "Future contract acceptance cases"; no orphan found | MET |
| ST3 | ST3 is met in V3 | §3 observation contract kept apart from §4 integrity rules and §5-§9 renderings | MET |
| ST4 | ST4 is met in V3 | Cross-refs §5 "specified in section 10"; §10 "W, M and V use the definitions from section 4" (no TOC, but cross-references present) | MET |
| ST5 | ST5 is met in V3 | §2 R01-R16 with acceptance conditions; §12 risks, limits, gates G01-G08 | MET |
| CL1 | CL1 is met in V3 | §4 rule 8 "Footer distinguishes `observed actionable items`, `shown`, `omitted from render` and `unobserved unknown`" | MET |
| CL2 | CL2 is met in V3 | §4 rule 7 "no more than six actionable item bundles and a target of 44 lines" | MET |
| CL3 | CL3 is met in V3 | §1 "These organize the entire report by priority, run ownership, dependency, dialogue and change respectively" | MET |
| CL4 | CL4 is not met in V3 | W/M/V are defined (§4), but "API" (§12) and "ANSI" (§11 "A transcript containing ANSI sequences") are never defined; searched §1-§4, §11, §12 | NOT MET |
| CL5 | CL5 is met in V3 | Closing "Decision for the next design review: evaluate Decision Brief with the synthetic tasks, while verifying G01..." | MET |
| RK1 | RK1 is not met in V3 | §12 risks header "\| Risk \| Consequence \| Required mitigation \|" gives consequence only, with no probability or likelihood; searched §12 | NOT MET |
| RK2 | RK2 is met in V3 | §12 "Required mitigation" column for every risk row | MET |
| RK3 | RK3 is met in V3 | §11 "A collection interruption cannot advance a source's last-success pointer. A rendering interruption cannot publish a half report" | MET |
| RK4 | RK4 is met in V3 | §12 G03 "Show completion claims and verification unavailable; do not invent check results or ready totals." | MET |
| RK5 | RK5 is met in V3 | §11 "Before implementation approval, define fixture-based checks for R01-R16"; "Any false all-clear in E02-E04 is a design blocker" | MET |
| IE1 | IE1 is met in V3 | Empty: §10 "Shown 0/0 observed actionable items"; single: §10 "Shown 1/1 observed actionable items"; overflow: §11 "Seven observed actionable bundles under a six-bundle budget account for one omitted bundle" | MET |
| IE2 | IE2 is met in V3 | §10 "Terminal exists; process liveness unknown; neither proves ready."; §2 R13 "workspace parentage does not become a dependency" | MET |
| IE3 | IE3 is met in V3 | §4 rule 1 "Future timestamps produce `clock conflict`, never negative waiting time"; §10 "If no successful history exists, print `No last-known records available`" | MET |
| IE4 | IE4 is met in V3 | §4 rule 6 "A task blocked by two questions contributes once to fleet impact"; §11 "Duplicate worker records do not inflate counts" | MET |
| IE5 | IE5 is met in V3 | §11 "A successful empty worker response plus failed message response never produces `all clear`."; §7 "multi-parent tasks must repeat with `also under <ID>` and count once" | MET |

## Summary
| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total /30 |
|---------|--------------|-------------|-----------|---------|------|-----------|-----------|
| V1 | 5 | 4 | 5 | 4 | 4 | 5 | 27 |
| V2 | 5 | 4 | 5 | 4 | 5 | 5 | 28 |
| V3 | 5 | 5 | 5 | 4 | 4 | 5 | 28 |
