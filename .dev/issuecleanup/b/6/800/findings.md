# Round 2 findings: issue #800 (C19) Settle each worker at the end: release or retain its terminal

Checked 2026-11-24 against master `f2894fc44f6e68a7dd6a78c75f59683cb0b5acb9` (worktree `/home/coder/workspaces/worktrees/IronClaude/Realign`). Live state: OPEN, label `enhancement`, no comments, sub-issue of umbrella #716 (read in full with its comments and closing backlog review). Round 1 findings read: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/7/800/findings.md`. Static command: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/6/analyze` (report `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/6/analyze/analyze-report.md`, finding 2: no terminal-settling code in the package). Plan files read-only from `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`).

## Alignment with architectural decisions

| Decision or rule | Verdict | Evidence |
|---|---|---|
| **WORKER-CONTRACT.md:94** ("After `worker_done`, the coordinator opens the contract, then releases or reuses the worker.") | **Aligned; the item gives that sentence its verbs and a test** | The only rule on master names no verb, no check and no recorded reason. |
| **WORKER-CONTRACT.md:183-191** (never on silence: no stop, no retry Task, no release of a worker or worktree, no marking failed) | **Aligned** | The item releases only after `worker_done` is handled. It should say so in one line, because Orca's `worker-release` is the "release" this rule bans on silence. |
| **FR-40** (SPEC:242: never interrupt a worker) | **Aligned** | The item forbids `worker-stop` and `worker-abandon`; `worker-release` is cleanup after settling, not an interrupt. |
| **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): one standing coordinator per project, Clay's design not adopted | **Aligned** | Terminal settling is an Orca-side duty of the standing coordinator, not one of Clay's rows. It is not in the spec's Clay-strength table (SPEC section 7, :435-470) and no row of it is superseded. |
| **FR-26 / S13 / S15** (SPEC:228, :497, :499): verbs of `superclaude coordinator` are NOT BUILT (SPEC:62) | **Partly aligned** | The plan has no verb or stage for terminal settling: S02-F54 is a not-covered row. The duty can still live as a contract rule first, as `WORKER-CONTRACT.md:94` does today. UNVERIFIED which stage the owner wants it in. |
| **FR-70 / X-001** (SPEC:327, :667): claim terminal lifetime is a live check | **Not the same thing** | That is the watcher's claim agent (launched by `orca agent launch`), not a supervised worker; `worker-release` applies only to supervised workers (see below). UNVERIFIED whether a claim agent's terminal ever appears in `worker-list`. |
| **Name clash with the guard verb** (the plan's `release-worker`, issue #698; code `cli.py:201`, `release.py:38`) | **Name clash, no conflict** | `release-worker` removes the launch-level guard's session record; Orca `worker-release` closes a terminal. The item cites SPEC:762 as evidence; that line is Appendix B's bullet on issue 698 and does not support a terminal rule, so the evidence line is wrong (round 1 said the same). |
| **`/sc:closeout`** (`src/superclaude/commands/closeout.md:76`: never "Release, stop, abandon or message a worker or its Dispatch"; it only sets the worker's Task to completed) | **Aligned; complementary** | Closeout (after merge) deliberately leaves terminal release to the coordinator. This item is that duty (after `worker_done`). |
| Orca CLI, read live 2026-11-24 (`worker-release --help`, `worker-retain --help`, `worker-list --help`) | **Fact base for the build** | `worker-release --dispatch <id>` "closes only the exact coordinator-owned agent terminal of that worker", keeps an output archive, is idempotent (repeat reports `already_released`), and "only `release_unknown` exits 1; retained, `release_pending`, and `already_released` exit 0". `worker-retain` records a durable exception and does nothing else. `worker-list --terminal-state` accepts `active|reclaimable|retained|release_pending|release_unknown|released`; without `--run` it is scoped to the bound Run, or every Run if unbound. |

Searched DECISIONS.md, SPEC.md and the verdicts for `worker-release`, `worker-retain`, `reclaimable`, `terminal`, `settle`: only FR-18 (shared terminal helper), FR-34 (restart), FR-70 (claim terminal lifetime) and X-001 hit; none states a settle-the-terminal rule. So "none apply" is false; the governing rules are the ones above, and the plan is silent on this item.

## Complementary issues

- **#799** (C18): needs the old worker's terminal released before a hand-back round. Interface: #800's `worker-list --run <id> --terminal-state` result is #799's start precondition.
- **#788** (C7): its `orca worktree ps` check refuses to start a worker where another agent is live; an unreleased settled terminal would trip it. #800 runs before that check can pass on a reused worktree.
- **#792** (C11): defines and validates `worker_done`; #800 starts only from a handled, valid one.
- **#786** (C5) and **#755** (open, Run rule): `worker-list --run` needs one known Run id; #755 decides how many Runs exist.
- **#784** (C3): the return contract reports what #800 settles (per #716 order).
- **#771** (open): the other "end of a worker's life" duty (after the merge). Same file, different moment.
- **#766 / #590** (open, sweep reads of terminal states): read side of the same states; no conflict. The sweep already reads `reclaimable` (`src/superclaude/cli/sweep/classify.py:491`) and calls no release (round 1; Grep in this round of `src/superclaude` finds no `worker-release` caller).

## Closest overlap

**#771** (finish after merge). Shared: the ordered "end of a worker's life" list in `WORKER-CONTRACT.md` ("Issue pipeline duties", `:292-303`); both say what the coordinator does after the work is done. Share of #800's done-when it covers: about 10 percent (none of its test; it only competes for the same contract paragraph). Next closest: **#799** (about 5 percent; consumes the settled terminal) and **#788** (about 5 percent; the live-agent worktree check that #800's output feeds). No open issue builds `worker-release`, `worker-retain` or the `reclaimable` check.

## Standalone or merge

**Verdict: stand alone.** Test against #771:
- *Owner*: same coordinator-duty line; #771 needs three owner decisions (who runs closeout, the recipient of `not_done`, the worktrees schedule); #800 needs none.
- *Acceptance test*: #771 pins contract text for a post-merge route; #800 needs a fixture run that ends with no `reclaimable` Run row and a recorded reason per retained one.
- *Files touched*: both touch `WORKER-CONTRACT.md`; #800 also touches the Orca call site and a fixture; #771 touches `closeout.md`/`worktrees.md` boundaries.
- *Build phase*: #771 is unscheduled; #800 is Phase 2 in #716's order (with C5 to C15, C19).
- *Risk if merged*: a small (S) item with no open decision would wait behind #771's open owner questions, and the merge-time duty and the worker-time duty (before vs after the merge) would be tested together.
Merging would be right only if the owner wants one single "finish list" item for both moments; the cheaper fix is a cross-link plus one ordered list in the contract, as round 1 proposed. The owner's 2026-11-24 precedent of folding a small item into its host (#798 into #797, #806 into #782) applies when the small item has no consumer without the host; #800 has its own consumer (the sweep's "settled" signal and #799) and its own fixture.

## Closed issues and merged PRs checked

- **#668 / PR #683** (merged): `/sc:closeout` explicitly excludes releasing a worker (`closeout.md:76`); delivers the Task-completed half, not the terminal half.
- **#687 / PR #711** (merged): cleanup closes a worktree's own Orca terminals before removing a worktree (PR body, removal pipeline "close Orca terminals, check again"); a different path (worktree removal, a person's run), it does not settle coordinator workers. Complementary, no overlap.
- **#507 / PR #508** (merged): coordinators apply `--unattended`; no bearing on terminals.
- **#796, #798, #804, #806, #809** (closed 2026-11-24): none concerns this item; #796/#804/#809 are rejected R38 architecture, so C19 is not in that group.
- **PR #539** (merged): the read-only sweep and WC-16; it reads terminal states but never releases.
- **PR #591 / #584 / #707 / #729 / #735 / #736** (merged): the coordinator duties and R38 baseline; none adds a terminal rule.
- **#444** (closed not planned): sub-orchestrator evaluation; no bearing.

## Updated recommendation

**Keep open with changes, P2, simple, size S. Unchanged from round 1 on action, priority, complexity and size; one change of timing.**
Changes: (1) the done-when must also fail on `release_unknown` (the only state that exits 1) and treat `release_pending` as not yet settled, not only `reclaimable`; a retained terminal needs the written reason (`worker-retain`). (2) Replace the evidence line SPEC:762 with `WORKER-CONTRACT.md:94` and keep the name-clash warning against `release-worker` (`cli.py:201`). (3) State that release comes after the Task is completed and the result admitted, before any hand-back round (#799), and never on silence (`:183-191`). (4) Pass `--run <id>` to `worker-list` explicitly (unbound it covers every Run). (5) Write the duty in the same ordered finish list as #771. New in round 2: the first build can be a contract rule plus a pinned test (as `:94` already is), so it does not have to wait for the coordinator skill skeleton; the executable fixture check follows once a coordinator step exists. Risk to keep: closing a terminal can send the Task back to `ready` (owner memory note `orca-coordinator-rebind-after-resume.md`, not re-tested; UNVERIFIED on this host).

## Scan record

- Lists read in full: open-issues.tsv 134 of 134 lines, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Search terms: release, retain, terminal, settle, worker, reclaimable, finish, end of worker, closeout, worktree, Run, sweep, return contract, lifecycle.
- Opened in full (read-only `gh`): open issues #716, #771, #788, #799, #801, #792, #786, #784, #755, #787 (10) and #766/#590 by list title only; closed issues #668, #687, #507, #796, #798, #804, #806, #809, #444 (9); merged PRs #683, #711, #539, #591, #584, #707, #729, #735, #736 (9).
- Live reads: Orca `worker-release`, `worker-retain`, `worker-list` help (read-only help calls). UNVERIFIED: any real release run (none was made); whether `worker-release` refuses an unsettled worker; whether claim-agent terminals appear in `worker-list`.
