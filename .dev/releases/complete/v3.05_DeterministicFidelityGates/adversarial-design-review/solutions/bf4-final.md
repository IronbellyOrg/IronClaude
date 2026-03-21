# BF-4 Resolution: Replace Worktrees with Temporary Directory Isolation

## Selected Solution

**Solution B: Temporary Directory Copies (No Worktrees)**

The structural checkers are pure functions that operate on parsed `SpecData` and `RoadmapData` frozen dataclasses. They read exactly 2 files (`spec_path`, `roadmap_path`) and need zero access to the git repository, its history, or its working tree. Git worktrees solve the wrong problem -- they isolate git-tracked code, but the files that need isolation (`roadmap.md`, `spec-fidelity.md`, `deviation-registry.json`) are untracked output artifacts.

Solution B achieves identical isolation (NFR-4) with 100x less disk overhead (~1.5MB vs ~150MB), simpler lifecycle management (stdlib `mkdtemp`/`rmtree` vs git worktree add/remove), and no dependency on git state cleanliness.

## Architecture Design Change

### Sec 4.5.1: Replace Worktree Management with Temp Directory Management

**Remove** the following from `convergence.py`:

```python
# REMOVED
def _create_worktrees(count: int = 3) -> list[Path]:
    """Create temporary git worktrees for parallel validation."""

def _cleanup_worktrees(paths: list[Path]) -> None:
    """Remove worktrees: git worktree remove <path>"""
```

**Replace with**:

```python
import shutil
import tempfile
import uuid
from pathlib import Path

def _create_validation_dirs(
    spec_path: Path,
    roadmap_path: Path,
    registry_path: Path,
    count: int = 3,
) -> list[Path]:
    """Create isolated temporary directories with input file copies.

    Each directory receives independent copies of all input files
    required by the checker suite. No shared filesystem state between
    directories (NFR-4).

    Returns list of temp directory Paths.
    """
    session_id = uuid.uuid4().hex[:8]
    dirs: list[Path] = []

    for i in range(1, count + 1):
        tmp = Path(tempfile.mkdtemp(prefix=f"fidelity-validation-{session_id}-{i}-"))
        # Copy input files
        shutil.copy2(spec_path, tmp / spec_path.name)
        shutil.copy2(roadmap_path, tmp / roadmap_path.name)
        if registry_path.exists():
            shutil.copy2(registry_path, tmp / registry_path.name)
        dirs.append(tmp)

    return dirs


def _cleanup_validation_dirs(dirs: list[Path]) -> None:
    """Remove all temporary validation directories.

    Safe to call multiple times. Logs warnings on failure but does not raise.
    """
    for d in dirs:
        try:
            shutil.rmtree(d)
        except OSError as e:
            import logging
            logging.getLogger(__name__).warning(
                "Failed to clean up validation dir %s: %s", d, e
            )
```

**Update `handle_regression()`**:

```python
def handle_regression(
    registry: DeviationRegistry,
    spec_path: Path,
    roadmap_path: Path,
    config: RoadmapConfig,
) -> list[Finding]:
    """Spawn 3 parallel agents in isolated temp directories for regression validation.

    Steps:
    1. Create 3 temp directories with copies of input files
    2. In each directory, run full checker suite independently
    3. Collect all findings from all 3 agents
    4. Merge by stable_id: union of all findings
    5. Deduplicate: finding present in >=2 agents = confirmed
    6. Write consolidated report to fidelity-regression-validation.md
    7. For each HIGH in consolidated: adversarial debate
    8. Update registry with debate verdicts
    9. Clean up temp directories (guaranteed via try/finally)

    Returns merged+debated findings.
    """
    validation_dirs = _create_validation_dirs(
        spec_path, roadmap_path,
        registry.path, count=3,
    )
    try:
        # Run agents in parallel using ThreadPoolExecutor
        # Each agent reads from its own validation_dirs[i]
        ...
    finally:
        _cleanup_validation_dirs(validation_dirs)
```

### FR-8 Requirement Text Update

**Old**: "3 agents spawned in parallel, each in its own git worktree"

**New**: "3 agents spawned in parallel, each in its own isolated temporary directory containing independent copies of all input files (spec, roadmap, registry snapshot)"

### Sec 4.5.1 Heading Update

**Old**: "Regression Detection & Parallel Validation (FR-8)" with worktree management subsection

**New**: Same heading, but worktree management replaced with temp directory management as shown above.

## Isolation Mechanism

Each agent operates in complete filesystem isolation:

1. **Input isolation**: Each temp directory contains its own copies of `spec.md`, `roadmap.md`, and `deviation-registry.json`. File copies are made via `shutil.copy2()` (preserves metadata). Agents receive paths to their local copies, never the shared originals.

2. **In-memory isolation**: The spec parser produces frozen (`@dataclass(frozen=True)`) `SpecData` and `RoadmapData` objects. Even if agents shared the same parsed data (they don't -- each parses its own copy), mutation is prevented at the type level.

3. **Output isolation**: Each agent writes its findings to `findings.json` within its own temp directory. The orchestrator reads from all 3 directories after completion. No agent can see or modify another agent's output.

4. **Registry isolation**: Each agent receives a read-only snapshot of the registry. Agents do NOT write back to the registry. Only the orchestrator merges the collected findings into the canonical registry after all agents complete.

## File Copy Manifest

Per agent directory (3 directories total):

| Source File | Destination | Size (typical) | Purpose |
|------------|-------------|----------------|---------|
| `config.spec_file` | `{tmp}/spec.md` | 20-50 KB | Spec for parser input |
| `output_dir/roadmap.md` | `{tmp}/roadmap.md` | 30-80 KB | Roadmap for parser input |
| `output_dir/deviation-registry.json` | `{tmp}/deviation-registry.json` | 5-20 KB | Read-only registry snapshot for prior findings context |

**Total per agent**: ~55-150 KB
**Total for 3 agents**: ~165-450 KB
**Contrast with worktrees**: ~150 MB (3 full repo checkouts)

Output written per agent:

| File | Size (typical) | Purpose |
|------|----------------|---------|
| `{tmp}/findings.json` | 5-30 KB | Agent's checker findings |

## Cleanup Protocol

1. **Primary cleanup**: `_cleanup_validation_dirs()` called in `finally` block of `handle_regression()`. Guarantees cleanup even if agent execution raises exceptions.

2. **Fallback cleanup**: Register `atexit.register(_cleanup_validation_dirs, dirs)` as a secondary safety net in case the process is killed between directory creation and the try/finally block.

3. **Temp directory prefix**: All directories use the prefix `fidelity-validation-{session_id}-` making them identifiable for manual cleanup if needed.

4. **OS-level cleanup**: Since directories are created under the system temp directory (`/tmp/` on Linux, `%TEMP%` on Windows), the OS will eventually clean them up even if the process crashes without running cleanup handlers.

5. **No git state pollution**: Unlike worktrees, temp directories leave no trace in `.git/worktrees/` and cannot cause "worktree already exists" errors on subsequent runs.

## Validation

To verify isolation works correctly:

1. **Unit test -- file independence**: Create 3 validation dirs from the same inputs. Modify a file in dir-1. Assert dir-2 and dir-3 are unmodified.

```python
def test_validation_dir_isolation(tmp_path):
    spec = tmp_path / "spec.md"
    roadmap = tmp_path / "roadmap.md"
    registry = tmp_path / "registry.json"
    spec.write_text("# Spec")
    roadmap.write_text("# Roadmap")
    registry.write_text("{}")

    dirs = _create_validation_dirs(spec, roadmap, registry, count=3)
    try:
        # Mutate file in dir 0
        (dirs[0] / "spec.md").write_text("# MUTATED")
        # Assert dirs 1 and 2 are unaffected
        assert (dirs[1] / "spec.md").read_text() == "# Spec"
        assert (dirs[2] / "spec.md").read_text() == "# Spec"
    finally:
        _cleanup_validation_dirs(dirs)
```

2. **Unit test -- cleanup**: Create validation dirs, call cleanup, assert directories no longer exist.

```python
def test_cleanup_removes_dirs(tmp_path):
    spec = tmp_path / "spec.md"
    roadmap = tmp_path / "roadmap.md"
    spec.write_text("# Spec")
    roadmap.write_text("# Roadmap")

    dirs = _create_validation_dirs(spec, roadmap, tmp_path / "reg.json", count=3)
    _cleanup_validation_dirs(dirs)
    for d in dirs:
        assert not d.exists()
```

3. **Integration test -- parallel execution**: Run 3 checker instances simultaneously on the 3 directories. Assert all 3 produce identical findings (determinism, NFR-1) and no race conditions occur.

4. **Regression test -- no worktree artifacts**: After `handle_regression()` completes, assert that no `.fidelity-worktree-*` directories exist in the repo root and `git worktree list` shows only the main worktree.
