# Issue watcher: one watcher entry point, per-project instances

## Decision
<!-- Source: Base (V2) -->
<!-- Source: Variant 1, merged per Change #1 -->
Run the existing single-project watcher once per Orca repo, each with its own config, state directory, lock and kill switch. A new verb in the `issue-watch` entry point (such as `run-all`) walks the repos and starts one child per repo, and it is also the R8 sweep, so there is no outer wrapper script. Zero setup becomes a config generator plus one scheduled entry, not a rewrite of the cycle.

## Design
<!-- Source: Base (V2) -->
<!-- Source: Variant 1, merged per Change #2 -->
<!-- Source: Variant 1, merged per Change #3 -->
<!-- Source: Variant 1, merged per Change #4 -->
<!-- Source: Variant 1, merged per Change #5 -->
<!-- Source: Variant 1, merged per Change #9 -->
<!-- Source: Variant 1, merged per Change #10 -->
<!-- Source: Variant 1, merged per Change #11 -->
- **What runs.** One scheduled entry (R6) runs the loop verb, which starts `superclaude issue-watch once --config <path>` per repo, serially.
- **Where state lives.** One config per repo. The generator always writes an explicit absolute `state_dir` (cycle.py:259-266), so each repo has its own `state_dir/lock` (record.py:381-403), `DISABLED` file (record.py:283, 422) and store. The loop keeps its own account rate wait in one loop-level file.
- **The loop.** It reads `orca repo list`; a failed or timed-out list is an error exit, not "zero repos". Temporary and foreign-owner repos are skipped. Zero Projects: skip and report. Several: use the one in the central config and report it.
- **Rate wait.** One account-wide wait, stored once, applied only for plain `rate_limited`, not `rate_limit_clamped` (github.py:418-431). Children never write each other's stores.
- **Launch brake.** One launch per sweep: the loop stops after the first `launched` child (cycle.py:35, 36, 872-876). `DAY_CAP` stays per repo and `status` prints it. The repo order rotates each sweep so one repo cannot hold the slot.
- **Loop cap.** About 270 s for the whole loop. Each child's kill timer exceeds its own 240 s deadline (cycle.py:41, 1091-1099). Unfinished repos are skipped and reported.
- **Config generator.** It validates with `load_config` (cycle.py:195) and writes the config, approvers file and state directory per repo. A new config starts `enabled: false` (cycle.py:685-686) until the owner switches it on; that manual gate is stated in the zero-setup requirements.

## Code that must change
<!-- Source: Base (V2) -->
<!-- Source: Variant 1, merged per Change #6 -->
- `github.py`: the `REPO` constant (line 37, also 187, 208, 259) must come from the repo's config.
- `launch.py`: `ORIGIN_REPO` (line 50, also 249) must come from the repo's config.
- This is code change, not reuse; the base claim of "no change to github.py" was false.
- `cli.py`: the new loop verb, which also performs the sweep.
- A new generator function writing configs under `~/.config/superclaude/issue-watch.d/<repo>.json`.

## Requirements this design depends on
<!-- Source: Variant 1, merged per Change #12 -->
<!-- Source: Variant 1, merged per Change #7 -->
<!-- Source: Variant 1, merged per Change #8 -->
- **R6 scheduler:** the host has no crontab, so the Coder template must install the one timer.
- **R9 coordinator:** a claim launched with `--pipeline none` needs a coordinator session to act on it.
- **R10 Coordinator worktree:** each repo's worktree must exist with its origin matching the repo. The loop checks this before the child runs (launch.py:249); without it the cycle stops with `worktree_invalid` (cycle.py:373-375).
- **R11 labels:** `issue-watch:trigger` and `issue-watch:approved` are created on each repo by the per-project init. A missing label is reported. Otherwise the run is clean but never launches (predicates.py:224-225).

## Risks and how each is handled
<!-- Source: Variant 1, merged per Change #2 -->
<!-- Source: Variant 1, merged per Change #3 -->
<!-- Source: Variant 1, merged per Change #4 -->
<!-- Source: Variant 1, merged per Change #5 -->
<!-- Source: Variant 1, merged per Change #6 -->
<!-- Source: Variant 1, merged per Change #7 -->
<!-- Source: Variant 1, merged per Change #8 -->
<!-- Source: Variant 1, merged per Change #9 -->
<!-- Source: Variant 1, merged per Change #10 -->
<!-- Source: Variant 1, merged per Change #11 -->
<!-- Source: Variant 1, merged per Change #12 -->
- INV-001, shared state: explicit absolute `state_dir`.
- INV-002, account rate wait: one loop-level wait, plain `rate_limited` only.
- INV-003, origin guard: repo threaded from config, plus worktree origin check.
- INV-004, prompt names no repo: the worktree check covers it.
- INV-005, launch cap: one per sweep, rotating order.
- INV-006, loop cap: kill timer above 240 s, rotation.
- INV-007, wrong repo or Project: skip temporary repos, handle zero or several Projects.
- INV-008, empty list: a failed `orca repo list` is an error exit.
- INV-009, threading `REPO`: already addressed.
- INV-010, labels: created by init, absence reported.
- INV-011, `enabled`: starts false, manual gate stated.
- INV-012, sufficiency: R6, R9, R10, R11 are named.

## What was rejected and why
<!-- Source: Base (V2) -->
<!-- Source: Variant 1, merged per Change #1 -->
- A single multi-project config with a new schema version: not needed, both sides keep one config per repo.
- A shared day cap: the count lives per store, and a global one needs a new shared counter.
- Parallel children: not needed unless a measured sweep exceeds the cap.
- An outer wrapper script: the loop lives in the entry point.
- An in-process loop without children: it loses the per-repo kill timer.
