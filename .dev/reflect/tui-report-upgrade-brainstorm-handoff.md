# Handoff — `/sc:brainstorm`: sprint-run TUI report-view upgrade

Paste this into a fresh chat to kick off the design brainstorm. Self-contained.

```
/sc:brainstorm "Upgrade the SuperClaude sprint-run TUI to support a toggleable, real-time 'release report' view with per-phase snapshots" --codebase --depth deep --personas frontend,architect --handoff tasklist

CONTEXT — this is a framework change (edit src/superclaude/cli/sprint/, then `make sync-dev`), NOT a change to any sprint's target repo.

## Goal
`superclaude sprint run` currently shows a Rich `Live` phase-table TUI (src/superclaude/cli/sprint/tui.py — `class SprintTUI`, `rich.live.Live`, refresh_per_second=2; tmux pane in tmux.py). Add a second view + three behaviours:
1. Toggle (hotkey, e.g. `v`/Tab) between the current phase-table view and a new "release report" view. Both live.
2. Real-time report view — re-renders continuously from live run state as tasks/phases progress.
3. Per-phase snapshot — on phase completion, auto-capture the report to a file (results/reports/R{phase}.{txt|svg}) and surface it.

## Target report rendering (locked style — see .dev/reflect/progress-report-template.md)
Heavy wired frame + multi-phase colored-square heatmap (rows=phases, cols=tasks, per-row counts) + 3 satellite panes (top release-rail, right cumulative AUX/NFR, bottom log+legend) + left nav + gate scorecard + HEALTH band + waterfall + detail + lessons. Reproduce natively in Rich (Layout/Panel/Table).

## Live data sources
- .dev/releases/current/<release>/execution-log.jsonl — phase_start/phase_complete(status,duration)/task_complete.
- .../tasklists/checkpoints/CP-*.md — per-checkpoint status + gate closures (G1/G3/G4/G5/G6/CG-3) + milestone exits.
- .../results/phase-N-task-TNN.NN-output.txt — per-task stream-json: terminal_reason, num_turns, total_cost_usd, duration.
- In-process: executor.py aggregate_task_results, models.py TaskStatus/PhaseStatus — read live state directly.

## Hard-won constraints (don't rediscover)
- Emoji are DOUBLE-WIDTH → break monospace alignment in a real terminal. Use ANSI-colored single-cell glyphs (Rich `[green]█[/]`), NOT emoji, for status/heatmap cells. Emoji only for chat exports.
- Stats duration-only by default; token/turn burn = future-instrumentation, only via parsing per-task stream-json (num_turns, total_cost_usd) — the runner's own KPI emits tokens=0.
- Runner `status: error` ≠ phase failed. A phase is flagged error when ANY task hit --max-turns (monitor.py detect_error_max_turns) even if deliverable+tests+checkpoint passed. The report MUST distinguish "task capped" (🟡) from "real failure" (🟥). (This is the bug fixed on branch fix/per-task-error-max-turns-falseneg.)
- Multi-phase heatmap is the centerpiece; must scale (20–23 tasks/phase × 13 phases).
- Frame ~116 cols; handle narrower terminals (collapse the right AUX pane or horizontal scroll).

## Brainstorm these
1. Toggle UX + clean Rich `Live` renderable swap (table ↔ report ↔ logs).
2. Real-time architecture: poll JSONL/checkpoints on the 2 Hz refresh vs. in-process event bus from executor.py; debounce; re-render cost.
3. Snapshot format (text / Rich .svg|.html export) + destination + how to 'post' it (stdout / notify hook / watched file).
4. Native Rich rendering of the heavy wired frame; ANSI single-cell heatmap; responsive width.
5. Minimal-coupling live gate/heatmap/health sourcing.

Produce 3 proposals, debate, converge on a buildable plan + tasklist handoff."
```

Verified invocation: `/sc:brainstorm` at .claude/commands/sc/brainstorm.md — flags `--codebase`, `--depth deep`, `--personas`, `--handoff tasklist` all canonical.
