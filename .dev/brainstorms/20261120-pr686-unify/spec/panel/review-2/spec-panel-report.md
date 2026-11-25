review: 2 of 3

# Spec panel report: unification spec candidate-2 (critique, re-review, detailed, unattended)

| Field | Value |
|---|---|
| Candidate | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/candidate-2.md` (739 lines, 119,965 bytes) |
| Candidate sha256 | `fb076ecc5547122d29d71128bd24f46bcaf7ebb25967139caa38f9c2a1d3ef48` (taken with `sha256sum`; equals the frozen hash in the brief) |
| Baseline | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/candidate-1.md` (738 lines, 119,121 bytes) |
| Baseline sha256 | `6f16cdf0b2ec7bb5714a9d19fe55c6b4ea1206a3f7daf0fc748bbdd9c97b6fbc` |
| Prior report | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/review-1/spec-panel-report.md` (`review: 1 of 3`, `verdict: FAIL`), sha256 `209670b63ce20bb3d032cad04c018b51b114406cc42396b5eab838b5dde547f6` |
| Reviser net change | +844 bytes (119,121 to 119,965), 39 changed hunks (`diff -w`), 40 baseline lines and 41 candidate lines |
| Reviewer model actually used | `claude-gw-tier1b[1m]` |
| Date | 2026-11-20 |
| Mode, focus, format | critique, `--re-review`; requirements, architecture, testing, compliance, correctness; detailed |
| Report directory | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/review-2` |
| Inputs read in full | the command file `spec-panel.md`, `~/.claude/WORKER-CONTRACT.md`, `~/.claude/rules/prompts/document_review_loop_prompts.md` (RE-REVIEW prompt followed: roles, Step 1, review number, self-check), steps 1-5 of the Fix Cycle process in `~/.claude/agents/rf-qa.md`, the whole prior report, the whole diff, and every section of the candidate that the diff touches or that the F1 fix must agree with |
| Panel | one reviewer session playing the 11 experts in the fixed order. `superclaude review panel resolve`, `superclaude review merge` and the ledger step belong to the coordinator and were not run here; the findings block at the end is written for that merge. |

## Summary

Prior blocking finding F1 is resolved. No new blocking finding. Verdict PASS (scoped). 5 Medium findings (warnings) and 4 Notes, all on changed lines or on text that depends on a changed line. Medium and Note findings of review 1 were not rechecked.

| ID | Severity label | Grade | Spec section | One line |
|---|---|---|---|---|
| F1 (prior) | MAJOR | resolved | 4.1 FR-82; 4.2 FR-83; 4.5 SEC-07; 1.3; 3.1; 3.2 step 6; 5.1 L-08; 8.2 S9; 8.3; 10 OA-11; 12; Appendix A | FR-82 and its acceptance check now agree: two permitted writers, the second one has a requirement (FR-83), a grant name, a flow step, a stage and a trace row |
| G1 | MAJOR | Medium | 11 X-1; 2 OD-11; 4.5 SEC-07 | The grant list is "three" in X-1 and OD-11 and four in SEC-07 and OA-11 |
| G2 | MAJOR | Medium | 4.2 FR-83; 8.2 S9, S14 | FR-83's no-grant refusal has no stage that builds or tests it; S9 lands the verb, grants arrive at S14 |
| G3 | MAJOR | Medium | 4.1 FR-82 vs 4.5 SEC-02 | "The only code that may write" is worded repo-wide; the merge verb, the claim session and `repos grant` also write |
| G4 | MAJOR | Medium | 4.2 FR-83; 8.3 | The "new home for complete.py" branch (PR 682 stands) has no owner-action row, and FR-82's "test unchanged" cannot pass in it |
| G5 | MAJOR | Medium | reviser contract; 8.2 S15; 8 rules; 4 row form | The reviser edited 23 hunks no blocking finding names; three removals narrow stage or row text (S15a and S15b qualifiers, the combined-tree caution, the enumeration pointer) |
| N12 to N15 | MINOR | Note | various | see follow-up candidates |

## Coverage (what this review checked)

- Hashes of the candidate, the baseline and the prior report taken with `sha256sum`; the candidate hash equals the brief's. The prior report carries `review: 1 of 3`, so N is 2. Nothing was unreadable or empty.
- The whole diff (`diff -w`, 39 hunks) read, and the role-swap self-check run: all 41 AFTER lines were found exactly (`grep -Fx`) in the candidate and all 40 BEFORE lines exactly in the baseline. Roles are not swapped.
- F1 re-checked against the AFTER text in each place the brief names: FR-82, FR-83, SEC-07, 1.3 (line 61), 3.1 (line 124), 3.2 step 6 (lines 150-152), 5.1 L-08, 8.2 S9, S17, 8.3 (line 500), OA-11 (line 573), 12.2 (line 665), 12.4 (line 679), 13.1 (line 687), Appendix A (line 720), and the rows that quote the grant list (OD-11, R-4, X-1, line 450).
- Source reads, read-only, in the owner's unpushed branch `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb` (HEAD `d0a0a433b`, matches the spec): `src/superclaude/cli/issue_pipeline/complete.py` (header, outcomes, `END_STATUS`, "Status read and write are two calls" limit), `issue_pipeline/cli.py:226-255` (the `complete` verb exists and says "Run it only under the issue's grant row"), `tests/issue_watch/test_security_invariants.py:1062-1082` (`_WRITER_MODULES = {"complete.py", "repo_init.py"}`, `assert name not in writers` for `github.py` and `cycle.py`; so FR-82's parenthetical is true), `tests/issue_pipeline/test_complete.py` and `test_complete_cli.py` (exist), `src/superclaude/hooks/scripts/launch-level-guard.sh:445-455` (a bound worker's `issue-pipeline complete` is refused as TAMPER, "best effort, not a control: the grant-row rule of WORKER-CONTRACT.md is the control"), and `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` row R24 (matches FR-83: coordinator only; succeeded moves Status to `In review`; failed, blocked, partial comment only; needs "that issue's grant row"; lives in `issue_pipeline/`).
- The five owner rules re-checked against the changed text (table below). The new grant name `issue.status.move` checked against SEC-06 (refuses `pr.merge`, `issue.close`) and against the document's other uses of "standing".
- Not checked: Medium and Note findings of review 1 (not rechecked by rule); the 42 verdict files; the live GitHub state (no `gh` call was made in this review); the full planb test run.
- Method note: Guard Condition Boundary Table and State Variable Registry cover guards and variables on changed lines only (FR-83 and the changed FR-82 clause, the grant list). Pipeline Dimensional Analysis ran on the one new stage (after `worker_done`) and found no unhandled count divergence.

## Prior blocking findings (re-check)

| Prior id | Status | Evidence (AFTER text) |
|---|---|---|
| F1 | resolved | The defect was two stated texts that cannot both hold: FR-82 "only `repo_init.py` may write" against its own check (the planb two-writer scan, which requires `complete.py` to be a writer), with the second writer absent from every requirement, flow step and grant list. AFTER: FR-82 now reads "The only code that may write is `issue_watch/repo_init.py` (only `gh label create` for the trigger label, after the owner's chat OK) and the coordinator-only `issue_pipeline/complete.py` (FR-83); `github.py` and the cycle never", and its check reads "planb `test_security_invariants.py:1059-1079` unchanged (it names both writers and keeps `github.py` and `cycle.py` read-only)", which matches the planb test (verified). FR-83 gives the second writer a requirement (who, when, what it posts, which outcomes move the Status, refusal without grants, sources R24 and D04) that matches planb `complete.py` and R24. SEC-07 names `issue.status.move`, tagged `NEW (author)`; 12.4 says it is the only such tag and that the grant is refused until the owner grants it. Flow step 6 (3.2) and the 3.1 paragraph show the step and its grant. S9 lands `complete.py` and its verb with the two-writer scan in its tests column and "Status move needs OA-11". L-08, 1.3, 8.3, OA-11, 12.2, 13.1 and Appendix A carry FR-83 or the fourth name. SEC-06 (no `pr.merge`, no `issue.close`) is untouched, and `issue.status.move` is neither, so owner rule 4 holds. |

## Step 1, the evidence block

`diff -w candidate-1.md candidate-2.md`, changed lines copied verbatim: `<` lines under BEFORE (baseline), `>` lines under AFTER (candidate). Hunk headers are `<baseline lines>c<candidate lines>`. Self-check result: 41 of 41 AFTER lines found in the candidate, 40 of 40 BEFORE lines found in the baseline.

#### Hunk 37c37

BEFORE (baseline):
~~~text
Two lines of work grew in the same files. The owner's line built the issue watcher (PRs 447 and 448, the merged poller), the claim pipeline (`/sc:issue --claim`), the launch guard, the sweep (PR 539, read-only report of Orca sessions), the observer and a plan-approval package (PRs 584 and 591, Plan A and Plan B). Clay's line produced a design (PR 681, merged `docs/designs/orchestrator.md`), a deletion of the owner's plan-approval package (PR 682, merged about 66 minutes after it opened with only a bot review), a watcher rewrite (PR 686, open, 59 files), `/sc:issue --plan` (PR 690, open), `/sc:closeout` (PR 683, merged) and a work-report skill (PR 684, merged). No `ironbelly` review exists on PRs 681 to 684, 686 or 690 (FULL-REPORT sections 1 and 3).
~~~

AFTER (candidate):
~~~text
Two lines of work grew in the same files. The owner's line built the issue watcher (PRs 447 and 448, the merged poller), the claim pipeline (`/sc:issue --claim`), the launch guard, the sweep (PR 539, read-only report of Orca sessions), the observer and a plan-approval package (PRs 584 and 591). Clay's line produced a design (PR 681, merged `docs/designs/orchestrator.md`), a deletion of that plan-approval package (PR 682, merged about 66 minutes after it opened, with only a bot review), a watcher rewrite (PR 686, open, 59 files), `/sc:issue --plan` (PR 690, open), `/sc:closeout` (PR 683, merged) and a work-report skill (PR 684, merged). No `ironbelly` review exists on PRs 681 to 684, 686 or 690 (FULL-REPORT sections 1 and 3).
~~~

#### Hunk 61c61

BEFORE (baseline):
~~~text
| NOT BUILT on master | Dispatcher `run-all`, per-repo configs, `first_run`, stage-aware `brief.py`, `complete.py` (planb only, 225 uncommitted entries); wake files, ack, `max_in_flight`, plan-check skip, label writer (pr-a only; `wake.py:46-47` still says `orchestrator-wake/1`); `/sc:issue --plan` (pr-p `skills/sc-issue-protocol/scripts/plan_body.py:138`) | planb, pr-a and pr-p reads |
~~~

AFTER (candidate):
~~~text
| NOT BUILT on master | Dispatcher `run-all`, per-repo configs, `first_run`, stage-aware `brief.py`, `complete.py` (coordinator-only result comment and Status move, FR-82, FR-83) (planb only, 225 uncommitted entries); wake files, ack, `max_in_flight`, plan-check skip, label writer (pr-a only; `wake.py:46-47` still says `orchestrator-wake/1`); `/sc:issue --plan` (pr-p `skills/sc-issue-protocol/scripts/plan_body.py:138`) | planb, pr-a and pr-p reads |
~~~

#### Hunk 65c65

BEFORE (baseline):
~~~text
In one line: nothing of the unified flow has run live. The watcher is complete but off; the coordinator is design text; the guard has never bound a coordinator-started worker.
~~~

AFTER (candidate):
~~~text
Nothing of the unified flow has run live: the watcher is complete but off, the coordinator is design text, the guard has never bound a coordinator-started worker.
~~~

#### Hunk 69c69

BEFORE (baseline):
~~~text
Issues 687 and 689 are issues, not PRs; nothing is built for either. Issue 651 (Clay's request for plan sections) is closed by PR 661. PR 693 (owner's PR saving the claim launch result file; issue 691) appeared after the inventory and edits four of PR 690's files. The branches `clayphi/issue-655-pr-p`, `-pr-c`, `-pr-d` and `-spec-pr` have PRs (690, 684, 682, 681); only `clayphi/v61-part-b-map` has none. PR B (the unbuilt coordinator skill) and PR E (the unbuilt runbook rewrite) have no PR or branch.
~~~

AFTER (candidate):
~~~text
Issues 687 and 689 are issues, not PRs; nothing is built for either. Issue 651 (Clay's request for plan sections) is closed by PR 661. PR 693 (owner's PR saving the claim launch result file; issue 691) came after the inventory and edits four of PR 690's files. Branches `clayphi/issue-655-pr-p`, `-pr-c`, `-pr-d` and `-spec-pr` have PRs (690, 684, 682, 681); only `clayphi/v61-part-b-map` has none. PR B (coordinator skill) and PR E (runbook rewrite) are unbuilt.
~~~

#### Hunk 73c73

BEFORE (baseline):
~~~text
One row per entry of `<W>/DECISIONS.md` (42 entries: D01-D16, Q01-Q03, OD-1 to OD-13 and the ten sub-answers OA-13a to OA-28b of the later debates OAG1 to OAG3). `debates/OA-TRIAGE.md` classed 20 of the 34 owner actions as settled by verdicts, 9 as owner-only (section 10.6) and 5 as debated. Source verdict files are `<W>/debates/<ID>/VERDICT.md`. Winner: OURS (owner's line), CLAY or HYBRID. Confidence is the verdict's own; (p) = partial, with open HIGH findings kept as conditions (section 12). OD answers come from QG1 (OD-1, 2, 13), QG2 (3-5), QG3 (6, 10-12), QG4 (7-9). All are recommendations until the owner rules in chat. Numbers: PR 682 (Clay's merged deletion of the owner's plan-approval package); PR 686 (Clay's open watcher rewrite); PR 690 (Clay's open `/sc:issue --plan` PR); PR 661 (merged plan sections in templates); PR 670 (merged daily PR log); issues 687 (Clay's cleanup request), 689 (Clay's create-time design request).
~~~

AFTER (candidate):
~~~text
One row per entry of `<W>/DECISIONS.md` (42 entries: D01-D16, Q01-Q03, OD-1 to OD-13 and the ten sub-answers OA-13a to OA-28b of the later debates OAG1 to OAG3). `debates/OA-TRIAGE.md` classed 20 of the 34 owner actions as settled by verdicts, 9 as owner-only (section 10.6) and 5 as debated. Winner: OURS (owner's line), CLAY or HYBRID. Confidence is the verdict's own; (p) = partial, with open HIGH findings kept as conditions (section 12). OD answers come from QG1 (OD-1, 2, 13), QG2 (3-5), QG3 (6, 10-12), QG4 (7-9). All are recommendations until the owner rules in chat. Numbers: PR 682 (Clay's merged deletion of the owner's plan-approval package); PR 686 (Clay's open watcher rewrite); PR 690 (Clay's open `/sc:issue --plan` PR); PR 661 (merged plan sections in templates); PR 670 (merged daily PR log); issues 687 (Clay's cleanup request), 689 (Clay's create-time design request).
~~~

#### Hunk 124c124

BEFORE (baseline):
~~~text
One flow runs per project. A cron entry (installed by the Coder image, Coder issue 515: the owner's issue for cron at boot) starts one dispatcher every five minutes, which runs one read-only poll per project. When an issue is open, assigned only to the watcher login, approved by a person (field `Approved`, unedited since), in an allowed Project Status, with its plan sections filled and no `hold:backlog`, the poll starts a claim session as master already does: `/sc:issue --claim <N> --pipeline none` (master `cli/issue_watch/launch.py:33`). When the claim marker appears, the poll saves claim evidence and a delivery intent in one store save and writes an ids-only wake file. The project's coordinator (`COORD-<RepoName>` in the `Coordinator` worktree, Coder issue 516: the owner's issue for that worktree and session) pulls the wake, saves its own record, then acknowledges. It starts one supervised worker bound to guard level W, releases it to WA after the person's recorded plan approval (route A), and commits the work itself. A person's typed go precedes every push and merge. Then closeout and a dry-run cleanup list run. The sweep stays the one source of session facts, the observer shows it, the work report gives plain-English progress. The system is local and at-least-once: a wake may arrive twice, and handling one round twice must have no second effect.
~~~

AFTER (candidate):
~~~text
One flow runs per project. A cron entry (installed by the Coder image, Coder issue 515: the owner's issue for cron at boot) starts one dispatcher every five minutes, which runs one read-only poll per project. When an issue is open, assigned only to the watcher login, approved by a person (field `Approved`, unedited since), in an allowed Project Status, with its plan sections filled and no `hold:backlog`, the poll starts a claim session as master already does: `/sc:issue --claim <N> --pipeline none` (master `cli/issue_watch/launch.py:33`). When the claim marker appears, the poll saves claim evidence and a delivery intent in one store save and writes an ids-only wake file. The project's coordinator (`COORD-<RepoName>` in the `Coordinator` worktree, Coder issue 516: the owner's issue for that worktree and session) pulls the wake, saves its own record, then acknowledges. It starts one supervised worker bound to guard level W, releases it to WA after the person's recorded plan approval (route A), and commits the work itself; on success it also posts the result comment and moves the Status to In review (FR-83). A person's typed go precedes every push and merge. Then closeout and a dry-run cleanup list run. The sweep stays the one source of session facts, the observer shows it, the work report gives plain-English progress. Delivery is at-least-once: a wake may arrive twice, and handling a round twice must have no second effect.
~~~

#### Hunk 150c150,152

BEFORE (baseline):
~~~text
  6 WA worker edits and tests, worker_done (no commit, push or PR command)
~~~

AFTER (candidate):
~~~text
  6 WA worker edits and tests, worker_done (no commit, push or PR command);
    on succeeded the coordinator runs `issue-pipeline complete`: result comment,
    Status to In review (failed, blocked, partial: comment only), under grants [P]
~~~

#### Hunk 181,182c183

BEFORE (baseline):
~~~text
Row form: ID, the "shall" sentence, acceptance check (a command, test or observable; NEW = to be written; a path = exists in the snapshot named, under `tests/`), source (verdict id; `BS` = merged brainstorm design only, see 12.4). Long enumerations stay in the verdict item cited. The component is named under each subsection heading. Numbers: PR 686 (Clay's open watcher rewrite, pr-a); PR 682 (Clay's merged plan-approval deletion); PR 690 (Clay's `/sc:issue --plan` PR); PR 661 (merged plan sections in templates); PR 693 (owner's claim-launch-result PR); issue 442 (live guard observations); issues 687, 689 (Clay's cleanup and create-time design requests); Coder issues 515, 516 (cron at boot; `Coordinator` worktree and session); R18, R33 (owner's zero-setup rows: default-on config; `GOVERNED_LEVELS_ALLOWED = False`). The coordinator, merge gate and dashboard items are not built (1.3).

~~~

AFTER (candidate):
~~~text
Row form: ID, the "shall" sentence, acceptance check (a command, test or observable; NEW = to be written; a path = exists in the snapshot named, under `tests/`), source (verdict id; `BS` = merged brainstorm design only, see 12.4). The component is named under each subsection heading. Numbers: PR 686 (Clay's open watcher rewrite, pr-a); PR 682 (Clay's merged plan-approval deletion); PR 690 (Clay's `/sc:issue --plan` PR); PR 661 (merged plan sections in templates); PR 693 (owner's claim-launch-result PR); issue 442 (live guard observations); issues 687, 689 (Clay's cleanup and create-time design requests); Coder issues 515, 516 (cron at boot; `Coordinator` worktree and session); R18, R24, R33 (owner's zero-setup rows: default-on config; completion comment and Status move; `GOVERNED_LEVELS_ALLOWED = False`).
~~~

#### Hunk 216c217

BEFORE (baseline):
~~~text
| FR-82 | Keep NG-2 as "the poll cycle writes nothing to GitHub"; only `repo_init.py` may write, only `gh label create` for the trigger label, only after the owner's chat OK; while `auto_enable` is false the label step reads only and reports `would_create` (design proposal, UNVERIFIED); the go that turns `auto_enable` on covers later repos' trigger label; `hold:backlog` stays by hand. | planb `test_security_invariants.py:1059-1079` unchanged; NEW | OAG3, D09 |
~~~

AFTER (candidate):
~~~text
| FR-82 | Keep NG-2 as "the poll cycle writes nothing to GitHub". The only code that may write is `issue_watch/repo_init.py` (only `gh label create` for the trigger label, after the owner's chat OK) and the coordinator-only `issue_pipeline/complete.py` (FR-83); `github.py` and the cycle never. While `auto_enable` is false the label step reads only and reports `would_create` (design proposal, UNVERIFIED); the go that turns `auto_enable` on covers later repos' trigger label; `hold:backlog` stays by hand. | planb `test_security_invariants.py:1059-1079` unchanged (it names both writers and keeps `github.py` and `cycle.py` read-only); NEW | OAG3, D09, R24 |
~~~

#### Hunk 220c221

BEFORE (baseline):
~~~text
Component: coordinator; exceptions FR-31 (and guard), FR-33, FR-35 (and watcher), FR-39 (cleanup script).
~~~

AFTER (candidate):
~~~text
Component: coordinator; exceptions FR-31 (and guard), FR-33, FR-35 (and watcher), FR-39 (cleanup script), FR-83 (`issue_pipeline`).
~~~

#### Hunk 240a242

AFTER (candidate):
~~~text
| FR-83 | Let only the coordinator run `superclaude issue-pipeline complete` (planb `issue_pipeline/complete.py`), after it reads a succeeded `worker_done` or a launched agent's `result.md`: post one result comment (per-run marker; outcome word, validated paths, PR number only) and, for succeeded only, move the Project Status to `In review`, only when the current Status is allowed (else `status_moved_by_person`). Failed, blocked or partial: comment only. No worker or launched agent calls it. Without the issue's grants `issue.comment` and `issue.status.move` (SEC-07) it refuses before any `gh` call. | planb `tests/issue_pipeline/test_complete.py`, `test_complete_cli.py`; the two-writer scan of FR-82; NEW: no grant, no `gh` call | R24 (owner), D04; grant name NEW (author) |
~~~

#### Hunk 292c294

BEFORE (baseline):
~~~text
| SEC-07 | Start with empty `grants`; the owner grants at most `issue.assign`, `issue.comment`, `issue.body.append_plan_sections` once in chat, recorded by an agent with `repos grant`; missing or malformed means none; log each use naming its go. | NEW: one `E-NO-GRANT` case per entry | QG3, Q01, Q03 |
~~~

AFTER (candidate):
~~~text
| SEC-07 | Start with empty `grants`; the owner grants at most `issue.assign`, `issue.comment`, `issue.body.append_plan_sections` and `issue.status.move` (for FR-83; NEW (author)) once in chat, recorded by an agent with `repos grant`; missing or malformed means none; log each use naming its go. | NEW: one `E-NO-GRANT` case per entry | QG3, Q01, Q03 |
~~~

#### Hunk 349c351

BEFORE (baseline):
~~~text
| L-01 | Interim ledger of owner answers: one file in the unification work's task package under `.dev/tasks/` (name UNVERIFIED); `git add .dev/tasks`; the recorder commits it when the owner says. | SEC-14 | H0 |
~~~

AFTER (candidate):
~~~text
| L-01 | Interim ledger of owner answers: one file in the unification work's task package under `.dev/tasks/`; `git add .dev/tasks`; the recorder commits it when the owner says. | SEC-14 | H0 |
~~~

#### Hunk 356c358

BEFORE (baseline):
~~~text
| L-08 | Planb (5.2) carries: skips `held_incomplete`, `held_backlog`; MR-1, MR-2 tests; absolute child paths; `auto_enable` false; loader support for its keys; corrected requirements line 18 and Coder 515 text. | FR-02, FR-03, FR-05, FR-12, FR-23, FR-82, NFR-01, FR-69 | L2 (S9) |
~~~

AFTER (candidate):
~~~text
| L-08 | Planb (5.2) carries: skips `held_incomplete`, `held_backlog`; MR-1, MR-2 tests; absolute child paths; `auto_enable` false; loader support for its keys; corrected requirements line 18 and Coder 515 text. | FR-02, FR-03, FR-05, FR-12, FR-23, FR-82, FR-83, NFR-01, FR-69 | L2 (S9) |
~~~

#### Hunk 365c367

BEFORE (baseline):
~~~text
Read by the author on 2026-11-20: worktree `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`, branch `ironbelly/issue-watcher-zero-setup-plan`, HEAD `d0a0a433b` ("zero-setup requirements R1-R34 and plan v5"), based on master `e3e9d636a`, no upstream, not pushed; 225 `git status` entries (D14 counted 348; the figure moves). It edits `issue_watch/{audit,cli,cycle,github,launch,predicates}.py`, `issue_pipeline/{brief,cli,reads}.py` (deleted by PR 682), `core/WORKER-CONTRACT.md` and `hooks/scripts/launch-level-guard.sh`, and overlaps PR 686 on 23 files (7 source). Requirements: `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (121 lines, R1 to R36).
~~~

AFTER (candidate):
~~~text
Read by the author on 2026-11-20: worktree `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`, branch `ironbelly/issue-watcher-zero-setup-plan`, HEAD `d0a0a433b` ("zero-setup requirements R1-R34 and plan v5"), based on master `e3e9d636a`, no upstream, not pushed; 225 `git status` entries. It edits `issue_watch/{audit,cli,cycle,github,launch,predicates}.py`, `issue_pipeline/{brief,cli,reads}.py` (deleted by PR 682), `core/WORKER-CONTRACT.md` and `hooks/scripts/launch-level-guard.sh`, and overlaps PR 686 on 23 files (7 source). Requirements: `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (121 lines, R1 to R36).
~~~

#### Hunk 367c369

BEFORE (baseline):
~~~text
**The state of its `/sc:implement` run is UNCLEAR and must be re-checked before the revert sequence starts.** The ledger `.dev/tasks/done/TASK-WF-requirements-20261119-143917-2/progress.md` ends `T28: complete`, `FINAL: pass`, `ARCHIVE: start`, and the inventory calls the run finished; D14 and D15 say not to resume its "half-finished" ledger across the rebase. Nobody ran its tests. Re-check, read-only, by a session the owner names: `git -C <planb> status --short | wc -l`; whether the ledger folder is complete; `uv run pytest tests/issue_watch` in planb; then the owner states in chat which is true (X-12).
~~~

AFTER (candidate):
~~~text
**The state of its `/sc:implement` run is UNCLEAR and must be re-checked before the revert sequence starts.** The ledger `.dev/tasks/done/TASK-WF-requirements-20261119-143917-2/progress.md` ends `T28: complete`, `FINAL: pass`, `ARCHIVE: start`, and the inventory calls the run finished; D14 and D15 say not to resume its "half-finished" ledger across the rebase. Re-check, read-only, by a session the owner names: `git -C <planb> status --short | wc -l`; whether the ledger folder is complete; `uv run pytest tests/issue_watch` in planb; then the owner states in chat which is true (X-12).
~~~

#### Hunk 373c375

BEFORE (baseline):
~~~text
**None of these actions is executed by this spec's author, and none may be executed without the owner's go in chat for that named action** (recorded by an agent, SEC-14). Words: KEEP, KEEP-ADAPT, REVERT (one new PR), CLOSE, DRAFT (set to Draft and hold). Every `gh` call names `--repo IronbellyOrg/IronClaude`; PRs open only through `/sc:pr-submit --monitor 3`; a returned URL must read `github.com/IronbellyOrg/IronClaude/pull/N`; nothing touches `SuperClaude-Org/SuperClaude_Framework`. "Clay" is the account `clayphi`. Order words: H0, lane 1, lane 2, lane 3 (D14).
~~~

AFTER (candidate):
~~~text
**None of these actions is executed by this spec's author, and none may be executed without the owner's go in chat for that named action** (recorded by an agent, SEC-14). Words: KEEP, KEEP-ADAPT, REVERT (one new PR), CLOSE, DRAFT (set to Draft and hold). Every `gh` call names `--repo IronbellyOrg/IronClaude`; PRs open only through `/sc:pr-submit --monitor 3`; a returned URL must read `github.com/IronbellyOrg/IronClaude/pull/N`; nothing touches `SuperClaude-Org/SuperClaude_Framework`. "Clay" is the account `clayphi`. Order: H0, lanes 1-3 (D14).
~~~

#### Hunk 406,407c408,409

BEFORE (baseline):
~~~text
| 620 (removes `/sc:save`, `/sc:load`), 622 (removes `/sc:build`), 627 (removes `/sc:improve`), 629 (removes cli-portify), 631 (removes `/sc:index`, `/sc:index-repo`), 632 (removes roadmap, tasklist, sprint family; edits `sc-issue-protocol/refs/chains.md`), 650 (removes prd, tdd, tech-research and other skills), 656 (removes task, task-builder, roadmap skills and level 4 of `HOW-WE-WORK.md`) | KEEP, not reverted (D14) | no recorded owner approval of waves 2-6 found (UNVERIFIED, comments read in part); already released in 6.0.0 and 6.1.0; the one question to the owner (OA-21) blocks only a host install (FR-66) |
| 625 (launcher alias fixes), 626 (help text fixes), 633 (installer retire step; the hazard of FR-66), 634 (6.0.0 notes), 639 (merge of master into integration), 640 (release 6.0.0), 646 (installer `filecmp` fix), 649 (post-release sync 6.0.0), 653 (re-points task-file routes to `/sc:workflow` then `/sc:implement`; consistent with the owner's PR 613, which stops recommending `/sc:task`), 657 (6.1.0 notes), 659 (docs: cleanupPeriodDays 90), 667 (post-release docs 6.1.0, on `integration` only) | KEEP | independent of the watcher area |
~~~

AFTER (candidate):
~~~text
| 620 (removes `/sc:save`, `/sc:load`), 622 (removes `/sc:build`), 627 (removes `/sc:improve`), 629 (removes cli-portify), 631 (removes `/sc:index`, `/sc:index-repo`), 632 (removes roadmap, tasklist, sprint family; edits `sc-issue-protocol/refs/chains.md`), 650 (removes prd, tdd, tech-research and other skills), 656 (removes task, task-builder, roadmap skills and level 4 of `HOW-WE-WORK.md`) | KEEP, not reverted (D14) | no recorded owner approval of waves 2-6 (UNVERIFIED, comments read in part); released in 6.0.0 and 6.1.0; OA-21 blocks only a host install (FR-66) |
| 625 (launcher alias fixes), 626 (help text fixes), 633 (installer retire step; the hazard of FR-66), 634 (6.0.0 notes), 639 (merge of master into integration), 640 (release 6.0.0), 646 (installer `filecmp` fix), 649 (post-release sync 6.0.0), 653 (re-points task-file routes to `/sc:workflow` then `/sc:implement`, as the owner's PR 613 does), 657 (6.1.0 notes), 659 (docs: cleanupPeriodDays 90), 667 (post-release docs 6.1.0, on `integration` only) | KEEP | independent of the watcher area |
~~~

#### Hunk 465c467

BEFORE (baseline):
~~~text
Rules for every stage: one reviewable PR, one local action or one consented host operation; a stage never enables a later one; no stage schedules `run-all` or installs cron before S17 (only `run-all --dry-run` runs earlier); `auto_enable` stays false; the `DISABLED` kill file works throughout; every stage reverts by reverting its PR. "Owner gate" is the owner's go for that named action, recorded by an agent (SEC-14); a typed go precedes every push and merge. Run suites with `uv run`; run `make sync-dev`; never stage `.claude/`. A green PR 686 alone does not prove the combined tree. Source: merged design section 5, order fixed by D14 and D15. Numbers: PR 693 (owner's claim-launch-result PR), PR 690 (Clay's `/sc:issue --plan` PR), PR 685 (owner's issue 442 runbook PR), PR 682 (Clay's merged deletion), PR 686 (Clay's watcher rewrite), issue 442 (live guard observations), Coder issues 515 and 516 (cron at boot; `Coordinator` worktree and session).
~~~

AFTER (candidate):
~~~text
Rules for every stage: one reviewable PR, one local action or one consented host operation; a stage never enables a later one; no stage schedules `run-all` or installs cron before S17 (only `run-all --dry-run` runs earlier); `auto_enable` stays false; the `DISABLED` kill file works throughout; every stage reverts by reverting its PR. "Owner gate" is the owner's go for that named action, recorded by an agent (SEC-14); a typed go precedes every push and merge. Run suites with `uv run`; run `make sync-dev`; never stage `.claude/`. Order: merged design section 5, D14, D15. Numbers: PR 693 (owner's claim-launch-result PR), PR 690 (Clay's `/sc:issue --plan` PR), PR 685 (owner's issue 442 runbook PR), PR 682 (Clay's merged deletion), PR 686 (Clay's watcher rewrite), issue 442 (live guard observations), Coder issues 515 and 516 (cron at boot; `Coordinator` worktree and session).
~~~

#### Hunk 484c486

BEFORE (baseline):
~~~text
| S9 land planb | L-08, 5.2 | S7, S8; OA-4 | planb `test_dispatch.py`, `test_cycle.py`; MC-1 to MC-5, MC-7 to MC-9, MC-12; NEW `test_first_run_keeps_config_off_while_auto_enable_false`, `test_dry_run_generates_nothing`; no governed level launches while R33 is false | revert and restore old config files; master returns to the single-config poll, off | go to commit, to push as a draft, to merge | L2 |
~~~

AFTER (candidate):
~~~text
| S9 land planb (with `complete.py` and its verb, FR-83) | L-08, 5.2 | S7, S8; OA-4; Status move needs OA-11 | planb `test_dispatch.py`, `test_cycle.py`, `test_complete*.py`, two-writer scan `test_security_invariants.py:1059-1079`; MC-1 to MC-5, MC-7 to MC-9, MC-12; NEW `test_first_run_keeps_config_off_while_auto_enable_false`, `test_dry_run_generates_nothing`; no governed level launches while R33 is false | revert and restore old config files; master returns to the single-config poll, off | go to commit, to push as a draft, to merge | L2 |
~~~

#### Hunk 490c492

BEFORE (baseline):
~~~text
| S15 transport, cap, restart, audit, hand-back, `report-entry`, cleanup `list` (four PRs: S15a wake-check and wake-ack with kill-and-restart tests at every persistence boundary; S15b cap with single writers; S15c AU1-AU8, handback, `report-entry`, `escalate`; S15d cleanup `list`) | FR-28 to FR-40, FR-48 | S14; OA-14, OA-15, OA-16, OA-18, OA-25; Coder 516 for restart | tests in 4.2; `orca worktree rm` behaviour proved first (S15d) | revert per PR | go per PR | O6 |
~~~

AFTER (candidate):
~~~text
| S15 transport, cap, restart, audit, hand-back, `report-entry`, cleanup `list` (four PRs: S15a wake-check and wake-ack with kill-and-restart tests; S15b cap; S15c AU1-AU8, handback, `report-entry`, `escalate`; S15d cleanup `list`) | FR-28 to FR-40, FR-48 | S14; OA-14, OA-15, OA-16, OA-18, OA-25; Coder 516 for restart | tests in 4.2; `orca worktree rm` behaviour proved first (S15d) | revert per PR | go per PR | O6 |
~~~

#### Hunk 498c500

BEFORE (baseline):
~~~text
PR 682 stands under D03's three conditions. S6 and S7 are dropped; S8 shrinks to lines 57, 70, 245 plus D05's marker line in a new handoff template; S9 rebases planb onto a tree without `issue_pipeline` (untested path); workers are bound at F; the plan-approval step and route A leave FR-31. Confidence in the disposition set falls to about 50 percent (D14).
~~~

AFTER (candidate):
~~~text
PR 682 stands under D03's three conditions. S6 and S7 are dropped; S8 shrinks to lines 57, 70, 245 plus D05's marker line in a new handoff template; S9 rebases planb onto a tree without `issue_pipeline` (untested path) and the owner names a new home for `complete.py` (FR-83); workers are bound at F; the plan-approval step and route A leave FR-31. Confidence in the disposition set falls to about 50 percent (D14).
~~~

#### Hunk 517c519

BEFORE (baseline):
~~~text
Order: 1, 2, then 3 and 4 in parallel; 5 after 4 merges; 6 after 5; 7 after 6 passes and 3 is merged and accepted by Clay; 8 in parallel; 9 fourteen days after 5. Admin-only list: create the ruleset or branch protection on `master`; add `integration`; require code-owner review; set the approvals count; dismiss stale approvals; block force push and deletion; set the bypass list; make any CI check required (including `.github/workflows/boundary-guard.yml`). Organisation rulesets could not be read (token lacks `admin:org`): UNVERIFIED.
~~~

AFTER (candidate):
~~~text
Order: 1, 2, then 3 and 4 in parallel; 5 after 4 merges; 6 after 5; 7 after 6 passes and 3 is merged and accepted by Clay; 8 in parallel; 9 fourteen days after 5. Admin-only list: create the ruleset or branch protection on `master`; add `integration`; require code-owner review; set the approvals count; dismiss stale approvals; block force push and deletion; set the bypass list; make any CI check required (including `.github/workflows/boundary-guard.yml`). Organisation rulesets: UNVERIFIED (token lacks `admin:org`).
~~~

#### Hunk 520c522

BEFORE (baseline):
~~~text
Lightest version that would have prevented the incident: ranks 1, 3, 4, 5, 6, 7, 9 limited to `docs/designs/`, `WORKER-CONTRACT.md` and the CODEOWNERS file, about 120-150 minutes of session, maintainer and chat time plus 15-30 minutes of admin time (arithmetic over the estimates). Words alone would not have prevented it: PR 681's body said "the owner reviews and merges" and its author merged it about 90 minutes after opening. The claim is "probably, UNVERIFIED" until the throwaway test passes.
~~~

AFTER (candidate):
~~~text
Lightest version that would probably have prevented the incident (UNVERIFIED until the throwaway test passes): ranks 1, 3, 4, 5, 6, 7, 9 limited to `docs/designs/`, `WORKER-CONTRACT.md` and CODEOWNERS, about 120-150 minutes plus 15-30 minutes of admin time. Words alone would not: PR 681 said "the owner reviews and merges"; its author merged it about 90 minutes after opening.
~~~

#### Hunk 524c526

BEFORE (baseline):
~~~text
De-duplicated from `<W>/DECISIONS.md` ("Actions only the owner can take") and merged design section 7 (OA-1 to OA-34; OD-n are D15's open questions, folded in). "Chat" means the owner says it in chat and an agent records it; the owner writes no file. Until the owner answers, nothing that depends on the answer is switched on; silence is never a yes. The other answers and what each does are in merged design section 7. Numbers: PRs 686, 690 (Clay's open PRs), PR 693 (owner's), issues 450 and 655, issue 687 (Clay's cleanup request), Coder issues 515, 516, 477 (cron at boot; `Coordinator` worktree and session; listener), issue 442 (live guard observations).
~~~

AFTER (candidate):
~~~text
De-duplicated from `<W>/DECISIONS.md` ("Actions only the owner can take") and merged design section 7 (OA-1 to OA-34; OD-n are D15's open questions, folded in). "Chat" means the owner says it in chat and an agent records it; the owner writes no file. Until the owner answers, nothing that depends on the answer is switched on; silence is never a yes. Numbers: PRs 686, 690 (Clay's open PRs), PR 693 (owner's), issues 450 and 655, issue 687 (Clay's cleanup request), Coder issues 515, 516, 477 (cron at boot; `Coordinator` worktree and session; listener), issue 442 (live guard observations).
~~~

#### Hunk 571c573

BEFORE (baseline):
~~~text
| OA-11 | grant any of the three standing writes | empty `grants`; the refusal names the missing entry and the sentence to say; the agent records the owner's words |
~~~

AFTER (candidate):
~~~text
| OA-11 | grant any of the standing writes (three of QG3 plus `issue.status.move`, SEC-07) | empty `grants`; the refusal names the missing entry and the sentence to say; the agent records the owner's words |
~~~

#### Hunk 606c608

BEFORE (baseline):
~~~text
| X-14 | D06 item 1: a merge go "expires" (number an owner decision); Q01 item 5: it ends only on the action, a head move or a revoke | OAG1: Q01 is the default, no clock in the first build; D06's number stays the owner's open option; merge automation needs an age check before it is built | the head pin, the second gate run and WC:241 already cover a stale go; no source gives a number (SEC-01) |
~~~

AFTER (candidate):
~~~text
| X-14 | D06 item 1: a merge go "expires" (number an owner decision); Q01 item 5: it ends only on the action, a head move or a revoke | OAG1: Q01, no clock in the first build; D06's number stays the owner's option; merge automation needs an age check first | the head pin, the second gate run and WC:241 cover a stale go; no source gives a number (SEC-01) |
~~~

#### Hunk 608c610

BEFORE (baseline):
~~~text
| X-16 | Merged K9: a waiting go counts toward `max_in_flight`; QG1 OD-13: a hand-back waiting for re-approval does not | OAG1: both stand | a waiting merge go has a worker finished and a PR open, so it counts and never expires; a `waiting_reapproval` hand-back has neither, so it does not count and may expire on an owner-set limit (FR-35, SEC-21) |
~~~

AFTER (candidate):
~~~text
| X-16 | Merged K9: a waiting go counts toward `max_in_flight`; QG1 OD-13: a hand-back waiting for re-approval does not | OAG1: both stand | a waiting merge go has a finished worker and an open PR: it counts, never expires; a `waiting_reapproval` hand-back has neither: it does not count and may expire on an owner-set limit (FR-35, SEC-21) |
~~~

#### Hunk 611c613

BEFORE (baseline):
~~~text
| X-19 | OA-TRIAGE: OA-1 (both gates stay, PR 682 reverted) is SETTLED; D01 does not decide PR 682, D14 makes the revert depend on the owner saying in chat that BOTH gates stay | D14: the owner's chat answer is still needed | an owner rule (approvals in chat) outranks a triage label; the spec writes to "both gates stay" as its plan and does not open the revert PR without that answer (FR-72, OA-1) |
~~~

AFTER (candidate):
~~~text
| X-19 | OA-TRIAGE: OA-1 (both gates stay, PR 682 reverted) is SETTLED; D01 does not decide PR 682, D14 makes the revert depend on the owner saying in chat that BOTH gates stay | D14: the owner's chat answer is still needed | an owner rule (approvals in chat) outranks a triage label; the plan assumes "both gates stay" but opens no revert PR without that answer (FR-72, OA-1) |
~~~

#### Hunk 632c634

BEFORE (baseline):
~~~text
Every mitigation narrows a risk. Numbers: PR 682 (Clay's merged deletion of the plan-approval package), PR 686 (Clay's open watcher rewrite), PR 690 (Clay's `/sc:issue --plan` PR), PR 693 (owner's claim-launch-result PR), Coder issues 515 and 516 (cron at boot; `Coordinator` worktree and session).
~~~

AFTER (candidate):
~~~text
Mitigations narrow, never close. Numbers: PR 682 (Clay's merged deletion of the plan-approval package), PR 686 (Clay's open watcher rewrite), PR 690 (Clay's `/sc:issue --plan` PR), PR 693 (owner's claim-launch-result PR), Coder issues 515 and 516 (cron at boot; `Coordinator` worktree and session).
~~~

#### Hunk 649c651

BEFORE (baseline):
~~~text
HIGH findings left open by the standard-depth debates (no third round) are carried as conditions: D05's seven and D06's seven as RK-1, RK-2, SEC-01 to SEC-04, SEC-08, SEC-09, SEC-13, SEC-18; D15's C-INV-1 to C-INV-4 as FR-33, FR-35, SEC-10, SEC-12; D14's four as MC-1 to MC-6 and FR-72; D01 MR-1, MR-2 as FR-02, FR-03; D10 M1, M2 as FR-15, FR-16; D16's four as FR-75 to FR-77. The merged design's 27 invariant findings are mapped in merged 8.3.
~~~

AFTER (candidate):
~~~text
HIGH findings left open by the standard-depth debates are carried as conditions: D05's and D06's seven each as RK-1, RK-2, SEC-01 to SEC-04, SEC-08, SEC-09, SEC-13, SEC-18; D15's C-INV-1 to C-INV-4 as FR-33, FR-35, SEC-10, SEC-12; D14's four as MC-1 to MC-6 and FR-72; D01 MR-1, MR-2 as FR-02, FR-03; D10 M1, M2 as FR-15, FR-16; D16's four as FR-75 to FR-77. The merged design's 27 invariant findings are mapped in merged 8.3.
~~~

#### Hunk 663c665

BEFORE (baseline):
~~~text
| `merge-gate`, `answer-check`, `E-NO-GRANT` exist nowhere (searched `src/` of three exports) | SEC-01 to SEC-09 | `grep -rn` on the live repository before S14 |
~~~

AFTER (candidate):
~~~text
| `merge-gate`, `answer-check`, `E-NO-GRANT` exist nowhere (searched `src/` of three exports); whether `E-NO-GRANT` covers `issue.comment` for the R24 result comment (D04) | SEC-01 to SEC-09, FR-83 | `grep -rn` on the live repository before S14 |
~~~

#### Hunk 677c679

BEFORE (baseline):
~~~text
`NEW (author)`: no FR, NFR or SEC row carries that tag; each traces to a verdict, the merged design or the project's `CLAUDE.md`. Acceptance tests marked NEW are the author's proposals. Rows resting on the merged design alone (tag `BS`; the owner should confirm them when ruling): FR-03, FR-10 to FR-12, FR-19, FR-21 to FR-23, NFR-01 to NFR-04, FR-27, FR-29 to FR-35, FR-44, FR-54, FR-67, FR-70, SEC-13, SEC-14, SEC-17.
~~~

AFTER (candidate):
~~~text
`NEW (author)`: only the grant name `issue.status.move` (SEC-07, FR-83): R24 requires a grant, no verdict names one; refused until the owner grants it. Every other row traces to a verdict, the merged design, R24 or the project's `CLAUDE.md`. Acceptance tests marked NEW are the author's proposals. Rows resting on the merged design alone (tag `BS`; the owner should confirm them when ruling): FR-03, FR-10 to FR-12, FR-19, FR-21 to FR-23, NFR-01 to NFR-04, FR-27, FR-29 to FR-35, FR-44, FR-54, FR-67, FR-70, SEC-13, SEC-14, SEC-17.
~~~

#### Hunk 681c683

BEFORE (baseline):
~~~text
Each stage is shown to work by the "deliverables and tests" column of section 8.2, with MC-1 to MC-12 as the common gate. A test marked NEW is an acceptance requirement, not a passing test; none was run by this spec's author. Paths are under `tests/` of the snapshot named. Numbers: PR 686 (Clay's open watcher rewrite, pr-a), PR 690 (Clay's `/sc:issue --plan` PR), PR 682 (Clay's merged deletion), issue 442 (live guard observations), Coder issues 515, 516 (cron at boot; `Coordinator` worktree and session).
~~~

AFTER (candidate):
~~~text
Each stage is shown to work by the "deliverables and tests" column of section 8.2, with MC-1 to MC-12 as the common gate. A test marked NEW is an acceptance requirement, not a passing test; none was run by this spec's author. Paths are under `tests/`. Numbers: PR 686 (Clay's open watcher rewrite, pr-a), PR 690 (Clay's `/sc:issue --plan` PR), PR 682 (Clay's merged deletion), issue 442 (live guard observations), Coder issues 515, 516 (cron at boot; `Coordinator` worktree and session).
~~~

#### Hunk 685c687

BEFORE (baseline):
~~~text
Under `tests/` of the snapshot named: master `issue_watch/test_security_invariants.py:652, 683, 936`, `test_launch.py:75`, `test_marker_contract.py:28-48`, `test_origin_parity.py`, `test_audit.py` (reasons pin rewritten, MC-10), `test_cycle.py`; `hooks/test_launch_level_guard.py`, `test_launch_level_guard_worker.py` (G2 rule 1 tamper tests return with the revert), `test_launch_level_observations.py:79-84` (twelve skipped observations; un-skipped only by the owner); `skills/test_worker_contract.py` and `core/test_orca_session_launch_guidance.py:33, 53` (edited with SEC-15, FR-65); `skills/test_issue_protocol.py:131-135, 462, 745-784` (moved with claim rule C1); `skills/test_issue_orca_worktree.py`, `test_primitive_dual_surface_lookup.py`, `test_agent_work_report.py`, `cli/test_how_we_work_install.py`, `cli/test_issue_body_templates.py`, `commands/test_sweep_command.py`, `sweep/`, `observe/` (sweep golden test edited by a person, FR-41); planb `issue_watch/test_dispatch.py`; pr-a `test_hold.py`, `test_wake.py`, `test_repos.py`, `test_route.py` (adapted per FR-06, FR-13 to FR-22); the restored `issue_pipeline/` tests (about 117 functions, present at `01e7a9e23^`, back with S7). Tests to write are named in sections 4 and 8.
~~~

AFTER (candidate):
~~~text
Under `tests/` of the snapshot named: master `issue_watch/test_security_invariants.py:652, 683, 936`, `test_launch.py:75`, `test_marker_contract.py:28-48`, `test_origin_parity.py`, `test_audit.py` (reasons pin rewritten, MC-10), `test_cycle.py`; `hooks/test_launch_level_guard.py`, `test_launch_level_guard_worker.py` (G2 rule 1 tamper tests return with the revert), `test_launch_level_observations.py:79-84` (twelve skipped observations; un-skipped only by the owner); `skills/test_worker_contract.py` and `core/test_orca_session_launch_guidance.py:33, 53` (edited with SEC-15, FR-65); `skills/test_issue_protocol.py:131-135, 462, 745-784` (moved with claim rule C1); `skills/test_issue_orca_worktree.py`, `test_primitive_dual_surface_lookup.py`, `test_agent_work_report.py`, `cli/test_how_we_work_install.py`, `cli/test_issue_body_templates.py`, `commands/test_sweep_command.py`, `sweep/`, `observe/` (sweep golden test edited by a person, FR-41); planb `issue_watch/test_dispatch.py`; pr-a `test_hold.py`, `test_wake.py`, `test_repos.py`, `test_route.py` (adapted per FR-06, FR-13 to FR-22); the restored `issue_pipeline/` tests (about 117 functions, back with S7) and planb's `test_complete*.py` (FR-83). Tests to write are named in sections 4 and 8.
~~~

#### Hunk 689c691

BEFORE (baseline):
~~~text
Nothing below has run. Each needs the owner's go when it writes to GitHub or types into a session.
~~~

AFTER (candidate):
~~~text
Nothing below has run. Each needs the owner's go if it writes to GitHub or types into a session.
~~~

#### Hunk 694c696

BEFORE (baseline):
~~~text
| Cron shadow run | the cron line runs `run-all --dry-run` for 24 hours under cron's environment | no agent, no config generated, no GitHub write; real replies captured to replace assumed fixtures. S17 pass list (proposal): six `first_run` checks green, this run clean, X-001 run, owner's go; then `auto_enable` on once | D02, D09; BS |
~~~

AFTER (candidate):
~~~text
| Cron shadow run | the cron line runs `run-all --dry-run` for 24 hours under cron's environment | no agent, no config generated, no GitHub write; real replies captured to replace assumed fixtures. The S17 pass list is in 8.2 | D02, D09; BS |
~~~

#### Hunk 704,705d705

BEFORE (baseline):
~~~text
The S17 go/no-go record names the code head, host, installed primitive hashes, fixture captures and the failed as well as passed probes, and is kept by an agent from the owner's chat go.

~~~

#### Hunk 719a720

AFTER (candidate):
~~~text
| FR-83 | R24 (owner), D04 | planb `issue_pipeline/complete.py`, requirements line 50 (R24), `tests/issue_watch/test_security_invariants.py:1059-1079` |
~~~


## Re-review findings on changed lines

Grading check used for each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is blocking only when that sentence holds with no further guess (two stated texts that contradict, harm to a safety boundary, or an acceptance check that cannot pass). Where the sentence needs a guess between two readings the text allows, or the finding is a requirement the text never states, it is Medium.

=== REQUIREMENTS ANALYSIS ===

Experts: Wiegers (lead), Adzic, Cockburn. What holds: FR-83 has an id, a "shall" sentence, named acceptance checks that exist in planb (`tests/issue_pipeline/test_complete.py`, `test_complete_cli.py`, the two-writer scan) and a source (R24, D04); it matches R24 point by point (coordinator only; succeeded moves Status to `In review`; failed, blocked, partial comment only; Status moved only from an allowed Status; no worker or launched agent calls it). Appendix A and 12.4 trace it.

**G1 (MAJOR, Medium) The grant list is three names in two places and four in the requirement.** origin=changed (SEC-07 and OA-11 changed; X-1 and OD-11 did not). Expert: Wiegers.
- SEC-07 (4.5): "the owner grants at most `issue.assign`, `issue.comment`, `issue.body.append_plan_sections` and `issue.status.move` (for FR-83; NEW (author))". OA-11 (10) says "three of QG3 plus `issue.status.move`".
- X-1 (11, the spec's own resolution of D04 against Q03): "three: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`; default empty". OD-11 (2) says "the owner grants three standing entries". The reviser updated SEC-07, OA-11 and 12.4 but not X-1.
- Grading: an implementer who builds the loader's closed list from X-1 gets three names, and FR-83 can then never be granted, so the verb always refuses. The implementer who builds it from SEC-07 (the row with the acceptance check "one `E-NO-GRANT` case per entry") gets four. 12.4 and SEC-07 both say the fourth name is the author's addition, and OD-11 is a faithful record of what QG3 said, so the text allows the better reading. Medium.
- Recommendation: X-1's resolution reads "three of QG3 plus `issue.status.move` for FR-83 (SEC-07)"; leave OD-11 as the verdict record. Priority Medium.

**N12 (Note) FR-83 says "the issue's grants".** R24 says the Status write needs "that issue's grant row" (an owner record per issue, restored contract line 300); SEC-07 defines a standing per-repo `grants` list. FR-83's phrase "Without the issue's grants `issue.comment` and `issue.status.move` (SEC-07)" blends the two, and does not say whether a succeeded run needs both grants while a failed run (comment only) needs only `issue.comment`. This sits on the unresolved two-records question of review 1 (F6), which is not rechecked; FR-83 adds one more mention. Recommendation: say "grants of the repo" and which outcome needs which name.

**N13 (Note) FR-83's trigger and its placement in the flow.** FR-83 acts "after it reads a succeeded `worker_done`". WORKER-CONTRACT WC-5 sends `--outcome succeeded` for a contract whose `worker_status` is `partial` as well, while FR-83 and step 6 say partial gets a comment only; the verb should key on the contract's `worker_status`, not on the outcome word. Step 6 also runs before the commit (step 7) and the push and PR (step 8), so for a worker at level None the comment holds no PR number; "PR number only" describes the Full Submit result file, which `GOVERNED_LEVELS_ALLOWED` keeps off. Both are wording.

=== ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Newman, Hohpe, Nygard. What holds: the two-writer rule now has one owner per writer (poll: none; `repo_init.py`: the trigger label at init; `complete.py`: the coordinator's result comment and Status move); NFR-02's one-writer-per-file rule is not touched, because `complete.py` writes to GitHub, not to a spec-owned file; the per-run marker makes a second call for the same run post nothing new (verified in planb `complete.py`), which satisfies the at-least-once rule of 3.1. The worker-side control exists: planb's guard refuses a bound worker's `issue-pipeline complete` as TAMPER (best effort; the guard comment names the grant-row rule as the real control).

**G3 (MAJOR, Medium) FR-82 is worded as a repo-wide rule but the spec's other writers contradict the wording.** origin=changed. Experts: Fowler, Whittaker (divergence attack).
- FR-82: "The only code that may write is `issue_watch/repo_init.py` (...) and the coordinator-only `issue_pipeline/complete.py` (FR-83); `github.py` and the cycle never." SEC-02 runs `gh pr merge <N> --repo <R> ...` in the merge verb; SEC-07 grants `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`; the claim session (`/sc:issue --claim`, master) assigns and comments; `repos grant` writes config. None of them is `repo_init.py` or `complete.py`.
- The acceptance check scopes the rule correctly (the planb scan covers `issue_watch/*.py` and `issue_pipeline/*.py` only), and OA-28b says "NG-2 covers only the poll cycle", so the intended meaning is clear from the same row.
- Grading: an implementer who reads the first sentence as written could add a repo-wide scan that fails on the merge verb; the check column and OA-28b point the other way. Two readings: Medium.
- Recommendation: "The only code in `issue_watch/` and `issue_pipeline/` that may write is ...". Priority Low within Medium.

**G4 (MAJOR, Medium) The branch where PR 682 stands names an owner decision that has no owner-action row, and its check cannot pass.** origin=changed (8.3 line 500). Experts: Fowler, Nygard.
- 8.3: "S9 rebases planb onto a tree without `issue_pipeline` (untested path) and the owner names a new home for `complete.py` (FR-83)". FR-82's check keeps the planb scan "unchanged"; that test (planb `test_security_invariants.py:1062-1079`) globs `issue_pipeline/*.py` and asserts `complete.py` is among the scanned names, so with `complete.py` elsewhere it fails and must be edited, which "unchanged" forbids.
- Section 10 has no row for naming the new home (the only mention is 8.3), so the branch has no owner gate and no rule for the test.
- Grading: the branch is the one the document marks "untested path" and gives about 50 percent confidence; an implementer who reaches it must guess where the file goes and how to keep the scan. Medium.
- Recommendation: add the home of `complete.py` and the scan-test edit to the OA-1 row (or to 8.3's list of consequences). Priority Medium.

=== TESTING ANALYSIS ===

Experts: Crispin (lead), Gregory, Adzic. What holds: the S9 row lists `test_complete*.py` and the two-writer scan; 13.1 lists planb's `test_complete*.py`; FR-83's check names existing planb tests plus one NEW case; 12.2 records the open question "whether `E-NO-GRANT` covers `issue.comment` for the R24 result comment" with the `grep -rn` check that settles it.

**G2 (MAJOR, Medium) FR-83's no-grant refusal has no stage that builds or tests it.** origin=changed. Experts: Crispin, Nygard.
- FR-83: "Without the issue's grants `issue.comment` and `issue.status.move` (SEC-07) it refuses before any `gh` call", check "NEW: no grant, no `gh` call". Planb's `complete.py` has no grant check (the word appears only in the docstring and the verb's help text; the guard comment says the grant-row rule of the contract is the control). The grants store, `repos grant` and `E-NO-GRANT` do not exist on master and are built at S14 (SEC-01 to SEC-13; OA-11 is an S14 precondition). The S9 row lands the verb with "Status move needs OA-11" but its tests column does not list the NEW no-grant case, and S14's deliverables column does not name FR-83.
- Grading: an implementer who follows S9 as written lands a GitHub-writing verb that refuses on no grant at no stage, and the NEW check passes nowhere. Mitigations the text gives or the code has: nothing calls the verb until the coordinator exists (S14 at the earliest), the watcher stays off until S17, and a bound worker is refused by the guard. SEC-07's "one `E-NO-GRANT` case per entry" at S14 may cover the fourth name, but that is a reading, not a stated link. Medium.
- Recommendation: list FR-83 in S14's requirement column (its grant refusal rides on SEC-07), or put the NEW no-grant case in S9's tests column and say how S9 reads a grant before S14 exists. Priority Medium.

**G5 (MAJOR, Medium) The reviser edited text no blocking finding names, and two edits narrow stage acceptance.** origin=changed. Experts: Wiegers, Crispin.
- Review Loop bullet 6 and the review-1 Reviser brief: "revise only text a blocking finding names ... prefer deleting or narrowing to adding". The diff has 39 hunks; 16 belong to F1 (1.3, 3.1, step 6, row-form numbers line, FR-82, the 4.2 header, FR-83, SEC-07, L-08, S9, 8.3, OA-11, 12.2, 12.4, 13.1, Appendix A). The other 23 are trims and rewording of text F1 does not touch (1.1, 1.3 closing line, 1.3 PR 693 line, section 2 note, L-01, 5.2, 6.1 line, 6.3 rows, section 8 rules, S15, 9, 10, 11 rows X-14, X-16, X-19, 12 lines, 13 intro, the cron shadow run row and the S17 record sentence).
- Most are wording only and keep their meaning (for example X-14, X-16, X-19, the 6.3 rows, 5.2's dropped "Nobody ran its tests"). The S17 go/no-go record and the pass list were removed from 13.2 but remain in the 8.2 S17 row, so nothing is lost there. Three removals change what a stage or a row requires:
  1. S15 (8.2): "kill-and-restart tests at every persistence boundary" became "kill-and-restart tests", and "S15b cap with single writers" became "S15b cap". Kill-and-restart tests stay required by FR-29 and RK-9 (MC-6) at the ack-to-state boundary and NFR-02 keeps one writer per file, so no stated text now fails; the scope "every persistence boundary" for S15a is no longer stated anywhere (grep of the candidate: no other "boundary" in a test requirement).
  2. Section 8 rules lost "A green PR 686 alone does not prove the combined tree."
  3. Section 4's row form lost "Long enumerations stay in the verdict item cited", which told a reader where rows such as SEC-02's "13 closed reasons" are enumerated.
- Grading: Medium, because the narrower texts are still consistent with the requirements that survive and nothing named rests on the removed qualifiers. The reviser's own byte accounting per finding id was not among this review's inputs; the net change is +844 bytes.
- Recommendation: restore the three removals (they add about 200 bytes) and leave the other 20 hunks. Priority Medium. No brief clause was overridden by this review.

**N14 (Note) Planb scope and tag.** 5.2 lists planb's edits to `issue_pipeline/{brief,cli,reads}.py` but not that planb adds `complete.py` (1.3 and FR-83 say so); step 6 tags the verb `[P]` while the package it lives in is `[R]` (removed by PR 682) until the revert restores it.

**N15 (Note) L-01 lost its UNVERIFIED mark.** L-01 now reads "one file in the unification work's task package under `.dev/tasks/`" with the "(name UNVERIFIED)" mark removed; the file name is still not given.

=== COMPLIANCE ANALYSIS ===

Experts: Wiegers (lead), Nygard, Hightower. The five owner rules, checked against the changed text:

| Owner rule | Where the spec states it | Result after the F1 fix |
|---|---|---|
| 1 The poll writes nothing to GitHub outside the allowed steps | FR-06, FR-82, MC-8, OA-28b, step 6 | Holds. `complete.py` is a coordinator verb, not a poll step; the scan keeps `github.py` and `cycle.py` read-only (verified in the planb test). Wording issue: G3. |
| 2 A person's typed go before every push and merge | 3.1, section 8 rules, FR-32, SEC-01, SEC-02 | Holds for the changed text. The result comment and Status move are neither a push nor a merge. (The review-1 push-scope question, F4, is not rechecked.) |
| 3 Workers never run `/sc:pr-submit` | SEC-05, FR-32, FR-38 | Unchanged. FR-83 adds "No worker or launched agent calls it", backed by the planb guard's TAMPER refusal (best effort). |
| 4 No standing merge or close grant | SEC-06, SEC-12, OD-10 | Holds. `issue.status.move` is not `pr.merge` or `issue.close`; SEC-06 still refuses both; `grants` still starts empty and the fourth name is refused until the owner grants it once in chat (SEC-07, OA-11, 12.4). The only "standing" statements in the document concern merge and close, plus the definition "Grant: a standing permission for a small class of GitHub writes. Default none", which the fourth name fits. |
| 5 Approvals given in chat, recorded by an agent | SEC-07, SEC-08, SEC-14, OA-11 | Holds: the grant is "once in chat, recorded by an agent with `repos grant`". |

**Does `issue.status.move` conflict with the no-standing-grant rule?** No. The rule bars standing merge and close; a Status move to `In review` is neither, default stays empty, and the name is added under the same chat-recorded, once-only door as the other three. The one tension is wording (N12: R24 says "that issue's grant row", SEC-07 is a standing per-repo list), which is a Note.

=== CORRECTNESS ANALYSIS ===

Experts: Nygard (lead), Fowler, Adzic, Crispin, Whittaker. Scope: changed lines only (re-review rule for FR-8 to FR-10).

### State Variable Registry (changed surface)

| Variable | Type | Initial value | Invariant | Read by | Written by |
|---|---|---|---|---|---|
| `grants` | list of strings | empty | subset of four names (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.status.move`); `pr.merge` and `issue.close` refused (SEC-06, SEC-07); X-1 and OD-11 still say three (G1) | coordinator verbs, `complete` | `repos grant` on a recorded chat go |
| per-run result marker | GitHub comment text `<!-- sc:issue:result issue=<N> run=<approval event id> -->` | absent | a second call for the same run posts no second comment (planb `complete.py`; FR-83 says "per-run marker") | `complete` | `complete` |
| issue Project Status | enum | an allowed Status (Research, Spec, Plan, Debug) | moved to `In review` only from an allowed Status; any other current Status is left alone and reported `status_moved_by_person` | poll start gate, `complete` | `complete` (succeeded only), a person |

### Guard Condition Boundary Table (changed guards only)

An input class with no row is left out because it cannot occur for that guard; the reasons are in the last row.

| Guard | Location | Input condition | Variable value | Guard result | Specified behavior | Status |
|---|---|---|---|---|---|---|
| grant gate | FR-83 | Zero/Empty | `grants` empty | refuse | "refuses before any `gh` call" | OK (stage for the check: G2) |
| grant gate | FR-83 | Legitimate edge: succeeded run, only `issue.comment` granted | one of two names | not stated | refuse everything, or comment only? | GAP (N12) |
| grant gate | FR-83 | Legitimate edge: failed run, only `issue.comment` granted | comment only needs one name | not stated | whether `issue.status.move` is required for a comment-only outcome | GAP (N12) |
| outcome | FR-83 | Divergence: contract `partial` with `worker_done --outcome succeeded` | WC-5 mapping | trigger says "succeeded `worker_done`" | partial is "comment only" in FR-83 but the trigger word could read as succeeded | GAP (N13) |
| Status guard | FR-83 | Typical | Status Research, Spec, Plan or Debug | allowed | moves to `In review` | OK |
| Status guard | FR-83 | Legitimate edge: Status already `In review` or moved by a person | not allowed | left alone | `status_moved_by_person` | OK |
| per-run marker | FR-83 | Legitimate edge: second call for the same run | marker present | skip | "one result comment (per-run marker)" | OK |
| label step | FR-82 | Zero/Empty | `auto_enable` false | read only | "reports `would_create`" | OK (unchanged semantics) |
| result outcome, writers | FR-83, FR-82 | Sentinel, Maximum | no sentinel or capacity exists for these guards | n/a | left out: the guards compare an enum and a presence test | n/a |

Three rows are GAP: two belong to N12 and one to N13 (Notes; no stated text does harm and nothing named rests on them). The table is complete for the changed guards.

### Quantity Flow Diagram (new stage after `worker_done`, FR-21)

```text
[B workers finish: worker_done]
   --> [contract worker_status: succeeded S, partial P, failed F, blocked K; S+P+F+K = B]
   --> [complete: result comments = S+P+F+K (one per run, marker-deduplicated)]
   --> [Status moves = S only; P, F and K never move it]        <-- divergence N != M, handled by FR-83
   --> [step 7 commit, step 8 typed go, push, PR]               <-- no count dependency on the Status move
```

No consumer assumes the Status moves equal the comments. The one under-specified edge is N13 (partial mapped through the outcome word).

### Whittaker adversarial analysis (changed surface)

1. **Zero/Empty Attack.** The invariant at FR-83 ("refuses before any `gh` call" without the grants) fails when `grants` is empty and the verb has no grant code: planb's `complete.py` checks no grant. Trace: S9 merged; before: `grants` absent; after: `issue-pipeline complete` run by a person posts a comment and moves the Status. Nothing in the first build calls it by itself, so the harm is bounded. (G2.)
2. **Divergence Attack.** The invariant at FR-82 ("The only code that may write") fails when read repo-wide: the merge verb of SEC-02 and the claim session also write. Trace: a repo-wide scan over `src/superclaude/cli` fails on `gh pr merge`. The acceptance check scopes it to two packages. (G3.)
3. **Sentinel Collision Attack.** The Status value `In review` is both the end Status of `complete` and "not an allowed Status" for the poll's start gate, which is how a second call or a person's move is detected (`status_moved_by_person`). A second call for the same run therefore reports `status_moved_by_person` although the Status was moved by `complete` itself. The report is harmless (the comment marker already blocks a second comment); recorded here, not as a finding.
4. **Sequence Attack.** Step 6 runs before the commit and the typed go (steps 7, 8). Trace: worker succeeds; Status becomes `In review`; the commit is refused (FR-32, escalated); the issue stays `In review` with no commit. R24 decides the timing ("when the agent has finished the work"); the spec follows R24, so this is the owner's rule applied, not a defect. S9 before S14: the verb lands before grants exist (G2).
5. **Accumulation Attack.** One comment per run through the marker; repeated runs for one issue each add one comment (a hand-back round has its own approval event id), bounded by `HANDBACK_MAX` 3 (FR-35). No finding.

## Follow-up candidates

Medium warnings and notes never fail the review, trigger a revision or appear in the Reviser brief. This run is `--unattended`, so the list is only recorded; no issue is opened. Medium and Note findings of review 1 (F2 to F14, N1 to N11) are carried by that report and were not rechecked.

Medium (5): G1 grant list three versus four (11 X-1, 2 OD-11, 4.5 SEC-07); G2 FR-83 no-grant refusal has no stage (4.2 FR-83, 8.2 S9, S14); G3 FR-82 "only code that may write" is repo-wide in wording (4.1 FR-82, 4.5 SEC-02); G4 new home of `complete.py` has no owner-action row and the scan test cannot stay unchanged (8.3, 4.2 FR-83, 10); G5 reviser edits outside F1, three of which narrow stage or row text (8.2 S15, 8 rules, 4 row form).

Notes (4): N12 FR-83 "the issue's grants" and which outcome needs which grant; N13 FR-83 trigger keyed on the outcome word and step 6 placement before the PR exists; N14 5.2 omits that planb adds `complete.py`, and the `[P]` tag; N15 L-01 lost its UNVERIFIED mark.

## Findings block

```findings-v1
{"id": "G1", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "three: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`; default empty", "anchor2": "`issue.body.append_plan_sections` and `issue.status.move` (for FR-83; NEW (author))", "refs": ["X-1", "OD-11", "SEC-07", "OA-11", "FR-83"], "claim": "X-1 and OD-11 still give the grant list as three names while SEC-07 and OA-11 now allow four, so the closed list has two sizes."}
{"id": "G2", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Without the issue's grants `issue.comment` and `issue.status.move` (SEC-07) it refuses before any `gh` call.", "anchor2": "S9 land planb (with `complete.py` and its verb, FR-83)", "refs": ["FR-83", "SEC-07", "S9", "S14"], "claim": "FR-83's no-grant refusal is not built or tested at S9 (grants arrive at S14) and no later stage names FR-83, so its NEW check passes at no stage."}
{"id": "G3", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "The only code that may write is `issue_watch/repo_init.py`", "anchor2": "again before `gh pr merge <N> --repo <R>", "refs": ["FR-82", "SEC-02", "SEC-07", "OA-28b"], "claim": "FR-82 says the only code that may write is two files, while the merge verb, the claim session and repos grant also write; the check column scopes it to two packages."}
{"id": "G4", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "the owner names a new home for `complete.py` (FR-83)", "anchor2": "planb `test_security_invariants.py:1059-1079` unchanged", "refs": ["8.3", "FR-82", "FR-83", "OA-1"], "claim": "In the branch where PR 682 stands the owner must name a new home for complete.py, no owner-action row records it, and the unchanged planb scan test cannot pass with the file elsewhere."}
{"id": "G5", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "four PRs: S15a wake-check and wake-ack with kill-and-restart tests; S15b cap;", "anchor2": "Order: merged design section 5, D14, D15.", "refs": ["S15", "8", "4", "Review Loop bullet 6"], "claim": "The reviser edited 23 hunks no blocking finding names; three removals narrow stage or row text (S15a every persistence boundary, S15b single writers, the combined-tree caution, the enumeration pointer)."}
{"id": "N12", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Without the issue's grants", "refs": ["FR-83", "SEC-07", "R24"], "claim": "FR-83 blends R24's per-issue grant row with SEC-07's standing grants and does not say which outcome needs which grant name."}
{"id": "N13", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "after it reads a succeeded `worker_done` or a launched agent's `result.md`", "refs": ["FR-83", "WC-5", "3.2"], "claim": "The trigger keys on the outcome word although partial maps to outcome succeeded, and step 6 runs before any PR exists."}
{"id": "N14", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`complete.py` (coordinator-only result comment and Status move, FR-82, FR-83)", "refs": ["5.2", "1.3", "3.2"], "claim": "Section 5.2 does not list complete.py among planb's changes and step 6 tags the verb [P] while its package is [R]."}
{"id": "N15", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Interim ledger of owner answers: one file in the unification work's task package under `.dev/tasks/`;", "refs": ["L-01"], "claim": "L-01 dropped its UNVERIFIED mark on the file name although no name is given."}
{"prior": "F1", "status": "resolved"}
```

scoped PASS: changed lines + prior blockers

## Reviser brief

Blocking finding ids: none. No revision is required. Medium and Note findings (G1 to G5, N12 to N15) never trigger a revision, never fail the review and never appear in a reviser brief; the report names no brief clause it overrode.

verdict: PASS
