# Design: Fix `--resume` Agent-State Restoration (4 Bugs)

**Date**: 2026-03-18
**Scope**: `src/superclaude/cli/roadmap/commands.py`, `executor.py`, `models.py`
**Status**: PROPOSAL

---

## Problem Summary

When a user runs `superclaude roadmap run spec.md --agents opus:architect,haiku:analyzer` and later resumes with `superclaude roadmap run spec.md --resume` (no `--agents`), the pipeline:

1. Uses the Click default agents (`opus:architect,haiku:architect`) instead of the original agents
2. Builds steps with wrong output paths (e.g., `roadmap-haiku-architect.md` instead of `roadmap-haiku-analyzer.md`)
3. Gate-checks these phantom paths, finds them missing, marks everything as failed
4. Re-runs all steps with wrong agents, then overwrites the state file -- destroying the original agent config

A second `--resume` is now permanently broken.

---

## Bug 1: `--resume` Doesn't Restore Agents from State File

### Root Cause

Click cannot distinguish "user passed `--agents`" from "Click substituted the default value". The `run()` function at `commands.py:120` always parses whatever string is in `agents`, then at line 137 constructs `RoadmapConfig` with it. By the time `execute_roadmap()` runs at `executor.py:1140`, `_build_steps(config)` uses `config.agents` unconditionally -- BEFORE `_apply_resume()` at line 1151 ever looks at the state file.

### Fix

**Strategy**: Use `click.Context.get_parameter_source()` to detect whether `--agents` was explicitly passed or defaulted.

**Change 1** -- `commands.py`: Detect default vs explicit agents.

```python
# commands.py:99 -- add ctx parameter
@click.pass_context
def run(
    ctx,
    spec_file: Path,
    agents: str,
    ...
) -> None:
    ...
    # Detect whether --agents was explicitly provided
    agents_source = ctx.get_parameter_source("agents")
    agents_explicit = agents_source == click.core.ParameterSource.COMMANDLINE

    agent_specs = [AgentSpec.parse(a.strip()) for a in agents.split(",")]

    config = RoadmapConfig(
        spec_file=spec_file.resolve(),
        agents=agent_specs,
        ...
    )

    execute_roadmap(config, resume=resume, no_validate=no_validate,
                    agents_explicit=agents_explicit)
```

**Change 2** -- `executor.py:execute_roadmap()`: Restore agents from state BEFORE building steps.

```python
def execute_roadmap(
    config: RoadmapConfig,
    resume: bool = False,
    no_validate: bool = False,
    auto_accept: bool = False,
    agents_explicit: bool = True,  # default True = backward compatible
) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)

    # NEW: On --resume with defaulted agents, restore from state file
    if resume and not agents_explicit:
        config = _restore_agents_from_state(config)

    steps = _build_steps(config)
    ...
```

**Change 3** -- `executor.py`: New helper function.

```python
def _restore_agents_from_state(config: RoadmapConfig) -> RoadmapConfig:
    """Restore agent specs from .roadmap-state.json when --agents wasn't explicit."""
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)
    if state is None:
        _log.info("No state file found; using CLI agents for fresh run")
        return config

    saved_agents = state.get("agents")
    if not saved_agents or not isinstance(saved_agents, list):
        _log.warning("State file has no agents key; using CLI agents")
        return config

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
    return config
```

### Edge Cases

| Scenario | Behavior |
|---|---|
| State file missing | Use CLI default agents (fresh run) |
| State file has no `agents` key | Use CLI default agents + warning |
| State file has malformed agents | Use CLI default agents + warning |
| User passes `--agents` explicitly on resume | Honors user's explicit choice |
| User passes same agents as default explicitly | Honors explicit choice (correct) |

---

## Bug 2: Gate Checks Phantom File Paths Silently

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

### Root Cause

`_apply_resume()` lines 1589-1592: once `found_failure = True`, every remaining entry is appended without checking its gate. Steps 3-7 might have valid outputs on disk but are re-run anyway. This wastes significant compute (each step is a Claude subprocess).

### Fix

**Strategy**: Replace the boolean `found_failure` with a `must_rerun` flag that is set when a step fails, but also allow subsequent steps to be skipped if their gates pass AND none of their declared `inputs` are outputs of a step that will be re-run.

However, the simpler and safer approach is: **continue gate-checking all steps, but track which output files will be regenerated, and force re-run of any step whose inputs overlap with regenerated outputs**.

```python
def _apply_resume(
    steps: list[Step | list[Step]],
    config: RoadmapConfig,
    gate_fn: Callable,
) -> list[Step | list[Step]]:
    """Apply --resume logic: skip steps whose outputs pass gates.

    Uses dependency tracking: if a step's inputs include the output of a
    step that will be re-run, it must also re-run regardless of gate status.
    """
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)
    force_extract = False
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

    skipped = 0
    result: list[Step | list[Step]] = []
    regenerated_outputs: set[Path] = set()  # files that will be regenerated

    for entry in steps:
        if isinstance(entry, list):
            # Parallel group
            group_needs_rerun = False

            # Check if any step in group depends on a regenerated output
            for s in entry:
                if any(inp in regenerated_outputs for inp in (s.inputs or [])):
                    group_needs_rerun = True
                    break

            if not group_needs_rerun:
                # Gate-check each step in group
                all_pass = True
                for s in entry:
                    if s.gate:
                        passed, reason = gate_fn(s.output_file, s.gate)
                        if not passed:
                            _log.info("Gate fail for %s: %s", s.id, reason)
                            if reason and "File not found" in reason:
                                print(
                                    f"[roadmap] WARNING: Expected output missing: "
                                    f"{s.output_file.name}",
                                    file=sys.stderr, flush=True,
                                )
                            all_pass = False
                            break
                    else:
                        all_pass = False
                        break
                group_needs_rerun = not all_pass

            if group_needs_rerun:
                result.append(entry)
                for s in entry:
                    regenerated_outputs.add(s.output_file)
            else:
                skipped += len(entry)
                print(
                    f"[roadmap] Skipping {', '.join(s.id for s in entry)} (gates pass)",
                    flush=True,
                )
        else:
            # Single step
            needs_rerun = False

            # Force re-run of extract on stale spec
            if force_extract and entry.id == "extract":
                needs_rerun = True
            # Check dependency on regenerated outputs
            elif any(inp in regenerated_outputs for inp in (entry.inputs or [])):
                needs_rerun = True
            elif entry.gate:
                passed, reason = gate_fn(entry.output_file, entry.gate)
                if passed:
                    skipped += 1
                    print(f"[roadmap] Skipping {entry.id} (gate passes)", flush=True)
                    continue
                else:
                    _log.info("Gate fail for %s: %s", entry.id, reason)
                    needs_rerun = True
            else:
                needs_rerun = True

            if needs_rerun:
                result.append(entry)
                regenerated_outputs.add(entry.output_file)

    if skipped > 0:
        print(f"[roadmap] Skipped {skipped} steps (gates pass)", flush=True)

    if not result:
        print("[roadmap] All steps already pass gates. Nothing to do.", flush=True)

    return result
```

### Why This Is Safe

The dependency graph is already encoded: each `Step` has an `inputs` list of file paths. If step 2's output is being regenerated, step 3 which consumes it must also re-run (stale input). But if step 5 only depends on step 4's output and step 4 passes its gate, step 5 can be checked independently.

The existing pipeline order guarantees topological sort, so a single forward pass through the step list is sufficient.

---

## Bug 4: `_save_state` Overwrites State with Wrong Agents

### Root Cause

`_save_state()` at `executor.py:879` writes `config.agents` (current session's agents) to the state file unconditionally. On a broken resume where Bug 1 caused wrong agents to be loaded, this destroys the original correct agent config.

### Fix

With Bug 1 fixed, `config.agents` will always be correct by the time `_save_state` runs. However, as a defense-in-depth measure:

**Change 1** -- `_save_state()`: Preserve original agents if current run had no generate results.

```python
def _save_state(
    config: RoadmapConfig,
    results: list[StepResult],
    remediate_metadata: dict | None = None,
    certify_metadata: dict | None = None,
) -> None:
    state_file = config.output_dir / ".roadmap-state.json"
    spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()

    existing = read_state(state_file)
    existing_validation = existing.get("validation") if existing else None
    existing_fidelity = existing.get("fidelity_status") if existing else None
    existing_remediate = existing.get("remediate") if existing else None
    existing_certify = existing.get("certify") if existing else None

    # Defense-in-depth: if no generate steps ran successfully,
    # preserve the original agents from state to prevent corruption
    generate_ran = any(
        r.step and r.step.id.startswith("generate-")
        and r.status == StepStatus.PASS
        for r in results
    )
    if generate_ran or existing is None:
        agents_to_save = config.agents
    else:
        saved_agents = existing.get("agents")
        if saved_agents:
            agents_to_save = config.agents  # Bug 1 fix ensures this is correct
            # But if they differ and no generate ran, prefer existing
            existing_specs = [
                AgentSpec(model=a["model"], persona=a["persona"])
                for a in saved_agents
            ]
            if existing_specs != config.agents and not generate_ran:
                _log.warning(
                    "Agents differ from state file and no generate steps ran; "
                    "preserving original agents in state"
                )
                agents_to_save = existing_specs
        else:
            agents_to_save = config.agents

    state = {
        "schema_version": 1,
        "spec_file": str(config.spec_file),
        "spec_hash": spec_hash,
        "agents": [
            {"model": a.model, "persona": a.persona} for a in agents_to_save
        ],
        "depth": config.depth,
        "last_run": datetime.now(timezone.utc).isoformat(),
        "steps": { ... },  # unchanged
    }
    ...
```

**Simpler alternative** (recommended if Bug 1 fix is considered sufficient):

Since Bug 1 ensures `config.agents` is always correct on resume, the simplest defense is a pre-save assertion log:

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

I recommend the **full defense-in-depth version** because the cost is ~15 lines and it prevents data loss in any future scenario where `config.agents` might be wrong.

---

## Implementation Order

1. **Bug 1 first** -- this is the root cause. All other bugs are consequences or amplifiers.
2. **Bug 4 second** -- defense-in-depth for the state file.
3. **Bug 3 third** -- the `_apply_resume` rewrite replaces the naive `found_failure` cascade.
4. **Bug 2 last** -- diagnostic improvement, folded into the Bug 3 rewrite.

Bugs 2 and 3 share the same function (`_apply_resume`), so they should be implemented together as a single rewrite.

## Files Changed

| File | Changes |
|---|---|
| `commands.py` | Add `@click.pass_context`, detect `agents_source`, pass `agents_explicit` |
| `executor.py` | Add `_restore_agents_from_state()`, modify `execute_roadmap()` signature, rewrite `_apply_resume()`, add defense-in-depth to `_save_state()` |
| `models.py` | No changes needed (`AgentSpec.__eq__` works via dataclass default) |

## Test Plan

### Test 1: Agent Restoration from State (Bug 1)

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

    restored = _restore_agents_from_state(config)
    assert restored.agents[1].persona == "analyzer"
    assert restored.agents[1].model == "haiku"
```

### Test 2: Explicit `--agents` Overrides State (Bug 1)

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

    # agents_explicit=True means _restore_agents_from_state is never called
    # So config.agents stays as passed
    assert config.agents[0].persona == "security"
```

### Test 3: Missing State File Graceful Fallback (Bug 1)

```python
def test_restore_agents_no_state_file(tmp_path):
    """Missing state file falls back to CLI agents."""
    config = RoadmapConfig(
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        output_dir=tmp_path, work_dir=tmp_path,
        spec_file=tmp_path / "spec.md",
    )

    restored = _restore_agents_from_state(config)
    assert restored.agents == config.agents  # unchanged
```

### Test 4: Phantom File Path Warning (Bug 2)

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

### Test 5: Dependency-Aware Skip (Bug 3)

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

### Test 6: State File Not Corrupted on Broken Resume (Bug 4)

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

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|---|---|---|
| `get_parameter_source` not available in older Click | Low (added Click 8.0, we require >=8.0) | Version check in CI |
| `Step.inputs` is `None` for some steps | Medium | `(s.inputs or [])` handles it |
| State file written by older version has no `agents` | Medium | Explicit fallback to CLI agents |
| Dependency tracking misses transitive deps | Low | Forward pass + regenerated set propagates correctly |
| Race condition: two resume runs on same dir | Low (pre-existing) | Out of scope; state file locking is a separate concern |

## Backward Compatibility

- Existing explicit `--agents` usage: **no change**. `agents_explicit=True` preserves current behavior.
- Existing state files without `agents` key: **graceful fallback** to CLI agents.
- `_apply_resume` return type: **unchanged** (`list[Step | list[Step]]`).
- `execute_roadmap` signature: new optional kwarg `agents_explicit` defaults to `True`, so all existing callers are unaffected.
