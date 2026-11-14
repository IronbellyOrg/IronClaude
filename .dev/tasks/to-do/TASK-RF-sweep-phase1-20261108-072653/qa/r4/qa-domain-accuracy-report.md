# QA Report - Domain accuracy lens (WC-16 against master's Liveness supervision)

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` section 8 (WC-16), items 5.1 to 5.11
**Date:** 2026-11-09
**Phase:** doc-qualitative, domain-accuracy lens (research/09 Gap 5)
**Fix cycle:** N/A (fix_authorization: false; only this report was written)

## Scope and method

Read from disk: master `src/superclaude/core/WORKER-CONTRACT.md` lines 20-25, 46-47, 85-164, 244, 268-282; DESIGN lines 20-31, 286-316, 468-545, 660-734; `tests/skills/test_worker_contract.py` lines 20-50, 84-93, 150-190, 380-392, 750-771, 910-914, 1320-1323, 1554-1558, 1936-2030; `tests/core/test_how_we_work_routing_table.py` 25-40; `tests/recommend/test_routing_refresh.py` 30-40, 645-650; research/07 lines 1-100; research/08 lines 1-125; `r4-wc14-hits.md` lines 1-110; `r4-mechanical.md` and `r4-reanchor.md` by grep only. No `orca` command was run and no network call was made.

Fact base: master has no WC-16 anywhere under `src/superclaude` (grep: no match). The test file has no `"WC-16"` key (`grep -c` = 0).

## Findings

### F1 - MAJOR - WC-16 does not say how `/sc:sweep` relates to master's sweep (line 110); two readings on one wake

Evidence:
- Master `WORKER-CONTRACT.md:110`: "**The sweep.** After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep: one `worker-list`, one prompt-wait listing (`worktree ps --agent-wait`) and one `stat` per worker contract path (WC-11), updating each worker's heartbeat record (arrival time, progress token, declared window)." The state table (`:116-129`), the ladder (`:148-155`) and "within one sweep" (`:127`) all hang on this procedure.
- DESIGN `:677` (WC-16): "On every coordinator wake, at most once every 5 minutes (the cadence of "The sweep." under `### Liveness supervision`), the coordinator runs `/sc:sweep` and reads its report before it acts." Later sentences in the same paragraph use the bare term again: "The sweep's classes follow WC-10", "The sweep report is a dated local file", "The sweep recommends nothing: no stop, retry, release, merge or removal."
- DESIGN `:672` states only a negative: "WC-16 does not reword contract line 110 (the sweep)". Nothing in WC-16, R2 (`:712`) or D6 (`:829`) says whether `/sc:sweep` replaces, is, or runs beside that sweep.
- `/sc:sweep` cannot be master's sweep. DESIGN `:537`: `FORBIDDEN_TOKENS = {"--include-remote", "--agent-wait"}`, so it never takes the prompt-wait listing that S4 needs (`WORKER-CONTRACT.md:110`, `:122`). Its eight allowed Orca templates (`:526-535`) have no `check` or `inbox`, so it cannot see heartbeat arrivals, and it is read-only (it writes only its report), so it cannot update the coordinator's heartbeat records.

Answer to the three lens questions:
- Replace? WC-16 does not say, and R2's bold lead ("The coordinator sweeps on every wake, at most once every 5 minutes", `:712`) is the same wording as line 110 with `/sc:sweep` substituted. A coordinator that treats `/sc:sweep` as "the sweep" skips the `agent-wait` listing and the heartbeat bookkeeping, so S1, S2, S3 and S4 triggers lose their inputs.
- Run? "the cadence of 'The sweep.'" plus "the coordinator runs `/sc:sweep`" is also compatible with running both. Then one wake yields two sweeps in an undefined order, and it is unclear whether `/sc:sweep` counts toward the 5-minute cap or has its own.
- Beside? This is the only reading the DESIGN intends (`:672`), but the text never says it.
- "The sweep recommends nothing" (WC-16) sits in the same contract as a sweep whose state table has a Response column that drives L2 nudges and L4 restarts. Read literally with master, the sentence is false for master's sweep.

Fix (smallest): in `:677`, make `/sc:sweep` explicitly additive and stop reusing "the sweep" for the command. Replace the sentence "On every coordinator wake, at most once every 5 minutes (...), the coordinator runs `/sc:sweep` and reads its report before it acts." with: "On every coordinator wake, at most once every 5 minutes, the coordinator runs "The sweep." under `### Liveness supervision`, unchanged, and in the same pass runs `/sc:sweep` and reads its report before it acts. `/sc:sweep` is an added read, not a replacement and not a second pass; it does not update heartbeat records or list `agentWait`." Then replace each later "The sweep" in WC-16 with "`/sc:sweep`" or "The `/sc:sweep` report". The four pinned phrases survive ("WC-16. Coordinator loop", "On every coordinator wake", "it is never posted", "It never stops watching on its own"). Change the R2 bold lead to "**The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes, in the same pass as the contract's liveness sweep.**" and update D6 (`:829`) to match.

### F2 - MINOR - Trigger set differs: master "wake or timeout", WC-16 "wake"

- Master `:110` "After every wake or timeout"; WC-16 `:677` "On every coordinator wake", and in the same paragraph a wait that "expires" is only re-armed. R2 `:712` repeats "on every wake".
- On an expired wait the master sweep runs and `/sc:sweep` is not required. This is not exclusive (the master sweep still runs), so it is MINOR, but the routing-guide bullet reads as the sweep rule and omits the timeout.
- Fix: "On every coordinator wake or wait timeout" in WC-16 and R2; the pinned phrase "On every coordinator wake" is still a substring.

### F3 - MAJOR - `/sc:sweep` on every wake breaks master's trigger-gated probe rule (lines 110 and 151)

- Master `:110`: "Costly probes (transcript tail, screen read) run only for workers a trigger fired for in this sweep." `:151` L1 probe: "Read-only: `worker-show`, `worker-read --source transcript`, a screen read, the contract `stat`", When "A trigger fired", Cap "Every sweep; at most 2 costly probes per triggered worker per sweep."
- DESIGN `:303`: `worker-show` for `min(D, 50)` Dispatch rows on every run; `:292` and `:514` read the tail (last 256 KiB) of every transcript under the scanned project keys, and every contract record named by Orca rows. These are the same probes as L1, run for all workers whether or not a trigger fired.
- DESIGN `:672` says WC-16 "does not reword ... line 151", so the conflict is neither resolved nor acknowledged. A strict reader of master must either skip `/sc:sweep` when no trigger fired (contradicting WC-16 "on every wake") or break the cap.
- Fix (smallest): add one sentence to WC-16: "`/sc:sweep`'s own reads are not L1 probes and do not count against the L1 cap; the coordinator's own L1 probes stay limited to triggered workers." This needs owner approval with GQ-11, and it does not touch the pinned `liveness-*` phrases.

### F4 - MINOR - Two vocabularies, no tie-break

- `/sc:sweep` classes (DESIGN `:472`: waiting on a person, stalled (proved), fenced, working, finished, idle, person session (active), could not determine) are not mapped to S0-S11 (`WORKER-CONTRACT.md:116-129`). Example: sweep rule 5 `working` (DESIGN `:491`) while master S9 or S3 fires.
- Sweep rule 2 `orca_exit_proof` (`:479`) covers only the Orca exit proof. Master's L4 proofs (`:157`) also include "a transcript whose final agent turn sent no `worker_done`". WC-16's "only Orca's stall proofs make a worker stalled" is consistent with WC-10 (`:46`) and `:157`, but the sweep can under-report; absence of "stalled (proved)" must not be read as absence of a proof.
- Fix: one sentence in WC-16: "The master state table decides the response; a `/sc:sweep` class never overrides it."

### F5 - MINOR - Never-as-worker order and pin-insert hazard

- DESIGN `:701` puts `/sc:sweep` before `/sc:swarm-wizard`; the existing list is alphabetical (`spawn`, `swarm-wizard`), and `sweep` sorts after `swarm`. Cosmetic. If reordered, the test phrase at `test_worker_contract.py:89`, `:701` and R7 must change together.
- Dict-literal hazard (not a defect today): pin 1 is an insert of a new `"WC-16"` key into the `RULE_PHRASES` dict literal. Applying the edit twice would silently keep the later duplicate. Today `grep -c '"WC-16"'` = 0. Check `= 1` after the edit.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Master `### Liveness supervision` (`:95-164`) and line 110 read from disk | PASS |
| C2 | WC-16 states whether `/sc:sweep` replaces, runs or sits beside the line 110 sweep | FAIL (F1) |
| C3 | WC-16 + master cannot yield two different actions on one wake | FAIL (F1) |
| C4 | Trigger set matches ("wake or timeout" vs "wake") | FAIL (F2, MINOR) |
| C5 | `/sc:sweep` probes fit line 110 and line 151 trigger-gated, capped probes | FAIL (F3) |
| C6 | Stall-proof statement matches WC-10 (`:46`) and `:157` | PASS |
| C7 | Sweep classes map to S-states with a tie-break | FAIL (F4, MINOR) |
| C8 | Dict-literal duplicate-key risk: no `"WC-16"` key in `RULE_PHRASES`; insert anchors (WC-15 at `:165-172`, `heartbeats` at `:173`) verified | PASS |
| C9 | Pinned phrases occur verbatim in the WC-16 text and the ident shares the heading line (`_check_rule`, `:755-762`) | PASS |
| C10 | Line 23 text and the `never-as-worker` pin (`test_worker_contract.py:86-92`) agree after the edit | PASS |
| C11 | Placement (fan-in paragraph `:273`, worked example `:275`) and no ID clash with worker rules WC-14 (`:63`) and WC-15 | PASS |
| C12 | Escalation list does not contradict master (third brief-guard refusal, `:244`; WC-6 retries) | PASS |
| C13 | R2 routing bullet (`:712`) is consistent with master line 110 | FAIL (F1, F2) |
| C14 | Cited test lines (25, 86-92, 165-173, 382-391, 755-771, 912, 1322, 1556) spot-checked | PASS |
| C15 | Master has no WC-16 and no `/sc:sweep` text (`src/superclaude` grep) | PASS |
| C16 | Dict-literal duplicate-key risk remains anywhere else (`_OTHER_COMMANDS` and `_POST_REFRESH_ADDITIONS` are sets; `NEVER_AS_WORKER` is a tuple; `WRITE_VERB_CLASSIFICATION` keys are path-specific) | PASS (note in F5) |

Confidence: Verified 16/16 checks with tool evidence | Unverifiable 0 | Unchecked 0.
Tool engagement: Read 17 | Grep 13 | Glob 0 | Bash 1.

## Self-Audit

**(a) Reliance list:** Relied on `r4-mechanical.md` and `r4-wc14-hits.md` for the WC-14 to WC-16 rename counts and heading locations only; research/07 and research/08 for line-move tables (spot-checked, C14).

**(b) Independent semantic checks:**
- Whether `/sc:sweep` can substitute for master's sweep: checked against `FORBIDDEN_TOKENS` (DESIGN `:537`) and the allowed Orca templates (`:526-535`) versus contract `:110`. It cannot, which the mechanical reports do not address.
- Whether `/sc:sweep` reads fit the L1 probe cap: DESIGN `:292`, `:303`, `:514` versus contract `:110`, `:151`.
- Dict-literal duplicate-key: `grep -c '"WC-16"'` on the test file and a read of `RULE_PHRASES` anchors.

Zero-issue suspicion: not applicable; two MAJOR findings were found.

## Verdict

Verdict: FAIL
Blocking count: 2
