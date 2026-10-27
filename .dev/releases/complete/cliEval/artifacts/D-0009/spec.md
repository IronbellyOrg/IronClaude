# D-0009 — CapabilityReport dataclass spec

**Task:** T01.10 (Phase 1, Roadmap DM-008 / R-009)
**Module:** `src/superclaude/cli/eval/capabilities.py`
**Status:** Implemented 2026-05-20

## Field schema (6-field contract per DM-008)

| Field | Type | Default | Purpose |
|---|---|---|---|
| `report` | `tuple[CapabilityStatus, ...]` | `()` | Per-capability outcome rows for the doctor green-checklist. |
| `blocked_evals` | `tuple[str, ...]` | `()` | Eval ids gated off because a capability they depend on failed or was skip-flagged. |
| `skip_flags` | `tuple[str, ...]` | `()` | CLI flags currently active (e.g. `--no-mcp`) that force soft-skip behaviour. |
| `hard_failures` | `tuple[str, ...]` | `()` | Names of capabilities classified `hard` that failed; doctor exits 2 when this is non-empty (FR-CLI4 / T01.13). |
| `soft_skips` | `tuple[str, ...]` | `()` | Names of capabilities classified `skip` that failed or were skip-flagged. |
| `soft_xfails` | `tuple[str, ...]` | `()` | Names of capabilities classified `xfail` that failed. |

Tuples are used instead of lists so `CapabilityReport` is frozen and
hashable; `to_json()` converts each tuple to a JSON array.

## `CapabilityStatus` helper (per `report[]` entry)

| Field | Type | Default | Purpose |
|---|---|---|---|
| `name` | `str` | required | Capability identifier mirroring `Capability.name` (e.g. `binary.claude`). |
| `passed` | `bool` | required | `True` when the capability's `check()` succeeded and no skip-flag was active. |
| `failure_mode` | `Literal["hard","skip","xfail"]` | required | Validated by `__post_init__`; `ValueError` on any other value. |
| `description` | `str` | `""` | Human-readable label (mirrors `Capability.description`). |
| `detail` | `str` | `""` | Resolved binary path on success or error message on failure. |
| `skipped_by_flag` | `bool` | `False` | `True` when the capability would have passed but was forced down by `Capability.skip_flag`. |

## `to_json()` contract

Returns a `dict[str, Any]` that is directly JSON-serialisable. Keys
preserve the dataclass field order so `eval doctor --json` payloads are
stable across invocations.

### Empty report — canonical shape

```json
{
  "report": [],
  "blocked_evals": [],
  "skip_flags": [],
  "hard_failures": [],
  "soft_skips": [],
  "soft_xfails": []
}
```

### Populated report — example

```json
{
  "report": [
    {
      "name": "binary.claude",
      "passed": true,
      "failure_mode": "hard",
      "description": "Claude CLI on PATH",
      "detail": "/usr/local/bin/claude (v0.5.3)",
      "skipped_by_flag": false
    },
    {
      "name": "mcp_server.airis-mcp-gateway",
      "passed": false,
      "failure_mode": "skip",
      "description": "AIRIS MCP gateway reachable",
      "detail": "connection refused",
      "skipped_by_flag": false
    }
  ],
  "blocked_evals": ["E5"],
  "skip_flags": ["--no-mcp"],
  "hard_failures": [],
  "soft_skips": ["mcp_server.airis-mcp-gateway"],
  "soft_xfails": []
}
```

## Invariants

- `@dataclass(frozen=True)` — mutation raises `dataclasses.FrozenInstanceError`.
- Defaults provided by `field(default_factory=tuple)`, so
  `CapabilityReport()` constructs an empty-but-valid report.
- `to_json()` is a pure function of the dataclass state; calling it
  twice on the same instance returns equal dicts.
- Tuple ordering is preserved as supplied by the caller. Determinism is
  the caller's responsibility — downstream doctor snapshot tests
  (T01.13) may sort independently if byte-level determinism is needed
  (see Notes in `phase-1-tasklist.md` T01.10).

## Caller contract (downstream consumers)

- **COMP-009 `CapabilityGates.check_all()`** (T01.11) — constructs and
  returns a `CapabilityReport` after iterating the static `CAPABILITIES`
  table.
- **`eval doctor`** (FR-CLI4 / T01.13) — calls `to_json()` for the
  `--json` output and renders `report[]` rows into the green checklist.
- **`eval run` pre-flight** — inspects `hard_failures` to decide whether
  to abort (exit 2) and `blocked_evals` to mark evals SKIPPED.

## Acceptance criteria → implementation map

| AC bullet (T01.10) | Implementation site |
|---|---|
| Class `CapabilityReport` exposes the 6 list fields and a `to_json()` method. | `capabilities.py` — `@dataclass(frozen=True) class CapabilityReport` + `to_json()`. |
| `to_json()` produces a JSON-serializable mapping per DM-008. | `to_json()` returns `dict[str, Any]` (covered by `test_capability_report_to_json_returns_mapping`). |
| Empty report serialises to a stable canonical form. | See "Empty report — canonical shape" above (covered by `test_capability_report_empty_to_json_canonical_shape`). |
| `spec.md` records the JSON shape. | This file. |

## Out of scope for T01.10

- Static `CAPABILITIES` table (`binary.claude`, `binary.jq`, …) — lives
  in COMP-009 (T01.11).
- `which_or_skip` / `mcp_server_reachable` implementations — T01.11.
- Doctor CLI rendering and `--json` flag wiring — T01.13.
- Byte-stable snapshot determinism — derived doctor-test requirement,
  not in DM-008 (see Notes in T01.10).
