# Codebase Context — sprint run-lock

Quality tier: primary (Auggie + direct Reads during diagnosis).

## Anchor map

| Concern | Location | Note |
|---|---|---|
| Run loop entry (acquire here) | `src/superclaude/cli/sprint/executor.py:1586` `execute_sprint()` | No lock today; preflight `shutil.which("claude")` at ~1598; phase loop at ~1687 |
| Reusable lock pattern | `src/superclaude/cli/sprint/recovery.py:275-353` | `acquire_recovery_lock` / `release_recovery_lock` |
| Phase-scoped recovery lock caller | `src/superclaude/cli/sprint/rerun_tasks.py` step 1 (`acquire_recovery_lock(results_dir, phase)`) | Must not deadlock with run lock |
| Passive concurrent detector | `src/superclaude/cli/sprint/resume/planner.py:292` | "Detect concurrent unpaired phase_start events" |
| Detector surfaced (auto-resume only) | `src/superclaude/cli/sprint/commands.py:307`, `:862` | "Ambiguous resume state ... concurrent runs?" |
| Run command entry | `src/superclaude/cli/sprint/commands.py` `run` (Click command) | Where a `--force`/override flag would be added |

## Reuse decision

Extend `recovery.py` with a sibling `acquire_run_lock(results_dir)` / `release_run_lock(path)`:
release-scoped lockfile `<results_dir>/.run.lock`, same `{pid,timestamp}` JSON + `os.kill(pid,0)`
liveness + stale reclamation, but **harden** the three known weaknesses (TOCTOU → atomic
`O_CREAT|O_EXCL`; add `SIGINT`; document SIGKILL/SIGSEGV → stale-reclaim path).

## Empirical evidence backing the fix

- Exclusive run: phases 4(PASS)/5(ERROR)/6(ERROR) — all boundaries crossed, **0 segfaults**, exit 1 (task errors, not a crash).
- Synthetic `preexec_fn` fork-race repro: 20k contended spawns clean on Py 3.12 AND 3.13 → race is NOT the trigger.
- Memory flat ~93 GB free throughout → not OOM.
- Concurrency was system-detected at crash time (`planner.py:292`).
