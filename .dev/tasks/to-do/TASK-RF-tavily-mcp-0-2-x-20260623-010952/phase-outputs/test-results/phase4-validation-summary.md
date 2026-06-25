# Phase 4 Validation Summary

**Date:** 2026-06-23
**Overall result:** PASS (all in-scope artifacts; pre-existing env failures isolated)

## pytest — new C7 test
- `tests/cli/eval/test_tavily_eval_capability.py`: **3 passed** (M2 registration, suite resolves capability + E16 with `expect_tool_call: mcp__tavily__tavily-search`, gated SKIP without key).

## superclaude eval describe --suite real
- **exit 0**; renders `mcp_server.tavily` capability + `id: E16` + `expect_tool_call: mcp__tavily__tavily-search`.

## ruff
- `capabilities.py`, `models.py`, new test: ruff check + format **clean**.

## Regression check — full `tests/cli/eval/` (capabilities.py + real.yaml are widely depended on)
- **8 failed, 1367 passed, 4 skipped.**
- **1 failure was mine and is FIXED:** `test_default_roster_contains_expected_binaries_and_mcp_servers` — the `_DEFAULT_CAPABILITY_SPECS` roster legitimately gained `mcp_server.tavily` (M2), so the test's expected set was updated to include it (not a weakening — the roster genuinely changed). `test_capability_gates.py` now 18 passed.
- **The remaining 8 are PRE-EXISTING / ENVIRONMENTAL** (none reference tavily/my changed files):
  - `test_claude_process_adapter.py::test_ruff_*` (×2) — `No module named ruff` (ruff not installed as a `.venv` python module in this worktree).
  - `test_eval_run.py::test_d0072_spec_documents_flag_wiring` — missing `.dev/releases/current/cliEval/artifacts/D-0072/spec.md`.
  - `test_validation_commands.py::*` (×5) — missing `.dev/releases/current/cliEval/evidence/T06.11`.
  - These require populating worktree release artifacts / installing ruff-as-module — out of task scope; not introduced by this task.

## Files changed this phase
- `src/superclaude/cli/eval/capabilities.py` (`mcp_server.tavily` spec — M2)
- `src/superclaude/cli/eval/suites/real.yaml` (capability entry + `E16` eval; id renamed from `E-tavily-search` per schema, user-approved)
- `src/superclaude/cli/eval/models.py` (docstrings `mcp.tavily` → `mcp_server.tavily` — X4)
- `tests/cli/eval/test_capability_gates.py` (roster expected set += `mcp_server.tavily`)
- NEW: `tests/cli/eval/test_tavily_eval_capability.py`
