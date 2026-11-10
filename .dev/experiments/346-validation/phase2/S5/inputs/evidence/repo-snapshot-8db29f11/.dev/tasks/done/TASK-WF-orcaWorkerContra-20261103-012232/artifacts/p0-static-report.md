# P0 static report: Orca worker contract

Plan: `./TASK-WF-orcaWorkerContra-20261103-012232.md` (static P0 plan, version 2). Spec: `./source.md`. Checkout: branch `ironbelly/OrcaCLICommandRefactor-Specs`, HEAD `d01759e1` (unchanged by this plan). Run date: 2026-11-03. Every evidence file below is under `./artifacts/` of this package.

## Check results

| Check | Result | Evidence file |
|---|---|---|
| AC-0.1 | PASS: `WORKER-CONTRACT.md` is in `KNOWN_CORE_FILES` (rc=0), the install check copies it into a fresh directory (rc=0), and `tests/skills/test_worker_contract.py` passes (196 passed, rc=0) | `./artifacts/ac-0.1.txt` |
| AC-0.2 | PASS: `cmp` of the routing guide and its `sc-recommend` copy exits 0, and the three routing-guide test files pass (92 passed, rc=0) | `./artifacts/ac-0.2.txt` |
| AC-0.3 | PASS: the deletions check on `src/superclaude/core/HOW-WE-WORK.md` prints nothing (numstat `11 0`: 11 lines added, none deleted) | `./artifacts/ac-0.3.txt` |
| AC-0.7 | PASS: the trace lists `worker-start`, `dispatch` and low-level dispatch as checked, and `task-create`, `worktree create --agent` and `agent launch` as not checked (covered only by WC-13 and section 7.2 step 5); a person-opened session is depth 0; each with `path:line` in Orca 1.4.237's installed code | `./artifacts/ac-0.7-depth-trace.md` |
| AC-0.9 | PASS: the write-verb audit in `tests/skills/test_worker_contract.py` finds 101 hit lines (99 unique keys) and every one is classified (wc9-allowed 10, deferred:P1 1, deferred:P2 11, deferred:P4 5, never-worker 48, no-command 2, read-only 24); it fails on an unclassified scratch hit | `./artifacts/ac-0.9-hits.txt` |
| AC-C1 | PASS: the scan prints nothing | `./artifacts/ac-c1.txt` |
| AC-C2 | PASS: `make verify-sync` exits 0 ("All components in sync.") | `./artifacts/ac-c2.txt` |
| AC-C3 | PASS: `uv run pytest tests/skills/ -q -rf` gives 804 passed against the 608-passed baseline; no baseline test fails and all 196 new tests pass (re-run in Task 8: 804 passed) | `./artifacts/ac-c3-compare.md` |
| AC-C4 | PASS: on the index after `git add .dev/tasks` and the coordinator-directed `git restore --staged` of the superseded package (see the commit list below), the check prints nothing (empty file); nothing under `.claude/` is staged | `./artifacts/ac-c4-index.txt` |
| AC-C5 | PASS: run with an empty edit set, because P0 edits no command file (no tracked or untracked change under `src/superclaude/commands/`) | `./artifacts/ac-c5.txt` |
| AC-C6 | PASS: one profile (`local-default`) prints `"nestedWorkerMaxDepth":1`; no profile relies on the presumed default | `./artifacts/ac-c6-depth-setting.txt` |

Known baseline failures outside these checks: the wider suite run by Task 4 still has 5 failures, all labelled `accepted` in `./artifacts/t1-accepted-failures.md` (they need the `ruff` executable, which this environment lacks); see `./artifacts/t4-wider-compare.md`.

## Paths for the owner-approved commit

Every repo path this plan created or changed outside `.claude/`. The `.claude/` copies written by `make sync-dev` are sync output and are not committed.

- `src/superclaude/core/WORKER-CONTRACT.md` (new)
- `src/superclaude/cli/install_core.py` (changed: `KNOWN_CORE_FILES` entry)
- `src/superclaude/core/HOW-WE-WORK.md` (changed: new `## Orca coordination` section)
- `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (changed: byte-for-byte copy)
- `tests/skills/test_worker_contract.py` (new)
- No plugin copy of `WORKER-CONTRACT.md`: Task 3 decided none is needed (`./artifacts/t3-plugin-mirror.md`).
- `.dev/tasks`: this package, `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/` (moved to `.dev/tasks/done/` when the archive runs), with its `progress.md` and `artifacts/`. Staging: Task 8 ran `git add .dev/tasks`, which staged everything under `.dev/tasks/`, and then at once `git restore --staged .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`. That second command is the coordinator's decision, not this plan's: the coordinator's dispatch brief for this run orders it right after the add, so that the superseded package `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/` (an earlier, replaced plan package) stays unstaged, and forbids staging that package. It is therefore not part of this commit. This is a deliberate exception to the always-staged rule for `.dev/tasks/`; whether that package is later staged, committed or removed is for the coordinator and the owner to decide.

## Next steps (`./source.md` section 6 and section 7.2)

1. The coordinator asks the owner to approve the commit of the paths above.
2. After approval, the coordinator commits and runs `uv run superclaude install --force` from this checkout, so the installed `~/.claude/` copy carries the P0 files.
3. Then the P0 live plan is written: the section 7.2 live checks AC-0.4, AC-0.5 and AC-0.6, and the P0 phase report. P0 passes only when both the static and the live plan's checks pass.
