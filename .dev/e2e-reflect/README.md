# E2E Reflect-Gate Tests (sandbox)

Real-world end-to-end exercises of the reflect gates wired into `/task-builder`
and `/sc:tasklist` (PR #138). Everything here is throwaway — agents MUST confine
all writes to `.dev/e2e-reflect/<scenario>/` and MUST NOT run git add/commit or
touch `src/`, `.claude/`, or anything outside their sandbox.

## Matrix

| Group | Scenario | Command sequence | Reflect-feature facet challenged |
|---|---|---|---|
| A (task-builder) | **tb-1** spec-backed | `/task-builder` (+`--spec`) → `/task` | PRE gate runs UC-1 coverage → `reflect_pre: pass`; templated POST item present + penultimate; `/task` HALTs at POST gate |
| A | **tb-2** specless | `/task-builder` (no spec) → `/task` | PRE gate degrades to `verdict: skipped (no-spec)` (Decision C2); POST item still templated |
| A | **tb-3** refactor | `/task-builder` (refactor goal) → `/task` | TCS override O2 (`type` refactor → `S6=1`) forces `--depth deep`; POST depth floored ≥ standard (O4) |
| B (sc:tasklist) | **tl-1** happy 2-phase | `/sc:tasklist` → `/sc:task` | Stage 10.5 pre-reflect fan-out (1/phase); terminal Post-Execution Reflection task is the LAST task per phase; index "Pre-Reflect Sign-off" column + `reflect_pre_summary` |
| B | **tl-2** escape hatch | `/sc:tasklist --no-reflect` → `/sc:task` | Both gates skipped; NO terminal reflect task; Stage 10.5 skipped; index SKIPPED/omitted |
| B | **tl-3** STRICT/CPO | `/sc:tasklist` → `/sc:task` | Per-phase COMPLEXITY_SCORE override (`n_cpo≥1 OR n_strict≥2` → floor `deep`/`tier 2`); `depth-map.yaml` records it |
| C (sprint) | **sprint-1/2/3** | `superclaude sprint run <tl-N index>` | Generated bundle (with terminal Post-Execution Reflection task, scanner-visible, checkpoint-is-last preserved) is Sprint-CLI-compatible |

Group C runs AFTER Group B produces the bundles.
