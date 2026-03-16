# D-0007 — Non-Blocking OQ Documentation: OQ-007 and OQ-014

**Produced by**: T01.07
**Sprint**: v2.25-cli-portify-cli
**Date**: 2026-03-16

---

## OQ-007 — Agent Discovery Warning Behavior

**Blocking/Non-Blocking**: NON-BLOCKING

**Phase Assignment**: Phase 2 — `inventory.py` implementation

**Default Behavior**: Emit `warnings.warn()` for missing agent/skill/command files; do not suppress silently.

**Rationale**: Silent failures during agent discovery lead to incomplete portify runs with no indication of what was skipped. A `warnings.warn()` allows users to see discovery gaps without halting the run. Fatal errors are reserved for cases where the missing file is required (e.g., `SKILL.md`).

**Specification**:
```python
import warnings

def discover_agents(workflow_path: Path) -> list[AgentRef]:
    agents_dir = workflow_path / "agents"
    if not agents_dir.exists():
        warnings.warn(
            f"No agents/ directory found in {workflow_path}. "
            "Agent inventory will be empty.",
            UserWarning,
            stacklevel=2,
        )
        return []
    # ... scan for .md files ...
    for agent_file in agents_dir.glob("*.md"):
        if not agent_file.is_file():
            warnings.warn(
                f"Expected agent file is not readable: {agent_file}",
                UserWarning,
                stacklevel=2,
            )
            continue
        # ... process agent ...
```

Warning categories:
- Missing `agents/` directory → `UserWarning`
- Missing `refs/` directory → `UserWarning`
- Unreadable agent `.md` file → `UserWarning`
- Missing `SKILL.md` → `FileNotFoundError` (fatal, not a warning)

---

## OQ-014 — Workdir Cleanup Policy

**Blocking/Non-Blocking**: NON-BLOCKING

**Phase Assignment**: Phase 9 — observability completion documentation

**Default Behavior**: Work directory is retained after run completes. No automatic cleanup.

**Rationale**: Portify work directories contain intermediate artifacts (phase outputs, step logs, gate results) that are valuable for debugging failed runs. Automatic deletion would destroy diagnostic evidence. Users who want cleanup can delete the directory manually or use a future `--clean` flag.

**Retention policy**:
- Work directory (`work_dir`) is retained after successful run: YES
- Work directory retained after failed run: YES
- Automatic cleanup on `--dry-run`: N/A (no subprocess, no files written)
- Future `--clean` flag: planned but NOT in Phase 1–10 scope

**Phase 9 documentation note**: The observability phase (T09.xx) will document the work directory layout and cleanup expectations in the CLI help text.

---

## Summary

| OQ | Classification | Phase | Default |
|----|---------------|-------|---------|
| OQ-007 | NON-BLOCKING | Phase 2 (`inventory.py`) | `warnings.warn()` for missing agent files |
| OQ-014 | NON-BLOCKING | Phase 9 (observability) | Work dir retained; no auto-cleanup |

Neither OQ prevents any phase from proceeding.
