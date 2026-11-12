# QA Cross-Source Consistency Report (item 7.28, rf-analyst)

fix_authorization: false. Read-only except this report. Date of review: 2026-11-12 (session date). Analysis type: cross-validation (cross-source consistency lens).

Method. Every path below was read from disk in this session in chunks of at most 150 lines (large files by targeted ranges). No earlier QA report in `qa/decisions/` was read or relied on. Read-only commands run: `grep -F` of each APPROVED quote against its APPROVED line, `jq` over the fixtures, `git merge-base --is-ancestor`, `git diff --shortstat`, line probes with `sed -n`. `gh pr view 422` was not re-run (network call, not needed for a consistency check; the git ancestry halves were re-run). No web research was done.

Result in one line: no BLOCKING and no MAJOR mismatch. Nine MINOR mismatches are listed, each with both `file:line` sides. In this report the task folder prefix `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/` is written `T/`.

## Findings

All findings are MINOR. MINOR findings never fail the gate.

### F1 (MINOR) The signed-off D9 text and open item 22 still say the sign-off is pending

- Side A (decision): `T/phase-outputs/plans/OQ-7-D9-signoff-decision.md:40-43` is RESOLVED, option (a), owner, 2026-11-11. `T/phase-outputs/discovery/1.0a-facts.md:24` marks open item 22 CLOSED.
- Side B (design): `docs/designs/orchestrator-mode.md:836` (D9: "which is still pending", "Needs the owner's sign-off at step 1.0b"), `:875` (SP-29 row: "which is still pending") and `:1012` (open item 22: "the classify step does not start until the owner signs off D9"). Task file `T/TASK-RF-sweep-phase1-20261108-072653.md:2873` says the same.
- Why it is only MINOR. The owner signed the design text "as written" (OQ-7 record `:41`, `:43`), and the quote in OQ-7 matches design `:836` (both the SPEC-text and Design columns, checked with `grep -F`) and `:1012` (first 200 characters, checked with `grep -F`). The stale words are history inside a text the owner accepted verbatim. Item 7.12 Branch 2 does not ask for a design edit.
- Smallest fix: when the classify item (8.4) is read, treat `1.0a-facts.md:24` and the OQ-7 record as the closure of D9 and open item 22. Optionally append one closure sentence under design section 13 after D9. Do not rewrite D9.

### F2 (MINOR) `owner-decisions.md` calls OQ-8 and OQ-17 "still open", but both records are RESOLVED

- Side A: `T/artifacts/owner-decisions.md:55` ("Still open and not recorded here as decisions: OQ-8 ... and the optional OQ-17 and OQ-18").
- Side B: `T/phase-outputs/plans/OQ-8-run-id-decision.md:24-29` (Run id given, owner selection 2026-11-11), `T/phase-outputs/plans/OQ-17-cursor-template-decision.md:35-40` (owner kept 10 templates, 2026-11-11), `T/phase-outputs/discovery/1.0a-facts.md:54-56` (OQ-18 did not fire).
- Why MINOR. The file was compiled by item 7.13, which runs before items 7.14 to 7.17 (task file `:1229` and `:1236`), so the sentence was true when written. Item 7.13 does not require OQ-8 or OQ-17 rows. A later reader of the 1.0b artifact alone would still get a wrong picture.
- Smallest fix: add one dated line under that sentence naming OQ-8 and OQ-17 as RESOLVED with their record paths, or leave as is and rely on the records.

### F3 (MINOR) The `--agent-wait` change to INV-005 condition 1 rests on a relayed quote, and the SPEC's stated reason for the ban is only partly answered

- Side A (SPEC): `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:500` ("`worktree ps` (never with `--agent-wait`)"), `:504` (negative test for `--agent-wait`), `:510` ("`--agent-wait` turns on terminal wait-state reads, which is why it is forbidden"), `:143` (NFR-014: "exactly the eight pinned templates"), `:562` (GQ-109).
- Side B (decision): `T/phase-outputs/plans/OQ-1-agent-wait-decision.md:19-22` (allow, "Allow it, no conditions needed.", relayed by the coordinator, not selected by the owner in the executing session) and `:34-37` (24 calls, one idle worktree, 5 ms polling, locks under 5 ms could be missed). `T/artifacts/owner-decisions.md:17` states the relay.
- What is consistent. The change is recorded as design deviation D10 (`docs/designs/orchestrator-mode.md:837`), whose cited SPEC lines `310, 323, 500, 504, 510, 562, 619` and NFR-003 `:132` / NFR-014 `:143` all exist and say what D10 says. Ten templates and seven verbs agree in design `:537`, `:555`, `:759`, `:815`, `:895`. `--include-remote` stays the only forbidden token (design `:539`, `:66`). The version-scoped lock claim stays (`OQ-1:28-30`, design `:611`, `:816`). Phase 1 never issues either `--agent-wait` template (design `:535-536`, `:759`, `:895`), so the thin lock evidence does not touch any call the sweep makes.
- Why MINOR. The other six rows record direct owner selections; OQ-1 is the one relayed row, and it is labelled as such. The SPEC file itself keeps the old "never" text by design (D10 is the override).
- Smallest fix: none required. If the owner is next asked anything about the allowlist, confirm OQ-1 in the owner's own words.

### F4 (MINOR) Execution authorization is stated as fact in one file and as the executor's reading in another

- Side A: `T/artifacts/owner-decisions.md:29-33` ("It authorized item 7.10 only (the one style edit)").
- Side B: `T/phase-outputs/test-results/step-7.10-style-exception.md:13` and `:19` ("The executor reads 'Accepted ... Proceed' as the first and recommended option ... Scope of the authorization as the executor applies it").
- What is consistent. The owner's words match in both files (`owner-decisions.md:31`, result file `:11`), and `T/phase-outputs/test-results/decisions-mechanical.md:677-685` (check S7) matches them to exactly one user message at 2026-11-11T20:26:41.816Z in the session transcript. The scope (7.10 only, no skill, test, sync, install) is the same in both.
- Why MINOR. The words are verified; only the strength of the wording differs. The message itself is ambiguous ("it reported a decline"), and the executor said so openly.
- Smallest fix: in `owner-decisions.md:33`, change "It authorized item 7.10 only" to "The executor read it as authorizing item 7.10 only (result file line 19)".

### F5 (MINOR) The design append points at a "section 15.2 GQ-63/style/skill/test allocation" that section 15.2 does not contain

- Side A: `docs/designs/orchestrator-mode.md:1051` ("For section 7.6, section 15.2's GQ-63/style/skill/test allocation, section 17 item 20's GQ-63 boundary ...") and `T/revisions/chat-output-exception-20261109-133150/design-addendum.md:9` (same phrase).
- Side B: design section 15.2 step table `docs/designs/orchestrator-mode.md:926-962` has no style row and no GQ-63 allocation; GQ-63 appears only in the step 1.0b row (`:929`) and open item 20 (`:1010`). The allocation to items 7.10, 11.3 and 11.4 exists only in `design-addendum.md:23-31` and the task file.
- Why MINOR. The append is explicitly additive and narrow (`design-addendum.md:9`), the allocation is stated in full in the addendum, and section 7.6 and item 20 do exist. The phrase reads as if the table already carried that allocation.
- Smallest fix: none for this gate. A later docs pass may reword to "the allocation in this addendum, which section 15.2 does not list".

### F6 (MINOR) Stale line anchors in downstream text (the facts file, the task file, research/09)

- `T/phase-outputs/discovery/1.0a-facts.md:21` says the before/after comparison starts "line 769 onward"; `T/artifacts/readonly-probe.md:767` is the heading (`:769` is its first body line). Harmless.
- Task file `T/TASK-RF-sweep-phase1-20261108-072653.md:1501`, `:1812`, `:1815` cite "DESIGN line 638" for "The report holds no action control, no command to paste and no advice to delete anything under `.dev/tasks/`"; that text is at `docs/designs/orchestrator-mode.md:647` (`:638` is blank). `owner-decisions.md:44` already re-anchors this to `:647` and `:643`, so the two files disagree on the anchor. Items 8.12 and 10.5 are not yet done.
- Task file `:1267` (item 7.17 Context) cites DESIGN lines 550, 552, 971, 973; the live lines are `docs/designs/orchestrator-mode.md:557`, `:559`, `:993`, `:995`. `1.0a-facts.md:56` notes only the 973 case.
- `T/research/09-gap-fill.md:89` lists `--agent-wait` as forbidden in the 1.0a capture; design `:895` now says it is allowed by R5 but not run in step 1.0a. The capture did not run it (`readonly-probe.md:8`), so no behaviour differs.
- Smallest fix: the executor of items 8.12 and 10.5 re-reads the design at the quoted text, as `T/artifacts/pr422-409-check.md:35` already requires for the contract lines. No edit needed now.

### F7 (MINOR) The "identical apart from timestamps" rule was read to exclude the response envelope id

- Side A: `docs/designs/orchestrator-mode.md:897` ("must be identical apart from timestamps ... A difference stops the build and goes to the owner").
- Side B: `T/artifacts/readonly-probe.md:783` (raw bytes differ in the top-level `id` on every call; executor reading stated openly, with the HALT text the owner would use) and `1.0a-facts.md:21` (row 11, same reading).
- Why MINOR. Both files state the reading; the payloads are identical once `id` is removed for all 7 reads (`readonly-probe.md:775-781`). A literal reading would halt on every call, so the reading is reasonable. The owner was not asked.
- Smallest fix: none; the owner can overrule using the HALT text in `readonly-probe.md:783`.

### F8 (MINOR) The pr422 and #409 ancestry result rests on the local `origin/master` ref, which the item forbade refreshing

- Side A: `T/artifacts/pr422-409-check.md:3` and `:31` (local `origin/master` is `35073356`, not fetched) and design `docs/designs/orchestrator-mode.md:947` (point 3 names `origin/master`).
- Side B: I re-ran the git halves: `git merge-base --is-ancestor 2327fbd3 HEAD` exits 0, `git merge-base --is-ancestor 495eb96d origin/master` exits 1, `git rev-parse origin/master` prints `35073356ec1a...`, and `495eb96d` is reachable only from the `docs/409-orca-dashboard-designs` branches. Local `origin/master` is 24 commits ahead of HEAD (`5dc29d23`), not behind it.
- Why MINOR. The record discloses the limit, the result is reproducible, and no `gh` state for #409 was rechecked on 2026-11-11 (OQ-4 record `:20` already says it makes no claim about present status).
- Smallest fix: none.

### F9 (MINOR) The D4 re-anchor for "never posted" points at a `.gitignore` comment

- `T/artifacts/owner-decisions.md:42` says the never-posted statement "is at `docs/designs/orchestrator-mode.md:736`". Line 736 is the comment line inside the `.gitignore` snippet ("never posted (WC-16)"). The operative statement is in the WC-16 text at design `:679` ("it is never posted"). Both say it; `:679` is the better anchor.
- Smallest fix: cite `:679` (and `:736` as the second place).

## Checks

| Check | Description | Result |
|---|---|---|
| C1 | All 13 APPROVED quotes in `owner-decisions.md:41-53` (D3, D4, D5, GIT, L3, CR-01, PATHS, UPSTREAM, B1, B1-N1, S4, G1, F1) are substrings of the cited `APPROVED.md` line (10, 11, 12, 13, 20, 25, 29, 30, 35, 36, 47, 71, 90); `grep -F` gave 13 of 13 MATCH | PASS |
| C2 | The 13 row ids equal the list in task item 7.13 Action (`TASK-RF-sweep-phase1-20261108-072653.md:1231`); the "not applied" rows P1-C5 `:83` and H1 to H3 `:54-56` point at the right `APPROVED.md` lines; the constraint column equals research/09 Gap 1 table `:29-41` apart from the bracketed re-anchors | PASS |
| C3 | The re-anchors in `owner-decisions.md:42-44,48` hold against live files: `WORKER-CONTRACT.md:63` is a different WC-14; design `:647`, `:643`, `:947` hold the quoted text; design `:638` is blank. Only the `:736` choice is weak (F9, MINOR) | PASS |
| C4 | Rows OQ-1 to OQ-7 of `owner-decisions.md:9-15` match their records: option, quoted owner words, decider, date and cited line ranges (`OQ-1:19-22`, `OQ-2:33-36`, `OQ-3:36-39`, `OQ-4:40-43`, `OQ-5:33-36`, `OQ-6:32-35`, `OQ-7:40-43`); no row says "default" without the owner's words | PASS |
| C5 | OQ-6 is recorded as option (b) in the row (`owner-decisions.md:14`), the record (`OQ-6:32-35`), the addendum (`design-addendum.md:7`) and `BUILD-REQUEST.md:15`; decision, checked revision and execution permission are kept apart (`owner-decisions.md:19-33`) | PASS |
| C6 | SPEC section 13 INV-005 condition 1 (`merged-requirements.md:495-504`) against OQ-1 and design: seven verbs kept; `--include-remote` still forbidden; `--agent-wait` change is deviation D10 (design `:837`), whose SPEC line cites (`310, 323, 500, 504, 510, 562, 619`, NFR-003 `:132`, NFR-014 `:143`) all exist and match. Relay and thin lock evidence noted in F3 | PASS |
| C7 | SPEC section 13 INV-005 condition 2 (`merged-requirements.md:505`) against OQ-1 `:28-30`, design `:611`, `:816` and the live version: `readonly-probe.md:1013` string `1.4.245-aidev02.9cfecdd30b2a` has leading part `1.4.245`, equal to `CHECKED_ORCA_VERSION`; the build suffix change does not affect the match rule | PASS |
| C8 | DESIGN 7.3, 11, 12, 13, 15.1, the GQ-109 row (`:66`) and the Fix cycle 3 R5 row (`:1047`) agree on ten templates, seven verbs, `FORBIDDEN_TOKENS = {--include-remote}`, four "not called in Phase 1" templates, and the version-scoped claim; no leftover "eight templates" or "never carries `--agent-wait`" in the design (`grep`: only `templates 1 to 8` of 10 in `:851`, `:895`, and the quoted SPEC text in D10 `:837`) | PASS |
| C9 | DESIGN section 8 WC-16 text (`:677-679`) against OQ-3 (`OQ-3:14`, `:36-39`) and OQ-1: new WC-16, additive to master's sweep, no heartbeat update, no `--agent-wait` listing run by `/sc:sweep`, never posted, recommends nothing; `WORKER-CONTRACT.md:110` still holds the `worktree ps --agent-wait` sweep | PASS |
| C10 | DESIGN section 15 against OQ-2, OQ-4, OQ-5, OQ-7 and OQ-8: `<root>/.dev/sweeps/` and `<YYYYMMDD-HHMMSS>` (design `:201`), `495eb96d` pin and 7.5 ordering (`:603`, `:642-643`), `"6h"` only as CLI default (`:59`), D9 (`:836`), 15.1 Run rule (`:894`, quoted correctly in `OQ-8:13`). F1 and F5 noted | PASS |
| C11 | OQ-7 quotes of D9 and of open item 22 match design `:836` (SPEC-text and Design columns) and `:1012` (`grep -F`); heading `:822` and row `:836` are as the record says | PASS |
| C12 | `1.0a-facts.md` against `readonly-probe.md`: section line anchors 12, 441, 455, 461, 475, 735, 785, 830, 910, 964, 968, 982, 997, 1015 all equal the probe headings; F6 notes the one `:769` versus `:767` slip | PASS |
| C13 | `1.0a-facts.md` values against probe bodies: join fields (`probe:493-499`), `agentWait` absent (`:505`), `liveness.verdict` and `status` paths (`:506-507`), time forms (`:508-509`), page object (`:469`), creator fields (`:761-763`), worktree path and `totalCount` 28 (`:791-793`), unknown-Run shapes (`:919-962`), regexes and samples (`:972-980`), version (`:1008`), tab-map join and four of five banners (`:1056-1058`) | PASS |
| C14 | Facts coverage: 15 rows for open items 1 to 11, 15, 16, 22, 23; STILL UNVERIFIED rows 3, 6 (`agentWait`), 9, 16 match the probe's "not captured" list (`probe:1066`); no OQ-18 file exists and the facts file says so (`facts:55`) | PASS |
| C15 | Facts and OQ-8 against probe: Run `run_a4723d345399`, 5 Dispatch ids, all `completed` / `succeeded` / `released` (`OQ-8:27`, `probe:20`); the 10 Run ids in `OQ-8:35-42` plus `run_000000000000` and the 5 `ctx_` ids all match the regexes `run_[0-9a-f]{12}` and `ctx_[0-9a-f]{12}` (re-run, 16 of 16) | PASS |
| C16 | OQ-17 against design and facts: quotes of design `:559` and `:995` and of probe section 3 (`probe:469`) are exact; refusal outcome in `OQ-17:37-40` equals `facts:56` and item 7.17 text (`task:1272`); allowlist stays at 10 | PASS |
| C17 | Probe before/after reading against design `:897` | PASS (F7, MINOR) |
| C18 | `pr422-409-check.md` against design `:947`, research/09 Gap 3 `:113-115` and live git: `2327fbd3` ancestor of HEAD (exit 0), `495eb96d` not ancestor of local `origin/master` (exit 1), both commit objects exist, `git rev-parse origin/master` = `35073356ec1a...` as recorded | PASS (F8, MINOR) |
| C19 | `tests/sweep/fixtures/` against `SOURCES.md` and probe: 19 `captured-*.json` plus `SOURCES.md` (20, equals `decisions-mechanical.md:565-592`); for all 5 workers the pane key (`:` to `+`), handle and terminal handle join to the tab-map fixture; `agentWait` absent, `status` completed, verdict exited; page object, unknown-Run bodies and no-binding sentence equal the probe; worktree arrays cut to 3 and 2 with matching `totalCount` as `SOURCES.md:12` says; no `coder` or owner name and no non-fake UUID left | PASS |
| C20 | `decisions-mechanical.md` Run 3 against disk: 6 qualifier lines (57, 62, 64, 73, 84, 94), 7 hunks, `## Work discipline` at 107, 238 lines now versus 234 at HEAD, `git diff --shortstat` = 11 insertions, 7 deletions, only `src/superclaude/output-styles/pragmatic.md` modified under `src`/`tests` apart from untracked `tests/sweep/`; no skill, CLI or test output exists | PASS |
| C21 | Actual style text (`pragmatic.md:22-26`) against `design-addendum.md:13-21,27` and `BUILD-REQUEST.md`: same five conditions (explicit top-level coordinator assignment, loaded `sc-sweep-protocol` for an actual `/sc:sweep`, exit 0, parsed counts and path, successful report Read); same exclusions (workers, subagents, other messages, ordinary person-run, quoted sweep, failures, unknown or conflicting role); stderr visible; no advice; "Formatting never authorizes advice the sweep skill prohibits" (`:25`); chat-presentation only (`:26`) | PASS |
| C22 | Narrow override scope: only the final successful reply is exempt (`pragmatic.md:23`); six later restatements qualified and examples labelled non-exempt (`:57, 62, 64, 73, 84, 94`); the length-budget sentence (`:29`) and everything from `## Work discipline` (`:107`) to the end are identical to HEAD (`step-7.10:78`, `decisions-mechanical.md:606-622`); runtime safety, Python report and CLI JSON unchanged (`:26`); design `:663` (skill prints no recommendation) and `:662` step 4 (counts and path) agree with the exempt reply | PASS |
| C23 | Old no-exception text outside the override: the pre-edit `No exceptions` line survives only as history (OQ-6 record `:12`, research/09 `:20`, step-7.10 diff `:44`) and in the installed HOME copy `~/.claude/output-styles/pragmatic.md:22` (not refreshed by `make sync-dev`, disclosed at `step-7.10:85` and `design-addendum.md:39`). No live canonical source contradicts the override | PASS |
| C24 | Step-7.10 result file against the style file: line numbers it gives (22-26, 57, 62, 64, 73, 84, 94, 25, 107), the 234 to 238 line count and the 7 removed / 11 added counts all equal the disk state; its excerpts equal the diff recorded in `decisions-mechanical.md:729-763` | PASS |
| C25 | Authorization chain: owner words and timestamp equal across `owner-decisions.md:31`, result file `:7-11` and the transcript row in `decisions-mechanical.md:682`; scope 7.10 only is the same | PASS (F4, MINOR) |
| C26 | Revision evidence consistency: `research-gate-cycle1.md` (F0 = 2, F1 = 0, five PASS, `gpt-6.1-sol`) equals `BUILD-REQUEST.md:33`; `delta-manifest.md:31` row for 7.28 matches the lens in task item 7.28 (`task:1349`); second revision request `plan-defect-fixes-20261110/BUILD-REQUEST.md:7` carries "Fix the plan first" as `owner-decisions.md:28` says | PASS |

Notes on scope. I did not certify future skill or test work (11.3, 11.4) or rewrite history. `decisions-mechanical.md` Runs 1 and 2 were not re-read; Run 3 is the latest and its summary (`:769`) lists all checks PASS with C3 SKIP, which matches C3 SKIP for the absent OQ-18 file.

Verdict: PASS
Blocking count: 0

