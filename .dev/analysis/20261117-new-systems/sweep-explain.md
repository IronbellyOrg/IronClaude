# Explanation: `superclaude sweep` (advanced level)

Source: origin/master, read with `git show`. Graph token: graph:stale (codegraph not used).

## One-line summary
`superclaude sweep run` takes one read-only snapshot of Orca (Runs, workers, worktrees), git status of each worktree, Claude Code transcripts and ccsession tab files. It sorts every session into one of 8 classes with an ordered rule list, and publishes one Markdown report plus one JSON object.

## Layers (functional core, imperative shell)
1. `commands.py` (shell): checks arguments (exit 2), calls collect, classify, render, then `_publish` (the only write). Exit 0 published, 1 internal error, 2 usage error (`commands.py:1-9`).
2. `probes.py` (read side): the only module that starts a subprocess. Two seams, `_orca` and `_git`, each guarded by an argv allowlist (`probes.py:49-81`, `226-244`).
3. `classify.py` (pure): joins Orca rows to transcripts, runs `RULES` in order, first match wins (`classify.py:345-386`).
4. `report.py` (pure): Markdown sections and JSON v1; `sanitize` strips escape codes and neutralises Markdown (`report.py:545-610`).
5. `models.py`: frozen dataclasses only.

## The eight classes
waiting on a person, stalled (proved), fenced, working, finished, idle, person session (active), could not determine (`models.py:50-59`).
Rule order: blocked_contract, orca_exit_proof, fenced, waiting_signal, working, finished, idle, person_active, fallback (`classify.py:345-355`). Anything unproved becomes "could not determine" rather than a guess.

## Read-only mechanics
- Orca: 10 allowed templates, 7 verbs, binary `orca-ide` never bare `orca`; `--include-remote` rejected anywhere.
- git: only `status --porcelain=v1 -z --branch --untracked-files=all --ignore-submodules=all` plus three config inspections; always `--no-optional-locks`, `core.fsmonitor=false`, `GIT_OPTIONAL_LOCKS=0`. A git filter that could run a program makes the worktree "unscanned" instead (`probes.py:995-1048`).
- Disk reads are bounded (1 MiB contract, 256 KiB transcript tail, 8 MiB command output), checked to stay inside their root, and re-read once if the file changed during the read.
- Budget: 50 worker-show calls, 90 s total, 10 s per call (`probes.py:124-130`).
- One write: temp file, then `os.link` to the first free name (`<stamp>-sweep.md`, `-2` to `-99`), never overwriting, under `<root>/.dev/sweeps/` only (`commands.py:153-208`).

## Phase 1 honesty features
Every unreadable source becomes a `SourceCoverage` row ("unscanned" plus reason). Safe to close never says yes. `total_is_lower_bound` is always true because remote hosts are never scanned. Stalled and fenced are marked "not observed in Phase 1".

## Skill and command
`/sc:sweep` (allowed-tools Skill) loads `sc-sweep-protocol`, which runs the CLI once (PATH first, `uv run --frozen --no-sync` fallback only on "command not found"), reads the report, prints counts and path, recommends nothing.
