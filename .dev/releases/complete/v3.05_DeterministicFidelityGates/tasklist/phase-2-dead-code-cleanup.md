---
phase: 2
title: "Dead Code Cleanup"
tasks: 2
depends_on: []
parallelizable: true
---

# Phase 2: Dead Code Cleanup

Independent of Phase 1. Can execute in parallel with spec rewrite.

---

### T06: Delete fidelity.py

**Tier**: simple
**File**: src/superclaude/cli/roadmap/fidelity.py

**Action**: Delete the file entirely. It contains `Severity` enum and `FidelityDeviation` dataclass — both superseded by `Finding` (models.py) and `DeviationRegistry` (convergence.py).

**Pre-verification**: Confirm zero imports: `grep -r "from .fidelity import\|from ..roadmap.fidelity" src/superclaude/`

**Acceptance criteria**:
- [ ] fidelity.py deleted
- [ ] No import errors when running `uv run pytest tests/`
- [ ] No references to fidelity.py in any remaining code

---

### T07: Remove dead RunMetadata from convergence.py

**Tier**: simple
**File**: src/superclaude/cli/roadmap/convergence.py, line 36

**Action**: Remove the `RunMetadata` dataclass definition. `begin_run()` uses raw dicts, never instantiates `RunMetadata`.

**Pre-verification**: Confirm zero instantiations: `grep -r "RunMetadata(" src/superclaude/`

**Acceptance criteria**:
- [ ] RunMetadata class removed from convergence.py
- [ ] No import errors
- [ ] No references to RunMetadata in remaining code
