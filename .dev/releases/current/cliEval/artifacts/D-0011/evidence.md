# D-0011 — Evidence (T01.13)

## Source files

* `src/superclaude/cli/eval/commands.py` — Click `eval doctor` command +
  `build_doctor_report`, `doctor_payload`, `render_checklist`,
  `render_hard_failure_artifact` helpers; supplementary capability
  probes (`_check_claude_version`, `_check_claude_home`,
  `_check_ptytest_vendored`).
* `src/superclaude/cli/eval/__init__.py` — re-exports `eval_group`,
  `build_doctor_report`, `doctor_payload`, render helpers,
  `HARD_FAIL_EXIT_CODE`.
* `src/superclaude/cli/main.py` — `main.add_command(eval_group, name="eval")`
  wiring (after the `prd_group` block).

## Tests

`uv run pytest tests/cli/eval/test_doctor.py -v` — 28 passed (0.15 s).

```
tests/cli/eval/test_doctor.py::test_version_probe_passes_on_supported_release PASSED
tests/cli/eval/test_doctor.py::test_version_probe_passes_on_higher_release PASSED
tests/cli/eval/test_doctor.py::test_version_probe_fails_below_min PASSED
tests/cli/eval/test_doctor.py::test_version_probe_fails_when_unparseable PASSED
tests/cli/eval/test_doctor.py::test_version_probe_fails_when_callable_returns_none PASSED
tests/cli/eval/test_doctor.py::test_version_probe_catches_callable_exception PASSED
tests/cli/eval/test_doctor.py::test_claude_home_passes_when_directory_exists PASSED
tests/cli/eval/test_doctor.py::test_claude_home_fails_when_missing PASSED
tests/cli/eval/test_doctor.py::test_ptytest_vendored_passes_when_init_present PASSED
tests/cli/eval/test_doctor.py::test_ptytest_vendored_soft_skips_when_absent PASSED
tests/cli/eval/test_doctor.py::test_build_doctor_report_appends_three_supplementary_rows PASSED
tests/cli/eval/test_doctor.py::test_build_doctor_report_clean_host_has_no_hard_failures PASSED
tests/cli/eval/test_doctor.py::test_build_doctor_report_missing_claude_binary_is_hard PASSED
tests/cli/eval/test_doctor.py::test_build_doctor_report_missing_claude_home_is_hard PASSED
tests/cli/eval/test_doctor.py::test_build_doctor_report_below_min_version_is_hard PASSED
tests/cli/eval/test_doctor.py::test_build_doctor_report_no_mcp_flag_forces_soft_skip PASSED
tests/cli/eval/test_doctor.py::test_build_doctor_report_accepts_gate_override PASSED
tests/cli/eval/test_doctor.py::test_cli_doctor_exits_zero_on_clean_host PASSED
tests/cli/eval/test_doctor.py::test_cli_doctor_json_payload_matches_report_contract PASSED
tests/cli/eval/test_doctor.py::test_cli_doctor_json_is_deterministic_across_invocations PASSED
tests/cli/eval/test_doctor.py::test_cli_doctor_exits_two_when_hard_capability_missing PASSED
tests/cli/eval/test_doctor.py::test_cli_doctor_json_exit_two_includes_hard_failures_in_payload PASSED
tests/cli/eval/test_doctor.py::test_cli_doctor_no_mcp_flag_propagates_to_skip_flags PASSED
tests/cli/eval/test_doctor.py::test_cli_doctor_check_coverage_flag_is_accepted PASSED
tests/cli/eval/test_doctor.py::test_cli_doctor_check_coverage_marker_emitted_in_json PASSED
tests/cli/eval/test_doctor.py::test_render_checklist_lists_every_row PASSED
tests/cli/eval/test_doctor.py::test_render_hard_failure_artifact_lists_each_failure PASSED
tests/cli/eval/test_doctor.py::test_doctor_payload_extends_capability_report_contract PASSED
============================== 28 passed in 0.15s ==============================
```

`uv run pytest tests/cli/eval/ -q` — **211 passed** (full eval suite green, no regressions).

## Smoke test — human checklist (exit 0)

```
$ uv run superclaude eval doctor
superclaude eval doctor:
  [ok] Claude CLI on PATH -- /config/.local/bin/claude
  [ok] GNU make on PATH -- /usr/bin/make
  [ok] jq JSON processor on PATH -- /usr/bin/jq
  [ok] git VCS on PATH -- /usr/bin/git
  [ok] Auggie MCP server reachable -- /config/.nvm/versions/node/v22.22.0/bin/auggie
  [--] auggie-mcp MCP server reachable (SOFT-SKIP) -- MCP server binary not on PATH
  [--] AIRIS MCP gateway reachable (SOFT-SKIP) -- MCP server binary not on PATH
  [ok] Claude CLI >= 0.5.0 -- claude 2.1.145
  [ok] ~/.claude/ directory exists -- /config/.claude
  [--] ptytest vendored under cli/eval/pty/ (SOFT-SKIP) -- /config/.../pty/__init__.py not found (vendored at M2)
all HARD capabilities satisfied
soft skips: mcp_server.auggie-mcp, mcp_server.airis-mcp-gateway, vendored.ptytest
$ echo $?
0
```

## Smoke test — JSON payload determinism (exit 0)

`uv run superclaude eval doctor --json` emits the deterministic payload
captured in `/tmp/doctor-json.txt` (top-level keys sorted, last three
`report[]` rows = `claude.min_version`, `filesystem.claude_home`,
`vendored.ptytest`, and `coverage_gate` extension present).

## AC traceability

| AC bullet (T01.13) | Evidence |
|---|---|
| Exits 0 on clean dev machine | Smoke test above (live host: exit 0); `test_cli_doctor_exits_zero_on_clean_host`. |
| `--json` deterministic, matches `CapabilityReport` contract | `test_cli_doctor_json_payload_matches_report_contract`, `test_cli_doctor_json_is_deterministic_across_invocations`. |
| Fails closed (exit 2) on HARD capability missing + HARD-failure artifact | `test_cli_doctor_exits_two_when_hard_capability_missing`, `test_cli_doctor_json_exit_two_includes_hard_failures_in_payload`. |
| `spec.md` documents green-checklist + JSON schema | `artifacts/D-0011/spec.md`. |
