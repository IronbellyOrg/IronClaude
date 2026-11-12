# QA Report: R3-B2 evidence-quality lens (task-integrity / design-fix gate)

**Topic:** R3-B2 (several scoped Dispatch rows match one pane session), DESIGN `docs/designs/orchestrator-mode.md` after items 3.1 to 3.4
**Date:** 2026-11-09 (session date from env context; the task package dates itself 2026-11-08)
**Phase:** design-fix gate, evidence-quality lens (`fix_authorization: false`)
**Fix cycle:** 1 (first review of this gate)
**DESIGN size at review time:** 1026 lines (build-time sizing said 1013; the 500-1500 row still applies)

## Inputs read (all in chunks of at most 150 lines)

- DESIGN lines 1-36, 490-519, 740-745, 870-903, 965-1026, plus targeted greps over the whole file for every Orca-behaviour term.
- research/04 lines 110-185 (section 3 is lines 134-176; section 3.2 is 142-144, section 3.6 is 172-176).
- research/09 lines 139-208 (Gap 4 and Gap 5).
- `phase-outputs/test-results/r3-b2-mechanical.md` (117 lines).
- Primary source behind research/04 section 3.2: the Orca bundle `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js`, read at the byte offsets research/04 cites.
- `docs/designs/orchestrator-mode-review-3.md` line 137 (note m11).

## Inventory: every Orca-behaviour claim the R3-B2 text makes

The R3-B2 text is: the added sentences in the 7.2 worker bullet (DESIGN:498), the seven fixtures in the `test_classify.py` row (DESIGN:743), the additions to the FR-010, D9 and SP-29 rows (DESIGN:768, 819, 857), the revision-log row (DESIGN:1026) and the review-status bullet (DESIGN:10).

| # | Claim in DESIGN | Where | research/04 evidence | Status in 04 section 3.6 | DESIGN states it as |
|---|---|---|---|---|---|
| 1 | Several rows can match one tab-map entry through "a reused pane" | DESIGN:498 | 04:142-143: insert `$nt` @1629395 refuses a new row only while another row with the same `assignee_handle` or `assignee_pane_key` is `pending` or `dispatched`, so sequential rows on one pane are allowed | Not listed (static) | Possibility ("can match"). Supported. I read the guards in the bundle and they say exactly this |
| 2 | ... through "a retry" | DESIGN:498 | 04:143 cites `retryOfDispatchId` @1422174, which is only a mapped field name | 04:176 lists "Whether a retry (`retryOfDispatchId`) reuses its pane" as UNVERIFIED | Fact, with no UNVERIFIED tag. Over-stated (F1) |
| 3 | ... through "two rows on one terminal handle" | DESIGN:498 | 04:142 (same `assignee_handle` guard, sequential rows) and 04:144 (worker-start insert `ert` @1630462 has no pane-key guard) | 04:175 lists "Whether the worker-start path can leave two `pending` or `dispatched` rows on one pane in practice" as UNVERIFIED | Possibility. The sequential case is statically supported; the overlapping case is not asserted in 7.2. Acceptable (see M1) |
| 4 | Which `worker-show` value is `session_join` | DESIGN:497, 889, 973, 994 | 04:174 | UNVERIFIED (open item 22, capture item 13) | Not asserted. 497 says the field "is decided from the step 1.0a capture" and the path-B rule covers `file_name` or `terminal_handle`, which covers all three candidates. Supported |
| 5 | Dispatch refusing a second active row | not in DESIGN | 04:142 | n/a | Not stated anywhere in DESIGN (grep for `refus`, `second active`, `two active` found only unrelated hits). No over-statement |
| 6 | Worker-start rows | not in DESIGN | 04:144 | UNVERIFIED (04:175) | Not stated anywhere in DESIGN (grep for `worker-start` finds only the forbidden-verb list at DESIGN:550) |
| 7 | Fixture inputs: `pending` and `dispatched` rows with a start time and no end, on one pane | DESIGN:743 fixtures 2 and 3 | Bundle `ert` inserts `status 'pending'` with `dispatched_at datetime('now')` (read at @1630462), so a `pending` row with a start time is consistent | n/a | Test inputs, not reachability claims. No over-statement |

## Findings

### F1 (MAJOR): "a retry" is stated as a cause of several rows on one pane, but research/04 marks it UNVERIFIED

- **Evidence.**
  - `docs/designs/orchestrator-mode.md:498`: "Several scoped Dispatch rows can match one tab-map entry by path B (a reused pane, a retry, or two rows on one terminal handle)."
  - `research/04-design-fixes-r3.md:176`: "Whether a retry (`retryOfDispatchId`) reuses its pane." is listed under "3.6 UNVERIFIED until step 1.0a".
  - The only evidence for "a retry" is `research/04-design-fixes-r3.md:143`, which cites `retryOfDispatchId` @1422174. I read that offset in the bundle: it is the output mapping `retryOfDispatchId:e.retry_of_dispatch_id`, a field name. It says nothing about which pane a retry row gets.
  - The only insert that carries `retry_of_dispatch_id` is `ert` @1630462. It sets no `assignee_handle` or `assignee_pane_key`; those are filled later by the `UPDATE dispatch_contexts SET assignee_handle = ?, assignee_pane_key = ?` at @1840874. So the static bundle gives no reason to think a retry lands on its predecessor's pane.
  - research/04 contradicts itself: 04:143 offers the retry as an example, 04:176 says it is unverified. The DESIGN copied the 04:143 side and dropped the 04:176 caveat.
  - Nothing in DESIGN section 15.1 (capture items 1-13, lines 884-898) or section 17 (items 1-23, lines 971-995) records "does a retry reuse its pane" as unverified, so the reader has no marker and no closing step.
- **What is wrong.** A claim that research/04 section 3.6 marks UNVERIFIED is written into DESIGN as a fact about Orca. The lens rule says this must not happen.
- **Smallest fix.** In DESIGN:498 change "(a reused pane, a retry, or two rows on one terminal handle)" to "(a reused pane or two rows on one terminal handle)". The rule does not depend on the retry case, so nothing else changes and the open-item total stays 23. If the author wants to keep the retry, the alternative is to write "a retry, if it reuses its pane (UNVERIFIED until step 1.0a)" and add that clause to open item 22; this keeps the total at 23 but touches section 17.

## Minor notes (never fail the gate)

- **M1 (MINOR). Two UNVERIFIED items from 04 section 3.6 have no closing step in DESIGN.** Items 2 and 3 of 04:175-176 (worker-start rows leaving two active rows on a pane; retry pane reuse) appear in neither section 15.1 nor section 17. Only item 1 (the `session_join` value) is covered (capture item 13, open items 1 and 22). Today DESIGN states only the supported part of item 2 (sequential rows on one handle), so nothing is over-stated; but the rule's "two windows hold it" branch (fixtures 2 and 3 at DESIGN:743) is justified in research/04:144 only by the worker-start path and by same-second rows, and DESIGN does not say so. Fix: add one clause to open item 22 or capture item 13 ("also whether the worker-start path can leave two active rows on one pane"). Keep the open-item total at 23.
- **M2 (MINOR). The mechanical report is weaker evidence than its "7 of 7 PASS" suggests.** `phase-outputs/test-results/r3-b2-mechanical.md:80-84` (Command 5) shows no captured output: the text "(no output expected; grep exit status 1 means no match)" is an expectation, not an observation. Lines 59-64 and 66-72 show grep output cut off mid-line, so they cannot show which literal each hit contains. The outcome-to-fixture table (lines 100-104) lists "Hits in 7.2 / Hits in 11" counts with no command that produced them. I re-ran the checks myself (see C9) and they hold, so the PASS results are right; the file just does not prove them. Fix: re-run with `grep -o` and paste real output, and add the counting commands.
- **M3 (MINOR). Internal label.** DESIGN:498 says "Several matching rows follow the R3-B2 rule below." R3-B2 is a review-finding id, defined only in section 18 and section 1; the sentence reads fine but points to a label rather than to the sentence that holds the rule. Wording only.

## Checks

Verification notes behind the table: C1 to C8 by Read and Grep on the DESIGN, research/04 and research/09 files plus the bundle slices (offsets @1629395, @1629880, @1630400, @1422000, @1840800 read with `tail -c` and `head -c`); C9 by re-running the mechanical commands.

| ID | Check | Result |
|---|---|---|
| C1 | Every Orca-behaviour claim in the R3-B2 text was listed (7.2 additions, fixtures, FR-010/D9/SP-29 rows, revision log, review-status bullet) | PASS |
| C2 | Dispatch refusing a second active row: not asserted in DESIGN; the guard exists in the bundle as 04:142 says (`$nt` @1629395, handle guard @1629916 area, pane-key guard @1630095 area) | PASS |
| C3 | Retries: no claim in DESIGN may rest on a point 04 marks UNVERIFIED (04:176) | FAIL (F1) |
| C4 | Worker-start rows: not asserted in DESIGN; no over-statement of 04:175 | PASS |
| C5 | Which value is `session_join`: DESIGN does not pin one (DESIGN:497, 889, 973, 994) and the path-B rule covers all three candidates of 04:174 | PASS |
| C6 | "A reused pane" and "two rows on one terminal handle" (sequential case) are supported by static evidence I read in the bundle | PASS |
| C7 | research/04 section 3.2 static evidence reproduces in the bundle (`$nt` guards on `assignee_handle` and `assignee_pane_key`; `ert` has no guard and sets no pane; `retryOfDispatchId` is a mapped field; handle update at @1840874) | PASS |
| C8 | Each item in 04 section 3.6 has a visible UNVERIFIED marker or closing step in DESIGN 15.1 or 17 | FAIL (item 1 covered; items 2 and 3 not; see M1; F1 for the retry) |
| C9 | Mechanical report claims reproduce: em-dash count 0; no `TODO`/`TBD` (grep exit 1); `Total: 9 deviations.` at 821; `Total: 23 open items.` at 997; `exactly one window holding it` on the D9 (819) and SP-29 (857) lines; `several rows matching one pane session` on the FR-010 line (768); the `conflict: one pane session matches several Dispatch rows` literal appears once in 7.2 (498), once in section 11 (743) and once in the log (1026) | PASS |
| C10 | The mechanical report itself carries observed output for each check | FAIL (M2, minor) |
| C11 | The FR-010, D9 and SP-29 edits (768, 819, 857) add no Orca-behaviour claim beyond 7.2 | PASS |
| C12 | Fixtures (743) state inputs only and assert no reachability or Orca behaviour beyond the evidence | PASS |
| C13 | The section 18 R3-B2 row (1026) matches research/04 section 3.3 edit 5 word for word, and m11 (review 3, line 137) is the note the 7.2 note-order sentence settles | PASS |
| C14 | research/09 Gap 4 gate for R3-B2 ("each outcome has a fixture in section 11") holds: one window holds, two or more hold, none holds each map to a named fixture at DESIGN:743 | PASS |
| C15 | Self-audit: I can point to the exact sentence (DESIGN:498), the exact research lines (04:143, 04:176) and the bundle offsets for the one defect, and I looked for the other three lens terms (refusal, worker-start, `session_join` value) and found them either unstated or hedged | PASS |

## Summary

- Checks passed: 12 / 15
- Checks failed: 3 (C3 and C8 are tied to F1/M1; C10 is minor M2)
- BLOCKING findings: 0; MAJOR findings: 1 (F1); MINOR notes: 3 (M1 to M3)

## Confidence and tool engagement

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 2 | Glob: 0 | Bash: 3 (one of them a single batched read-only script over six bundle slices plus the m11 grep, per the batching policy). Read plus Grep plus Glob is 11, below the 15 checks, so I flag this per the minimum-engagement rule: C2, C7 and C9 were verified through the Bash calls and the other checks overlap on the same reads.
- **Limits:** Orca runtime behaviour was not observed; only the static 1.4.245 bundle was read. Whether a retry reuses its pane stays UNVERIFIED until step 1.0a. No web research was done.
- No file other than this report was written.

Verdict: FAIL

Blocking count: 1
