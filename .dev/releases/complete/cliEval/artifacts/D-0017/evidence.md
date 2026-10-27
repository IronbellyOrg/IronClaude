# D-0017 — Evidence

## Verification matrix

| Surface | Direction | Expected | Observed | Log |
|---|---|---|---|---|
| `make verify-sync` | synced tree | exit 0, "All components in sync." | exit 0 | `evidence/T01.20/verify-sync-positive.log` |
| `make verify-sync` | synthetic `.claude/` drift | exit non-zero, "Drift detected", names file | exit 2 (make's translation of subshell exit 1), `DIFFERS: refactoring-expert.md` | `evidence/T01.20/verify-sync-negative.log` |
| pre-commit `verify-sync` hook | synced tree, scope-matched file | Passed (exit 0) | Passed | `evidence/T01.20/pre-commit-positive.log` |
| pre-commit `verify-sync` hook | synthetic `.claude/` drift | Failed (non-zero), surfaces drift report | exit 1 with full drift listing | `evidence/T01.20/pre-commit-negative.log` |
| `pre-commit validate-config` | static check of `.pre-commit-config.yaml` | exit 0 | exit 0 | `evidence/T01.20/validate-config.log` |

## Acceptance criteria → evidence map

| AC (phase-1-tasklist T01.20) | Evidence |
|---|---|
| Target `make verify-sync` exists in `Makefile` and exits 0 on a synced tree. | `evidence/T01.20/verify-sync-positive.log` (exit 0, "✅ All components in sync."). |
| Pre-commit hook rejects a synthetic commit that edits a `.claude/` file without touching the matching `src/superclaude/` source. | `evidence/T01.20/pre-commit-negative.log` — after a synthetic edit to `.claude/agents/refactoring-expert.md`, `pre-commit run verify-sync` reports `Failed` with `DIFFERS: refactoring-expert.md` and exit 1. |
| Pre-commit hook test fixture confirms a benign synced edit is allowed (positive case). | `evidence/T01.20/pre-commit-positive.log` — `pre-commit run verify-sync --files src/superclaude/agents/refactoring-expert.md` on a synced tree reports `Passed` with exit 0. |
| `TASKLIST_ROOT/artifacts/D-0017/spec.md` records the gate wiring. | `artifacts/D-0017/spec.md`. |

## Files touched

| Path | Kind | Change |
|---|---|---|
| `.pre-commit-config.yaml` | config | Added local `verify-sync` hook (id, files-scope, `make verify-sync` entry, `pass_filenames: false`). |
| `.claude/hooks/reject-workspace-writes.sh` | sync | `make sync-dev` re-applied FU-003 defense-in-depth block from `src/` (pre-existing drift, not introduced by this task). |
| `.dev/releases/current/cliEval/artifacts/D-0017/spec.md` | doc | Gate-wiring spec (this deliverable). |
| `.dev/releases/current/cliEval/artifacts/D-0017/notes.md` | doc | Implementation decisions + follow-ups. |
| `.dev/releases/current/cliEval/artifacts/D-0017/evidence.md` | doc | This file. |
| `.dev/releases/current/cliEval/evidence/T01.20/verify-sync-positive.log` | log | `make verify-sync` on synced tree (exit 0). |
| `.dev/releases/current/cliEval/evidence/T01.20/verify-sync-negative.log` | log | `make verify-sync` with synthetic `.claude/` drift (exit 2). |
| `.dev/releases/current/cliEval/evidence/T01.20/pre-commit-positive.log` | log | `pre-commit run verify-sync` on synced tree (exit 0 Passed). |
| `.dev/releases/current/cliEval/evidence/T01.20/pre-commit-negative.log` | log | `pre-commit run verify-sync` with synthetic drift (exit 1 Failed). |
| `.dev/releases/current/cliEval/evidence/T01.20/validate-config.log` | log | `pre-commit validate-config` smoke check (exit 0). |

## Methodology — negative-case fixture

The pre-commit fixture is reproducible from any synced checkout:

```bash
TARGET=".claude/agents/refactoring-expert.md"
BACKUP=$(mktemp); cp "$TARGET" "$BACKUP"
echo "# synthetic drift" >> "$TARGET"
uv run --with pre-commit pre-commit run verify-sync --files "$TARGET"
# → Verify src/superclaude/ ↔ .claude/ sync (AC11) .............. Failed
# → exit 1, "DIFFERS: refactoring-expert.md"
cp "$BACKUP" "$TARGET"; rm -f "$BACKUP"
```

The positive fixture is the same command on a clean tree (no edit
applied) — observe `Passed` and exit 0.

## Cross-suite regression check

`make verify-sync` (whole-tree) on the post-task working copy exits 0
— see `evidence/T01.20/verify-sync-positive.log`. The only file
that drifted before this task was `.claude/hooks/reject-workspace-writes.sh`
(pre-existing FU-003 source-fix lag); `make sync-dev` resolved it.
No new drift was introduced.
