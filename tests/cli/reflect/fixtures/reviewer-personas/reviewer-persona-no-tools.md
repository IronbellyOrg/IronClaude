---
name: reviewer-persona-no-tools
description: NEGATIVE FIXTURE — a reviewer persona variant with the tools line stripped, used to prove the read-only guard flags an absent/empty tools line (such an agent inherits ALL tools, including Bash/Edit/Write/Task).
category: quality
---

# Reviewer Persona (no tools line) — NEGATIVE FIXTURE

This fixture intentionally omits the `tools:` frontmatter line, mimicking the
pre-L1 reviewer personas (`quality-engineer` / `root-cause-analyst` /
`refactoring-expert`) that carry no `tools:` line and therefore inherit
Bash/Edit/Write/NotebookEdit/Task. The read-only guard MUST flag this as
NOT read-only-safe.
