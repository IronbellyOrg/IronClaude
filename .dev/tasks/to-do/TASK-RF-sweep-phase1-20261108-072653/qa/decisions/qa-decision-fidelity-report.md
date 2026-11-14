# QA Report - Decision-fidelity lens (item 7.25)

**Phase:** decisions-qualitative (rf-qa-qualitative), decision-fidelity lens
**Date:** 2026-11-11
**fix_authorization:** false (report-only)

## Checks

| Check | Description | Result |
|-------|-------------|--------|
| C1 | OQ-1: recorded Chosen (allow `worktree ps --agent-wait`, lock-check waived) matches the quoted words "Allow it, no conditions needed." | PASS |
| C2 | OQ-1: the quoted owner words come from the owner directly, not from a peer relay (the standard this task applies to OQ-3 and OQ-6) | FAIL (F-1) |
| C3 | OQ-2: Chosen, quote ".dev/sweeps/ (Recommended)", date and source lines match the record and the session transcript answer | PASS |
| C4 | OQ-3: Chosen "New WC-16 rule", quote, date, source lines match; peer relay used as corroboration only | PASS |
| C5 | OQ-4: Chosen (pin 495eb96d, DESIGN 7.5 ordering and labels unchanged), quote and source lines match; no import of dashboard code claimed | PASS |
| C6 | OQ-5: Chosen (6h, activity only, open work always listed), quote and source lines match | PASS |
| C7 | OQ-6: Chosen is actual option (b) and rests on the owner words "Add an exception" | PASS |
| C8 | OQ-7: Chosen (a) with both residual path-B cases, quote, date and DESIGN line 836 anchor match | PASS |
| C9 | OQ-8: Run id record matches the owner's selection "Use run_a4723d345399 (Recommended)" and records no extra consent | PASS (N-3) |
| C10 | OQ-17 (resolved file exists): Chosen "refuse the cursor command, allowlist stays 10" matches the owner's selection and the option text quoted | PASS |
| C11 | No recommendation was recorded as a decision without the owner's words (all nine records; each Chosen follows a located owner answer) | PASS (OQ-1 provenance is C2) |
| C12 | GQ-63 (OQ-6) carries no recommendation: record lines 22-24 and the question put to the owner | PASS |
| C13 | GQ-63 stays actual (b); quote, no-recommendation text and history unchanged (edit log, mtime, index copy) | PASS |
| C14 | owner-decisions.md rows OQ-1 to OQ-7 match their seven decision files (option, words, decider, date, source line ranges, unblocked steps) | PASS |
| C15 | owner-decisions.md has a row for the resolved OQ-17 file that exists | FAIL (F-2) |
| C16 | owner-decisions.md statements about open decisions are current (line 55 on OQ-8, OQ-17, OQ-18) | FAIL (F-2) |
| C17 | The 13 APPROVED constraint rows quote their APPROVED.md lines unchanged (lines 10-13, 20, 25, 29, 30, 35, 36, 47, 71, 90) | PASS |
| C18 | GQ-63 section keeps decision, checked revision (planning only) and execution permission as three separate things | PASS (N-2) |
| C19 | Bounded planning ("Authorize bounded revision") is not treated as execution consent anywhere (BUILD-REQUEST, addendum, DESIGN pointer, owner-decisions) | PASS |
| C20 | The execution-permission quote "Accepted, I accepted, but it reported a decline.  Proceed" is the owner's own message (session transcript, 2026-11-11T20:26:41.816Z) | PASS |
| C21 | The style exception is not a generic coordinator exemption (pragmatic.md:25 and :26) | PASS (N-1) |
| C22 | R5 design edits (7.3, 11, 12, 13, 15.1, GQ-109 row, section 18 Fix cycle 3 R5 row) say no more than the relayed words and keep the version-scoped limits | PASS |
| C23 | 1.0a-facts.md "Owner allowlist branch" section agrees with the OQ-17 record | PASS |
| C24 | readonly-probe.md, pr422-409-check.md and tests/sweep/fixtures/SOURCES.md present no executor choice as an owner decision | PASS (N-4) |
| C25 | decisions-mechanical.md S7, S9, S10 evidence for GQ-63 is sound and nothing in it claims a decision the owner did not make | PASS |

## Findings (blocking: F-1, F-2; the rest are MINOR notes)

All paths below are relative to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/` unless they start with `docs/`, `src/` or `~`. "Transcript" means the session files under `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-339-orchestrator-mode/` (`db62cb58-fc67-47da-9997-00e1192076a7.jsonl` is the executing session; `6ee233a2-7499-47c8-aae7-7d1ee19bb68e.jsonl` is the earlier task-building session).

### F-1 | MAJOR | OQ-1 (R5, `worktree ps --agent-wait`) rests only on a peer relay, not on the owner's own answer

- Evidence: `phase-outputs/plans/OQ-1-agent-wait-decision.md:22` says "the owner's words, relayed by the coordinator (run `run_93bfa00cae2b`, messages `msg_d95a87e312e1` and `msg_6ee5998d0874`)". In the transcript `6ee233a2...jsonl`, the first appearance of "Allow it, no conditions needed" is at 2026-11-08T12:05:48Z inside a tool result that carries the coordinator's message `msg_d95a87e312e1`. I searched both session files for a direct owner string message or an owner question answer containing those words or mentioning `agent-wait`: none exists. The owner's only first-hand answers in `db62cb58...jsonl` start at 2026-11-09T02:43Z and none is about R5.
- Why it matters: this task holds every later decision to the direct-answer rule. `revisions/chat-output-exception-20261109-133150/BUILD-REQUEST.md:15`: "Peer relays are corroboration only and do not replace direct consent." `phase-outputs/plans/OQ-3-GQ-11-rule-id-decision.md:39`: the relay "corroborates but is not the authority used here". The 2026-11-09T13:32 question to the owner reads "this session cannot use a peer message as your answer". OQ-1 is the one record that violates that rule, and it is the only one that widens the Orca allowlist: `docs/designs/orchestrator-mode.md:535-536` (two new templates), `:837` (D10 "Owner decision R5, 2026-11-08"), `:1047` (section 18 R5 row "RESOLVED by the owner").
- What is faithful: the Chosen text does match the relayed words. `artifacts/owner-decisions.md:17` discloses the relay. The earlier accepted R5 gate failure (`qa/r5/cycle1-decision.md:19`) concerned a Run id citation in the relay, not who spoke, so it does not waive this.
- Smallest fix: put one direct question to the owner ("May the sweep's allowlist include `worktree ps --agent-wait`, with and without `--json`?"). On yes, add the answer and date to `OQ-1-agent-wait-decision.md` (Decision source) and to the OQ-1 row of `owner-decisions.md`. On no, R5 (design lines 535-536, 837, 895, 1047) must be reverted by a design revision.

### F-2 | BLOCKING | owner-decisions.md has no row for the resolved OQ-17 decision and says OQ-8 and OQ-17 are still open

- Evidence: `phase-outputs/plans/OQ-17-cursor-template-decision.md:1-4` is `status: RESOLVED` and lines 35-40 hold the owner's selection "Keep the 10 commands (Recommended)" (transcript: answer at 2026-11-11T22:25:33Z). `artifacts/owner-decisions.md` was last written at 20:51 on 2026-11-11 (before OQ-8 at 21:32 and OQ-17 at 22:28). Its table (lines 9-15) has exactly OQ-1 to OQ-7; line 5 says "(seven rows)"; line 55 says: "Still open and not recorded here as decisions: OQ-8 (the Run id, item 7.14) and the optional OQ-17 and OQ-18 (only if step 1.0a fires them)." Both statements are now false: OQ-8 is RESOLVED (`OQ-8-run-id-decision.md:26-29`) and OQ-17 fired and is RESOLVED (`phase-outputs/discovery/1.0a-facts.md:54-56`). `grep -c 'OQ-17\|OQ-8\|cursor' artifacts/owner-decisions.md` returns 1 (line 55 only).
- Why the gate did not catch it: item 7.13 (task file line 1229-1234) only required seven rows, and no later item (7.17, task file lines 1266-1275) updates owner-decisions.md. `phase-outputs/test-results/decisions-mechanical.md` C5 checks only that the file is non-empty and C4 counts recommendation sentences; no check compares file rows to decision files.
- This lens requires a row for "each resolved OQ-17 or OQ-18 decision file that exists" (an absent OQ-18 needs none; `decisions-mechanical.md` C3 confirms it is absent).
- Smallest fix (append-only to `artifacts/owner-decisions.md`): add one table row for OQ-17 (Chosen: refuse the extra cursor command, allowlist stays at exactly 10 templates, full page of 100 shown as truncated with a lower-bound total; owner's words "Keep the 10 commands (Recommended)"; Ryan Wiancko, owner, 2026-11-11; source `OQ-17-cursor-template-decision.md:35-40`; unblocks item 7.17 and, through it, step 1.2, 8.10 and 10.3 with the count kept at 10); change the heading count; and rewrite line 55 to say OQ-8 is resolved (record file and line 26-29), OQ-17 is row N, OQ-18 was not fired.

### N-1 | MINOR | The style text goes past "an exception to the table", and the owner never saw its wording

- Evidence: the owner's words are "Add an exception" (transcript 2026-11-09T13:23:01Z); the option text was "Choose a coordinator exception to the table requirement. Stop for a separate design/task revision before editing the output style." `src/superclaude/output-styles/pragmatic.md:23` also waives the WHAT / WHY / RECOMMENDED ACTION wrapper and the plain-English label gloss for that one reply, behind a five-condition test (assignment, loaded skill, exit 0, parsed JSON, report Read). That text comes from `revisions/chat-output-exception-20261109-133150/design-addendum.md:13-21`, a builder product. The question that led to "Proceed" (2026-11-10T07:07Z) named reports, not these clauses.
- No file claims the owner approved the wording: `OQ-6-GQ-63-done-next-decision.md:33` and `owner-decisions.md:14` both say the exact wording needs a separate revision, and `pragmatic.md:25` says "There is no general exemption for coordinators". So this is not a recording defect. Note for later gates (11.x, 14.x): do not call the wording "owner-approved"; the owner approved the route (revision, then proceed), not the clauses.

### N-2 | MINOR | "Accepted ... Proceed" is mapped to a specific option by the executor, and owner-decisions.md states the mapping as fact

- Evidence: the 2026-11-10T07:07Z question (tool call `toolu_016w5Z6Mo4fGtNy9UAdQ4xbt`) never returned an answer: its result is "[Tool call interrupted: the session ended before this call's result was recorded ...]" (2026-11-11T16:59:32Z). The owner's message at 20:26:41.816Z does not name an option. `phase-outputs/test-results/step-7.10-style-exception.md:13` says openly "The executor reads ... as the first and recommended option". `artifacts/owner-decisions.md:29-31` says only "It authorized item 7.10 only" without saying that scope is the executor's reading. The reading is the narrowest possible (the other two options were further revisions), so no harm is shown. Fix: add "(scope as read by the executor; the tool recorded no option)" after line 31.

### N-3 | MINOR | OQ-8: the owner picked the assistant's own recommendation, although the question said the assistant's pick "does not count"

- Evidence: transcript question 2026-11-11T21:24:47Z: "The plan requires you to name it in your own words; my pick from your list does not count"; the owner then selected "Use run_a4723d345399 (Recommended)" (answer 21:32:21Z). `OQ-8-run-id-decision.md:29` records this honestly and records that an earlier delegation ("pick one, your choice") was withdrawn. It is the owner's own selection of a labelled option and widens nothing, so I treat it as met. Fix if wanted: none.

### N-4 | MINOR | The 1.0a capture holds two executor judgments that stand in for an owner decision

- `artifacts/readonly-probe.md:783`: the executor decided that a changing envelope `id` is not a "difference" under the rule that sends a difference to the owner (DESIGN line 875 "A difference stops the build and goes to the owner"), and wrote the HALT text the owner would use. `:1071` (Deviation D1): one `task-list` read outside the item's allowed list. Both are disclosed and neither is recorded as an owner decision, so fidelity holds; the owner has not yet been told. Fix: mention both at the next owner contact.

### Out of this lens (not graded)

- `artifacts/pr422-409-check.md:3` ran the "495eb96d is not an ancestor" check against a local `origin/master` (`35073356`) that differs from HEAD (`5dc29d23`) and was not refreshed. The evidence-quality lens owns this.

## Self-Audit

**(a) Reliance list - structural passes relied on without re-checking:**
- Relied on `phase-outputs/test-results/decisions-mechanical.md` C1 (eight records RESOLVED), C3 (OQ-18 absent), C5 to C8 (files exist) and S1/S2/S4 (style diff is limited to the seven table sites).

**(b) Independent semantic checks (own tool evidence):**
- Every owner quote in the seven rows plus OQ-8 and OQ-17 was matched to the owner's answer in the session transcript with `jq` (answers at 2026-11-09T11:49, 12:52, 13:09, 13:15, 13:23, 13:33; 2026-11-10T04:54; 2026-11-11T20:43, 21:32, 22:25) and the option texts the owner chose were read from the `AskUserQuestion` calls.
- OQ-1: searched both transcripts for a first-hand owner message; found only the coordinator relay (source of F-1).
- The "Accepted ... Proceed" message was located as a plain user message and its question call was found interrupted (N-2); `decisions-mechanical.md` S7 only checked that the words exist.
- OQ-6 history: `Write`/`Edit` calls on the record stop at 2026-11-09T13:23:27Z; the file matches its staged copy by md5 (`f6811aaf3a718f85d3ab8963f6663739`).
- owner-decisions.md versus the OQ-17 record and the live file list (F-2): not covered by any mechanical check.
- All 13 APPROVED rows re-read against `.dev/orca-command-refactor/decisions/APPROVED.md` lines 10-13, 20, 25, 29, 30, 35, 36, 47, 71, 90; bracketed re-anchors spot-checked against `docs/designs/orchestrator-mode.md` lines 643, 647, 736, 947 and `src/superclaude/core/WORKER-CONTRACT.md:63`.

**Confidence:** Verified: 25/25 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (computed over the 25 checks above; 22 PASS, 3 FAIL). Not verifiable by anyone from the files: whether the owner read the style clauses (N-1).
**Tool engagement:** Read: 29 | Grep: 6 | Glob: 0 | Bash: 14 (jq over session transcripts, git status/diff/md5, sed). Web research: none, so no Tavily call was needed.

## Verdict

Seven of nine decision records (OQ-2 to OQ-7, OQ-17) match the owner's own words; OQ-8 matches with a note. OQ-1 rests on a peer relay (F-1), and owner-decisions.md omits the resolved OQ-17 and carries a stale "still open" line (F-2). GQ-63 is intact as actual (b), with its quote, no-recommendation text and history unchanged, and bounded planning is nowhere treated as execution consent or a generic coordinator exemption.

Verdict: FAIL
Blocking count: 2
