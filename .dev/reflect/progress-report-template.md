# Sprint Progress Report — TEMPLATE (locked 2026-06-02)

Standard render for the per-phase progress reports of the TUIBBS V1 MVP sprint
(phases 5→10). Decisions below are user-finalized; apply verbatim for R6–R10.

## Cadence & two-tier assembly

- **Per-task report** — written live to `.dev/reflect/progress/T0N.NN.md` the moment
  each task completes. Source of all per-task data; the phase report is assembled
  cheaply by `cat .dev/reflect/progress/T0N.*.md` + a thin computed header (NO
  expensive end-of-phase rollup).
- **Per-phase report** — one full report per `phase_complete`, rendered in the
  locked layout below. A richer **release-readiness report** at the Phase-10 pause.

## Per-task captured fields

- **Stats:** duration (from JSONL timestamps) · ⌀duration/task · models used · sub-agents spawned · verdict · deviation class
- **Diffstat:** +/- LOC · files · **new packages** · **new `TUIBBS-NNNN` codes** · **new migrations** · **new public API surface** (flag explicitly — ripples downstream)
- **What was done** (1–2 lines) + **Lessons → future agents** (bugs hit, what worked, what to avoid)
- ▲ **token-burn / turns / turns-per-min = FUTURE-INSTRUMENTATION placeholder** — the sprint runner emits `tokens=0/turns=0`; show `n/a (▲)` rather than fabricate. Revisit if the runner gains per-task token accounting.

## Remediation decision matrix (severity gates *whether*; complexity picks *mechanism*)

| Finding severity | Fix complexity | Action |
|---|---|---|
| LOW / drift | low | auto-remediate silently → fix, re-test, log in task report, continue |
| MEDIUM+ | low | flag + auto-spawn `task-builder` in parallel, fix inline |
| MEDIUM+ | medium | flag + parallel `/sc:brainstorm` → adversarial debate of fix → implement via `/sc:task` |
| MEDIUM+ | high | flag + `/sc:reflect --remediate` pipeline |
| Regression, LOW sev | — | flag, keep going (surface in phase report) |
| Regression, MED+ sev | per complexity | flag + parallel remediation, fix it |

JSONL/bookkeeping gaps (recurring runner journaling shortfall): authoritative evidence
is on-disk checkpoints + evidence dirs (postscript pattern); **batch-backfill at the
Phase-10 pause**, do not block the running sprint.

## Locked layout — split-pane frame + otel-tui waterfall + contrib heatmap (~116 cols)

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ◤ TUIBBS V1 MVP · PHASE {N} REPORT ◢   {🟢PASS|🟡ATTN|🔴FAIL}   ▸ now: {…}   ⏱ {dur}   gates {n}✅   reflect{✓}  #R{N} │
├────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────┤
│ PHASES             │ KPIs   tasks {evd}·{jrnl}    reflect {verdict}    regr {n}    drift {n}    lint {🟢}  race {🟢} │
│ {tree: ▾done ▸run  │ ──────────────────────────────────────────────────────────────────────────────────────────│
│  ⬚pending, gates   │ WATERFALL   t0 {…} ─────────────────────────────────────────────────────────▶ now {…}       │
│  + tasks nested}   │  {phase span bars on a time axis; current-phase tasks nested w/ duration + verdict}         │
├────────────────────┤ ──────────────────────────────────────────────────────────────────────────────────────────│
│ GATES              │ HEATMAP · Ph{N}   ✅pass ◆nec-dev ◇drift ✖regr ·pend                                          │
│ {G1..G6 + CG-x     │  HEATMAP · run 4▸{N}  — MULTI-PHASE grid: rows = phases, cols = tasks 01..22(23).         │
│  with ✅/⬚ +       │  Cells are UNIFORM colored squares (🟩 pass · 🔵 running · ⬜ pending · ⬛ n/a · 🟦 nec   │
│  closed count}     │  · 🟨 drift · 🟥 regr · 🔥 cfg-fail) so columns never drift. Per-row count at right.       │
│                    │  NOTE: do NOT mix emoji (double-width) with single-width glyphs in a cell row.             │
│  with ✅/⬚ +       │ ──────────────────────────────────────────────────────────────────────────────────────────│
│  closed count}     │ DETAIL — Phase {N} · {milestone name}                                                        │
│                    │  {2–4 lines: what landed, keystone NFR numbers, gate evidence}                              │
│ COST / VELOCITY    │ LESSONS → FUTURE AGENTS                                                                     │
│ tokens   n/a (▲)  │  • {bug/course-correction + the better approach}                                            │
│ turns    n/a (▲)  │  • {what to preserve / what ripples downstream}                                             │
│ dur/task {~Nm}    │                                                                                            │
│ models   {…}      │                                                                                            │
├────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────┤
│ ISSUES   {🟢 0 open | 🟡 … | 🔴 …}  {+ remediation taken per matrix}                                              │
│ LOG      {recent phase_start/gate-closed/phase_complete events, newest right}                                    │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Zones: **left nav** (phase tree + GATE scorecard + COST/VELOCITY) · **main** (KPIs →
WATERFALL → HEATMAP → DETAIL → LESSONS) · **full-width footer** (ISSUES + LOG).
Width ~116 cols. Renders cleaner in true monospace/TUI than markdown preview.

## Final R6 decorations (locked)
- **Heavy/bold outer frame** on the main board (`┏ ━ ┓ ┃ ┗ ┛` + `┣ ┫ ┳ ┻ ╋`); inner split-pane divider heavy too.
- **Three detached satellite panes**, attached by plug-ended patch cables (`◉` beads · `⌇` coil · ⚡/🔌 accents · `◖━╮…╰━◗` hooks):
  - TOP — release rail: milestones + 13-phase colored rail (`🟩🟩🟩🟩🟩🔵⬜…`).
  - RIGHT — cumulative since-start stats + NFR vitals + next/pause preview.
  - BOTTOM — event log + color legend.
- **Color** via colored-square/emoji glyphs for chat delivery (🟩🟦🟨🟥🔥⬜🔵 + 🩺📊📦💡⏱🆕 section icons). For raw-terminal rendering, swap to ANSI-on-single-cell glyphs (emoji are double-width and drift in strict monospace).
- **Heatmap = multi-phase** phases×tasks grid (see above), the run-progress centerpiece.

## Inspirations
split-pane app frame (primary container) · otel-tui span/Gantt waterfall · GitHub-contrib heatmap (multi-phase) · dolphie KPI ribbon + right-rail · bashtop meters/gauges · patch-panel cabling.
