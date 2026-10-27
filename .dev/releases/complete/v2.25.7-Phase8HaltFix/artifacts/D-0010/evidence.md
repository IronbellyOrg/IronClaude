# D-0010 Evidence: Sprint Context Header in build_prompt()

## Deliverable
`build_prompt()` in `src/superclaude/cli/sprint/process.py` emits a `## Sprint Context` section.

## Implementation

**File:** `src/superclaude/cli/sprint/process.py`
**Method:** `ClaudeProcess.build_prompt()` (lines 123–191)

### Sprint Context block fields included:
- **Sprint name**: `getattr(config, "release_name", None) or config.release_dir.name` (safe fallback per OQ-002)
- **Phase N of M**: `pn` (current phase number) of `len(config.phases)` (total phases from config)
- **Artifact root path**: `config.release_dir / "artifacts"`
- **Results directory**: `config.results_dir`
- **Prior-phase artifact directories**: computed for phases 1..pn-1 that exist on disk
- **Prior-phase directories**: `config.release_dir / "phase-{i}"` for phases 1..pn-1
- **Instruction**: "All task details are in the phase file. Do not seek additional index files."

### Sample output (Phase 3 of 6):
```
## Sprint Context
- Sprint: v2.25.7-Phase8HaltFix
- Phase: 3 of 6
- Artifact root: /path/to/release/artifacts
- Results directory: /path/to/release/results
- Prior-phase artifact directories: /path/to/release/artifacts/D-0001, ...
- Prior-phase directories: /path/to/release/phase-1, /path/to/release/phase-2
- All task details are in the phase file. Do not seek additional index files.
```

## Verification

`uv run pytest tests/sprint/ -v --tb=short` → **629 passed** in 37.22s

## Milestone
M3.1 satisfied.
