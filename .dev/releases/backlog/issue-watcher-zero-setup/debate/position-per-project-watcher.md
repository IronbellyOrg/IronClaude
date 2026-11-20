# Position: one watcher instance per project

## 1 Thesis

Run the existing single-project watcher once per Orca-registered repo, each with its own configuration, state directory, lock and scheduled run. The code already assumes exactly one project per run, and every safety property (lock, kill switch, rate-limit pause, day cap, 240 second deadline, health stamp) is scoped to that one project. Zero setup then becomes a generator problem (write one config per repo) instead of a rewrite of a hardened cycle.

## 2 Arguments for

1. **The config is one project by construction.** `Config` holds one `project_id`, `worktree`, `approvers_file` and `state_dir` (cycle.py:97-107). `_TOP_KEYS` rejects any other key (cycle.py:58-69, 216-220). A multi-project watcher needs a new schema version (`SCHEMA_VERSION = 1`, cycle.py:54) and a migration; instances need only new files in the existing format.
2. **Failure isolation comes free.** The lock is a `flock` on `state_dir/lock` (record.py:381-403). `DISABLED` is `state_dir/DISABLED` (record.py:283, 422). A bad store, a held lock or a kill switch on one repo stops only that repo. In a single multi-project process these would have to be re-scoped by hand.
3. **Per-project rate pause.** `next_permitted_at` lives in the store and stops the cycle with `rate_limited` (cycle.py:748-750, 663-668). Per instance, a throttled repo sleeps while the others run. One shared store would pause everything, or force a per-project map in `dispatch.json` (record.py:281).
4. **The time budget is per cycle.** `DEADLINE_TOTAL_S = 240`, `LAUNCH_CUTOFF_S = 120`, `MAX_CANDIDATES = 10`, `MAX_LAUNCHES_PER_CYCLE = 1`, `DAY_CAP = 6` (cycle.py:34-43). Five repos in one 240 second deadline starve the later ones; the first repo with a slow `gh` call eats the budget. Instances each get a full budget.
5. **Approvers differ per repo.** The approvers file is read and validated per run (cycle.py:298-310, 372-377), and R4 adds each repo's maintainers. Per-repo files keep one repo's maintainer from approving work in another. A merged watcher needs a per-project approver map and a check that the right map is used.
6. **Wrong-target safety is per worktree.** `_origin_ok` checks the config's worktree origin (cycle.py:670-678) and launches run in `cfg.worktree` (cycle.py:1086). Project and worktree are bound one to one; the check is meaningful only if they cannot be mixed.
7. **Blast radius of a bug.** A launch bug in a multi-project loop can misfire across all five repos. Per instance, `status` (cycle.py:1275 onward, exit 1 when `last_completed_cycle_at` is over 900 seconds old, HEALTH_AGE_S at cycle.py:45) names the broken repo directly.
8. **R3 and R8 fit it.** R3 (project looked up per repo) is a per-repo config field; R8 (sweep that creates a config for repos with none) is "write a file if missing". Both are idempotent and need no running-process state. Coordinator-per-project is already a stated need, so the unit of ownership is already the project.
9. **No Orca event, no daemon.** There is no Orca add-project event and no crontab (requirements.md findings). A sweep then a loop over config files, each launching `superclaude issue-watch once --config <path>`, needs no new long-running service.

## 3 Strongest objections and rebuttals

- **GitHub rate limits are per account, so five instances multiply API cost.** True, and design risk R12 already says "the API cost multiplies" for multiple stores (issue-watcher-setup.md section on risks). Rebuttal: the loop runs instances serially, not in parallel, so spend equals one multi-project watcher making the same calls; the per-instance clamp (cycle.py:663-668) backs off on a 429 and the scheduler skips the rest. UNVERIFIED: the real calls-per-cycle count per repo.
- **Five schedules, five lock files, five locations is more to operate.** Rebuttal: one scheduled entry runs the loop; only state is per repo. Operators read five `status` lines, which is the point.
- **A new repo needs a new instance created by the sweep (R8), which is the thing a single watcher would avoid.** Rebuttal: a single watcher still needs the sweep to learn each repo's project id, worktree and approvers (R3, R4). The sweep exists in both designs.
- **Duplicate-launch risk when two instances see the same issue.** Rebuttal: an issue belongs to one repo, and each repo has one store. The double-launch risk in R12 is two stores for the same repo, which one config per repo prevents.
- **One Project board may span repos (the "Ironclaude - Development" board).** UNVERIFIED how many repos share it. If they do, two instances can both see one board item. Mitigation below.

## 4 What would have to change

- **A generator, not a rewrite.** New function in the issue_watch package (for example `configs.sync_from_orca`) that runs `orca repo list`, calls `gh project list`, `gh api user`, and `gh api repos/<o>/<r>/collaborators`, and writes `config.json`, the approvers file and `state_dir` per repo. Reuses `load_config` (cycle.py:195) to validate before saving.
- **A loop verb.** New Click verb in cli.py (for example `issue-watch run-all`) that walks the config directory and calls the existing `once` path per file, serially, with a total wall-clock cap.
- **Config path layout.** `~/.config/superclaude/issue-watch.d/<repo>.json` and `state_dir` default per repo (replaces the single default at cycle.py:187-192).
- **Coder template.** One scheduler entry for the loop (R6), and R1 central default config. No change to `cycle.py` logic, `record.py` or `github.py`.
- **Board overlap.** If two repos share one `project_id`, a per-instance `repo` filter on discovery (predicates.project_check, cycle.py:958, 1015). UNVERIFIED whether discovery is already repo-scoped.

## 5 Risks I accept

- Five approvers files and stores to keep fresh (R10 grows to five).
- API cost multiplies by repo count (R12), bounded by serial runs and the clamp.
- Cycle latency grows linearly: five repos at up to 240 seconds each is 20 minutes worst case, so the six-field 5 minute schedule must be replaced by a loop with its own cap.
- Config drift between repos if the generator changes.

## 6 When I would concede

- Measured GitHub spend shows the account rate limit is hit at current repo counts even when serial.
- Most Orca repos share one Project board and discovery cannot be scoped per repo without edits, making duplicates likely.
- The count of repos grows past about ten, so serial runs cannot finish inside the schedule.
- Cross-repo ordering (one global day cap or launch cap) becomes an owner requirement.
