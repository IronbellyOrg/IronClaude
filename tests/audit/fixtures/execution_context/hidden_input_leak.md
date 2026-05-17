---
id: "TASK-RF-20260517-TEST006-LEAK"
title: "TEST-006 Hidden-input Leak (negative-path) Fixture"
---

# TEST-006 Hidden-input Leak (negative-path) Fixture

## Execution Context

<!-- OPTIONAL header — sample showing a HEADER that violates NFR-CONV.3 hidden-input determinism. This fixture is asserted to be REJECTED by the hidden-input guard (grep -cE "src/|/.*:[0-9]+" returns > 0). -->

- **References:** R-001: Demonstrate header leak — see src/superclaude/skills/task-builder/SKILL.md:879 for the offending citation.
- **Source areas:** rf-task-builder.md:312, src/superclaude/agents/rf-qa.md.
- **Key constraints:** Per-item Context fields cite file:line; header must NOT — this fixture intentionally violates the rule.

---
