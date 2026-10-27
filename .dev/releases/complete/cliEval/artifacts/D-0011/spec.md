# D-0011 — `superclaude eval doctor` subcommand spec

**Task:** T01.13 (Phase 1, Roadmap FR-CLI4 / R-011)
**Module:** `src/superclaude/cli/eval/commands.py`
**CLI surface:** `superclaude eval doctor [--json] [--no-mcp] [--check-coverage]`
**Status:** Implemented 2026-05-20

## Command surface

| Flag | Type | Effect |
|---|---|---|
| `--json` | bool flag | Emit a JSON payload extending the `CapabilityReport` contract; stdout only. |
| `--no-mcp` | bool flag | Forwarded to `CapabilityGates(skip_flags={"--no-mcp"})` so SOFT-SKIP MCP rows are flag-overridden. |
| `--check-coverage` | bool flag | Reserved for FR-G5 coverage gate (M4 T04.14); for M1 it stamps a `coverage_gate` marker into the JSON payload and prints a deferral note in the human checklist. |

Exit codes:

* `0` — every HARD capability satisfied.
* `2` (`HARD_FAIL_EXIT_CODE`) — at least one HARD capability failed.
  The stderr artifact (`render_hard_failure_artifact`) lists every
  offending capability name + description + detail.

## Green-checklist format

Rendered by `render_checklist(report)`:

```
superclaude eval doctor:
  [ok] <description> -- <detail>
  [--] <description> (SOFT-SKIP) -- <detail>
  [XX] <description> (HARD) -- <detail>
skip flags: <…>            # only when CapabilityReport.skip_flags is non-empty
all HARD capabilities satisfied | HARD failures: <names>
soft skips: <names>        # only when there are no HARD failures
```

Row markers are emitted by `_row_marker(row)` and never use shell colour
codes so the output is safe to capture in CI logs.

## JSON payload schema

The payload is `CapabilityReport.to_json()` plus a single extension key:

```json
{
  "report":         [ {CapabilityStatus rows…} ],
  "blocked_evals":  [],
  "skip_flags":     [],
  "hard_failures":  [],
  "soft_skips":     [],
  "soft_xfails":    [],
  "coverage_gate": {
    "requested":  bool,
    "status":     "deferred",
    "milestone":  "M4",
    "task":       "T04.14"
  }
}
```

`json.dumps(payload, indent=2, sort_keys=True)` guarantees byte-level
determinism across invocations on a stable host (verified by
`test_cli_doctor_json_is_deterministic_across_invocations`).

The `report[]` list ordering is fixed: the seven default capability rows
(from `_DEFAULT_CAPABILITY_SPECS`) in declaration order, followed by the
three doctor-specific rows in this fixed order:

1. `claude.min_version`     — HARD
2. `filesystem.claude_home` — HARD
3. `vendored.ptytest`       — SOFT-SKIP

## Supplementary capability rows (T01.13-specific)

`CapabilityGates` covers the binary / MCP roster per `D-0010`. The
doctor command appends three rows via `build_doctor_report()`:

| Row name | Failure mode | Probe | Notes |
|---|---|---|---|
| `claude.min_version` | hard | `claude --version` parsed for `>=0.5.0` | Probe is injectable via `_default_claude_version_probe`; fails closed when binary missing, output unparseable, or below floor. |
| `filesystem.claude_home` | hard | `Path.home() / ".claude"` is_dir | Override via `claude_home=` for tests. |
| `vendored.ptytest` | skip | `<cli/eval>/pty/__init__.py` is_file | SOFT-SKIP until M2 vendoring task; lets M1 doctor exit 0 on a clean dev machine. |

## HARD-failure artifact

When `report.hard_failures` is non-empty, `render_hard_failure_artifact`
emits the following stderr block (the "artifact" mandated by FR-CLI4
AC):

```
eval doctor: HARD failures
  - <name> (<description>): <detail>
  - <name> (<description>): <detail>
```

The artifact is emitted regardless of `--json` / human mode so CI logs
always capture a stable per-failure diagnostic line.

## Test injection seams

| Seam | How tests use it |
|---|---|
| `commands._default_claude_version_probe` | `monkeypatch.setattr` to return a literal version banner or `None`. |
| `shutil.which` | `monkeypatch.setattr` to fake PATH state without touching the host. |
| `Path.home` | `monkeypatch.setattr` to redirect `~/.claude/` resolution to a tmp dir. |
| `build_doctor_report(gates=…, claude_version_probe=…, claude_home=…, pty_dir=…)` | Direct kwargs for unit tests that need full control of every probe. |

## Wiring

* `eval_group` added to `superclaude.cli.main:main` via
  `main.add_command(eval_group, name="eval")`.
* `commands.eval_group` and `commands.doctor` use Click 8.3-compatible
  decorators (no removed `mix_stderr` kwarg).

## Acceptance criteria → implementation map

| AC bullet (T01.13) | Implementation site |
|---|---|
| `superclaude eval doctor` exits 0 on a clean dev machine. | `doctor` Click handler; covered by `test_cli_doctor_exits_zero_on_clean_host`. |
| `--json` emits a deterministic JSON payload matching the `CapabilityReport` contract. | `doctor_payload` + `json.dumps(..., sort_keys=True)`; covered by `test_cli_doctor_json_payload_matches_report_contract` + `test_cli_doctor_json_is_deterministic_across_invocations`. |
| Doctor fails closed (exit 2) when any HARD capability is missing; emits a HARD-failure artifact. | `sys.exit(HARD_FAIL_EXIT_CODE)` + `render_hard_failure_artifact`; covered by `test_cli_doctor_exits_two_when_hard_capability_missing` + `test_cli_doctor_json_exit_two_includes_hard_failures_in_payload`. |
| `artifacts/D-0011/spec.md` documents the green-checklist format and JSON schema. | This file. |

## Out of scope for T01.13

- Full FR-G5 coverage gate evaluation — M4 T04.14 (the `--check-coverage` flag is wired now but only stamps a deferral marker).
- Real ptytest vendoring under `cli/eval/pty/` — M2 follow-up.
- Real MCP handshake probe (OQ-5) — M2 follow-up, override hook is
  `CapabilityGates(mcp_probe=…)`.
