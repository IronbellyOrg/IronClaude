# Design: Resume Pipeline -- Defensive Guard Architecture

**Status**: PROPOSED
**Author**: Brainstorm Agent C (adversarial design review)
**Date**: 2026-03-18
**Scope**: `src/superclaude/cli/roadmap/executor.py` -- `execute_roadmap()`, `_apply_resume()`, `_save_state()`

---

## 1. Problem Statement

When `superclaude roadmap run --resume` is invoked without `--agents`, four bugs compound into a single failure mode: the pipeline restarts from the wrong step with wrong agents, overwrites the state file, and destroys evidence of the original successful run.

The conventional fix is "restore agents from the state file." This document explores a different approach: make the system **structurally incapable** of these failures through defensive guards, state-driven path resolution, and conditional writes.

### 1.1 The Failure Chain

```
User runs: roadmap run spec.md --agents opus:architect,haiku:analyzer
Pipeline fails at: spec-fidelity
State file records: agents=[opus:architect, haiku:analyzer]

User runs: roadmap run spec.md --resume  (no --agents)
Click default: agents=[opus:architect, haiku:architect]  <-- Bug 1

_build_steps() generates: roadmap-opus-architect.md, roadmap-haiku-architect.md
_apply_resume() checks: roadmap-haiku-architect.md (does not exist)  <-- Bug 2
  gate_passed() returns (False, "File not found: ...") -- no warning printed
  found_failure = True
  ALL downstream steps included in re-run list  <-- Bug 3

Pipeline re-runs from generate-haiku-architect with wrong agent
_save_state() overwrites agents=[opus:architect, haiku:architect]  <-- Bug 4
Original agent config destroyed
```

## 2. Design Philosophy: Guards Over Restores

The "restore agents from state" approach is fragile. It assumes:
- The state file always exists and is valid
- The state file's agent list is always authoritative
- Every caller remembers to check state before constructing config

A **guard** approach inverts the control flow: `execute_roadmap()` refuses to proceed when its inputs are inconsistent with the on-disk state, rather than silently "fixing" them.

## 3. Proposed Fixes

### 3.1 Bug 1 Fix: Agent Mismatch Guard in `execute_roadmap()`

Instead of restoring agents from state, detect the mismatch and abort with an actionable error message. The user explicitly chose agents on the original run; they should explicitly confirm them on resume.

**Location**: `executor.py`, inside `execute_roadmap()`, after the `if resume:` branch begins.

```python
# Inside execute_roadmap(), after steps = _build_steps(config)
if resume:
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)

    if state is not None:
        saved_agents = state.get("agents", [])
        current_agents = [
            {"model": a.model, "persona": a.persona} for a in config.agents
        ]

        # Detect Click default vs explicit --agents
        click_default = [
            {"model": "opus", "persona": "architect"},
            {"model": "haiku", "persona": "architect"},
        ]
        agents_match = saved_agents == current_agents
        using_click_default = current_agents == click_default

        if not agents_match and using_click_default and saved_agents != click_default:
            saved_desc = ", ".join(
                f"{a['model']}:{a['persona']}" for a in saved_agents
            )
            print(
                f"ERROR: --resume detected agent mismatch.\n"
                f"  State file agents: {saved_desc}\n"
                f"  Current agents:    opus:architect,haiku:architect (Click default)\n"
                f"\n"
                f"  To resume with original agents:\n"
                f"    superclaude roadmap run {config.spec_file} --resume "
                f"--agents {saved_desc}\n"
                f"\n"
                f"  To intentionally restart with new agents (destroys prior work):\n"
                f"    superclaude roadmap run {config.spec_file} "
                f"--agents opus:architect,haiku:architect\n"
                f"    (without --resume)",
                file=sys.stderr,
            )
            sys.exit(1)
```

**Why guard instead of restore**: The user may have intentionally changed agents. Silently restoring old agents hides intent. An explicit error forces the user to be deliberate. This is the same principle as git's "divergent branches" refusal -- make the user resolve the ambiguity.

**Trade-off**: Adds one extra flag to the resume command. Acceptable because resume is already a recovery operation where precision matters more than convenience.

**Edge case -- Click default IS the original agents**: If the original run also used the default `opus:architect,haiku:architect`, `saved_agents == current_agents` is true, so the guard does not fire. No false positive.

### 3.2 Bug 2 Fix: State-Driven Path Resolution in `_apply_resume()`

The root cause is that `_apply_resume()` derives paths from `config` (which may have wrong agents) instead of reading paths from the state file (which recorded the actual outputs).

**Approach**: Before gate-checking, cross-reference each step's `output_file` against the state file's `steps[].output_file`. If the state file records a different path for the same step ID, use the state file's path for the gate check.

```python
def _apply_resume(
    steps: list[Step | list[Step]],
    config: RoadmapConfig,
    gate_fn: Callable,
) -> list[Step | list[Step]]:
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)
    force_extract = False

    # Build lookup: step_id -> recorded output_file from state
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
    found_failure = False

    def _gate_check_step(s: Step) -> bool:
        """Check gate using state-recorded path if available."""
        if not s.gate:
            return False

        # Use state-recorded path for gate check (not config-derived path)
        check_path = state_paths.get(s.id, s.output_file)
        if check_path != s.output_file:
            _log.info(
                "Resume: step '%s' using state-recorded path %s "
                "(config-derived: %s)",
                s.id, check_path, s.output_file,
            )
        passed, reason = gate_fn(check_path, s.gate)
        if not passed and check_path != s.output_file:
            _log.warning(
                "Resume: step '%s' gate FAIL on state path %s: %s",
                s.id, check_path, reason,
            )
        return passed

    for entry in steps:
        if found_failure:
            result.append(entry)
            continue

        if isinstance(entry, list):
            all_pass = all(_gate_check_step(s) for s in entry)
            if all_pass:
                skipped += len(entry)
                print(
                    f"[roadmap] Skipping {', '.join(s.id for s in entry)} "
                    f"(gates pass)",
                    flush=True,
                )
            else:
                found_failure = True
                result.append(entry)
        else:
            if force_extract and entry.id == "extract":
                found_failure = True
                result.append(entry)
                continue

            if _gate_check_step(entry):
                skipped += 1
                print(f"[roadmap] Skipping {entry.id} (gate passes)", flush=True)
                continue
            found_failure = True
            result.append(entry)

    if skipped > 0:
        print(f"[roadmap] Skipped {skipped} steps (gates pass)", flush=True)

    if not result:
        print(
            "[roadmap] All steps already pass gates. Nothing to do.",
            flush=True,
        )

    return result
```

**Key insight**: This makes resume independent of `config.agents`. Even if the user passes wrong agents, `_apply_resume` still checks the correct files on disk. The guard from 3.1 catches the mismatch early, but if it somehow slips through (e.g., state file missing), this layer provides defense in depth.

### 3.3 Bug 3 Fix: Eliminate `found_failure` Cascade

The `found_failure` flag is a greedy cascade: once any step fails its gate, ALL subsequent steps are included in the re-run list, even if their outputs are perfectly valid.

**Scenario where this wastes money**: The pipeline ran successfully through step 7 (test-strategy) but failed at step 8 (spec-fidelity). On `--resume`, `found_failure` triggers at step 8, which correctly re-runs spec-fidelity. But if there were a step 9, it would also re-run needlessly.

In the current 9-step pipeline this is mostly harmless because spec-fidelity is the last step. But the architecture is wrong in principle and will bite when new steps are added.

**Proposed fix**: Replace `found_failure` with per-step gate evaluation. Each step is independently checked. Steps that pass are skipped; steps that fail are included.

```python
# Replace the found_failure loop with:
for entry in steps:
    if isinstance(entry, list):
        all_pass = all(_gate_check_step(s) for s in entry)
        if all_pass:
            skipped += len(entry)
            print(
                f"[roadmap] Skipping {', '.join(s.id for s in entry)} "
                f"(gates pass)",
                flush=True,
            )
        else:
            result.append(entry)
    else:
        if force_extract and entry.id == "extract":
            result.append(entry)
            continue

        if _gate_check_step(entry):
            skipped += 1
            print(f"[roadmap] Skipping {entry.id} (gate passes)", flush=True)
            continue
        result.append(entry)
```

**Counter-argument and why the cascade exists**: The cascade exists because steps have data dependencies. If step 3 (diff) needs to re-run because its output is stale, step 4 (debate) must also re-run even if its output currently passes gates -- the output was generated from stale diff input.

**Resolution**: The counter-argument is valid for *forward* dependencies but not for *backward* ones. The correct model is: when a step fails, re-run it AND all steps that depend on its output. Since the pipeline is linear (each step depends on the previous), the cascade behavior is actually correct for the current pipeline shape.

**Revised recommendation**: Keep the cascade but add explicit logging. The real bug is not the cascade itself but the silent behavior when a file is not found (Bug 2). Once Bug 2 is fixed by state-driven paths, the cascade correctly identifies "step N's output is missing/stale, so steps N+1..9 must re-run."

```python
# Add to the found_failure branch:
if found_failure:
    if isinstance(entry, list):
        _log.info(
            "Resume: including %s (downstream of failed step)",
            ", ".join(s.id for s in entry),
        )
    else:
        _log.info(
            "Resume: including %s (downstream of failed step)", entry.id,
        )
    result.append(entry)
    continue
```

### 3.4 Bug 4 Fix: Conditional State Writes

`_save_state()` should not overwrite state when no progress was made. Two conditions must be met before writing:

1. At least one step in `results` has status PASS
2. The agents in `config` match the agents in the existing state (or no state exists)

```python
def _save_state(
    config: RoadmapConfig,
    results: list[StepResult],
    remediate_metadata: dict | None = None,
    certify_metadata: dict | None = None,
) -> None:
    """Write .roadmap-state.json -- only when the pipeline made progress."""
    state_file = config.output_dir / ".roadmap-state.json"

    # Guard 1: No progress, no write
    any_passed = any(r.status == StepStatus.PASS for r in results if r.step)
    if not any_passed:
        _log.info(
            "State not saved: no steps passed in this run "
            "(%d results, all non-PASS)",
            len(results),
        )
        return

    # Guard 2: Agent mismatch with existing state -- refuse to overwrite
    existing = read_state(state_file)
    if existing is not None:
        saved_agents = existing.get("agents", [])
        current_agents = [
            {"model": a.model, "persona": a.persona} for a in config.agents
        ]
        if saved_agents and saved_agents != current_agents:
            _log.warning(
                "State not saved: agent mismatch between config (%s) "
                "and existing state (%s). Use explicit --agents to override.",
                current_agents,
                saved_agents,
            )
            return

    # Normal save logic continues...
    spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()
    # ... (rest of existing _save_state body)
```

**Why "no progress = no write"**: A broken resume that fails immediately at the generate step (because it's looking for wrong files) produces zero PASS results. Writing state in this case overwrites the agents list, destroying the record of which agents actually produced the existing outputs. The "at least one PASS" guard prevents this.

**Why "agent mismatch = no write"**: Even if a step passes (e.g., extract passes because it's agent-independent), writing state with wrong agents would corrupt the agent record for subsequent resumes.

## 4. The `--depth` Problem

`--depth` has the same class of bug as `--agents`. The state file records `"depth": "deep"` but `--resume` without `--depth` defaults to `"standard"`.

### 4.1 Impact Analysis

`--depth` affects exactly one step: debate (line 457 of executor.py).

```python
prompt=build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth)
```

The depth value controls how many debate rounds occur. If the original run used `--depth deep` (3 rounds) and the resume defaults to `--depth standard` (2 rounds), two outcomes:

1. **If debate already passed**: `_apply_resume` skips it. The depth mismatch is irrelevant because the step is not re-run. No bug.
2. **If debate needs re-run**: It re-runs with fewer rounds. The debate output may be lower quality, but it will likely still pass gates. This is a **silent quality degradation**, not a crash.

### 4.2 Proposed Fix

Apply the same guard pattern from 3.1:

```python
if resume and state is not None:
    saved_depth = state.get("depth")
    if saved_depth and saved_depth != config.depth:
        # Only warn if depth was not explicitly passed
        # (Click doesn't distinguish "user passed default" from "default applied")
        print(
            f"WARNING: --depth mismatch.\n"
            f"  State file depth: {saved_depth}\n"
            f"  Current depth:    {config.depth}\n"
            f"  Using state file depth: {saved_depth}\n",
            file=sys.stderr,
            flush=True,
        )
        config.depth = saved_depth  # Override with saved value
```

**Unlike agents, depth can be safely auto-restored** because:
- It affects a single step (debate), not file paths
- There is no ambiguity about intent -- depth has no structural side effects
- The user sees a WARNING and knows the override happened

This differs from agents where auto-restore is dangerous because agents determine file paths, parallel group structure, and step IDs.

## 5. Defense in Depth: Layered Guard Summary

```
Layer 1: Agent mismatch guard (execute_roadmap)
  -> Refuses to proceed if agents don't match state + using Click default
  -> User must explicitly pass --agents to resume

Layer 2: State-driven path resolution (_apply_resume)
  -> Gate checks use state-recorded paths, not config-derived paths
  -> Even if Layer 1 is bypassed, gate checks still work

Layer 3: Cascade logging (_apply_resume)
  -> Downstream re-runs are logged explicitly
  -> Operator can see exactly which steps re-run and why

Layer 4: Conditional state writes (_save_state)
  -> No progress = no write (prevents state corruption)
  -> Agent mismatch = no write (prevents agent record destruction)

Layer 5: Depth auto-restore with warning
  -> Non-structural config values are silently restored from state
  -> WARNING printed so operator is informed
```

## 6. Click's `is_eager` Problem (Architectural Note)

Click has no built-in way to distinguish "user explicitly passed `--agents opus:architect,haiku:architect`" from "Click applied the default." Both arrive in the `run()` function as the same string value.

The guard in 3.1 works around this by comparing against the known Click default value. But this is brittle -- if the default changes in `commands.py`, the guard's hardcoded comparison must also change.

A more robust approach: use `click.Context.get_parameter_source()` (Click 8.0+):

```python
@click.pass_context
def run(ctx, spec_file, agents, ...):
    source = ctx.get_parameter_source("agents")
    agents_explicitly_set = source == click.core.ParameterSource.COMMANDLINE
```

This cleanly separates "user typed it" from "default applied" without hardcoding the default value.

## 7. Implementation Order

1. **3.1 (Agent guard)** -- highest impact, prevents the entire failure chain
2. **3.4 (Conditional writes)** -- prevents state corruption even if guard is bypassed
3. **3.2 (State-driven paths)** -- defense in depth for edge cases
4. **4.2 (Depth restore)** -- low-severity but easy to implement alongside 3.1
5. **3.3 (Cascade logging)** -- observability improvement, lowest priority

Steps 1 and 2 together eliminate all four bugs. Steps 3-5 are hardening.

## 8. Test Plan

| Test | Validates |
|------|-----------|
| Resume with Click default agents when state has different agents -> exits with error and actionable message | 3.1 |
| Resume with explicit `--agents` matching state -> proceeds normally | 3.1 (no false positive) |
| Resume with explicit `--agents` NOT matching state -> proceeds (user is explicit) | 3.1 (intentional override) |
| `_apply_resume` with state-recorded paths different from config-derived paths -> uses state paths | 3.2 |
| `_save_state` with zero PASS results -> does not write state file | 3.4 |
| `_save_state` with agent mismatch -> does not write state file | 3.4 |
| Resume with `--depth` mismatch -> restores saved depth with WARNING | 4.2 |
| `ctx.get_parameter_source("agents")` returns COMMANDLINE when user passes `--agents` | 6 |
| `ctx.get_parameter_source("agents")` returns DEFAULT when user omits `--agents` | 6 |

## 9. Files Affected

| File | Change |
|------|--------|
| `src/superclaude/cli/roadmap/executor.py` | `execute_roadmap()`: add agent mismatch guard; `_apply_resume()`: state-driven paths, cascade logging; `_save_state()`: conditional writes |
| `src/superclaude/cli/roadmap/commands.py` | `run()`: accept `click.Context`, pass `agents_explicitly_set` to executor |
| `tests/` | New test cases per section 8 |
