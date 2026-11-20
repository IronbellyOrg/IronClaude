# Adversarial Debate Transcript: single multi-project watcher (V1) vs one watcher per project (V2)

## Metadata
- Depth: standard (Round 1, Round 2, Round 2.5 invariant probe; Round 3 not run)
- Rounds completed: 2 plus the invariant probe
- Convergence: reached on design shape; the invariant probe blocks convergence until its HIGH items are handled (see invariant-probe.md and the merged output)
- Focus: correctness, risk, operability
- Advocates: V1 advocate, V2 advocate (both general-purpose agents). Both verified claims against `src/superclaude/cli/issue_watch/`.

## Round 1: Advocate Statements (condensed; both statements were read in full)

### V1 advocate (single watcher)
- Position: a loop inside the watcher is the least machinery, because R8 already needs one sweeper that sees every repo. The real gain over V2 is one account-level rate stop.
- Steelman of V2: isolation. Lock, kill switch, store and rate pause all sit under `state_dir` (record.py:283, 381-422; cycle.py:748-750), the 240 s budget, one launch per cycle and day cap are per project (cycle.py:34-43), and `status` points at the broken repo.
- Claims: R8 forces a loop; V1 keeps per-repo state_dir, lock and kill switch; a shared rate stop is something V2 cannot get; a fresh `Deadline` per repo (cycle.py:405).
- Weaknesses found in V2: "no change to cycle.py, record.py or github.py" is false (`github.py:37` `REPO`, used at 187, 208, 259; `launch.py:50` `ORIGIN_REPO`, checked at 249); V2's schema objection does not apply to V1; a wrapper loop is V1's loop as subprocesses; the scheduler "skip the rest" behaviour does not exist.
- Concessions: X-001 holds against V1 too; a loop bug reaches every repo; the shared rate stop is new work; wall time grows with repo count.
- Shared assumptions: A-001 REJECT (`github.py:37`, `launch.py:50`); A-002 QUALIFY (a repo with no Project must be skipped and reported); A-003 QUALIFY (five repos at 240 s can reach 20 minutes).

### V2 advocate (one watcher per project)
- Position: V2 is safer and easier to operate (one lock, kill switch, rate pause, deadline and health stamp per repo), and the audited cycle stays untouched. Concedes up front that neither variant works for a second repo without code changes.
- Steelman of V1: a thin `once --all` loop; R8 needs the sweeper anyway; one account-level rate stop; one summary and worst exit code.
- Claims: isolation from the existing structure; a full budget per repo; per-repo health; one-to-one worktree and approvers binding (`_origin_ok`, cycle.py:670); per-repo rollout and rollback.
- Weaknesses found in V1: the shared rate stop is new behaviour and a coupling (one 429 could silence all repos for 3600 s); a loop bug reaches every repo; V1 never specifies a loop cap.
- Concessions: X-001 hits V2 as hard (V2 s4 claim is false); the 20 minute worst case is real; U-001 stands.
- Shared assumptions: A-001 REJECT; A-002 QUALIFY (board overlap unverified); A-003 REJECT (20 minutes exceeds the 5 minute schedule).

## Round 2: Rebuttals (sequential)

### V1 advocate, after reading V2's Round 1
- (a) A hang or exception stalls every later repo: qualify. Every `gh` and `git` call takes a timeout from the `Deadline` (cycle.py:418, 578-585, 716-720); the fix is a child process per repo with a kill timer, "V2's mechanism inside V1's single entry point".
- (b) One 429 silencing all repos: concede in part. The quota is per account so silencing is correct, but the 3600 s clamp is the problem; `github.py:419-430` reads the real retry-after or reset time first.
- (c) Per-repo rollout and rollback: rebut. `DISABLED` is per state_dir (record.py:283, 422).
- (d) No loop cap: concede. States about 240 s per repo and a total of about 270 s, remaining repos skipped and reported.
- Would ship: one scheduled entry, a serial loop with a total cap, a per-repo child process with a kill timer, per-repo config and state_dir, one account-level rate wait. Changes its mind only on a measured case where a repo's `once` run hangs past its `Deadline` and cannot be killed.
- Hidden assumptions raised: `DAY_CAP` is per store (six repos, up to 36 launches a day); the repo field must feed `_origin_ok`; `MAX_LAUNCHES_PER_CYCLE` becomes one per repo unless the loop enforces one global launch; zero repos and a repo with no Project; two repos on one Project board.

### V2 advocate, after reading V1's Round 2
- The converged design is V2 with the loop owned by the watcher entry point: yes, accepted. "It removes the outer-process objection."
- Single account-level rate wait: accept with limits. Keep it in one loop-level file (children do not write each other's stores), and apply it only for the plain `rate_limited` reason, not `rate_limit_clamped`, because a secondary or abuse limit may be per repo and an unreadable header would silence every repo for an hour (github.py:418-431).
- `DAY_CAP`: keep per repo (count lives in each store, cycle.py:872-876, 1157); print it in `status`. `MAX_LAUNCHES_PER_CYCLE`: make it global per sweep (a safety brake; later repos wait one sweep).
- Remaining objection: the `REPO` and `ORIGIN_REPO` hard-wiring must be threaded first; if it spreads past a handful of call sites the cost is higher than either side admitted. Would change its mind on a measured sweep that exceeds the cap even when serial.

## Round 2.5: Invariant probe
See `invariant-probe.md` (12 findings, 4 HIGH, 11 unaddressed when found).

## Scoring Matrix (winner per diff point)
| Diff Point | Winner | Confidence | Evidence |
|---|---|---|---|
| S-001, S-002 | Tie | 60% | same layout; V2 slightly more evidence |
| C-001 (where the loop lives) | V1 | 80% | V2 accepted the loop in the watcher entry point |
| C-002 (state, lock, kill switch) | Tie | 95% | both keep per-repo state |
| C-003 (shared rate stop) | V1 | 75% | V2 accepted one loop-level wait, limited to plain `rate_limited` |
| C-004 (time budget) | V2 | 75% | V1 conceded it needs a cap; per-repo child with kill timer |
| C-005 (approvers) | Tie | 90% | both end with per-repo file content |
| C-006 (operability view) | Tie | 85% | one `status` line per repo in both |
| X-001 (cycle code unchanged) | Neither | 95% | both claims false (`github.py:37`, `launch.py:50`) |
| X-002 (schema objection) | V1 | 80% | V1 keeps one config per repo |
| X-003 (rate limits per account) | V1 | 70% | shared wait accepted |
| U-001 (R8 forces a sweeper) | V1 | 90% | V2 conceded |
| U-002 (account-level stop) | V1 | 75% | accepted with limits |
| U-003 (wrong-target safety, `_origin_ok`) | V2 | 70% | V1 agreed the repo must feed it |
| U-004 (board overlap) | V2 | 60% | UNVERIFIED; discovery is repo-scoped by `gh issue list --repo` (github.py:186) |

## Convergence Assessment
- Points resolved: 14 of 14 on the design shape (alignment 100% on the converged design).
- Status: CONVERGED on design; BLOCKED_BY_INVARIANTS until the HIGH items in the probe are carried into the merged requirements (done in the merged output).
- Unresolved points: none on the choice. Open items are the probe's findings and the loop-level rate-wait file location.
