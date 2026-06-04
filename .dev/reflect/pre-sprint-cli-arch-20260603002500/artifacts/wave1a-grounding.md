# Wave 1A — Independent Grounding of SYNTHESIS Load-Bearing Claims

Verified against worktree `SprintCLIWireDead` source at `src/superclaude/cli/sprint/`
(branched from `docs/octocode-integration-investigation-backlog`). Spec authored against
the main working tree on 2026-06-02 → expect line drift.

| # | Claim (SYNTHESIS / agent docs) | Spec cite | Actual (this worktree) | Verdict |
|---|---|---|---|---|
| 1 | `setup_isolation` has zero callers (dead) | executor.py:150 | def at executor.py:151; grep finds only the def, no call site | ✅ TRUE |
| 2 | `build_task_context`/`compress_context_summary` dead, "zero callers (def + docstring only)" | process.py:257-385 | `build_task_context` def@257, 0 external callers; **`compress_context_summary` HAS 1 caller** — `build_task_context:290` | ⚠️ build_task_context dead = TRUE; compress is transitively dead but "zero callers" is imprecise |
| 3 | No `task_complete` writer anywhere | logging_.py | grep `task_complete` → **empty** | ✅ TRUE (strongest claim) |
| 4 | Runtime fork on heading regex | config.py:374-377; executor.py:1261-1324 | `_TASK_HEADING_RE`@380, used@426; fork at executor.py:1264-1270 | ✅ TRUE (line drift +6) |
| 5 | `turns_consumed` hardcoded `0` | executor.py:1114-1115 | `_run_task_subprocess` returns `(exit_code, 0, output_bytes)` @ executor.py:1118; thin prompt @1090-1094; no `env_vars` @1101-1111 | ✅ TRUE — **+ comment line 1117: "Turn counting is wired separately in T02.06"** (existing task ref the spec never mentions) |
| 6 | "**`CLAUDE_SETTINGS_DIR` is never set anywhere**" | SYNTHESIS §1 | **SET at executor.py:133** inside `IsolationLayers.env_vars` (the dead class) | ⚠️ IMPRECISE — literally false ("set anywhere"); TRUE in spirit ("never set in any LIVE path"). agent1-execution-model.md states it precisely; SYNTHESIS overstated it. |
| 7 | `TaskEntry.dependencies` parsed but ignored by loop; "**Stage 3 is the first consumer**" | config.py:436-441 | parsed @441-447,492; `execute_phase_tasks` body (928-1075) has zero dependency/topology refs (loop ignores ✅); **BUT `rerun_tasks.py:446-449` already consumes `entry.dependencies` / `tr.task.dependencies`** | ⚠️ "loop ignores" TRUE; "Stage 3 first consumer" **FALSE** — rerun_tasks.py is an existing consumer |
| 8 | `_jsonl` bare lock-free append | logging_.py:210-212 | `def _jsonl` @265-267: `open(path,"a"); f.write(json.dumps(...))` — no lock/flush/fsync/rename | ✅ TRUE (line drift +55) |
| 9 | checkpoints atomic temp+replace idiom | checkpoints.py:204-206 | `tmp.write_text(...)`@209; `tmp.replace(output_path)`@210 | ✅ TRUE (line drift +4) |

## Cross-cutting findings (not in spec)

- **F-A (line drift, HIGH for tasklist authoring).** Every spec citation has drifted in this
  worktree: +4 (checkpoints), +6 (config), +3 (executor turns), **+55 (logging_.py)**. A tasklist
  built from this spec MUST anchor on symbol names (`_run_task_subprocess`, `_jsonl`,
  `setup_isolation`), NOT literal line numbers — they are already stale and will drift further.
- **F-B (existing T02.06 turn-counting task).** executor.py:1117 comment references an existing
  task `T02.06` for turn counting. Stage 0's "fix turns_consumed=0" overlaps it; reconcile before
  authoring a duplicate.
- **F-C (rerun_tasks.py is a prior `dependencies` consumer).** Contradicts "Stage 3 is the first
  consumer." A Stage-3 DAG scheduler builder should read rerun_tasks.py:446-449 first — it already
  demonstrates the parsed `dependencies` shape in use, partially discharging Open Item §5.3.

## Verdict

The SYNTHESIS's **central thesis is VERIFIED**: dead `setup_isolation` + dead `build_task_context`
+ missing `task_complete` + hardcoded `turns_consumed=0` + heading-regex fork all confirmed. This
is genuinely "a wiring job, not a greenfield build." The two imprecisions (claims 6, 7) do not
undermine the thesis but would mislead a literal-reading tasklist author.
