<!-- Provenance: This document was produced by merge-executor agent -->
<!-- Base: Variant A (brainstorm-resume-fix-A.md) — bug-centric organization -->
<!-- Incorporated: Variant B (brainstorm-resume-fix-B.md), Variant C (brainstorm-resume-fix-C.md) -->
<!-- Refactoring plan: 18 changes applied -->
<!-- Merge date: 2026-03-18 -->

# Design: Fix `--resume` Agent-State Restoration (4 Bugs)

<!-- Source: Base Variant A — title and metadata preserved -->

**Date**: 2026-03-18
**Scope**: `src/superclaude/cli/roadmap/commands.py`, `executor.py`, `models.py`
**Status**: PROPOSAL

---

## Problem Summary

<!-- Source: Base Variant A — problem summary preserved -->

When a user runs `superclaude roadmap run spec.md --agents opus:architect,haiku:analyzer` and later resumes with `superclaude roadmap run spec.md --resume` (no `--agents`), the pipeline:

1. Uses the Click default agents (`opus:architect,haiku:architect`) instead of the original agents
2. Builds steps with wrong output paths (e.g., `roadmap-haiku-architect.md` instead of `roadmap-haiku-analyzer.md`)
3. Gate-checks these phantom paths, finds them missing, marks everything as failed
4. Re-runs all steps with wrong agents, then overwrites the state file -- destroying the original agent config

A second `--resume` is now permanently broken.

<!-- Source: Change #14 (Variant C) — 5-layer defense summary -->

### Defense-in-Depth Summary

The fixes below implement a **5-layer defense model** to break the cascade at every link:

| Layer | Defense | Addresses |
|-------|---------|-----------|
| 1 | `get_parameter_source()` + `None`-default detection | Bug 1 — correct parameter origin detection |
| 2 | State-driven path resolution in `_apply_resume` | Bug 2 — validate paths against state |
| 3 | Dependency-aware selective rerun with `_step_needs_rerun()` | Bug 3 — minimize blast radius |
| 4 | No-progress guard + agent-mismatch guard in `_save_state` | Bug 4 — prevent state corruption |
| 5 | Cascade logging + `--on-conflict` flag | All — observability and operator control |

No single layer is sufficient alone; the design assumes any individual layer may have edge-case gaps and relies on overlapping coverage.

---

## Bug 1: `--resume` Doesn't Restore Agents from State File

<!-- Source: Base Variant A — root cause preserved -->

### Root Cause

Click cannot distinguish "user passed `--agents`" from "Click substituted the default value". The `run()` function at `commands.py:120` always parses whatever string is in `agents`, then at line 137 constructs `RoadmapConfig` with it. By the time `execute_roadmap()` runs at `executor.py:1140`, `_build_steps(config)` uses `config.agents` unconditionally -- BEFORE `_apply_resume()` at line 1151 ever looks at the state file.

### Fix

<!-- Source: Base Variant A — 3-change structure preserved, updated per Change #5 (Variant B's None-default + get_parameter_source approach) -->

**Strategy**: Change Click defaults to `None` and use `click.Context.get_parameter_source()` to detect whether `--agents` was explicitly passed or defaulted. Restore from state file BEFORE building steps.

**Change 1** -- `commands.py`: Change defaults to `None`, detect explicit vs default.

```python
# commands.py -- change Click defaults to None
@click.option("--agents", default=None, help="... Default: opus:architect,haiku:architect")
@click.option(
    "--depth",
    type=click.Choice(["quick", "standard", "deep"], case_sensitive=False),
    default=None,
    help="... Default: standard.",
)

@click.pass_context
def run(
    ctx,
    spec_file: Path,
    agents: str | None,
    depth: str | None,
    resume: bool,
    ...
) -> None:
    from .executor import execute_roadmap

    # Detect whether --agents and --depth were explicitly provided
    agents_source = ctx.get_parameter_source("agents")
    agents_explicit = agents_source == click.core.ParameterSource.COMMANDLINE

    depth_source = ctx.get_parameter_source("depth")
    depth_explicit = depth_source == click.core.ParameterSource.COMMANDLINE

    # agents and depth may be None when user omitted them
    agent_specs = (
        [AgentSpec.parse(a.strip()) for a in agents.split(",")]
        if agents is not None
        else None
    )

    config = RoadmapConfig(
        spec_file=spec_file.resolve(),
        agents=agent_specs,  # may be None
        depth=depth,         # may be None
        ...
    )

    execute_roadmap(
        config, resume=resume, no_validate=no_validate,
        agents_explicit=agents_explicit,
        depth_explicit=depth_explicit,
    )
```

**Change 2** -- `executor.py:execute_roadmap()`: Restore agents from state BEFORE building steps.

```python
def execute_roadmap(
    config: RoadmapConfig,
    resume: bool = False,
    no_validate: bool = False,
    auto_accept: bool = False,
    agents_explicit: bool = True,   # default True = backward compatible
    depth_explicit: bool = True,    # default True = backward compatible
) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)

    # NEW: On --resume with defaulted agents/depth, restore from state file
    if resume:
        config = _restore_from_state(
            config,
            agents_explicit=agents_explicit,
            depth_explicit=depth_explicit,
        )

    # Apply hardcoded defaults for any still-None fields (non-resume or no state)
    if not config.agents:
        config.agents = [AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")]
    if not config.depth:
        config.depth = "standard"

    # NOW build steps with correct agents
    steps = _build_steps(config)
    ...
```

**Key invariant**: `_build_steps(config)` is never called until `config.agents` and `config.depth` are resolved to their correct values.

**Change 3** -- `executor.py`: New helper function.

```python
def _restore_from_state(
    config: RoadmapConfig,
    agents_explicit: bool,
    depth_explicit: bool,
) -> RoadmapConfig:
    """Restore agent/depth specs from .roadmap-state.json when not explicit."""
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)
    if state is None:
        if not agents_explicit or not depth_explicit:
            print(
                "WARNING: --resume with no state file found. "
                "Using defaults for unspecified options.",
                file=sys.stderr, flush=True,
            )
        _log.info("No state file found; using CLI agents for fresh run")
        return config

    # Restore agents from state if user did not explicitly pass --agents
    if not agents_explicit:
        saved_agents = state.get("agents")
        if saved_agents and isinstance(saved_agents, list):
            try:
                restored = [
                    AgentSpec(model=a["model"], persona=a["persona"])
                    for a in saved_agents
                ]
            except (KeyError, TypeError) as exc:
                _log.warning("Malformed agents in state file (%s); using CLI agents", exc)
                return config

            if restored != config.agents:
                agent_str = ", ".join(f"{a.model}:{a.persona}" for a in restored)
                print(
                    f"[roadmap] Restoring agents from state file: {agent_str}",
                    flush=True,
                )
            config.agents = restored
        else:
            _log.warning("State file has no agents key; using CLI agents")

    # Restore depth from state if user did not explicitly pass --depth
    if not depth_explicit:
        saved_depth = state.get("depth")
        if saved_depth:
            if saved_depth != config.depth:
                print(
                    f"WARNING: --depth mismatch.\n"
                    f"  State file depth: {saved_depth}\n"
                    f"  Current depth:    {config.depth}\n"
                    f"  Using state file depth: {saved_depth}\n",
                    file=sys.stderr,
                    flush=True,
                )
            config.depth = saved_depth

    return config
```

### Edge Cases

<!-- Source: Base Variant A — edge cases table preserved -->

| Scenario | Behavior |
|---|---|
| State file missing | Use CLI default agents (fresh run) |
| State file has no `agents` key | Use CLI default agents + warning |
| State file has malformed agents | Use CLI default agents + warning |
| User passes `--agents` explicitly on resume | Honors user's explicit choice |
| User passes same agents as default explicitly | Honors explicit choice (correct) |

<!-- Source: Change #1 (Variant B) — --depth coverage section -->

### `--depth` Coverage

The same detection pattern applies to the `--depth` parameter. Without `None`-default + source detection, `--resume` cannot distinguish "user wants `--depth standard`" from "Click filled in the default `standard`."

Fix 1b (above) handles this uniformly: `depth_explicit` is detected from `get_parameter_source`, and `_restore_from_state` merges depth from the state file with the same explicit-wins precedence as agents.

<!-- Source: Change #4 (Variant C) — differential depth/agents rationale -->

### Differential Treatment: `--depth` vs `--agents`

Although both parameters use the same `None`-default + source detection mechanism, their *semantic behavior* on resume differs:

- **`--agents`**: Always restore from state. The agent selection directly affects which outputs are generated and which file paths are used; using different agents mid-pipeline produces incoherent results and phantom paths.
- **`--depth`**: Auto-restore from state **with a warning**. Depth affects a single step (debate rounds at executor.py:457). A user *might* legitimately want to resume a `deep` run at `standard` depth. The warning ensures this is a conscious choice, not a silent default.

This differs from agents where auto-restore without warning is safe because agents determine file paths, parallel group structure, and step IDs -- there is no valid reason to silently change them.

<!-- Source: Change #15 (Variant C) — depth/agent coupling WARNING validation -->

> **WARNING -- Depth/Agent Coupling**: If the user overrides `--agents` on resume but *not* `--depth`, the combination may produce different quality outputs than the original run (e.g., different debate rounds with different agents). The executor logs this as a WARNING but does not block, since depth affects only debate quality, not structural correctness.

---

## Bug 2: Gate Checks Phantom File Paths Silently

<!-- Source: Base Variant A — Bug 2 root cause and fix preserved -->

### Root Cause

`gate_passed()` at `pipeline/gates.py:33` returns `(False, "File not found: ...")` but `_apply_resume()` at `executor.py:1600` discards the reason string into `_reason` and never logs it. The user sees no distinction between "file doesn't exist because you used wrong agents" and "file exists but fails quality gate".

### Fix

**Change 1** -- `_apply_resume()`: Log gate failure reasons.

```python
# executor.py, inside _apply_resume(), for parallel groups:
for s in entry:
    if s.gate:
        passed, reason = gate_fn(s.output_file, s.gate)
        if not passed:
            _log.info("Gate fail for %s: %s", s.id, reason)
            if reason and "File not found" in reason:
                print(
                    f"[roadmap] WARNING: Expected output missing: {s.output_file.name}\n"
                    f"  Hint: Were different --agents used in the original run?",
                    file=sys.stderr,
                    flush=True,
                )
            all_pass = False
            break
    else:
        all_pass = False
        break

# Same pattern for single-step branch:
if entry.gate:
    passed, reason = gate_fn(entry.output_file, entry.gate)
    if passed:
        skipped += 1
        print(f"[roadmap] Skipping {entry.id} (gate passes)", flush=True)
        continue
    _log.info("Gate fail for %s: %s", entry.id, reason)
    if reason and "File not found" in reason:
        print(
            f"[roadmap] WARNING: Expected output missing: {entry.output_file.name}\n"
            f"  Hint: Were different --agents used in the original run?",
            file=sys.stderr,
            flush=True,
        )
```

This fix becomes a **safety net**. With Bug 1 fixed, this path should rarely trigger, but it provides a clear diagnostic if it does.

---

## Bug 3: `found_failure` Cascade Is Overly Aggressive

<!-- Source: Base Variant A — Bug 3 root cause preserved -->

### Root Cause

`_apply_resume()` lines 1589-1592: once `found_failure = True`, every remaining entry is appended without checking its gate. Steps 3-7 might have valid outputs on disk but are re-run anyway. This wastes significant compute (each step is a Claude subprocess).

### Fix

<!-- Source: Base Variant A — dependency-aware _apply_resume, updated per Change #7 (state-driven paths), Change #8 (_step_needs_rerun), Change #9 (parallel groups), Change #11 (cascade logging), Change #16 (topological order note) -->

**Strategy**: Replace the boolean `found_failure` with dependency-aware selective rerun, state-driven path resolution, and parallel group semantics.

#### `_step_needs_rerun()` Helper

<!-- Source: Change #8 (Variant B) — extracted _step_needs_rerun helper -->

Extract the per-step rerun decision into a testable helper:

```python
def _step_needs_rerun(
    step: Step,
    gate_fn: Callable,
    dirty_outputs: set[Path],
    force_extract: bool,
    state_paths: dict[str, Path],
) -> tuple[bool, str]:
    """Determine if a single step needs re-running.

    A step needs re-run if:
    1. force_extract and step is 'extract', OR
    2. Any of its input files are in the dirty set, OR
    3. Its own gate check fails (using state-recorded paths when available).

    Returns:
        (needs_rerun: bool, reason: str)
    """
    if force_extract and step.id == "extract":
        return True, "spec file changed; forcing extract rerun"

    # If any input was re-generated, must re-run
    if any(inp in dirty_outputs for inp in (step.inputs or [])):
        deps = [str(inp) for inp in (step.inputs or []) if inp in dirty_outputs]
        return True, f"input dependency regenerated: {deps}"

    # Defense-in-depth: use state-recorded path for gate check (Change #7)
    check_path = state_paths.get(step.id, step.output_file)
    if check_path != step.output_file:
        _log.info(
            "Resume: step '%s' using state-recorded path %s "
            "(config-derived: %s)",
            step.id, check_path, step.output_file,
        )

    # Check own gate
    if step.gate:
        passed, reason = gate_fn(check_path, step.gate)
        if passed:
            return False, "gate passes"
        # Log the failure reason
        if reason and "File not found" in reason:
            print(
                f"[roadmap] {step.id}: output missing ({check_path.name})",
                file=sys.stderr, flush=True,
            )
        else:
            print(f"[roadmap] {step.id}: gate failed -- {reason}", flush=True)
        return True, f"gate failed: {reason}"

    # No gate defined -- must run
    return True, "no gate defined"
```

#### `_apply_resume()` -- Dependency-Aware with State Paths and Parallel Groups

```python
def _apply_resume(
    steps: list[Step | list[Step]],
    config: RoadmapConfig,
    gate_fn: Callable,
) -> list[Step | list[Step]]:
    """Apply --resume logic: skip steps whose outputs pass gates.

    Uses dependency tracking: if a step's inputs include the output of a
    step that will be re-run, it must also re-run regardless of gate status.

    Includes state-driven path resolution (Change #7) and parallel group
    semantics (Change #9).
    """
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)
    force_extract = False

    # --- State-driven path resolution (Change #7) ---
    # Build lookup: step_id -> recorded output_file from state,
    # so gate checks validate against real locations, not config-derived paths.
    state_paths: dict[str, Path] = {}
    if state is not None:
        saved_hash = state.get("spec_hash", "")
        current_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()
        if saved_hash and saved_hash != current_hash:
            print(
                f"WARNING: spec-file has changed since last run.\n"
                f"  Last hash: {saved_hash[:12]}...\n"
                f"  Current:   {current_hash[:12]}...\n"
                f"Forcing re-run of extract step.",
                file=sys.stderr,
                flush=True,
            )
            force_extract = True

        # Extract recorded output paths from state
        for step_id, step_data in state.get("steps", {}).items():
            recorded_path = step_data.get("output_file")
            if recorded_path:
                state_paths[step_id] = Path(recorded_path)

    skipped = 0
    result: list[Step | list[Step]] = []
    dirty_outputs: set[Path] = set()  # files that will be regenerated

    # --- Parallel group tracking (Change #9) ---
    # Steps in a parallel group (list[Step]) run concurrently.
    # high_water_mark tracks the furthest completed group index (-1 = none).
    group_index: int = -1

    for entry in steps:
        group_index += 1

        if isinstance(entry, list):
            # Parallel group -- check each step, re-run entire group if any needs it
            group_needs_rerun = False
            rerun_reasons: list[str] = []

            for s in entry:
                needs, reason = _step_needs_rerun(
                    s, gate_fn, dirty_outputs, force_extract, state_paths,
                )
                if needs:
                    group_needs_rerun = True
                    rerun_reasons.append(f"{s.id}: {reason}")

            if group_needs_rerun:
                # --- Cascade logging (Change #11) ---
                _log.info(
                    "Parallel group [%s] marked for rerun: %s",
                    ", ".join(s.id for s in entry),
                    "; ".join(rerun_reasons),
                )
                result.append(entry)
                # Mark all group outputs as dirty (atomic group completion)
                for s in entry:
                    dirty_outputs.add(s.output_file)
            else:
                skipped += len(entry)
                print(
                    f"[roadmap] Skipping {', '.join(s.id for s in entry)} (gates pass)",
                    flush=True,
                )
        else:
            # Single step
            needs, reason = _step_needs_rerun(
                entry, gate_fn, dirty_outputs, force_extract, state_paths,
            )

            if needs:
                # --- Cascade logging (Change #11) ---
                _log.info("Step '%s' marked for rerun: %s", entry.id, reason)
                dirty_outputs.add(entry.output_file)
                result.append(entry)
            else:
                skipped += 1
                print(f"[roadmap] Skipping {entry.id} (gate passes)", flush=True)

    if skipped > 0:
        print(f"[roadmap] Skipped {skipped} steps (gates pass)", flush=True)

    if not result:
        print("[roadmap] All steps already pass gates. Nothing to do.", flush=True)

    return result
```

### Why This Is Safe

<!-- Source: Base Variant A — safety rationale preserved -->

The dependency graph is already encoded: each `Step` has an `inputs` list of file paths. If step 2's output is being regenerated, step 3 which consumes it must also re-run (stale input). But if step 5 only depends on step 4's output and step 4 passes its gate, step 5 can be checked independently.

The existing pipeline order guarantees topological sort, so a single forward pass through the step list is sufficient.

<!-- Source: Change #16 (Variant C) — topological order note -->

> **Note -- Topological Ordering**: The dependency-aware rerun in `_apply_resume` assumes steps are processed in topological order (dependencies before dependents). If dirty outputs propagate forward, a simple linear scan will miss transitive invalidation. The `steps` list MUST be topologically sorted before `_apply_resume` is called. The current pipeline already guarantees this, but any future step-reordering must preserve the invariant.

---

## Bug 4: `_save_state` Overwrites State with Wrong Agents

<!-- Source: Base Variant A — Bug 4 root cause and fix preserved -->

### Root Cause

`_save_state()` at `executor.py:879` writes `config.agents` (current session's agents) to the state file unconditionally. On a broken resume where Bug 1 caused wrong agents to be loaded, this destroys the original correct agent config.

### Fix

With Bug 1 fixed, `config.agents` will always be correct by the time `_save_state` runs. However, as a defense-in-depth measure:

<!-- Source: Base Variant A + Change #10 (no-progress guard from Variant C) + Change #17 (atomic writes from Variant C) -->

**Change 1** -- `_save_state()`: Defense-in-depth with no-progress guard, agent-mismatch guard, and atomic writes.

```python
def _save_state(
    config: RoadmapConfig,
    results: list[StepResult],
    remediate_metadata: dict | None = None,
    certify_metadata: dict | None = None,
) -> None:
    """Write .roadmap-state.json -- only when the pipeline made progress."""
    state_file = config.output_dir / ".roadmap-state.json"

    # --- No-progress guard (Change #10) ---
    # If no steps passed, do not write state -- prevents corruption from
    # broken resumes that fail immediately.
    any_passed = any(r.status == StepStatus.PASS for r in results if r.step)
    if not any_passed:
        _log.info(
            "State not saved: no steps passed in this run "
            "(%d results, all non-PASS)",
            len(results),
        )
        return

    existing = read_state(state_file)

    # --- Agent-mismatch guard (Change #10) ---
    # Even if a step passes (e.g., extract is agent-independent), writing state
    # with wrong agents would corrupt the agent record for subsequent resumes.
    if existing is not None:
        saved_agents = existing.get("agents", [])
        current_agents = [
            {"model": a.model, "persona": a.persona} for a in config.agents
        ]
        if saved_agents and saved_agents != current_agents:
            # Check if any generate step ran -- if so, the agent change is intentional
            generate_ran = any(
                r.step and r.step.id.startswith("generate-")
                and r.status == StepStatus.PASS
                for r in results
            )
            if not generate_ran:
                _log.warning(
                    "Agents differ from state file and no generate steps ran; "
                    "preserving original agents in state"
                )
                return

    spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()

    agents_to_save = [{"model": a.model, "persona": a.persona} for a in config.agents]

    state = {
        "schema_version": 1,
        "spec_file": str(config.spec_file),
        "spec_hash": spec_hash,
        "agents": agents_to_save,
        "depth": config.depth,
        "last_run": datetime.now(timezone.utc).isoformat(),
        "steps": {
            r.step.id: {
                "status": r.status.value,
                "output_file": str(r.step.output_file) if r.step.output_file else None,
            }
            for r in results
            if r.step
        },
    }

    # Merge with existing state (preserve steps not in this run)
    if existing:
        existing_steps = existing.get("steps", {})
        for step_id, step_data in existing_steps.items():
            if step_id not in state["steps"]:
                state["steps"][step_id] = step_data

    # --- Atomic write (Change #17) ---
    # Write to temp file then rename, so a crash mid-write cannot corrupt state.
    import os
    tmp_path = state_file.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(state, indent=2, default=str))
    os.replace(tmp_path, state_file)

    _log.info("State saved: %d steps completed", len(state["steps"]))
```

**Simpler alternative** (if full defense is deferred):

Since Bug 1 ensures `config.agents` is always correct on resume, the simplest defense is a pre-save log:

```python
# In _save_state, after reading existing state:
if existing and "agents" in existing:
    saved = existing["agents"]
    current = [{"model": a.model, "persona": a.persona} for a in config.agents]
    if saved != current:
        _log.info(
            "Agent config changed: %s -> %s",
            saved, current,
        )
```

I recommend the **full defense-in-depth version** because the cost is ~25 lines and it prevents data loss in any future scenario where `config.agents` might be wrong.

<!-- Source: Change #17 (Variant C) — atomic write note -->

> **Note -- Atomic State Writes**: The `os.replace()` call is atomic on POSIX systems -- the state file is either the old version or the new version, never a partial write. On Windows, `os.replace()` also provides atomicity (unlike `os.rename()` which fails if the target exists). This is critical for crash safety during `_save_state`.

---

<!-- Source: Change #6 (Variant B) — --on-conflict flag design -->

## Conflict Resolution: `--on-conflict` Flag

For non-interactive contexts (CI pipelines, cron jobs), add an `--on-conflict` option to control behavior when `--resume` detects a parameter mismatch between the state file and the current invocation:

```python
@click.option(
    "--on-conflict",
    type=click.Choice(["ask", "override", "fail"]),
    default="ask",
    help="Behavior when resumed state conflicts with CLI args",
)
```

| Mode | Behavior | Use Case |
|------|----------|----------|
| `ask` (default) | Prompt user to choose CLI or state value | Interactive terminal |
| `override` | CLI values silently win | CI with intentional overrides |
| `fail` | Exit with error code 1 and diagnostic | CI with strict reproducibility |

Implementation in `_restore_from_state`:

```python
def _resolve_conflict(param: str, cli_val, state_val, mode: str):
    """Resolve a conflict between CLI and state-file parameter values."""
    if cli_val == state_val:
        return cli_val
    if mode == "override":
        _log.info("Conflict on '%s': using CLI value '%s' (override mode)", param, cli_val)
        return cli_val
    if mode == "fail":
        raise SystemExit(
            f"ERROR: Parameter '{param}' conflicts: CLI='{cli_val}' vs state='{state_val}'. "
            "Use --on-conflict=override to force CLI values."
        )
    # mode == "ask"
    return click.prompt(
        f"'{param}' differs: CLI='{cli_val}', state='{state_val}'. Use which?",
        type=click.Choice(["cli", "state"]),
    )
```

---

## Implementation Order

<!-- Source: Base Variant A — implementation order preserved -->

1. **Bug 1 first** -- this is the root cause. All other bugs are consequences or amplifiers.
2. **Bug 4 second** -- defense-in-depth for the state file.
3. **Bug 3 third** -- the `_apply_resume` rewrite replaces the naive `found_failure` cascade.
4. **Bug 2 last** -- diagnostic improvement, folded into the Bug 3 rewrite.

Bugs 2 and 3 share the same function (`_apply_resume`), so they should be implemented together as a single rewrite.

<!-- Source: Change #3 (Variant B) — fix interaction matrix -->

### Fix Interaction Matrix

What happens when each fix is applied *alone* (without the others):

| Applied Alone | Result |
|--------------|--------|
| Bug 1 only | Agents correct, but cascade still overwrites valid outputs (Bug 3) |
| Bug 2 only | Better diagnostics but still uses wrong agents |
| Bug 3 only | Independent checking, but on phantom paths from wrong agents |
| Bug 4 only | State preserved, but next resume still builds wrong steps |
| **Bug 1 + Bug 4** | **Minimum viable fix** -- agents correct and state preserved |

> **Recommendation**: Bug 1 + Bug 4 is the minimum viable fix. Bug 2 and Bug 3 are high-value improvements but the pipeline will produce correct results with only Bugs 1+4 fixed.

---

## Files Changed

<!-- Source: Base Variant A — files table preserved and extended -->

| File | Changes | Bug(s) |
|---|---|---|
| `commands.py` | Change `--agents`/`--depth` defaults to `None`; add `@click.pass_context`; detect `agents_source`/`depth_source`; pass explicit flags; add `--on-conflict` option | 1, (conflict) |
| `executor.py` | Add `_restore_from_state()`, `_step_needs_rerun()`; rewrite `_apply_resume()` with dependency tracking + state-driven paths + parallel groups; add defense-in-depth to `_save_state()`; add gate failure logging | 1, 2, 3, 4 |
| `models.py` | No changes needed (`AgentSpec.__eq__` works via dataclass default) | -- |

<!-- Source: Change #18 (Variant C) — estimated diff size -->

### Estimated Diff Size

| File | Lines Added | Lines Modified | Lines Removed |
|------|-------------|----------------|---------------|
| `commands.py` | ~25 | ~10 | ~5 |
| `executor.py` | ~200 | ~40 | ~25 |
| **Total** | **~225** | **~50** | **~30** |

Test code: ~120 lines added in `tests/roadmap/test_resume_restore.py`.

---

<!-- Source: Change #2 (Variant B) — CLI option audit table -->

## CLI Option Audit

All CLI options and their resume behavior:

| Option | Current Default | Stored in State? | Risk if Wrong on Resume | Fix Needed? |
|--------|----------------|-----------------|------------------------|-------------|
| `--agents` | `"opus:architect,haiku:architect"` | Yes | **HIGH** -- changes file paths and step IDs | Yes (None-default) |
| `--depth` | `"standard"` | Yes | **MEDIUM** -- changes debate rounds | Yes (None-default) |
| `--output` | `None` (derived from spec_file) | Implicit via `spec_file` | LOW -- path derivation is stable | No |
| `--model` | `""` | No | LOW -- empty means per-agent default | No |
| `--max-turns` | `100` | No | LOW -- performance not correctness | No |
| `--retrospective` | `None` | No | LOW -- only affects extract prompt | No |

Only `--agents` and `--depth` need the `None`-default treatment.

---

## Test Plan

<!-- Source: Base Variant A — original 6 tests preserved + Change #13 (expanded to ~17 tests from Variant B and C) -->

### Unit Tests: Agent Restoration (Bug 1)

#### Test 1: Agent Restoration from State

```python
def test_restore_agents_from_state_file(tmp_path):
    """Resume without --agents restores original agents from state."""
    state = {
        "schema_version": 1,
        "agents": [
            {"model": "opus", "persona": "architect"},
            {"model": "haiku", "persona": "analyzer"},
        ],
        "spec_hash": "abc123",
    }
    (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

    config = RoadmapConfig(
        spec_file=tmp_path / "spec.md",
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        output_dir=tmp_path,
        work_dir=tmp_path,
    )

    restored = _restore_from_state(config, agents_explicit=False, depth_explicit=True)
    assert restored.agents[1].persona == "analyzer"
    assert restored.agents[1].model == "haiku"
```

#### Test 2: Explicit `--agents` Overrides State

```python
def test_explicit_agents_override_state(tmp_path):
    """When --agents is passed explicitly, it overrides state file."""
    state = {
        "agents": [{"model": "opus", "persona": "architect"},
                    {"model": "haiku", "persona": "analyzer"}],
    }
    (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

    config = RoadmapConfig(
        agents=[AgentSpec("sonnet", "security"), AgentSpec("haiku", "qa")],
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )

    # agents_explicit=True means _restore_from_state does not overwrite
    restored = _restore_from_state(config, agents_explicit=True, depth_explicit=True)
    assert restored.agents[0].persona == "security"
```

#### Test 3: Missing State File Graceful Fallback

```python
def test_restore_agents_no_state_file(tmp_path):
    """Missing state file falls back to CLI agents."""
    config = RoadmapConfig(
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )

    restored = _restore_from_state(config, agents_explicit=False, depth_explicit=False)
    assert restored.agents == config.agents  # unchanged
```

<!-- Source: Change #13 (Variant B) — depth restoration test -->

#### Test 4: Depth Restoration from State

```python
def test_resume_restores_depth_from_state(tmp_path):
    """Resume without --depth restores original depth from state."""
    state = {
        "agents": [{"model": "opus", "persona": "architect"}],
        "depth": "deep",
    }
    (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

    config = RoadmapConfig(
        agents=None, depth=None,
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )

    restored = _restore_from_state(config, agents_explicit=False, depth_explicit=False)
    assert restored.depth == "deep"
```

### Unit Tests: Gate Diagnostics (Bug 2)

#### Test 5: Phantom File Path Warning

```python
def test_resume_warns_on_missing_output(tmp_path, capsys):
    """Gate failure on missing file emits diagnostic hint."""
    steps = [Step(
        id="generate-haiku-architect",
        prompt="...",
        output_file=tmp_path / "roadmap-haiku-architect.md",  # doesn't exist
        gate=GENERATE_A_GATE,
    )]

    def mock_gate(path, criteria):
        return (False, f"File not found: {path}")

    result = _apply_resume(steps, config, mock_gate)
    captured = capsys.readouterr()
    assert "Expected output missing" in captured.err
```

### Unit Tests: Dependency-Aware Resume (Bug 3)

#### Test 6: Dependency-Aware Skip

```python
def test_resume_skips_independent_passing_steps(tmp_path):
    """Steps after a failure are still skipped if their gates pass
    and they don't depend on regenerated outputs."""
    extraction = tmp_path / "extraction.md"
    roadmap_a = tmp_path / "roadmap-opus-architect.md"
    merge_file = tmp_path / "roadmap.md"
    test_strat = tmp_path / "test-strategy.md"

    # extraction exists and passes, generate fails, merge passes, test passes
    extraction.write_text("x\n" * 100)
    merge_file.write_text("x\n" * 200)
    test_strat.write_text("x\n" * 100)

    steps = [
        Step(id="extract", output_file=extraction, gate=EXTRACT_GATE, ...),
        [Step(id="generate-a", output_file=roadmap_a, gate=GENERATE_A_GATE,
              inputs=[extraction], ...)],
        Step(id="merge", output_file=merge_file, gate=MERGE_GATE,
             inputs=[roadmap_a], ...),  # depends on regenerated output
        Step(id="test-strategy", output_file=test_strat, gate=TEST_STRATEGY_GATE,
             inputs=[merge_file], ...),  # depends on merge (transitive)
    ]

    result = _apply_resume(steps, config, gate_passed)
    # extract skipped, generate re-runs, merge re-runs (input regenerated),
    # test-strategy re-runs (input regenerated)
    result_ids = [s.id if isinstance(s, Step) else [x.id for x in s] for s in result]
    assert "extract" not in str(result_ids)
    assert "generate-a" in str(result_ids)
    assert "merge" in str(result_ids)
```

<!-- Source: Change #13 (Variant B) — dirty propagation test -->

#### Test 7: Dirty Output Propagation

```python
def test_resume_dirty_propagation(tmp_path):
    """When step 1 re-runs, dependent steps re-run, but independent steps skip."""
    # Setup: step 1 failed, steps 2a/2b depend on step 1, step 3 depends on step 2
    step1_out = tmp_path / "step1.md"
    step2a_out = tmp_path / "step2a.md"
    step2a_out.write_text("valid output\n" * 100)
    step3_out = tmp_path / "step3.md"
    step3_out.write_text("valid output\n" * 100)

    steps = [
        Step(id="step1", output_file=step1_out, gate=GATE, inputs=[]),
        [
            Step(id="step2a", output_file=step2a_out, gate=GATE, inputs=[step1_out]),
        ],
        Step(id="step3", output_file=step3_out, gate=GATE, inputs=[step2a_out]),
    ]

    def gate_fn(path, criteria):
        if path.exists() and path.stat().st_size > 0:
            return (True, "")
        return (False, f"File not found: {path}")

    result = _apply_resume(steps, config, gate_fn)
    result_ids = [s.id if isinstance(s, Step) else [x.id for x in s] for s in result]
    assert "step1" in str(result_ids)    # failed -- must rerun
    assert "step2a" in str(result_ids)   # input dirty -- must rerun
    assert "step3" in str(result_ids)    # transitive dirty -- must rerun
```

<!-- Source: Change #13 — state-driven path resolution test from Variant C -->

#### Test 8: State-Driven Path Resolution

```python
def test_apply_resume_uses_state_paths(tmp_path):
    """_apply_resume gate-checks state-recorded paths, not config-derived paths."""
    # State records output at a different path than config would derive
    state_path = tmp_path / "roadmap-haiku-analyzer.md"
    state_path.write_text("valid output\n" * 100)

    config_path = tmp_path / "roadmap-haiku-architect.md"  # wrong path

    state = {
        "spec_hash": hashlib.sha256(b"spec content").hexdigest(),
        "steps": {
            "generate-haiku": {"output_file": str(state_path)},
        },
    }
    (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

    steps = [Step(
        id="generate-haiku",
        output_file=config_path,  # config derives wrong path
        gate=GATE,
        inputs=[],
    )]

    def gate_fn(path, criteria):
        if path.exists():
            return (True, "")
        return (False, f"File not found: {path}")

    result = _apply_resume(steps, config, gate_fn)
    # Should pass because state-recorded path exists
    assert len(result) == 0
```

### Unit Tests: State Preservation (Bug 4)

#### Test 9: State File Not Corrupted on Broken Resume

```python
def test_save_state_preserves_agents_when_no_generate_ran(tmp_path):
    """If no generate steps ran successfully, state preserves original agents."""
    original_state = {
        "agents": [{"model": "opus", "persona": "architect"},
                    {"model": "haiku", "persona": "analyzer"}],
    }
    (tmp_path / ".roadmap-state.json").write_text(json.dumps(original_state))

    config = RoadmapConfig(
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )

    # Results with no generate steps (only extract ran)
    results = [StepResult(step=Step(id="extract", ...), status=StepStatus.PASS, ...)]

    _save_state(config, results)

    saved = json.loads((tmp_path / ".roadmap-state.json").read_text())
    assert saved["agents"][1]["persona"] == "analyzer"  # preserved, not overwritten
```

<!-- Source: Change #13 — no-progress guard test from Variant C -->

#### Test 10: No-Progress Guard Prevents Write

```python
def test_save_state_no_progress_no_write(tmp_path):
    """_save_state does not write when no steps passed."""
    original = {"agents": [{"model": "opus", "persona": "architect"}]}
    state_file = tmp_path / ".roadmap-state.json"
    state_file.write_text(json.dumps(original))
    mtime_before = state_file.stat().st_mtime

    config = RoadmapConfig(
        agents=[AgentSpec("opus", "architect")],
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )

    # All results are FAIL
    results = [StepResult(step=Step(id="extract", ...), status=StepStatus.FAIL, ...)]

    _save_state(config, results)

    # State file should not have been modified
    assert state_file.stat().st_mtime == mtime_before
```

### Integration Tests

#### Test 11: Full Resume Cycle

```python
def test_full_resume_cycle_different_agents(tmp_path):
    """Run with custom agents, crash, resume -- agents restored, no data loss."""
    # First run with custom agents
    config = RoadmapConfig(
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "analyzer")],
        depth="deep",
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )
    (tmp_path / "spec.md").write_text("# Spec")

    # Simulate partial run that saves state
    results = [
        StepResult(step=Step(id="extract", ...), status=StepStatus.PASS, ...),
        StepResult(step=Step(id="generate-opus-architect", ...), status=StepStatus.PASS, ...),
        StepResult(step=Step(id="generate-haiku-analyzer", ...), status=StepStatus.PASS, ...),
    ]
    _save_state(config, results)

    # Resume with default config (simulating Click defaults -> None)
    resume_config = RoadmapConfig(
        agents=None, depth=None,
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )
    restored = _restore_from_state(resume_config, agents_explicit=False, depth_explicit=False)

    assert restored.agents[1].persona == "analyzer"
    assert restored.depth == "deep"
```

<!-- Source: Change #13 (Variant B) — double resume stability test -->

#### Test 12: Double Resume State Stability

```python
def test_double_resume_state_stability(tmp_path):
    """Run, resume, resume again -- state file agents stable across all three."""
    original_agents = [
        AgentSpec("opus", "architect"),
        AgentSpec("haiku", "analyzer"),
    ]
    (tmp_path / "spec.md").write_text("# Spec")

    # First run saves state
    config1 = RoadmapConfig(
        agents=original_agents, depth="deep",
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )
    results1 = [StepResult(step=Step(id="extract", ...), status=StepStatus.PASS, ...)]
    _save_state(config1, results1)

    # First resume
    config2 = RoadmapConfig(agents=None, depth=None, output_dir=tmp_path,
                             work_dir=tmp_path, spec_file=tmp_path / "spec.md")
    restored2 = _restore_from_state(config2, agents_explicit=False, depth_explicit=False)
    _save_state(restored2, results1)

    # Second resume
    config3 = RoadmapConfig(agents=None, depth=None, output_dir=tmp_path,
                             work_dir=tmp_path, spec_file=tmp_path / "spec.md")
    restored3 = _restore_from_state(config3, agents_explicit=False, depth_explicit=False)

    assert restored3.agents == original_agents
    assert restored3.depth == "deep"
```

<!-- Source: Change #13 (Variant B) — explicit override test -->

#### Test 13: Resume with Explicit Override

```python
def test_resume_with_explicit_override(tmp_path):
    """Resume with --agents B overrides state's agents A."""
    state = {
        "agents": [{"model": "opus", "persona": "architect"},
                    {"model": "haiku", "persona": "analyzer"}],
        "depth": "deep",
    }
    (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

    config = RoadmapConfig(
        agents=[AgentSpec("sonnet", "qa"), AgentSpec("haiku", "qa")],
        depth="standard",
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )

    # Both explicit
    restored = _restore_from_state(config, agents_explicit=True, depth_explicit=True)
    assert restored.agents[0].model == "sonnet"
    assert restored.depth == "standard"
```

### Edge Case Tests

<!-- Source: Change #13 — edge case tests from all variants -->

#### Test 14: Corrupted State File

```python
def test_corrupted_state_file_graceful(tmp_path, caplog):
    """Resume with corrupted state file warns and uses CLI agents."""
    (tmp_path / ".roadmap-state.json").write_text("NOT VALID JSON{{{")
    config = RoadmapConfig(
        agents=[AgentSpec("opus", "architect")],
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )

    restored = _restore_from_state(config, agents_explicit=False, depth_explicit=False)
    # read_state returns None for corrupted JSON; _restore_from_state logs warning
    assert restored.agents == config.agents  # unchanged
```

#### Test 15: State File from Different Spec

```python
def test_resume_with_changed_spec(tmp_path, capsys):
    """Resume after spec file changed forces extract re-run."""
    (tmp_path / "spec.md").write_text("# Updated spec")
    state = {
        "spec_hash": "old_hash_that_does_not_match",
        "agents": [{"model": "opus", "persona": "architect"}],
        "steps": {},
    }
    (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

    config = RoadmapConfig(
        agents=[AgentSpec("opus", "architect")],
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )

    extract_step = Step(id="extract", output_file=tmp_path / "extract.md",
                        gate=EXTRACT_GATE, inputs=[])

    def gate_fn(path, criteria):
        return (True, "")

    result = _apply_resume([extract_step], config, gate_fn)
    captured = capsys.readouterr()
    assert "spec-file has changed" in captured.err
    assert len(result) == 1
```

#### Test 16: `_step_needs_rerun` Returns Reason String

```python
def test_step_needs_rerun_returns_reason():
    """_step_needs_rerun returns descriptive reason for rerun."""
    step = Step(id="merge", output_file=Path("/tmp/merge.md"),
                gate=GATE, inputs=[Path("/tmp/diff.md")])

    needs, reason = _step_needs_rerun(
        step, gate_fn=lambda p, c: (True, ""),
        dirty_outputs={Path("/tmp/diff.md")},
        force_extract=False,
        state_paths={},
    )
    assert needs is True
    assert "dependency" in reason.lower() or "regenerated" in reason.lower()
```

#### Test 17: Atomic Write Crash Safety

```python
def test_atomic_write_crash_safety(tmp_path, monkeypatch):
    """If write fails mid-way, original state file is intact."""
    state_file = tmp_path / ".roadmap-state.json"
    original = {
        "agents": [{"model": "opus", "persona": "architect"}],
        "schema_version": 1,
    }
    state_file.write_text(json.dumps(original))

    config = RoadmapConfig(
        agents=[AgentSpec("opus", "architect")],
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )
    (tmp_path / "spec.md").write_text("# Spec")

    # Simulate crash during tmp write
    original_write_text = Path.write_text
    def crash_on_tmp(self, *args, **kwargs):
        if str(self).endswith(".tmp"):
            raise IOError("Disk full")
        return original_write_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", crash_on_tmp)

    results = [StepResult(step=Step(id="extract", ...), status=StepStatus.PASS, ...)]
    with pytest.raises(IOError):
        _save_state(config, results)

    # Original file should be untouched
    saved = json.loads(state_file.read_text())
    assert saved == original
```

---

## Risk Assessment

<!-- Source: Base Variant A — risk table preserved and extended -->

| Risk | Likelihood | Mitigation |
|---|---|---|
| `get_parameter_source` not available in older Click | Low (added Click 8.0, we require >=8.0) | Version check in CI |
| `Step.inputs` is `None` for some steps | Medium | `(s.inputs or [])` handles it |
| State file written by older version has no `agents` | Medium | Explicit fallback to CLI agents |
| Dependency tracking misses transitive deps | Low | Forward pass + dirty_outputs set propagates correctly |
| Race condition: two resume runs on same dir | Low (pre-existing) | Out of scope; state file locking is a separate concern |
| State-driven path stale if state file is from older format | Low | Falls back to config-derived path when state entry missing |
| No-progress guard blocks legitimate state update | Very Low | Only blocks when zero steps PASS -- if everything failed, there is nothing to save |
| `--on-conflict` prompts in headless CI | Low | Default is `ask` but CI scripts should pass `--on-conflict=fail` or `--on-conflict=override` |

---

## Backward Compatibility

<!-- Source: Base Variant A — backward compatibility preserved + Change #12 (expanded migration analysis from Variant B and C) -->

### State File Format Migration

<!-- Source: Change #12 (Variant B) — expanded backward compatibility -->

State files written before this fix will have `agents` and `depth` keys. The new code reads these keys, so existing state files are compatible. No `schema_version` bump is needed -- the state file format is unchanged; we are reading existing fields that were already being written.

| State File Scenario | Behavior |
|--------------------|----------|
| Has `agents` and `depth` keys (normal) | Restored normally on `--resume` |
| Missing `agents` key (very old format) | Falls back to CLI agents with warning |
| Missing `depth` key | Falls back to CLI depth (or Click default) |
| Has extra unknown keys (forward-compat) | Ignored; preserved on merge-save |

### CLI Interface Compatibility

- Changing `--agents` and `--depth` defaults to `None` is backward-compatible for non-resume runs: the `execute_roadmap()` function applies the same hardcoded defaults when values are `None`.
- The only behavioral change is on `--resume`, where the state file now takes precedence over Click defaults.
- New `--on-conflict` option defaults to `ask`, which is implicitly the current behavior (fail silently). The only difference is that conflicts are now *visible*.
- No flags are removed or renamed.

### Behavioral Changes

| Behavior | Before | After |
|----------|--------|-------|
| `--resume` agent handling | Silently uses Click defaults | Restores from state file |
| `--resume` depth handling | Silently uses Click default | Restores from state file with warning |
| Gate failure output | Reason silently discarded | Logged with diagnostic hint |
| Step rerun on failure | All downstream steps blindly | Only dependency-affected steps |
| State file on save | Overwrites unconditionally | Guarded by no-progress + agent-mismatch checks |
| State file write mechanism | Direct `write_text` | Atomic `write_text` + `os.replace` |

- Existing explicit `--agents` usage: **no change**. `agents_explicit=True` preserves current behavior.
- Existing state files without `agents` key: **graceful fallback** to CLI agents.
- `_apply_resume` return type: **unchanged** (`list[Step | list[Step]]`).
- `execute_roadmap` signature: new optional kwargs `agents_explicit` and `depth_explicit` default to `True`, so all existing callers are unaffected.
