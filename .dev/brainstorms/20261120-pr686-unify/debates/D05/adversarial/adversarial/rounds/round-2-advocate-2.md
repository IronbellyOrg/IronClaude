# Round 2, Advocate 2 (Variant 2 = CLAY), D05 launch guard for started workers

Written 2026-11-20, read-only. Short names as before: "the guard" is `launch-level-guard.sh`; "D:nnn" is a line of `docs/designs/orchestrator.md` and "LD:nnn" a line of `docs/designs/sc-issue-launch-level-hook.md`, both in `/home/coder/.cache/ic-snap-20261120/master`. "G2" is `docs/designs/issue-pipeline-guard-g2.md` there. "FS" is the guard level that allows commit, push of a feature branch and PR creation. Numbers below follow the seven responses of `round-2-advocate-1.md`. I re-read the source for every citation I rely on. In this file the owner means the repository owner `ironbelly`, who wrote G2; "Clay" is the account `clayphi`.

Bottom line first. OURS wins the central question (the guard is required for orchestrator-started workers), staged behind a live probe. I could not find any CLAY benefit that is both evidenced and tied to the guard-less rule. CLAY keeps real, separable wins (controls that bind the orchestrator, a friction map, a fallback control, a limit on what the guard covers).

## Response to the OURS rebuttal

1. **Collisions 1 and 2 and the session-id problem (their response 1). Conceded; my Round 1 point was wrong for level FS.**
   - Verified in the guard: the `.ok` file is read only when the level is `W` (`launch-level-guard.sh:270`), and the release that writes it runs only at `W` (the comment in the block at about `:341-361`: "only at worktree ..., never at full or full-submit"). The grid row for a typed `approved` or `/sc:implement` says "A, no write" at FS (LD grid row 34). G2 section 1 itself scopes both collisions to "the plan-writing worker" of the Plan B handoff. So facts 1 and 4 of G2 (session id, forged `.ok`) are not needed for an FS worker.
   - Collision 1 is also closed: rule 2 is in the guard (`:485-520`) and tests use real preamble shapes (`tests/hooks/test_launch_level_guard_worker.py:32,36,66,67`: `send --from term_1d62 --type heartbeat`, `ask --from ...`, `send --type worker_done`). `WORKER-CONTRACT.md:66` already writes "Messages carry no `--to` ... the launch-level guard blocks any `--to` from a bound worker". The contract was written for a bound worker. I withdraw "G2 collisions block binding".
   - What this changes: C-002 loses its strongest leg. What stays is only the unobserved delivery (G2 facts 2 and 3 live, FU-1 precondition f), which is a probe, not a block. The hook tests use synthetic envelopes, so "tests pass" is not "live".
2. **Citation slip. Conceded**, no effect.
3. **Fail-open on identity loss; fail-closed first prompt; pending-file receipt (their response 3). Mostly conceded.**
   - Verified in `:366-384`: a prompt with a strict marker sets governed, denies with LL-NOBIND when the session id is missing (`[ -n "$LL_SID" ] || ll_deny LL-NOBIND`), and denies unless a regular `sessions/<sid>` file exists after the rename. So a marker that reaches the hook cannot silently leave the worker unbound. The fail-open of LD (identity loss) applies only when no marker reached the hook.
   - Their receipt test (`pending/<nonce>` gone after the first turn) is sound for the case I worried about, a marker that never reaches the hook, and needs no session id. Two additions. (a) Pair it with the D:975 listing of `sessions/` so the receipt proves the right session. (b) A worker whose first prompt is denied never starts a turn, so the check must run on a timeout ("no heartbeat in N minutes, then read `pending/` and the screen"), not only "after the first turn". Their text leaves N unset.
   - Evidence in their favor that they did not use: the strict marker is accepted "anywhere" in the prompt (LD binding paragraph), so Orca's preamble in front of the brief does not break binding; and the claim path already delivers its marker with `orca agent launch ... --prompt` (`orca_worktree.py:1777-1778`), which produced bound sessions in the 442 runs. That narrows the unknown to "does `worker-start` deliver the task the same way". It does not remove it.
   - One failure mode to test: a prompt that begins `[sc-launch:` with a missing or used nonce is bound as `degraded`, which reads as level `W` (`:268-271`, B12). That worker is blocked from implement and commit and never reaches FS. It is loud (a block message), but it is not "bound at FS".
4. **U42 and K22 (their response 4). Conceded.** The guard blocks MERGE at every level (LD grid), so it cannot bind the orchestrator, and OB-CTX is precedent for session-scoped hooks, not an answer to K22. C-010 stays SPLIT.
5. **pr-submit friction at FS (their response 5). Partly conceded, partly countered with a new finding.**
   - Conceded: the `gh api` writes of replies and resolves sit in scripts (`reply-resolve-thread.sh:131,141`); the refs show the inline forms as "the contract of the script" (`refs/thread-reply.md:5-6`). The merge cycle is off by default (`--conflict-max-tier` default 0, `SKILL.md:240`; the one inline `git ... merge` is `refs/conflict-mechanical.md` step 4), and the design never passes the flag. My Round 1 reading of the whole cycle was too wide.
   - Countered: two pr-submit steps are model-typed inline `gh api --method POST ... issues/<N>/comments`, not script calls. The "single summary thread" (T-642, `summary_posted` in the contract, `SKILL.md:268`) and the fallback follow-up comment are specified at `refs/thread-reply.md:87-89` and `:93-100`; no script posts them (`retrigger-review.sh:56` posts only a re-trigger body). The guard classes any `gh api` with a method, a field, quotes or variables as GHWRITE at every level (`:554` accepts only plain tokens; the block text at `:67-69` names `gh pr comment` as the route instead). So at FS those two steps are blocked as written, and the worker must improvise with `gh pr comment` (class SUBMIT, allowed at FS). Small, fixable, and not seen by either paper; it is exactly the kind of mismatch a live run would find. Not a veto.
6. **Selective reading of the 442 evidence and R33 (their response 6). Conceded.** `GOVERNED_LEVELS_ALLOWED = False` (`launch.py:48`) gates the watcher's claim launches. It does not forbid binding a `worker-start` worker. I accept their reading: the gate's reasoning applies by analogy and supports staging, nothing more. I also checked #678 (open issue: a bare nested `claude "<prompt>"` runs a turn outside the limits). Its own text says the owner decided on 2026-11-19 that the risk is parked and no gate depends on it. I should not have counted OB-H1 item 8 against binding.
7. **Who is "the owner" in D:3 and D:1152 (their response 7). Conceded; this decides C-007.**
   - The analyst map (`H-design681-map.md`) shows ruling 3, the design approval, #655 (the orchestrator design issue) and #681 (the PR that merged it) all came from `clayphi`; `ironbelly` left nothing on them. D:1152 does say, in the OD1 cell itself, "The worker runs with no launch-level guard". But D:1397 (the ruling 3 row) says only "workers push and open pull requests, never merge or force-push", and D:970 and D:975 keep it open ("settled before the first real issue"; option B still named).
   - A literal point for CLAY that I do not rely on: G2:9 says "this worker" and "the flow" of the Plan B handoff, and #682 (Clay's PR that deleted the issue-pipeline package) removed that flow. But D:117 itself calls the DQ7 condition "the same condition" as G1, so Clay tied the two. The literal escape does not hold up.
   - Their claim that nothing of Clay's stops a direct push to `master`: **conceded in full.** I re-read D:801-828: the audit is `--pr <N>`; `refuse(argv)` binds the orchestrator's verbs (K22, D:1244); the merge gate acts on the orchestrator's merge (D:118). No CLAY control acts on a worker's `git push origin master`. The repository holds no push-time control of its own either: `.claude/settings.json` registers only two unrelated hooks.

## Test of the nine-point resolution

Their file holds eight numbered points, not nine; I test those eight.

| # | Point | Clear and testable? | Comment |
|---|---|---|---|
| 1 | The guard-less condition is the owner's open G2 item, not ruling 3 | Clear | A doc check on the OD1 and DQ7 cells and the ruling 3 row. Needs the owner to confirm; that is already the owner order. |
| 2 | Before the second real orchestrated issue every worker is bound at FS | Partly | "Second real issue" is an event, not a switch. R33 used a constant (`GOVERNED_LEVELS_ALLOWED`); this needs the same, for example a refusal in the skill. It also clashes with G2:9 ("before any other issue") unless the first orchestrated issue is declared the one accepted test issue. Say so in the rule. |
| 3 | Preflight before the first worker, fixture with `jq` missing | Clear, but incomplete | `enforcement_preflight` sees only the claim process: its docstring says "The agent Orca starts may run with another one" (`orca_worktree.py:955-960`), and it is Linux only. `cmd_pending` runs no preflight today (their concession). The receipt in point 4 is the real check. |
| 4 | Receipt: `pending/<nonce>` gone, else stop and escalate | Clear | Add the `sessions/` listing and a timeout trigger (see response 3). A fake `worker-start` fixture is easy. |
| 5 | Staging gate on a throwaway issue: receipt, `send` and `ask` with no `--to`, a full `/sc:pr-submit --monitor 3` cycle at FS | Clear, three items short | Add (d) a scripted `git push origin master` on a throwaway repo (442 left the protected push pending because the agent declined, results lines 537 and 550); (e) the summary-thread step of response 5; (f) a bare `git push` and a compound `git add && git commit` (both refused at FS, LD grid rows 13 and 15). |
| 6 | Adopt `refuse(argv)`, the head-pinned merge, audit AU1 to AU8, with a test that the audit is not described as covering a push with no PR | Clear | Fully testable. This is the CLAY win and it needs no guard. |
| 7 | K22 and U42 stay open and graded | Clear | A doc check. |
| 8 | Ruleset on `master` is a separate owner action, recorded with the live value | Not testable | A live value is not a test, and "separate" leaves the strongest control without an owner, a trigger or a date. |

What the resolution still lacks, each a CLAY-side benefit with evidence:
- **A fallback if the probe fails.** If `worker-start` does not deliver the marker as a hook event, point 5 says only "DQ7 keeps unbound". "Required" then binds nothing. The fallback must be named: no real orchestrated issue until a server-side rule protects the branch, or the worker runs in a fork PR flow.
- **The guard's real coverage.** `:720` classes only a push to `master` or `main` as PROTECTED. The orchestrator's repo list carries `default_branch` and `release_head: integration` per repo (D:281-284), and IronClaude's own flow has an `integration` branch. A worker's `git push origin <sha>:integration`, or a push to a default branch named `develop`, is plain PUSH and allowed at FS. The resolution should say what covers those branches.
- **An L2 position.** The question names L2. `launch-level-pre-push.sh` exists on master, is installed only in the claim's launch step, and its refusal path is off (`IR7_REFUSE = False`, `orca_worktree.py:822`). It would catch the leaks the guard pins open (`bash ./push.sh`, LD:122) because it acts on git's own update stream. The resolution is silent on it.
- **What happens to real issues while the gate is open.** Point 2 allows one more unbound real issue. Point 5 keeps K12 at M / H meanwhile. The owner must be asked that in so many words.

## Updated assessment of Variant 1

Stronger than I credited in Round 1. The collisions do not apply at FS; first-prompt binding fails closed when a marker arrives; binding leaves a testable receipt; rule 2 is already in the guard and tested with Orca's own preamble shapes; the worker contract already assumes a bound worker (`WORKER-CONTRACT.md:66`); the claim path's marker delivery is live-observed. They conceded the right things (X-001, X-003, C-002 in part, U-006) and corrected a CLAY error in a way I verified.

Still weak: the guard covers only `master` and `main`, a name filter and not a protection; L1 leaks are open and L2 is not part of the resolution; the preflight cannot see the worker's `HOME`; "bound at FS" has never been observed for a `worker-start` worker; the marker slot was deleted with `brief.py` (they conceded); one pr-submit step is blocked at FS as written.

## New evidence

All read this round in the snapshot or the live repository. UNVERIFIED marks what I could not run.
1. `launch-level-guard.sh:720`: PROTECTED is only `master` or `main`. D:281-284: repos carry their own `default_branch` and `release_head`.
2. `refs/thread-reply.md:87-89` and `:93-100`: the summary thread and the fallback follow-up are model-typed `gh api --method POST .../issues/<N>/comments`. No script posts them. Guard `:67-69` and `:554`: such a call is GHWRITE at every level and the guard's remedy is `gh pr comment`. Read, not run live.
3. `WORKER-CONTRACT.md:66` and `tests/hooks/test_launch_level_guard_worker.py:32,36,66-67`: bound-worker verbs are already specified and hook-tested. Favors OURS.
4. `orca_worktree.py:955-960`: the preflight sees only the claim process's `HOME`, `PATH` and settings. `:822`: `IR7_REFUSE = False`, so L2 is advisory.
5. `launch-level-guard.sh:268-271` with B12: a loose marker with no usable nonce binds as `degraded`, which reads as `W`.
6. `#678` (bare nested `claude` runs outside the limits) is parked by the owner's 2026-11-19 decision and is not a gate (`gh issue view 678`). Favors OURS on C-003.
7. `.claude/settings.json` in the snapshot has no push-time or merge-time control. Favors OURS on C-005.
8. UNVERIFIED: whether `worker-start` delivers the task as a hook-visible first prompt; whether the orchestrator's host is Linux (the governed path needs it); whether a ruleset can be set by the login that runs the orchestrator.

## Concessions

1. C-002: the "G2 collisions block binding" leg is gone (response 1). CLAY keeps only "unobserved".
2. Fail-closed first prompt and the receipt test are sound (response 3).
3. R33 and #678 do not support my reading of the 442 evidence beyond staging (response 6).
4. C-007: the repository owner's G2 sentence governs; Clay's ruling 3 does not undo it (response 7).
5. C-005: no CLAY control stops a worker pushing to `master` (response 7).
6. C-006 is narrower than I wrote (script path works; default cycle has no inline merge).
7. The guard at FS is the same policy as OD1 on paper (C-009). The mapping is unwritten, but the policy is not CLAY's to deny.
8. K12 is graded M / H by Clay himself, with only a prompt holding the worker back. I cannot show that binding costs more than that exposure.

## Updated point positions

| Point | Superior (OURS, CLAY or SPLIT) | Confidence percent | One-line evidence |
|---|---|---|---|
| S-001 | SPLIT | 95 | Same six sections by the brief; no merit difference |
| S-002 | SPLIT | 95 | Same list counts; presentation only |
| C-001 | OURS | 72 | CLAY end state conceded; LD:23 describes today, G2:9 and K12 (M / H) state the rule |
| C-002 | SPLIT | 55 | OURS right that FS needs no `.ok` or session id (`:270`); CLAY right that `worker-start` binding is unobserved and the marker slot is gone |
| C-003 | SPLIT | 62 | PASS blocks real (442 results lines 530-549, 557); item 8 (#678) parked by owner; protected push never exercised |
| C-004 | SPLIT | 55 | R33 gates claim launches only; `--pipeline none` writes no record (LD:349); one fact, two readings |
| C-005 | OURS | 62 | No CLAY control acts on a worker push to `master` (D:801-828, K22); CLAY controls are real and adopted as HYBRID (U-006) |
| C-006 | CLAY | 55 | Summary thread and fallback comment are inline `gh api` POST (`refs/thread-reply.md:87-100`), GHWRITE at FS; reply and resolve are scripts, so narrow; fixable |
| C-007 | OURS | 78 | G2:9 owner text; "owner (Clay)" is `clayphi`; D:1397 ruling 3 omits the guard; D:970 leaves it open |
| C-008 | SPLIT | 62 | Both note `protected: false`; guard covers only `master` and `main` (`:720`), so a ruleset is the broader fix; neither designs it |
| C-009 | OURS | 68 | FS equals OD1 (LD:25-30 versus D:1152); CLAY gives the worker no level; mapping unwritten |
| C-010 | SPLIT | 60 | OB-CTX shows session-scoped hooks; the guard blocks MERGE at all levels and cannot bind the orchestrator |
| X-001 | CLAY | 65 | "Not new code in the hook" true, "whole job" false; OURS conceded (marker slot deleted, no `cmd_pending` preflight) |
| X-002 | OURS | 68 | OB-H2 FAIL rows are verbatim-detail checks (442 results lines 471-472); the refusal matched |
| X-003 | CLAY | 68 | LD:23 and LD:349: coordinator-started worker and `--pipeline none` carry no record; OURS conceded |
| A-001 | SPLIT | 62 | Same user and `HOME` likely (claim sessions bound live); preflight sees only the claim process (`orca_worktree.py:955-960`); the receipt tests it |
| A-002 | SPLIT | 65 | Both lean on a trusted orchestrator; K22 and U42 open for both; write the limit as a graded risk |

## Separable CLAY benefits

Ranked by strength, each independent of whether the guard is required.
1. **Controls that bind the orchestrator (U-006): `refuse(argv)` with a failing test per "may never" pattern (D:767, D:1117), the head-pinned merge `--match-head-commit` with no `--auto`, `--admin` or `--delete-branch` (D:118), audit AU1 to AU8 after each merge (D:801-828).** None exists on master. They cover the orchestrator's own highest-power act, the merge, which the guard cannot cover (it has no level that merges, LD:23, LD:32). This is the strongest CLAY benefit. Adopt it whether or not the guard is required. Nothing in OURS competes with it.
2. **A fallback and a coverage statement.** If the staging probe fails, a server-side rule on the default and release branches is the only control left that also works against a deliberate worker (the guard is "not a sandbox", LD:32, and covers only `master` and `main`, `:720`). The design already reads `protected` per repo (D:118). Ask for a named fallback and list which branches each control covers.
3. **A friction map for FS** with the three added probe items of point 5 and the summary-thread fix (post it with `gh pr comment`, or let `retrigger-review.sh --body` carry it). It turns "friction is a cost" into a written mapping.
4. **Staging itself.** Not making the whole orchestrated flow wait on an unobserved binding is a sound sequencing rule, and OURS adopted it (their point 5). The rule becomes testable only if it is a code switch like R33's constant.

## Any non-separable CLAY benefit

No. I looked for one that should override OURS on the central question and found none.
- "Binding is unproven" is real but separable: it is cured by a probe and a gate before the second real issue, which OURS now proposes.
- "The guard is leaky and not runtime-approved" (LD:6, LD:122; #442 and #685, the PR holding its runbook and results, are open) lowers the value of the guard. It does not give CLAY a control that does the same job: the CLAY controls act on the orchestrator or after a PR, not on a worker's push.
- "The risk is recorded and graded" (K12) is honest, but a graded exposure with only a prompt holding it back is not a benefit under the owner's weighting rule. Clay grades it M / H himself.
- "Cost of binding" is not shown. I found no evidence that FS blocks a step the OD1 worker cannot route around: the one clear mismatch (summary thread) has an allowed workaround.
So under the owner order, where CLAY shows no clear evidenced benefit tied to the contested rule, OURS wins C-001, C-007 and C-009, and the guard (or an equal mechanical control) is required for orchestrator-started workers, staged behind the live probe. CLAY's wins are adopted as a HYBRID next to it. The one open question I cannot close, and that the owner should answer, is point 2 of their resolution: whether one more real orchestrated issue may run unbound while the gate is open.
