# Tasklist (fixture) — serena-citation-freshness (NFR-4, holistic)

# A run whose REPORT.md cites file:line ranges derived from type_hierarchy (step 4.5) and
# execute_shell_command (step 5.5) outputs. The holistic audit asserts every cited file:line
# entering REPORT.md was re-Read within the §6.2 5-tool-call window (CLAUDE.md S1).
- Task 1: produce findings citing hierarchy-slice.yaml + verify-logs file:line anchors
- Task 2: confirm each citation has a preceding re-Read within 5 tool calls
