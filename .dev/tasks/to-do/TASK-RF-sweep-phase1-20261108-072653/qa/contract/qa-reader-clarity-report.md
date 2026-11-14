# QA Report: Reader-clarity lens (WC-16, never-as-worker line, developer-guide line)

**Reviewer:** rf-qa-qualitative (T270)
**Date:** 2026-11-12
**Fix authorization:** false

## Findings

Method: read on disk now (chunks of at most 150 lines) `src/superclaude/core/WORKER-CONTRACT.md` lines 1-30, 49-67, 95-160, 200-290; `git diff` of the contract, the test file and the guide; the guide at lines 978-1002; `src/superclaude/commands/sweep.md`; DESIGN `docs/designs/orchestrator-mode.md` lines 655-716; OQ-1, OQ-3, research/07 (a) to (e); the step 1.17, r7 and phase 12 records. I read WC-16 (contract line 277), line 23 and guide line 991 as a coordinator and as a worker new to the project, with no knowledge of the sweep project.

Verified true (no finding): WC-16 paragraph at contract:277 is byte-identical to the DESIGN section 8 fenced paragraph (`cmp` on my own re-run printed PARA_IDENTICAL); contract line 23 and guide line 991 list the same nine names in the same order; `uv run pytest tests/skills/test_worker_contract.py -q` gives 742 passed; ruff check and ruff format --check pass on the test file. The never-as-worker wording does make the guard (contract:20, case 3) refuse a `Command: /sc:sweep` line, so a coordinator that dispatches it by mistake is stopped.

## Findings

### F1. MAJOR. WC-16 says "every coordinator wake"; the sweep it builds on runs on "every wake or timeout"

Evidence: `WORKER-CONTRACT.md:277` "When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake, at most once every 5 minutes, the coordinator runs "The sweep." ... unchanged and, in the same pass, runs `/sc:sweep`". `WORKER-CONTRACT.md:110` "After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep". The contract itself separates a wake from a timeout (line 110, and the 300000 ms wait at line 101).

What is wrong: the sentence just before says an expired wait is re-armed, then the next sentence says the pass runs on a wake. A coordinator that reads "wake" as "a message arrived" skips `/sc:sweep` on a quiet timeout, which is exactly when all workers are silent and the read matters most. The word "unchanged" points back to line 110 but a reader has to notice that the two triggers differ. `sweep.md:20` and DESIGN R2 repeat "every wake", so the gap is in three places.

Smallest fix: WC-16 reads "On every coordinator wake or timeout, at most once every 5 minutes, ...". The pinned phrase "On every coordinator wake" (`tests/skills/test_worker_contract.py` WC-16 entry) stays a substring, so no pin changes. DESIGN section 8 and the step 1.17 byte-compare must change with it, and OQ-3 approved the text as written, so the owner must re-approve the edit.

### F2. MINOR. "Phase 1 adds this duty, not a scheduler" has no referent in the contract and collides with "P1"

Evidence: `WORKER-CONTRACT.md:277`. In the same file "P1" is the worker-conversion phase: `:16` "from P1", `:307` "From P1 the 16 commands converted in P1 do", `:308` "From P2 the 15 commands". "Phase 1" appears nowhere else in the contract (grep: only line 277). Its meaning (phase 1 of the sweep project, the label also used in `src/superclaude/cli/sweep/report.py:283`) is defined only in the design.

What is wrong: a reader of the installed `~/.claude/WORKER-CONTRACT.md` in another project reads "Phase 1" as the contract's own P1 and concludes the 16-command conversion added a coordinator loop, which is false. The same sentence pair is also tense: the paragraph says the coordinator "keeps that pass scheduled while work remains" and the next sentence says there is "not a scheduler", without saying that the 5-minute wait timeout (line 101) is the schedule.

Smallest fix: "The first release of `/sc:sweep` adds this duty only; no scheduler runs it. The coordinator's own wait timeout is the schedule." (Or drop the sentence.) Needs the same owner re-approval as F1.

### F3. MINOR. The `/sc:sweep` class sentence is ungrammatical and uses undefined shorthand

Evidence: `WORKER-CONTRACT.md:277` "only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine." and "do not count against the L1 cap".

What is wrong: "is could not determine" reads as a typo; `stalled` and `could not determine` are class names defined only in `sweep.md:14`, and the contract never lists the classes. "The L1 cap" is not a named term; the cap is the Cap column of the L1 row at `:151`. A new reader cannot tell which words are labels.

Smallest fix: put the two labels in code spans or quotes ("stalled", "could not determine") and say "the cap in the L1 row of the ladder table".

### F4. MINOR. "needing ownership review" is a dangling phrase in the escalation list

Evidence: `WORKER-CONTRACT.md:277` "... a ready Task it did not create, needing ownership review, a frozen plan, and a fan-in ...". Every other item maps to a contract line (`:244`, `:246`, `:250`, `:273`, `:242`/WC-6). "ownership review" appears nowhere else in the contract; it is the label of a sweep report section (`src/superclaude/cli/sweep/report.py:283`).

What is wrong: between commas it reads as a separate item with no subject, or as a modifier of the previous item; a reader cannot tell what needs review, by whom.

Smallest fix: "a ready Task it did not create (the report lists it as needing ownership review)".

### F5. MINOR. Nothing in the contract says a worker session never runs `/sc:sweep` itself

Evidence: `WORKER-CONTRACT.md:23` says "never dispatched as workers" and `:20` case 3 refuses a `Command:` line naming it; `:277` says "the coordinator runs `/sc:sweep`". The words "coordinator or person only" and "a dispatched worker never runs it" exist only in `sweep.md:16` and `:40`, which a worker does not read unless it loads the command.

What is wrong: a worker new to the project that wants to know what its peers are doing sees a read-only command named in the contract with no stated bar on its own use. The guard only checks the brief's `Command:` lines (`:16`), and WC-7/WC-13 do not name it. Effect is limited (it reads, and writes one report under `.dev/sweeps/`), which is why this is not blocking.

Smallest fix: add to WC-16 "Only the coordinator or the person runs `/sc:sweep`; a worker session never does." (Changes WC-16, so same owner re-approval as F1.)

### F6. MINOR. Guide bullet at line 992 does not explain why a read-only report command is on the list

Evidence: guide line 991 now lists `/sc:sweep`; line 992 still gives only "orchestration, a conversation with a human, or an outward action that must be authorized" as the reasons, attributed "Per the rollout plan". `/sc:sweep` is neither a conversation nor an outward action, and the guide never says it is the coordinator's own read tool. Contract line 23 ("coordinator-only command set") carries the real reason.

Smallest fix: one clause at line 992: "or, like `/sc:sweep`, the coordinator's own read of its Run".

### F7. MINOR. WC-16 gives no flag and no failure path for `/sc:sweep`

Evidence: `WORKER-CONTRACT.md:277` "runs `/sc:sweep` and reads its report before it acts"; `sweep.md:35` says with no bound Run and no `--run <id>` the command exits asking for one.

What is wrong: "its report" has no stated location, and if the command exits with an error there is no report to read; the paragraph does not say whether the coordinator then waits, retries or carries on. A coordinator told "it never stops watching" could still read "before it acts" as a block.

Smallest fix: "reads its report before it acts; if `/sc:sweep` fails, the coordinator notes the failure in its run notes and carries on with the unchanged sweep."

### Sentences that are clear (checked, no finding)

"`/sc:sweep` is an added read: it does not replace that sweep, it is not a second pass, and it does not update heartbeat records or run the `worktree ps --agent-wait` listing" and "`/sc:sweep` recommends nothing: no stop, retry, release, merge or removal" are unambiguous and consistent with `:110` and `:151`. "A missing heartbeat is absence, never death" matches WC-10 (`:46`). "The `/sc:sweep` report is a dated local file; it is never posted" is clear enough in context (the contract's "posts" are issue comments and PRs, `:231`).

## Checks

| Check | Description | Result |
|---|---|---|
| C1 | WC-16 paragraph (contract:277) equals DESIGN section 8 paragraph | PASS |
| C2 | Contract line 23 and guide line 991 name the same commands in the same order | PASS |
| C3 | Never-as-worker line makes the brief guard refuse `/sc:sweep` (case 3, :20) | PASS |
| C4 | WC-16 trigger wording agrees with the sweep it builds on (:110 "wake or timeout") | FAIL (F1) |
| C5 | Every term in WC-16 has a referent in the contract ("Phase 1", classes, L1 cap) | FAIL (F2, F3) |
| C6 | Escalation list items each map to a contract rule | FAIL (F4) |
| C7 | A worker new to the project is told it never runs `/sc:sweep` itself | FAIL (F5) |
| C8 | Guide bullet explains why `/sc:sweep` is on the list | FAIL (F6) |
| C9 | WC-16 says what to read and what to do when the command fails | FAIL (F7) |
| C10 | "added read, not a replacement, not a second pass" is unambiguous and consistent with :110, :151 | PASS |
| C11 | "recommends nothing" and report-is-local sentences are unambiguous | PASS |
| C12 | Test pins and contract text agree (742 passed; ruff check and format clean) | PASS |
| C13 | OQ-1 and OQ-3 records match what WC-16 and line 23 say (WC-16 id, no `--agent-wait` run by `/sc:sweep`) | PASS |
| C14 | Master WC-14 and WC-15 untouched; no WC-16 text reuses their ids | PASS |

Notes: F2 to F7 are MINOR and never fail the gate. This review made no repository change except this report (two `/tmp` files used for the `cmp` check were deleted).

Verdict: FAIL
Blocking count: 1
