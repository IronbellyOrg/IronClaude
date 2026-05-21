# D-0010 — Evidence

## Test execution

Command:

```
uv run pytest tests/cli/eval/test_capability_gates.py -v
```

Result: **18 passed** (see `../../evidence/T01.11/pytest.log`).

| Test | Acceptance criterion |
|---|---|
| `test_default_roster_contains_expected_binaries_and_mcp_servers` | T01.11 Steps[2]: roster = claude/jq/make/git HARD + 3 MCP SOFT-SKIP. |
| `test_hard_binaries_are_hard_and_mcp_servers_are_skip` | Roster classification matches design-spec §11. |
| `test_check_all_returns_capability_report` | `check_all()` returns a populated `CapabilityReport`. |
| `test_check_all_is_idempotent` | AC: calling twice returns equal reports. |
| `test_which_or_skip_resolves_existing_binary` | `which_or_skip` returns `(True, "<resolved path>")` on hit. |
| `test_which_or_skip_returns_false_when_missing` | `which_or_skip` returns `(False, "not found …")` on miss. |
| `test_missing_claude_classifies_hard` | AC: missing `claude` classifies HARD; lands in `hard_failures`. |
| `test_missing_mcp_server_classifies_soft_skip` | AC: missing MCP server classifies SOFT-SKIP under `--no-mcp`. |
| `test_no_mcp_flag_skips_even_when_servers_are_reachable` | `--no-mcp` forces SOFT-SKIP even when probe would have passed; `skipped_by_flag` set. |
| `test_mcp_server_reachable_default_uses_path_presence` | OQ-5 M1 stub uses PATH presence as the reachability signal. |
| `test_mcp_server_reachable_honours_injected_probe` | `mcp_probe` constructor hook overrides the default probe (M2 upgrade seam). |
| `test_capabilities_accessor_returns_capability_dataclasses` | `capabilities()` materialises `Capability` instances aligned with the roster. |
| `test_capability_check_closures_defer_to_gate_probes` | `Capability.check()` closures reuse gate probe methods (no duplicate logic). |
| `test_check_all_report_status_rows_carry_descriptions` | `CapabilityStatus.description` mirrors the spec table. |
| `test_xfail_capability_classifies_into_soft_xfails` | Custom spec with `failure_mode="xfail"` lands in `soft_xfails`. |
| `test_unknown_capability_kind_is_rejected_at_check_time` | `_probe` raises `ValueError` on a typo'd `kind` field. |
| `test_skip_flags_are_emitted_sorted_and_deduplicated` | `skip_flags` property is sorted + deduplicated. |
| `test_status_rows_for_passing_binaries_have_no_skipped_by_flag` | HARD binaries never carry `skipped_by_flag=True`. |

## Regression check

Full cli/eval suite:

```
uv run pytest tests/cli/eval/ -v
```

Result: **183 passed** (no regressions introduced by T01.11).

## Module surface

- `superclaude.cli.eval.capabilities.CapabilityGates` — new class
  (T01.11) with `check_all`, `which_or_skip`, `mcp_server_reachable`,
  `capabilities`, `skip_flags`.
- `_CapabilitySpec` + `_DEFAULT_CAPABILITY_SPECS` — private static
  roster carrying `(name, target, kind, failure_mode, skip_flag,
  description)`.
- `Capability` (T01.09) and `CapabilityReport` / `CapabilityStatus`
  (T01.10) unchanged in behaviour; only the module docstring was
  updated to point at T01.11.
- `superclaude.cli.eval.__init__` re-exports `CapabilityGates`,
  `CapabilityReport`, `CapabilityStatus` so doctor / SuiteLoader
  callers do not have to reach into the submodule.

## Cross-task traceability

- **Roadmap COMP-009 / R-010** — `CapabilityGates` class with the three
  named methods is now landed; `claude/jq/make/git` are HARD,
  `auggie/auggie-mcp/airis-mcp-gateway` are SOFT-SKIP via `--no-mcp`.
- **OQ-5** — deferred to M2 per roadmap Open Questions table.
  `mcp_server_reachable` ships with a PATH-presence M1 stub and a
  `mcp_probe` constructor hook so the M2 patch can swap in a real
  handshake probe without breaking the public surface.
- **DM-007 / DM-008** — `CapabilityGates.check_all()` produces a
  `CapabilityReport` populated with `CapabilityStatus` rows; field
  semantics match the DM-008 contract documented in
  `D-0009/spec.md`.
- **Downstream T01.13 (FR-CLI4)** — `eval doctor` will instantiate
  `CapabilityGates`, call `check_all()`, and render the report. The
  `to_json()` consumer hook is already in place via
  `CapabilityReport.to_json()` (T01.10).
- **Downstream T01.07 (COMP-002)** — SuiteLoader currently uses the
  `PermissiveCapabilityResolver` stub; T01.13 will wire an adapter
  that exposes `CapabilityGates` to the loader's `CapabilityResolver`
  protocol.
