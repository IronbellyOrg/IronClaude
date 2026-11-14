<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 5 (review 05, "The built superclaude observe versus Orchestrator mode (#339)", variant-5-original.md; base score 0.915) -->
<!-- Merge date: 2026-11-13T18:50:58Z -->

# Alignment findings, decisions and course of action

<!-- Source: Base (original, modified) - restructured into a decision document per Change #1; status block carried per Change #20 -->

> **Status: BLOCKED_BY_INVARIANTS.** The debate reached agreement on every point it compared, but it stopped at its last check because one high-severity problem is still open and nobody has fixed or accepted it. That problem is **INV-008** (an item id from the debate's last check, the "invariant probe"): the open security review thread on PR #539 asks for a fix that, measured on this host, does not close the hole it describes. Only the owner can fix it or accept the risk. It is the first action in Part 2.2 and the first step in Part 4, and nothing in this document waives it. **INV-008 is UNRESOLVED.**
>
> **What this document is.** One adjudicated record of five independent reviews (of issue #409 and the built observer, issue #450, Coder#477, issue #423, and the observer versus Orchestrator mode), after two debate rounds and one invariant check. It says what is true, what the debate withdrew, what the owner must decide (with a recommended answer for each), what to do and in what order. It posts nothing, edits no issue and changes no repository.
>
> **Read first:** Part 1.1 (the verdict), then Part 2.2 action 1 (INV-008), then Part 7 questions Q1 to Q4.

## Part 0: Status, convergence, unresolved items, glossary and how to read this document

<!-- Source: Base (original, modified) - header block per Change #20; glossary per Change #22 (repairs the base's L4 miss: coined names were never defined) -->

### 0.1 Status and convergence

| Field | Value |
|---|---|
| status | **BLOCKED_BY_INVARIANTS** (carried, not waived; this document must never be read as "converged" or "success") |
| convergence | 100% on 36 of 36 points (the "X" and "A" points defined in 0.3); it was 63.9% (23 of 36) before Round 2; the coverage check for kinds of problem passed; the invariant check did not pass |
| base | Variant 5 (score 0.915; Variant 2 scored 0.893; the margin is 2.2 points; the tie was broken by Variant 5 winning 18 of the 36 scored points) |
| unresolved | INV-008 (no fix specified, owner ruling pending); A-009 (two builds of the same Orca release are on record and the observer records no build); X-016 (whether one Orca read consumes messages on a live coordinator Run is unproven both ways) |
| what ran | Nothing was run against live Orca by the debate except read-only list, help and version calls recorded in the invariant probe; every "verified now" claim names its source |

### 0.2 Unresolved items (all labelled UNRESOLVED)

1. **INV-008, UNRESOLVED.** The git-config hole in the sweep's `git status` calls. The fix is not specified and the owner's ruling does not exist (Part 2.2 action 1).
2. **A-009, UNRESOLVED by evidence (67%).** The Orca build divergence (Part 3.3, Part 5.3).
3. **X-016, UNRESOLVED (61%).** Whether `check --all --types question` consumes messages on a live coordinator Run (Part 3.1, Part 5.3).
4. Further open facts, each with the single fact that settles it, are listed in Part 5.3 item 4 (all UNRESOLVED).

### 0.3 Glossary: every id and coined name used in this document

**The five source reviews ("variants").** Each is a file in the debate folder.

| Short name | What it reviewed | File |
|---|---|---|
| V1 (review 01) | Issue #409 (the TUI observer dashboard) against Orchestrator mode Phase 1 (#339) | `variant-1-original.md` |
| V2 (review 02) | Issue #450 (rollout of the issue watcher) against #339 and #409 | `variant-2-original.md` |
| V3 (review 03) | IronbellyOrg/Coder#477 (workspace listener) against #339 and #409 | `variant-3-original.md` |
| V4 (review 04) | Issue #423 (Orchestrator v2) and the #339 boundary | `variant-4-original.md` |
| V5 (review 05) | The already built observer `superclaude observe` against the sweep. This is the base of this document | `variant-5-original.md` |

**Debate files and id families** (all in the folder `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/`).

| Id form | Plain meaning | Where defined |
|---|---|---|
| R1-Vn, R2-Vn | Advocate Vn's Round 1 statement, or Round 2 rebuttal (`round1-advocate-Vn.md`, `round2-rebuttal-Vn.md`). "R2-V5 5.9" means section 5.9 of Variant 5's Round 2 rebuttal | those files |
| X-nnn | A point where the variants contradict each other (20 of them: X-001 to X-020) | `diff-analysis.md` |
| A-nnn | A shared assumption that all variants made and the debate tested (16 of them: A-001 to A-016) | `diff-analysis.md` |
| S-nnn, C-nnn, U-nnn | A structural difference, a content difference, a unique contribution of one variant | `diff-analysis.md` |
| SC-nn | A row in the spot-check log (a re-verification of a claim against its source) | `diff-analysis.md` |
| "matrix" | The Scoring Matrix: the winner and mean confidence of each X and A point | `debate-transcript.md` |
| INV-nnn | A finding from the invariant probe (the last check after Round 2, by a fault-finder who argues for no variant): 44 findings, INV-001 to INV-044; severity HIGH, MEDIUM or LOW; ADDRESSED means the debate already handled it, UNADDRESSED means it did not | `invariant-probe.md`; summarised in Part 5 |
| C-nn, F-nn, A-nn, W-n (with a V1 prefix); W-nn (V2); Fn (V3, V4); Q1..Qn (inside a variant) | Item numbers inside one review: claim checks, alignment findings, acceptance-criteria checks, proposed wordings, questions. When a number could belong to two reviews it is written with its review (for example "V1 C-07", "V2 W-05") | the variant files |
| O-nn | An overlap finding in V5 (O-01 to O-16): a place where the observer and the sweep touch the same thing | `variant-5-original.md` |
| RT-Fnn | V5's re-test of V1's finding F-nn against the built observer | `variant-5-original.md` |
| S1 to S10 | The ten parts of V5's section "What `superclaude observe` is today" | `variant-5-original.md` |
| D1 to D9 | V5's nine integration decisions | `variant-5-original.md` |
| D-1 to D-9, D-A, D-B, D-E, D-F, D-G, D-H | "Remaining disagreement" items in the Round 2 rebuttals, each with the single fact that would settle it. The numbers restart in each file, so the same label can mean different things: unless a file is named, D-3, D-5 and D-8 mean `round2-rebuttal-V5.md` section 4 (D-3 the join-key comparison, D-5 whether `agent launch` creates a Run, D-8 the `projection.attention` values) and D-A and D-B mean `round2-rebuttal-V2.md` section 4; "R2-V3 D-7" is the owner-token route to the Orca app and "R2-V5 D-7" is reuse of the observer's paging code. The ones that still matter are spelled out in Part 5.3 | `round2-rebuttal-V*.md` section 4 |
| BC-01 to BC-23 | V5's 23 numbered corrections to the #409 body (Part 6.1) | `variant-5-original.md` |
| E-01 to E-18 | Fact numbers used only in this document (Part 1.2) | this document |
| Q1 to Q24 | The owner questions in Part 7 of this document. (A hyphen means something else: Q-1, Q-2, Q-3 are Orca gate tests, defined below) | this document |
| #nnn, PR #nnn, Coder#nnn | Issue or pull request numbers in `IronbellyOrg/IronClaude`, except "Coder#nnn" which is an issue in the `IronbellyOrg/Coder` repository | GitHub |
| PLAN INFERENCE | A point that no debate file states; the refactoring plan derived it from a debate file or from the invariant probe. It is marked wherever it appears | this document |
| UNVERIFIED | Not confirmed from a source the debate opened. It never drives a recommendation | this document |

**Programs and terms.**

| Term | Plain meaning |
|---|---|
| Orca | The local agent-orchestration application. Both programs below call its command line (`orca` or `orca-ide`). Its records: a Run (one coordinated piece of work), a Dispatch (one task handed to a worker), a Worker (an agent session working on a Dispatch) |
| the observer, `superclaude observe`, the "TUI panel" in the owner's wording | The read-only terminal dashboard of Orca workers, issue #409. Built and merged: release 1 in PR #503, release 2 in PR #514 |
| the sweep, `superclaude sweep run`, Orchestrator mode Phase 1 | The read-only report a coordinator session produces about its workers (#339), in PR #539 (open) |
| the watcher | The issue watcher (#331, rollout #450): a poller that starts a claim session for an approved issue |
| coordinator | A person-opened Claude session that runs the sweep loop and dispatches workers |
| WC-16 | The worker-contract rule that caps a coordinator's sweep at once per 5 minutes (it is a cap, not a schedule) and says the sweep recommends nothing |
| WC-12, WC-13 | Other worker-contract rules (`src/superclaude/core/WORKER-CONTRACT.md`): WC-12 is the coordinator's answer and the worker's acknowledgement line for it (the channel by which a coordinator corrects a worker); WC-13 says a worker session never starts other workers or agents (no `worker-start`, `dispatch`, `task-create`, `agent launch`) |
| NFR-001 | The sweep rule "a sweep adds exactly one report file" (design `docs/designs/orchestrator-mode.md:128`, pinned by two tests) |
| NFR-014 | The owner-signed allow-list of exact Orca commands (10 templates over 7 verbs) and git commands the sweep may run |
| FU-1 | The watcher's first live test (item 1 in #450); FU-2 to FU-6 are its later steps (FU-2 enables the cron schedule) |
| AC-S | The owner's own dated direction-selection record: the record that says which observer design direction was chosen. It does not exist yet |
| Q-1, Q-2, Q-3 | Observer gate tests from `release-gates.md`: Q-1 (an unbound terminal cannot read another terminal's Run) failed on 2026-11-11; Q-2 is the effect of `run-use` on a live coordinator (never tested, forbidden for the observer); Q-3 is whether `ask` writes a message of type `question` |
| QUESTION-OBSERVATION, QUESTION-LINK | The observer's gate names: QUESTION-OBSERVATION is the gate for reading coordinator questions (release 2); QUESTION-LINK is the gate for release 3 (Decision Desk) |
| guard, the flip, `QUESTION_GATE_PASSED` | The observer's one boolean switch that turns the coordinator-questions read on. It is `False` on master. "The flip" or "guard-flip PR" is the change that sets it to `True` |
| OB-H1, OB-H2, OB-H3 | The ship gates of the claim command (`claim.md:131`); issue #394 is cited with them in the watcher review (V2) |
| TUIBBS | The owner's separate TUI platform that runs on a different SSH host; the observer snapshot is shaped so a read-only Go screen there could read it later |
| R1 to R4 (observer) | The observer's planned releases; R3 is Decision Desk, R4 is the remote fleet. Not the same as Round 1 and Round 2 of the debate |
| Signal Bridge, Attention Ledger, Fleet Quilt, Decision Desk, Loop Detector, Mission Pulse, Collision Lens | Names of designs in the twenty synthetic design images of the #409 package. The built observer implements only Signal Bridge's worker ledger and the Attention Ledger's question panel |
| #534 | The issue that tracks Phase 1 follow-ups of the sweep (including the shared live capture) |
| snapshot ("observe snapshot v1") and "sweep report JSON v1" | The two JSON files both loosely called "the JSON v1"; they are different (Part 1.2 E-05) |
| join key | The field that would let a reader match an observer row to a sweep row: `dispatchId` against the part of `row_id` after `orca:`. Not yet confirmed on real ids |
| consume, "does not mark read" | Orca's plain `check` reads and removes a message from a mailbox; whether `check --all` does the same is the open question X-016 |

### 0.4 How to read a point record

Every point in Part 3 has the same eight fields, in this order: **id, verdict, confidence, evidence, decision needed from the owner (with the recommended answer), course of action, dependencies (what must happen first, what it unblocks), reversibility.** "Confidence" is the mean across the five advocates' final positions (the matrix), not a probability of success. In Part 2 each action ends with a bracket giving the decision it needs, what it waits for and unblocks, and whether it can be undone; the verdict, confidence and evidence for the underlying points are in Part 3. "Reversible: yes" means a revert, an edit or an issue-history restore undoes it. Nothing here is irreversible except a posted comment's notification and a merged PR's squash commit (which a revert PR undoes).

Where the debate gave no winner the recommended answer is marked "default (no debate verdict)". Where this document adds a point that no debate file states it is marked PLAN INFERENCE.

## Part 1: Verdict, the facts the debate established, and the findings it withdrew

### 1.1 Verdict

<!-- Source: Base (original, modified) - V5 "Verdict" replaced by the adjudicated verdict per Change #2 (X-019: V5 overgeneralised "all four earlier reviews were wrong") -->

> The five reviews (of #409, #450, Coder#477, #423, and the built observer) agree on one conclusion once Round 2 is applied: Orchestrator mode (the `superclaude sweep` command on PR #539) and the TUI panel (the `superclaude observe` command, merged in PR #503 and PR #514) already exist as two separate programs, were built independently from the same design package, mention each other nowhere, and point in the same direction. They are aligned in intent and not yet in practice: two readers of the same Orca command, two JSON files that both call themselves "v1", three vocabularies, two lists of allowed Orca commands that disagree on one command (`check`), and no written contract between them. Recommended course: keep both programs; write one short contract note; settle the open security question on PR #539 first; correct the four issue bodies in one ordered edit pass; do not build a reader of the sweep's JSON inside the observer; answer the 24 owner questions in Part 7, starting with Q1 to Q4.
>
> Status: BLOCKED_BY_INVARIANTS. All 36 diff points reached one winner or an agreed "unresolved" (convergence 100 percent on points, 63.9 percent before Round 2). One HIGH invariant is not addressed: INV-008, the git-config hole in the sweep's `git status` calls. It is the first action in Part 2.2 and in Part 4 and is not waived.

Where earlier reviews were wrong: V1 stated that no observer exists; V2 W-10 and V4 F13 and its proposals (a) and (b) assumed one exists; V3 wrote generically and did not check (X-019, 87%; conceded by V5 in Round 1 concession 7 and Round 2 row 1). The earlier shorthand "all four earlier reviews were wrong about one fact" is withdrawn.

Nothing was run against live Orca by the debate except read-only list, help and version calls recorded in the invariant probe; every "verified now" claim in this document names its source.

### 1.2 Facts the debate established

<!-- Source: Base (original, modified) - V5 "What superclaude observe is today" (S1 to S10) condensed into facts, with debate corrections, per Change #1 and Change #4; V5 sections remain in full in variant-5-original.md (see Appendix A) -->

Each row: fact, evidence, confidence (from the matrix where one exists).

| # | Fact | Evidence | Confidence |
|---|------|----------|------------|
| E-01 | The observer is built and merged: release 1 in PR #503 (2026-11-11T19:54:57Z, `9e2608b03`) and release 2 in PR #514 (2026-11-12T12:36:19Z, `cd8736199`); registered in the shipped CLI | `src/superclaude/cli/main.py:572-574`; `gh pr view` (SC-13) | 98% (X-012) |
| E-02 | The observer's coordinator-questions read is OFF on master: `QUESTION_GATE_PASSED = False` (`observe/commands.py:63-67`). The switch-on exists only as two unpushed local commits (`1ae72e1a1`, `f104ca51a`) in sibling worktree `issue-409-mvp`; remote branch `409-Phase2` is gone; `origin/master` is not an ancestor of the sibling HEAD, so a fresh branch is needed | R2-V5 section 1 rows 5, 11; `git merge-base --is-ancestor` exit 1; INV-001 | verified in Round 1 and by the probe |
| E-03 | The observer reads Orca only and reads no sweep file; the sweep, its design, command, skill and WORKER-CONTRACT contain no reference to the observer, `cli/observe`, #503 or #514. The two programs never mention each other | X-013 (SC-15, SC-16) | 95% |
| E-04 | Two readers of `worker-list`: observer all Runs, 15 s per process, up to 5 calls of 100 rows, 8 MiB and 10 s per call; sweep one Run per wake, WC-16 cap at most once per 5 minutes, up to 50 `worker-show`, 90 s budget. No shared limit; several observers multiply the load | `adapter.py:29,57`; `collector.py:28-34`; `probes.py:112-118`; X-015 | 87% |
| E-05 | Two JSON files both called "v1": "observe snapshot v1" (`schemaVersion`, camelCase, `"UNKNOWN"` strings, rows keyed `dispatchId`, additionalProperties false, rewritten every live cycle in the user state directory) and "sweep report JSON v1" (`schema_version`, snake_case, `null`, rows keyed `row_id` = `orca:<dispatch>`, printed to stdout only) | A-014; O-08 | 94% |
| E-06 | Three vocabularies (observer, sweep, Orca). The built observer shows none of the ten dimension names; it prints Orca's words and marks report status, acceptance, tests, approval, settled and policy-frozen `unavailable (no source)` | X-008; `view.py:96,412` | 91% |
| E-07 | `superclaude sweep run` always writes a dated report before it prints JSON; the JSON goes to stdout only; the rule "a sweep adds exactly one report file" (NFR-001) is pinned by the design (`docs/designs/orchestrator-mode.md:128`) and two tests (`tests/sweep/test_readonly.py:300`, `tests/sweep/test_cli_contract.py:1474`) | X-004; R2-V5 row 7 | 91% |
| E-08 | PR #539: open, head `873599d59`, six review threads, four resolved, two unresolved (`probes.py:1052` Augment, filtered count under-reads a page; `probes.py:1211` Codex security thread). CI fails on one test (`test_every_worktree_gets_an_agent_and_its_creator_owns_it`), the same test that fails on master. PR #541 re-pins that test, changes one file (`tests/core/test_claude_md_worktree_rule.py`), is OPEN and CLEAN; #539's 1003 files do not include it | INV-022, INV-036, INV-038; A-004 | 88% |
| E-09 | The sweep's reads are not fully confined: `git status` runs in every path `worktree ps` lists with the inherited environment; a shared repo config reaches every linked worktree | `probes.py:305-327,1203-1214`; X-007; INV-008 measurement | 89% |
| E-10 | The watcher prompt `/sc:issue --claim <N>` has no `--pipeline`, so the claim runs at its default `worktree` level: it creates or reuses worktree `issue-<N>` and starts a governed second agent. The watcher design says the claim stops at `next-steps.md` | `issue.md:43,88`; `launch.py:33`; `issue-watcher.md:44`; X-001 | 91% |
| E-11 | On this host launched Claude sessions run with permission checks off: `CCSESSION_PERMISSIONS` is unset and `ps` shows `--dangerously-skip-permissions --allowedTools=Grep`; a non-empty `CC_CLAUDE_FLAGS` replaces the flags whatever `CCSESSION_PERMISSIONS` says | `ccsession:134-141`; INV-011 (probe, `ps`) | verified on this host only |
| E-12 | Coder#477's premise (a watcher that sends prompts to a listener) contradicts the built watcher (design decision D1 option A: no listener, inbound port or address registry) | `issue-watcher.md:28,43,47-49`; R2-V3 5.1 | per V3 and V2 |
| E-13 | "v1" and "v2" mean different things in the #339 issue summary, in the Phase 1 research report (phases 1 to 6) and in #423; at least five numbering namespaces are in play (adds observer R1 to R4 and "release 2", and the watcher's FU-1 to FU-6) | R2-V4 5.1; INV-021 | 100% for the three; INV-021 for five |
| E-14 | On this host the observer is already past its read cap: an unscoped `worker-list` reports `page.total` 513 while the observer stops after 5 calls of 100; only the 13 oldest rows are hidden (order newest-first is an observation, not documented) | `adapter.py:57`; INV-017 | probe, live read |
| E-15 | Two builds of one Orca release are on record: design lock `1.4.245-aidev02.780594c521aa` and host `1.4.245-aidev02.9cfecdd30b2a`; the sweep compares only the text before the first hyphen, so it cannot tell them apart; the observer records no Orca version | `report.py:160`, `:23`; INV-020 | A-009 unresolved |
| E-16 | Most owner decision records the observer relies on are not on master: only `owner-decisions-20261111.md` is; the 2026-11-08 and 2026-11-12 records, the pass record, `live-test-guide.md` and `tuibbs-review/` are untracked or in unpushed commits in the sibling worktree | `git ls-tree origin/master .dev/issues/409/`; INV-002 | 83% (A-015) |
| E-17 | `observe --once` already prints a plain-text record with no file write unless `--snapshot` is passed; the #339 "static report in chat" ask does not need a new program | `commands.py:215-237`; O-16 | verified in Round 1 |
| E-18 | Orca's own `orchestration check --help` on this build says `--all` "does not mark read" and that `--peek` and `--all` "do not drain a mailbox on their own"; no debate file cited it; the owner's measurement on the coordinator's own Run is non-diagnostic (0 pending is expected either way) | INV-041(a); R2-V1 section 5 item 2; `release-gates.md` | X-016 stays "unproven both ways" (61%) |

**Facts the debate could not establish (carry as UNVERIFIED):** whether `agent launch` creates any Run or Dispatch record (D-A); the real launch-reply shape (`OPERATION_ID_PATHS`, `launch.py:39-45`); whether a human can use the observer's questions panel in a terminal that already holds a Claude coordinator session (INV-024); who wrote the pass record (authorship); whether Orca prunes worker rows; `projection.attention` values for live and blocked workers; non-owner non-consumption of `check --all`; real message rate; whether an owner API token can drive the owner-shared Orca app (R2-V3 D-7); the second host's Orca shape.

### 1.3 Findings the debate withdrew or disproved

<!-- Source: Variants 1 to 5 Round 2 rebuttals (R2-V1 to R2-V5, section 1 concessions), invariant probe rows INV-008, INV-017, INV-037, INV-041 - merged per Change #3 -->

Purpose: so no reader re-raises a dead finding. Each row uses the advocate's own concession from Round 2, not the orchestrator's reading. In `step3-quantitative.md` section 2 the totals are 8 items withdrawn in full for V1, 0 for V2 and V3, 1 for V4 and 2 for V5, plus narrowed items.

| Finding | From | Why it fell | What stands instead |
|---------|------|-------------|---------------------|
| "No observer code exists; 20 designs await a human choice" (V1 C-03, C-02 second half, #409 body L16) | V1 | PR #503 and #514 are merged (X-012, 98%) | observer built; selection record (AC-S) missing |
| V1 C-21, C-26, A-01 "aligned", A-05 to A-07 as gaps, F-01 "(1) the observer reads the sweep JSON", F-03's observer option, F-04 as an observer gap, F-12, F-14, F-15 as observer gaps, W-3, Q1 | V1 | all rest on the false premise; withdrawn in R2-V1 section 1 "Net" | sweep-side F-02, F-05, F-07, F-08 to F-11, F-13, F-17, F-18, C-07, C-25, C-34 stand |
| "Persist `<stem>.json` beside the report" as the recommended answer (V1 F-03, Q1) | V1, and V5 Round 1 concession 4 "persist now, it is cheap" | breaks NFR-001 and two pinned tests; needs an owner requirement change in a contested PR (R2-V5 row 7) | persistence is Phase 2, owner choice; or caller-side stdout capture |
| V1 C-08 "#539 needs a rebase after #541" | V1 | no file overlap (INV-036) | a new merge ref is needed, not a rebase (INV-037) |
| Verdict "share the same dimension names" and its tally | V1 | contradicts V1's own C-02 and F-02 (X-008); tally miscount (X-009) | F-02 table plus three vocabularies |
| V2 W-10 "observer reader" as written; "absent by construction" for the Run record (W-04); cites by `/tmp` line numbers | V2 | the built observer has no watcher input; the Run claim is an inference | "no watcher panel in `observe` before FU-1"; W-04 as UNVERIFIED |
| V2 W-05 "will be mislabelled person-started" as a firm claim | V2 | depends on `session_join`, which V2 did not run; `prompt` is empty or not a slash command on all 27 live agent rows | labelling by prompt UNVERIFIED until FU-1 (D-B) |
| V3 Edit 5 "the reply is produced without any write" (a status route from `sweep run`) | V3 | `sweep run` always writes a dated report (X-004); a sidecar breaks `test_readonly.py:400` | first status record = the observer snapshot (R2-V3 D-3) |
| V3 Edit 8 restated launch ("a new top-level session") without the second governed agent; the twelve-edit shape; all `/tmp` line cites | V3 | X-001 | state the claim level explicitly |
| V4 Edit 3 "both read the same sweep facts"; C8 "boundary sentence TRUE" (circular); F17 "confines every path"; F16 cadence count; F18 "Collision Lens" as an existing detector; F19; #423 edits 4 and 7; #339 edit 4 and #409 edit 2 narrowed | V4 | circular proofs; the sweep confines file reads only (X-007); Collision Lens is an unbuilt synthetic design | boundary relabelled "proposed" (X-002); the per-class acceptance criteria stand in narrowed form |
| V5 O-05 "the sweep's 'cannot read without consuming' is stronger than the evidence" and its proposed rewording | V5 | the owner's measurement was on the coordinator's own Run and is non-diagnostic; only a synthetic probe Run is diagnostic | X-016 unproven both ways; replacement wording in Part 2.2 action 6 |
| V5 BC-17 "(the sweep's output or the observer's snapshot) as a v2 input", as worded; RT-F16 | V5 | the snapshot's 15 required row keys contain no command, objective, branch, changed paths or issue or PR | R2-V5 row 9 replacement text (Part 6.1) |
| V5 D5 option (ii) "any Run the terminal holds" as a recommendation | V5 | scope is not the risk (Orca fences, `consumer_fenced`); consumption on a live coordinator Run is | seeded consumption test first; owner writes scope in own sentence |
| "All four earlier reviews were wrong about one fact" (X-019) and "drop W-3 from the #409 body" (X-020) | V5 | overgeneralisation; W-3 is V1's proposed wording, not body text | cite exactly; read as "do not add V1's W-3" |
| V5 F-04 headline "CLOSED" | V5 | holds for the Orca ledger on one host only | say "closed for the Orca ledger on one host; open for per-Run depth and for multi-host" |
| "#539 needs only a CI re-run after #541 merges" | R2-V1 A-004, R2-V2 A-004 | a re-run keeps the same merge commit and fails on the same test (INV-037) | push, update-branch, or close and reopen |
| "Filtering to the selected repository and disabling executable Git config closes the Codex thread" | the thread's suggested remedy | a repo filter leaves a shared `.git/config` exposed and one flag stops only `core.fsmonitor`, not `filter.*.clean` (INV-008) | Part 2.2 action 1 |
| "The observer's 5-call cap covers a host's worker ledger" (X-014 "closed" read broadly) | R2-V5 X-014 | this host has 513 rows (INV-017) | PARTIAL is the steady state here |
| "A seeded test on a throwaway Run proves `check --all --types question` does not consume" (as sufficient) | R2-V5 D-1, R2-V1 D-2, R2-V3 D-4 | one build, a Run with no `--wait` listeners, and Q-1 FAIL means a pass says nothing about usability (INV-041) | the test is necessary, not sufficient; Part 2.1 action 4 |

## Part 2: Adjudicated points by issue or system

<!-- Source: Base (original, modified) - V5 report order re-homed into per-system sections per Change #1; sections 2.1 to 2.7 carry Changes #4 to #10 -->

Each system section has: the points it covers (ids; the per-point record is in Part 3), the adjudicated verdict, numbered actions in order, "Do not", and the owner questions (Part 7 ids). Each action ends with a bracket: **Decision** (the owner question and the recommended answer), **Waits for / Unblocks**, **Undo** (reversibility).

### 2.1 Observer (`superclaude observe`) and issue #409

<!-- Source: Base (original, modified) - V5 S1 to S10, O-06, O-09, D5, D6, D8, with V1 C-07, C-25, C-34 and invariant rows INV-001 to INV-005, INV-014, INV-017, INV-018, INV-023, INV-024, INV-041, INV-044, merged per Change #4 -->

- **Points covered**: X-012, X-013, X-018, X-011, X-014, X-015, X-016, X-002, A-003, A-010, A-013, A-015, A-016; probe findings INV-001 to INV-005, INV-014, INV-017, INV-018, INV-023, INV-024, INV-041, INV-044.
- **Verdict**: the observer is built (E-01), reads Orca only (E-03), implements only Signal Bridge's worker ledger and the Attention Ledger's question panel (Fleet Quilt, Loop Detector, Mission Pulse and the reviewer's four asks are unbuilt; Decision Desk is release 3, gated). Its questions read is dark on master (E-02). The #409 body is wrong in 23 places (Part 6.1), headed by "No observer code exists" (L16) and "Preferred direction is Bubble Tea" (L54, L124, which the owner replaced with Python + Rich on 2026-11-08). The direction was chosen in staged form (2026-11-08, 2026-11-11); the dated selection record (AC-S) does not exist (X-018, 74%).
- **Actions, in order**:
  1. **One editor posts the #409 correction pass** (Part 6.1), after the owner answers Q8 and, for decision 6, Q16. Pin to `updatedAt` and re-read it immediately before the write (INV-030). [Decision: Q8 (write the AC-S record), Q16 (one vocabulary). Waits for: Q8, Q16, owner records (REC). Unblocks: an accurate #409 for every later step. Undo: yes, issue history.]
  2. **The owner writes the AC-S record**, or amends #409's first acceptance criterion (Q8). Agents cite it; they do not write it (`release-gates.md:22`). [Decision: Q8. Waits for: the owner. Unblocks: #409 acceptance criterion 1 wording and any release 3. Undo: yes.]
  3. **The owner commits or archives the evidence that exists only in the sibling worktree**: `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/` (INV-002), before that worktree is cleaned. The guard-flip PR itself must commit the owner's pass record (INV-001). [Decision: Q7 (yes). Waits for: before the sibling worktree is cleaned. Unblocks: citing those records, and the flip PR. Undo: yes.]
  4. **Guard-flip PR** (the switch-on of the questions read). Prerequisites, all of them: (a) the owner's scope sentence, "this Run only" or "any Run my terminal holds" (Q6; INV-003: the record names one Run, `run_93bfa00cae2b`, an old "Claim issue 375" Run; the guard is one boolean and `check_run_id` checks syntax only, so after the flip any `--run <id>` reads); no scope answer means the guard stays off; (b) the seeded consumption test, run by the owner or the 409 session from a plain terminal that holds no Run: `run-create` only, never `run-use`, record `run-current` before and after, put known `question`, `worker_done` and heartbeat messages in the mailbox, run the observer's exact template twice, then one consuming `check`, and confirm every seeded message is still returned (INV-005, INV-041 (c); safe precedent: the Task 17 sample `run_86013b917868`); cite Orca's own help text for `--all` first (INV-041 (a)); record the Orca build string in the gate record and add a build check or a test that fails when the build changes (INV-041 (b)); (c) one recorded live attempt of the panel in the real coordinator layout, because Q-1 FAIL means a passing test says nothing about usability and 28 of 53 Runs have no holder terminal (INV-024); (d) the owner-written pass record committed on master, because the constant cites a path that exists only in the sibling (INV-001; authorship rule INV-014: the owner supplies it); (e) the mapping-table row for `reclaimable` (INV-023); (f) grep `.dev/issues/409/` for "not passed" and fix each hit in the same change, including `release-gates.md` (INV-044). Open from a fresh branch off `origin/master` after #541, with `/sc:pr-submit --monitor 3` (project rule: never a bare `gh pr create`). [Decision: Q6 (default, no debate verdict: do not flip before the seeded test; the scope sentence is yours; no answer means guard off), Q7. Waits for: #541, Q6, the seeded test, owner records, a live-layout attempt, the build pin, the "not passed" grep. Unblocks: a usable questions panel. Undo: yes, flip the constant back.]
  5. **Routing row for `superclaude observe`** (Part 4 step 5; INV-029). [Decision: Q12 (yes, one row, own small PR after #539 merges). Waits for: #539 merged (it shares four files). Unblocks: discoverability. Undo: yes.]
  6. **Contract note** (Part 2.3). [Decision: Q5. Waits for: Part 4 step 2 for links. Unblocks: #409 wording, the status record of V3, the field list of V4. Undo: yes, remove file and test.]
- **Do not**: add a watcher panel to `observe` before FU-1 (V2 W-10 reworded); add an observer reader of the sweep's JSON (X-013, X-017); flip the guard before action 4 (a) and (b); treat the owner's "0 pending after reads" on the coordinator's own Run as proof of non-consumption (X-016).
- **Cap facts to state** (INV-017, INV-018): on this host the observer is partial in steady state (513 rows against 500); "at most 5 calls per read" is for `worker-list`; with `--questions` on a cycle can make 6.
- **Owner questions**: Q6, Q7, Q8, Q12, Q16, Q17, Q19, Q22, Q23.

### 2.2 Sweep, Orchestrator mode (#339) and PR #539

<!-- Source: Variant 1 (variant-1-original.md), F-07 and C-18, with Round 2 rebuttals R2-V1 sections 3 and 5 and R2-V5 section 3 (A-004) and 5.8, and invariant rows INV-008, INV-009, INV-010, INV-015, INV-019, INV-020, INV-022, INV-033, INV-036 to INV-040 - merged per Change #5. INV-008 is the first, blocking action; the fix design is not invented here (requirement and options only) -->

- **Points covered**: A-004, A-006, X-004, X-007, X-010, A-005, plus the surviving V1 findings C-07, C-25, F-02, F-05, F-07, F-08 to F-11, F-13, F-17, F-18; probe findings INV-008, INV-009, INV-010, INV-015, INV-019, INV-020, INV-022, INV-033, INV-036, INV-037, INV-038, INV-039, INV-040.
- **Verdict**: PR #539 (Phase 1, the read-only sweep) is open, mergeable and not ready: two unresolved threads, one of them a security thread whose suggested remedy does not work (INV-008). #541 clears the only red test and does not touch #539's files.
- **Actions, in order**:
  1. **INV-008 first, blocking. UNRESOLVED.** Facts (probe experiment, temp repo, git 2.47.3, the sweep's exact argv `git --no-optional-locks -C <wt> status --porcelain=v1 -z --branch --untracked-files=all`, `GIT_OPTIONAL_LOCKS=0`): with `core.fsmonitor=<hook>` and `filter.probe.clean=<cmd>` (`* filter=probe` in `.gitattributes`) set once in the shared repo config and one linked worktree, both the fsmonitor hook and the clean filter ran; with `-c core.fsmonitor=false` the hook did not run and the clean filter still did. So a filter to the selected repository does not protect the at least 18 of 29 listed worktrees that share one `.git/config`, and the thread's remedy is not one flag. Code: `probes.py:305-327`, `:1203-1214`, `:1255`. The owner chooses (Q1): (F1) a fix that neutralises both keys; or (F2) refusing a worktree that defines them, reported as an `unscanned` source row so no JSON key is added; or (F3) accepting the finding. F1 and F2 are an allow-list and test change, not a one-liner: `ALLOWED_GIT` is an exact one-entry list (`probes.py:64-67`) under the owner-signed allow-list (NFR-014), and `tests/sweep/test_probes_allowlist.py:503`, `tests/sweep/test_readonly.py:85,156,453` pin the argv prefix (INV-009). Filtering `paths` to one repo also changes the contract allow-list and transcript scans, which share the same `paths` (`probes.py:1255-1263`, `:1301`) and turns a contract in another repo's worktree into "outside root", the failure Codex thread 623cm5 describes; so the git-status scope must be separated from the contract allow-list, and the golden tests that change must be named (INV-039). Keep the probe experiment as the regression test. F3: the four statements that say read-only or "changes nothing else" must then carry a caveat in the same PR: `HOW-WE-WORK.md:335` and `:406`, `sc-sweep-protocol/SKILL.md:3` and `:15` (INV-010); the ruling must say which premise it relies on (`SECURITY.md:L166-L170`; counterweight: every session on this image runs permission-free, INV-011, so the "lower-privileged agent" premise may not hold here). Recommended answer: F1 or F2 (about 70 percent; PLAN INFERENCE from the probe's stated action, not a debate verdict). The design of the fix belongs to the #539 author and the owner; this document states the requirement, not the code. [Decision: Q1 (F1 or F2, about 70 percent, default with no debate verdict). Waits for: the owner's ruling. Unblocks: the #539 merge. Undo: a fix, yes; an acceptance is reversible only before merge.]
  2. **Resolve the Augment thread** (`probes.py:1052`, filtered count under-reads a page) with no new JSON key: Orca replies already carry `page.hasMore`, `page.total` and `page.limit`, and `probes.py:1046-1056` already ORs `hasMore` with `len(filtered) >= 100` (INV-040). [Decision: none. Waits for: the #539 author. Unblocks: the #539 merge. Undo: yes.]
  3. **Merge #541 first** (one file, CLEAN, six checks pass). It makes master green for one commit; any later edit of the CLAUDE.md bullet it pins fails the test again (INV-033). That is not a reason to hold #541. [Decision: none. Waits for: nothing. Unblocks: clean CI for #539 and the guard-flip PR. Undo: yes, revert.]
  4. **Refresh #539's merge commit** with a push (action 1 or 2 is one), an update-branch merge, or a close and reopen. A CI re-run alone keeps the old merge ref (`8c689986 = Merge 873599d59 into d2d8a2d16`) and fails on the same test (INV-037; GitHub docs: a re-run keeps the original `GITHUB_SHA` and `GITHUB_REF`). [Decision: none. Waits for: #541. Unblocks: the #539 merge. Undo: yes.]
  5. **Add no JSON keys and no files inside #539**: key additions change pinned golden sets (`ROW_KEYS`, `test_report.py:1255`; design `:599`), a sidecar file breaks NFR-001. Log wording and key items in #534 (A-004). [Decision: Q9 (persistence is Phase 2). Waits for: nothing. Unblocks: a clean #539. Undo: yes.]
  6. **Sweep wording to fix after #539 merges**, logged in #534 now: design 7.5 ("copied from #409 ... because #409 is unmerged": false since `9e2608b03`), design section 17 item 5 and line 559 (cursor field "open"; the capture already recorded `nextCursor` and `hasMore`), and `report.py:199,534`. Replacement text for the two lines (R2-V5 5.8): "This command reads no messages. A plain `check` consumes them. Whether `check --all --types question` consumes on a live Run is not established." This replaces V5's withdrawn O-05 rewording. [Decision: Q10 (observer's alone for now). Waits for: #539 merged. Unblocks: accurate sweep text. Undo: yes.]
  7. **#339 itself**: no body edit; one comment (Part 6.4). Phase 1 follow-ups get one table in #534: item, owner, trigger (A-005). [Decision: none. Waits for: nothing. Unblocks: #423 rewrite. Undo: yes.]
  8. **Smaller items the probe adds**: a pinned test that no other worker-written field reaches the report (INV-015; today only `blocked_question` prints, through `cell()`, `report.py:258`); state "first 50 in Orca list order" for the `worker-show` cap (INV-019, `probes.py:115,1114,1171`); the sweep's version check compares only the text before the first hyphen (INV-020). [Decision: none. Waits for: #539 merged. Unblocks: none. Undo: yes.]
- **Do not**: edit #539 for wording or alignment; add keys or a sidecar; claim "read-only" without saying "toward Orca" until INV-008 is ruled (A-006, 90%).
- **Owner questions**: Q1, Q9, Q10, Q11.

### 2.3 The integration contract between the sweep and the observer

<!-- Source: Variant 5 (round2-rebuttal-V5.md), Section 5.1 to 5.8, with additions from V2 W-10, V4 5.2 and invariant rows INV-006, INV-013, INV-017 to INV-020, INV-023, INV-028, INV-031, INV-035, INV-042 (shown in italics) - merged per Change #6. The note is described here; this document does not create it -->

- **Points covered**: X-006, X-008, X-009, A-001, A-002, A-009, A-012, A-014; probe findings INV-006, INV-013, INV-017 to INV-020, INV-023, INV-028, INV-031, INV-035, INV-042.
- **Verdict**: one short written note, no runtime link in version 1: neither program reads the other, neither gains a file or key (R2-V5 5.1). This is "the main product of the debate": three other variants' proposals (V3's status record, V4's field list, V1's mapping table) now depend on it (R2-V5 section 2, "Net effect").
- **Content of the note (from R2-V5 5.2 to 5.8; the probe's additions are in italics)**:
  - **File and owner.** `docs/designs/observe-sweep-contract.md`, tracked and shipped (not under `.dev/`). Owner: the Orchestrator mode design (#339), because the sweep JSON is the stricter contract (golden-tested key set). The observer spec (`.dev/issues/409/bmad/spec-orca-observer/release-gates.md`, `adapter-contract.md`) and `docs/designs/orchestrator-mode.md` section 1 link to it and do not restate its tables. *Which branch carries the draft: this checkout `ironbelly/issue-339-orchestrator-mode` IS PR #539's head, so a note committed here joins the PR; draft on a master-based branch (INV-031); links into `orchestrator-mode.md` wait for #539 to merge.*
  - **Amendment rule.** A change to a shared word, the join key, either schema version, or an Orca verb either program may call edits the note in the same PR. *The rule needs a test: one test that compares the note's Orca verb lists, schema versions, join key and shared words with `ALLOWED_ORCA`, the observer templates, `SCHEMA_VERSION` and the report constants; today no test reads any design document (INV-042).*
  - **Registry of contracts** so nobody says "the JSON v1" again: observe snapshot v1, sweep report JSON v1, the watcher's `status --json` (no `schema_version`) and `dispatch.json` v1, and any future v2 or Coder#477 status record. The note governs only the first two.
  - **Units** (R2-V5 5.3; table below): observer = all Runs on one host, up to 5 calls x 100 rows per 15 s cycle, PARTIAL beyond; *PARTIAL is the steady state on this host (513 rows) and newest-first order is an observation, not a contract (INV-017); with `--questions` a cycle can make 6 calls (INV-018)*; sweep = rows for the bound Run, `worktrees[]` and transcript scans host-global; `worker-show` for at most 50 *in Orca list order* (INV-019); Run-less sessions (watcher-launched, person-started) not observable by either program today. Write also "single owner, single OS user, single host" once (A-007).
  - **What each publishes for the other: nothing new in version 1.** Rules for what exists: the snapshot is last-writer-wins and stays on disk after the process exits (no pid, no liveness flag; `export.py:26`), so a reader applies its own age rule to `generatedAt` and shows an old file as stale (*the age threshold is the owner's number, Q22; INV-004*); the sweep's JSON is stdout-only, so a caller that wants it captures stdout and nobody re-runs the sweep; all strings from either program are untrusted input to a reader (two sanitizers: `sanitize.py` and `report.py:563-598`). *The two programs resolve `XDG_STATE_HOME` differently: the observer accepts it only when absolute (`export.py:241-242`), the sweep uses any non-empty value (`probes.py:1264-1266`); list both paths (INV-006).*
  - **Versioning** (R2-V5 5.5): always "observe snapshot v1" and "sweep report JSON v1"; adding an optional key stays v1 with a deliberate test change in the owner program's PR; rename, remove or change meaning is v2; consumers ignore unknown keys and never validate against a frozen copy of the producer's schema (INV-035: closes the cross-program case). **Join key:** `dispatchId` (observer) equals the part of `row_id` after `orca:` (sweep); structural basis verified (`probes.py:435`, `classify.py:891`) but not compared on real ids (D-3), so the note calls it a join key only after one comparison; *join on `runId` plus `dispatchId` and exclude empty or duplicate-flagged rows (sweep `NOTE_DUPLICATE_DISPATCH`, `classify.py:893-896`; only ids matching `ctx_[0-9a-f]{12}` reach `worker-show`; INV-028)*.
  - **Mapping table of shared words** (R2-V5 5.6; table below): stale, unknown, unavailable, could not determine, historical, frozen, settled, "coordinator question" versus "waiting on a person". *Add a `reclaimable` row: the observer's `HISTORICAL_STATES` is released and retained only (`view.py:35`) while Orca counts reclaimable separately (live first page: reclaimable 27, released 41, retained 32, active 0), so reclaimable rows stay in the observer's default view and the sweep derives "settled" from `outcome` (`classify.py:98,114,781-786`); the note decides which side of "historical" it is (Q23; INV-023).*
  - **Verb lists per caller**: observer 3 argv shapes (one `check --all --types question --run <id> --json` template behind the guard), sweep 10 exact templates over 7 verbs (owner-signed, NFR-014; `check` forbidden), watcher `skills list --json` plus `agent launch` (a write verb that starts an agent; so "read-only" is per caller, not per program pair; R2-V2 section 2). *The observer is for a person or a coordinator only: WORKER-CONTRACT.md:23 lists slash commands, and `observe` is a plain CLI whose unscoped `worker-list` is not fenced; one line "person only" in the routing row and the note (INV-013).* Binary resolution: observer and watcher use `_find_orca`; the sweep uses `$ORCA_CLI_COMMAND` else `orca-ide`; no host with both names was shown, so a note, not a risk row (INV-016; bare `orca` for the observer is Q13).
  - **`projection.attention{categories, requiresAction}`**: neither program reads it (verified now: only in observer fixtures). After the shared live capture (D-8), the observer may show it verbatim; the sweep does not read it in Phase 1; neither classifies from it until its values for live and blocked workers are recorded (R2-V5 5.8).
  - ***Record the Orca build string next to each capture; the sweep's check cannot tell two builds apart (INV-020; A-009 unresolved).***
- **Units and facts each program owns (R2-V5 5.3, carried verbatim)**:

| Subject | Observer (`superclaude observe`) | Sweep (`superclaude sweep run`) |
|---|---|---|
| Unit | all Runs on one host; up to 5 calls x 100 rows per 15 s cycle; PARTIAL beyond | rows for the bound Run; worktrees and transcript scans are host-global |
| Orca ledger facts (state, outcome, liveness, next action, evidence age) | owns; verbatim Orca words | reads per Run, `worker-show` for at most 50, 90 s budget; classifies with proof |
| Git, contracts, transcripts, `safe_to_close`, frozen plans, Task specs | none | owns |
| Coordinator questions (Orca message rows) | owns, one named Run, behind a guard that is False on master | none; `check` is forbidden |
| Sessions with no Run (watcher-launched, person-started) | not observable | transcript rows only, `could not determine` today |
| Orca binary resolution | `orca-ide` then `orca`, accepted only if `skills list --json` names `orca-cli` | `$ORCA_CLI_COMMAND` else `orca-ide`, never bare `orca` |
| Files written | `snapshot.json` and `observe-<stamp>.txt` under `$XDG_STATE_HOME/superclaude/observe/`, mode 0600 | one dated report under `<root>/.dev/sweeps/` |

- **Mapping table of shared words (R2-V5 5.6, carried verbatim; the `reclaimable` row is the invariant probe's addition, INV-023, and is not part of R2-V5)**:

| Word | Observer | Sweep | Rule |
|---|---|---|---|
| stale | its own feed: no good read for 45 s (`STALE_SECONDS = 45.0`, `view.py`); also a snapshot file judged by `generatedAt` | a transcript-only row older than the 6 h window (V1 F-02, `classify.py` freshness) | say "feed stale" or "session stale"; never show one as the other |
| unknown | the string `UNKNOWN` in JSON and on screen | `null` in JSON, `unknown` in text | `unknown` never becomes `not admitted`, `not frozen` or `no issue observed` |
| unavailable | `unavailable (no source)`: the program does not read the fact (report status, acceptance, tests, approval, SETTLED, POLICY FROZEN, cost) | `unavailable`: a source it tried and could not read | "no source" means not collected here, not false |
| could not determine | no counterpart (it classifies nothing) | a class and a `safe_to_close` value when proof is missing | if a panel ever shows sweep rows it prints the sweep's words verbatim and labels the report age |
| historical | Orca `terminalState` in (`released`, `retained`), hidden behind `h` (`HISTORICAL_STATES`, verified now) | a row older than the window when the list is complete (design FR-010) | label which program's meaning |
| frozen | `POLICY FROZEN` printed `unavailable (no source)` | `policy_of` returns `frozen` only from a blocked or failed worker contract with stop codes (`classify.py:377-392`, verified now) | the observer never prints `not frozen` |
| settled | `SETTLED` printed `unavailable (no source)`; Orca `outcome` shown verbatim | `_settled(orca)`: Orca outcome in `_SETTLED_OUTCOMES` (`classify.py:113-114`, verified now) | the observer shows the Orca word, not a derived verdict |
| coordinator question versus waiting on a person | Orca message rows of type `question` for one Run, labelled "coordinator questions", never "human" (owner decision 8, 2026-11-11) | "Waiting on a person" from blocked return contracts (and an inert agent-wait rule), plus frozen plans | neither implies the other is empty; both print "seen, not resolved"; fix #409 acceptance criterion 2, which still says "human attention items" |
| reclaimable (ADDED, INV-023; the note decides the side) | not in `HISTORICAL_STATES` (released and retained only, `view.py:35`), so reclaimable rows stay in the default view | settled is derived from Orca `outcome` (`classify.py:98,114,781-786`); historical from the 6 h window | the note decides which side of "historical" `reclaimable` is (Q23); until then show Orca's word `reclaimable` and do not call it live or historical |

- **Do not**: add keys or a file to either program for the note's sake; name anything a "join key" before the one real-id comparison (D-3); call either JSON "the JSON v1".
- **Actions**: draft the note on a master-based branch (Part 4 step 6), add its one comparison test (INV-042), run the one join-key comparison (JOIN, Q24) before the words "join key" appear. [Decision: Q5 (one note, keep both programs), Q24 (the 409 session runs the comparison). Waits for: #539 merged for links; JOIN for the wording. Unblocks: #409 wording, V3 status record, V4 field list. Undo: yes, remove file and test.]
- **Owner questions**: Q5, Q9, Q13, Q17, Q22, Q23, Q24.

### 2.4 Issue watcher (#331, rollout #450)

<!-- Source: Variant 2 (variant-2-original.md), findings W-01 to W-16 and "Proposed edits to #450", with round2-rebuttal-V2.md sections 3 and 5 and invariant rows INV-007, INV-011, INV-012, INV-016, INV-034 - merged per Change #7. The FU-1 precondition list is the probe's addition (INV-012 is absent from the one-paragraph consensus) -->

- **Points covered**: X-001, X-003, A-008, A-009 (watcher fixtures), plus V2 W-01 to W-16; probe findings INV-007, INV-011, INV-012, INV-016, INV-034.
- **Verdict**: partly aligned, and FU-1 (the first live test) is not ready to run as written. Two contradictions: the fixed prompt triggers the claim's default `worktree` pipeline against the design's "claim stops at `next-steps.md`" (W-01, W-02); #409 and Coder#477 picture a coordinator that the watcher design does not use (W-06). A watcher session is Run-less, unowned and unrecorded: the watcher keeps only an Orca operation id (W-03, W-04, W-05). Aligned and safe as built: plain-process launch, WC-13, never-as-worker, claim-marker detection, read-only `status` (W-13 to W-15).
- **Actions, in order**:
  1. **Owner decides the claim level** (Q2). Recommended `--pipeline none` (claim ends after the comments, no worktree, no second agent: exactly design decision D2). Code touched: `launch.PROMPT_PATTERN` (`launch.py:33`), `build_claim_prompt` (`:84-92`), the 12-element argv pin, `retry_argv`, the NFR-001 property test, runbook strings: one small PR, no overlap with #539. If the owner keeps the default: record it as a deliberate chain and require OB-H1 item 1, OB-H2, OB-H3 (#394) as a precondition (W-02). [Decision: Q2 (`--pipeline none`). Waits for: the owner. Unblocks: #450 edits, FU-1, #423 and Coder#477 text. Undo: yes, a small PR.]
  2. **FU-1 preconditions (explicit, from INV-012 and INV-011, which the one-paragraph consensus lacked)**: (a) the claim level recorded; (b) the owner accepts in writing the permission mode of the first session: `--pipeline none` removes only the second agent; the first session still assigns the issue, posts comments and runs the accuracy check over untrusted issue text, and on this host runs with permission checks off; (c) FU-1 records `CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS` and the real argv of the launched session (`ccsession:134-141`: a non-empty `CC_CLAUDE_FLAGS` replaces the flags); (d) before and after `run-list` and `worker-list` around one real `agent launch` (D-A); (e) one `worktree ps --json` agent row after the launch: does `prompt` hold `/sc:issue --claim N`, does `paneKey` equal a tab-map name (D-B); (f) the real launch-reply operation-id path (`OPERATION_ID_PATHS`, `launch.py:39-45`, a guess pinned by four `_assumed_shape` fixtures; a wrong path makes every correct launch `unknown`); (g) Orca build string (A-009); (h) the ccsession tab-map entry and whether the session stalls at the Session Name prompt (W-09); (i) the list of writes the test makes (assignment, two marked comments, ClickUp script if its env is set, `.dev/issues/<N>/` files) and closing or unlabelling the test issue, because the order "claim first, then label" can make the enabled watcher claim it again (R2-V2 5.6). The permission-mode facts are verified on this host only (INV-011); other hosts are UNVERIFIED. [Decision: Q2 (second part: accept the session mode in writing, for the test issue only). Waits for: action 1. Unblocks: FU-1, then the cron enable (FU-2). Undo: by hand, except ClickUp (unknown).]
  3. **Runbook**: add step 1.3a (create the watcher worktree with `orca worktree create --name issue-watch --agent claude --prompt "<task>"` as a person and name who owns its agent; W-07); add that `reset --forfeit-guarantee` on an `unknown` entry first requires checking Orca for a live session in the configured worktree (R2-V2 5.4; INV-007 handled). [Decision: Q20 (a named person owns it). Waits for: Q20. Unblocks: a safe runbook. Undo: yes.]
  4. **Machine-started sessions get a #534 row after FU-1** (W-05, A-005); the sweep may label them only after D-B. [Decision: Q21 (yes, Phase 2, after FU-1). Waits for: FU-1. Unblocks: the label in #534. Undo: yes.]
  5. **Do not add a watcher panel to `observe`, and do not route watcher prompts through a listener, until FU-1 is recorded** (W-10 reworded). [Decision: none. Waits for: FU-1. Unblocks: reconsidering W-10. Undo: yes.]
- **Owner questions**: Q2, Q3, Q20, Q21.

### 2.5 Coder#477 (workspace listener)

<!-- Source: Variant 3 (variant-3-original.md), findings F1, F2, F6, F8, F10 to F14, F17, with round2-rebuttal-V3.md sections 5.1 to 5.7 and invariant row INV-043 - merged per Change #8. Coder-repo facts rest on V3 alone and are marked "per V3" -->

- **Points covered**: X-001 family, X-004 (V3 Edit 5), X-005, A-002 (workspace unit), A-007; V3 F1, F2, F6, F8, F10 to F14, F17; probe finding INV-043.
- **Verdict**: do not build a listener for the watcher (E-12). Recommended: narrow #477 to read-only workspace status and identity with no prompt routing, about 65 percent, after the owner answers Q3 and Q4; close it (with the reopen conditions in text C of Part 6.3) if the observer stays single-host and TUIBBS is not near; keep as written is the least defensible. Narrowing or closing does not choose what "TUI Panel" means (INV-043).
- **Facts to carry (per V3 unless a source is named)**: identity and running state come from Coder (workspace id, owner, name, build status, last connected), not from a value the workspace reports about itself; key by workspace id, never by name; the existing heartbeat collector is anonymous (`collector/app.py:5`) and cannot be reused; any route that can start a session starts it with permission checks off on the stock image (`README.md:60-66`, `ccsession:135-141`), which is the strongest reason the narrowed version has no send route; a listener runs inside the workspace and cannot start a stopped one (R2-V3 5.1); "its project's orchestrator" is not an address (#339 accuracy check row 3); expose only the allowed list and never the "never exposed" list (R2-V3 5.3); the nine-item checklist in R2-V3 5.7 applies to any version.
- **Actions**: post text A, B or C from Part 6.3 once the owner has answered. [Decision: Q3 (narrow), Q4 (what "TUI Panel" means), Q18 (no snapshot-copy channel yet), Q22 (the age number). Waits for: Q3, Q4 (Part 4 step 7). Unblocks: nothing in IronClaude. Undo: yes, edit or reopen.]
- **Rewrites**: Part 6.3 (R2-V3 section 5.6, texts A narrow, B keep, C close) states which parts are paste-ready.
- **Owner questions**: Q3, Q4, Q18, Q22.

### 2.6 Orchestrator v2 (#423) and the trust design

<!-- Source: Variant 4 (variant-4-original.md), findings F1, F7, F9, F14, with round2-rebuttal-V4.md sections 5.1 to 5.7 and invariant row INV-021 - merged per Change #9. Only items that survived Round 2 enter (V4's weighted survival is 0.818, the lowest of the five) -->

- **Points covered**: X-002, X-005, A-007, A-005; V4 F1, F7, F9, F14; probe finding INV-021.
- **Verdict**: "v2" has at least three meanings (E-13): the #339 issue summary's v2 (signed grants plus an orchestrator of orchestrators), the research report's phases 2 to 6, and #423's knowledge layer. #423's gate ("after #339 is complete") has two readings and cannot be applied as written. Recommended gate: PR #539 merged plus the #534 live capture that restores the sweep's `working` class; `/sc:close`, resume and the trust layer are not prerequisites unless the brainstorm decides that v2 relays to agents and not only to a person. v2 is advisory, in a separate command or skill (the sweep "recommends nothing": WC-16, `WORKER-CONTRACT.md:288`), delivers to the person or the coordinator only, and keeps LLM-derived entries marked inferred and apart from sweep facts (V4 F14, supported by V5 as U-008).
- **Trust (X-005, 66 percent, owner decision)**: promise one grant vocabulary and one audit record format, not one trust design; the three consumers have different threat models and signing does not stop poisoned content (#339 comment 2: "encryption alone is not enough"). Recommended: one vocabulary (Q16).
- **Facts to carry**: a catalogue is at least an eighth data store (R2-V4 5.2: sweep report, observer snapshot, watcher store, PM memory, lessons learned, task ledgers, heartbeat collector, plus the catalogue); it needs a named store, owner, reader set, retention, file mode and a reconciliation with WC-16 ("a dated local file; it is never posted"); first release reads only what the same OS user on the same host can read, no transcript or log content enters the catalogue, no cross-user or cross-workspace read without a written read-permission model (R2-V4 5.3); relayed content is data: fixed typed fields, free text only in one `detail` field, a pinned set tested like the sweep's key set, relay through the coordinator because the contract has no worker-to-worker channel, summarisers read-only (5.4); the sweep sections of #423 must say "on PR #539" until it merges (5.5). *The numbering note in #339 also needs the observer's R1 to R4 releases and the watcher's FU-1 to FU-6 (INV-021; PLAN INFERENCE: R2-V4's comment covers three namespaces).*
- **Actions**: post the #339 comment first, then the #423 rewrite (Part 6.4). [Decision: Q14 (PR #539 merged plus the #534 capture), Q15 (report only, advisory), Q16 (one vocabulary). Waits for: the comment on #339; Q14 to Q16; #539 merged and the capture for the start of work (Part 4 step 9). Unblocks: the v2 brainstorm. Undo: yes.]
- **Rewrite**: Part 6.4 (R2-V4 section 5.7: title, body, #339 comment).
- **Owner questions**: Q14, Q15, Q16.

### 2.7 The "TUI panel" question

<!-- Source: Variant 5 (round2-rebuttal-V5.md), Section 5.7, with round2-rebuttal-V3.md Section 5.2 and D-2, and invariant row INV-043 - merged per Change #10 -->

- **Question**: in the owner's comment of 2026-11-13T16:20:07Z on Coder#477 ("Ensure this aligns with Orchestrator and TUI Panel"), what is the TUI panel?
- **Answer (working reading)**: read it as `superclaude observe` (the #409 dashboard) until the owner says otherwise: about 70 percent (R2-V5 5.7) to 75 percent (R2-V3 5.2: the comment's two nouns mirror the titles of #339 and #409; the phrase appears in no owner-written file). A TUIBBS Go screen is the weaker reading, about 15 percent (the owner's 2026-11-08 record: "the observer may become a TUIBBS module", "Background, not deciding"). Both are a sequence, not a conflict: a TUIBBS screen would be a second reader of the observer's snapshot, not a second program with its own collector. Before a TUIBBS screen can read anything, four things are missing: a transport (TUIBBS runs on a separate SSH host; "No document in TUIBBS mentions Coder or Orca", sibling `tuibbs-review/notes-3.md:78-84`), an identity envelope (the snapshot `scope` is only `object` or `"UNKNOWN"`; only per-row `hostId` and `hostKind`), an age rule (no liveness field), and re-sanitising. So Coder#477, if kept, is designed for a read-only, identity-tagged, aged copy of the observer snapshot and not around either screen. The contract holds under all three readings; the answer changes the transport, not the contract.
- **Owner decision**: one line on #477 (Q4). Recommended: "TUI Panel = `superclaude observe`; single-host; read-only". [Decision: Q4. Waits for: the owner. Unblocks: Q3 and the Coder#477 rewrite; nothing in IronClaude. Undo: yes.]
- **Dependencies**: gates Q3 and the Coder#477 rewrite; unblocks nothing in IronClaude.

## Part 3: Point register (every point)

<!-- Source: Base (original, modified) - point register built from the Scoring Matrix and the R2 section 3 tables per Change #11 -->

This part carries all 36 X and A points of the debate, grouped by the same systems as Part 2 (12 + 6 + 9 + 3 + 2 + 4 = 36). The actions that come from the invariant probe are in Part 5. Confidence is the matrix mean (`debate-transcript.md`, Scoring Matrix; the matrix cell text is truncated there, so the evidence column uses the diff-analysis and Round 2 wording). The matrix "winner" is dropped from the output: the verdict states what holds. "Q" ids are the owner questions of Part 7. Reversible: see 0.4.

Columns: **id | verdict | conf. | evidence | decision needed (Q, with recommended answer) | course of action | depends on (first) / unblocks | reversible**.

### 3.1 Observer and #409

<!-- Source: Variant 5 (matrix rows X-012, X-013, X-018, A-003, A-015, A-010, X-011, X-014, X-015, X-016, X-002, A-013) with R2 section 3 verdicts - merged per Change #11 -->

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| X-012 | The observer is built and merged; V1 C-03 and #409 L16 are wrong | 98% | PR #503, #514; `main.py:572-574` | none | correct #409 (BC-02, BC-04, BC-05) | Q8, Q16 before the #409 pass / unblocks the #409 pass | yes |
| X-013 | The observer does not read the sweep JSON; neither program mentions the other | 95% | `commands.py:37,393`; grep of both trees | none | no runtime link in version 1; the contract note links both | none / unblocks the note | yes |
| X-018 | A staged direction was chosen (2026-11-08, 2026-11-11) and releases 1 and 2 shipped; the dated selection record (AC-S) is missing | 74% | owner decisions; PR #503 "Known gaps" | Q8: write the AC-S record | owner writes the record or amends #409 AC 1 (BC-18) | owner / unblocks #409 AC 1 text and any release 3 | yes |
| A-003 | Observer built; only the selection record is open (replaces "owner will choose a design") | 96% | as X-018 | Q8 | same as X-018 | as X-018 | yes |
| A-015 | Owner decisions are not where reviewers can read them (master holds only `owner-decisions-20261111.md`) | 83% | `git ls-tree origin/master .dev/issues/409/`; INV-002 | Q7: commit or archive them (yes) | owner commits `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`; the flip PR commits the pass record | before the sibling worktree is cleaned / unblocks the flip PR | yes |
| A-010 | The reviewed text moves (#409 body 30,030 to 30,758 bytes; sibling HEAD moved; `409-Phase2` deleted) | 93% | SC-18; INV-030 | none | pin every cite to sha or `updatedAt`; re-read `updatedAt` before each write; abort on change; keep the before-body beside the edit set | none / gates every issue edit | yes |
| X-011 | V1's "observer needs a refresh interval for the file" and V4's "second scheduler" premises are both weakened: the observer polls on its own | 74% | `collector.py` INTERVAL 15.0, MAX_BACKOFF 60.0, STALE 45 s | none | drop both premises; say in the sweep design that an observer polling at 15 s runs beside it (O-10) | none / none | yes |
| X-014 | Fleet scale is closed for the Orca ledger on one host, open for the sweep's per-Run depth and for multi-host; this host is already past the cap | 79% | `adapter.py:57`; INV-017 (513 rows) | none | do not add V1's W-3; state "per-Run depth is the sweep's job; PARTIAL is the steady state" in the note | none / none | yes |
| X-015 | The observer already runs its own 15 s poller beside the sweep; several observers multiply load; simultaneous load never measured | 87% | `collector.py`; `commands.py:84-85`; INV-032 | none | record the load note; `PER_CALL_TIMEOUT` stays UNVERIFIED until the first permitted live read | none / none | yes |
| X-016 | **UNRESOLVED.** UNPROVEN BOTH WAYS whether `check --all --types question` consumes on a live coordinator Run; Orca's help says `--all` does not mark read | 61% | `owner-decisions-20261111.md:13-15`; `release-gates.md:36-50`; INV-041 | Q6: no scope answer, no flip | seeded test (Part 2.1 action 4), cite the help text, pin the build; the sweep keeps its caution and its wording is corrected (Part 2.2 action 6) | the test / unblocks the flip PR | yes |
| X-002 | The boundary sentence "observer shows the human what happened, v2 shares knowledge between agents" is not stated in the #409 body before decision 8; the weaker "distinct from" holds | 81% | `/tmp/pr339/i409-new-body.md:116,209`; V1 C-34 | none | relabel "proposed boundary (not yet stated in this issue)" (V1 W-7); #423 states the boundary itself | the #409 pass / none | yes |
| A-013 | Polling Orca read verbs is the only verified source; event replay unverified; `projection.attention` read by neither program | 65% | `orca-ide orchestration --help` lists 30 verbs, none streams | Q24: who runs the shared read-only capture | add to the shared capture: attention values of one live and one blocked worker, the `worktree ps` agent row of a Run-less session, Orca's event surface in help text only | live Orca / unblocks the sweep's `working` class (#534), V5's open items O-13 and O-14, and the #423 gate | yes |

### 3.2 Sweep, #339 and PR #539

<!-- Source: Variant 1 (matrix rows A-004, X-007, A-006, X-004, X-010) and Variant 5 (A-005) with R2 section 3 verdicts - merged per Change #11 -->

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| A-004 | PR #539 will change (two unresolved threads); added keys change pinned golden sets; a sidecar breaks NFR-001 | 88% | GraphQL threads; `ROW_KEYS`; `test_cli_contract.py:1474`; INV-022 | Q1 (INV-008) | resolve both threads; add no keys or files; log items in #534; merge #541 first; refresh the merge ref by push | #541, Q1 / unblocks the routing row, note links, #534 edits | yes |
| X-007 | The sweep's reads are not confined: `git status` runs in every `worktree ps` path with the inherited environment; V4's "confines every path" holds for file reads only | 89% | `probes.py:305-327,1203-1214`; INV-008 | Q1: fix (F1 or F2) rather than accept | Part 2.2 action 1 | Q1 / blocks the #539 merge | yes before merge |
| A-006 | "Read-only" holds toward Orca only: the sweep writes one report and runs git with inherited env; the observer writes snapshot files and one `check` template | 90% | `probes.py:309`; O-11 | Q1 (via INV-010) | say "no Orca write verb" and list the files each program writes; caveat four texts if the owner accepts | Q1 / none | yes |
| X-004 | `sweep run` always writes a dated report before printing JSON, so a "no write" status criterion cannot be met | 91% | `commands.py:186,277-278` | Q9: persistence is Phase 2 | drop V3 Edit 5; the first status record is the observer snapshot | none / unblocks the Coder#477 text | yes |
| X-010 | The sweep's rows are per Run but `worktrees[]` and transcripts are host-global | 85% | `probes.py:1203-1214` | none | state the host-global scope in the note and the sweep unit line | none / none | yes |
| A-005 | Nobody defends "Phase 2 and #534 will absorb the deferred items": only a reading list exists; observer R3 and R4 have no package | 85% | `PHASE2-preflight-input.md`; V5 section 10 | none | one table in #534: item, owner, trigger; unowned items labelled "unowned"; rows from R2-V5 A-005 (sweep JSON persistence, machine-started label, guard flip, relationship note, routing row, observer R3 and R4) plus V3's three (identity block, read-only status route, label) | #539 merged / none | yes |

### 3.3 The integration contract

<!-- Source: Variant 5 (matrix rows A-014, X-008, X-009, X-006, X-017, A-001, A-002, A-009, A-012) with Variant 1 F-02 and R2 section 3 verdicts - merged per Change #11 -->

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| A-014 | Two JSON "v1" schemas exist | 94% | `snapshot.schema.json`; design 7.4 | none | always "observe snapshot v1" and "sweep report JSON v1" | none / the contract note | yes |
| X-008 | V1's verdict line is wrong; its F-02 table is right; the built observer shows none of the ten dimension names; three vocabularies | 91% | `view.py:96,412`; V1 F-02 | none | drop the verdict sentence; publish the mapping table | none / the note | yes |
| X-009 | V1's tally miscounts; nothing depends on it | 95% | by inspection | none | none | none | n/a |
| X-006 | Two decisions: sweep JSON keys (decide in #339 after #539 merges) and snapshot changes (observer spec, additive); the note comes first and names all contracts and the join key; the join key is plausible but not compared on real ids | 74% | `classify.py:891`; `probes.py:435`; D-3 | Q24: run the one comparison | note first; keys decided in #339 after #539; comparison before the word "join key" | #539 merged for keys / unblocks the note wording | yes |
| X-017 | Keep two readers (observer, sweep), not one collector; V1's persistence idea survives only for an optional later panel | 70% | O-01; V5 D1 | Q5: yes, keep two | contract note; persistence stays Phase 2 | Q5 / none | yes |
| A-001 | Sweep JSON v1 is a candidate carrier only for v2 and for a Coder#477 status record, not for the observer | 78% | X-013 | Q17: no observer panel for sweep facts now | record in the note; v2 names its field list first | Q17, D-2 (when may the sweep JSON be stored) / none | yes |
| A-002 | The unit differs by program (sweep: bound Run plus host-global worktrees and transcripts; observer: all Runs on one host; watcher: one workspace; Coder: workspace id); Run-less sessions are in neither ledger | 82% | `probes.py:1203-1214`; `adapter.py` | none | one line per unit in the note; "Run-less sessions: not observable by either program today" | the note / none | yes |
| A-009 | **UNRESOLVED by evidence.** The observer's golden capture records no Orca version; design lock `.780594c521aa` against host `.9cfecdd30b2a`; the sweep compares only the text before the first hyphen; watcher launch shapes assumed until FU-1 | 67% | INV-020; `report.py:160` | none | record `orca --version` in the observer golden capture, the sweep lock line, the FU-1 record and every future v2 fact; treat a second host as UNVERIFIED | live Orca / none | yes |
| A-012 | Keep both programs (provisional); only V5 states it and asks the owner | 66% | V5 D1 | Q5 | proceed as provisional; ask once | Q5 / gates the note | yes |

### 3.4 Issue watcher

<!-- Source: Variant 2 (matrix rows X-001, X-003, A-008) with round2-rebuttal-V2.md verdicts - merged per Change #11 -->

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| X-001 | CONFIRMED contradiction: the watcher prompt has no `--pipeline`, so the claim runs at default `worktree` and starts a governed second agent; V3 Edit 8 and V4 C7 and F11 omit it | 91% | `issue.md:43,88`; `launch.py:33`; `issue-watcher.md:44` | Q2: `--pipeline none` plus the owner accepts the session mode in writing | Part 2.4 actions 1 and 2 | Q2 / unblocks the #450 edits, FU-1, and the #423 and Coder#477 text | yes (small PR) |
| X-003 | A watcher-started session is Run-less; today the sweep prints `could not determine`, later possibly "person session (active)"; V4's per-class acceptance criterion cannot be met until #534 gets a row | 78% | `classify.py:302-315,748-767` | Q21: yes, label after FU-1 | reword #409 decision 9 (V2 W-05(a)); #534 row (W-05(b)) | FU-1 D-B / none | yes |
| A-008 | The sweep needs a bound Run and a WC-16 pass; the observer ledger needs neither but sees only orchestration Workers; watcher-launched and person-started sessions are a blind spot in both; "no Run record for `agent launch`" is still inference | 83% | `WORKER-CONTRACT.md:288`; `classify.py:748-767` | none | name the blind spot in both docs; settle at FU-1 (D-A) | FU-1 / none | yes |

### 3.5 Coder#477, #423 and trust

<!-- Source: Variants 3 and 4 (matrix rows X-005, A-007) with round2-rebuttal-V3.md and round2-rebuttal-V4.md verdicts - merged per Change #11 -->

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| X-005 | One grant vocabulary and one audit record format, not one trust design; not decidable from sources | 66% | #339 comment 2; V4 F9; V3 F12 | Q16: one vocabulary | do not promise one design in #409 or #423; #409 decision 6 wording (V4 edit 1) only if Q16 = vocabulary | Q16 / #409 decision 6, #423 | yes |
| A-007 | True today: one owner, one OS user, one host, one enabled watcher per login; the live exposure is untrusted repo and issue content more than other users | 77% | `issue-watcher-setup.md:642`; `probes.py:305-327` | none | state it once in the note and in Coder#477; read-permission acceptance criterion before v2 or Coder#477 reads another workspace; treat Orca-listed worktrees as untrusted for git | the note / none | yes |

### 3.6 Process points

<!-- Source: Base (original, modified) - process points A-011, A-016, X-019, X-020 per Change #11 -->

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| A-011 | Five reports edit the same #409 sentences; edits must be one ordered set | 92% | S-006, X-002 | none | one editor, one ordered edit set per issue; order in Part 4.2 | none / gates every issue edit | yes |
| A-016 | Reading the issue text and the branch is not enough to find every implementation (the observer sat in the review checkout) | 91% | `main.py`; U-011 | none | before any review says "not built": grep the CLI registration, `git log`, merged PR list | none / none | yes |
| X-019 | V5 overgeneralised: V1 stated no observer exists; V2 W-10 and V4 F13 assumed it; V3 wrote generically and did not check | 87% | R1-V5 concession 7 | none | cite exactly that sentence | none / none | yes |
| X-020 | W-3 is V1's proposed wording, not #409 body text | 94% | SC-19 | none | read V5 RT-F04 as "do not add V1's W-3"; no body edit | none / none | yes |

## Part 4: Dependency graph and merge or implementation order

### 4.1 Dependency graph (text)

<!-- Source: Variant 5 (round2-rebuttal-V5.md, Section 5.9) corrected by invariant rows INV-001, INV-002, INV-029, INV-031, INV-033, INV-036, INV-037 and the A-011 row of round2-rebuttal-V4.md / round2-rebuttal-V1.md - merged per Change #12; replaces V5's "Dependencies for integrating Orchestrator mode with observe" table -->

Nodes: **R** = INV-008 owner ruling and fix specification; **P541** = PR #541; **P539f** = a push to PR #539 that fixes the two threads (new merge ref); **P539m** = PR #539 merged; **GF** = observer guard-flip PR; **RR** = observer routing row; **CN** = contract note (with its test); **E409** = #409 correction pass; **E450** = #450 edits; **FU1** = the watcher's first live test; **C477** = Coder#477 reply (narrow, keep or close); **E339** = #339 comment; **E423** = #423 rewrite; **T534** = the #534 table and wording fixes; **SEED** = the seeded consumption test; **REC** = owner records committed (pass record, decisions, live test guide); **CAP** = the shared read-only Orca capture (attention values, Run-less agent row, event help); **JOIN** = the one real-id comparison (join key); **QA** = owner answers (Part 7).

```
QA(Q1) -> R -> P539f -> P539m
P541 ------> P539f   (P539 CI is clean only after #541; refresh by push, not by re-run)
P539m --> RR, CN(links), T534(edits to design and report.py), E423(start of work), GF(practically)
QA(Q6) + SEED + REC + live-layout attempt + build pin -> GF
P541 --> GF          (fresh branch off master after #541 so CI is not red)
QA(Q8, Q16) -> E409 -> (decision 6 wording needs Q16; AC 1 wording needs Q8)
QA(Q2) -> E450 -> FU1 -> { cron enable (FU-2), D-A, D-B, W-05 label row in T534, W-10 reconsidered }
QA(Q3, Q4) -> C477
E339 -> E423 ; QA(Q14, Q15, Q16) -> E423
CAP -> { O-13, O-14, #534 `working` class, E423 gate }
JOIN -> CN (the word "join key")
REC -> GF ; REC -> E409 (cites owner records)
Independent of #539 (no shared files): GF, E450, FU1, C477, E339, E409, E423 text.
Shares files with #539: RR (HOW-WE-WORK.md, its plugin mirror, routing-table test, `tests/recommend/test_routing_refresh.py`), CN links (`docs/designs/orchestrator-mode.md` exists only on the #539 branch), T534 edits to design lines and `report.py`.
```

(In the graph, O-13 and O-14 are V5's open items: the meaning of `projection.attention` and the live-worker value names in `worker-show`.)

Sharing check (INV-036): `gh api pulls/539/files` (1003 files) does not include `tests/core/test_claude_md_worktree_rule.py`; #541 changes only that file; the guard flip touches `observe/` only; the one file every later PR also edits is `CHANGELOG.md`, so each PR rebases its own changelog hunk.

### 4.2 Merge and implementation order across the nine named items

<!-- Source: Variant 5 (round2-rebuttal-V5.md, Section 5.9) and Variant 4 (round2-rebuttal-V4.md, A-011 row), corrected by invariant rows INV-013, INV-029, INV-030, INV-031, INV-033, INV-037, INV-038, INV-042 - merged per Change #12 -->

| # | Item | Waits for | Unblocks | Notes and reversibility |
|---|------|-----------|----------|-------------------------|
| 0 | **Owner answers and the INV-008 ruling (R)** | nothing (owner) | everything below | decision only; no code. Q1 to Q4 first. |
| 1 | **PR #541** | nothing | clean CI for #539 and the guard-flip PR (GF) | one file, OPEN, CLEAN, six checks SUCCESS (INV-038). Green for one commit: any later reword of the CLAUDE.md bullet fails the test again (INV-033). Reversible by revert. |
| 2 | **PR #539**: fix push, then merge | #541; R | RR, CN links, T534, E423 start, practical GF | the thread fixes (INV-008 fix, Augment thread) are a push and so give a new merge ref (INV-037); a CI re-run alone does not. Add no keys or files. Two unresolved threads are the PR author's. Reversible by revert PR. |
| 3 | **#409 correction pass (E409)**, then the other issue edits in the cross-issue order below | Q8; Q16 for decision 6; REC | an accurate #409 for every later step | one editor, `updatedAt` re-read immediately before each write (INV-030); can run in parallel with steps 1 and 2 because it touches no code. Reversible by issue history. |
| 4 | **Observer guard-flip PR (GF)** | #541; Q6; SEED; REC; live-layout attempt; build pin; "not passed" text grep | questions panel usable | no file overlap with #539; practically after step 2 because SEED needs live Orca and the owner. `/sc:pr-submit --monitor 3` from a fresh branch off master. Default if Q6 is unanswered: guard stays off. Reversible by flipping the constant back. |
| 5 | **Routing row (RR)** for `superclaude observe` | step 2 (shares four files) | discoverability | not "one row" for the two machine-read tables: `tests/core/test_how_we_work_routing_table.py` needs 8 cells and a resolvable step (`:193-205`), and its other-commands block raises IndexError for a first cell with no backticked slash token and asserts `members == _OTHER_COMMANDS` (`:297-298`); every token needs a command file (`:218,312`). Decide which block carries the row and name the test edits (INV-029); plugin mirror byte-for-byte; add a "person only" line (INV-013). Reversible. |
| 6 | **Contract note (CN)** and its test | step 2 for links; JOIN for the wording "join key"; Q5 | #409 wording, V3 status record, V4 field list | draft on a master-based branch (INV-031); one test comparing its tables with code constants (INV-042). Reversible (remove file and test). |
| 7 | **Coder#477 reply (C477)** | Q3, Q4 | none in IronClaude | text A, B or C from R2-V3 5.6 (Part 6.3). Reversible (edit or reopen). |
| 8 | **#450 edits and FU-1** | Q2; edits first | cron enable; D-A; D-B; #534 label row | FU-1 runs `/sc:issue --claim` on a test issue and writes (Part 2.4 action 2 (i)); it is not read-only. Reversible by hand except ClickUp (unknown). |
| 9 | **#423 rewrite (E423)**, then the work it gates | E339; Q14 to Q16; step 2 and CAP for the start of work | the v2 brainstorm | the rewrite only states the gate; work starts after #539 merged and the #534 capture. Reversible. |

**Cross-issue edit order** (R2-V4 A-011 row, accepted by all five advocates): (1) owner answers (claim level, "TUI Panel", Coder#477 keep, narrow or close, v2 gate); (2) #450; (3) Coder#477; (4) #409 pass (V5 facts plus V1 C-07, C-25, C-34; then decisions 1 and 8; then decision 6 only if Q16 = vocabulary; W-05(a) decision 9 and the W-06 diagram; banner removal last); (5) one #339 comment; (6) #423 rewrite. The relationship note is a document and can be drafted alongside (2) to (4). Sentences are disjoint across issues (R2-V2 A-011 row; R2-V3 A-011 row), so the order is mainly for cross-links.

## Part 5: Invariant probe (the debate's last check)

<!-- Source: invariant-probe.md (all 44 rows and its Summary) - merged per Change #13 -->

Source: `invariant-probe.md` (the Round 2.5 fault-finder, who argued for no variant and tested each "X resolves Y" claim of the consensus against live state and code). It has 44 findings: 16 ADDRESSED (the debate already handled them) and 28 UNADDRESSED; by severity 2 HIGH, 19 MEDIUM, 23 LOW. HIGH and UNADDRESSED: INV-008 only. The probe's own conclusion: the 28 gaps are in the fixes the consensus proposed, not in its direction. "Action lands in" names the Part 2 or Part 4 step that carries the action. Method and limits: read-only on GitHub and on both checkouts; Orca calls were read verbs only (`run-list`, `run-current`, `worker-list`, `worktree ps`, `check --help`, `--version`); no `check` was run and no message was sent; the only writes were the probe file and one temporary git repository under `/tmp`, removed by its own exit trap.

### 5.1 HIGH and MEDIUM findings that nobody addressed (16 rows)

<!-- Source: invariant-probe.md rows INV-008, INV-002, INV-003, INV-005, INV-009, INV-010, INV-011, INV-017, INV-023, INV-024, INV-029, INV-030, INV-037, INV-039, INV-041, INV-042 - merged per Change #13 -->

| id | sev. | what is wrong | action that addresses it | action lands in | depends on / unblocks | reversible |
|----|------|---------------|--------------------------|-----------------|----------------------|------------|
| INV-008 | HIGH. **UNRESOLVED** | The Codex security thread's remedy does not close the git-config hole: `core.fsmonitor` and `filter.*.clean` both run in linked worktrees; `-c core.fsmonitor=false` stops only the first; a repo filter leaves at least 18 of 29 worktrees exposed | before #539 merges: the owner and the #539 author pick a fix that neutralises both keys or refuses a worktree that defines them (`unscanned` source row, no JSON key); accept it is an allow-list and test change; keep the experiment as a regression test; or accept the finding and caveat four texts | Part 2.2 action 1; Part 4 step 0 | Q1 / blocks the #539 merge | a fix, yes; an acceptance is reversible only before merge |
| INV-002 | MED | Evidence for "observer first, TUIBBS later" is untracked files in a sibling worktree (`owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`) | the owner commits or archives them before that worktree is cleaned | Part 2.1 action 3 | Q7 / unblocks citing them | yes |
| INV-003 | MED | The pass record covers one Run (`run_93bfa00cae2b`, an old "Claim issue 375" Run, consumer_generation 3); the guard is one global boolean and `check_run_id` checks syntax only | put "this Run only, or any Run my terminal holds" to the owner and make the code match; no answer means guard off | Part 2.1 action 4 (a) | Q6 / gates GF | yes |
| INV-005 | MED | The seeded test's procedure is unwritten: a tester's terminal must hold no Run; `run-use` on a live coordinator is Q-2, "never tested and forbidden for the observer"; 35 of 53 Runs have consumer_generation 2 or more | write the procedure: plain terminal, `run-create` only, never `run-use`, record `run-current` before and after (precedent: Task 17 sample `run_86013b917868`) | Part 2.1 action 4 (b) | owner or 409 session / gates GF | n/a (a live test that writes seeded messages) |
| INV-009 | MED | The git-config fix is an allow-list change plus three test edits: `test_probes_allowlist.py:503`, `test_readonly.py:85,156,453`, `ALLOWED_GIT` (`probes.py:64-67`), NFR-014 | name them in the fix step; the owner's ruling covers the allow-list edit | Part 2.2 action 1 | Q1 / part of INV-008 | yes |
| INV-010 | MED | If the thread is accepted unchanged, "read-only" or "changes nothing else" still stands in `HOW-WE-WORK.md:335`, `:406`, `sc-sweep-protocol/SKILL.md:3,15`; `/sc:recommend` reads the guide; acceptance is a policy call | the owner ruling states which premise it relies on; if accepted, the four texts get a caveat in the same PR | Part 2.2 action 1 (F3) | Q1 / none | yes |
| INV-011 | MED | Two permission knobs, not one: `CCSESSION_PERMISSIONS=default` and a non-empty `CC_CLAUDE_FLAGS` that replaces the flags whatever it says; on this host both unset and live `claude` runs with `--dangerously-skip-permissions --allowedTools=Grep` | FU-1 records both variables and the real argv of the launched session | Part 2.4 action 2 (c) | Q2 / gates FU-1 | yes |
| INV-017 | MED | The observer is already past its 5-call, 500-row cap on this host (513 rows; only the 13 oldest hidden; order is an observation) | the note says PARTIAL is the steady state and that newest-first order is not a contract | Part 2.3 units | none / none | yes |
| INV-023 | MED | `reclaimable` rows stay in the observer's default view (`HISTORICAL_STATES = ("released", "retained")`, `view.py:35`) while the sweep derives settled from `outcome` and historical from a 6 h window | add a `reclaimable` row to the mapping table and decide which side of "historical" it is | Part 2.3 mapping table | Q23 / none | yes |
| INV-024 | MED | The flipped questions panel may not work for the Runs people point it at: 28 of 53 Runs have no `coordinator_handle`; Q-1 FAIL means only the terminal holding the Run can read; the observer never runs `run-use` | record one live attempt in the real coordinator layout before the flip PR | Part 2.1 action 4 (c) | live Orca / gates GF | n/a |
| INV-029 | MED | The routing row is not one row: the two machine-read tables reject a CLI-only entry (`test_how_we_work_routing_table.py:193-205,297-298,218,312`); #539 edits the same test, `tests/recommend/test_routing_refresh.py:33` and both guide copies | decide which block carries the row; name the test changes in the step | Part 4 step 5 | step 2 / none | yes |
| INV-030 | MED | Issue-body edits have no version check: `gh issue edit` has `--body` and `--body-file` with no etag; #409 `updatedAt` moved after the banner; #423 2026-11-08T10:16:24Z; #339 2026-11-07T11:53:40Z; Coder#477 2026-11-13T16:20:07Z | re-read `updatedAt` immediately before each write; abort on any change; keep the before-body beside the edit set | Part 4 step 3; Part 6 | none / gates all issue edits | yes |
| INV-037 | MED | "#539 needs only a CI re-run after #541" is false: a re-run keeps the old merge ref (`8c689986`) and fails the same test | replace "re-run CI" with "push or update the branch" (or close and reopen) | Part 2.2 action 4 | #541 / unblocks the #539 merge | yes |
| INV-039 | MED | A thread fix "without adding JSON keys" is not invisible: `paths` feeds git status, the contract allow-list (`probes.py:1262,1301`) and transcript scans; filtering it forces `could not determine` and changes pinned `worktrees[]` and `sources[]` rows | separate the git-status scope from the contract allow-list; name the golden tests that change | Part 2.2 action 1 | Q1 / part of INV-008 | yes |
| INV-041 | MED | The seeded test is not sufficient alone: (a) Orca's own `check --help` says `--all` "does not mark read" (no debate file cited it); (b) the flip is a bare constant with no build condition; (c) a throwaway Run has no `--wait` listeners or acknowledge cycle ("A bound Run replays the same Delivery until --ack"); (d) Q-1 FAIL means a pass says nothing about usability | cite the help text first; record the Orca build string in the gate record; add a build check or a test that fails when the build changes | Part 2.1 action 4 (b) | owner or 409 session / gates GF | yes |
| INV-042 | MED | One written note has no test; nothing fails when a word, verb list or schema version changes; the note's tables are already incomplete against code (INV-006, 015, 017 to 019, 023) | one test that compares the note's verb lists, schema versions, join key and shared words with `ALLOWED_ORCA`, the observer templates, `SCHEMA_VERSION` and the report constants | Part 2.3 | CN / none | yes |

### 5.2 Carry-forward and addressed items

<!-- Source: invariant-probe.md (HIGH ADDRESSED carry-forward INV-012, MEDIUM ADDRESSED with residual, LOW rows) - merged per Change #13 -->

- **INV-012 (HIGH, ADDRESSED in R2-V2 5.1, 5.5, 5.6 and R2-V3 5.5; carried here because the one-paragraph consensus omits it)**: the watcher's first session reads untrusted issue text with permission checks off; `--pipeline none` removes only the second agent. FU-1 preconditions (b) and (c) in Part 2.4 action 2 make it explicit.
- **MEDIUM ADDRESSED with a residual**: INV-001 (the record survives until the flip PR commits it: item 5.4 of R2-V1 and 5.9 step 3 of R2-V5; residual: the PR must commit it, Part 2.1 action 4 (d)); INV-004 (snapshot last-writer-wins: handled; residual: no age threshold, Q22); INV-007 (watcher `dispatch.json` at-most-once: handled by the FU-1 gate; residual: the `reset --forfeit-guarantee` precondition, Part 2.4 action 3); INV-014 (the owner writes the record, agents cite it; git cannot show authorship, so Q7).
- **LOW, UNADDRESSED (12) with one-line actions**: INV-006 list both `XDG_STATE_HOME` rules in the note; INV-013 one "person only" sentence in the routing row and the note; INV-015 a pinned test that no other worker-written field reaches the report and apply the untrusted-strings rule to the coordinator; INV-018 say a cycle can make 6 calls with `--questions` on; INV-019 "first 50 in Orca list order"; INV-020 the sweep's version check cannot tell two builds apart (A-009); INV-021 widen the #339 numbering comment to five namespaces; INV-028 join on `runId` plus `dispatchId`, exclude empty or duplicate-flagged rows; INV-031 draft the note on a master-based branch; INV-032 simultaneous load never measured (observer 5 to 6 calls per 15 s per process, sweep up to 3 list calls per Run plus up to 50 `worker-show` per wake, the coordinator's own `worktree ps --agent-wait`, the watcher's `skills list --json`; about 0.2 s per call, `PER_CALL_TIMEOUT` UNVERIFIED); INV-033 #541 green for one commit; INV-044 grep `.dev/issues/409/` for "not passed" in the flip PR checklist.
- **LOW or other ADDRESSED, no action**: INV-016, INV-022, INV-025, INV-026, INV-027, INV-034, INV-035, INV-036, INV-038, INV-040, INV-043 (INV-043's narrowed text names both candidates and so does not choose; the choice is Q4).

### 5.3 Unresolved items

<!-- Source: invariant-probe.md Summary and debate-transcript.md "Convergence Assessment" (lines 1843 to 1849), with round2-rebuttal-V5.md section 4 and round2-rebuttal-V2.md section 4 - merged per Change #13 and Change #20. Return-contract fields: status BLOCKED_BY_INVARIANTS; unresolved INV-008, A-009, X-016 -->

State these as unresolved everywhere they are mentioned (the lead's return contract carries the same list):

1. **INV-008, UNRESOLVED**: the fix is not specified and the owner ruling does not exist. Status stays BLOCKED_BY_INVARIANTS until it does.
2. **A-009, UNRESOLVED by evidence (67%)**: the Orca build divergence: the observer records no Orca version, two builds of 1.4.245 are on record, the sweep's check compares only the prefix, a second host was never checked.
3. **X-016, UNRESOLVED (61%)**: whether `check --all --types question` consumes on a live coordinator Run is unproven both ways; Orca's help text says it does not mark read (INV-041 (a)) but no one ran the seeded test.
4. **Also open, each with the single fact that settles it (R2-V5 section 4, R2-V2 section 4); all UNRESOLVED**:
   - D-A and D-5: does `agent launch` create a Run or Dispatch record? Settled by `run-list` and `worker-list` before and after one real launch at FU-1.
   - D-B: does the agent row's `prompt` hold the claim? Settled by one `worktree ps --json` agent row after the launch.
   - D-3: is `dispatchId` the sweep's `row_id` minus `orca:`? Settled by one comparison on a real Run (JOIN).
   - D-8: the values of `projection.attention` for one live and one blocked worker (the shared capture).
   - Authorship of the pass record (git cannot show it; the owner supplies it, INV-014).
   - Whether a human can use the questions panel in a terminal that holds a Run (INV-024).
   - Whether Orca prunes worker rows (INV-017).
   - The owner API token route to the owner-shared Orca app (R2-V3 D-7).

## Part 6: Corrections to the #409 body and proposed edits to #450, Coder#477, #423 and #339

<!-- Source: Base (original, modified) - Part 6 assembled per Changes #14 to #17 -->

Nothing in this part is posted by the debate, the plan or the merge. "Paste-ready" means the exact replacement text exists in this document (carried verbatim from the named debate file, or written here and marked PLAN INFERENCE) and needs only the pins and owner answers listed. Every body edit is preceded by a fresh read of `updatedAt` (INV-030, A-010). One editor makes all edits in the order of Part 4.2 (A-011).

### 6.1 Corrections to the #409 body

<!-- Source: Variant 5 (variant-5-original.md, "Corrections to the #409 body (exact wording)", lines 176 to 204), carried verbatim as the 23-row table; dispositions modified by the debate (R2-V5 rows 4, 7, 8, 9, 13; R2-V1 A-011), with additions from V1 C-07, C-25, C-34, W-7, V2 W-05(a), W-06, W-11, V4 edit 1 - merged per Change #14 -->

- **Exact wording.** V5's 23 rows BC-01 to BC-23 are carried verbatim below (columns: row number, line in the review's scratch copy of the body, current text, problem, replace with). The "Replace with" cell is the text to post unless the disposition table after it says otherwise. V5's own remarks: items marked "(owner)" restate an owner decision and the owner should confirm the wording before posting.
- **Pins.** V5 checked the live body (fetched 2026-11-13) only through its first 30 lines against `/tmp/pr339/i409-new-body.md`; all line numbers are the scratch file's. The live body had `updatedAt` 2026-11-13T16:57:51Z when probed and keeps moving (30,030 bytes, then 30,756, then 30,758). Before posting: re-read the live body, re-map every line number to a quoted sentence, and use the sentence, not the number, as the locator (V2 and V4 conceded the same drift).

**V5's 23 corrections, verbatim (`variant-5-original.md` lines 180 to 204).** Warning: the "Replace with" cells of BC-12, BC-15, BC-16 and BC-17 are superseded by the disposition table and the proposed text below this table; do not post those four cells as they stand.

| # | Line | Current text | Problem | Replace with |
|---|---|---|---|---|
| 1 | L9 | "The two are built to show the same facts in the same way (see "Status and summary" and "How the pieces fit" below). Both are read-only." | They were built separately and mention each other nowhere; no shared code, schema or vocabulary (overlap table O-01 to O-16). | "Both halves are read-only toward Orca. They were built separately: the observer (`superclaude observe`, merged in PR #503 and PR #514) reads Orca directly; the sweep (PR #539, open) reads Orca plus git, transcripts and worker contracts. They share no code, schema or vocabulary yet, and aligning them is open work (see "Alignment decisions")." |
| 2 | L16 | "No observer code exists yet: there are twenty synthetic designs, waiting for a human to choose a direction." | Wrong. | "Release 1 (worker ledger) and release 2 (coordinator questions for one named Run, live read off) are merged as `superclaude observe` (PR #503, PR #514). The twenty synthetic designs are the design reference; the observer implements Signal Bridge's worker ledger and the Attention Ledger's question notice and panel, and no other design." |
| 3 | L18 | "...so the report and the future observer are meant to say the same thing." | "Future observer" is wrong; "meant to say the same thing" overstates (both borrowed wording from the package independently). | "...The sweep report borrows wording and the ten dimension names from this issue's design package; the built observer was derived from the same package separately. They do not yet say the same thing (see "Alignment decisions")." |
| 4 | L22 (table row 1) | "Done. No direction chosen. No production integration." / "(commit `495eb96d`; no PR, not merged)" | The package is on master (PR #503, `9e2608b03`, identical to the branch). `superclaude observe` is registered in the shipped CLI (`main.py:572-574`). The owner chose a staged direction on 2026-11-08 (owner); no dated selection record exists. | "Done. On master since PR #503 (`9e2608b03`) and on branch `docs/409-orca-dashboard-designs` (`495eb96d`). The owner chose a staged direction on 2026-11-08 (worker ledger, then the question ledger after QUESTION-OBSERVATION, then Decision Desk after QUESTION-LINK); the dated selection record (AC-S) does not exist." |
| 5 | after L22 (new rows) | none | The table omits the observer. | Add: "`superclaude observe` release 1 | Merged 2026-11-11, PR #503: worker ledger on `worker-list`, counts and freshness strips, inspector, changes since last look, text export at 160/116/80, JSON snapshot v1 | `src/superclaude/cli/observe/`". Add: "`superclaude observe` release 2 | Merged 2026-11-12, PR #514: coordinator questions for one named Run. Live read OFF (`QUESTION_GATE_PASSED = False`). Two local commits that switch it on, citing the owner's pass record of 2026-11-12, are not pushed and have no PR | PR #514". |
| 6 | L23 | "Recorded, not yet turned into a chosen design" | True, but the built observer and its release table do not cover Fleet Quilt, Loop Detector or Mission Pulse; Decision Desk is release 3, gated. | Append: "The built observer and the release table in `release-gates.md` cover none of Fleet Quilt, Loop Detector, Mission Pulse; Decision Desk is release 3, behind QUESTION-LINK (not established)." |
| 7 | L33 | "Nothing in this table claims a live Orca run of the observer; the observer does not exist." | Second half wrong; first half misleading. | "Release 1's golden samples were recorded from one live read-only `worker-list` read; whether the owner's live test of PR #503 was completed is not recorded." |
| 8 | L52 | "If the observer built its own collector, two programs would classify the same session and could disagree. Reading the sweep's output keeps one definition of "waiting on a person" or "stalled", and keeps the observer free of any LLM polling loop, which this issue already forbids." | The observer already has its own collector and classifies nothing; it already has no LLM loop. | "The observer already has its own collector (all Runs, paged) and does not classify sessions: it shows Orca's own fields. The sweep classifies with proof. The risk is two vocabularies for the same facts and two readers of the same Orca verb, not two classifiers. The observer's poll is a plain thread with no LLM." |
| 9 | L54 and L124 | "The preferred stack (Bubble Tea v2, Lip Gloss v2, Bubbles v2)..." / "Preferred direction is Bubble Tea v2, Lip Gloss v2 and Bubbles v2..." | The owner confirmed Python + Rich on 2026-11-08 (owner) and PR #503 shipped it. | "Built stack: Python + Rich with a versioned JSON snapshot (owner decision 2026-11-08; PR #503), so a read-only Go screen in TUIBBS can read the snapshot later. Bubble Tea v2, Lip Gloss v2 and Bubbles v2 remain the candidate for that later TUIBBS screen only." |
| 10 | L56 | "The observer follows the human's choice of design, not the other way round." | Releases 1 and 2 were built before a recorded selection. | "Releases 1 and 2 were built on the owner's staged direction of 2026-11-08, before a dated selection record existed; later releases follow the gates in `release-gates.md`." |
| 11 | L64 | "After a human selects a visual direction, develop an observer that shows..." | Already developed. | "Develop the observer in gated releases. Releases 1 and 2 are merged. The remaining releases show affected missions, orchestrators, sessions and worktrees, ..." (keep the rest of the sentence). |
| 12 | L66 | "Complete non-consuming message enumeration ... remain unverified." | Partly answered by the gate research. | Append: "For one named Run, `orchestration check --all --types question --run <id>` was seen not to consume when the Run's owner read it, returns at most 100 rows after the type filter and has no read marker; it works only from the terminal that holds the Run. Complete enumeration remains unverified." |
| 13 | L68-81 (diagram) | "this observer (read-only; proposed reader of the JSON)" fed by the sweep | The built observer reads Orca directly; it reads no sweep file. | Replace the two branches with: "Orca ... -> `superclaude observe` (PR #503, #514; live ledger for a human, 15 s, snapshot v1 JSON in the user state directory)" and "Orca + git + transcripts + contracts -> `superclaude sweep run` (PR #539; one dated report + JSON v1 per coordinator wake, at most every 5 minutes)". Add: "No link between the two exists today." |
| 14 | L95 | "None of this is built." | True of the four asks, misleading as a status. | "None of the four asks is built in releases 1 and 2: the observer shows Orca's own fields, with no summary, no issue or PR link, no named steps and no open-session action." |
| 15 | L102 (Plan item 4) | "**This observer.** A human picks a design direction; the missing source fields are settled (below); then a read-only observer is built against confirmed source contracts. A human selects the direction before production integration (this issue's first acceptance criterion)." | Wrong sequence. | "**This observer.** Releases 1 and 2 are merged. Next: merge the switch-on of the questions read (no PR exists yet), record the owner's direction selection (AC-S) and the Run permission, then release 3 (Decision Desk) behind QUESTION-LINK, and decide where the reviewer's four asks are built." |
| 16 | L109 (Alignment item 1) | "Proposal: read the sweep's JSON, not a second collector." | A second collector exists. | "The observer reads Orca directly today (merged). Options: (a) keep separate with a written contract joined on dispatch id; (b) add an optional observer panel that reads the sweep's JSON (the sweep must first store it); (c) merge the collectors. Proposal: (a), with (b) later. Gaps in sweep JSON v1 for (b): ..." (keep the existing gap list). |
| 17 | L116 (item 8) | "v2 reuses the sweep's output instead of a third scanner" | The observer snapshot is also a candidate. | "...v2 reuses the sweep's output or the observer's snapshot instead of another scanner..." |
| 18 | L174 (AC 1) | "A human selects the visual direction before production integration." | Not met in the recorded sense; the command is already registered. | Keep the criterion and append: "(Status 2026-11-13: not met as recorded. `superclaude observe` is registered in the shipped CLI; PR #503 lists the missing selection record as a known gap.)" |
| 19 | L195 | "This issue request does not authorize production code changes or deployment." | Stale. | "Releases 1 and 2 are merged under the owner's decisions of 2026-11-08 and 2026-11-11. Write-back stays out of scope until the boundary is changed explicitly." |
| 20 | L199 | "Quick static inspection of the offline prototype ... The future production component paths are not known yet." | Wrong: the production paths exist. | "Production components: `src/superclaude/cli/observe/` (adapter, collector, parse, view, render, export, terminal, keys, questions, sanitize, commands, fixtures), `tests/observe/`, registration at `src/superclaude/cli/main.py:572-574`. The files under `.dev/design/orca-observer-20261106/` are the design reference." |
| 21 | L201 | "...no observer path is known yet." | Wrong. | Delete the clause (paths are in item 20). |
| 22 | Related PRs (after L205) | none | PRs #503 and #514 missing. | Add "[PR #503](...) release 1 (merged 2026-11-11), [PR #514](...) release 2 (merged 2026-11-12)". |
| 23 | Banner (top) | "...plus more work on the `409-Phase2` branch." | The remote branch does not exist (`gh api .../branches` lists only `docs/409-orca-dashboard-designs`); the work is two unpushed local commits. | "...plus two local, unpushed commits in the 409 worktree that switch the questions read on; the remote branch `409-Phase2` was deleted after the merge of PR #514." |

**Disposition by row (the debate's changes to V5's text):**

| BC rows | Disposition | Why |
|---------|-------------|-----|
| BC-01 to BC-07, BC-09 to BC-11, BC-13, BC-14, BC-18 to BC-22 | post as written, after re-pinning | unchanged by Round 2; BC-18 (AC 1 "not met as recorded") waits for Q8 if the owner prefers to amend the criterion |
| BC-08 (L52, "observer already has its own collector and classifies nothing") | post as written | supported by V4 F14 and U-008 |
| **BC-12** (L66, "was seen not to consume when the Run's owner read it") | **reword before posting** (PLAN INFERENCE from R2-V5 row 4, not stated in a debate file): say the reads did not consume on a synthetic probe Run read by its owner, that no diagnostic result exists for a live coordinator Run, and that Orca's help says `--all` does not mark read (INV-041 (a)); keep "returns at most 100 rows after the type filter, no read marker, works only from the terminal that holds the Run" | R2-V5 row 4 withdrew O-05; the owner's measurement on the coordinator's own Run is non-diagnostic (X-016, unproven both ways) |
| **BC-15** (L102, plan item 4) | **extend**: "Next: the seeded consumption test and the owner's scope sentence, then the switch-on PR (none exists yet), the owner's AC-S record, then release 3 behind QUESTION-LINK; decide where the reviewer's four asks are built" | R2-V5 row 8; Part 2.1 action 4 |
| **BC-16** (L109, alignment item 1: options (a), (b), (c); proposal (a), with (b) later) | **keep, add**: "(b) needs the sweep's JSON to be stored or captured by the caller; storing it needs an owner decision on the one-report-file rule (NFR-001); both are Phase 2" | R2-V5 row 7; D-2 |
| **BC-17** (L116, decision 8, "v2 reuses ... or the observer's snapshot") | **REPLACE** with R2-V5 row 9: "v2 reads the facts it names in its own field list, each with a named source (sweep JSON for per-Run and disk facts; observe snapshot only for Orca ledger fields)." The decision-8 boundary sentence uses V1 W-7: "Proposed boundary (not yet stated in this issue): this observer shows the human what happened, v2 shares knowledge between agents." | R2-V5 row 13; X-002; the snapshot's 15 row keys carry no command, objective, branch, changed paths, issue or PR |
| BC-23 (banner) | post **last**, after all other rows | R2-V1 section 3 A-011 row |

**Proposed text for the three rows the plan changes (PLAN INFERENCE; written here, not in a debate file; the owner confirms before posting):**

- **BC-12, replace with:** "For one named Run, `orchestration check --all --types question --run <id>` returns at most 100 rows after the type filter, has no read marker, and works only from the terminal that holds the Run. The reads did not consume on a synthetic probe Run read by its owner; no diagnostic result exists for a live coordinator Run, and Orca's own help says `--all` does not mark read. Complete enumeration remains unverified."
- **BC-15, replace with:** "**This observer.** Releases 1 and 2 are merged. Next: the seeded consumption test and the owner's scope sentence, then the switch-on PR (none exists yet), the owner's direction-selection record (AC-S), then release 3 (Decision Desk) behind QUESTION-LINK; decide where the reviewer's four asks are built."
- **BC-16, replace with:** V5's BC-16 text, then append: "(b) needs the sweep's JSON to be stored or captured by the caller; storing it needs an owner decision on the one-report-file rule (NFR-001); both are Phase 2."

**MERGE-EXECUTOR NOTE (reconciles carried wording with the contract rules in Part 2.3; logged in the merge log).** V5's BC-13 says "JSON v1" without a name and BC-16 says "joined on dispatch id". When re-pinning, write "sweep report JSON v1" and "observe snapshot v1" (rule A-014), and keep "dispatch id" as a join key only provisional until the one real-id comparison (D-3, Q24).

**Additions from other variants (not in V5's 23 rows):**

- V1 C-07: the body's "five review findings" against 6 threads, 4 resolved, 2 unresolved on PR #539. V1 C-25: `policy` IS a JSON row key, so #409's "not keys in the JSON" is wrong. V1 C-34 and W-7: the boundary sentence (see BC-17). V1 C-18: the "read-only" claim (see INV-008).
- V2 W-05(a), decision 9: "A session the watcher launches has no Run and no coordinator; the sweep cannot tell it from a person's session and may label it person-started." V2 W-06, the diagram: watcher to ordinary top-level session, no coordinator; the "project's orchestrator" box goes. V2 W-11 (item 9): show "disabled or planned stop" from `disabled_since` and `enabled`, not only `healthy` (UNVERIFIED how the observer would learn `enabled`).
- V5 Round 2 section 5.6 last row: acceptance criterion 2 still says "human attention items"; owner decision 8 (2026-11-11) says "coordinator questions", never "human".
- V4 edit 1 (decision 6: "Decide one design, not two." becomes "Decide one grant vocabulary and one audit record.") only if Q16 = vocabulary; V4's #409 edit 2 (append to decision 8) is superseded by W-7 plus BC-17.
- Do NOT add V1's W-3 (fleet mode wording; X-020).
- Other carriers of the stale "not passed" wording are fixed in the guard-flip PR, not by the issue edit (INV-044).

**Order inside the pass** (R2-V1 section 3 A-011 row, accepted by R2-V5 row 13): (1) V5 facts plus V1 C-07, C-25, C-34, C-18; (2) decisions 1 and 8 (W-7, BC-17 replaced); (3) decision 6 (only if Q16 = vocabulary); (4) decision 9 and the diagram (V2); (5) banner removal last.

**Paste-ready:** yes for the rows marked "post as written" once re-pinned; yes for BC-17 (text above) and the V2 wordings; not yet for BC-12, BC-15, BC-16 (the proposed text above is PLAN INFERENCE and needs the owner's confirmation); no for decision 6 (waits for Q16) and BC-18 (waits for Q8). [Decision: Q8, Q16. Waits for: owner answers, re-pinning, REC. Unblocks: an accurate #409. Undo: yes, issue history.]

### 6.2 Proposed edits to #450 (watcher rollout)

<!-- Source: Variant 2 (variant-2-original.md, "Proposed edits to #450", lines 59 to 67, carried verbatim), dispositions from round2-rebuttal-V2.md sections 1, 5.1, 5.4, 5.6 and invariant rows INV-011, INV-012 - merged per Change #15 -->

**V2's five proposed edits to #450, verbatim (`variant-2-original.md` lines 61 to 65):**

1. Add "Done when 0: decide the claim level the watcher passes (Owner question Q1). Recommended `--pipeline none`; change `build_claim_prompt` and its pins, or record the decision to keep the default and the OB-H1 gate (W-01, W-02)."
2. Replace item 4 with "Done in #485"; fix the test count (W-12).
3. Item 1 (FU-1), add: record the session's identity fields (pane key, terminal handle, session id) from the reply and from `orca worktree ps --json`; the before/after `run-list` check; the Orca Claude command, the session name behaviour and the tab-map entry; the permission mode; keep the unsanitised values in a private note and commit only the sanitised fixture (W-03, W-04, W-08, W-09).
4. Add runbook step 1.3a for creating the watcher worktree with an agent and naming its owner (W-07).
5. Add a note: "Do not build the observer's watcher reader, and do not route watcher prompts through a listener, until FU-1 is recorded" (W-10).

**Disposition:**

| # | V2 edit | Disposition | Paste-ready |
|---|---------|-------------|-------------|
| 1 | "Done when 0: decide the claim level ... Recommended `--pipeline none` ..." | keep; wording depends on Q2 (either "changed to `--pipeline none`" or "kept at the default, with OB-H1 item 1, OB-H2, OB-H3 (#394) recorded as passed") | after Q2 |
| 2 | Replace item 4 with "Done in #485"; fix the test count (2655 against 2637 and 2653) | keep | yes |
| 3 | Item 1 (FU-1): record session identity fields, before and after `run-list` and `worker-list`, the Orca Claude command, session name behaviour, tab-map entry, permission mode; unsanitised values in a private note, sanitised fixture only committed | **extend** with: `CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS` and the real argv (INV-011); the owner's written acceptance of the first session's permission mode (INV-012); the writes the live test makes and closing or unlabelling the test issue (R2-V2 5.6); the Orca build string (A-009); the real operation-id path | after those additions are written in |
| 4 | Runbook step 1.3a: create the watcher worktree with an agent, name its owner | keep; add that `reset --forfeit-guarantee` on an `unknown` entry first requires checking Orca for a live session in the configured worktree (R2-V2 5.4) | after Q20 names the person |
| 5 | "Do not build the observer's watcher reader, and do not route watcher prompts through a listener, until FU-1 is recorded" | **reword** (R2-V2 row 1): "Do not add a watcher panel to `observe`, and do not route watcher prompts through a listener, until FU-1 is recorded." | yes |

Edits 2 and 4 and the runbook additions share no sentence with another report (R2-V2 A-011 row): apply independently of the #409 pass and of #539. [Decision: Q2, Q20. Waits for: Q2 for edits 1 and 3; Q20 for edit 4. Unblocks: FU-1. Undo: yes.]

**MERGE-EXECUTOR NOTE (numbering clash, logged in the merge log).** In V2's verbatim edit 1, "Owner question Q1" means question 1 of review 02. In this document the claim-level question is **Q2** (Part 7). When posting to the issue, describe the question in words rather than by number.

### 6.3 Coder#477 rewrites

<!-- Source: Variant 3 (round2-rebuttal-V3.md, Section 5.6 lines 122 to 172 and Section 5.7 lines 176 to 184, carried verbatim) - merged per Change #16 -->

- **Recommendation.** Text A (narrow) at about 65 percent, after Q3 and Q4. Text C (close) if the observer stays single-host and TUIBBS is not near. Text B (keep) is the least defensible and only if the owner revisits listener option B or C.
- **Paste-ready.** C yes. A: not fully; it holds the placeholder `[N minutes: owner decides]` (Q22), a "Depends on" line naming Q3 and Q4, an owner-token route to the owner-shared Orca app that is UNVERIFIED (R2-V3 D-7), and it names "observe snapshot v1", which must match the contract note's naming (A-014). B: not until the grant format of #339 exists. The Coder-repo paths in "Components Affected" were checked only by V3 and not re-checked by any other variant; keep "per V3".
- **MERGE-EXECUTOR NOTE (numbering clash, logged in the merge log).** In the verbatim text below, "D-1" and "D-2" are R2-V3's own items: D-1 is this document's Q3 (keep, narrow or close) and D-2 is Q4 (what "TUI Panel" means). "D-7" (R2-V3's) is the owner-token route to the owner-shared Orca app (UNVERIFIED); it is not R2-V5's D-7 (shared parser).

**R2-V3 section 5.6, verbatim (`round2-rebuttal-V3.md` lines 122 to 172):**

Recommendation: **narrow** (about 65%), and only after the owner answers D-1 and D-2. If the owner says the observer stays single-host and TUIBBS is not near, **close**. Keep-as-written is the least defensible: its premise (a watcher that sends prompts to a listener) contradicts the built watcher.

Nothing here edits the issue. Paths are relative to the Coder repo root.

**A. NARROW (recommended).**

Title: `Read-only workspace status and identity for the Orchestrator observer (no prompt routing)`

Feature Summary:
> Let a read-only observer outside a workspace (IronClaude's `superclaude observe`, IronbellyOrg/IronClaude#409, and a possible later TUIBBS screen) see which of one owner's Coder workspaces exist, whether each is running, whether it has Orca and IronClaude, and its supervision status record. Nothing can be sent to a workspace through this feature.

Problem Statement:
> The IronClaude issue watcher (IronbellyOrg/IronClaude#331, rollout #450) runs inside each workspace and starts a claim with a local `orca agent launch`. By its design (IronClaude `docs/designs/issue-watcher.md` section 2.1, decision D1 option A, 2026-11-07) it needs no listener, inbound port or address registry, so this issue no longer carries watcher routing. What is still missing: the observer reads one host's Orca only (remote fleet is its release R4, gated on cross-host ownership joins) and cannot see another workspace.

Proposed Solution:
> Workspace identity and running state come from the Coder control plane (workspace id, owner, name, build status, agent last-connected), not from a value the workspace reports about itself. Each workspace also exposes one read-only record: profile slugs, Orca and Claude Code versions, image hash, a last-written time, the observer snapshot (`observe snapshot v1`) and the watcher's status counts. It is reached through an owner-authenticated route (for example the existing owner-shared Coder app mechanism), never an unauthenticated port. No address or port is stored; the route is resolved from the workspace id at read time.

Acceptance Criteria:
> - [ ] Identity (workspace id, owner, name) and running or stopped state are read from Coder. A workspace that reports another workspace's id is rejected and the event is logged.
> - [ ] No address, port, Orca pairing offer, device token, agent token, API key or other standing credential is stored in the registry or sent through this feature.
> - [ ] The read route returns only the fields listed under Proposed Solution, as a named, versioned record with an age. It runs no `superclaude sweep run`, writes nothing, and consumes no Orca message.
> - [ ] This feature has no prompt, command or session-start route. A test shows the route rejects every non-read request and every request type other than "status".
> - [ ] Only the workspace owner, or a read credential the owner issued, can read. Unauthenticated and other users' requests are rejected and logged; no unauthenticated port is exposed; transport is protected.
> - [ ] A stopped, deleted or never-registered workspace is reported as stopped, deleted or none, with a time. A record older than [N minutes: owner decides] is reported stale, never current.
> - [ ] A Minimal-profile workspace is reported as "no orchestrator", not as missing.
> - [ ] Each read writes an audit line (time, reader, workspace id, result) that the workspace owner can read.

Out of Scope:
> - Routing a prompt or command to any workspace, session or orchestrator.
> - The issue watcher (IronbellyOrg/IronClaude#331, #450); it needs no listener.
> - Choosing a grant format (IronbellyOrg/IronClaude#339) and Claude Code cross-session messaging.
> - Reusing the central heartbeat collector (`templates/VSCode-AIDev02/collector/`); its endpoint is anonymous.
> - Upstream component monitors (#419, `.github/workflows/orca-upstream-monitor.yml`).
> - Changing the sweep or the observer.

Components Affected (corrected paths): `templates/VSCode-AIDev02/main.tf`; `templates/VSCode-AIDev02/startup.tf`; `templates/VSCode-AIDev02/modules.tf`; `templates/VSCode-AIDev02/image/catalogue/orca/module.tf`; `templates/VSCode-AIDev02/image/catalogue/profiles.yaml`; `templates/VSCode-AIDev02/image/orca/runtime.mjs`.

Related: IronbellyOrg/IronClaude#339 and PR #539; #409 (and PRs #503, #514); #450; Coder#195; Coder#419. Depends on: the owner's answers to D-1 and D-2; observer release R4.

**B. KEEP (only if the owner revisits option B or C). Replace the Problem Statement with the status paragraph above plus "the owner has chosen to revisit option A", and replace the acceptance criteria with:**
> - [ ] The listener exists only in workspaces whose profile includes the `orca` and `ironclaude` slugs (`image/catalogue/profiles.yaml`). Minimal workspaces are reported as "no orchestrator".
> - [ ] A request is one of a fixed list of types. For the issue watcher the only type is `claim` plus one integer issue number (IronClaude decision D3); no free text ever reaches a session prompt, and the requester cannot choose a flag, a working directory or a permission mode.
> - [ ] An accepted `claim` starts a new top-level session in the workspace checkout whose `origin` is the issue's repository, with the same fixed prompt and launch the watcher uses (the claim level is decided in IronbellyOrg/IronClaude#450). It is not sent as a message to a running session.
> - [ ] The owner has accepted in writing the permission mode of every session the request starts. The stock image launches every Claude session with permission checks off (`README.md`, "Permission checks are off", #455); a live test records the actual mode.
> - [ ] Every request carries sender identity, a grant naming the workspace, the request type and an expiry, and a one-use nonce. Unsigned, expired, wrong-workspace and replayed requests are rejected and logged. The grant format is the one chosen in IronbellyOrg/IronClaude#339; the route stays disabled until it exists. The grant does not replace the watcher's approver, label and integer-only checks.
> - [ ] A request for a stopped, stale or deleted workspace is refused with a reason; it is never queued. A per-type rate cap applies (the watcher's is 6 a day).
> - [ ] Reading status and sending a request use separate credentials; a read credential is rejected by the request route; a test shows it. No address, port, offer or standing credential is stored.
> - [ ] Each decision is audited with time, sender, workspace id, request type, issue number and reason, and can be joined to the watcher's `audit.jsonl` by issue number and workspace id.

**C. CLOSE (comment text).**
> Closing as superseded. The IronClaude issue watcher was built as a poller inside each workspace (IronbellyOrg/IronClaude#331, rollout #450; design `docs/designs/issue-watcher.md` section 2.1, decision D1 option A, 2026-11-07), so no listener, inbound port or address registry is needed. Reopen, or open a new issue from the narrowed text in [link to the comment holding option A], when (1) one of the nine revisit conditions in that design section 2.3 occurs, or (2) the IronClaude observer's release R4 (remote fleet) or a TUIBBS screen has a task package that needs to read another workspace.

**R2-V3 section 5.7, verbatim: state, guard and boundary checklist for any version of Coder#477 (`round2-rebuttal-V3.md` lines 176 to 184):**

1. **Stale registration.** A registry entry for a stopped or deleted workspace must not look live; key by workspace id; show age; remove on delete. Coder, not the workspace, reports deletion.
2. **Name reuse.** Names are reusable; ids are not (`main.tf:111` embeds names). Never route by name.
3. **Spoofed identity.** The existing collector accepts any caller; a registry that copies it fails AC4.
4. **Credential leakage into Coder's own stores.** The #195 PRD forbids putting a standing credential in agent metadata, `coder_metadata` or build logs because Coder stores them. A registration must not do so either.
5. **Read credential escalation.** A reader's credential must be rejected by any route that can start a session; the observer must never hold a credential that can.
6. **Consumed state.** A status read must not consume Orca messages (D-4).
7. **Version skew.** Carry Orca, Claude Code and image versions in the record (A-009).
8. **Untrusted content in records.** Records come from workspaces that read untrusted issue and repo text; readers re-sanitise and treat every string as data.
9. **Bypass by default.** Any route that can start a session starts it with permission checks off on the stock image (5.5). That is the strongest reason the narrowed version has no send route.

### 6.4 #423 rewrite and #339 comment

<!-- Source: Variant 4 (round2-rebuttal-V4.md, Section 5.7 lines 136 to 209, carried verbatim), with the clause dependencies and the numbering sentence from invariant row INV-021 - merged per Change #17 -->

- **Dependencies inside the text (flag each before posting):** (1) the sequencing gate "after PR #539 merges and the #534 live capture" assumes Q14 = Phase 1 only; (2) the Related bullet on #331 says "the claim at its default level also launches a second governed agent (#450)", which is false if Q2 = `--pipeline none` and must change then; (3) the "if #477 is kept" clause follows Q3; (4) the words "on PR #539" must go once it merges; (5) the "Collision Lens" criterion states it is a synthetic image, not built.
- **Addition to the #339 comment (PLAN INFERENCE from INV-021, which says the comment covers only three of at least five numbering namespaces):** add one sentence: "Other numbering in play is not a version of #339: the observer's releases R1 to R4 and the watcher's FU-1 to FU-6."
- **Paste-ready.** The #339 comment: yes, with the added sentence. The #423 body: after Q14, Q2 and Q3 settle the three clauses above.
- **Not edited:** the #339 body (a comment is reversible without editing history).

**R2-V4 section 5.7, verbatim (`round2-rebuttal-V4.md` lines 136 to 209):**

Both are drafts for the owner to post or discard. They carry four corrections to R1-V4's text (data source names both collectors; per-class criterion; observer components and PRs; #331 caveat) and the "if #477 is kept" clause.

**#423 title.** `[FEATURE] Orchestrator v2 (knowledge layer): catalogue of agent work and advisory cross-agent reviews` (keeps "v2" because #339, #409 and #423's own links use it by number).

**#423 body (replaces Feature Summary, Proposed Solution, Acceptance Criteria, Out of Scope, Components Affected, Related; Problem Statement and User Story stay as they are).**

````markdown
## Feature Summary

Orchestrator v2 (knowledge layer) gives an orchestrator, here a coordinator session running the WC-16 loop, a catalogue of what agents are doing and regular cross-agent reviews that share relevant knowledge and flag duplicate or overlapping work. It is advisory: it reports to the person or the coordinator and sends no instruction to an agent on its own. In this issue "v2" means this knowledge layer. It is not the "version 2" in the comments on #339 of 2026-11-05 (trust layer and orchestrator of orchestrators); those are later #339 phases.

## Proposed Solution

Sequencing. This starts only after PR #539 (#339 Phase 1, the read-only sweep) is merged and the #534 live capture that restores the sweep's `working` class is recorded. The other #339 phases (`/sc:close`, resume, trust layer, orchestrator of orchestrators) are not prerequisites, unless the brainstorm decides that v2 relays to agents and not only to the person; then the trust decisions in #339 are.

Start with `/sc:brainstorm --depth deep --handoff design`, then the dedicated `/tech-research` pass on multi-agent memory and context techniques (save its findings to this issue). Do not begin implementation before both are complete.

Data sources and boundaries. The catalogue reads facts through one named fact schema; the collectors are `superclaude sweep run` (per Run: class with proof, contracts, git state, transcript metadata; on PR #539, not on master) and `superclaude observe` (all Runs on one host: Orca worker rows; on master, PRs #503 and #514). Neither carries a command or objective, branch, changed paths, issue or PR today; the design names each field the catalogue needs and its source, and any schema change is decided in #339 (sweep JSON v1) or #409 (observe snapshot v1), never by a v2-only scanner. First release scope is one host and several Runs. Sessions with no Run (person-started, watcher-launched) are not observable by either collector and are listed as "not observable". "All workspaces" depends on whether Coder#477 is kept (the issue-watcher design says option A makes it unnecessary) and on a written read-permission model.

Trust and safety. Relayed knowledge is data, never an instruction: fixed typed fields, free text only in one `detail` field that is never acted on. LLM-derived entries are marked inferred, stored apart from sweep facts and never change a sweep class. The first release delivers to the person or the coordinator only.

## Acceptance Criteria

- [ ] `/sc:brainstorm --depth deep --handoff design` has been run, with its design handoff linked here before implementation begins.
- [ ] A dedicated `/tech-research` pass on multi-agent memory and context techniques is saved to this issue (it may be done ahead of the rest).
- [ ] The design names every catalogue field, where each comes from (sweep report JSON v1, observe snapshot v1, other), and which fields need a schema decision in #339 or #409; no field is added by a new scanner of Orca, git or transcripts.
- [ ] The design states the scope (one host and several Runs for the first release; several Coder workspaces only with a written read-permission model and an owner decision on Coder#477) and what is read: no transcript or log content enters the catalogue; session text is untrusted.
- [ ] The catalogue has a named store, owner, reader set, retention and file mode, says which of the existing stores it extends (sweep report, observe snapshot, watcher `dispatch.json`, `.superclaude/memory/`, `docs/memory/`, task ledgers) or why it is new, and says how it differs from the WC-16 rule that a sweep report is local and never posted.
- [ ] For each session class (Orca worker, watcher-launched, person-started, session without a Run) the design states what is observable, how a checkpoint is obtained, and how a course correction is delivered: a coordinator follow-up (WC-12) for workers, a report to the person for the rest. Labelling machine-started sessions depends on a #534 row.
- [ ] Relayed knowledge is data: a pinned set of typed fields, free text only in `detail`, checked by a test; relay passes through the coordinator (the contract has no worker-to-worker channel); summarizer agents have read-only tools.
- [ ] LLM-derived entries are marked inferred, stored apart from sweep facts, and never change a sweep class; overlapping files are reported as possible overlap, never as conflict.
- [ ] The refresh is the WC-16 coordinator pass, or the design records the owner decision for a further scheduler (existing clocks: WC-16 at most every 5 minutes, observer 15 s, watcher cron 5 minutes, PM checkpoints 30 minutes).
- [ ] The design says what GitHub reads the relevance check needs (unmerged PRs) and whether they are a v2-only collector or a new sweep template with a new owner note.
- [ ] The harness-neutral fact schema is named, with the sweep and the observer as two collectors of it (including the Mastra question, currently UNVERIFIED: nothing in the repo mentions it).
- [ ] The design lists what each review adds beyond `worktrees[].shared_package_ids`, the watcher's one-claim-per-issue rule and the observer's "changes since last look"; the "Collision Lens" design is a synthetic image, not built.
- [ ] The design and resulting components are checked against `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, with the review recorded; any new command is placed on, or kept off, the never-as-worker list in the same change.
- [ ] v2 is delivered as a separate later release after the sequencing gate above.

## Out of Scope

- v1 orchestrator work (#339 Phase 1 and later phases: `/sc:close`, resume, trust layer, orchestrator of orchestrators, management-server relay).
- A second scanner of Orca, git or transcripts; changing sweep classes or the sweep JSON v1 keys (decided in #339).
- Sending prompts or commands to person-started sessions (WC-16: they are never messaged) or to workers outside WC-12.
- A listener or workspace registry (Coder#477).
- Implementation before the brainstorm and research are complete.

## Components Affected

Existing surfaces to review, not a file list: `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`; `src/superclaude/core/WORKER-CONTRACT.md` (WC-12, WC-13, WC-16 and the never-as-worker list); `src/superclaude/skills/sc-pm-protocol/SKILL.md` (memory is one store per worktree, self-ignored; not a cross-workspace store) and `src/superclaude/commands/spawn.md`; `src/superclaude/cli/sweep/`, `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `docs/designs/orchestrator-mode.md` (all on PR #539, not on master); `src/superclaude/cli/observe/` (on master); `src/superclaude/cli/issue_watch/` (starts an ordinary session; notifies no orchestrator); `src/superclaude/pm_agent/reflexion.py`, `docs/memory/solutions_learned.jsonl`, `docs/memory/reflect/` (existing lessons-learned stores); `~/.claude/skills/orchestration/SKILL.md` (installed Orca discovery stub, external).

## Related Issues/PRs

- #339: orchestrator; Phase 1 is PR #539. Its comments use "version 2" for the trust layer and orchestrator of orchestrators; this issue is the knowledge layer.
- #409 and PRs #503, #514: the read-only observer (`superclaude observe`) is built; it shows the human what happened, this layer shares knowledge between agents.
- #331: issue watcher, built (PRs #447, #448; rollout #450). It starts an ordinary `/sc:issue --claim <N>` session through `orca agent launch` and notifies no orchestrator; the claim at its default level also launches a second governed agent (#450).
- #450: watcher rollout.
- #444: sub-orchestrator evaluation (open); relevant to who holds a catalogue when a coordinator sits under another.
- #534: Phase 1 follow-ups; the `working` class and agent-wait rule gate what a catalogue can say.
- PR #539: Phase 1 of #339, the sweep.
- IronbellyOrg/Coder#477: workspace listener; the only planned cross-workspace channel if it is kept (the watcher design says option A makes it unnecessary).
- #326: Git/GitHub communication improvements, not the catalogue itself.
````

**#339: minimal edits.** One comment, no body edit, no scope change (the issue body stays as the owner wrote it):

````markdown
Terminology and links only; no scope change.

1. Version numbers mean three things in this repo. The issue summary puts `/sc:sweep`, `/sc:close` and the comment-3 research in version 1 and signed grants plus the orchestrator of orchestrators in version 2. The Phase 1 research report numbers later phases separately: Phase 2 `/sc:close`, 3 resume, 4 trust layer, 5 orchestrator of orchestrators, 6 management-server relay. #423 uses "v2" for a different release, the knowledge layer (catalogue and cross-agent reviews). From here: "Phase N" means the research report's phases; "version 2" in the 2026-11-05 comments means Phases 4 and 5; #423 is the knowledge layer and starts after PR #539 and the #534 capture.
2. Related: #409 (observer built: PRs #503, #514), #423, #444, #450, #534, PR #539, IronbellyOrg/Coder#477.
3. "Orchestrator management server" is still undefined. Candidates: Orca itself, the observer, a #423 catalogue store. Not decided.
````

If the owner prefers a body edit over a comment, the same three paragraphs fit as a "Related and terminology" section; the comment form is reversible without editing history.

[Decision: Q14, Q15, Q16 (and Q2, Q3 for the clauses above). Waits for: E339 first, then E423. Unblocks: the v2 brainstorm. Undo: yes.]

## Part 7: Owner questions (24, each once, with a recommended answer)

<!-- Source: Base (original, modified) - V5 "Questions only the owner can answer" (questions 1 to 10) replaced by the deduplicated set, merged with V2 Q1 to Q4, V3 Q7, V4 Q1 and Q4, the Round 2 "who can check" lists and invariant rows INV-003, INV-004, INV-014, INV-023, INV-030 - merged per Change #18 -->

The five reviews, the Round 2 "who can check" lists and the invariant probe ask the owner overlapping questions (the first four reports pose 29, many duplicated; V5 adds 10; Round 2 adds more). The 24 below are each asked once, in the order they gate other work. The owner is not asked anything the files can answer. Where the debate gave no winner, the recommendation is the orchestrator's default and is labelled "default (no debate verdict)". Q1's "about 70 percent" and Q6's default are the orchestrator's reading of the invariant probe and of the withdrawn V5 D5(ii) option; they are not debate verdicts.

| Q | Question (plain English) | Recommended answer | Gates | Sources deduplicated |
|---|--------------------------|--------------------|-------|----------------------|
| Q1 | The Codex security thread on PR #539: fix the `git status` hole (neutralise both `core.fsmonitor` and `filter.*.clean`, or refuse any worktree that defines them and show it as `unscanned`) or accept the risk and add a caveat to four "read-only" texts? | Fix, by neutralising both keys or refusing and showing `unscanned` (about 70 percent; PLAN INFERENCE from the probe's stated action; default, no debate verdict) | the #539 merge; X-007, A-006, INV-008, INV-009, INV-010, INV-039 | V1 F-07 and C-18; INV-008, INV-009, INV-010 |
| Q2 | Should the watcher's claim run at `--pipeline none` (claim only: assign, comment, no worktree, no second agent) or at the default `worktree` level (claim plus worktree `issue-<N>` plus a governed second agent)? And do you accept in writing that the first session runs with permission checks off on the FU-1 test issue? | `--pipeline none`, and yes, in writing, for the test issue only | the #450 edits, FU-1, X-001, INV-011, INV-012, the #423 and Coder#477 text | V2 Q1 and D-G; INV-011; INV-012 |
| Q3 | Coder#477: keep as written, narrow to read-only status and identity with no prompt routing, or close? | Narrow (about 65 percent); close if the observer stays single-host and TUIBBS is not near; keep only if you revisit the listener options | the Coder#477 rewrite | V2 Q2 and D-H; R2-V3 D-1 and 5.6; V4 D-4 |
| Q4 | What does "TUI Panel" mean in your 2026-11-13 comment on Coder#477: `superclaude observe` (the #409 dashboard), a future TUIBBS screen reading the snapshot, or both? | `superclaude observe`; TUIBBS is a possible later reader; single-host; read-only (about 70 to 75 percent) | Q3, the Coder#477 text, Part 2.7 | V5 Q1 and D9; R2-V3 D-2; R2-V5 D-4 |
| Q5 | Do you want one written contract note between the observer and the sweep (keep both programs), an optional observer panel that reads the sweep's JSON, or a merge? | One contract note; keep both programs (A-012 and X-017) | the note, X-006, A-001 | V5 Q2 and D1; V1 Q1; V4 D-3 |
| Q6 | Does your 2026-11-12 pass for the coordinator-questions read cover only `run_93bfa00cae2b` or any Run your terminal holds? Do you want it flipped before the seeded consumption test has run? | Default (no debate verdict): do not flip before the seeded test; after it, the scope sentence is yours; no answer means the guard stays off. The only debate recommendation to widen scope (V5 D5(ii)) was withdrawn | the guard-flip PR; INV-003, INV-024, X-016 | V5 Q3 and D5; INV-003; R2-V1 D-3; R2-V5 row 8 |
| Q7 | Will you write the pass record yourself (git cannot show who typed it) and commit or archive the records that exist only in the sibling worktree (`owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`)? | Yes, both, before that worktree is cleaned | the guard-flip PR; A-015, INV-002, INV-014 | V5 Q10; INV-002; INV-014 |
| Q8 | Will you write the dated direction-selection record (AC-S) naming the staged direction, your reading of "production integration" and the command name, or amend #409's first acceptance criterion? | Write the record (one paragraph) | #409 AC 1 text; X-018, A-003 | V5 Q4 and D6 |
| Q9 | Should the sweep's JSON ever be stored beside the report (which needs you to relax "a sweep adds exactly one report file", NFR-001), or captured from stdout by the caller, or not at all? | Not now. Phase 2: caller-side stdout capture first; relax NFR-001 only if a stored file is needed | persistence, X-004, A-001 | V1 Q2 and D-1; V5 Round 1 concession 4 (withdrawn); R2-V2 D-E; R2-V3 D-3; R2-V4 D-1 |
| Q10 | May the sweep ever read Orca messages with `check --all --types question`, or is that the observer's alone? | Observer's alone for now; correct the sweep's two sentences (Part 2.2 action 6) | the sweep allow-list (NFR-014), O-04, O-05 | V5 Q6 and D4 |
| Q11 | Is the "static report in chat every 3 to 5 minutes" that #339 asks for the sweep's summary, the `observe --once` text, or both? | The sweep summary only until the contract note exists | #339 D2 | V5 Q7 and D2 |
| Q12 | Should the observer get a routing row in `HOW-WE-WORK.md` (and its plugin mirror and the sc-recommend table)? | Yes, one row, own small PR after #539 merges (the two table tests need edits: INV-029) | the routing row | V5 Q8 and D8 |
| Q13 | Is bare `orca` acceptable for the observer when the sweep's rule is "never bare `orca`"? | Yes: the observer validates the binary with `skills list --json`; record it in the note. The watcher uses the same rule, so only the sweep differs | the note | V5 Q9; R2-V2 section 2 |
| Q14 | What does "#339 is complete" mean for #423's gate: PR #539 merged only, or also `/sc:close`, resume and the trust layer? | PR #539 merged plus the #534 live capture; the other phases only if the brainstorm decides v2 relays to agents | the #423 rewrite | V4 Q1 and D-2 |
| Q15 | Must v2 ever deliver a course correction to a session that is not a worker, or does it report to a person or the coordinator only? | Report only (advisory); no delivery to non-worker sessions | the #423 acceptance criteria | V4 Q4 and D-8 |
| Q16 | Trust: promise one trust design, or one grant vocabulary and one audit record format? | One vocabulary and one audit format (X-005, 66 percent) | #409 decision 6, #423, Coder#477 text | V3 Q7; V4 D-4; X-005 |
| Q17 | Should the observer ever show the sweep's facts (frozen plans, safe-to-close, contract questions, git state) on the same screen as the Orca ledger? | No, not now; if yes later, persistence (Q9) becomes a real requirement | A-001, D-6 | V5 D-6; V1 Q1 |
| Q18 | Do you want a channel that copies the observer snapshot from the Coder workspace to the separate TUIBBS host? | Not before observer release R4 or an owner statement that a TUIBBS screen is planned | the Coder#477 text | R2-V5 D-9; V3 D-1 |
| Q19 | Which of the reviewer's four asks (Fleet Quilt, Decision Desk, Loop Detector or Mission Pulse, summary and links) comes first, and in which program? | Fleet Quilt or Decision Desk first, in the observer, after the contract note and the shared capture | `release-gates.md` rows | V5 Q5 and D7 |
| Q20 | Who owns the agent in the watcher worktree, and may that one worktree hold up to 6 new sessions a day that are never owned by a coordinator? | A named person owns it; watcher sessions stay person-reviewed top-level sessions | runbook step 1.3a | V2 Q2 and Q4; R2-V2 5.2 |
| Q21 | May the sweep label machine-started sessions separately from person-started ones, reading `worktree ps` agent rows (`prompt`, `paneKey`)? | Yes, in Phase 2 and only after FU-1 shows what those rows hold (D-B) | the #534 row, X-003 | V2 Q3; V4 D-5 |
| Q22 | What age makes a snapshot or a workspace record "stale" (the observer's own feed uses 45 s; a file on disk has no liveness flag)? | Your number; no debate recommendation. Until set, readers show any file older than the producer's own cycle as stale and print its age | the note, the Coder#477 acceptance criteria | INV-004; R2-V3 5.6 A |
| Q23 | Is a `reclaimable` worker live, historical, or its own state? | Its own state, shown with Orca's word, until you decide (default, no debate verdict) | the mapping table, INV-023 | INV-023 |
| Q24 | Who runs the shared read-only Orca capture (attention values for a live and a blocked worker, the agent row of a Run-less session, Orca's event help) and the one-time comparison of the observer's dispatch ids with a sweep's `row_id` list? | The 409 session with live Orca, read-only, one sitting | CAP, JOIN, A-013, X-006 | V5 D3 and D-3; R2-V1 D-5; R2-V2 D-A, D-B; R2-V4 D-7 |

For the first four, what each answer does: **Q1** F1 or F2 means a code and test change in #539 before it merges; F3 means a caveat on four texts and a recorded acceptance of risk. **Q2** `--pipeline none` means one small PR and no second agent; the default means a worktree and a governed second agent per claim. **Q3** narrow means a rewrite of Coder#477 with no send route; close means a comment with two reopen conditions. **Q4** answers what the owner meant by "TUI Panel" and so decides the transport, not the contract.

## Part 8: Changes not being made

<!-- Source: refactor-plan.md "Changes NOT Being Made" table, built from the R2 concessions, X-004, X-013, X-017, A-012, X-005 and invariant row INV-008 - merged per Change #19 -->

Rejected proposals, each with the debate's own evidence, so nobody reopens them. "Diff Point" is the debate id.

| Diff Point | Non-base or rejected approach | Rationale for not making it |
|------------|-------------------------------|-----------------------------|
| X-004, A-001, X-017 | Persist the sweep JSON now (V1 F-03 and Q1 "persist; it keeps one collector"; V5 Round 1 concession 4 "cheap"; V3 Edit 5 status route "produced without any write") | NFR-001 ("a sweep adds exactly one report file") is pinned by the design (`orchestrator-mode.md:128`) and two tests (`test_readonly.py:300,400`, `test_cli_contract.py:1192,1361,1474`); a sidecar needs an owner requirement change inside a contested PR; `sweep run` writes a report on every run. V1, V2, V3, V4 and V5 all converged on Phase 2 (R2-V1 D-1; R2-V5 row 7). Alternative kept open: caller-side stdout capture inside the WC-16 pass (R2-V2, R2-V4). Matrix: X-004 V1 91%, X-017 V5 70%. |
| A-012, X-017 | Merge the two programs, retire one, or have the sweep reuse the observer's adapter (V5 D1 option (c); V1 "one collector") | The facts differ (git, contracts and transcripts versus fleet-wide Orca rows); one collector would break one design's rules (stdlib-only models, exact-token owner-signed allow-list NFR-014); #539 is in review; the observer's only gain for the sweep is paging. A shared parser is revisited after #539 merges (R2-V5 D-7). A-012 is 66% and provisional: Q5. |
| X-013, X-011, X-015 | Build an observer reader of the sweep JSON, or let the observer start the sweep itself (V1 F-01 (1), #409 L109 "read the sweep's JSON, not a second collector"; V4 proposal (b); V5 BC-17 as worded) | The observer exists, reads Orca only and has its own 15 s poller; the sweep's JSON is stdout-only; the snapshot's 15 row keys carry no command, objective, branch, changed paths or issue or PR (R2-V5 row 9); running the sweep from a reader writes a report and runs `git status` in every worktree each time (X-004). X-013 95%. An optional panel stays a later owner choice (Q17). |
| X-005 | One trust design instead of one grant vocabulary (V3 F12 and Edit 7; #409 decision 6 "Decide one design, not two") | The three consumers have different threat models and signing does not stop poisoned content (#339 comment 2: "encryption alone is not enough"); under watcher option A the watcher's trust is a local model (V3 itself). Not decidable from sources, so it is Q16; the recommended default is the narrower promise. X-005 66%. |
| X-001 | Keep the watcher's default pipeline unexamined, or restate it as "one ordinary session" (V3 Edit 8; V4 C7 and F11) | `issue.md:43,88` and `launch.py:33` show a second governed agent is created at the default level; the design says the claim stops at `next-steps.md`. X-001 91%. |
| A-004 | Add JSON keys, a sidecar file, wording fixes or observer wording inside PR #539 | two threads are unresolved and the key set is golden-tested (`ROW_KEYS`); log items in #534 and edit after merge. A-004 88%. |
| A-004 | "#539 needs only a CI re-run" (R2-V1, R2-V2) and "needs a rebase" (V1 C-08) | a re-run keeps the old merge ref (INV-037); there is no file overlap with #541 (INV-036). |
| X-016 | Treat the observer's non-consumption as established (V5 O-05 and its sweep rewording) or the sweep's "cannot be read without consuming" as established (the sweep's `report.py:534`) | unproven both ways on a live coordinator Run (61 percent); the owner's measurement is non-diagnostic; Orca's help says `--all` does not mark read (INV-041 (a)). Both programs keep their cautions; the sweep's two lines are reworded to state only what is established. |
| A-003, X-018 | Flip the guard on the owner's "Do it" record alone, or recommend scope "any Run the terminal holds" now (V5 D5(ii)) | the seeded consumption test, the live-layout attempt, the build pin and the owner's own scope sentence are prerequisites (R2-V5 row 8; INV-003, INV-005, INV-024, INV-041). |
| X-002 | State the observer and v2 boundary sentence as already established in #409 (V4 C8, V4 #409 edit 2) | the sentence appears only inside decision 8 (V1 C-34; circular proof withdrawn by V4); it is proposed wording (V1 W-7). X-002 81%. |
| X-007 | Treat "the sweep confines every path" as true (V4 F17) | it holds for file reads only; `git status` runs with the inherited environment in every listed worktree (`probes.py:305-327,1203-1214`). X-007 89%. |
| INV-008 | Accept the Codex-suggested remedy ("restrict `git status` to the selected repository" and "disable executable Git config") as sufficient | measured: `core.fsmonitor` and `filter.*.clean` both ran; one flag stops only the first; a repo filter leaves a shared `.git/config` exposed. |
| X-019, X-020, X-009 | Repeat "all four earlier reviews were wrong about one fact", "drop W-3 from the #409 body" or V1's tally | overgeneralisation, a mislabel and a miscount; none changes a decision. |
| A-013 | A separate research task on an Orca event stream | the shared capture covers a help-text read of Orca's event surface at no extra cost (R2-V1, R2-V2, R2-V3, R2-V4, R2-V5 all agree). A-013 65%. |
| A-011 | Five parallel edit sets to the #409 sentences | one editor, one ordered edit set, pinned cites (A-011 92%). |
| X-001 family | A listener, inbound port or address registry for the watcher (Coder#477 as written) | design decision D1 option A (2026-11-07) and the stopped-workspace case (R2-V3 5.1); the narrowed read-only form is the recommendation. |

## Appendix A: Sources read and not read, and pointers into the base

<!-- Source: Base (original, modified) - V5 "Scope read" moved to an appendix with section pointers per Change #1 -->

**Where each part of the base review went.** The full text of every base section is kept in `variant-5-original.md` (in the debate folder `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/`); this document condenses or re-homes it.

| V5 section (`variant-5-original.md`) | Where it went |
|---|---|
| Scope read (lines 5 to 19) | this appendix |
| "What `superclaude observe` is today", parts 1 to 10 (lines 20 to 104) | facts E-01 to E-18 (Part 1.2) and Part 2.1 |
| "Overlap and conflict with the sweep", O-01 to O-16, "Facts each program owns", "Could `observe` read the sweep..." (lines 105 to 148) | Part 2.3 (units table, mapping table) and Part 8 |
| "Re-test of review 01 findings F-01..F-18" (lines 149 to 175) | Part 1.3 (withdrawn findings) and Part 3 |
| "Corrections to the #409 body (exact wording)" (lines 176 to 207) | Part 6.1, carried verbatim with the debate's changes |
| "Integration decisions and dependencies", D1 to D9 and the dependencies table (lines 208 to 283) | Part 2, Part 4 (the dependencies table is replaced), Part 7 |
| "Questions only the owner can answer" (lines 284 to 298) | Part 7 (deduplicated into Q1 to Q24) |
| "Verdict" (lines 299 to 309) | Part 1.1 (replaced by the adjudicated verdict) |

**Sources this document is built from.** The base review (V5, sections "Re-test" to "Verdict" read in full for this merge; earlier sections through the refactoring plan's citations); the refactoring plan `refactor-plan.md` (read in full); `invariant-probe.md` (read in full); `round2-rebuttal-V5.md` sections 1 to 5 (read); `round2-rebuttal-V3.md` sections 5.5 to 5.7 and `round2-rebuttal-V4.md` sections 5.6 to 5.7 (read); `variant-2-original.md` "Proposed edits to #450" (read); `debate-transcript.md` Scoring Matrix and Convergence Assessment (read); `diff-analysis.md` metadata (read).

**Not read in full by the merge step (relied on through the refactoring plan's citations, each marked per its source):** the rest of `debate-transcript.md`, `round1-advocate-V1..V5.md`, `round2-rebuttal-V1.md`, `round2-rebuttal-V2.md`, `step3-*.md`, `base-selection.md` beyond its summary, and the bodies of `variant-1-original.md` to `variant-4-original.md`. Nothing in this document was checked against GitHub, Orca or the repository; every "verified now" claim is the debate's, with the source it named.
