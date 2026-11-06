# Owner-approved decisions for the combined revision (round 4)

Approved by the owner on 2026-11-02 (session answer: "yes. Approve all six recommendations in table 1 (D1 to D5 and the hybrid git ownership) and your three loose-end answers"). The reviser applies these; the reviewer checks that they were applied faithfully. Nothing here is reopened for debate.

## Decisions (exact wording to apply lives in each source file)
| ID | Approved outcome | Wording source |
|---|---|---|
| D1 | Option (c): `--unattended` is the only switch, plus the worker-session brief guard from Phase 1 | `decisions/D1/RECOMMENDATION.md` section 5; edits W1-W16 in `decisions/D1/debate/adversarial/merged-output.md` (merge W14 with CR-01's rewrite of 7.2) |
| D2 | Option (a)+(c): only the person gives a Ruling (own session, or typing it into the ledger); the coordinator never relays one; coordinator no-retry/freeze rule for a Ruling-halted plan | `decisions/D2/RECOMMENDATION.md` section 4 |
| D3 | Option (a) amended: `/sc:pr-submit` is never an Orca worker; one ordinary session per PR, in that PR's own child worktree, started only when the person names the PR | `decisions/D3/RECOMMENDATION.md` section 5 |
| D4 | Option (c′): no worker acts outward; the coordinator performs every push, PR, comment, install and paid run, on `IronbellyOrg/IronClaude` only; worker local commits opt-in only (quoted grant, alone in its own Orca child worktree, one `git commit --only -- <paths>` after a succeeded Task, never push, never `--no-verify`) | `decisions/D4/RECOMMENDATION.md` sections 2 and 5 |
| D5 | Option (a): keep nesting depth 1; corrected reasons; coordinator is a person-opened session; WC-13; AC-0.7; AC-C6 | `decisions/D5/RECOMMENDATION.md` section 4 |
| GIT | Hybrid E: coordinator owns push, PR, review replies, comments, merges and worktree removal; workers write no git state except the D4 opt-in commit and `/sc:implement`'s own snapshot and revert | `decisions/git-ownership/RECOMMENDATION.md` section 4 (D4's wording wins where section 6 says so) |

## Loose ends (owner answers)
| ID | Answer |
|---|---|
| L1 | Who runs `/sc:pr-submit`: D3's model wins. A separate ordinary session per PR. Drop git ownership's per-PR worker opt-in (O3) and its "coordinator runs pr-submit in its main chat" wording, except where D3 allows the coordinator's own session after its check passes. |
| L2 | One PR per feature, opened from the feature branch after the child worktrees have been merged back into it. |
| L3 | `.dev/tasks` staging in worker sessions is left to the coordinator, which stages `.dev/tasks` at every commit and at the end of the run; this satisfies the repo's "always staged" rule (`CLAUDE.md:37`). |

## Also apply in this round
| ID | Item | Source |
|---|---|---|
| CR-01 | Feature worktree hierarchy, with the owner's resolutions: Orca's default paths (never `.dev/worktrees/`), no Orca issue/PR linking until it resolves to the fork | `changes/CR-01-feature-worktree-hierarchy.md` |
| FDR-D1..D3 | The three MAJOR (blocking) defects of the Task 11 final review. FDR-D4..D7 are MINOR: notes only under PR #343; touch them only where a line is already being edited for another item | `review/final-diff-review.md` "Changed-line defect list" |
| F0-F5 | Six items from issue #326; F2's location `.dev/worktrees/<run>-<n>/` is replaced by Orca's default paths (CR-01); F5 per L1 | `review/issue-326-evaluation.md` section 3 |
| CMD | Inventory gap: `/sc:impact` and `/sc:graph` (PR #336) are now commands (45, not 43); add rows and fix shifted citations | `review/issue-326-evaluation.md` section 6 |
| PATHS | Every spec mention of `.dev/worktrees/` becomes an Orca-created worktree at Orca's default path | owner decision 2026-11-02 |
| UPSTREAM | SuperClaude upstream is never pushed to or interacted with | owner decision 2026-11-02 |

## Round-4 review fixes (owner decision 2026-11-02, after `review/round4-review.md` FAIL)
| ID | Fix |
|---|---|
| B1 | Before a phase's live tests (7.2), the coordinator asks the owner for approval, then installs that phase into `~/.claude` by running `superclaude install` from the phase branch. One approval per phase, asked before every phase's install. If a phase is abandoned, reinstall from master (`superclaude install` from master). Replace the "`~/.claude` is never reinstalled for this check" wording to match. |
| B1-N1 | Recheck N1 (`review/round4-review.md`, "Recheck after fix pass 1"): `superclaude install` skips existing files unless `--force` is passed (`src/superclaude/cli/install_commands.py:55-57`, `install_core.py:68-69`), so both B1 install lines (phase branch, and master after an abandoned phase) use `superclaude install --force`, as `update.sh:8` does. This is how the approved install takes effect; no approved outcome changes. |
| B2 | Move AC-0.8 from P0 to P1 (the first phase with WC-4 contracts), content unchanged; record it as a placement adaptation of D4's "one P0 check". |

## P0 plan-review spec fixes (owner decision 2026-11-03, after the `/sc:workflow` pre-review of `TASK-WF-orcaWorkerContra-20261102-231950`)
Source: `.dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/REPORT.md` (INV-002, D-004, D-011). The approved version before these fixes is saved as `specs/history/spec-v7-approved-969c770.md`.

| ID | Fix |
|---|---|
| S1 | AC-0.4 at P0: 7.2 steps 3 and 4 use the report file the command already writes, because no P0 command writes the WC-4 contract. Owner answer: yes. As refined after `review/p0-spec-fix-review.md` (B1, B2, N1-N4): AC-0.4 names each command's file. Troubleshoot gains `--output-dir <dir>` and uses `<dir>/REPORT.md`. Workflow uses the `return-contract.yaml` of the package the run creates, which must be new. Adversarial uses `<dir>/adversarial/merge-log.md` and its Metadata `Status:` line (recheck note R1). Section 2.1 lists WC-5's P0 brief override among the contract file's worker-session rules (recheck note R2). Step 3's report path is that file. Its outcome is `failed` when the file is missing or empty or its status is `failed` or `blocked`, and `succeeded` otherwise. Step 4 is `test -s` and must pass. WC-5 states that, before P1, a brief carrying this rule replaces its mapping. Section 2.3 lists the rule as a P0-only brief item. Steps 3 and 4 of 7.2 point to AC-0.4 for P0. |
| S2 | Erratum in AC-1.1: the brief guard has four refusal conditions but three exact reason texts, plus the `guard refused:` prefix for case 3 (section 2.1). |
| S3 | Erratum in section 2.1: `KNOWN_CORE_FILES` spans `install_core.py:13-27`, not 13-24. The same sentence's other `install_core.py` cites move to `:36,56,65-70` and `:12,155` (review note N5). |
| S4 | Section 6: each phase's plan comes in two parts, because `/sc:implement` may not prompt the user outside its halt paths (`sk/sc-implement-protocol/refs/qa.md:288`), and the 7.2 commit and install need the owner's approval. The static plan holds the edits and the checks that need no live run. The coordinator then asks the owner, commits and installs outside any plan. The live plan holds the 7.2 live checks and the phase report, and is written after the static checks pass. Owner answer 2026-11-03: yes. |

## Heartbeat reading (owner decision 2026-11-05, after the P0 phase report)
Source: `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/p0-phase-report.md`, section "Notes for the coordinator and owner", note 2 (heartbeat gaps) and the "Heartbeat length" section. The owner accepted the looser reading. Nothing here is reopened for debate.

| ID | Decision |
|---|---|
| H1 | The looser reading of section 7.2 step 5 condition 4 is accepted. A gap between heartbeats that lies inside a command's own subagent fan-out is accepted, not failed. Spec WC-10 stands as written. Condition 4 limits (a) (at most the cadence once subagent time and `ask` / `check --wait` time are removed) and (b) (at most 20 minutes with nothing removed) are the whole test. The stricter reading (a raw gap longer than the cadence while a subagent runs fails condition 4) is rejected. |
| H2 | The P0 verdict stays PASS. The condition 4 result of the three P0 live checks stays PASS. No P0 check is re-run for this decision. |
| H3 | No spec text changes. WC-10 (section 2.2) and condition 4 (a) and (b) in section 7.2 step 5 already state the looser reading, and no other spec line contradicts it. |

## P1 owner decisions (owner decision 2026-11-05, after the P1 static plan review)
Source: `.dev/reflect/pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258/REPORT.md`, section "Open owner questions". Plan: `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/`.

| ID | Decision |
|---|---|
| P1-D1 | Approved (plan decision D-P1-1). Graph and impact keep the short-name `command` value (`graph`, `impact`) in their contract, and it counts as the worker `command` field. No second key is added. Spec WC-4 ("the exact command line") is read as met by the existing key for these two commands. |
| P1-D4 | Approved after an adversarial debate between two advocates (one per option, one rebuttal round; both ended on option A). Plan decision D-P1-4 stands: in P1 brainstorm passes `--unattended` and `<report-dir>/nested/<command>-<n>/` to its nested `/sc:analyze` and adversarial calls, research enrichment is off, and the `tasklist` and `task` handoffs are skipped and recorded. Reason: spec section 2.1 (nested propagation) applies to every called command that accepts the flag in this phase, and both are P1 commands; the spec's "from P2" wording (row for brainstorm, section 3.1) and AC-2.1 name research enrichment only. One addition: `<n>` starts at 1 per nested command and a retry of a nested call uses the next number, so a nested directory is never reused. |

## AC-1.8 commit grant (owner decision 2026-11-05, after the P1 live plan review)
Source: the owner's own words to the IronClaude orchestrator in session, 2026-11-05: "Why the hell do I need to make this random file ... My words, quoted exactly or not, are all that is required for things like this." The grant file `decisions/P1-AC-1.8-commit-grant.txt` was an invention of the P1 live plan (step lc22), not part of the spec, WORKER-CONTRACT.md or decision D4. Recorded by the coordinator, who heard the owner directly.

| ID | Decision |
|---|---|
| G1 | The owner's own instruction naming a local commit for the AC-1.8 Task, given in the session in any plain wording, is the quoted grant of WC-9 and D4. The brief copies it as given. No separate grant file is created and none is checked for. |
| G2 | WC-9 and D4 are otherwise unchanged: the brief still quotes the owner's instruction, the worker still runs alone in its own child worktree, commits once with `git commit --only -- <paths>`, never pushes, never uses `--no-verify`. |
