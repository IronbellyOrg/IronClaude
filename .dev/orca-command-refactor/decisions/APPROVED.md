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
