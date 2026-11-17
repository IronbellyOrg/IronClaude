## Anti-Omission Report (Gate 5, agent 2)

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md` (5,098 lines; read-only, not modified)
**Input files checked:** `research/06-reflect-two-engines.md`, `07-e1-evidence-grading.md`, `08-e2-evidence-grading.md`, `09-collaboration-designs.md`, `10-process-redesign.md`, `11-consumers-tasklist-workflow.md`, `web-03-git-branch-hierarchy-stacked-prs.md`, `web-04-finding-schemas-review-bots.md`, `synthesis/synth-04-external-findings.md`, `synth-09-sequence-and-gates.md`, `synth-10-questions-evidence.md`, and (moved to this agent by `qa/gate5-partition.md`) `research/21-value-ledger-brainstorms.md` and `research/20-value-ledger-e2-study.md`. **3,431 distinct findings enumerated** (enumeration file: `qa/qa-anti-omission-enumeration-2.md`).
**Date:** 2026-11-14
**Status:** Complete

Grading override read first (`qa/grading-override.md`): an omission is BLOCKING only if (1) leaving it out makes a decision, recommendation, value-inventory destination, conflict-log outcome or a number the recommendation rests on wrong or unsupported, (2) a required deliverable or section is missing, or (3) it is a security, data-loss or safety-boundary risk. Everything else is MINOR and carries `(minor under grading override)`.

### Method

1. Coverage was judged by meaning, never by id citation. For research files 06-11 and web-03 / web-04 I read every file completely, enumerated distinct findings, and for each searched the report with several key terms (Grep batches) and by reading the report sections that carry the material (2.1, 2.2, 2.3, 2.7, 5.3, 5.4, 6.7, 6.8, 7, 8.1, 8.2, 9, 10).
2. Synthesis files 04, 09 and 10: every substantive line was tested for a verbatim (whitespace-normalised) match in the report with a read-only script. Result: synth-04 386 of 389 substantive lines, synth-09 229 of 230, synth-10 253 of 257 match exactly; the 8 non-matching lines are the file title, the "Inputs:" line and the "Research question context" line of each preamble (not findings). Each of the 552 enumerated findings and rows of these three files was then located by exact line in the report (0 not found); the line numbers are in the enumeration file.
3. Ledgers 21 and 20 (as instructed): every row is a separate list entry (1,685 and 868). Counts recounted with read-only `grep -c '^| VL-21-'` = 1,685 and `grep -c '^| VL-20-'` = 868 (both equal the ledgers' rows and the figures in report 8.1.0). A read-only script parsed every ledger row and the matching row in Appendix A (`synthesis/synth-08-value-inventory.md`, 2,024,775 bytes, unchanged) and compared, row by row, Statement, Kind and Destination. The id was used only to locate the row; the match was on text. Result:
   - 2,553 of 2,553 rows are present in Appendix A with an identical Statement and Kind (0 statement or kind differences).
   - Destination equal to the ledger destination: ledger 21: 1,655 rows (of which 584 are ledger-DROP rows kept as DROP; with the 2 DROP duplicates below that is 586 DROP in all, equal to the 586 in 8.1.0); ledger 20: 847 rows (of which 298 are ledger-DROP rows kept as DROP; with the 12 DROP duplicates below that is 310 DROP in all, equal to 8.1.0).
   - Destination changed with a recorded reason in the row: ledger 21: 28 rows `moved from MODULE-tasklist` (to CORE) plus 2 `DROP[duplicate]: duplicate of ... was MODULE-tasklist`; ledger 20: 9 rows `moved from` plus 12 `DROP[duplicate]` rows (named kept row; 3 of those are the P3-014 duplicates). These counts (28 + 2, 9 + 3) equal the P3-014 table of 8.1.3. Rows with a changed destination and no recorded reason: 0.
   - Every `DROP[duplicate]` row names a kept row that exists in Appendix A; the kept row is non-DROP except VL-20-025 (kept DR-028, DROP "fixed in the harness", with the per-module category concern carried by DR-080 CORE) and VL-20-407 (kept DR-087, DROP "wording correction; the real defect is DR-002", DR-002 is CORE and carries "surface dropped counts and ids"); both are a recorded reason, and the substance is in the report (Section 6.12.7 rows DOC-5, B-6 at line 1477).
   - Every ledger row sits under the `### <DESTINATION>` heading equal to its Destination column (0 mismatches over the 2,553 rows).
4. Earlier-gate removals: I read `qa/qa-fix-log.md` (Gate 3 cycle 1: two additions, P6-001 and P6-002, nothing removed; minor findings untouched), `qa-fix-log-c2.md` ("Skipped"), `qa-fidelity-fix-log-c1.md` ("No fix required"), `qa-fidelity-fix-log-c2.md` ("Skipped"), and the four consolidated-findings files (phase6, phase6-c2, fidelity, fidelity-c2). No log records a claim removed as false or unsupported. So no finding is classified JUSTIFIED-REMOVED, and none of the omissions below is excused by a removal.

### Omissions Found

No omission is blocking. Details of 81 enumerated entries (of 326 hand-enumerated entries in files 06-11, web-03, web-04; 16 of the 81 are wholly absent, the rest are a missing sub-detail of an entry whose main substance is in the report) are not in the report text. Each is MINOR: none changes a decision, recommendation, value-inventory destination, conflict-log outcome or a number the recommendation rests on; none is a required section or a safety risk. Rows marked * are wholly absent from the report. "#" is the entry number in the enumeration file for that source.

| # | Source finding | Source file | Status | If deduped, by which report item; if JUSTIFIED-REMOVED, fix-log entry and code evidence | Severity |
|---|---|---|---|---|---|
| 06-3 | BLOCKED slugs other than contract-missing (timeout, child-crash, contract-version-missing, unknown-major-version, malformed-*) | 06-reflect-two-engines.md | OMITTED (detail) | report names the order and the 36-test matrix (186, 4432) | MINOR (minor under grading override) |
| 06-4 | The 14 DEGRADED trigger slugs, halt set, verification-skip exemptions, `promoting` effect | 06 | OMITTED (detail) | "halt and exemption sets" named at 4432 | MINOR (minor under grading override) |
| 06-5* | HALTED reasons and the PASS / tier-mismatch rule | 06 | OMITTED | none | MINOR (minor under grading override) |
| 06-11 | Engine A step-level data flow (preflight, passthrough, reduce, scorer child internals) | 06 | OMITTED (detail) | summary at 159, 201, 873, 892 | MINOR (minor under grading override) |
| 06-13* | verification_ran False / no-verification-stage is exempt even under --promote | 06 | OMITTED | none | MINOR (minor under grading override) |
| 06-15* | `reviewer-shortfall` token not in the halt set (2-of-3 stays PASS-eligible) | 06 | OMITTED | none | MINOR (minor under grading override) |
| 06-17 | Swarm docstring calls git-diff materialization a logged follow-up | 06 | OMITTED (detail) | tasklist-only input at 176, 2700 | MINOR (minor under grading override) |
| 06-19 | Names of the 10 contract keys outside the frozen lists | 06 | OMITTED (detail) | count 10 at 179, 2703 | MINOR (minor under grading override) |
| 06-20* | Probe variants (two same-vendor workers, one worker) | 06 | OMITTED | none | MINOR (minor under grading override) |
| 06-26 | Lint assertion map L0-L7 and rule B | 06 | OMITTED (detail) | L2, L7, bump rule cited at 197, 227, 2721 | MINOR (minor under grading override) |
| 06-27 | _ev1 pass 2 "loud fallback", ev1_failures use_manifest | 06 | OMITTED (detail) | regex and reviewers_resolved at 225, 1351 | MINOR (minor under grading override) |
| 06-36 | task-builder emits the wrapper only with CLI_MODE | 06 | OMITTED (detail) | tasklist callers at 157, 1278 | MINOR (minor under grading override) |
| 06-42 | config.py output default path, --output under .claude rejected, stub default ladder off | 06 | OMITTED (detail) | clamp and floor at 201 | MINOR (minor under grading override) |
| 06-47* | Engine B grounding chain (reuse-auditor use, reachability gate 5.6, required-capability pass 5.6a) absent from engine A | 06 | OMITTED | none | MINOR (minor under grading override) |
| 06-48 | Deviation precedence Regression > Drift > Necessary > Authorized, grounding-gaps artifact, modifier mapping | 06 | OMITTED (detail) | "4-class taxonomy" at 178 | MINOR (minor under grading override) |
| 06-49 | Rules D1-D5 of the shadow flag | 06 | OMITTED (detail) | flag semantics at 165-167 | MINOR (minor under grading override) |
| 06-51 | Skill null-convergence handling (status partial, halt-phase-for-review), 0.60 floor | 06 | OMITTED (detail) | 0.75 vs 0.80 at 192, 2767 | MINOR (minor under grading override) |
| 06-56 | Invented keys zero_drop_flag, memory_status, notes, run_started, run_finished | 06 | OMITTED (detail) | 7 of 28 at 227 | MINOR (minor under grading override) |
| 06-57 | Commit ids 9874d63fb and c2e3347d3 for the compliance fix | 06 | OMITTED (detail) | mean 0.704 at 215 | MINOR (minor under grading override) |
| 06-58 | Exit docstring "trivially equal" parity | 06 | OMITTED (detail) | L313 defect at 229 | MINOR (minor under grading override) |
| 06-64* | Additional deterministic logic in SKILL prose (Wave 7 gate, convergence routing, envelope validator, executor rotation, memory trim) as move-into-code candidates | 06 | OMITTED | "candidates only" in the source; core steps listed at 2749-2752 | MINOR (minor under grading override) |
| 07-2 | Per-run token min 93,616 (A3) and max 367,381 (E3) | 07-e1-evidence-grading.md | OMITTED (detail) | totals at 236 | MINOR (minor under grading override) |
| 07-10 | Pilot cluster figures (71 clusters, 19 multi-reviewer, 45%) | 07 | OMITTED (detail) | combo figures at 242 | MINOR (minor under grading override) |
| 07-15 | 689 findings with 0 per-finding calibration | 07 | OMITTED (detail) | 479/712 at 245 | MINOR (minor under grading override) |
| 07-16 | Strata of the 50-pair check | 07 | OMITTED (detail) | TP/FP/FN/TN at 244 | MINOR (minor under grading override) |
| 07-20* | E1-F19 troubleshoot report (three root causes, two prompt-only fixes) | 07 | OMITTED | none | MINOR (minor under grading override) |
| 07-21 | Replay "49 skipped" | 07 | OMITTED (detail) | 42 replayed, self-replay at 213 | MINOR (minor under grading override) |
| 07-22* | Stage 0a agreement 24/358 = 6.70% (rerun 6.33%) | 07 | OMITTED | conversion 67.28/63.38 at 245 | MINOR (minor under grading override) |
| 08-13 | three-way rows for sonnet+luna+ember and h2 | 08-e2-evidence-grading.md | OMITTED (detail) | sonnet+2x luna vs ember+2x luna at 311 | MINOR (minor under grading override) |
| 08-23 | j1 sensitivity table S0-S4 rows | 08 | OMITTED (detail) | named at 337 | MINOR (minor under grading override) |
| 08-32* | G9 surviving significant effects (second luna, ember+terra, 6 of 48 p<0.05) | 08 | OMITTED | exploratory; 48 tests at 779 | MINOR (minor under grading override) |
| 08-35* | G12 single-run leaders are anecdotes | 08 | OMITTED | none | MINOR (minor under grading override) |
| 08-36 | Audit span-null rows (46, 13 blocking) | 08 | OMITTED (detail) | chains, 1,398, 83 at 1368 | MINOR (minor under grading override) |
| 08-41 | Per-audit grade table A-F | 08 | OMITTED (detail) | summaries only A and D at 320 | MINOR (minor under grading override) |
| 09-4 | Transport tally over 25 proposals and the rejection table for Orca mail, A2A, cross-session messaging | 09-collaboration-designs.md | OMITTED in the body (substance is in Appendix A rows VL-21-054 to 057) | Appendix A (8.1.2) | MINOR (minor under grading override) |
| 09-8 | Hook lock placement differences | 09 | OMITTED (detail) | skeleton at 363 | MINOR (minor under grading override) |
| 09-9 | Parallel-call race found by smoke runs | 09 | OMITTED (detail) | shared skeleton at 363 | MINOR (minor under grading override) |
| 09-11 | parametrize marker counts | 09 | OMITTED (detail) | test counts at 370 | MINOR (minor under grading override) |
| 09-12 | r1 gate0 gate names | 09 | OMITTED (detail) | at 371 | MINOR (minor under grading override) |
| 09-13 | r2 smoke elapsed pairs | 09 | OMITTED (detail) | at 371, 373 | MINOR (minor under grading override) |
| 09-14 | r3 baseline variance remark | 09 | OMITTED (detail) | at 371 | MINOR (minor under grading override) |
| 09-15 | r4 "own gate says F7 should not run on 0/5 luna" | 09 | OMITTED (detail) | act rates at 371 | MINOR (minor under grading override) |
| 09-16 | r5 diagnostic chain sentence | 09 | OMITTED (detail) | at 372 | MINOR (minor under grading override) |
| 09-18 | Per-design requirement table | 09 | OMITTED (detail) | at 1081, 2344 | MINOR (minor under grading override) |
| 09-24 | Radar signatures M1/M2/M4/M7 are Bash patterns | 09 | OMITTED | none | MINOR (minor under grading override) |
| 09-28 | Three-implementation split of the exchange capability | 09 | OMITTED (detail) | optional exchange at 3492 | MINOR (minor under grading override) |
| 09-33 | H4 "list per module" | 09 | OMITTED (detail) | at 378 | MINOR (minor under grading override) |
| 09-34 | argv-diff test for the kill switch | 09 | OMITTED (detail) | kill switch at 1155 | MINOR (minor under grading override) |
| 09-39 | MR:396 and MR:909 kit statements | 09 | OMITTED (detail) | MR:917 at 382 | MINOR (minor under grading override) |
| 09-42 | MR line offset +6 note | 09 | OMITTED (detail) | none | MINOR (minor under grading override) |
| 10-2 | verify-citations reads coverage only to pass to parse_block | 10-process-redesign.md | OMITTED (detail) | at 396 | MINOR (minor under grading override) |
| 10-3 | findings-v2 constants other than LENSES, CHANNELS, REFLECT_CATEGORIES | 10 | OMITTED (detail) | at 2674 | MINOR (minor under grading override) |
| 10-7 | Two naming conventions (`<noun>-v<N>` vs `review-<noun>/<N>`) | 10 | OMITTED (detail) | at 2653, 3523 | MINOR (minor under grading override) |
| 10-10 | Wave 1B Pass 2 INF-NNN quote pinning, 0.6 threshold | 10 | OMITTED (detail) | at 396 | MINOR (minor under grading override) |
| 10-18 | Class card block kinds | 10 | OMITTED (detail) | fields at 2629 | MINOR (minor under grading override) |
| 10-19* | Anti-overfitting rules AO-1 to AO-8 | 10 | OMITTED | none | MINOR (minor under grading override) |
| 10-21 | Recipe Ledger row budgets and re-ask rules | 10 | OMITTED (detail) | at 2624-2627 | MINOR (minor under grading override) |
| 10-26 | Individual D1-D7 thresholds | 10 | OMITTED (detail) | D2 at 393 | MINOR (minor under grading override) |
| 10-29 | quote_other as a printed tool line | 10 | OMITTED (detail) | at 2640, 2655 | MINOR (minor under grading override) |
| 10-31 | Per-item decidability rows for C1-C8, X1-X7, G0, D1-D7 | 10 | OMITTED (detail) | summary at 400, 2633 | MINOR (minor under grading override) |
| 10-32 | The doubtful C6/C5 instance and the #346 file list | 10 | OMITTED (detail) | at 2633 | MINOR (minor under grading override) |
| 10-33* | C6 instances 8 of 12 are delivered docs | 10 | OMITTED | none | MINOR (minor under grading override) |
| 10-36 | Line-cite drift findings.py:15-22 | 10 | OMITTED (detail) | corrected statement at 402 | MINOR (minor under grading override) |
| 10-38 | Unit 9 table rows 15-19 individually | 10 | OMITTED (detail) | at 1310-1318 | MINOR (minor under grading override) |
| 10-40 | 0.914 x 0.914 = 0.835 product | 10 | OMITTED (detail) | 0.914 at 3512 | MINOR (minor under grading override) |
| 10-41 | Explicit M1-M10 to C1-C8 mapping | 10 | OMITTED (detail) | "each move lands in one class" at 391 | MINOR (minor under grading override) |
| 11-3* | Wave 4 pre-check file, Will / Will Not lines | 11-consumers-tasklist-workflow.md | OMITTED | none | MINOR (minor under grading override) |
| 11-7 | PatchChecklist, gate-results.txt names | 11 | OMITTED (detail) | T1-T5 at 668-672 | MINOR (minor under grading override) |
| 11-9* | Stage 10.5 writes the index column and reflect_pre_summary | 11 | OMITTED | none | MINOR (minor under grading override) |
| 11-11 | COMPLEXITY_SCORE terms, override, depth-map.yaml | 11 | OMITTED (detail) | mapping at 671 | MINOR (minor under grading override) |
| 11-13* | Outputs the panel must keep (index column, summary, directories) | 11 | OMITTED | key interface kept at 667 | MINOR (minor under grading override) |
| 11-18 | UC-1 partial cases (zero-task, validator unavailable, dropped citations) | 11 | OMITTED (detail) | none | MINOR (minor under grading override) |
| 11-19 | D1-D5 | 11 | OMITTED (detail) | at 671 | MINOR (minor under grading override) |
| 11-20 | commands/reflect.md does not document the flag | 11 | OMITTED (detail) | none | MINOR (minor under grading override) |
| 11-22 | Pool-exclusion detail (executor_exclusion_degraded, source values) | 11 | OMITTED (detail) | at 182 | MINOR (minor under grading override) |
| 11-23 | 25 fixtures, pass.yaml version | 11 | OMITTED (detail) | 36 and 10 tests at 1216 | MINOR (minor under grading override) |
| 11-24 | Per-trigger lines of the matrix | 11 | OMITTED (detail) | at 3757, 4432 | MINOR (minor under grading override) |
| 11-32 | troubleshoot refs and remediation-handoff readers | 11 | OMITTED (detail) | readers at 667 | MINOR (minor under grading override) |
| web03-3 | Hacker News source naming | web-03 | OMITTED (detail) | error text at 1821 | MINOR (minor under grading override) |
| web03-14 | pr-submit force-push remark | web-03 | OMITTED (detail) | at 1862 | MINOR (minor under grading override) |
| web04-22 | SARIF kind / suppression tables partly visible | web-04 | OMITTED (detail) | at 2036 | MINOR (minor under grading override) |

Rows listed: 81 (16 marked *, wholly absent). COVERED-BY-DEDUP (not omissions): 14 ledger rows whose destination changed to DROP with a named kept row recorded in the row: VL-21-131 (VL-22-017), VL-21-158 (DR-023), VL-20-025 (DR-028), VL-20-128 (DR-023), VL-20-241 (DR-086), VL-20-319 (DR-016), VL-20-407 (DR-087), VL-20-451 (DR-080), VL-20-643 and VL-20-644 (DR-091), VL-20-645 and VL-20-664 (DR-102), VL-20-651 (DR-104), VL-20-767 (DR-092); and web-04 enumeration entry 23 (Key findings 1-7 restate entries 1-16). JUSTIFIED-REMOVED: none.

Points checked that I looked at hard and found represented (not omissions): the numbers the recommendation rests on from these files (0.80 vs 0.75, 36 tests, 19 fields, 89 of 110, 8/13 EV-1, 7 of 28, 92/80/49 and 3 flips, 65 vs 38, 156 of 665, 13 of 20, the +59% kit cost, 36 conflicts 13/4/4/15, the 1,047/510 precheck figures, the 4 byte-identity limits), the composition decision of 06 section 8(d) (report 2.1, 6.8 option 4, 7), the H1/H2 unconditional and H3/H4 per-module verdicts of 09 (report 2.3, 1310, 3440), the owner decisions DO4, T-1..T-10 and S-0..S-5 (report 247, 718, 1293), the plugin-mirror and consumer-key interfaces of 11 (report 667, 699, 726), the whole of Sections 5.3 and 5.4 of the web files and the three synthesis files (verbatim carry).

### Per-File Counts

| File | distinct findings enumerated |
|---|---|
| research/06-reflect-two-engines.md | 69 |
| research/07-e1-evidence-grading.md | 38 |
| research/08-e2-evidence-grading.md | 46 |
| research/09-collaboration-designs.md | 42 |
| research/10-process-redesign.md | 43 |
| research/11-consumers-tasklist-workflow.md | 35 |
| research/web-03-git-branch-hierarchy-stacked-prs.md | 24 |
| research/web-04-finding-schemas-review-bots.md | 29 |
| synthesis/synth-04-external-findings.md | 145 |
| synthesis/synth-09-sequence-and-gates.md | 191 |
| synthesis/synth-10-questions-evidence.md | 216 |
| research/21-value-ledger-brainstorms.md (rows; `grep -c '^| VL-21-'` = 1,685) | 1,685 |
| research/20-value-ledger-e2-study.md (rows; `grep -c '^| VL-20-'` = 868) | 868 |
| **Total** | **3,431** |

(The `COUNT <file name>: <n>` lines of the enumeration file give the same numbers: `COUNT 21-value-ledger-brainstorms.md: 1685`, `COUNT 20-value-ledger-e2-study.md: 868`, and one line for each of the other eleven files.)

### Summary

- Findings enumerated: 3,431 (2,553 ledger rows; 326 findings of research 06-11 and web-03/04; 552 findings and rows of synth-04, 09, 10).
- Represented: 3,400 as to main substance (3,431 enumerated, less 16 wholly absent and 15 covered by dedup; of the 3,400, 65 lack a sub-detail, listed above), of which 2,539 ledger rows (plus the 14 deduplicated ledger rows) are confirmed by meaning against Appendix A (8.1.2 / Section 8.1: statement and kind identical, destination equal to the ledger's or a recorded `moved from` / `DROP[duplicate]` reason; 0 rows without a recorded reason; row counts 1,685 and 868 equal 8.1.0).
- Covered by dedup: 15 (14 ledger rows plus web-04 entry 23).
- Justified-removed: 0 (no earlier-gate fix log records a removal; Gate 3 cycle 1 only added text, the other logs say Skipped or No fix required).
- Omitted: 16 findings wholly absent from the report (all MINOR) plus 65 missing sub-details of otherwise represented findings (all MINOR); 0 CRITICAL or IMPORTANT by the information label either, since none was a distinct foundational or secondary finding that a recommendation depends on.
- Blocking omissions under the grading override: 0.
- **Verdict: PASS (0 blocking omissions).** Follow-up list for the owner: the 81 rows above, all `(minor under grading override)`.
