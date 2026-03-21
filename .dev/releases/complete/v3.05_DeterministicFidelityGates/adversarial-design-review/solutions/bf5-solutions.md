# BF-5: Missing --allow-regeneration Flag -- Solution Analysis

## Problem Statement

FR-9 requires: "Full regeneration only with explicit user consent (--allow-regeneration flag)."

The architecture design (Sec 4.6) defines `apply_patches()` with a `diff_threshold: float = 0.30` parameter and per-patch `diff_size_ratio()` guard, but provides no mechanism for the user to override this guard when full regeneration is intentional. There is no `--allow-regeneration` CLI flag, no config field, and no conditional bypass logic.

---

## Solution A: Binary Flag Override

### Design

Add an explicit boolean flag `allow_regeneration` that, when set, bypasses the diff-size guard entirely.

**Config Model Change** (`models.py`):
```python
@dataclass
class RoadmapConfig(PipelineConfig):
    # ... existing fields ...
    allow_regeneration: bool = False
```

**CLI Change** (`commands.py`, on `run` command):
```python
@click.option(
    "--allow-regeneration",
    is_flag=True,
    help=(
        "Allow patches that exceed the diff-size threshold (default 30%). "
        "Without this flag, patches changing >30% of a file are rejected."
    ),
)
```

**Guard Logic Change** (`remediate_executor.py`, `apply_patches()`):
```python
def apply_patches(
    patches: list[RemediationPatch],
    config: PipelineConfig,
    registry: DeviationRegistry,
    diff_threshold: float = 0.30,
    allow_regeneration: bool = False,
) -> tuple[int, int]:
    # ... existing grouping logic ...
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
                # Reject as currently designed
                _log.warning("Patch %s rejected: %.1f%% > threshold", ...)
                registry.update_finding_status(patch.finding_id, "FAILED")
                rejected += 1
                continue
        # Apply patch (MorphLLM or fallback)
```

### Analysis

| Criterion | Assessment |
|-----------|------------|
| **FR-9 Alignment** | Exact match. FR-9 says "--allow-regeneration flag" -- this implements that literal requirement. The flag name, boolean semantics, and override behavior all match the requirement text verbatim. |
| **User Experience** | Simple and clear. `--allow-regeneration` is self-documenting. Users either want to allow it or they do not. No numeric values to reason about. |
| **Safety** | High safety. The flag defaults to `False`. It requires deliberate `--allow-regeneration` on the command line. No numeric value that could be accidentally set too high. Binary choice eliminates partial-override confusion. |
| **Implementation Complexity** | Minimal. One boolean field on RoadmapConfig, one Click flag, one conditional branch in `apply_patches()`. Three files touched, roughly 15 lines of change. |

---

## Solution B: Tiered Threshold with Convenience Alias

### Design

Replace the fixed 30% threshold with a configurable `--max-patch-size` percentage. Values above 100% effectively allow full regeneration. Add `--allow-regeneration` as a convenience alias that sets the threshold to 100%.

**Config Model Change** (`models.py`):
```python
@dataclass
class RoadmapConfig(PipelineConfig):
    # ... existing fields ...
    max_patch_size: float = 0.30  # 0.0-1.0 range; >1.0 allows regeneration
```

**CLI Change** (`commands.py`, on `run` command):
```python
@click.option(
    "--max-patch-size",
    type=float,
    default=0.30,
    help=(
        "Maximum allowed patch size as fraction of file lines (0.0-1.0). "
        "Default: 0.30 (30%). Values >1.0 allow full regeneration."
    ),
)
@click.option(
    "--allow-regeneration",
    is_flag=True,
    help="Convenience alias: sets --max-patch-size to 1.0 (allow full file rewrites).",
)
```

Mutual exclusion / precedence logic in the `run()` function:
```python
if allow_regeneration:
    effective_threshold = 1.0
elif max_patch_size is not None:
    effective_threshold = max_patch_size
else:
    effective_threshold = 0.30
```

**Guard Logic Change** (`remediate_executor.py`, `apply_patches()`):
```python
def apply_patches(
    patches: list[RemediationPatch],
    config: PipelineConfig,
    registry: DeviationRegistry,
    diff_threshold: float = 0.30,
) -> tuple[int, int]:
    # No change to function signature -- threshold is passed in from caller.
    # The caller resolves --allow-regeneration vs --max-patch-size before calling.
    for patch in file_patches:
        ratio = patch.diff_size_ratio(file_content)
        if ratio > diff_threshold:
            _log.warning("Patch %s rejected: %.1f%% > threshold %.1f%%", ...)
            registry.update_finding_status(patch.finding_id, "FAILED")
            rejected += 1
            continue
        # Apply patch
```

### Analysis

| Criterion | Assessment |
|-----------|------------|
| **FR-9 Alignment** | Partial match. FR-9 explicitly names "--allow-regeneration flag" and "diff-size guard: reject individual patch if changed_lines / total_file_lines > threshold (default 30%)". Solution B satisfies both ACs but through indirection: the flag is an alias, not the primary mechanism. The configurable threshold goes beyond what FR-9 asks for. |
| **User Experience** | More flexible but more complex. Users now have two options (`--max-patch-size` and `--allow-regeneration`) that interact. What does `--max-patch-size 0.5 --allow-regeneration` mean? Need precedence rules. The `--max-patch-size` flag requires understanding the 0.0-1.0 scale. |
| **Safety** | Lower safety. A user could accidentally type `--max-patch-size 1.0` or `--max-patch-size 0.8` without realizing they are effectively allowing near-full regeneration. The continuous scale makes the boundary between "safe" and "unsafe" fuzzy. There is no clear "you are now in dangerous mode" signal like a boolean flag provides. |
| **Implementation Complexity** | Moderate. Requires mutual exclusion logic between two flags, input validation (what if value is negative? > 2.0?), threshold propagation through the config, and documentation of the interaction semantics. Roughly 30-40 lines of change across 3-4 files. |

---

## Comparative Summary

| Criterion | Weight | Solution A | Solution B |
|-----------|--------|-----------|-----------|
| FR-9 Alignment | 40% | 10/10 -- exact match to requirement text | 7/10 -- satisfies intent but adds unrequested complexity |
| Safety | 30% | 9/10 -- binary, no accidental partial override | 6/10 -- continuous scale enables accidental over-permitting |
| Implementation Simplicity | 30% | 9/10 -- minimal changes, no interaction logic | 6/10 -- flag interaction, validation, precedence rules |
| **Weighted Score** | | **9.3** | **6.4** |

## Recommendation

**Solution A wins decisively.** It matches FR-9's literal requirement text, provides the strongest safety guarantees, and has the lowest implementation complexity. Solution B's additional flexibility (configurable threshold) is not requested by any FR and introduces user-facing complexity and safety risk without compensating benefit.

If configurable thresholds are needed in the future, they can be added as a separate FR without disrupting Solution A's clean boolean override.
