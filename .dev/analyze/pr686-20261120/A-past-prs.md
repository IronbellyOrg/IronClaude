# A: past pull requests versus PR #686 (lens: merged and closed PRs)

## Summary

1. PR #686 is not a fresh project. It is a rewrite of the issue watcher that ironbelly built in #447 and #448: the same package, with cycle, github, launch, predicates, record, audit and cli reshaped in place, runner.py unchanged, and four new files (hold, repos, route, wake).
2. It is "PR A" of a plan the same author (clayphi) had approved in the design merged as #681 (`docs/designs/orchestrator.md`). That design lists, symbol by symbol, what PR A keeps, reshapes, removes and adds. So #686 builds on #447/#448 and implements #681.
3. It finishes a removal that #682 (PR D, clayphi, merged) started. #682 deleted the `issue_pipeline` package (ironbelly's #584 and #591) and rule WC-17. #686 then deletes the watcher's side of that handoff (the `/sc:issue --claim N --pipeline none` launch, approval comment, trigger and approver settings, project-board reads). So it replaces the #584/#591 handoff and makes the #548 option 3 claim-level decision moot for the watcher.
4. It does not touch or duplicate the sweep (#539, #579), the observer (#503, #514, #577, #592, #598, #673) or the worker contract. Its diff is limited to `issue_watch/`, `tests/issue_watch/` and CHANGELOG. The word "sweep" in it is the poller's own record sweep (`record.sweep`, `_sweep`), not the `superclaude sweep` command.
5. Two lineages. Ironbelly authored the original watcher, issue pipeline, sweep, observer and worker contract. Clayphi authored the 655 series (#681, #682, #683, #684, #686, open #690). Commit identities are mixed: both lineages' PR commits show the shared `coder` account plus Claude Code.
6. Siblings: #681 to #684 merged; #690 (PR P, `/sc:issue --plan`) is open and complements #686. No PR B (orchestrator skill) and no PR E (live test, status banners) exists yet; #686 depends on both by contract and leaves the old watcher design docs stale until PR E.

## Table of relevant PRs

| PR | State | Author | What it did | Relation to #686 | Evidence |
|---|---|---|---|---|---|
| 447 | merged 2026-11-08 | ironbelly | Added `superclaude issue-watch` (check-config, init-state, once, reset, status), nine modules in `issue_watch/`. Finds issues with a trigger label and an approval label from a listed approver, writes a durable pending record, starts one Orca claim session. Never ran live, `enabled: false`. | Builds on and replaces most of its behaviour. Same package; lock, record, audit, runner, call budget kept; trigger, approver and claim launch removed. | PR body: "starts one Orca claim session (/sc:issue --claim N)". Master `launch.py:33` pins `/sc:issue --claim N --pipeline none`; `origin/pr-686` `launch.py` has `build_wake_line` and `session_command` instead. cycle.py 1406 to 2226 lines, record.py 865 to 1118. |
| 448 | merged | ironbelly | Follow-up to #447: closed the approvers-file race, re-read the deadline per Orca probe (cycle, launch, tests). | Replaces (the approvers file is removed by #686). | #686 body: "the `issue-watch:trigger` and approver-file settings" removed. |
| 451 | merged | ironbelly | Docs only: watcher brainstorm record, task outcome, reflect patterns (#331). | Complements (history, no overlap). | Title and file list under `.dev/brainstorms/...github-issue-watcher`. |
| 485 | merged | ironbelly | Docs: design drift fixes and owner rollout checklist (`issue-watcher.md`, `issue-watcher-setup.md`). | Now stale: #686 changes no design doc, so these still describe removed code. | `git diff --stat origin/master origin/pr-686 -- docs/designs` is empty; `issue-watcher.md` line 3 still says "Implemented and merged in PRs #447 and #448". |
| 548 | merged 2026-11-14 | ironbelly | Docs: owner's option 3 decision, the watcher's claim keeps its default worktree level, D2 claim-only marked superseded. | Conflicts with the new direction (the watcher no longer claims). Becomes history. | #548 body; #686 removes the claim session launch. |
| 584 | merged 2026-11-17 | ironbelly | Plan A of the claim handoff: new `issue_pipeline` package (plan hash, approval records, approval-line check, worker brief), D2 chat-approval amendment. | Replaced (deleted by #682; #686 removes the watcher's matching approval code). | #682 body: "Deletes `src/superclaude/cli/issue_pipeline/`". `git ls-tree origin/master` shows only `docs/designs/issue-pipeline-*.md` left. |
| 591 | merged 2026-11-17 | ironbelly | Plan B: coordinator handoff. WC-17, guard G2 change, `release-worker`, watcher switched to `--pipeline none`. | Replaced. WC-17 and guard rule 1 removed by #682; the watcher's `--pipeline none` launch removed by #686. | #591 body: "The watcher now claims with `--pipeline none`". #682 body: "removes rule WC-17". |
| 583, 613, 636, 425, 373 | merged | ironbelly | `/sc:issue` command and its claim pipeline levels, remove plain `approved` route, default level from the issue, stop recommending `/sc:task`. | Complements. `/sc:issue --claim` still exists for manual use; #686 only stops the watcher calling it. | Titles and file lists only; #686 touches none of those files. Detail UNVERIFIED. |
| 432 | merged | ironbelly | Launch-level guard for claim-launched agents (#394). | Complements; guard is outside #686's file set. | Title; `git diff --name-only origin/master...origin/pr-686` shows no hook file. |
| 587 | merged | ironbelly | Docs: orchestrator, observer and issue-watcher alignment decisions (#339). | Complements (earlier decision record). Not read in detail. | Title and file list under `.dev/brainstorms/20261113-orchestrator-tui-alignment/`. |
| 539 | merged 2026-11-14 | ironbelly | `superclaude sweep run`, `/sc:sweep`, `sc-sweep-protocol`, WC-16 coordinator loop (Phase 1 of orchestrator mode, #339). Read-only report of Orca sessions. | Complements. No shared code. Design `orchestrator.md` line 65 gives `/sc:orchestrator` to the issue-polling orchestrator and leaves #444's general `--sub` mode to another piece. | `git grep` of `origin/pr-686` finds no import of `cli.sweep` or `cli.observe`. |
| 579 | merged | ironbelly | Sweep fix: working class with real Orca names. | Complements. | Title; sweep files untouched by #686. |
| 503, 514, 577, 592, 598, 673 | merged | ironbelly | The observer (`superclaude observe`): release 1, release 2 coordinator questions, live read, question text and dispatch link, visual parity. | Complements. Separate read-only tool; no shared module. Both read Orca terminal state, but #686's `wake.py` has its own `/proc` process lookup. | `cli/observe` and `cli/sweep` are separate packages on master; absent from #686's diff. UNVERIFIED whether the observer will later show wake state. |
| 434, 508, 585, 411, 397 | merged | ironbelly | Worker contract work (liveness rules, `--unattended` default, D2 Ruling wording, P1 contract for 16 commands). | Complements. #686 does not edit `WORKER-CONTRACT.md`. The contract edit that matters (WC-17 removal) is #682. | #682 file list contains `WORKER-CONTRACT.md`; #686 does not. |
| 532 | merged | ironbelly | Supervised orchestration technical reference and task records. | Complements; one sentence of it was patched by #682. | #682 body. |
| 681 | merged 2026-11-20 | clayphi | Docs only: approved design `docs/designs/orchestrator.md` (1412 lines), the spec for the 655 series. | Builds on / implements it (#686 is PR A). | Design line 363: "PR A does all of this"; line 145: PR A and PR B build against the wake format. |
| 682 | merged 2026-11-20 | clayphi | PR D: deleted `issue_pipeline`, WC-17, guard G2 first rule; 4,599 lines removed. | Builds on (#686 states it depends on this). Same author, same series. | #682 body: "so PR A can delete the `issue_watch` symbols the old package imported without a shim". |
| 683 | merged | clayphi | `/sc:closeout` command and skill (issue 668); adopts a third-party closeout skill under Apache-2.0. | Complements. The orchestrator's close wave uses it; the live test (PR E) needs it. No shared code. | Design line 797: issue 668's PR "must be merged before the live test (PR E)". |
| 684 | merged | clayphi | PR C: moves `agent-work-report` into IronClaude and adds the living report with an entry-file contract. | Complements. No shared code with #686. | #684 body ("Contract with PR B") and file list. |
| 690 | OPEN | clayphi | PR P: `/sc:issue --plan` and `--remaining`, adds plan sections to an existing issue. | Complements. #686's plan request wake path assumes it. Both edit CHANGELOG, so a textual conflict is possible (UNVERIFIED). | #690 body; design 4.11 and 8.3. |
| none | n/a | n/a | PR B (orchestrator skill, `superclaude orchestrator` group) and PR E (live test, status banners) have no PR among 300 listed. | #686 is a dependency of both, not a duplicate. | `gh pr list` branch filter for 655, issue-watch, orchestrator returned only 681, 682, 684, 686, 690 and old 447, 539, 548. |

Closed unmerged PRs (#680, #663, #654, #652, #497, #483, #464, #439, #345, #283, #260, #196): none concern the watcher or orchestrator.

## Overlap and duplication findings

- Intended duplication outside this repo: `wake.py` ports about 100 lines of IronFlow's `orca_term.py` (find session by process and ccsession tag, typing check, idle check, send). Its docstring says it "duplicates that script on purpose; consolidating the two is a follow-up (design section 11)". Nothing in this repo is copied.
- Reuse, not rewrite: `runner.py` is unchanged; the lock, budget and audit pieces are reshaped under the design's "keep" rows (design table row 1: reuse of the built issue-watch code).
- Test churn: #447 and #548 report about 2,650 watcher tests; #686 reports 1,399 after about 16,600 deleted lines, which is the removed claim and approval code plus six fixtures.
- Stale docs left behind on master: `issue-watcher.md`, `issue-watcher-setup.md`, `issue-pipeline-fu1.md`, `issue-pipeline-guard-g2*.md`. #682 says status banners are PR E's job.

## Lineage

- Ironbelly (PR author): #339 sweep and orchestrator mode, #331 watcher (#447, #448, #485, #548), claim handoff (#584, #591), the observer (#409 series), the worker contract, `/sc:issue`.
- Clayphi (PR author): the 655 series (#681 to #684, #686, #690). Clayphi also authored #499, #616, #652, #663.
- Reading: #686 is one contributor rewriting the other's watcher, after the same contributor's #682 removed the other's handoff. #681 says the design was "approved by Clay on 2026-11-19". Whether ironbelly agreed is UNVERIFIED in this lens.

## Caveats

- Bodies of #583, #613, #636, #425, #373, #432, #587 and the observer and worker-contract PRs were not read in full; their classification rests on titles and file lists. `gh pr view --json files` caps at 100 files for big PRs.
- Issue #450 is an issue, not a PR. The 300-PR listing starts at #216, so older PRs are not covered.
