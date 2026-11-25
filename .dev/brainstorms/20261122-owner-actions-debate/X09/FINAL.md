# X09 (OA-19) Switching the issue watcher on, repository by repository: FINAL

Reconciler of agents A (pragmatic) and B (risk-first), three rounds. Read on origin/master 2ea524514 (PR 707) on 2026-11-22. Every verdict here is a recommendation until the owner says so in chat. Hour figures are estimates.
Terms: "watcher" = the poll that finds issues assigned to the launch login. "once" = one poll of one repo. "run-all" = one sweep over every Orca repo. "first_run" = the six setup checks a new config gets. "gate PR" = plan stage S9 (a new key `auto_enable` ships false). "L1" = one claim launched by hand before any enabled cycle. "S17" = the plan's live-test stage.

## 1 Unified proposal
First throwaway repository: IronbellyOrg/orchestrator-sandbox (private). Not IronClaude (public, the real backlog), not Coder (real infrastructure). IronClaude comes last, with its own go. Leave sandbox issue 1 alone (assigned to clayphi); make new test issues. Approver is clayphi (or IB-JonathanB if the owner names them); never the shared ironbelly login.
Phase R, rehearsal (starts now; no code change, no cron line, no real `run-all`, `enabled: false` throughout):
- R0 agent, read only, no go: `uv run pytest tests/issue_watch -q` green; `GOVERNED_LEVELS_ALLOWED` False; no cron line; sandbox private; `Approved` issue field exists; Orca knows the sandbox.
- R1 owner go 1 (section 7). Agent makes the Project, the trigger label, three test issues and one Orca worktree with an agent. It hand-writes the config (`enabled: false`, `claim_by: poll`, approvers file with the approver only, ironbelly in `approval_excluded_ids`) and runs `check-config`, `init-state`, the lock test and the restart test (setup doc 8.2, 8.3). It does NOT run `first_run` yet: on today's code a pass writes `enabled: true`.
- R2 shadow, 24 hours: `once --dry-run` every 5 minutes under `flock -n` and a clean environment, plus one `run-all --dry-run` at start and end. Pass: zero `cycle_crashed`; every tick exits 0 or gives a named skip; sandbox `dispatch.json` hash unchanged; zero launches; every gap over 15 minutes explained; the four decisions seen (right approver would launch, wrong approver `not_approved`, ironbelly approving `not_approved`, edit after approval `edited_after_approval`); no config for any other repo.
- R3 timed off drills: `DISABLED` gives `disabled`; `enabled: false` gives `not_enabled`.
- R4 L1 by hand (setup doc 14.1), after a fresh read of `docs/designs/issue-pipeline-fu1.md` section 6: one `orca agent launch` of `/sc:issue --claim N` at Pipeline None into the sandbox worktree; save captures; replace the `_assumed_shape` fixtures; write the live-test record; the same run is the X-001 check (claim agent and standing coordinator share one worktree) at four points. Needs owner go 2 naming issue N.
Phase S17 entry, all must hold: gate PR merged through `/sc:pr-submit --monitor 3` plus the owner's merge go (`auto_enable` false; `first_run` writes no `enabled: true` and no label while false; `run-all --dry-run` generates nothing; a global kill file checked before `run-all` lists repos; tests named at SPEC S9); Coder 515 built (cron line, one daemon); Coder 516 built or waived for the sandbox (section 9); R2 to R4 re-run only where the gate PR changed the code they touch (agent lists the changed files in the record); `GOVERNED_LEVELS_ALLOWED` still False; exactly one issue carries the trigger label, listed in chat before the flip.
- S1 cron shadow, 24 hours: real cron `run-all --dry-run` plus the `once --dry-run` loop; the six `first_run` checks green on the sandbox with the config still off; same pass rule as R2.
- S2 owner go 3. Agent sets `enabled: true`; the approver sets Approved; one cycle runs; the moment `launched` shows the agent touches `DISABLED`, sets `enabled: false`, and writes the go/no-go record (code head, host, hashes, captures, passed and failed probes). A second issue needs a new go.
- S3 stop. Turning `auto_enable` on and enabling IronClaude are later, separate gos (OA-28a). No agent runs a real `run-all` before the gate PR merges, and the gate PR merges before Coder 516 lands.
Switch off, fastest first: touch `~/.local/state/superclaude/issue-watch/<repo>/DISABLED` (checked before any GitHub call; stops new starts only; a started claim session is closed by hand in Orca); set `"enabled": false` (lasting); the global kill file once built; remove the cron line last (not lasting after Coder 515, which recreates it each boot).

## 2 Context
OA-19 is the owner's go for each repository. The plan says every repository ships off, but master does not enforce that (section 10). Today only a missing `Coordinator` worktree stops other repos from switching themselves on.

## 3 Implications
Changes: three separate gos, each naming one action; a small gate PR (S9) comes before any enabled cycle; the sandbox gets a Project, a label and test issues. Stays blocked: IronClaude, `auto_enable`, any level above Pipeline None (ship gate closed), a second polling host, `claim_by: coordinator`. Coder 515 and 516 are on hold at Clay's request until the issue 655 design comparison, so S2 has no date.

## 4 Benefits
The first real claim, kill switch and cron environment are proved where failure is harmless (private repo, closed ship gate: worst case is an assignment and comments). It yields the first real captures to replace guessed fixtures. One live record is taken on the final code.

## 5 Risks (and containment)
- A slip (a real `run-all` on old code) enables other repos: no real `run-all` until the gate PR merges; pre-gate shadow runs use `--dry-run` only.
- Shared login ironbelly: an agent could approve its own issue: approver is clayphi; the generator already drops ironbelly.
- Public repo later: issue text is agent input in a session with permission checks off; the launch guard reads command text only and master is unprotected (SPEC RK-2). Gates: exact assignee, trigger label, non-launch approver, edit-after-approval void; none tested in public. Hand-write IronClaude's approvers file because generation adds every maintainer. Claim comments and the new label are public and could show host paths (UNVERIFIED).
- Caps: 1 launch per cycle, 6 per day per repo; `claim_by` and `max_in_flight` are not built, so "one issue" is procedure (one labeled issue, `DISABLED` on first `launched`).
- One shared GitHub rate limit: about 24 calls an hour idle (agent A's figure, not re-measured).
- The gate PR could miss an enabling path: pass list includes its four named tests.

## 6 Costs (estimates)
Basis: about 12 setup-doc commands, four X-001 points, one record. Phase R about 4 hours of attention over 2 days plus 24 hours wall clock. S17 about 3 hours plus 24 hours wall clock. Gate PR: 3 to 5 hours of agent time (agent B's estimate; includes the kill file, 1 to 2 hours), counted under S9, not here. Coder 515 and 516 are outside this cost.

## 7 The sentence the owner says in chat
Now (go 1): "Go: set up IronbellyOrg/orchestrator-sandbox only for the watcher rehearsal: a Project, the trigger label, three new test issues, one Orca worktree with an agent. Every repository stays off; no cron line and no real run-all until the gate pull request is merged."
Later: go 2 "Go: run one claim by hand on sandbox issue N; the launch-level guard is off for that one issue." Go 3 "Go: switch on orchestrator-sandbox only, for issue N, then switch it off." Stop: "Stop the watcher."

## 8 What an agent does after it
Records the go in the ledger, runs R0 then R1 to R4 in order, posts nothing to Coder 515 or 516 until the owner says go, and reports each pass list. After the gate PR merges, it asks for the Coder 515 go and the merge go. On "Stop the watcher" it touches every `DISABLED`, sets every `enabled: false`, and shows each `disabled` or `not_enabled` line.

## 9 Consensus: full on method; two owner choices remain
A moved to B's order (gate PR before the flip); both dropped the self-approval fallback and the 95-percent tick rule; both put the global kill file in the gate PR.
- Choice A, Coder 516 before the sandbox flip. My recommendation: waive for the sandbox only, because the sandbox has a hand-made worktree and, once the gate PR merges, the gate (not the missing worktree) is the brake. Consequence of waive: S17 departs from SPEC line 501 and the record says so; the first real claim can come after the gate PR and 515. Consequence of not waiving: S2 waits for 516, which is on hold, so no date.
- Choice B, if clayphi cannot approve. Default: wait. Fallback: remove ironbelly from the exclusion for the sandbox only after the negative drill; the separate-approver path stays untested live and an `approver_is_launch_account` warning is accepted.

## 10 What could not be verified
Verified by me: no `auto_enable` on master; `first_run` writes `enabled: true` on a pass and creates the label (`first_run.py` lines 100-200); `run-all` generates and runs `first_run` for repos with no config (`dispatch.py` 410-428); generated config starts false and drops the launch account (`generate.py`); `GOVERNED_LEVELS_ALLOWED = False` (`launch.py`); no global kill file; `claim_by` not in `src`; live-test doc absent; sandbox PRIVATE; Coder 515 answer of 2026-11-21 and 516 hold comment of 2026-11-20; setup doc 14.1 and SPEC S17 text.
UNVERIFIED: that no cron line or `crontab` exists on this host; that the sandbox has no Project and Orca knows it; the `Approved` field on it; whether clayphi or IB-JonathanB will approve; whether claim comments leak host paths; the exact Orca commands; the 24-calls-an-hour figure; the hour estimates.
