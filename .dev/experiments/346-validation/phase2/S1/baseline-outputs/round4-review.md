# Round-4 changed-line review (Task 13)

Reviewer: independent worker (did not write or revise the spec).
Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (SPEC)
Baseline: `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md` (BASE)
Inputs: `decisions/APPROVED.md`, its wording sources, `review/disposition-round4.md`.
Severity model: merged PR #343 (blocking or minor; only blocking fails).

## 1. Method
- Diff: `git diff --no-index -U0 --word-diff=plain BASE SPEC` (56 hunks; `--stat`: 137 insertions, 91 deletions), run 2026-11-02. Only lines inside those hunks were reviewed for defects.
- Each APPROVED.md item was compared word by word against its named wording source, read live: `decisions/D1/debate/adversarial/merged-output.md:210-320` (W1-W16) and `decisions/D1/RECOMMENDATION.md:62-85`; `decisions/D2/RECOMMENDATION.md:63-126` (section 4); `decisions/D3/RECOMMENDATION.md:57-79` (section 5); `decisions/D4/RECOMMENDATION.md:18-35,69-104` (sections 2 and 5) plus `decisions/D4/debate/adversarial/merged-output.md:45-94`; `decisions/D5/RECOMMENDATION.md:41-62` plus `decisions/D5/debate/adversarial/merged-output.md:104-213`; `decisions/git-ownership/RECOMMENDATION.md:43-113` (sections 4-6); `changes/CR-01-feature-worktree-hierarchy.md:1-54`; `review/final-diff-review.md:50-83`; `review/issue-326-evaluation.md:44-56,82-90`.
- Task 12's own brief was read from Orca's read-only task list (`orca orchestration task-list --run run_8c464f208721 --json`, task `task_ec4df0cad251`). It says "Replace section 9 open decisions with a short record of the approved outcomes" and "every added or changed sentence must trace to one item ID in APPROVED.md". That sentence is the stated reason for every "superseded by the short record" row in the disposition, and it holds.
- Citations on changed lines were re-read in the live files and Orca help (section 6 lists them). The three changed shell checks (AC-C1, AC-C6, the AC-0.7 grep) were run read-only.
- Not done, per the task scope: no `/sc:spec-panel`, no review of unchanged text, no reopening of approved decisions.

## 2. Item table
"Faithful" means the spec text matches the wording source (verbatim, or changed only as the disposition records and an APPROVED.md precedence rule allows). "Reason holds" means the item was not applied and the stated reason was checked and is true. Line numbers are `SPEC:N` as of 2026-11-02 (451 lines).

### D1-D5 and GIT
| ID | Where (`SPEC:N`) | Verdict | Notes |
|---|---|---|---|
| D1 W1 | 55 | Faithful, verbatim | |
| D1 W2 | 59 | Faithful, verbatim | Adds WC-13 to the worker-session list (D5 Edit 4), as D5 asks. |
| D1 W3 | 60-62 | Faithful, verbatim | Brief guard, never-as-worker list, nested propagation rule. See finding B1. |
| D1 W4 | 84 | Faithful, verbatim | Joined with D4's authorization clause and GIT 4.3's placement clause in one sentence. |
| D1 W5 | 86 | Faithful, verbatim | |
| D1 W6 | 96 | Faithful, verbatim | |
| D1 W7 | 125, 128 | Faithful, verbatim | |
| D1 W8 | 315, 319 | Faithful, verbatim | |
| D1 W9-W11 | 390 (record) | Not applied; reason holds | They edit the old D1 option bullets; Task 12's brief replaced section 9 with a short record. Option (c) is recorded at 390 and selected at 55. |
| D1 W12 | 437 | Faithful, verbatim | See minor m7 (names an option no longer described). |
| D1 W13 | 448-451 | Faithful, verbatim | |
| D1 W14 | 282-283 | Faithful, verbatim; merged with CR-01 as APPROVED.md asks | See findings B1 and m1. |
| D1 W15 | 307, 309, 313, 314, 320, 364-365 | Faithful, verbatim | AC-2.9 sits after AC-2.6 as W15 says. See minor m6. |
| D1 W16 | 142, 152, 222 | Faithful, verbatim | |
| D2 4.1 | 391 (record) | Not applied; reason holds | Short record keeps (a), (c), the Ruling line format (`ledger.md:65,71`), "never relays" and (b) rejected. |
| D2 4.2 | 71 | Faithful, verbatim | |
| D2 4.3 | 72 | Faithful, verbatim | |
| D2 4.4 | 95, 100-120 | Faithful, verbatim (dagger provenance marks dropped) | See minor m4. |
| D2 4.5 | 169 | Faithful, verbatim | Same cell also carries D4's implement sentence. |
| D2 4.6 | 326 | Faithful | Four bullets flattened into one cell sentence; content identical. |
| D2 4.7 | 15, 224, 379 | Faithful | `qa.md:247-256`, `:249`, `:254`, `:283`, `ledger.md:65,71,155-156`, `retry.md:498` re-read: all hold. |
| D3 Edit 1 | 201, 392 | Faithful, adapted | Option (a) text moved to section 4 (short record); "(CR-01 T3)" dropped; L2 sentence added (disposition C3). See minor m3. |
| D3 Edit 2 | 174 | Faithful | "(the worker may use `ask` or `escalation`)" deleted; new anchors `SKILL.md:43-49,51-86,234-248,267-274,313-318` re-read and hold. |
| D3 Edit 3 | 75, 78 | Faithful | `:47-49` is the top-level rule; `:51-80` is the attended poll loop. |
| D3 Edit 4 | 329 | Faithful, verbatim | `prompt.outcome` value `journaled` exists in Orca (`/opt/Orca/resources/app.asar.unpacked/out/cli/agent-launch-test-fixtures.js:22`). |
| D3 Edit 5 | 224, 234 | Faithful | Count renumbered for CMD (37, or 38). |
| D4 block (section 5) | 393 (record); rules at 77, 84, 90 | Not applied as a block; reason holds; content moved | Outward list, commit conditions, refusals, confirm at the moment of action, fork-only and review-before-push all appear in WC-9 (77) and 2.3 (84, 90). |
| D4 WC-9 | 77 | Faithful | `README.md:31` citation removed. See minor m10, m11. |
| D4 WC-5 | 73 | Faithful, verbatim | |
| D4 2.3 | 84, 88, 90 | Faithful | Authorization clause verbatim; review before push, grant ends at `worker_done`, no commit or merge where a worker runs or an implement Task is frozen, placement record, distinct slugs, absolute report directory in a child. |
| D4 section 3 rows | 160, 169, 173, 181 | Faithful | |
| D4 `/sc:git` row | 193 | Faithful (GIT 4.4 text, same content) | |
| D4 AC-4.2 + P0 check | 327; 305 (AC-0.8) | Faithful to the wording, but the P0 placement is unimplementable | See finding B2. |
| D4 7.2 | 282-283 | Faithful through W14 | |
| D5 Edits 1-3 | 28, 37, 375 | Faithful, verbatim | |
| D5 Edit 4 | 81, 59 | Faithful, verbatim | INV-005 given its file path; `invariant-probe.md:25` holds INV-005. |
| D5 Edit 5 | 98 | Faithful | Two sentences joined into one bullet; "(section 9)" added. |
| D5 Edit 6 | 244-254, 276-279 | Faithful | Block verbatim; AC-C1 run 2026-11-02 prints nothing; AC-C6 prints `"nestedWorkerMaxDepth":1` (one profile, `local-default`). |
| D5 Edits 7-10 | 291, 304 + 341-342, 363, 429 | Faithful, verbatim | AC-0.7 grep run: lists the three files D5 names. |
| D5 M10 | 394 (record) | Not applied; reason holds | Short record; see minor m9. |
| GIT 4.1 | 77 | Faithful, with D4 precedence | Disposition C1 checked against `git-ownership/RECOMMENDATION.md:105-107` (section 6 adopts D4 on points 1-3) and `:73` (4.6 keeps installs with the coordinator): holds. D3 (b) exception dropped per L1. |
| GIT 4.2 | 79 | Faithful, minus the pr-submit trigger (L1) | See minor m2. |
| GIT 4.3 | 84, 88, 90 | Faithful, adapted per L1 and D4 | "main chat" → "own conversation" (D4); "run from the PR-head checkout" → "run as section 4 states" (L1). |
| GIT 4.4 | 193 | Faithful, verbatim | |
| GIT 4.5 | none | Not applied; reason holds | L1 drops the per-PR worker and the main-chat wording; section 9 is a short record. |
| GIT 4.6 | none | Not applied; reason holds | APPROVED.md GIT row: D4's wording wins. |
| GIT 4.7 | 77, 306, 330 | Faithful | Staging lines re-read: `managed-workspace.md:36`, `ledger.md:3`, `sc-workflow-protocol/SKILL.md:28`, `task/SKILL.md:35`, `task-builder/SKILL.md:2237`: all hold. See minor m5. |

### Loose ends and other items
| ID | Where (`SPEC:N`) | Verdict | Notes |
|---|---|---|---|
| L1 | 201, 77, 79, 90, 396 | Faithful | Coordinator's own session carries a run only after AC-4.4 (2), as D3 allows. |
| L2 | 201, 396 | Faithful in content | PR opened after every child is merged back; its head is a branch cut from the feature branch (disposition C3, sound: git checks a branch out in one worktree only). See minor m3. |
| L3 | 90, 77, 396 | Faithful | |
| CR-01 (four edits) | 84, 79, 88, 330 | Faithful | Applied through GIT 4.2/4.3 text (C4); AC-4.5 verbatim. "Linked to its issue" correctly dropped per the owner's no-linking resolution (`CR-01:45`). |
| CR-01 owner resolutions | 88, 282, 90 | Faithful | |
| FDR-D1 | 74 | Faithful | Comparison excludes the report-directory value and names the coordinator as the one comparing. |
| FDR-D2 | 71, 409 | Faithful | Took the fix direction "reword the opening sentence". |
| FDR-D3 | 282-283, 448, 451 | Applied, but the fix introduces finding B1 | Edits committed and synced into the worktree; copy precedence listed as UNVERIFIED 24. |
| FDR-D4, D5 | none | Not applied; reason holds | Fan-in line (122) and reading-guide line (134) are absent from the diff, so no other item edits them. |
| FDR-D6 | 74 | Faithful | `task-update --help` line 21 holds ("set --status failed --result cancelled"). |
| FDR-D7 | none | Not applied; reason holds | Phase edits are now committed before Orca creates the worktree, so step 6 lists none of them and "step 6 empty" can hold. |
| F0 | 193 | Faithful | |
| F1 | 77, 169 | Faithful in D4's form | |
| F2 | 79, 88 | Faithful as replaced by CR-01 | `.dev/worktrees/<run>-<n>/` not used. |
| F3 | 88 | Faithful | Guard widened by GIT 4.3. |
| F4 | 90 | Faithful | |
| F5 | 90 | Faithful | `/sc:git` not named as the outward path. |
| CMD | 132, 136, 144-145, 72, 221, 231-236, 238, 415 | Faithful | `ls src/superclaude/commands` lists 45 command files; 12 + 27 + 6 = 45; P1 16, P2 31, P3 35, P4 37 add up; `HOW-WE-WORK.md:325,326` and `core/CLAUDE.md:66` hold; graph/impact citations hold. |
| PATHS | 88, 282 | Faithful | The only `.dev/worktrees` strings in the spec (lines 88, 282) say "never"; `CLAUDE.md:299` citation gone. |
| UPSTREAM | 90 | Faithful | |

## 3. Findings
2 blocking, 11 minor. Every finding is on a changed or added line. Minor findings are notes under PR #343 and trigger no fix.

### B1. BLOCKING: the 7.2 live check can never dispatch a converted command, because `~/.claude` is never updated but every copy must carry the section
- **Lines:** `SPEC:282` ("`~/.claude` is never reinstalled for this check"), `SPEC:283` ("confirm before dispatch that every existing copy of its file (`<worktree>/.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`) has its `## Unattended mode` section"), `SPEC:60` (the guard refuses when "the copies disagree").
- **Evidence:** `make sync-dev` updates only the project `.claude/` copy (`CLAUDE.md:156`: "Copy src/superclaude/{skills,agents,commands,hooks,templates} → .claude/"). The installed copy exists and is pre-phase: `~/.claude/commands/sc/analyze.md` (3,551 bytes, 2026-11-02 14:03) has 0 matches for `Unattended mode` today. During a phase's acceptance checks the phase is not yet installed, and 7.2 forbids installing it. So for every command that gains `--unattended` in that phase, the worktree copy has the section and the `~/.claude` copy does not: step 1's pre-dispatch confirmation fails, and if dispatched anyway the guard refuses with `guard refused: command copies disagree (stale copy)`. D1's own sources show the gap: `decisions/D1/debate/adversarial/merged-output.md:189` keeps `~/.claude` untouched, while `decisions/D1/debate/adversarial/refactor-plan.md:235` (risk 18) expects "the branch base or `make sync-dev` step" to fix a disagreement, which neither can do for the `~/.claude` copy.
- **Effect:** every 7.2-based check for a converted command (AC-1.2, AC-1.6, AC-2.2, AC-2.3, AC-2.6, AC-3.2-3.4, AC-4.1, AC-4.2, AC-4.5) fails, and the refusal checks AC-1.7 case 1 and AC-2.9 pass for the wrong reason (a "copies disagree" refusal still starts `guard refused:`). Later phases wait for earlier checks (`SPEC:216`), so P1 can never pass. This is unimplementable as written.
- **Fix direction (coordinator or owner to pick; not applied here):** either the live checks run the worker against a scratch Claude configuration that holds an install of the phase branch (whether Orca and Claude Code honour such a configuration is UNVERIFIED), or updating the person's `~/.claude` from the phase branch becomes a recorded decision point before the live checks, like the commit decision already at `SPEC:282`. Then reword the "never reinstalled" sentence to match.

### B2. BLOCKING: AC-0.8 runs in P0, where the WC-9 commit it tests cannot happen
- **Lines:** `SPEC:305` (AC-0.8, P0) against `SPEC:77` (WC-9 condition (3): "the command has exited with `worker_status: succeeded`").
- **Evidence:** `worker_status` exists only in the WC-4 contract, which commands write from P1 (`SPEC:221`; AC-0.4 at `SPEC:301`: "the contract arrives in P1"). No command accepts `--unattended` after P0 (`SPEC:230`). WC-5 forbids reading a command's own `status` instead (`SPEC:73`). So a commit-authorized P0 worker must refuse the commit. AC-0.8 then either fails ("the only change is new commits on the worker's child branch" with no commit), which blocks P1 (`SPEC:216`), or passes with zero commits and proves nothing about the grant. The reviser listed this as residual observation 3 (`review/disposition-round4.md:131`) and left it unresolved. The placement comes from D4's own wording ("Also add one P0 check", `decisions/D4/RECOMMENDATION.md:102`), so the item was applied faithfully; the defect is that the result cannot run.
- **Fix direction:** move AC-0.8 to P1, the first phase with contracts, keeping D4's content unchanged, and record it as a placement adaptation. The owner confirms, because D4 named P0. This changes no approved outcome.

### Minor findings (notes only)
| # | Line | Defect | Evidence | Fix direction |
|---|---|---|---|---|
| m1 | `SPEC:84`, `:88`, `:283`; also AC-0.8 `:305` and AC-4.2 `:327` | Steps required "before dispatch" in a worktree that `worker-start` itself creates. 2.3 names `worker-start --worktree new-child` as the child verb, then requires `make sync-dev` before dispatch when setup does not run it; 7.2 option A confirms the worktree's command copy before dispatch; AC-0.8 and AC-4.2 record `git -C <worker worktree>` before dispatch. | `orca orchestration worker-start --help` line 40: "New worktrees use agent-first creation ... Repository start-immediately runs setup beside the agent". The worktree and the agent arrive in one call. Inferable from 7.2 option B (`orca worktree create`, sync, then `--worktree path:`). | Name the two-step route (create with `orca worktree create --parent-worktree ... --base-branch ... --setup run`, sync, then `worker-start --worktree path:`) for children while UNVERIFIED item 27 is open; take the "before" records from the base branch. |
| m2 | `SPEC:79` (WC-11) | "Workers share the feature worktree only when they write nothing but their own report directory" makes the `/sc:implement` trigger's condition ("and any other writer ... may write outside `.dev/`") dead text, and gives source-editing workers with no trigger (cleanup, improve, document) a child only by implication. | GIT 4.2 verbatim; disposition residual 2 (`review/disposition-round4.md:130`). Behaviour inferable: any worker that writes outside its report directory gets a child. | State that rule once and drop the redundant condition. |
| m3 | `SPEC:396` vs `:201` | Section 9's L2 row says the PR is "opened from the feature branch"; section 4 opens it from the child's own branch cut from the feature branch. Same content, different words. | Disposition C3 (`review/disposition-round4.md:101`). | L2 row: "from a branch cut from the feature branch after merge-back". |
| m4 | `SPEC:120` | "never in a new or child worktree" can be read as forbidding a child, yet implement often runs in a child (`SPEC:79`) and "A resume runs in its existing child" (`SPEC:88`). | D2 4.4 verbatim. | "never in a newly created worktree". |
| m5 | `SPEC:77` (WC-9) | The staging deferral is required under `--unattended` for workflow, which accepts the flag from P1 (`SPEC:221,231`), and for `/task` under tdd (P2), but no phase row or check names the edits to `sk/sc-workflow-protocol/SKILL.md:28` or `sk/task/SKILL.md:35`. | AC-0.9 (`SPEC:306`) only allowlists them in P0. Inferable: each command's conversion phase. | Add the deferral to the workflow P1 fix and the tdd P2 fix. |
| m6 | `SPEC:313` (AC-1.7) | Live checks cover guard cases 1-3 but not the "copies disagree" refusal, one of the four reasons AC-1.1 checks statically (`SPEC:307`). | W15 verbatim. | One more AC-1.7 case, or note the gap in 7.4. |
| m7 | `SPEC:379`, `:224`, `:437` | Edited lines keep open-decision wording: non-goal 6 "unless the user chooses D2 option (b)" though section 9 records (b) as rejected (`SPEC:391`); P4 "so it needs the user's decision first"; UNVERIFIED 13 "how risky D1 option (b) is", an option section 9 no longer describes. | Only citations changed on 379 and 224; 437 is W12. | Point to `decisions/<ID>/RECOMMENDATION.md`, or reword in the past tense. |
| m8 | `SPEC:306` (AC-0.9) | Quotes "a worker writes no git state" as WC-9's words; WC-9 (`SPEC:77`) has no such phrase. It is the GIT row's wording (`SPEC:395`). | Citation precision. | "WC-9's no-git-write rule". |
| m9 | `SPEC:394` | The D5 record drops M10's second precondition before any raise: "the mailbox that receives a depth-2 worker's questions and `worker_done` is established". | `decisions/D5/RECOMMENDATION.md:49`. | Add the clause, or rely on the pointer to the D5 file. |
| m10 | `SPEC:77` (WC-9) | "stages with `git add -- <paths>` plus `.dev/tasks`, commits with `git commit --only -- <paths>`" leaves open whether `.dev/tasks` is in the commit; if not, it stays staged and uncommitted in the child. | D4 says the commit is "of its own files plus `.dev/tasks`" (`decisions/D4/RECOMMENDATION.md:27`); GIT 4.1 has the same ambiguous wording. | `git commit --only -- <paths> .dev/tasks`. |
| m11 | `SPEC:77` (WC-9) | "A worker that finds `index.lock` in its worktree reports `blocked` with the path": the finder is the worker session, but contracts are written by the command (WC-4 owner), and a `blocked` contract needs `blocked_question` (7.2 step 4). Who writes what is unstated. | GIT 4.1 verbatim. | "reports `worker_done --outcome failed` with the path in the body". |

## 4. Untraced changed sentences
Every changed sentence was matched to an item ID through the diff, except these:

| `SPEC:N` | Sentence | Note |
|---|---|---|
| 6-7 | Line 6 relabelled from "Revised last:" to "Revised:"; new line 7 "Revised last: task_ec4df0cad251 (Task 12) applied the owner-approved items ..." | Header provenance, same form as lines 4-6. No item asks for it (disposition section 4, last Decisions row, says so). States no rule, check or mechanism, so it is harmless. |

Sentences that look new but do trace: "and never under `.dev/worktrees/`" (88) → PATHS; "if that setup does not run `make sync-dev` (UNVERIFIED item 27), the coordinator runs it before dispatch" (88) → CR-01 open question 2; the L2 sentence in section 4 (201) → L2 with disposition C3; "Orca counts failures only per Task ..." (74) → FDR-D1; the stall-settle clause (74) → FDR-D6; "and the flag-STOP `blocked` of impact and graph" (72) → CMD; "Progress posts ..." (90) → F4; "(section 9)" (98) → D5 Edit 5 pointer; the "Inventory verdicts" sentence (415) → CMD.

## 5. Verdict
**FAIL.** Two blocking findings: B1 (the 7.2 live checks cannot dispatch a converted command while `~/.claude` stays pre-phase) and B2 (AC-0.8 cannot exercise the WC-9 commit in P0). Every APPROVED.md item was applied faithfully or not applied for a reason that holds; both blocking findings come from approved wording whose combination cannot run, not from a distorted item. The 11 minor findings are notes only.

## 6. Self-Audit
What was checked, and how:
- Every one of the 56 diff hunks was read; every APPROVED.md row (D1-D5, GIT, L1-L3, CR-01, FDR-D1..D7, F0-F5, CMD, PATHS, UPSTREAM) has a row in section 2, compared against its source text read live.
- Task 12's brief was read from Orca to test the "short record" reason; it holds.
- Disposition conflicts C1-C7 were checked against their sources; C1 (D4 over GIT) and C2 (L1) follow APPROVED.md precedence; C3 is sound git behaviour; C4-C7 lose no approved rule.
- Live citation re-reads, all holding: `sk/sc-pr-submit-protocol/SKILL.md:43-58,80-86,234-248,267-268,273-275,313-318`; `sk/sc-implement-protocol/refs/qa.md:247-256,283`; `refs/ledger.md:3,65,71,153-156`; `refs/retry.md:41,220,498`; `sk/sc-implement-protocol/SKILL.md:35,111,113`; `refs/managed-workspace.md:36`; `sk/sc-workflow-protocol/SKILL.md:28,58`; `sk/task/SKILL.md:35`; `sk/task-builder/SKILL.md:2237`; `sk/sc-brainstorm-protocol/SKILL.md:185`; `sk/sc-post-release-protocol/SKILL.md:340,351`; `CLAUDE.md:37,50,156`; `src/superclaude/core/HOW-WE-WORK.md:22,208-223,280,282,324-326`; `src/superclaude/core/CLAUDE.md:66`; `cmd/graph.md:31,33,48,64`; `sk/sc-graph-protocol/SKILL.md:23,85,110,158`; `cmd/impact.md:37,47-50`; `sk/sc-impact-protocol/SKILL.md:15,29,75,98-100`; `CAPS:97,103,115,126,139`; `review/issue-326-evaluation.md:51,74`; `decisions/D5/debate/adversarial/invariant-probe.md:25`.
- Orca help read live: `orchestration worker-start --help` (lines 3, 18, 21, 36, 40-41), `orchestration task-update --help` (lines 3, 20-21), `worktree create --help`, `worktree rm --help`, `agent launch --help`; `orca-ide skills get orchestration` lines 36-41.
- Commands run read-only: AC-C1 (prints nothing), AC-C6 (`"nestedWorkerMaxDepth":1`), the AC-0.7 grep (three files), `ls src/superclaude/commands` (45 command files), a grep of the spec for `.dev/worktrees` (lines 88 and 282 only).
- Arithmetic: 12 + 27 + 6 = 45; P1 16, P2 31, P3 35, P4 37; 37 + load + pr-submit = 39 = 12 + 27.
- Not checked: unchanged text, and whether Orca honours a scratch Claude configuration (B1's first fix direction, UNVERIFIED).

## Decisions
| Decision | Options | Rationale |
|---|---|---|
| Grade of B1 | blocking; minor | Blocking: as written, no 7.2 check for a converted command can reach a pass, and phase gating (`SPEC:216`) then stops P1. No reading of the spec avoids it; the fix needs a new decision (scratch configuration or an install step). |
| Grade of B2 | blocking; minor | Blocking: the P0 gate either never passes or passes on zero commits; the remedy (move to P1) changes a placement D4 named, so it needs the owner, not inference. |
| Grade of m1 and m2 | blocking; minor | Minor: in each case one consistent behaviour can be read from the spec itself (7.2 option B; the strict sharing sentence). |
| Findings that trace to approved wording | report; skip as "approved" | Report: the task scope covers defects on every changed line; approval covers the outcome, not wording that cannot run. No approved outcome is reopened by either fix direction. |
| Self-Audit on a FAIL | include; omit | Included: it shows what was checked, at no cost to the verdict. |

## Recheck after fix pass 1 (Task 15)
Reviewer: independent worker (did not write the spec or the fix pass). Task `task_dcf1a60db1bb`, run 2026-11-02.
Spec: `specs/orca-worker-contract-spec.md` (SPEC, 451 lines). Baseline: `specs/history/spec-v5-after-round4.md` (BASE). Inputs: `decisions/APPROVED.md:32-36` ("Round-4 review fixes"), `review/disposition-round4.md:137-163` ("Fix pass 1"), findings B1 and B2 above (`:97-106`). Severity model: merged PR #343, as in section 3 above.

### R1. Method
- Diff: `diff BASE SPEC` gives 7 hunks: `SPEC:216`, `:282`, BASE `:305` (removed), `:313` (added), `:358`, `:393`, `:414`. Only those lines, and the unchanged lines they touch, were reviewed.
- B1 and B2 were compared word by word with `APPROVED.md:35-36`.
- The B1 install mechanism was traced in the live installer: `src/superclaude/cli/main.py:29-46,178-204,340-378`, `install_core.py:62-69,106-125`, `install_commands.py:46-62`, `install_skills.py:100-104`. `uv run python -c "import superclaude.cli.install_core as m; print(m.__file__, m._get_core_source())"` was run in this checkout (prints this checkout's `src/superclaude/...`).
- Installed state read: `~/.claude/commands/sc/analyze.md` (3,551 bytes, 2026-11-02 14:03) and `~/.claude/skills/sc-adversarial-protocol/SKILL.md` exist.
- Spec-wide grep for `AC-0.8`, `AC-1.8`, `P0 check`, `phase branch`, `never reinstalled`, `superclaude install`.
- Not done, per scope: no `/sc:spec-panel`, no recheck of minor findings m1-m11, no review of unchanged text.
### R2. B1/B2 resolution
| ID | Approved fix (`APPROVED.md`) | Applied as stated? | Defect resolved? | Evidence |
|---|---|---|---|---|
| B1 | `:35`: owner approval before a phase's live tests, then `superclaude install` from the phase branch; one approval per phase; reinstall from master if abandoned; replace "never reinstalled" | Yes. Every clause is at `SPEC:282`; "`~/.claude` is never reinstalled for this check" is gone (grep finds no match). The added `uv run superclaude install` inside a checkout of the branch is a sound adaptation: `uv run` resolves the installer to the checkout's own `src/superclaude/cli/install_core.py`, and `_get_core_source` returns `src/superclaude/core` there (`install_core.py:117-122`, run 2026-11-02). Consequential edits at `SPEC:216` and `:414` remove the "no user decision" contradiction. | **No.** The command as written skips every file already in `~/.claude`, so the phase's edited command files are never copied and the stale-copy refusal B1 described still fires. See finding N1. | `install_commands.py:55-57`; `main.py:35-39,188` |
| B2 | `:36`: move AC-0.8 from P0 to P1, content unchanged; record as a placement adaptation of D4's "one P0 check" | Yes. P0 row removed; `SPEC:313` AC-1.8 has the same Check and Pass cells word for word (diff of the two rows differs only in phase and ID); adaptation recorded at `SPEC:393` and in `disposition-round4.md:144,148`. Renumbering to AC-1.8 is consistent with the per-phase ID scheme (`SPEC:306-312`). | **Yes.** In P1 every condition of the WC-9 grant can hold: the grant rule is in `WORKER-CONTRACT.md` from P0 (`SPEC:59,220`); P1 commands write the WC-4 contract with `worker_status` (`SPEC:221,231`), so condition (3) (`SPEC:77`) can be met; `worker-start --worktree new-child` (`SPEC:84`) meets condition (2). References updated at `SPEC:358` and `:393`; grep finds no `AC-0.8` left. | `SPEC:77,221,231,313,358,393` |
### R3. Changed-line findings
1 blocking, 3 minor. All on changed lines. Minor findings are notes under PR #343 and trigger no fix.

#### N1. BLOCKING: `uv run superclaude install` without `--force` leaves `~/.claude` pre-phase, so B1's failure recurs
- **Line:** `SPEC:282` ("installs that phase into `~/.claude` by running `superclaude install` from the phase branch, as `uv run superclaude install` inside a checkout of that branch"; "reinstalls from master (`superclaude install` from master)").
- **Evidence:** `superclaude install` passes `force=force` to every installer step, and `--force` is off unless given (`main.py:35-39,178,188,196,204`). Each step skips a target that already exists: commands `if target_file.exists() and not force: skipped_commands.append(...); continue` (`install_commands.py:55-57`), core files (`install_core.py:68-69`), skills (`install_skills.py:102-104`). Every command a phase converts is already installed (for example `~/.claude/commands/sc/analyze.md`, 3,551 bytes, pre-phase, which round 4 found has no `Unattended mode` section). So the phase install copies only files that are new (for example `WORKER-CONTRACT.md`) and skips every edited command and skill file.
- **Effect:** identical to round-4 B1. At 7.2 step 1 (`SPEC:283`) the `~/.claude` copy still lacks the `## Unattended mode` section while the worktree copy has it, so the pre-dispatch confirmation fails; dispatched anyway, the guard refuses with "command copies disagree" (`SPEC:60`). Every 7.2 check on a converted command fails, and P1 cannot pass (`SPEC:216`). Edited skills are also not installed, and skills are read from `~/.claude/skills/` first (`CLAUDE.md:88`), so a worker would run the pre-phase skill. The master reinstall is a no-op for the same reason: the abandoned phase's command files stay in `~/.claude`.
- **Fix direction (not applied):** write both installs with `--force` (`uv run superclaude install --force` in the phase-branch checkout; the same in a master checkout), or use `superclaude update`, which forces every step (`main.py:340-378`). This keeps the approved outcome of `APPROVED.md:35` ("installs that phase into `~/.claude`"); only the command line changes. What else `--force` overwrites (for example `install_user_setup`, `main.py:236`) was not read: UNVERIFIED.

#### Minor findings (notes only)
| # | Line | Defect | Evidence | Fix direction |
|---|---|---|---|---|
| n1 | `SPEC:282` | The master reinstall is written as bare `superclaude install`, which the same sentence says installs "its own files, not the branch's"; it restores master only if the separately installed package happens to be master. | `SPEC:282`, earlier clause; `install_core.py:117-122`. Inferable: "from master" read as "in a master checkout", like the phase install. | "`uv run superclaude install --force` in a master checkout" (folds into N1's fix). |
| n2 | `SPEC:282` | "the phase branch" is not defined; the same paragraph names "the feature branch or a scratch branch" as where the phase's edits are committed. | `SPEC:282`. Inferable: the branch the disposable worktree is created from. | "from that branch". |
| n3 | `SPEC:282` | Reinstalling from master after abandoning phase N also removes the earlier passed phases from `~/.claude`, because they reach master only with the feature's one PR (L2). No check breaks: the next phase's checks start with that phase's own install. | `APPROVED.md:20` (L2), `:35` (approved wording, verbatim). | Note only; the wording is approved. |
### R4. Scope check
| Hunk (`SPEC:N`) | Traces to | In scope? |
|---|---|---|
| 216 | B1 consequence (owner approval per phase) | Yes |
| 282 | B1 | Yes (the `uv run` adaptation and its citation serve B1) |
| BASE 305 removed, 313 added | B2 | Yes |
| 358 | B2 consequence (reference update) | Yes |
| 393 | B2 (placement adaptation record, as `APPROVED.md:36` asks) | Yes |
| 414 | B1 consequence (same as 216) | Yes |

No change beyond B1, B2 and their consequential edits. The disposition's count (6 insertions, 6 deletions, `disposition-round4.md:138`) matches the diff. Citations on changed lines re-read: `install_core.py:117-122` holds; `CLAUDE.md:37` and `CAPS:115` are unchanged text on line 282 and were not re-read.
### R5. Verdict
**FAIL.** One blocking finding, N1: B2 is resolved, and B1's approved wording is applied faithfully, but the install command it names (`uv run superclaude install`, no `--force`) skips every already-installed file, so `~/.claude` stays pre-phase and the 7.2 checks still cannot dispatch a converted command. The fix is one flag on two command lines and changes no approved outcome. n1-n3 are notes only.

### R6. Self-Audit
Included on a FAIL for traceability (the task requires it only on PASS).
- Checked: all 7 diff hunks; each B1 and B2 clause against `APPROVED.md:35-36`; the installer's source resolution (live `uv run` probe) and its skip-if-exists logic for core, commands and skills; the default of `--force`; the presence of pre-phase installed files; that AC-1.8's three WC-9 conditions can all hold in P1; that no `AC-0.8` reference remains; that the "no user decision" sentences at 216 and 414 no longer contradict 282; that no hunk falls outside B1, B2 and their consequences.
- Not checked: unchanged text; minor findings m1-m11; what `--force` does to `install_user_setup` and the codegraph step (UNVERIFIED).

#### Decisions
| Decision | Options | Rationale |
|---|---|---|
| Grade of N1 | blocking; minor | Blocking: same effect and same gate as round-4 B1 (`:97-101`), which was graded blocking; the spec spells out the exact command, so an implementer following it gets the skip. |
| Report N1 though the wording is approved | report; skip as approved | Report: `APPROVED.md:35` approves the outcome ("installs that phase into `~/.claude`") and names bare `superclaude install`; the `uv run` form is the reviser's adaptation, and neither form installs edited files without `--force`. Same rule as round-4 Decisions row 4 (`:152`). |
| Grade of n1-n3 | blocking; minor | Minor: n1 is inferable and folds into N1's fix; n2 has one reading; n3 breaks no check. |

## Final recheck after fix pass 2 (Task 17)
Reviewer: independent worker (did not write the spec or either fix pass). Task `task_5963b2ccb7f4`, run 2026-11-02.
Spec: `specs/orca-worker-contract-spec.md` (SPEC). Baseline: `specs/history/spec-v6-after-fix1.md` (V6). Binding inputs: `README.md:29-38` (rules), `decisions/APPROVED.md:32-37` ("Round-4 review fixes", rows B1, B1-N1, B2). Severity model: merged PR #343 (only blocking findings fail).

### F1. Method
- Diff: `diff V6 SPEC` gives exactly one hunk, `282c282` (one line replaced by one line). Only that line was reviewed.
- N1 (`:174-178` above) and its row `APPROVED.md:36` (B1-N1) were compared clause by clause with the new `SPEC:282`; B1 (`APPROVED.md:35`) was checked to still hold on the same line.
- Installer source read for the claims on the changed line: `src/superclaude/cli/main.py:35-39` (the `--force` flag), `:178-236` (`force=force` passed to each step), `:239-241` (codegraph step, `--force` not forwarded); skip-unless-force guards in `install_commands.py:55-57`, `install_core.py:68-69`, `install_agents.py:51`, `install_skills.py:102`, `install_hooks.py:246`, `install_templates.py:71`, `install_user_setup.py:56`; `install_core.py:117-122` (source resolution); `update.sh:8`.
- Not done, per scope: no `/sc:spec-panel`, no review of unchanged lines, no recheck of minor findings (m1-m11, n1-n3).

### F2. N1 resolution
| Check | Result | Evidence |
|---|---|---|
| Phase-branch install uses `--force` | Yes: "running `superclaude install --force` from the phase branch, as `uv run superclaude install --force` inside a checkout of that branch" | `SPEC:282` |
| Master reinstall uses `--force` | Yes: "reinstalls from master (`superclaude install --force` from master)" | `SPEC:282` |
| `install_commands.py:55-57` confirms `--force` overwrites existing files | Yes. `:55` `if target_file.exists() and not force:` skips (`:56-57`) only when `force` is false; with `force` true the loop falls through to `shutil.copy2(command_file, target_file)` (`:61`), which overwrites. The same guard exists for core (`install_core.py:68`), agents (`install_agents.py:51`), skills (`install_skills.py:102`), hook scripts (`install_hooks.py:246`), templates (`install_templates.py:71`) and rules/output styles (`install_user_setup.py:56`). `superclaude install` passes the flag to every one of these steps (`main.py:178-236`). | `install_commands.py:55-61` |
| `update.sh:8` runs `superclaude install --force` | Yes, verbatim | `update.sh:8` |
| B1 still holds (approval per phase, install before live checks, master reinstall on abandon) | Yes, every clause of `APPROVED.md:35` is still on `SPEC:282`; only `--force` and the rationale sentence were added | `SPEC:282`; `APPROVED.md:35` |

**N1 is resolved.** With `--force`, the phase's edited command, skill and core files overwrite the pre-phase copies in `~/.claude`, so the 7.2 step-1 copy comparison can match and the B1 failure no longer recurs.

### F3. Diff scope
The single hunk at `SPEC:282` changes three things relative to V6: `--force` added to the phase-branch install (twice: the command and its `uv run` form), `--force` added to the master reinstall, and one new sentence giving the reason with citations (`install_commands.py:55-57`, `update.sh:8`). All three trace to `APPROVED.md:36` (B1-N1). Nothing else in the line, and no other line in the file, changed. **The diff contains nothing else.**

### F4. Changed-line findings
0 blocking, 2 minor. Minor findings are notes under PR #343 and trigger no fix.

| # | Line | Defect | Evidence | Fix direction |
|---|---|---|---|---|
| f1 | `SPEC:282` | `--force` overwrites every framework file in `~/.claude`, not only the phase's: agents, templates, hook scripts, and also `~/.claude/rules/` and `~/.claude/output-styles/`. Local edits the owner made to any of those installed files are lost at each phase install; the line does not say so. Hook data files are kept even with `--force`. | `main.py:178-236`; `install_user_setup.py:56,92-98,121-130`; `install_hooks.py:87-88` | Name the overwrite in the per-phase approval ask. Minor: the owner approves every install, `update.sh:8` does the same routinely, and no check breaks. |
| f2 | `SPEC:282` | The master reinstall with `--force` restores files master has, but deletes nothing, so files that only the abandoned phase added (for example `WORKER-CONTRACT.md`, new in P0, `SPEC:59`) stay in `~/.claude`. Not introduced by this pass: V6 had the same gap. | `install_commands.py:50-61` (copy loop only, no removal); same pattern in the other installers listed in F1 | Note only. Minor: the next phase's checks start with that phase's own `--force` install, so no 7.2 check reads a stale leftover. |

Earlier minor n1 (master reinstall written as bare `superclaude install --force`, not `uv run ... --force` in a master checkout) is unchanged by this pass and, as a minor finding, is not rechecked.

### F5. Verdict
**PASS (with notes).** N1 is fixed: both B1 install lines use `--force` (`SPEC:282`), and `install_commands.py:55-57` skips an existing file only when `force` is false, so `--force` overwrites it. The diff against V6 is that one line and nothing else, and its changed text has no blocking defect; f1 and f2 are notes only.

### F6. Self-Audit
- Checked: that the diff has exactly one hunk; every `superclaude install` occurrence on the changed line carries `--force` (three command forms); the skip-unless-force guard and the overwrite path in `install_commands.py:55-61`; that the CLI flag exists and is forwarded to every copy step (`main.py:35-39,178-236`); the same guard in all seven installers; `update.sh:8` verbatim; that the B1 clauses of `APPROVED.md:35` survive unchanged; that the new rationale sentence's two citations say what it claims; what `--force` overwrites beyond the phase files (f1) and what it does not remove (f2).
- Why no blocking defect: the only behavioural change is the flag, which the installer honours exactly as the line says, and which `APPROVED.md:36` orders verbatim; the two side effects found (f1, f2) break no check and are covered by the owner's per-phase approval.
- Not checked, per scope: unchanged lines, earlier minor findings, `/sc:spec-panel`.
