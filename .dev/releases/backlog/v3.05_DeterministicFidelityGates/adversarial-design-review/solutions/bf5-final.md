# BF-5 Resolution: Binary --allow-regeneration Flag

## Selected Solution

**Solution A: Binary Flag Override** -- selected with weighted score 9.3/10 vs Solution B's 6.4/10.

Rationale:
- FR-9 explicitly names "--allow-regeneration flag" -- Solution A implements this verbatim
- Binary flag prevents accidental over-permitting (no continuous scale to misconfigure)
- Minimal implementation surface: 1 config field, 1 CLI flag, 1 conditional branch

## Architecture Design Change

Add to Section 4.6.2 (`apply_patches()` documentation), after the `diff_threshold` parameter description:

```
Parameters:
    ...
    diff_threshold: float = 0.30
        Per-patch diff-size guard. Reject patch if changed_lines / total_file_lines > threshold.
    allow_regeneration: bool = False
        When True, patches exceeding diff_threshold are applied with a WARNING log
        instead of being rejected. Corresponds to CLI --allow-regeneration flag (FR-9).
        Default False ensures full regeneration requires explicit user consent.
```

Add to Section 4.6.2 algorithm, step 2.b.ii:

```
ii.  If ratio > threshold:
       - If allow_regeneration is True: log WARNING with patch ID, ratio, and
         threshold; proceed to apply (step iii/iv)
       - If allow_regeneration is False (default): reject, log, mark FAILED in registry
```

## Config Model Change

File: `src/superclaude/cli/roadmap/models.py`

Add field to `RoadmapConfig`:

```python
@dataclass
class RoadmapConfig(PipelineConfig):
    spec_file: Path = field(default_factory=lambda: Path("."))
    agents: list[AgentSpec] = field(
        default_factory=lambda: [
            AgentSpec("opus", "architect"),
            AgentSpec("haiku", "architect"),
        ]
    )
    depth: Literal["quick", "standard", "deep"] = "standard"
    output_dir: Path = field(default_factory=lambda: Path("."))
    retrospective_file: Path | None = None
    allow_regeneration: bool = False  # FR-9: override diff-size guard
```

## CLI Change

File: `src/superclaude/cli/roadmap/commands.py`

Add Click option to the `run` command (after `--no-validate`, before `--retrospective`):

```python
@click.option(
    "--allow-regeneration",
    is_flag=True,
    help=(
        "Allow patches that exceed the diff-size threshold (default 30%%). "
        "Without this flag, patches changing >30%% of a file are rejected. "
        "Use when full file regeneration is intentional."
    ),
)
```

Add `allow_regeneration: bool` parameter to the `run()` function signature.

Add to `config_kwargs` dict:

```python
config_kwargs: dict = {
    ...
    "allow_regeneration": allow_regeneration,
}
```

## Guard Logic

File: `src/superclaude/cli/roadmap/remediate_executor.py` (to be created per architecture Sec 2.2)

Modify `apply_patches()` signature and body:

```python
def apply_patches(
    patches: list[RemediationPatch],
    config: PipelineConfig,
    registry: DeviationRegistry,
    diff_threshold: float = 0.30,
    allow_regeneration: bool = False,
) -> tuple[int, int]:
    """Apply patches sequentially per file with diff-size guard.

    When allow_regeneration is True, patches exceeding diff_threshold
    are applied with a warning instead of being rejected (FR-9).
    """
    applied, rejected = 0, 0

    for target_file, file_patches in _group_by_file(patches).items():
        file_content = Path(target_file).read_text(encoding="utf-8")
        _create_snapshot(target_file)

        for patch in file_patches:
            ratio = patch.diff_size_ratio(file_content)

            if ratio > diff_threshold:
                if allow_regeneration:
                    _log.warning(
                        "Patch %s exceeds threshold (%.1f%% > %.1f%%) "
                        "-- applying anyway (--allow-regeneration)",
                        patch.finding_id,
                        ratio * 100,
                        diff_threshold * 100,
                    )
                    # Fall through to apply
                else:
                    _log.warning(
                        "Patch %s rejected: %.1f%% exceeds %.1f%% threshold",
                        patch.finding_id,
                        ratio * 100,
                        diff_threshold * 100,
                    )
                    registry.update_finding_status(patch.finding_id, "FAILED")
                    rejected += 1
                    continue

            # Apply via MorphLLM or fallback
            success = _apply_single_patch(patch, target_file)
            if success:
                registry.update_finding_status(patch.finding_id, "FIXED")
                applied += 1
            else:
                registry.update_finding_status(patch.finding_id, "FAILED")
                rejected += 1

    return applied, rejected
```

The caller in `convergence.py` (`execute_fidelity_with_convergence`) passes the flag through:

```python
apply_patches(
    patches=generated_patches,
    config=config,
    registry=registry,
    diff_threshold=0.30,
    allow_regeneration=config.allow_regeneration,
)
```

## Validation

1. **Unit test -- flag rejected by default**:
   - Create a patch with `diff_size_ratio() = 0.5` (exceeds 0.30 threshold)
   - Call `apply_patches(..., allow_regeneration=False)`
   - Assert: patch rejected, finding marked FAILED, rejected_count == 1

2. **Unit test -- flag allows override**:
   - Same patch with `diff_size_ratio() = 0.5`
   - Call `apply_patches(..., allow_regeneration=True)`
   - Assert: patch applied, finding marked FIXED, applied_count == 1
   - Assert: WARNING log emitted with patch ID and ratio

3. **CLI integration test -- flag wiring**:
   - Parse `superclaude roadmap run spec.md --allow-regeneration`
   - Assert: `config.allow_regeneration is True`
   - Parse `superclaude roadmap run spec.md` (no flag)
   - Assert: `config.allow_regeneration is False`

4. **Safety test -- default behavior unchanged**:
   - Run existing test suite without `--allow-regeneration`
   - Assert: all patches exceeding 30% are still rejected (no regression)
