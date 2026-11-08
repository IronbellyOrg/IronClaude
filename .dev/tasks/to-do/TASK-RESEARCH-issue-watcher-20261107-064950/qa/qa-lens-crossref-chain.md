# QA Report: crossref-chain lens

**Status:** Complete
**Date:** 2026-11-07
**Phase:** report-lens-crossref-chain
**Fix cycle:** N/A
**Fix authorization:** false (report only)

## crossref-chain QA Report

Report reviewed: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md` (2,167 lines by `wc -l`; adversarial minimum N = 2167/100 = 21)
Lens: crossref-chain
Date: 2026-11-07

### Traced chains (each link read in the report; line numbers are the report's current lines)

**Chain (i): security question, "securely tie each workspace to a GitHub account"**

| Link | Where | Result |
|---|---|---|
| 1 Issue question | Section 1 table row 2 (line 120): tie = the workspace's own `gh` login; owner = login unverifiable [UNVERIFIED] (R03 Gaps 14, GQ #19) | present |
| 2 Evidence, Section 2 | 2.1 "Which login assigns" (lines 202-206, `@me`, `gh api user -q .login`); 2.4 "Security properties" row Authentication (line 490) | present |
| 3 Evidence, Section 5 | 5.8 external-auth row (line 838: owner identity not guaranteed), 5.10 `create-task-action` (855), 5.14 chain row (922) | present |
| 4 Gap, Section 4 | G4 (line 686), G18 (700); G14 for the readable token file (696) | present |
| 5 Options, Section 6 | 6.0 R7 (1021), 6.1 Q-a (1109), 6.2 Q-a (1163), 6.3 Q-a (1207), 6.4 Q-a (1249), Requirement Scoring R7 row (1267), Options Comparison "account binding" (1300) | present; 6.2/6.3 depend on the OIDC/lettering text that finding 1 flags |
| 6 Recommendation, Section 7 | 7.3 "Identity" row (1359), 7.7 (1412) | present, but the 7.3 table has no row for the audit/at-most-once/containment properties of the same security table (finding 18) |
| 7 Plan, Section 8 | Phase 4 step 4.2 `whoami` (1635), Phase 5 algorithm #2 (1659), Phase 5 test "GitHub failure" (1709); open question Q16 (1863) | present; the audit line omits the login (finding 20) |
| Verdict on chain | Intact end to end; weakened by findings 1, 18 and 20 | |

**Chain (ii): listener question, "what is the Coder-side listener"**

| Link | Where | Result |
|---|---|---|
| 1 Issue question | Section 1 table row 3 (line 121): under A the 5-minute poller is the whole listener; host unverified | present |
| 2 Evidence, Section 2 | 2.1 never-as-worker / plain-process paragraph (line 231); 2.5 row "Coder listener / registration" (528) | present |
| 3 Evidence, Section 5 | 5.7 (lines 819-829 `coder_script` cron, persistence, autostop), 5.8 (835), 5.13 to 5.15 (alternatives) | present |
| 4 Gap, Section 4 | G19 (line 701), G18 (700) | present |
| 5 Options, Section 6 | 6.1 Q-b (1110), 6.2 Q-b (1164), 6.3 Q-b (1208), 6.4 Q-b (1250), Requirement Scoring R8 (1268), Options Comparison "Inbound exposure" (1302) | present |
| 6 Recommendation, Section 7 | 7.1 (1334), 7.7 (1412), 7.9 item 7 (1428) | present |
| 7 Plan, Section 8 | 8.1 "does not build" (1473-1474), Phase 7 step 7.5 scheduler text (1742), follow-up rows (1783, 1785), `once` verb and lock (steps 5.1, 5.3); open question Q15 (1862) | present; the Coder-repo scheduler wiring has no tracking reference (observation only) |
| Verdict on chain | Intact | |

**Chain (iii): session launch, "how a prompt reaches a new top-level session running `/sc:issue --claim <N>`"**

| Link | Where | Result |
|---|---|---|
| 1 Issue question | Section 1 (lines 115, 124); claim is explicit-only (2.1 table, line 161) | present |
| 2 Evidence, Section 2 | 2.2 entry-point table (244-250), `orca agent launch` contract (267-283), mock contract (287), prompt contract (289-294), launch environment (296-299) | present |
| 3 Evidence, Section 5 | 5.9 (845-849 `claude -p`, `--bare`), 5.11 (868-872 prompt injection) | present |
| 4 Gap, Section 4 | G3 (685), G12 (694), G15 (697), G20 (702), G21 (703), G25 (707), G14 (696) | present |
| 5 Options, Section 6 | 6.0 shared facts (1032-1043), 6.1 steps 6-8 (1069-1071) and launch-route variant (1113), Requirement Scoring R6 (1266) | present |
| 6 Recommendation, Section 7 | 7.3 "Prompt (Q3)" (1360), 7.5 route table (1386-1391) | present (decision label collides, finding 4) |
| 7 Plan, Section 8 | Phase 3 steps 3.2 to 3.6 (1589-1593), Phase 5 algorithm #11-#12 (1668-1669), Phase 6 step 6.2 (1726), 7.6 live-test items 1-3 (1743); open questions Q1 to Q3, Q5, Q6, Q17 (1848-1864) | present; SC-4 wording differs from step 3.2 (finding 19); Q5/Q13/Q18 resolutions have no plan step (finding 8) |
| Verdict on chain | Intact; weakened by findings 4, 8, 19 | |

**Chain (f): ADDENDUM conformance (owner decision A, claim-only, integer-only; ADDENDUM 2 in `research/research-notes.md` lines 108-112; Coder#477 sibling)**

| Link | Where | Result |
|---|---|---|
| 1 Owner decision stated | Section 1.1 table Q1/Q2/Q3 plus repo-side deliverable (lines 129-139); Section 3 legend (583), 3.3 (645-646), 3.4 (653-662); 9.1 D1 to D6 (1829-1840) | present; identifiers collide with open questions (finding 4) |
| 2 Scored against the issue's requirements | Section 6.0 R1 to R10 (1013-1024; R1 to R4 from the issue summary, R5 to R9 from the issue summary and Coder#477), Requirement Scoring for A, B, C and the hybrid D (1259-1270), tally (1274-1279) re-counted from the cells: A 2 Meets / 8 Partly, B 1 / 9, C 0 / 10, D 2 / 8, all matching | present and arithmetically consistent |
| 3 Recommendation labelled "decided by the owner" | 7.1 first line (1334) "Option A ... decided by the owner (ADDENDUM 2)"; 6.1 heading (1056) | present |
| 4 Implemented | 8.4 D1 to D3 (1517-1521), 8.1 (1469-1476), Phases 1 to 7 | present |
| 5 IronbellyOrg/Coder#477 as sibling dependency (repo boundary, filed assuming push design, unnecessary under A unless B or C is revisited) | Section 1.2 (141-147), 2.5 row (528), 3.4 (660), Section 4 G18 (700) and 4.5 (747), 5.13 to 5.15 scope notes, 7.7 (1410-1412), Section 8 follow-up (1783) and step 1.2 (1533), 9.1 D5 (1839) | present in Sections 4, 7, 8 and 9 |
| 6 Integer-only rule in Section 3 constraints, Section 7 security model and a Section 8 validation step | 3.3 (646), 3.2 SC-4 to SC-6; 7.3 "Prompt (Q3)" (1360); Phase 3 steps 3.2 and 3.6 (1589, 1593), 6.4 criterion 2 (1728), Integration Checklist (1815) | present; wording of the rule differs between Sections 3/7 and 8 (finding 19) |
| Verdict on chain | No missing item and no broken link in the ADDENDUM chain itself; the findings against it are label collision (4), SC-4 wording (19) and SC-5/SC-13 (5) | |

### Checklist results

| Item | Result | Basis |
|---|---|---|
| a. every Section 4 gap has a resolution step (Section 8) or open question (Section 9) | PASS by content, FAIL on explicit traceability for G15's "own basis" requirement | all 30 gaps mapped (finding 12 lists the mapping); G15 sub-requirement orphaned (finding 6); G23 only partly met (finding 20) |
| b. every Section 6 option references evidence from Section 2 or Section 5 | PASS by content, weak by key | Section 6 cites research files (R01/W01/W02), not Section 2/5 subsection numbers; the cited W01/W02 items were found in Section 5 (5.1 to 5.15) and R01/R02/R03 items in Section 2; the lettering conflict (finding 1) breaks the 5.13 to 6.2/6.3 link |
| c. every Section 7 recommendation traces to the Section 6 comparison | PASS with one exception | 7.1/7.2 trace to the Requirement Scoring and Options Comparison; the 7.4 candidate-1 recommendation traces to 4.3, not Section 6 (finding 22) |
| d. every Section 2 and 3 finding that warrants action appears in Section 4 or Section 8 | FAIL (findings 5, 6, 9) | G15 "own basis", ClickUp identity vs `gh` login, minimum `gh` scopes; SC-5 and SC-13 are not met by the plan as written |

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT | 5.1 (line 763 "alternative C-lite"), 5.13 (line 894 and comparison table line 904 "option C"), unresolved marker at line 908; vs 6.0 contradiction 1, 6.3 Cons, Requirement Scoring R8, 9.3 C10 | Link break Section 5 to Section 6. Section 5 still uses the web files' letters: an Action is "C-lite" / "option C", and "GitHub OIDC fits C (an Action calls the listener), not B". Section 6 (binding naming: B = Action + listener, C = central microservice) says the opposite: OIDC fits B, "OIDC does not fit a non-Action sender" for C (6.3 Cons, R8 cell). Same statement, opposite conclusion, left "as written" with a `[CONTRADICTION ... Both versions presented for QA resolution]` marker inside the final report. 6.0 contradiction 1 and 9.3 C10 give a mapping rule, but the Section 4.4 table ("Contradictions between research files") does not list it, and a reader of 5.13 who follows "fits C" into Section 6 lands on the wrong option. | Rewrite the letters in 5.1, 5.13 (OIDC row, comparison table "Fit" cell) to the binding naming (Action = B, microservice = C), delete the marker, and add the lettering conflict as a row of 4.4. |
| 2 | IMPORTANT | 5.15 revisit list (lines 953-965) vs Section 6 "Revisit conditions" (1308-1324), 7.8, 8 closing table (1792-1804); unresolved marker at line 1326 | Two different nine-item lists. 5.15 #7 = event-time reaction, #8 = change history, #9 = shared at-most-once ledger, and has no "workspaces cannot run a recurring poller". Section 6/7.8/8 #7 = Status change at event time OR change history (merged), #8 = shared ledger, #9 = workspaces cannot run a recurring poller. Conditions 7 to 9 therefore name different things depending on the section; the G19 (poller host) to revisit-condition link exists only in the Section 6 list, while 5.16 and Section 5's own "nine conditions" sentence (line 967) point at the 5.15 list. Marker left in the report. | Make 5.15 point to the Section 6 list as the single authoritative table (or copy it verbatim), keep W02 J3 / W01 14.5 provenance in a note, delete the marker. |
| 3 | IMPORTANT | 2.3 (lines 334 and 336), 5.5 (line 807), Appendix A.1 item 5 (line 2003), unresolved marker at line 336 | Contradiction between sections about the same fact: 2.3 and A.1 say whether `gh issue list --json` exposes a native issue-type field is [UNVERIFIED]; 5.5 says the official manual lists issue type and project items and "closes part of Gaps #11". Marker "Both versions presented for QA resolution" remains; Section 4.4 and Section 9 (Q8 covers only the `projectItems` Status name, not issue type) do not resolve it. Low downstream impact (the plan never reads issue type), but contradictions are never minor (rule 6). | State once: issue type is listed by the manual [EXTERNAL-VERIFIED], `projectItems` schema [UNVERIFIED]; update 2.3 and A.1 item 5, delete the marker. |
| 4 | IMPORTANT | 1.1 (lines 135-137), 2.1 (line 182), 3 legend (583), 3.2 SC-15 (635), 7.1 (1334), 7.3 (1353, 1360), 7.6 (1404) vs 8 (1541, 1589, 1592, 1743) and 9.2 / 10 (1949, 1983) | Identifier collision breaks every cross-reference that uses "Q1 to Q3". In Sections 1, 2, 3 and 7 "Q1/Q2/Q3" are the owner decisions (option A, claim-only, integer-only). In Sections 8, 9.2 and 10 "Q1/Q2/Q3" are open questions (slash command, argv vs paste, `--retry-launch`). Section 9.1 renames the decisions D1 to D3, but Sections 1, 2, 3 and 7 were not updated. Concrete misreads: 7.3 "Claim-only (Q2)" reads as open question Q2 (argv vs paste); step 1.10 "Live test checklist: Q1, Q2, Q3" are open questions while 7.6 row says "binding decisions Q1 to Q3" (owner decisions); step 3.2 has to say "Q3 of the owner" to disambiguate. | Use D1 to D3 for the owner decisions everywhere (Sections 1, 2, 3, 7 included) and reserve Qn for Section 9.2. |
| 5 | IMPORTANT | 3.2 SC-5 (line 625) and SC-13 (line 633) vs 8 Phase 4 (lines 1620-1630, 1638) and Phase 6 step 6.2 | The Section 3 pass/fail criteria cannot be satisfied by the Section 8 design as written. SC-5: "gh calls never request title, body or comment text"; Phase 4 calls `gh api .../issues/<N>/comments` with a jq filter that reads `.body` (`marker-jq`), i.e. it does request comment text (Section 8 only says the text "never reaches the poller"). SC-13: "no write-shaped gh call (`comment`, `-X`, `--method`, `edit`)"; Phase 4 requires every `gh api` call to carry `--method GET`, and step 4.5 redefines write-shaped as `--method` other than GET and allows the `/comments` path token. A test written from SC-13 would fail every events and comments call. | Reword SC-5 to "no title, body or comment text reaches the poller or any prompt (comment bodies are consumed inside `gh --jq`)" and SC-13 to the token rule of step 4.5 (`--method` other than GET). |
| 6 | IMPORTANT | 2.1 (line 232), 2.4 (line 506), G15 (line 697 "the design must state its own basis"), 10 coverage row (line 1964), A.3 (line 2118) vs 8 Phase 1 (steps 1.1-1.10) and 9.2 Q21 | Orphaned gap. The finding that the Worker Contract has no category for a standing authorization by an approver's label, so "the design must state its own basis" for an automated trigger, has no plan step and no open question. Section 10 says "the policy gap is stated for the design doc review (Q21)" and A.3 says it is carried to "7.6 design doc, Binding decisions", but Q21's text (line 1868) covers only the never-as-worker reading and open tabs, step 1.6 (security model) and row 7.6 (design doc) do not mention it, and `grep "standing authori"` finds it only in Sections 2, 10 and Appendix A.3. | Add the policy gap to step 1.6 (design doc: state the basis for a label-triggered outward action) and to Q21 (or a new Q), then fix the Section 10 and A.3 pointers. |
| 7 | IMPORTANT | 8 Phase 1 steps 1.5, 1.8, 1.9 (lines 1536, 1539, 1540) | Wrong internal pointers in the design-doc build steps. 1.5 says "Filter table of Phase 4 step 4.3": the filter table is the Phase 4 preamble, step 4.3 is the selection-logic code. 1.8 says "contract table of Phase 3 step 3.2": the contract table is the Phase 3 preamble, step 3.2 is `build_claim_prompt`. 1.9 says "Error table (Scenario, Behavior) from Phase 5 step 5.2": no table with those columns exists in Phase 5 (step 5.2 is `CycleConfig`/`run_cycle`; the nearest content is the algorithm column "On failure or skip" and the exit-code table), so the design doc's error-handling section has no source table to copy. | Point 1.5 and 1.8 at the Phase 4 and Phase 3 preamble tables; for 1.9 either add a Scenario/Behavior table to Phase 5 or point at the algorithm table plus exit-code table. |
| 8 | IMPORTANT | 9.2 Q5 (line 1852), Q13 (1860), Q18 (1865) vs 8 step 1.10 (line 1541) and step 7.6 (line 1743) | Open-question resolutions that point at plan content that does not exist. Q5 (High impact) says "Per-host preflight checklist in the design doc": the word occurs only in Q5; no Phase 1 step or 7.6 checklist item builds it. Q13 says "measure one claim's duration in the live test" and Q18 says "Run one claim twice in the live test": neither is among the eight items of the 7.6 owner-run checklist. Step 1.10 also lists the live-test questions as "Q1, Q2, Q3, Q6, Q7, Q8, Q15", while 7.6 has eight items covering Q1, Q2, Q3, Q8, Q7, Q6, Q15 plus Q11 (comment author field name) and Q17 (worktree path), so step 1.10 omits two of the eight checks it is meant to copy into the design doc. | Add the preflight checklist (Orca runtime, tier picker IDs, `gh` auth, ClickUp variables) as a design-doc step, add "claim duration" and "claim re-run" items to 7.6, and make 1.10 reference 7.6 instead of repeating a shorter list. |
| 9 | IMPORTANT | Section 1 (line 112), Section 5 intro (line 753), Appendix A.1 items 21 (line 2019) | The report states that every [UNVERIFIED] item is carried to Section 9, which is false for two items that matter to option A. (a) A.1 item 21 "whether the ClickUp identity (personal token) and the `gh` login belong to the same person" is listed "Carried to Open Questions", but Section 9.2 has no row for it (Q5 mentions ClickUp variables only; the identity match bears on R7 binding). (b) 5.11 (line 872) "least privilege in the session (which `gh` scopes the claim needs is [UNVERIFIED])" appears in no open question and not in A.2 either. | Add one Section 9.2 row each (ClickUp identity vs `gh` login; minimum `gh` scopes the claim needs, which feeds Q6/Q12). |
| 10 | IMPORTANT | 5.12 (line 880), 5.15 (lines 934-935), 8 Phase 5 step 5.1 (line 1649) vs 10 coverage row (line 1981) | Contradiction on whether option A uses an idempotency key. 5.12 says "For option A the natural key is (repository, issue number, approval event id), derived from GitHub so any workspace computes the same key". Section 10 (line 1981) says the idempotency key "applies to the push designs only (closing table)". Section 8 keys the dispatch store by issue number alone (`dict[int, DispatchEntry]`); `approval_event_id` is stored but is not part of the key, and the plan never says why the 5.12 key was not adopted or rejected (a re-approval creates a new approval event on the same issue and is invisible to an issue-keyed record). | Decide in Section 8 and state it: either key the record by `(repo, issue, approval_event_id)` or record in 5.12/Phase 5 that A deliberately keys by issue (and the consequence for re-approval); align Section 10. |
| 11 | MINOR | 5.10, 5.13, 5.14 and 5.8 [UNVERIFIED] items vs 9.2 Q26 to Q29 | Several [UNVERIFIED] items that Section 5 says are carried to Section 9 are only in Appendix A.2 Q18 or nowhere: meaning of `field_added`/`field_removed` (5.1, line 763); GitHub OIDC key rotation (5.13); status of the older experimental Coder task endpoint (5.10, line 856); exact status codes for a bad Coder token (5.13, line 896); `CODER_DANGEROUS_ALLOW_PATH_APP_SHARING` (5.14, line 918). All are B/C or context only, so no plan impact. | Add them to Q26/Q29 or soften the Section 5 intro sentence. |
| 12 | MINOR | Section 4 (all G rows), Section 8, Section 9, A.2 | No gap-to-resolution crosswalk. Sections 8 and 9 never cite a G-number (the only `G` hits in Sections 8 and 9 are W02 section letters); the G to plan/OQ mapping exists only in Appendix A.2 "Where it matters" with local Q numbers that "do not match the Section 9 numbers", and the A.2 carried-items table names 19 of the 30 gaps. Verified by content that every G1 to G30 does have a step, an open question or a 9.3 correction (G1/G2/G12/G24 Phases 2 to 5; G4 Q16; G5 Q10/Q25; G6 Q4; G7/G8 Q13/Q14; G9 Phase 5 attempt cap; G10 Q7/Q24; G11 7.1/Q9; G13 Q12; G14 Q6; G15 Q21 (see 6); G16/G17/G27 C1/C2; G18 D5/step 1.2; G19 Q15/7.5; G20 Q1; G21 Q5; G22 marker check; G23 step 13 (see 20); G25 Q17; G26 C6; G28 C3/Q33; G29 C5; G30 C7), but only through the GAPS-number bridge. Section 4.5 also lists only G5 to G8, G10, G13, G14, G18, G19 as carried to Sections 6 and 7 although the scoring rows R7 (G4), R9 (G23) and R10 (G7/G8/G9) address others. | Add a G to Step/Q crosswalk table at the end of Section 9. |
| 13 | MINOR | Appendix A.3 GAPS row (line 2140) | States "All 24 rows" but enumerates "Rows 1 to 5, 7 to 17, 19 to 22 ... row 6 ... row 18", so rows 23 and 24 of `gaps-and-questions.md` are not accounted for in that row (they are covered elsewhere: row 23 by C5, row 24 by Q21). | Add rows 23 and 24 to the sentence. |
| 14 | MINOR | 7.9 (lines 1420-1436) | The 15 "[OPEN]" details carry only GAPS/W02 sources, not the Section 9.2 Q numbers that Section 8 uses (for example 7.9 #8 is Q1+Q2, #13 is Q18, #14 is Q17, #15 is Q11). A reader cannot move from 7.9 to the plan's `open: ... (Qn)` markers without redoing the mapping. | Add a "Section 9 row" column to 7.9. |
| 15 | MINOR | Section 1 table (line 117) vs Section 6.0 (line 1026) and all "Answers to the three issue questions" blocks | Section 1 lists the three questions asked by issue #331 as (1) microservice versus Action, (2) tie workspace to account, (3) what the Coder-side listener is. Section 6.0 defines "the three questions every option must answer (from the issue and Coder#477)" as Q-a binding, Q-b listener, Q-c stopped workspace, and the blocks are titled "Answers to the three issue questions". Q-c is not one of the issue's three questions and issue question (1) has no answer block of its own (it is answered by the comparison). Q-a/Q-b/Q-c also look like open-question labels. | Rename the blocks "Answers to the binding, listener and stopped-workspace questions" and map issue question (1) to the Options Comparison. |
| 16 | MINOR | Whole report | Citation notation collisions: the same file `gaps-and-questions.md` is cited as "GQ #n" (Sections 1, 2, A.1), "Gaps #n" (Sections 3 to 5) and "GAPS n" (Sections 6 to 9); "R03 Gaps 14" (research-file gap, Coder tie) and "Gaps #14" (unified file, approver allow-list) differ only by a `#`; research keys R01/R02/R03 collide visually with requirement IDs R1 to R10 (a cell citing "R10" in the R10 row source list also cites "R01 §10"); Sections 3 to 5 use "file 01"/"web-01" for the keys that Sections 6 to 8 write "R01"/"W01". All cross-references verified consistent in meaning (every "Gaps #n" and "R0x Gaps n" checked against the source files), but the scheme is error-prone. | Pick one key per source and state it once in the report header. |
| 17 | MINOR | Appendix A.2 (lines 2035-2053) | A.2 numbers its carried items Q1 to Q18 locally ("A.2 Q4" = Coder workspace facts, Section 9 Q4 = routing rule; A.2 Q1 to Q15 collide with Section 9 Q1 to Q15). Disclosed in the Appendix preamble (line 1989), but Section 5's intro tells the reader that [UNVERIFIED] facts are "carried to ... Appendix A.2", sending them to a list whose numbers mean something else than Section 9's. | Renumber A.2 as "A2-1..." or drop the numbers. |
| 18 | MINOR | 7.3 security model table (lines 1357-1363) vs 2.4 "Security properties: provided versus missing" (lines 488-496) | The Section 7 security model has rows for Identity, Prompt, Fields read, Approval and Launch only. Three of the six properties in the 2.4 table (at-most-once, auditability, containment) have no row in 7.3 (they are handled in 7.6 poller rules, step 5 audit record, and the 7.3 residual-risk paragraph). The security chain 2.4 to 7.3 is therefore incomplete as a table. | Add rows for at-most-once, audit record and containment to 7.3 with pointers to 7.6, step 5.2 #13 and Q6. |
| 19 | MINOR | 2.2 line 292, 3.2 SC-4 (line 624), 7.3 (line 1360) vs 8 step 3.2 (line 1589) | The integer-only rule is worded three ways. 2.2, SC-4 and 7.3 specify `"/sc:issue --claim " + str(int(number))` ("built from `int()` of the number field"); Section 8 step 3.2 explicitly refuses coercion (`type(number) is int`, rejects the string `"331"`) and calls itself "stricter than the str(int(number)) of R01 §13". The deviation is disclosed only inside step 3.2; Sections 3 and 7 still describe the weaker rule, so SC-4's test text and the implemented test list (which rejects `"331"`) differ. | Change SC-4 and 7.3 to the step 3.2 wording. |
| 20 | MINOR | G23 (line 705) vs 8 step 5.2 row 13 (line 1670) | G23 target is "A dispatch log with issue, login, approval event and outcome" (and the gap says nothing records "for which login ... and when"). The audit record of step 5.2 #13 lists `issue, decision, reason, approver, approval_event_id, operation_id, attempts` with no login and no timestamp (timestamps exist only in `DispatchEntry`, not in the audit line). | Add `own_login` and a UTC time to the audit record and to 6.4 criterion 2. |
| 21 | MINOR | 3.2 SC-12 (line 632) vs 8 test plan and 6.4 | SC-12 (plain process, never a worker Task) is stated as a "pass/fail test" and 3.2 claims every criterion is decidable by the mock test method, but no Section 8 test, guard or acceptance criterion verifies it (6.4 has ten criteria, none on it). It is only a statement in 8.2 and the design doc. | Mark SC-12 as a design-doc statement, or add an environment guard test (refuse to run when launched inside a Claude session). |
| 22 | MINOR | 4.3 (line 725) vs 6 Requirement Scoring R5 and 7.4 | 4.3 says it condenses the routing candidates "so Section 6 can score them"; Section 6 never scores the four candidates (R5 cells only list them and say the choice is open). The candidate-1 recommendation in 7.4 ("Which one the research supports") is made in Section 7 from 4.3 and R01/W01 directly, not from a Section 6 comparison, so checklist item (c) is met only through 4.3. | Either score the candidates in Section 6 (a small table) or change 4.3's sentence to "so Section 7.4 can compare them". |

### Summary

- Total findings: 22
- Critical: 0
- Important: 10 (findings 1 to 10; blocking)
- Minor: 12 (findings 11 to 22; notes)
- Checks passed: chains (i), (ii), (iii) and (f) are intact end to end (with the weaknesses listed); checklist (a) and (b) pass by content; (c) passes with one exception; (d) fails
- Axis lens status: not applicable (report-qualitative lens review, not task-qualitative)

Verdict: FAIL (10 important findings; minor findings listed as notes)

VERDICT: FAIL

Blocking items to fix before the report is delivered: unresolved `[CONTRADICTION]` markers and the conflicting option letters and revisit lists (1, 2, 3); the Q1 to Q3 identifier collision (4); SC-5 and SC-13 versus the Section 8 design (5); the orphaned "design must state its own basis" gap (6); the three wrong step pointers in Phase 1 (7); open-question resolutions that have no plan step (8); the false "all [UNVERIFIED] items carried to Section 9" claim for the ClickUp identity and `gh` scope items (9); the idempotency-key contradiction (10).

### Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` section was in the spawn prompt, so none was relied on; fallback to standalone behaviour (independent checking) applied.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Gap to plan/OQ mapping for all 30 Section 4 rows: verified by reading Sections 8 and 9 in full and `Grep` for `G<n>` tokens (only Appendix A.2 uses G ids; Sections 8 and 9 do not), then by mapping every row through the `Gaps #n` / `GAPS n` bridge to `gaps-and-questions.md` (24 rows, Read in full) and to Q1 to Q33 / C1 to C11.
- Every `Gaps #n`, `GAPS n`, `R03 Gaps n`, `R01 gaps n`, `W01 gaps n` pointer in Sections 4, 7, 9 and Appendix A cross-checked against the numbered lists in `gaps-and-questions.md`, `research/03-governance-and-security-surface.md` (lines 204-222), `research/02-github-surface-and-cli-patterns.md` (210-220), `research/01-claim-flow-and-session-launch.md` (256-277) and `research/web-01-github-events-projects-and-limits.md` (209-227): all matched in meaning.
- Revisit-condition lists compared item by item against `research/web-02-coder-claude-dispatch-and-security.md` J3 (6 items, lines 308-315) and `research/web-01-github-events-projects-and-limits.md` 14.5 (7 bullets, lines 175-183): confirmed the 5.15 list and the Section 6 list differ in conditions 7 to 9 (finding 2).
- Section 3.2 SC-1 to SC-17 each traced to a Section 8 step or test; SC-5, SC-12 and SC-13 failed the trace (findings 5 and 21).
- Q numbers used in Section 8 (Q1 to Q23) each checked against the Section 9.2 row text; step 7.6 items 1 to 8 checked against the Q rows and step 1.10 (finding 8).
- Requirement Scoring tally re-counted from the 40 cells (matches); Requirement R1 to R10 compared with `.dev/issues/331/issue-summary.md` "What the issue asks for" and with ADDENDUM 2 in `research/research-notes.md` (lines 99-112, Read).
- Phase 1 step pointers (1.4, 1.5, 1.8, 1.9, 1.10) checked against the actual Phase 3, 4, 5 and 6 contents (finding 7).
- Existence of `.dev/issues/331/issue-summary.md` and of the "CORRECTION (2026-11-07" line at `enrichment/codebase-context.md:21` confirmed by Glob and Grep.

**Confidence (Confidence Gate Protocol):** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checklist items a, b, c, d, e(i), e(ii), e(iii), f)

**Tool engagement:** Read: 30 | Grep: 8 | Glob: 2 | Bash: 2 (about 42 calls against 8 checklist items)

**Web research:** none performed; Tavily not needed (this lens is internal to the report and the task folder).

**If I told the user 0 issues, would they believe me?** Not applicable: 22 findings recorded, minimum was 21 (2,167 lines / 100).

## QA Complete

