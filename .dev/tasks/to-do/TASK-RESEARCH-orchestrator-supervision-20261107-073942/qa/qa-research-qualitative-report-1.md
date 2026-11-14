# QA Report — Research Qualitative Review (Partition 1 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339): research depth for a read-only, coordinator-only `/sc:sweep` and a WC-14 coordinator-loop rule
**Date:** 2026-11-07
**Phase:** research-qualitative (adapted from report-qualitative; the research files are the document under review)
**Fix cycle:** N/A
**Fix authorization:** false (no research file edited)
**Assigned files:** `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/05-orca-row-schema.md`
**Input only:** `research/research-notes.md`

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: FAIL

## Items Reviewed

Checks 1-12 are the report-qualitative checklist adapted to research files; checks 13-17 are the five dimensions the task prompt names. No check is N/A.

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement matches findings (adapted: each file answers its assigned question for sweep/WC-14 design) | PASS | S1 maps contract rules that bind a sweep (items 1-15) and gaps G1-G7 with WC-14 insertion points (scope-01 :79-86); S2 maps Orca fields, rules and failure modes (scope-02 :80-109); 05 answers its five row-schema questions (05 :163-176). All stay on topic. |
| 2 | Current state is current | PASS (with notes) | 05 records 1.4.237 vs 1.4.245 staleness of the inventory (05 :194). S2 still cites inventory `[G]` line numbers that 05 shows have moved (MINOR, issue 8). Captures re-read: `lc17-show-1.json:128-166`, `lc16-show-4.json:128-186` match the shapes both files describe. |
| 3 | Options are distinct (adapted: the class definitions are distinct and non-overlapping) | FAIL | 05's mapping (05 :171-176) has overlapping classes and no precedence: a settled row with `terminalState` retained is both "finished" and "idle"; a settled row never sent to worker-show has `agentWait` absent and is also "could not determine". Issue 4. |
| 4 | Recommendation follows from analysis (adapted: derived classifier follows from the cited rules) | FAIL | S2 :172 says Orca shows `blocked` and `failed` both as outcome `failed` and the YAML must be read, yet S2's own mapping at :102 and 05 :171 classify any outcome `failed` as "finished". Issue 2. |
| 5 | Implementation plan actionable (adapted: could a designer write the classifier from these files) | FAIL | Two different "idle" definitions and two different "safe to close" objects (terminal vs worktree) across the partition; a designer would have to pick. Issues 3, 5. |
| 6 | Gaps are honest | PASS | S1 open questions (7), S2 open questions (9), 05 gaps 1-9 (05 :182-190); derived mappings tagged UNVERIFIED (S2 :97, 05 :167). |
| 7 | External research relevant (adapted: Orca help/guide sources inform the design) | PASS | Guide/help quotes drive the liveness, stall and agentWait rules; checked against `orca-capabilities.md:122-130` (read this session). |
| 8 | Scale claims substantiated | PASS (with note) | 05 (5) states N worker-show calls for N workers and a narrowing strategy, and tags the narrowing UNVERIFIED (05 :165). Batching-policy interaction unresolved (MINOR, issue 10). |
| 9 | Risk assessment complete | FAIL | The transcript stall proof misfires on a fenced worker (WC-12) and on a live worker mid-turn; no file states this risk. Issue 1. |
| 10 | Evidence trail complete | PASS (with notes) | Spot-checked citations: `WORKER-CONTRACT.md:45,58,60,108,122-129,133-136` all say what S1/S2 claim (read this session); `lc17-show-1.json:132` `activity` "working" after settlement confirmed; `:152-160` nextAction, `:161-166` attention confirmed (S2 cites `:153-165`, MINOR issue 7). |
| 11 | No circular reasoning | PASS | Classifier mappings are labelled as derivations, not cited as sources (S2 :97; 05 :167). |
| 12 | Conclusion proportionate | PASS (with note) | Mappings are tagged UNVERIFIED/derived; but S2 :151 calls `parse_session_log.py` "directly useful" for the stall proof without the qualifiers in issue 1. |
| 13 | Each class decidable from real evidence (waiting on a person, working, stalled (proved), could not determine, finished, idle) | FAIL | "waiting on a person" via pending coordinator `ask` (WC-3) or `worker_status: blocked` has no read path in S2's mapping (S2 :100); "idle" is undefined in S1/S2 and defined inconsistently with the notes in 05. Issues 2, 3, 6. |
| 14 | Safe-to-close as a separate dimension | FAIL | S2 :103 treats it as a fifth class defined only by `reclaimable` + `release`, omitting the five refusal conditions (`WORKER-CONTRACT.md:108`) and the freeze (`:133-136`) that S1 items 9 and 11 (scope-01 :64, :66) require; 05 does not cover it. Issue 5. |
| 15 | Respects WC-10 | PASS | S1 item 5 (scope-01 :60), S2 :101 and :90, 05 :175 all route `unverifiable` and late heartbeats to "could not determine", never "stalled". Matches `WORKER-CONTRACT.md:45`. |
| 16 | Says what a stall proof requires | FAIL | All three quote the guide's three proofs (S2 :86, :101; 05 :46, :174) but none says how a reader decides a transcript turn is *final*, nor excludes WC-12 fenced workers. Issue 1. |
| 17 | Avoids building on A4; names unknowns | PASS | S2 :234 marks A4's basis CODE-CONTRADICTED and builds nothing on it; S1 and 05 do not use it. Unknowns listed per check 6. |

## Summary

- Checks passed: 10 / 17 (four with notes)
- Checks failed: 7
- Critical issues: 0
- Important issues: 6
- Minor issues: 5
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | scope-02 :86, :101, :151; 05 :46, :174; scope-01 :62 | The stall proof "a transcript whose final agent turn sent no `worker_done`" is used as a classifier rule with no definition of *final*. A live worker mid-turn, or between turns, also has a last turn without `worker_done`; reading it as "stalled" turns absence into proof of death, which WC-10 (`WORKER-CONTRACT.md:45`) forbids. A WC-12 fenced worker (`WORKER-CONTRACT.md:60`: "stops without sending `worker_done`") matches the rule exactly; S1 :62 warns about fenced workers but S2/05 do not exclude them, so the files contradict. S2 :151 calls `parse_session_log.py` "directly useful" for this proof though the parser cannot tell final from latest. | State in S2 (and mirror in 05) that the transcript proof counts only when the turn is shown final by independent evidence (for example `exited` liveness or a process-exit observation, or Orca reporting the proof itself), that a fenced dispatch (`consumer_fenced`) is classified separately and never as stalled, and that a latest-turn read without such evidence is "could not determine". Qualify the S2 :151 reuse verdict accordingly. |
| 2 | IMPORTANT | scope-02 :102 vs :172; 05 :171 | Internal contradiction: S2 :172 says Orca reports `blocked` (waiting on a person/coordinator) and `failed` both as outcome `failed`, so the YAML must be read; S2's own mapping (:102) and 05 (:171) classify every outcome `failed` as "finished". A blocked worker would be reported finished, hiding a question a person must answer. "Finished" also ignores the admission rules at `WORKER-CONTRACT.md:122-129` (partial needs a read; guard refusal has no contract). | Make "finished" require outcome settled AND a read `return-contract.yaml` with `worker_status` succeeded/partial/failed; route `blocked` (and an `/sc:implement` freeze) to "waiting on a person"; route a missing contract on a non-guard failure to "could not determine". |
| 3 | IMPORTANT | 05 :176 vs research-notes :191; scope-01, scope-02 (absent) | "Idle" has two incompatible definitions: 05 says "settled and `resource.terminalState` retained or released" (an Orca worker); the notes say "person-started session with no Orca Task and no transcript activity inside the window". S1 and S2 do not define idle at all; S1 G6 (scope-01 :83) leaves person-started sessions open. | Pick one definition (the notes' version fits G6) and state it in S2 or 05 with its evidence source (session log mtime, absence of a Dispatch), and rename 05's state (for example "finished, terminal kept"). |
| 4 | IMPORTANT | 05 :169-176 | The mapping table has overlapping rows and no precedence: a settled row with `terminalState` retained matches "finished" and "idle"; a settled row that 05 (5) says needs no worker-show (:165) has `agentWait` absent, which :175 maps to "could not determine". A classifier built from this table gives two answers for the same row. | Add an explicit evaluation order (for example stall proof, then settled+contract, then agentWait, then live/in_progress, else could not determine) and state that `agentWait` absence matters only for unsettled rows. |
| 5 | IMPORTANT | scope-02 :103, :230 vs scope-01 :64, :66 | Safe-to-close is defined as a class by S2 (`reclaimable` + `nextAction release`), not the separate dimension the design needs, and it refers to a different object: S2 means releasing the Orca terminal, S1 means removing a worktree/branch, which needs all five refusal conditions (`WORKER-CONTRACT.md:108`) and is barred under a freeze (`:133-136`). 05 does not address the dimension. A reader cannot tell what "safe to close" licenses. | State in S2 that safe-to-close is a second dimension computed per row alongside the class; split it into "terminal releasable" (`reclaimable` + `release`, after the result is read) and "worktree removable" (all five `:108` conditions false, no freeze), both printed as REVIEW only. |
| 6 | IMPORTANT | scope-02 :100; 05 :172 | "Waiting on a person" has a read path only for `agentWait` (a human prompt seen by worker-show). The other cases have none: a worker blocked in a coordinator `ask` (WC-3, which sends no heartbeat, `WORKER-CONTRACT.md:57`), a `blocked` contract, a frozen implement plan (scope-01 :66) and a foreign ready Task (`:129`). S2 lists "an `ask` pending" with no source field or command; the partition defers this to research file 06, outside the assigned set. | Name the read-only source for each case (the message/`ask` listing verb and its field, the contract YAML, the ledger freeze test) or list each as an explicit open question with its consequence (sweep reports "could not determine" instead). |
| 7 | MINOR | scope-02 :87 | Cites attention/nextAction as `lc17-show-1.json:153-165`; the capture has `nextAction` at 152-160 and `attention` at 161-166 (05 :131 is correct). | Change to `:152-166`. |
| 8 | MINOR | scope-02 :82-94 | Cites `orca-capabilities.md` `[G]` line numbers from the 1.4.237 guide; 05 :194 shows they are off for 1.4.245 (for example liveness layering 62-64, not 61-63). | Add a note that `[G]` line numbers are 1.4.237 and point to 05's current numbers. |
| 9 | MINOR | 05 :174 | Source column says "row" for "other positive proof", but the transcript proof is not on the row; it needs `worker-read` or the session log. | Change the source to "row (exited) / worker-read or transcript". |
| 10 | MINOR | 05 :165; scope-02 open questions | N worker-show calls per sweep is not reconciled with the Bash inspection batching policy or a per-sweep call bound. | Note the call budget and whether the calls run in parallel or via one batch. |
| 11 | MINOR | scope-02, 05 (no window text); scope-01 :138 | The 6 h vs 72 h window (notes :195, :278) is not discussed in any assigned file except as F11 in S1's re-mapping. | Add one line in S2 stating which evidence the window bounds (activity only, not open Tasks or unread reports). |

## Actions Taken

- None. Fix authorization is false; no research file and no task file was edited. Only this report was written.
- No Orca, ccsession, sweep or close command was run; no Bash call was made.

## Confidence Gate

- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 13 | Grep: 4 | Glob: 1 | Bash: 0 (Read count includes the three assigned files and the notes read in full before a context compaction, reconstructed from the session summary; after compaction: `WORKER-CONTRACT.md:1-160`, `orca-capabilities.md:105-134`, `lc16-show-4.json`, `lc17-show-1.json`, scope-02 :80-109, 05 :163-200, and the report itself)
- No web research was performed; no Tavily or WebFetch call was needed (all sources are local).
- Tool calls (18) exceed checklist items (17).
- Limitation: the "Verified" judgement for checks 1, 6, 11 and 17 rests partly on full reads made before compaction; the citations used in Issues 1-11 were re-checked after compaction by Grep or Read.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` was provided in the spawn prompt, so nothing was relied on; standalone behaviour applied.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Outcome `failed` hides `blocked` -- verified by Read `WORKER-CONTRACT.md:58` (WC-5: `failed` or `blocked` → `--outcome failed`) against scope-02 :102 and 05 :171 (Grep), giving issue 2.
- Fenced worker ends without `worker_done` -- verified by Read `WORKER-CONTRACT.md:60` (WC-12) against the stall proof at scope-02 :86/:101 and 05 :46/:174 (Grep), giving issue 1.
- Safe-to-close object mismatch -- verified by Read `WORKER-CONTRACT.md:107-108`, `:133-136` and `orca-capabilities.md:108-109` (release closes only the terminal) against scope-02 :103, giving issue 5.
- `stage.activity` "working" after settlement -- verified by Read `lc17-show-1.json:128-134` (settled, outcome failed, activity working); confirms the S2 :74 and 05 :132 claim.
- Attention/nextAction line numbers -- verified by Read `lc17-show-1.json:152-166`, giving issue 7.
- "Idle" definitions -- verified by Grep of research-notes :191 vs 05 :176 and absence in scope-01/scope-02, giving issue 3.

**Answers to the mandatory questions:** about 20 factual claims were checked against source (the contract, the Orca inventory and two captures). Files read are listed above. Issues were found, so the zero-issue question does not apply. No web research was done.

## Recommendations

- Fix issues 1-6 in the research files (or in a follow-up research note that the synthesis must cite) before the report synthesizes a classifier or WC-14 text.
- The orchestrator should merge this report with partition 2, which holds research file 06 (the `ask`/message read path that issue 6 needs).
- MINOR issues 7-11 are notes and need no re-check.

## Verdict: FAIL


