# F-03: `_tier_min_lines` / `_tier_min_lines_assembly` unwired -- tier thresholds are dead code

**Final severity (Stage 2 preliminary)**: CRITICAL
**Pattern tags**: P2, P7
**Identified by**: B-1, C-1, F-5, F-12
**File:line**: `src/superclaude/cli/prd/gates.py:281-292, 367, 459`; consumer at `src/superclaude/cli/prd/executor.py:530, 596-609`

## Evidence

```python
# gates.py:281-292 -- defined but never called
def _tier_min_lines(tier: str) -> int:
    """Return tier-dependent minimum line count for task file gate."""
    return {"lightweight": 200, "standard": 400, "heavyweight": 600}.get(tier, 400)

def _tier_min_lines_assembly(tier: str) -> int:
    """Return tier-dependent minimum line count for assembly gate."""
    return {"lightweight": 400, "standard": 800, "heavyweight": 1500}.get(tier, 800)

# gates.py:367 -- hard-coded 400, not tier-aware
"build-task-file": GateCriteria(
    min_lines=400,  # default standard tier; callers override per tier
    ...
)
# gates.py:459 -- hard-coded 800, not tier-aware
"assembly": GateCriteria(
    min_lines=800,  # default standard tier; callers override per tier
    ...
)

# executor.py:530, 596 -- reads gate.min_lines directly, no tier lookup
gate = GATE_CRITERIA.get(step_id)
...
if gate.min_lines > 0:
    if line_count < gate.min_lines:
```

## Trace

- **Writer (intended)**: `_tier_min_lines` and `_tier_min_lines_assembly` are defined in gates.py:281-292 to compute tier-dependent thresholds. The comments at gates.py:367 and :459 say "callers override per tier" -- the override was intended but never built.
- **Writer (actual)**: `GATE_CRITERIA` is a module-level constant frozen at import time with standard-tier baselines (400, 800).
- **Reader**: `executor.py:530` calls `GATE_CRITERIA.get(step_id)` and `executor.py:596` reads `gate.min_lines` directly. No code path passes `config.tier` through a transform. `grep -r "_tier_min_lines" src/ tests/` returns only the two definition lines.
- **Config path**: `--tier` flag reaches `config.tier` correctly (wired through commands.py, config.py, models.py). Config is read elsewhere for step counts (executor.py:717-738) but never near gate evaluation.
- **Result**: `--tier heavyweight` still demands 400 lines on build-task-file and 800 on assembly instead of 600 and 1500. Lightweight runs are silently over-strict (250 lines pass when the function would allow 200).

## Reproduction sketch

`superclaude prd run "tiny feature" --tier lightweight` -- pipeline halts at build-task-file with "Min lines: <400" against `min_lines=400` even though the lightweight contract is 200 lines. A 500-line task file in heavyweight mode passes despite the spec requiring 600.

## Confidence (aggregated)

0.98 -- Agent B mechanically verified zero call sites via grep. Agent C traced the full config wiring from CLI to executor, confirming the value arrives at config but is never consumed at gate construction. Agent F provided a counterexample: `test_e2e_lightweight_prd` passes with 80-line content under a supposed 200-line floor, confirming the tier table is bypassed at runtime.

## Cross-agent corroboration

- **Agent B** identified the dead functions and verified zero consumers via grep, establishing the definitive mechanical proof.
- **Agent C** traced the full `--tier` wiring path (Click -> resolve_config -> PrdConfig.tier) and confirmed the value arrives correctly but is never read at gate construction, reclassifying Bug 3 from "knob unwired in argparse" to "knob fully wired through config but ignored by GateCriteria construction."
- **Agent F** produced the runtime witness: `test_e2e_lightweight_prd` uses `default_line_count=80` which is below the supposed lightweight floor of 200 and still passes, confirming the tier table is bypassed.
