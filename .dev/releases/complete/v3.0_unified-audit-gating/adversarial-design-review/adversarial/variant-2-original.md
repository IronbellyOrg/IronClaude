# Design: Fix `--resume` Data Loss -- 4 Compounding Bugs

**Status**: PROPOSED
**Author**: Brainstorm (adversarial design review)
**Date**: 2026-03-18
**Scope**: `commands.py` (CLI layer), `executor.py` (`execute_roadmap`, `_apply_resume`, `_save_state`, `_build_steps`)

---

## 1. Problem Statement

When a user runs `superclaude roadmap run spec.md --resume` without re-specifying `--agents`, four bugs compound into a data-loss cascade:

1. Click supplies its hardcoded default `"opus:architect,haiku:architect"` -- indistinguishable from an explicit user choice.
2. `_build_steps()` generates file paths derived from the wrong agents (e.g., `roadmap-haiku-architect.md` instead of `roadmap-haiku-analyzer.md`).
3. `_apply_resume()` gate-checks those phantom paths, finds them missing, cascades a full re-run from that point onward, overwriting valid outputs.
4. `_save_state()` writes the wrong agents into `.roadmap-state.json`, poisoning all future `--resume` attempts.

The same pattern affects `--depth` (hardcoded Click default `"standard"`) -- a user who originally ran `--depth deep` and resumes without the flag gets `standard`, which changes the debate prompt and could produce a different merge outcome.

---

## 2. Root Cause Analysis

### 2.1 The Click Default Problem

Click options with `default=` values are supplied automatically when the user omits the flag. The `run()` function receives `agents="opus:architect,haiku:architect"` whether the user typed it or not. There is no built-in Click mechanism to distinguish "user provided" from "default applied."

```
commands.py:36  -->  default="opus:architect,haiku:architect"
commands.py:53  -->  default="standard"
```

### 2.2 The Ordering Problem

In `execute_roadmap()`:

```python
steps = _build_steps(config)     # line 1140 -- uses wrong agents
if resume:
    steps = _apply_resume(...)   # line 1151 -- too late, paths already wrong
```

`_build_steps` derives output file paths from `config.agents` before `_apply_resume` has any chance to restore the original agents from the state file.

### 2.3 The Cascade Problem

`_apply_resume()` uses a `found_failure` flag (line 1587). Once any step fails its gate check, every subsequent step is appended to the re-run list unconditionally -- even steps whose outputs exist on disk and would pass their gates.

### 2.4 The State Corruption Problem

`_save_state()` writes `config.agents` unconditionally (line 879). After a broken resume, this overwrites the state file's agents with the Click defaults, destroying the original configuration.

---

## 3. Fix Design

### Fix 1: Change Click Defaults to `None` with Explicit Fallback

**Layer**: CLI (`commands.py`)
**Principle**: Make "user did not provide" detectable by using `None` as the Click default.

```python
# commands.py -- BEFORE
@click.option("--agents", default="opus:architect,haiku:architect", ...)
@click.option("--depth", default="standard", ...)

# commands.py -- AFTER
@click.option("--agents", default=None, help="... Default: opus:architect,haiku:architect")
@click.option(
    "--depth",
    type=click.Choice(["quick", "standard", "deep"], case_sensitive=False),
    default=None,
    help="... Default: standard.",
)
```

In the `run()` function body, resolve `None` to the fallback only for non-resume runs:

```python
def run(spec_file, agents, output_dir, depth, resume, ...):
    from .executor import execute_roadmap
    from .models import AgentSpec, RoadmapConfig

    # agents and depth are None when user omitted them
    config = RoadmapConfig(
        spec_file=spec_file.resolve(),
        agents=([AgentSpec.parse(a.strip()) for a in agents.split(",")]
                if agents is not None else None),
        depth=depth,  # may be None
        output_dir=resolved_output.resolve(),
        ...
    )

    execute_roadmap(config, resume=resume, agents_explicit=(agents is not None),
                    depth_explicit=(depth is not None), no_validate=no_validate)
```

**Alternative (simpler)**: Instead of threading `agents_explicit` through to the executor, pass `agents_raw=agents` and `depth_raw=depth` and let `execute_roadmap` handle the None-vs-default logic. This is the recommended approach -- see Fix 1b below.

#### Fix 1b: Let `execute_roadmap` Resolve Defaults After State Restore

```python
def run(spec_file, agents, output_dir, depth, resume, ...):
    execute_roadmap(
        spec_file=spec_file.resolve(),
        output_dir=resolved_output.resolve(),
        agents_raw=agents,       # None if user omitted
        depth_raw=depth,         # None if user omitted
        resume=resume,
        ...
    )
```

In `execute_roadmap`, the resolution order becomes:

1. If `--resume` and state file exists: restore agents/depth from state file for any `None` parameter.
2. If not `--resume` or state file missing: apply hardcoded defaults for any `None` parameter.
3. If user explicitly provided a value (non-None): always use it, even on resume.

This preserves the user's ability to intentionally override agents on resume (e.g., `--resume --agents sonnet:qa,haiku:qa`) while protecting against silent default substitution.

**Impact on `RoadmapConfig`**: The `agents` field needs to accept `None` temporarily. Recommended approach: resolve before constructing `RoadmapConfig`, so the dataclass always has a concrete value.

```python
def execute_roadmap(
    config: RoadmapConfig,
    resume: bool = False,
    agents_raw: str | None = None,
    depth_raw: str | None = None,
    no_validate: bool = False,
    auto_accept: bool = False,
) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)

    # --- Restore from state BEFORE building steps ---
    if resume:
        state = read_state(config.output_dir / ".roadmap-state.json")
        if state is not None:
            if agents_raw is None and "agents" in state:
                config.agents = [
                    AgentSpec(model=a["model"], persona=a["persona"])
                    for a in state["agents"]
                ]
            if depth_raw is None and "depth" in state:
                config.depth = state["depth"]
        elif agents_raw is None or depth_raw is None:
            print(
                "WARNING: --resume with no state file found. "
                "Using defaults for unspecified options.",
                file=sys.stderr, flush=True,
            )

    # Apply hardcoded defaults for any still-None fields (non-resume case)
    if not config.agents:
        config.agents = [AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")]
    if not config.depth:
        config.depth = "standard"

    # NOW build steps with correct agents
    steps = _build_steps(config)
    ...
```

**Key invariant**: `_build_steps(config)` is never called until `config.agents` and `config.depth` are resolved to their correct values.

---

### Fix 2: Distinguish "File Not Found" from "Gate Failed" in `_apply_resume`

**Layer**: Executor (`executor.py`, `_apply_resume`)

The gate function `gate_passed()` in `pipeline/gates.py` already returns distinct reason strings:
- `"File not found: {path}"` (line 34)
- `"File empty (0 bytes): {path}"` (line 39)
- `"Below minimum line count: ..."` (line 48)
- etc.

But `_apply_resume` discards the reason (`_reason` on lines 1600, 1624). The fix surfaces it:

```python
# _apply_resume -- AFTER
if entry.gate:
    passed, reason = gate_fn(entry.output_file, entry.gate)
    if passed:
        skipped += 1
        print(f"[roadmap] Skipping {entry.id} (gate passes)", flush=True)
        continue
    # Distinguish missing file (likely wrong config) from content failure
    if reason and "File not found" in reason:
        print(
            f"[roadmap] WARNING: {entry.id} output not found: {entry.output_file}\n"
            f"  This may indicate --agents or --depth differ from the original run.",
            file=sys.stderr, flush=True,
        )
    else:
        print(
            f"[roadmap] Re-running {entry.id}: {reason}",
            flush=True,
        )
```

For parallel groups, the same logic applies per-step within the group.

**Defensive check** (optional but recommended): Before entering the gate-check loop, verify that the state file's agents match `config.agents`. If they differ and `agents_raw` was `None`, something is wrong -- abort with a clear error rather than silently re-running everything.

```python
if state is not None:
    state_agents = state.get("agents", [])
    config_agent_dicts = [{"model": a.model, "persona": a.persona} for a in config.agents]
    if state_agents != config_agent_dicts:
        print(
            f"FATAL: Agent mismatch between state file and current config.\n"
            f"  State:   {state_agents}\n"
            f"  Current: {config_agent_dicts}\n"
            f"  Pass --agents explicitly or delete .roadmap-state.json to restart.",
            file=sys.stderr, flush=True,
        )
        sys.exit(1)
```

This guard should be placed in `execute_roadmap` after Fix 1's state restoration, as a belt-and-suspenders check.

---

### Fix 3: Replace `found_failure` Cascade with Per-Step Gate Checking

**Layer**: Executor (`executor.py`, `_apply_resume`)

Current behavior: once any step fails, all subsequent steps are blindly re-run.
Desired behavior: each step is independently checked. Only steps that fail their gate (or depend on a step that failed) are re-run.

#### 3.1 Dependency-Aware Resume

The pipeline has implicit dependencies encoded in `step.inputs`. A step should re-run if:
- Its own gate fails, OR
- Any of its input files were produced by a step that is being re-run.

```python
def _apply_resume(
    steps: list[Step | list[Step]],
    config: RoadmapConfig,
    gate_fn: Callable,
) -> list[Step | list[Step]]:
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)

    # Stale-spec detection (unchanged)
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
                file=sys.stderr, flush=True,
            )
            force_extract = True

    # Track which output files are being re-generated
    dirty_outputs: set[Path] = set()
    skipped = 0
    result: list[Step | list[Step]] = []

    for entry in steps:
        if isinstance(entry, list):
            # Parallel group
            needs_rerun = False
            for s in entry:
                if _step_needs_rerun(s, gate_fn, dirty_outputs, force_extract):
                    needs_rerun = True
                    break
            if needs_rerun:
                # Re-run entire group; mark all outputs dirty
                for s in entry:
                    dirty_outputs.add(s.output_file)
                result.append(entry)
            else:
                skipped += len(entry)
                print(
                    f"[roadmap] Skipping {', '.join(s.id for s in entry)} (gates pass)",
                    flush=True,
                )
        else:
            if _step_needs_rerun(entry, gate_fn, dirty_outputs, force_extract):
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


def _step_needs_rerun(
    step: Step,
    gate_fn: Callable,
    dirty_outputs: set[Path],
    force_extract: bool,
) -> bool:
    """Determine if a single step needs re-running.

    A step needs re-run if:
    1. force_extract and step is 'extract', OR
    2. Any of its input files are in the dirty set, OR
    3. Its own gate check fails.
    """
    if force_extract and step.id == "extract":
        return True

    # If any input was re-generated, must re-run
    if any(inp in dirty_outputs for inp in step.inputs):
        return True

    # Check own gate
    if step.gate:
        passed, reason = gate_fn(step.output_file, step.gate)
        if passed:
            return False
        # Log the reason
        if reason and "File not found" in reason:
            print(
                f"[roadmap] {step.id}: output missing ({step.output_file.name})",
                file=sys.stderr, flush=True,
            )
        else:
            print(f"[roadmap] {step.id}: gate failed -- {reason}", flush=True)
        return True

    # No gate defined -- must run
    return True
```

**Key improvement**: Steps 7-9 (test-strategy, spec-fidelity, certify) can be skipped even if Step 3 (diff) needed re-running, as long as their inputs (merge output) were not re-generated and their own gates pass. In practice, a cascade will still usually propagate because later steps consume earlier outputs -- but the dependency check makes this explicit rather than blind.

#### 3.2 Why Not Just Flip `found_failure` to Per-Step?

A minimal fix would be to simply remove `found_failure` and check each step independently. This is almost correct but misses the dependency chain: if `extract` is re-run, its output changes, so `generate-*` must also re-run even if their old outputs still pass gates (they are now stale). The `dirty_outputs` set captures this.

---

### Fix 4: `_save_state` Must Not Overwrite Agents on Broken Resume

**Layer**: Executor (`executor.py`, `_save_state`)

Two sub-fixes:

#### 4a: Merge, Don't Replace

When `_save_state` writes the state file, it should preserve the original agents/depth if the run was a resume that did not complete all steps:

```python
def _save_state(
    config: RoadmapConfig,
    results: list[StepResult],
    remediate_metadata: dict | None = None,
    certify_metadata: dict | None = None,
) -> None:
    state_file = config.output_dir / ".roadmap-state.json"
    existing = read_state(state_file)

    # Preserve original agents/depth from existing state if this was a partial run
    # (Fix 1 already ensures config.agents is correct, but this is defense-in-depth)
    agents_to_save = [{"model": a.model, "persona": a.persona} for a in config.agents]
    depth_to_save = config.depth

    spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()

    # ... rest of state construction uses agents_to_save and depth_to_save ...
```

#### 4b: With Fix 1 in Place, This Bug Is Largely Moot

If `execute_roadmap` correctly restores agents from the state file before doing anything (Fix 1), then `config.agents` will always be correct by the time `_save_state` runs. Fix 4a is defense-in-depth: even if Fix 1 has a bug, the state file won't be corrupted.

#### 4c: Write State Atomically with Schema Versioning

The current implementation already uses `write_state` (which presumably does atomic write). The `schema_version: 1` field is already present. No change needed here, but note that adding `agents_raw` or `depth_raw` to the state schema would be a schema_version bump -- avoid this; just store the resolved values.

---

## 4. Does `--depth` Have the Same Bug?

**Yes.** The `--depth` option has `default="standard"` (line 53). If a user originally ran `--depth deep` and resumes without the flag:

1. Click supplies `"standard"`.
2. `_build_steps` passes `config.depth` to `build_debate_prompt`, changing the number of debate rounds.
3. The debate step may produce a different output.
4. `_save_state` overwrites `depth: "deep"` with `depth: "standard"` in the state file.

The fix is identical to `--agents`: change Click default to `None`, restore from state on resume.

### Other Options to Audit

| Option | Current Default | Stored in State? | Risk |
|--------|----------------|-----------------|------|
| `--agents` | `"opus:architect,haiku:architect"` | Yes | **HIGH** -- changes file paths |
| `--depth` | `"standard"` | Yes | **MEDIUM** -- changes debate rounds |
| `--output` | `None` (derived from spec_file) | Implicit via `spec_file` | LOW -- path derivation is stable |
| `--model` | `""` | No | LOW -- empty means per-agent default |
| `--max-turns` | `100` | No | LOW -- performance not correctness |
| `--retrospective` | `None` | No | LOW -- only affects extract prompt |

Only `--agents` and `--depth` need the `None`-default treatment.

---

## 5. Interaction Between Fixes

The fixes must be applied together. Applying them in isolation creates partial states:

| Applied Alone | Result |
|--------------|--------|
| Fix 1 only | Agents correct, but cascade still overwrites valid outputs (Fix 3) |
| Fix 2 only | Better diagnostics but still uses wrong agents |
| Fix 3 only | Independent checking, but on phantom paths from wrong agents |
| Fix 4 only | State preserved, but next resume still builds wrong steps |

**Recommended application order**: Fix 1 -> Fix 4 -> Fix 3 -> Fix 2

Fix 1 is the critical path -- it eliminates the root cause. Fix 4 prevents state corruption as defense-in-depth. Fix 3 improves resume efficiency. Fix 2 improves diagnostics.

---

## 6. Test Plan

### 6.1 Unit Tests

| Test | Validates |
|------|-----------|
| `test_resume_restores_agents_from_state` | Fix 1: When `agents_raw=None` and state has `[haiku:analyzer, opus:qa]`, config.agents matches state |
| `test_resume_explicit_agents_override_state` | Fix 1: When `agents_raw="sonnet:security"`, config.agents uses the explicit value, not state |
| `test_resume_restores_depth_from_state` | Fix 1: When `depth_raw=None` and state has `"deep"`, config.depth is `"deep"` |
| `test_resume_no_state_uses_defaults` | Fix 1: When state file missing and agents_raw=None, falls back to hardcoded defaults |
| `test_gate_file_not_found_message` | Fix 2: `_apply_resume` prints warning about agent mismatch when file not found |
| `test_resume_skips_passing_downstream` | Fix 3: Steps 7-9 skipped when their inputs unchanged and gates pass |
| `test_resume_dirty_propagation` | Fix 3: When step 1 re-runs, steps 2a/2b re-run (input dependency), but step 9 can still skip if its input (step 6 output) unchanged |
| `test_save_state_writes_correct_agents` | Fix 4: After resume with restored agents, state file agents match original |

### 6.2 Integration Tests

| Test | Validates |
|------|-----------|
| `test_full_resume_cycle_different_agents` | Run with `--agents haiku:analyzer,opus:qa`, then `--resume` without `--agents` -- agents restored, no data loss |
| `test_full_resume_cycle_different_depth` | Run with `--depth deep`, then `--resume` without `--depth` -- depth restored |
| `test_double_resume_state_stability` | Run, resume, resume again -- state file agents stable across all three invocations |
| `test_resume_with_explicit_override` | Run with agents A, resume with `--agents B` -- uses B (intentional override) |

### 6.3 Edge Cases

- Resume with no state file at all (first run crashed before `_save_state`)
- Resume with corrupted state file (malformed JSON)
- Resume with state file from a different spec_file
- State file has agents but no depth key (forward-compat)
- User passes `--agents` identical to the original run on resume (should be no-op)

---

## 7. Migration / Backward Compatibility

### 7.1 Existing State Files

State files written before this fix will have `agents` and `depth` keys. The new code reads these keys, so existing state files are compatible. No migration needed.

### 7.2 CLI Interface

Changing `--agents` and `--depth` defaults to `None` is backward-compatible for non-resume runs: the `run()` function applies the same defaults. The only behavioral change is on `--resume`, where the state file now takes precedence over Click defaults.

### 7.3 Schema Version

No schema_version bump needed. The state file format is unchanged -- we are reading existing fields that were already being written.

---

## 8. Files to Modify

| File | Changes |
|------|---------|
| `src/superclaude/cli/roadmap/commands.py` | Lines 36, 53: Change defaults to `None`. Lines 119-150: Pass raw values to executor. |
| `src/superclaude/cli/roadmap/executor.py` | `execute_roadmap()`: Add state restore before `_build_steps`. `_apply_resume()`: Replace `found_failure` cascade with `_step_needs_rerun` + `dirty_outputs`. `_save_state()`: Defense-in-depth agent preservation. |
| `src/superclaude/cli/roadmap/models.py` | No changes needed (agents/depth are resolved before RoadmapConfig construction). |
| `tests/` | New test file: `tests/roadmap/test_resume_restore.py` |

**Estimated diff size**: ~180 lines changed, ~120 lines added (tests).
