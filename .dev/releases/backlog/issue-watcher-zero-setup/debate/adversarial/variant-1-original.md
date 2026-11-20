# Position: one multi-project issue watcher

(stub) Debate side FOR a single watcher that serves every Orca repo. Date 2026-11-18.

## 1 Thesis

Run one watcher entry point that, each cycle, lists the Orca repos and runs the existing one-project cycle once per repo. The cycle code already treats a project as a self-contained unit (Config, lock, store, state_dir), so the multi-project part is a thin loop on top, not a rewrite. That loop is the only design that meets "starts by itself in every workspace with no per-user setup" without a per-repo scheduler entry that someone must create when a repo is added.

## 2 Arguments for

1. **One scheduler entry, no per-repo wiring.** R6 needs a timer in every workspace and the host has no crontab (requirements.md R6, "Findings"). One timer is one thing for the Coder template to install. N timers means a new timer for each new repo, and R8 says Orca emits no event when a repo is added, so something must poll anyway.
2. **R8 already forces a single sweeper.** R8 says a sweep lists `orca repo list` each cycle and creates a config for any repo without one. A sweep that sees all repos is a multi-project loop. Per-project instances would need a second, outer process to start them, which is the single watcher under another name.
3. **The unit of isolation is already per-project, so a loop loses nothing.** `Config` holds one project_id, worktree, approvers_file, state_dir (cycle.py:96-107). `store.lock()` is an flock on `state_dir/lock` (record.py:381-417). `DISABLED` is `state_dir/DISABLED` (record.py:283, 422). Rate-limit wait is stored in the dispatch store as `next_permitted_at` (cycle.py:663-668). Give each repo its own state_dir and a loop keeps per-repo kill switch, lock, store and status. Nothing is shared that would couple repos.
4. **GitHub limits are per account, so one process sees them whole.** Each cycle calls `github.user` first (cycle.py:~750 `_login_step`). With N independent instances, each backs off separately, so a limit hit by repo A does not slow repo B and all N keep hitting the same account quota. A single loop can stop the whole sweep on the first `rate_limited` result. The design clamps to 3600 s when no header is readable (docs/designs/issue-watcher.md:109, 609), so a wasted extra instance costs an hour of lost cycles. Reading that coupling is UNVERIFIED in code: today nothing shares the wait across state_dirs.
5. **Approvers are mostly shared.** ironbelly and clayphi apply to every repo (stated fact); only maintainers differ. One approvers builder with a per-repo addition is simpler than N hand-kept files (R4).
6. **One status answer.** `status` reads one store and the `DISABLED` mtime (cli.py:167-180; design 733). One loop can print one line per repo and one overall health, which is what an operator looks at.

## 3 Strongest objections and rebuttals

- **"One failure takes down all repos."** Rebuttal: wrap each repo's cycle in its own try, as the cycle already converts every failure to a `_Stop` reason and exit code (cycle.py:689-702). One bad config is a `config_invalid` for that repo only.
- **"The code is one-project by design; a loop is a second design."** Rebuttal: the loop calls `load_config` and `Cycle.run` unchanged. The design doc's `Config` stays as is.
- **"Per-project instances isolate blast radius and keep the audited, shipped behaviour."** Rebuttal: true for the lock and store, which I keep per repo. What a loop adds is only iteration, and R8 needs iteration regardless.
- **"A slow repo eats the 'deadline' for others."** Rebuttal: `Deadline` is per cycle (cycle.py:405); each repo gets a fresh one. Total wall time grows with repos, which is acceptable at five repos.
- **"A shared worktree/coordinator is needed per project anyway."** Rebuttal: agreed (requirements note), and a single watcher does not remove that; it reads it from each config.

## 4 What code would have to change

- `cli.py`: add a verb (for example `once --all`) that globs a config directory, calls `_load_config` and the cycle per file, and prints a per-repo summary and the worst exit code.
- `cycle.py`: no change to `Config` or `load_config`; optionally a `resolve_exit` fold over repos. Add a small `ensure_config(repo)` that fills project_id, owner_account_id and approvers (R2-R4), writing a config per repo.
- `record.py`: none, if state_dir stays per repo (`init_state` is reused for R7).
- A shared rate-limit stop: pass a small in-process flag so the loop halts on the first account-level limit.
- Docs: issue-watcher-setup.md gains the all-repos run; the design doc gains one section.

## 5 Risks I accept

- A loop bug could affect every repo at once, so it needs its own test.
- Runtime grows with repo count; five repos is fine, fifty is not.
- Account-wide rate-limit sharing is new behaviour I must design, not inherit.
- The loop runs as one user account; a repo needing another identity is out of scope.

## 6 Concede if

- The code review shows the lock or state_dir is assumed global anywhere (a shared path I missed), making a per-repo loop unsafe.
- The Coder template can create timers per repo cheaply and Orca can announce new repos, so R8's sweep is not needed.
- Different repos need different GitHub accounts or tokens.
- Owners want one repo's watcher stopped or upgraded independently at the process level, not just by `DISABLED`.
