# Round 2, Advocate 1 (Variant 1 = OURS), D05 launch guard for started workers

Written 2026-11-20, read-only. Short names as before: "the guard" is `launch-level-guard.sh`; "D:nnn" is a line of `docs/designs/orchestrator.md` and "LD:nnn" a line of `docs/designs/sc-issue-launch-level-hook.md`, both in `/home/coder/.cache/ic-snap-20261120/master`. "G2" is the note `docs/designs/issue-pipeline-guard-g2.md` in the same snapshot. Numbers below match the "Weaknesses identified in Variant 1" list of Clay's advocate (round-1-advocate-2.md). I re-read the source for every point before answering.

## Response to criticisms

1. **"One marker line plus one pending call" versus G2 collisions 1 and 2 and the session-id problem.** Partly wrong, partly right.
   - Collision 1 (a bound worker cannot run `orchestration send` or `ask`) is closed on master. Rule 2 is in the guard today (`launch-level-guard.sh:485` sends `orchestration send|ask` to a raw-command check, `:503` is the pattern that admits one plain call with no `--to`). PR #682 (Clay's PR that deleted the issue-pipeline package) kept it, and D:1002 says so in Clay's words ("needed ... by every worker if the owner binds orchestrated workers (OD1, option B)").
   - Collision 2 (release needs a typed `/sc:implement`) does not apply at level FS. Does level FS need a release at all? No. The guard reads `.ok` only when the level is `W` (`:270`: `if [ "$LL_LEVEL" = W ] && [ -f "$LL_FILE.ok" ]`). The release code says "only at worktree ..., never at full or full-submit" (`:341-343`). The grid (LD:91-98, rows IMPL and TURN) allows implement at WA, F and FS with no release. So G2 route A, fact 1 (how the coordinator learns the worker's session id) and fact 4 (a `.ok` written by another session) belong to the plan-writing worker held at `W`. They are not needed for an orchestrated implementation worker bound at FS. Clay's advocate is wrong that the session-id problem blocks this.
   - What is still right in the criticism: G2 facts 2 and 3 (send and ask reach the hook with full text; an omitted `--to` reaches the coordinator's Run) are still UNVERIFIED (`issue-pipeline-guard-g2.md:41-42`). And my "one marker line" hid two verified costs. (i) #682 deleted the place the marker lived: `brief.py` function `build` had the `nonce` slot and `worker-brief.txt` the `[marker]` section (`git show 01e7a9e23 --stat` lists both as deleted). The line now has to be added to Clay's new `templates/handoff-prompt.md` (D:637), a new edit and not an existing switch. (ii) `cmd_pending` writes the record with no IR-4 preflight (`orca_worktree.py:1726` comment: the launch path runs the preflight before `publish_pending`; `cmd_pending` does not), so a "required" rule must add a preflight or it binds nothing when `jq` or the hooks are absent. Conceded as a defect in my mechanism text.
2. **Citation slip.** Conceded. I read the file again: `publish_pending` is at `orca_worktree.py:1488` and `cmd_pending` at `:1515`. My paper had them the other way round. The helper exists either way.
3. **Fail-open on identity loss (LD:81).** Half right, and the fix is cheap.
   - Where it is wrong: a worker whose first prompt carries a marker cannot be silently unbound. With a marker and no valid session id the guard denies the prompt (`:367`, `[ -n "$LL_SID" ] || ll_deny LL-NOBIND`), and a failed binding is also a denial (`:384`). The fail-open of LD:81 covers calls with no marker and no binding. So the loud failure is the first prompt, and the orchestrator sees a worker that never started a turn.
   - Where it is right: a marker that never reaches the hook (the first prompt arrives in a way that fires no `UserPromptSubmit` event, or the marker is not in it) leaves the worker silently unbound. FU-1 precondition f was never tried. Nothing in my paper tested for this.
   - The test needs no session id. On a successful bind the guard renames `pending/<nonce>` away (`:373-375`, `mv ... "$LL_TAKE"`). The orchestrator, an ordinary session that can read the store, checks that `pending/<nonce>` is gone after the worker's first turn. If it is still there, the worker is unbound and must be stopped. This extends D:975's probe (`ls sessions/` before and after); it does not replace it. UNVERIFIED that Orca's `worker-start` first prompt fires `UserPromptSubmit`; the probe is how to find out.
4. **U42 and K22 not answered by the guard.** Conceded in scope. The guard blocks MERGE at every level (grid row 17, LD:115) and the orchestrator is the only actor that merges (DQ8, D:118), so the guard cannot bind the orchestrator without a new level. What stands: U42 asks "whether a hook can run `refuse` on the Bash calls of an orchestrator session only (not on every session of the host)". The guard plus the live PASS of OB-CTX in the 442 results (`observation-results.md` lines 553-563: a governed `sleep 241` told from an ordinary `sleep 242` and from a person's terminal in one worktree) is working precedent that a user-level hook can be scoped to chosen sessions. That answers the feasibility half of U42 by precedent. It does not answer K22, and it is not an existing answer for the orchestrator. U-002 shrinks from "already built" to "precedent".
5. **Remedy not shown to fit the OD1 worker end to end.** Right in part. I checked the fit instead of assuming it.
   - `/sc:pr-submit` keeps its `gh api` writes inside scripts (`reply-resolve-thread.sh:131,141`; inline `gh api` appears in the refs only as documentation of what a script does). Scripts pass only through the pinned gap `bash ./push.sh` (LD:122). It works, by a leak, and nobody observed it at FS.
   - The merge cycle of pr-submit runs `git -c ... merge --no-commit --no-ff <base_sha>` inline (`refs/conflict-mechanical.md:77`), which is MERGE and blocked at FS. That cycle is off by default (`--conflict-max-tier` defaults to 0, `SKILL.md:240`) and the design never passes the flag (no match for `conflict-max-tier` in `orchestrator.md`). So the default `--monitor 3` command of ADD1 does not hit it. If the template later raises the flag, the worker stops at the merge.
   - Net: the friction is real but narrower than my paper implied, and the cycle at FS is unobserved. A written FS mapping plus one live run is required before "required" is true.
6. **Selective reading of the 442 evidence.** Partly fair. Line 17 of `observation-results.md` sets a gate for governed claims on real issues, and R33 closes `GOVERNED_LEVELS_ALLOWED = False` (`launch.py:48`) for the claim path. That constant gates the watcher's claim launches at `worktree` and `full`, not a `worker-start` worker. It does not forbid binding an orchestrated worker; its reasoning (no governed launch on a real issue until observed) applies by analogy, so I accept the staging it implies.
7. **OD1 is "Decided" by ruling 3; who is "the owner" in D:3 and D:1152?** This matters most for C-007.
   - D:3 says "approved by the owner (Clay)". The analyst map (`/home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/H-design681-map.md` lines 5-6, 16, 29, 33) shows every ruling, issue #655 (the orchestrator design issue), PR #681 (the PR that merged the design) and the approval came from the account `clayphi` (permission `maintain`). The repository admin `ironbelly` left no comment, review or reaction on them. The G2 sentence "for the one first test issue the owner accepted ... before any other issue ... bound" (`issue-pipeline-guard-g2.md:9`) came in PR #591 (Plan B, by `ironbelly`). So "owner" in D:3 and D:1152 means Clay. Ruling 3 is Clay's and does not undo the repository owner's G2 condition. UNVERIFIED: `RULINGS.md` was not read by the analyst or by me.
   - Even by Clay's ledger, ruling 3 is "workers push and open pull requests, never merge or force-push, only the orchestrator merges" (D:1397). That row does not mention the guard. The guard-less clause sits in the OD1 and DQ7 cells, while D:970 (row 5d) says the guard-less condition is "settled before the first real issue" and D:975 keeps option B open. Clay's design is inconsistent on whether this is closed, and their advocate concedes it (their Concession 3).

## Updated assessment of Variant 2

Clay's advocate was candid and conceded the end state: the guard (or an equal control) should bind an orchestrated worker before the owner's G2 condition lapses (their Position summary, Concessions 1 and 2). That moves the debate from "whether" to "when and how proven". On those terms CLAY has real wins, accepted below: binding has not been observed on a `worker-start` worker, the marker slot was deleted, and the owner's present plan runs only the unguarded launch. Their strengths (controls absent on master, the pr-submit friction check, server-side protection as the only control against a deliberate worker) are sound and separable. Where they stay weak: no CLAY control stops a worker's direct push to `master` (the merge gate and audit act at or after a pull request; `orchestrator audit --pr <N>`, D:801-828), their C-004 and X-003 describe today's state and not the rule, and they show no evidence that binding costs more than the exposure Clay himself grades M / H (K12, D:1234). I re-read the live value just now: `gh api repos/IronbellyOrg/IronClaude/branches/master -q .protected` printed `false`.

## New evidence

All checked this round in the snapshot or the worktrees. UNVERIFIED marks what I could not run.

1. The release step exists only at level W (`launch-level-guard.sh:270`, `:341-361`; grid row 34 in LD: at FS "A, no write"). Level FS needs no `.ok`, no session id and no coordinator write. Read, not run live.
2. Binding is fail-closed at the first prompt (`:366-384`) and leaves a receipt: `pending/<nonce>` is renamed to `sessions/.take-<sid>` (`:373-375`). A check "pending record gone" proves binding without the session id.
3. The marker line has to be written into `templates/handoff-prompt.md` (D:637) because #682 deleted `brief.py` and `worker-brief.txt`. `cmd_pending` has no preflight (`orca_worktree.py:1515`; the preflight is in the launch path, comment at `:1726`).
4. "The owner (Clay)" is the `clayphi` account; the repository admin `ironbelly` wrote the G2 condition (PR #591) and shows no comment on #655 or #681 (H-design681-map.md). Ruling 3's row at D:1397 omits the guard.
5. The OD1 worker's default `/sc:pr-submit --monitor 3` takes no inline merge (`--conflict-max-tier` default 0, `SKILL.md:240`; `refs/conflict-mechanical.md:77` is the only inline `git merge`), and its `gh api` writes live in scripts.
6. R33 gates the watcher's claim launches only (`launch.py:48`); it does not by itself forbid binding a `worker-start` worker.
7. Not verified: whether `worker-start` delivers the first prompt as a `UserPromptSubmit` event (FU-1 precondition f); whether a ruleset on `master` can be created by the owner's login (the design says classic protection answers 404 for `maintain`, D:118; `ironbelly` has admin per the analyst map).

## Concessions

1. X-001: my "one marker line plus one pending call, not new code in the hook" is true of the hook and false of the whole job. Honest wording: small code, unproven effect. The marker slot is gone (a new edit to the handoff template), a preflight is missing, and first-prompt delivery was never observed.
2. X-003 and C-004: "the guard governs every launch" is not true today. LD:23 says a coordinator-started worker is not governed, and IR-1 (LD:349) writes nothing for `--pipeline none`. The owner's line states the rule that should hold; it is not the state of master. CLAY is right on the description.
3. C-002: CLAY wins this point, narrowly. Binding a `worker-start` worker has never been shown (G2 facts 2 and 3, FU-1 f), and my paper counted code lines where it should have counted unknowns. The two G2 collisions are smaller than CLAY said (response 1), not gone.
4. Citation slip on `cmd_pending` and `publish_pending`: conceded (response 2).
5. U42 and K22 are answered only by precedent, not by the guard (response 4). The guard cannot bind the orchestrator.
6. The guard is not runtime-approved, leaks (`bash ./push.sh`), and is no defence against deliberate evasion (LD:6, LD:32, LD:122). Issue #678 (a bare `claude "<prompt>"` runs a turn outside the limits) is open, and so is PR #685 (the runbook and results for issue #442, the guard's live observations).
7. U-006 is a clear, evidenced CLAY gain, separable from the contested rule: `refuse(argv)` with a failing test per pattern (D:767, D:1117), the head-pinned merge (D:118), audit AU1 to AU8 (D:801-828). None exists on master. Adopt it.
8. The friction check C-006 is a fair finding (script leak, unobserved at FS). It becomes a probe, not a veto.

## Updated point positions

| Point | Superior (OURS, CLAY or SPLIT) | Confidence percent | One-line evidence |
|---|---|---|---|
| S-001 | SPLIT | 95 | Same six sections by the brief; no merit difference |
| S-002 | SPLIT | 95 | Same list counts; presentation only |
| C-001 | OURS | 70 | CLAY concedes the end state; LD:23 describes today; G2:9 and K12 (M / H) make the case |
| C-002 | CLAY | 60 | Binding unobserved (G2 facts 2 and 3, FU-1 f); marker slot deleted by #682; collision 2 and the session id do not apply at FS |
| C-003 | SPLIT | 60 | PASS blocks (lines 530-549, 557) and FAILs (267, 353) both true; OB-H2 FAILs are verbatim checks (471-472) |
| C-004 | SPLIT | 55 | R33 gates claim launches only (`launch.py:48`); `--pipeline none` writes no record (LD:349); two readings of one fact |
| C-005 | SPLIT | 65 | CLAY controls are real and absent on master (adopt as HYBRID); none stops a worker push to `master` (audit is per `--pr`) |
| C-006 | SPLIT | 55 | `gh api` writes pass only via script leak (LD:122), unobserved at FS; default `--monitor 3` has no inline merge |
| C-007 | OURS | 78 | G2:9 "before any other issue"; "owner (Clay)" is `clayphi`; D:1397 ruling 3 omits the guard; D:970 leaves it open |
| C-008 | SPLIT | 60 | Both note `protected: false` (re-read: false); a ruleset needs no hook; an owner action, not designed |
| C-009 | OURS | 65 | FS equals OD1 on paper (LD:25-30 versus D:1152); CLAY gives the worker no level; mapping unwritten, cycle unobserved |
| C-010 | SPLIT | 60 | OB-CTX is precedent for session-scoped hooks; the guard blocks MERGE at all levels so cannot bind the orchestrator |
| X-001 | CLAY | 70 | "Not new code in the hook" is true; the whole job has unknowns, a deleted marker slot and no preflight |
| X-002 | OURS | 65 | The FAIL rows are verbatim-detail; the refusal matched (lines 471-472); line 17 still gates governed claims |
| X-003 | CLAY | 70 | LD:23 and LD:349: coordinator-started worker and `--pipeline none` carry no launch record by design |
| A-001 | SPLIT | 60 | Same user and HOME likely (F3 PASS for claim sessions); worker-start delivery unobserved; the pending-file receipt tests it |
| A-002 | SPLIT | 65 | Both lean on a trusted orchestrator; K22 and U42 stay open for both; the limit must be written as a graded risk |

## Proposed resolution

What the rule in the unified design should say (concrete and testable):

1. The guard-less condition of DQ7 is the repository owner's open item G2, not a settled ruling. It stays marked "open, owner decision" and is never described as decided by ruling 3.
2. Before the second real orchestrated issue, every `worker-start` worker is bound at level `FS`: the first prompt carries `[sc-launch:v1:<nonce>]` (a line added to `templates/handoff-prompt.md`) and the orchestrator ran `orca_worktree.py pending --level full-submit` first.
3. A preflight runs before the first worker (jq present, hooks registered, the IR-4 checks the claim already does) and refuses to start a worker on failure. Test: a fixture with `jq` missing gives a refusal and no worker.
4. After the worker's first turn the orchestrator checks that `pending/<nonce>` is gone; if it remains, it stops the worker and escalates. Test: a fake `worker-start` whose prompt carries no marker leaves the file and triggers the stop.
5. Staging gate: the first bound worker runs on a throwaway issue and records (a) the pending-file receipt, (b) one `send` and one `ask` with no `--to` reaching the orchestrator (G2 facts 2 and 3), (c) a full `/sc:pr-submit --monitor 3` cycle at FS. Until it passes, DQ7 keeps "unbound" and K12 stays M / H.
6. Adopt Clay's controls whatever happens to the guard: `refuse(argv)` with a test per pattern, the `--match-head-commit` merge, audit AU1 to AU8. A test fails if the design describes the audit as covering a push with no pull request.
7. K22 and U42 stay open and graded; the guard is cited as precedent for session-scoped hooks, not as the orchestrator's guard.
8. Separate owner action, not part of this design: a ruleset or branch protection on `master` (needs admin; `ironbelly` has it). Record it as an open item with the live value `protected: false`.
