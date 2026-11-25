# Verdict D05: Launch guard for started workers

Short names, each defined once. "The guard" is `launch-level-guard.sh` (L1), a hook that blocks a governed agent's commit, push, merge and similar calls. "L2" is `launch-level-pre-push.sh`, the git pre-push hook. "D:nnn" is a line of Clay's `docs/designs/orchestrator.md` on origin/master (snapshot `/home/coder/.cache/ic-snap-20261120/master`); "LD:nnn" is a line of `docs/designs/sc-issue-launch-level-hook.md` in the same snapshot. "FS" is the guard level "full with `--submit`" (commit, push a feature branch, open a pull request; never merge, never push to `master`). "Clay" is the account `clayphi`; "the owner" is the repository owner, the account `ironbelly`. "K12" (D:1234) is Clay's risk row: workers run with no guard and no L2, `master` is unprotected, so only the written prompt holds a worker back (graded M / H, medium likelihood and high impact). "DQ7" (D:117) is Clay's rule that a `worker-start` worker runs without the guard. "G1" is the owner's earlier acceptance of a guard-less worker for the first test issue; "G2" is the guard note `docs/designs/issue-pipeline-guard-g2.md`.

## Question

CLAY DQ7 and K12 (D:117, D:1234) start workers with `worker-start` and no launch-level guard or L2 pre-push hook, with master unprotected. OURS (issues 394, 442, PR 685, R33 `GOVERNED_LEVELS_ALLOWED=False`) assume the guard governs every launch. Which wins, and should the guard be required for orchestrator-started workers? Include guard G2 rule 1 that PR 682 removed.

(Plain gloss of the numbers: issue 394 is the issue that asked for the guard; issue 442 holds the guard's live observations and is still open; PR 685 is the owner's runbook and results for 442 and is still open; R33 is the owner's rule in the unpushed zero-setup requirements that keeps only `--pipeline none` launching; PR 682 is Clay's merged PR that deleted the issue-pipeline package.)

## Winner

HYBRID. OURS wins the central question (the guard is required for orchestrator-started workers, staged behind a live probe), and Clay's orchestrator-side controls are adopted next to it because they do something the guard cannot.

## Winning recommendation

The unified design must say the following, each testable.

1. **The guard is required for every worker the orchestrator starts, staged and not exempted.** Every `worker-start` worker is bound at a named guard level (provisionally FS) before the owner's G1 acceptance is spent; DQ7 changes from "decided: runs unbound" to "required; open owner item G2". Test: a design check that DQ7, OD1 (D:1152) and K12 no longer call the guard-less condition decided, and that no text says "decided by ruling 3" for it.
2. **Binding steps are written down.** The orchestrator runs `orca_worktree.py pending --level full-submit` first (`publish_pending` is at `:1488`, `cmd_pending` at `:1515`), puts `[sc-launch:v1:<nonce>]` in the first prompt (a new line in Clay's `templates/handoff-prompt.md`, D:637, because PR 682 deleted the old marker slot in `brief.py`), runs a preflight before the worker (`cmd_pending` has none today), and after the worker starts checks that `pending/<nonce>` is gone, on a timeout whose value is stated, and stops the worker and escalates if it is not. Tests: a fake `worker-start` whose prompt carries no marker leaves the file and triggers the stop; a fixture with `jq` missing gives a refusal and no worker.
3. **Staging is a code switch, not a sentence.** A constant in the orchestrator skill (same idea as R33's `GOVERNED_LEVELS_ALLOWED`) keeps real issues unbound-and-flagged until a reviewed commit flips it. The first bound worker runs on a throwaway issue and records: the receipt; one `send` and one `ask` with no `--to` reaching the orchestrator (G2 facts 2 and 3); a full `/sc:pr-submit --monitor 3` cycle at FS; a scripted `git push origin master` on a throwaway repo (issue 442 left it pending twice because the agent declined); the summary-thread step; a bare `git push` and a compound `git add && git commit`, both refused at FS. Until it passes, K12 stays M / H.
4. **The design must not claim the guard closes K12.** Binding at FS covers plain pushes to `master` and `main` only. A script run (`bash ./push.sh`), a push to `integration` or another default branch, a new session id, and tools outside the hook matcher pass (invariant probe INV-034, INV-019, INV-003, INV-036). Wording: "mitigates K12 for honest drift on master and main". K12 is re-graded, not closed, until a push-time control outside the worker exists (INV-037).
5. **Adopt Clay's `refuse(argv)`, the head-pinned merge and the audit AU1 to AU8 alongside the guard**, with a test that fails if the design describes the audit as covering a push that has no pull request.
6. **G2 rule 1 stays removed; G2 rule 2 stays.** Rule 1 was a TAMPER class for the coordinator-side `issue-pipeline` verbs that wrote approval rows and the worker's release file (comment lines 441-443 and one `case` line 444 of the guard). PR 682 removed it because those verbs no longer exist; the guard change had an independent review recorded as PASS (E-pr682.md, partly self-reported, see Unverified). Rule 2 (a bound worker may `send` and `ask` only as one plain call with no `--to`) stays, is already tested, and is what an orchestrated bound worker needs. If the owner later restores any coordinator-side verb that writes an approval or release file, a TAMPER class for it must come back; the old text is readable with `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:src/superclaude/hooks/scripts/launch-level-guard.sh`.

## Strongest points

OURS:
1. The owner's acceptance was for one issue only. G2 (`issue-pipeline-guard-g2.md:9`): "for the one first test issue the owner accepted that this worker runs without the launch-level guard (G1)" and "Before any other issue runs through the flow, the worker must be bound to the guard (G2)". DQ7 (D:117) cites G1 as precedent for a standing rule. Debate: C-007, OURS 78%, both advocates agree.
2. Level FS is Clay's own policy for the worker, enforced mechanically. OD1 (D:1152): the worker "pushes its own feature branch and opens its pull request ... never merges and never force pushes". The guard grid refuses `--force` and non-plain pushes (LD:113), a push to `master` or `main` (LD:114) and any merge (LD:115), and allows FS exactly the rest (LD:25-30). Live PASS evidence from issue 442 (`observation-results.md` in worktree `issue-442-runbook`): implement blocked (line 530), four commit blocks (531, 535, 536), merge blocked (549), OB-CTX telling governed, ordinary and human sessions apart (553-563).
3. No CLAY control acts on a worker's direct push to `master`. The audit is `superclaude orchestrator audit --repo <R> --pr <N>` (D:801-828), the merge gate acts on the orchestrator's merge (D:118), and `refuse(argv)` "binds the verbs, not a command the model types itself" (K22, D:1244). The CLAY advocate conceded this in full (rounds/round-2-advocate-2.md, response 7).

CLAY:
1. Binding a `worker-start` worker has never been observed, and "one marker line" was overstated. G2 facts 1 to 4 are UNVERIFIED (`issue-pipeline-guard-g2.md:40-43`); PR 682 deleted the place the marker lived (`brief.py` function `build`, `templates/worker-brief.txt` section `[marker]`); `cmd_pending` runs no preflight (the launch path does, `orca_worktree.py:1726`). Debate: C-002, X-001 (CLAY 67%).
2. Orchestrator-side controls exist nowhere on master and cover what the guard cannot: `refuse(argv)` with a failing test per pattern (D:767, D:1117), a merge pinned with `--match-head-commit` and never `--auto`, `--admin` or `--delete-branch` (D:118), the audit AU1 to AU8 (D:801-828). The guard has no level that merges ("no level authorizes a merge", LD:32), so it cannot bind the orchestrator. Debate: U-006, adopted by both advocates.
3. "The guard governs every launch" is a rule, not the state of master. LD:23: a coordinator-started worker "is not launched by the claim script, so this guard does not govern it"; IR-1 (LD:349): nothing is written for `--pipeline none`. Plus real friction: `/sc:pr-submit`'s summary-thread and fallback comments are model-typed inline `gh api --method POST` calls (`refs/thread-reply.md:87-100`), blocked as GHWRITE at FS (LD:116), while its reply and resolve scripts pass only through a pinned leak (LD:122). Debate: X-003 (CLAY 69%), C-006.

## Clay strengths to adopt

- **The orchestrator-side controls (`refuse(argv)`, head-pinned merge, audit AU1 to AU8).** Why: a capability OURS lacks (nothing equivalent on master, H-design681-map.md rows 5.9 and 5.11, cited in the CLAY paper) and the only controls that bear on the orchestrator's own highest-power act, the merge. How to merge: add them beside the guard and do not tie them to the guard being absent; keep the limits stated (they do not stop a worker's push; K22 and U42 stay open and graded). Who may merge at all is decided in D06, not here: the head-pinned merge is a safeguard for whoever merges.
- **The honest K12 risk row and the live-test record of what a worker can reach (D:975, D:1234).** Why: it states the exposure with a grade and a mitigation. How to merge: keep K12 and keep the live test, but flip its expected result from "worker is unbound" to "worker is bound, `pending/<nonce>` gone", and list the worker's sessions with an inode match (the plain before-and-after `ls` cannot say whose file is new when three workers start in one cycle, INV-006, INV-002).
- **The friction map for FS.** Why: a verified mismatch neither paper had at the start (the summary-thread and fallback comments). How to merge: add it to the staging probe; the route is `gh pr comment` (class SUBMIT, allowed at FS) or `retrigger-review.sh --body`; the default `--monitor 3` cycle has no inline merge (`--conflict-max-tier` defaults to 0, `SKILL.md:240`).

## Our strengths that must be kept

- The guard L1 as built, including G2 rule 2 and the rule that unbound sessions are never blocked (LD:81, LD:206), so requiring it cannot break the orchestrator's session or a person's.
- The owner's G2 condition "Before any other issue runs through the flow, the worker must be bound", and the ship-gate principle behind R33: no governed launch on a real issue until it is observed (the guard's own status line, LD:6, LD:17).
- The mapping of FS onto OD1 (to be written down), and the live observation program of issue 442 (OB-H1, OB-H2, OB-H3, OB-CTX), with issue 678 (a bare nested `claude "<prompt>"` runs outside the limits) kept parked by the owner's 2026-11-19 decision.
- `WORKER-CONTRACT.md:66` ("Messages carry no `--to`") and the tests for it.
- The L2 design (`launch-level-pre-push.sh`), even though it is not installed for these workers today.

## Actions

| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Decide when binding starts: is the first orchestrated issue the one G1 test issue, or does "before any other issue" bind from the first; may one more real issue run unbound while the gate is open | DECISION | Owner (`ironbelly`), in chat | 1, first; everything below waits on it |
| Rewrite DQ7, the OD1 guard-less clause and K12 as "required, staged, K12 stays M / H"; stop calling the guard-less condition decided by ruling 3 (ruling 3's row, D:1397, omits the guard; D:970 and D:975 leave binding open); reconcile the three gates (guard status line, R33 constant, staging gate; INV-027) | DOC | `docs/designs/orchestrator.md` (D:117, D:970, D:975, D:1152, D:1234, D:1397) | 2, after action 1 |
| Add the marker line to `templates/handoff-prompt.md`, the `pending --level full-submit` step, the preflight in `cmd_pending` (or a call to the existing preflight), the receipt check with a timeout, and their tests | LOCAL CHANGE | PR B (the orchestrator skill pull request, not yet built) and `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` | 3, after action 2 |
| Re-home the staging switch: PR 686 has no `GOVERNED_LEVELS_ALLOWED` (checked in snapshot `pr-a`), the poll no longer launches workers, and R33 exists only in the owner's unpushed branch, so put the constant in the orchestrator skill | LOCAL CHANGE | PR B; owner's `claim-handoff-planb` plan (R33) | 3, with the item above |
| Run the staging probe on a throwaway issue and close issue 442's pending rows (protected push, `/sc:pr-submit --monitor 3` at FS) | LOCAL CHANGE (live test) | issue 442, PR 685 | 4, before any real orchestrated issue |
| Merge the owner's runbook and results PR | PR KEEP | PR 685 | independent; it is evidence for action 4 |
| Keep the guard edit of PR 682 (rule 1 removed, rule 2 kept) | PR KEEP | PR 682 (already merged) | none; revisit only if a coordinator-side approval verb returns |
| Adopt `refuse(argv)`, the head-pinned merge and the audit AU1 to AU8 with the "no push without a pull request" test | PR KEEP-ADAPT | Design sections 5.9, 5.11, DQ8; PR B | independent of the guard; merge authority is D06's decision |
| Server-side rule on `master` and `integration` (branch protection or a ruleset): the only control that closes K12 and works against a deliberate worker. This is an outward GitHub change; this debate only recommends it | DECISION | GitHub repo settings of `IronbellyOrg/IronClaude` (owner has admin; `protected` is `false` today) | parallel with 1; K12 stays M / H until done |
| Decide the L2 position (install it for `worker-start` worktrees, or not) and what covers branches other than `master` and `main` | DECISION | Owner; `orca_worktree.py:1754` (`install_l2` only in `cmd_launch`), `launch-level-guard.sh:720` | after the probe, because L2's refusal path is off (`IR7_REFUSE = False`, `orca_worktree.py:822`) and its classing of a `worker-start` worker is unverified |
| Write the FS-to-OD1 mapping and the friction map (summary thread via `gh pr comment`; compound pushes in split form) | DOC | New design note under `docs/designs/` | with action 3 |

## Implications

- **Orchestrator (PR B).** It cannot start a worker with a plain Task spec any more: the spec needs the marker line and the orchestrator needs the `pending` step, a preflight and a receipt check. The worker contract section ADD1 (D:135) must say the worker runs bound. The live test in D:975 changes meaning.
- **Watcher and claim pipeline.** R33's `GOVERNED_LEVELS_ALLOWED` has no counterpart in PR 686 (the watcher wakes the orchestrator and no longer launches workers), so the owner's staging switch must move to the orchestrator skill. A `--pipeline none` claim writes no launch record (IR-1, LD:349) and any worker started after it is unbound unless the bind step runs; `/sc:issue` text and LD:23 still describe the old scope. If D04 settles on the watcher choosing governed launch levels, R33 stays relevant on that path.
- **Dashboard and report.** Guard denials print only to the worker's stderr and leave no record (INV-028); nothing in the audit sees repeated blocked attempts. A dashboard that wants "blocked by guard" events needs a denial log, which does not exist.
- **What breaks or rubs.** The summary-thread step of `/sc:pr-submit` at FS; any compound push or commit (`LL-PUSH-FORM`); a branch name with `+`, `@` or `#`; text that names git together with push, merge or pull inside a message (`LL-TEXT`). The guard also fails closed for a bound worker if `jq` is missing, and a bound session's Bash calls pass the job-identity hook, whose behaviour for `worker-start` terminals is unobserved (INV-023).
- **What the owner must know.** (1) "The owner (Clay)" in D:3 and "owner" in D:1152 mean the account `clayphi`; ruling 3 is Clay's and does not undo the G2 sentence written by the owner in PR 591 (the Plan B PR). (2) Binding does not close K12: only a server-side rule does, and nobody owns that action. (3) The first orchestrated issue runs unbound unless the owner says otherwise in action 1. (4) The guard protects only `master` and `main`; `integration` is open at FS. (5) Seven HIGH invariant findings were left unaddressed by the debate (listed in Unverified and in `adversarial/invariant-probe.md`); they are carried as stated limits, not resolved.

## Confidence

78 percent that HYBRID is right and the central answer (guard required, staged) is right. Both advocates reached it independently after rebuttal, and the CLAY advocate conceded the end state. Lower, about 60 percent, on the staging details (timeout, the deadline wording, the L2 choice). What would change it: (a) if ruling 3 turns out to be the repository owner's own decision, C-007 flips to CLAY and the winner becomes CLAY on timing; (b) if a live probe shows `worker-start` cannot deliver the marker as a hook event, "required" binds nothing and the fallback (no real orchestrated issue until a server-side rule exists) becomes the main rule; (c) if the owner sets a server-side rule on `master` and `integration`, K12 closes by that route and the guard becomes a second layer, not the decisive one.

## Unverified

- That `worker-start` delivers the task as a first prompt that fires a `UserPromptSubmit` event, with the marker intact (FU-1 precondition f, never tried); G2 facts 1 to 4 (`issue-pipeline-guard-g2.md:40-43`).
- Whether Claude Code issues a new session id on `/clear` or resume (INV-003); whether a hook killed by its 5 second limit lets the call run (INV-011); the worker's `HOME`, `PATH`, MCP tool set and host operating system (INV-012, INV-036).
- Whether L2 would classify a `worker-start` worker as governed (`launch-level-pre-push.sh`, job records created by a bound Bash hook).
- The contents of `RULINGS.md` (Clay's rulings 1 to 39, not read by any analyst or advocate); who "GeneralIronFlow" is; whether the owner has seen ruling 3 outside GitHub.
- H-design681-map.md rows 5.9 and 5.11 and E-pr682.md (the independent review of the PR 682 guard change) were cited, and partly self-reported; the CLAY advocate did not open them.
- `launch.py:48` (R33's constant) is in the owner's worktree `claim-handoff-planb`, not in the snapshot; the invariant probe could not read it, the two advocates and this verdict's author read it there.
- Which issue the G1 acceptance meant; FU-1 step f already ran an unbound worker on 2026-11-17 (`issue-pipeline-fu1.md:113`).
- Whether the login that runs the orchestrator can create a ruleset (classic protection answers 404 for `maintain`, D:118).
- The 7 HIGH invariant findings left unaddressed by the debate (depth standard has no Round 3): INV-003 (binding keyed on one session id), INV-015 ("second real issue" cannot be counted), INV-019 (only `master` and `main` are protected), INV-027 (three gates disagree), INV-034 (a script run passes every gate), INV-035 (so FS alone does not close K12), INV-037 (K12 closes only with a control outside the worker). Twelve MEDIUM findings are listed in the merged output, Open items, item 12.
- Two factual slips in the position papers were corrected before the debate (OURS "three" commit blocks became four; CLAY's "FS not observed" was narrowed to the `/sc:pr-submit --monitor 3` cycle). The OURS paper still swaps the line numbers of `cmd_pending` and `publish_pending`; the merged output has them right.

## Debate artifacts

All under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D05/`:

- Position papers: `position-OURS.md`, `position-CLAY.md`
- Adversarial output folder: `adversarial/` with `merged-output.md`, `return-contract.yaml` (worker contract, status partial), `adversarial/return-contract.yaml` (the skill's own contract, status partial, convergence 0.824, base variant 2)
- `adversarial/adversarial/variant-1-original.md`, `variant-2-original.md`, `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`
- `adversarial/adversarial/rounds/round-1-advocate-1.md`, `round-1-advocate-2.md`, `round-2-advocate-1.md`, `round-2-advocate-2.md`, `qual-pass-1.md`, `qual-pass-2.md`
- `adversarial/adversarial/scripts/quant.py`, `qualcompare.py`
- The skill ran fully (Skill tool and nested agents were available): 2 advocates, 2 rebuttals, 1 fault-finder, 2 scoring evaluators, 1 merge executor. No `BLOCKED.md` was needed.
