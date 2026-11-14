# QA Report - Research Gate (Partition 1 of 2: gaps, depth, integration, patterns, incremental writing)

**Topic:** Orchestrator mode Phase 1 (issue #339): read-only coordinator-only `/sc:sweep` + coordinator-loop rule (WC-14)
**Date:** 2026-11-07
**Phase:** research-gate (checklist items 6, 7, 8, 9, 10 only)
**Fix cycle:** N/A
**Fix authorization:** false (no research file edited)
**Assigned files:** `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/05-orca-row-schema.md`
**Input only:** `research/research-notes.md`
**Depth tier:** Deep

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

Pre-review sha256 of the assigned files (to prove no edit):

| File | sha256 |
|---|---|
| `research/scope-01-contract.md` | `5ed8391297b3e510e1ddf40c00b6f69eb91cf1e1abda4cca5fd7d8cde2b3c719` |
| `research/scope-02-orca-recovery.md` | `b8ceb020dd4f326f9c470a8ab50ade1c253905a3ca17a5cc24383da2fa48fd8d` |
| `research/05-orca-row-schema.md` | `8d444571770273da41de645d7836ffcd46a16591df0beaef22f38ca3ac765b3f` |
| `research/research-notes.md` | `4dc1ed929b008684a8ecb520e008fc85ce81ae2032722e057a791318f0482ba6` |

---

## Overall Verdict: FAIL

Four blocking (IMPORTANT) findings are open: one integration gap (item 8) and three classification errors. Each would carry a wrong statement into synthesis. No finding is CRITICAL. 05 answers part of G-A. What it leaves open is correctly tagged UNVERIFIED in 05 and is recorded here as a note (issue 6), so it does not block on its own.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 6 | Gap severity | FAIL | research-notes rates G-A and G-B Critical (lines 244-245, 306). 05 answers part of G-A: liveness values `live`/`unverifiable`/`exited`, paging (100 rows, `page.hasMore`, `page.nextCursor`), `agentWait` location (worker-show `observation` and `terminal`) and the per-call cost. Checked against the worker-list help (22 lines, flags at 9-16) and the worker-show help (16 lines), and against the lc16/lc17/lc01 show captures. Still unproven: the worker-list row schema, the shape of a non-null `agentWait`, and real `unverifiable`/`exited` payloads. 05 marks all three UNVERIFIED (its Gap 1), so G-A is not blocking for synthesis provided they go to Section 9. Gaps G1-G7 carry no severity anywhere: scope-01, research-notes and the task file all lack it (issue 9). 05 states "cannot detect waiting on a person from the list alone" as fact even though its own Gap 1 leaves it open (issue 4). |
| 7 | Depth (Deep tier) | PASS (note) | scope-02 traces one flow end to end: Orca worker-list/worker-show, then `projection` fields (16 confirmed in the lc16 capture), then the classifier, then the return contract. It also traces orca-tabs, then the transcript, then `parse_session_log`. The weak hop, C12 (the pane-key join), is now verified: the orca-tabs file `ec61f494-...+2844c731-...` matches the lc16 `assigneePaneKey` (`tabId:leafId`, with `:` replaced by `+`), and its handle `term_1a6fde09-...` matches the lc16 `assigneeHandle`. |
| 8 | Integration points | FAIL | Where WC-14 goes is verified. The WORKER-CONTRACT.md headings sit at 9/26/48/64/68/77/91/101/110/120/131/154/158/166, no WC-14 exists yet (grep), and the rule can go after `:156` and before `:158`, or after `:129` and before `:131`. How the sweep reads Orca state is incomplete. `orca orchestration --help` lists `run-list`, `run-current`, `run-show`, `task-list`, `gate-list` and `inbox`, and none of these appears in the three assigned files. So the sweep has no stated source of Run IDs, although `[G:recovery]` 28-29 says to always pass `--run`. Decision gates are not covered, and `task-list` is not covered (WC `:129` needs it) (issue 1). ccsession integration is covered: the orca-tabs join and sc-crash-recovery SAFE/REVIEW. |
| 9 | Pattern documentation | PASS | The crash-recovery conventions are recorded: SAFE/REVIEW labels, `unscanned:` markers, the "What I could not determine" section, and propose-never-execute. So are the contract conventions: RULE_PHRASES pinning, the never-as-worker list (`NEVER_AS_WORKER`, 8 entries; the test file has 41 tests), the ASCII rule, the repo-setup gate and the write-verb audit over `AUDIT_ROOTS` (skills, commands, agents). The HOW-WE-WORK 396-405 citations hold: the never-workers bullet is at 403, and the file ends at 405. |
| 10 | Incremental writing | PASS (note) | All three files show iterative work: re-verification annotations stacked on earlier claims, Key Takeaways per source, and the stale wrong command form annotated in scope-02 instead of rewritten. Superseded text is left in place (issue 12), which hurts readability but does not show that data was lost. |

## Summary

- Checks passed: 3 / 5 (items 7, 9, 10)
- Checks failed: 2 (items 6, 8)
- Critical issues: 0
- Important (blocking) issues: 4
- Minor issues (notes): 11
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | scope-02 (data sources), 05 (Answer 1 and the command list) | Integration gap. `run-list`, `run-current`, `task-list`, `gate-list` and `inbox` (all listed by `orca orchestration --help`) appear in none of the three files. As a result: (a) the sweep has no stated source of Run IDs, although `[G:recovery]` 28-29 says to always pass `--run` because an unscoped list buries live rows; (b) decision gates are never considered as a "waiting on a person" signal; (c) `task-list` is missing, and WORKER-CONTRACT `:129` needs it to find a ready Task this coordinator did not create and to check that every Task is settled. | A gap-fill pass must read the help for `run-list`, `run-current`, `task-list`, `gate-list` and `inbox` (read-only `--help` only), and record for each: what it returns, whether it is paged, and which sweep class it feeds. It must also say where the sweep gets Run IDs. |
| 2 | IMPORTANT | scope-02 :102; 05 classification table, "finished" row | Both files call every outcome `failed` finished. Under WC-5 a worker that returns `blocked` is also recorded as outcome `failed` (scope-02 :172 says so itself), so a blocked worker that is waiting on a person would be labelled finished and never shown to the person. | Make the class depend on the return contract. Outcome `failed` with a `blocked` return goes to the "needs the person" class, and only a `failed` with a non-blocked return is finished. Cite WC-5 and scope-02 :172. |
| 3 | IMPORTANT | scope-02 :103 and :230 | "Safe to close = reclaimable + nextAction release" treats a terminal `release` as permission to close the worktree. It leaves out the five refusal conditions at `WORKER-CONTRACT.md:108` and the frozen-plan rule, which scope-01 item 9 lists. | Redefine "safe to close" as: reclaimable, `nextAction` release, AND none of the `WORKER-CONTRACT.md:108` refusal conditions AND no frozen plan. Otherwise label it REVIEW, the sc-crash-recovery convention. |
| 4 | IMPORTANT | 05 Answer (1) and Summary | "A sweep cannot detect waiting on a person from the list alone" is stated as fact, but 05's own Gap 1 says it is unproven whether a worker-list row carries `observation` or `agentWait`. This is an assumption stated as a verified fact. | Restate it as UNVERIFIED and make the per-row `worker-show` call the conservative default until a row with a non-null `agentWait` is captured. |
| 5 | MINOR | 05 classification table, "idle" row | Defines idle as settled with `terminalState` retained or released. That conflicts with research-notes table C, where idle means a person-started session. Synthesis could merge two different classes. | Rename one term (for example "settled" for the 05 meaning) and keep "idle" for the person-started session only. |
| 6 | MINOR | 05 Gap 1; research-notes 244-245, 306 | G-A is only partly answered. Still open: the worker-list row schema, the shape of a non-null `agentWait`, and real `unverifiable`/`exited` payloads. These are tagged UNVERIFIED and can only be captured from a live stall. | Downgrade G-A from Critical. Send the three open points to Section 9 (Open Questions) with "capture a live stalled row" as the resolution. |
| 7 | MINOR | scope-01, G1 source | The G1 source is left UNVERIFIED, but the memory file `coordinator-never-stop-polling.md` (the owner order of 2026-11-05) is readable. | Mark G1's source verified and cite the memory file. |
| 8 | MINOR | scope-02 open question 5; research-notes C12 | The pane-key join is UNVERIFIED there, but it can be verified now: the lc16 `assigneePaneKey` matches the orca-tabs file `ec61f494-...+2844c731-...`, and the handle `term_1a6fde09-...` matches. | Mark C12 verified, citing the lc16 capture and the orca-tabs file. |
| 9 | MINOR | scope-01 (G1-G7), research-notes, task file | Scope gaps G1-G7 have no severity anywhere. Suggested ratings: G3 periodic sweep, G4 classification vocabulary and G1 keep polling are Critical for the design; G2 re-arm, G5 when to tell the person, G6 person-started sessions and G7 report location are Important. | Add a severity column to the G1-G7 list during synthesis. |
| 10 | MINOR | 05, citation of `[G:recovery]` lines 6-14 | Leaves out row 9 ("Start a replacement with `--retry-of`"), which conflicts with WC-6 (a retry is a new Task, never `--retry-of`). | Cite row 9 and record it as a guide/contract conflict that WC-6 settles. |
| 11 | MINOR [OUT-OF-SCOPE] | research-notes 158, 168-170 (table B) | Uses `orca-ide worker-list` / `worker-show` / `worker-read` without `orchestration`. Running the top-level form prints `Unknown command: worker-list` (checked in this review). scope-02 annotates the wrong form; the notes carry it forward, so synthesis could copy it. | In synthesis, use `orca-ide orchestration worker-list` (and the same for show and read). The notes are input only and are not edited here. |
| 12 | MINOR | scope-01 :99; scope-01 open question 5; scope-01 F1-F12 section | Superseded text stays in place: line 99 still says "UNVERIFIED in this slice" beside the re-verified fact; open question 5 is answered but still listed; the F1-F12 section is stale, because the analysis file has F1-F14 (`analyze-worker-contract.md:30-55`) and F13 is never mentioned. | Strike or annotate the superseded lines, and extend the findings list to F14. |
| 13 | MINOR | scope-02, lc17 citations | Line ranges are off by one: attention is at 161-166 (cited 162-165), and resource is at 145-151 (cited 145-150). The claims are true. | Correct the ranges. |
| 14 | MINOR | scope-01, test-file description | The test is named "all_seven", but `NEVER_AS_WORKER` has 8 entries. scope-01 does not record the mismatch. | Note it, so that WC-14 work does not rely on the test name. |
| 15 | MINOR | scope-01 sources | D1-D5 in APPROVED.md (the brainstorm decisions) were never read. | Read D1-D5 and confirm none conflicts with the WC-14 placement or the sweep classes. |

## Actions Taken

None. Fix authorization is false, and no research file was edited. The post-review sha256 of all four files is identical to the table above (re-hashed at the end of this review).

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 12 | Grep: 2 | Glob: 0 | Bash: 7 (read-only: help output, sha256, grep of research-notes; no state-changing Orca, ccsession, sweep or close command run)
- Unchecked items: none. Unverifiable items: none. The live payloads behind issue 6 cannot be captured without a stalled worker, but this is recorded as a research gap, not as an unchecked QA item.

## Recommendations

- Resolve issues 1-4 before synthesis. Issue 1 needs a short read-only gap-fill (orchestration `--help` for run-list, run-current, task-list, gate-list and inbox). Issues 2-4 are corrections that synthesis must apply, and the fix cycle must re-check them.
- Carry issues 6 and 9 into synthesis: G-A's residual goes to Section 9, and the G1-G7 severities go to the gap table.
- In synthesis, use only `orca-ide orchestration worker-*` command forms (issue 11).
- Merge this report with the partition 2 report, which covers checklist items 1-5, before deciding the gate.

## QA Complete

## Verdict: FAIL

