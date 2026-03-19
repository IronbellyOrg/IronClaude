---
deliverable: D-0006
phase: 2
task: T02.05
status: committed
date: 2026-03-19
---

# D-0006: Registry Analyzer (G-003)

## Artifact
- `src/superclaude/cli/audit/wiring_gate.py` — `analyze_registries()`

## Algorithm
1. Scan for dict assignments matching DEFAULT_REGISTRY_PATTERNS
2. For each entry, verify value is resolvable (Name or string dotted path)
3. Emit unwired_registry finding for unresolvable references

## SC-003 Evidence
- Test `test_detects_broken_registry_entry` validates detection
- Test `test_valid_registry_not_flagged` validates no false positives
- Test `test_registry_string_reference_unresolved` validates string path detection
