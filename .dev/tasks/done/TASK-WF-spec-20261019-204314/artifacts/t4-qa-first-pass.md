# Task 4 independent first-pass compliance review

Verdict: **missing**, limited to T4.AC7. The independent reviewer inspected the actual four files and incremental diff; no commands/tests or edits were performed. T4.AC1–6 and AC8 were found met with produced-file citations. No extra scope or misunderstood requirement was verified.

## Verified AC7 gap

Gateway selection checks Docker but not curl in `src/superclaude/cli/install_mcp.py:551-558`. The curl prerequisite is checked only if Codebase Memory acquisition is needed (`:569-581`). Gateway itself creates its install directory before invoking curl (`:264-281`).

With Claude/Docker available but curl missing, gateway-only selection can therefore create state before identifying the failure. In a mixed gateway/native selection with an existing usable native executable, earlier registration effects can also occur before this predictable prerequisite failure. This violates the explicit Task 4 requirement to identify selected prerequisites before effects.

The existing missing-curl case (`tests/cli/test_install_codebase_memory.py:1031-1038`) uses a missing native executable, so it verifies acquisition prerequisites rather than the gateway-specific case.

One Q5 fix pass was requested: add gateway curl to complete selection preflight and add gateway-only plus mixed/reused-native regressions proving no installer, registration or directory effects. Dry-run must remain able to plan without this mutation-time prerequisite. No later task may start before re-review passes.
