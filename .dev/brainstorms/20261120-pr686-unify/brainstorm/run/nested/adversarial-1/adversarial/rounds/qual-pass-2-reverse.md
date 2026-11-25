# Qualitative evaluation, pass 2 of 2 (reverse order: V3, V2, V1)

Variants: V3 = variant-3-haiku-backend.md, V2 = variant-2-sonnet-analyzer.md, V1 = variant-1-opus-architect.md. Scored as written, before the debate. Code spot-checks were run in the snapshots (master, pr-a, pr-p) and the planb worktree.

## Completeness

| Criterion | V3 | V2 | V1 |
|---|---|---|---|
| C1 all Success Criteria | MET: Diagram, four labelled pieces, K1-K16, S0-S10, interface table with every listed item, ledger, owner actions, risks | MET: Diagram 2.0, four labelled pieces, K1-K17, S0-S20 with MC checks, numbered interface table, R1-R5 unproven items | MET: Section 2 diagram, four labelled pieces, K1-K15, S0-S14, interface table, OA-1 to OA-22, RK-1 to RK-17 |
| C2 edge cases and failures | MET: Section 8 crash tests: lost launch receipt, ack before state save, abandoned wake, stale lock | MET: M1/M2 ack and retarget; R15 stuck unknown entry stalls repo; 64 KiB wake test with 139-char names | MET: RK-12 abandoned wake, RK-13 crash between ack and state file, RK-14 branch lost on worktree removal |
| C3 dependencies and prerequisites | MET: Stage table Preconditions column, e.g. S5 needs "S1-S4, named editor, paired ack readers" | MET: Every stage lists Preconditions, e.g. S12 "S9, S11"; S20 needs Coder 515 and 516 | MET: Each stage names Preconditions, e.g. S9 "S2, S5, S7, S8; OA-2" |
| C4 completion criteria per stage | MET: Stage tests are "acceptance requirements"; merge gate M; go/no-go evidence names head, host, hashes | MET: Per-stage Tests plus MC-1 to MC-10; S20 needs all HIGH items proven or accepted | MET: Per-stage Tests and MC-1 to MC-7; S14 orders live-test gates before enable |
| C5 explicit out of scope | MET: "Increasing concurrency, Pipeline-field governed launches, label writes or a second host are separate future changes" | NOT MET: No spec-level out-of-scope list; only per-stage notes such as "Cap enforcement is not in this PR" | MET: "D16 has no VERDICT.md, so it is left out"; issue 409 stays a prototype; 689 deferred |
| **Subtotal (of 5)** | **5** | **4** | **5** |

## Correctness

| Criterion | V3 | V2 | V1 |
|---|---|---|---|
| R1 no factual errors (code spot-check) | MET: Checked cycle.py:1080-1112, orca_worktree.py:1515-1523, report.py:642-661, guard 785-799, plan_body.py:101-139, wake.py ack "taken"; all match | MET: Checked launch.py:33, record.py:34-35, guard 787-790, WC:244-246 match; _TOP_KEYS cite drifts (line 59), minor | MET: Checked predicates.py:14, models.py:103/131, WC-9 line 41, cycle.py:777-810 match; wake.py:47 cite for bucket "taken" is off |
| R2 feasible approaches | MET: Cron with flock, save-before-ack, F worker plus coordinator commit use built primitives; unproven parts marked UNVERIFIED | MET: Smallest-diff picks reuse built code (launch.py:33, status --json); R1-R5 name what stays unproven | MET: Coordinator-claims end state flagged unproven (RK-7) with fallback "poll keeps launching the claim" |
| R3 consistent terminology | MET: Defines AU, TUI, F; separates Coordinator worktree, coordinators branch, report coordinator; K ids named as contradictions only | NOT MET: "K12" is session name in section 3 but D05 master-push risk in item 2; "R9" is a risk row and a rule id | NOT MET: K12 is "close after merge" in section 3 but "unprotected master (K12)" in RK-2 and OA-5 |
| R4 no internal contradictions | MET: Cap 1, F binding, poll-claims and ack-means-received repeat consistently in sections 1-5 and 7; twelve verbs match | NOT MET: Section 7 says items 10+ gate S16-S20 but S8 needs item 10 (line 57 confirmation) | MET: start_mode claim/wake stated identically in section 1, 2.1, K1, S14 and OA-19 |
| R5 claims supported | MET: Each K row has reason and code cite, e.g. K2 cites launch-level-guard.sh:785-799 (verified) | MET: Every pick has reason and "what would reverse it", e.g. K2 and K8 with file:line | MET: Reason column per K, e.g. K2 cites guard 787-789 and WC:245 (verified) |
| **Subtotal (of 5)** | **5** | **3** | **4** |

## Structure

| Criterion | V3 | V2 | V1 |
|---|---|---|---|
| T1 logical ordering | MET: Summary, architecture, contradictions, interfaces, stages, ledger, owner actions, risks (sections 1-8) | MET: Same order, sections 1-8, reading guide first | MET: Same order, sections 1-8 |
| T2 consistent hierarchy | MET: ## sections, ### per piece, same four bold labels in each piece | MET: ## sections, ### 2.0-2.4, same four labels per piece | MET: ## sections, ### 2.1-2.4, same four bullets per piece |
| T3 separation of concerns | MET: Design, conflicts, interfaces, stages, ledger, decisions, risks in separate sections | MET: Distinct sections; MC checks defined once in section 5 and reused | MET: Distinct sections; MC checks named once and reused by stages |
| T4 navigation aids | MET: Ids S0-S10, K1-K16, gate M, section cross refs; interface and risk rows unnumbered | MET: Ids S, K, MC, R, row numbers, "Rows 20-23" refs; rows 4 and 22 missing so refs partly dangle | MET: Ids S, K, MC, OA, RK; owner actions grouped "Needed at S11 to S13" |
| T5 spec conventions | MET: Summary, architecture, contradictions, interfaces, stages, built ledger, owner actions, risks all present | MET: All eight required sections present | MET: All eight required sections present |
| **Subtotal (of 5)** | **5** | **5** | **5** |

## Clarity

| Criterion | V3 | V2 | V1 |
|---|---|---|---|
| L1 unambiguous language | NOT MET: Telegraphic fragments, e.g. "Both gates: S2 restoration." and "Neither: stop rollout." leave referents unclear | MET: Full sentences with named effects, e.g. item 3 "Both stay: S6 to S9 run as written" | MET: Each owner answer has a full-sentence effect, e.g. OA-1 "PR 682 stands under D03's three conditions" |
| L2 concrete not abstract | MET: Exact argv, paths and test names such as test_unknown_launch_no_second_claim | MET: Exact cron line, paths, test names such as test_ack_without_state_file_leaves_wake_entry | MET: Exact paths, schema names, tests such as test_wake_ack_m1.py |
| L3 one-sentence summarizable | MET: Each of sections 1-8 has one theme, e.g. section 6 is the built versus not built ledger | MET: Each section has one purpose; section 2 pieces open with a "What it is" sentence | MET: Each section has one purpose, e.g. section 6 ledger of built states |
| L4 acronyms defined, plain English | NOT MET: Defines TUI, AU, F only; MR-2, G2.1, R33, U25, T13, Rule B, IR7 stay undefined | NOT MET: Reading guide defines Poll, Dnn, O codes; U5, U25, R22, MR-2, INV-008 undefined for a non-expert | NOT MET: Defines Dnn, planb, F; U28, U30, U8, U54, C-INV-3, MR-2 left unexplained |
| L5 actionable decision points | MET: Section 7 lists ten decision groups with yes/no consequences, e.g. "Rules no: HIGH risk" | MET: Section 7 lists 18 owner decisions, each saying which stages it gates | MET: OA-1 to OA-22 grouped by stage needed, each answer states its effect |
| **Subtotal (of 5)** | **3** | **4** | **4** |

## Risk coverage

| Criterion | V3 | V2 | V1 |
|---|---|---|---|
| K1 at least 3 risks with likelihood and impact | NOT MET: One severity (HIGH/MEDIUM) per row; no separate likelihood | NOT MET: One severity per row; likelihood and impact given for one risk only (item 2, K12) | NOT MET: One severity (H/M/L) per row; no likelihood column |
| K2 mitigation for each risk | MET: Column "Required test and safe failure" gives a safe failure per row, e.g. "malformed state blocks, never resets" | NOT MET: Rows R3, R7, R8, R11 give only a proving test, no mitigation | NOT MET: RK-3 "None fully proves it"; RK-4 and RK-8 list tests only |
| K3 failure modes and recovery | MET: Outbox replay once, retarget with new wake id, startup reconciles outbox; per-stage Rollback column | MET: S20 rollback via DISABLED file or cron removal; reset N for stuck unknown (R15); per-stage rollback | MET: S14 rollback "DISABLED, enabled false, start_mode claim"; RK-12 new wake id recovery; per-stage rollback |
| K4 external dependencies and failures | MET: Outside-Run mailbox, unreadable process list, Coder image cron, "failed read is unknown, not empty" | MET: R2 mailbox, R3 tui-idle, R4 cron in image, R11 assumed GitHub and Orca fixtures | MET: RK-5 cron and Coordinator worktree, RK-8 Orca transport unknowns, RK-16 missing Project field |
| K5 monitoring or validation | MET: Watcher status JSON, audit.jsonl, shadow timer, observer watcher panel; evidence names head and host | MET: status --json recent_skips, AU1-AU8 audit, S20 24-hour shadow run, MC-10 reasons pin | MET: status --all holds with reasons, audit AU1-AU8, S14 24-hour dry-run poll |
| **Subtotal (of 5)** | **4** | **3** | **3** |

## Invariant and edge case coverage

| Criterion | V3 | V2 | V1 |
|---|---|---|---|
| I1 collection boundaries | MET: "Empty folder, zero rows and failed read differ"; cap 1; 64 KiB wake limit; empty grants default | MET: Empty folder, zero rows, could not read as three states; cap 1; 139-char names fit 64 KiB test | MET: Three distinct empty states; status --all with three repos, one unreadable; absent max_in_flight reads 1 |
| I2 state interactions across components | MET: Rule B ack versus state file; "never acquire watcher and coordinator locks in opposite orders" | MET: M1 ack after state file; R9 claim agent and coordinator in one worktree; K17 cap-state vocabulary | MET: M1 ordering (RK-13); waiting_reapproval outside cap, rechecked by poll (K15) |
| I3 guard condition gaps | MET: Rejects symlinks, oversize JSON, schema mismatch; unreadable process list means unknown; weakening refused | MET: C-INV-3 fail closed (empty reviewers, bad reach_daily_max); blind process table starts nothing | MET: Fail closed on empty reviewers and merge_safety_files; RK-10 admits hook misses shell writes |
| I4 count divergence | MET: test_concurrent_cap_one: waits excluded, unknown counted; restart tries persisted; duplicate wake returns existing state | MET: K17 counted-state set; store entry plus claim file "counts once"; three unknown do not block forever | NOT MET: No rule for which states count toward max_in_flight or duplicate counting; only waiting_reapproval excluded |
| I5 interaction effects | MET: "Green 686 alone does not prove the combined tree"; claim session versus standing Coordinator worktree (K9) | MET: R6 revert plus PR 686 breaks --help; R24 merge path safe only as one unit; R9 | MET: RK-6 revert plus 686 order; RK-9 F worker versus self-committing skill; RK-11 shared worktree |
| **Subtotal (of 5)** | **5** | **5** | **4** |

## Totals

| Dimension | V3 | V2 | V1 |
|---|---|---|---|
| Completeness | 5 | 4 | 5 |
| Correctness | 5 | 3 | 4 |
| Structure | 5 | 5 | 5 |
| Clarity | 3 | 4 | 4 |
| Risk coverage | 4 | 3 | 3 |
| Invariant and edge cases | 5 | 5 | 4 |
| **Total (of 30)** | **27** | **24** | **25** |

## Edge-case floor

Dimension I score: V3 5 of 5, V2 5 of 5, V1 4 of 5. All three are at or above the floor of 1 of 5, so none is ineligible as base.
