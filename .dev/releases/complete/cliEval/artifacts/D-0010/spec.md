# D-0010 — CapabilityGates spec

**Task:** T01.11 (Phase 1, Roadmap COMP-009 / R-010)
**Module:** `src/superclaude/cli/eval/capabilities.py`
**Status:** Implemented 2026-05-20

## Class surface

`CapabilityGates(skip_flags=None, capabilities=None, mcp_probe=None)`

| Method / property | Returns | Purpose |
|---|---|---|
| `check_all()` | `CapabilityReport` | Run every spec through its probe and build the report. Acceptance: idempotent across repeated calls on the same instance. |
| `which_or_skip(name)` | `tuple[bool, str]` | PATH probe via `shutil.which`. Detail = resolved path on hit, `"not found on PATH"` on miss. |
| `mcp_server_reachable(name)` | `tuple[bool, str]` | MCP reachability probe. OQ-5 M1 stub: PATH presence. Detail = resolved path or `"MCP server binary not on PATH"`. |
| `capabilities()` | `tuple[Capability, ...]` | Materialise the static spec table as `Capability` instances whose `check` closures defer to the gate's own probes (no duplicate logic). |
| `skip_flags` (prop) | `tuple[str, ...]` | Active CLI flags, sorted + deduplicated. Propagates onto `CapabilityReport.skip_flags`. |

## Static binary roster (HARD / SOFT-SKIP semantics)

| Capability `name` | `target` binary | `kind` | `failure_mode` | `skip_flag` | `description` |
|---|---|---|---|---|---|
| `binary.claude` | `claude` | binary | `hard` | — | Claude CLI on PATH |
| `binary.make` | `make` | binary | `hard` | — | GNU make on PATH |
| `binary.jq` | `jq` | binary | `hard` | — | jq JSON processor on PATH |
| `binary.git` | `git` | binary | `hard` | — | git VCS on PATH |
| `mcp_server.auggie` | `auggie` | mcp_server | `skip` | `--no-mcp` | Auggie MCP server reachable |
| `mcp_server.auggie-mcp` | `auggie-mcp` | mcp_server | `skip` | `--no-mcp` | auggie-mcp MCP server reachable |
| `mcp_server.airis-mcp-gateway` | `airis-mcp-gateway` | mcp_server | `skip` | `--no-mcp` | AIRIS MCP gateway reachable |

Roster ordering matches design-spec §11 (HARD binaries first, then
SOFT-SKIP MCP servers) so `eval doctor` (T01.13) renders a stable
green-checklist layout.

## HARD vs SOFT-SKIP semantics

* **HARD** — `which_or_skip(target)` returns `(False, …)` →
  `CapabilityStatus.passed = False`, name lands in
  `CapabilityReport.hard_failures`. The doctor + run pre-flight MUST
  exit 2 when `hard_failures` is non-empty (consumed in T01.13).
* **SOFT-SKIP** — probe fails OR `skip_flag` is present in
  `skip_flags` → `CapabilityStatus.passed = False`, name lands in
  `CapabilityReport.soft_skips`. `skipped_by_flag` carries the override
  bit so doctor can render "would have passed at <path>, skipped by
  --no-mcp".
* **SOFT-XFAIL** — reserved for manifest-driven `xfail_if:`
  conditions; the gate honours `failure_mode="xfail"` on custom spec
  tuples (test coverage:
  `test_xfail_capability_classifies_into_soft_xfails`). The default
  roster does not declare any xfail capabilities.

## `CapabilityReport` field population

| Field | Populated by `check_all` | Note |
|---|---|---|
| `report` | one `CapabilityStatus` per spec in declaration order | Tuple, frozen, JSON-safe via `to_dict`. |
| `blocked_evals` | empty | SuiteLoader (T01.07) populates this once it knows the eval-to-capability mapping. |
| `skip_flags` | sorted, deduplicated `frozenset` | Mirrors the constructor input. |
| `hard_failures` | names of HARD capabilities whose probe failed | Drives exit-2 from doctor/run pre-flight. |
| `soft_skips` | names of SKIP capabilities whose probe failed or were flag-overridden | Reported but not fatal. |
| `soft_xfails` | names of XFAIL capabilities whose probe failed | Reported but not fatal. |

## OQ-5 deferral

`mcp_server_reachable(name)` currently uses **PATH presence** as the
reachability signal because every MCP server in the default roster
ships as an executable. The roadmap Open Question OQ-5 ("Exact MCP
server reachability check semantics") is targeted to resolve **before
COMP-009 close at M2**.

The override hook is the `mcp_probe` constructor keyword:

```python
gate = CapabilityGates(mcp_probe=lambda name: (passed, detail))
```

The M2 follow-up will land a real handshake probe behind the same
signature so the gate's public surface does not change. Tests use this
hook to simulate reachable / unreachable servers without touching
`shutil`.

## Invariants

- `check_all()` is idempotent — repeated calls on the same instance
  produce equal reports (covered by `test_check_all_is_idempotent`).
- `CapabilityStatus` rows preserve declaration order so doctor output
  is stable.
- `skip_flags` are deduplicated and sorted before being emitted onto
  the report.
- Unknown capability kinds raise `ValueError` at `check_all()` time —
  guards against typos in a custom spec tuple from silently producing
  always-passing rows.

## Caller contract (downstream consumers)

- **`eval doctor`** (FR-CLI4 / T01.13) — calls `CapabilityGates().check_all().to_json()` for the `--json` output and renders `report[]` rows into the green checklist.
- **`eval run` pre-flight** (M2) — inspects `hard_failures` to decide whether to abort (exit 2) and consumes `soft_skips` + `--no-mcp` to mark dependent evals SKIPPED.
- **`SuiteLoader`** (T01.07) — does NOT currently inject `CapabilityGates`; uses the `PermissiveCapabilityResolver` stub. T01.13 wires the real gate through `commands.py`. Downstream may also adapt `CapabilityGates` to the `CapabilityResolver` protocol (`resolve(eval_id, required)`) when the loader → gate seam lands; the spec table provides the mapping needed for that.

## Acceptance criteria → implementation map

| AC bullet (T01.11) | Implementation site |
|---|---|
| Class `CapabilityGates` exposes `check_all()`, `which_or_skip()`, `mcp_server_reachable()` and returns a populated `CapabilityReport`. | `capabilities.py` — `CapabilityGates` methods. |
| Missing `claude` on PATH classifies HARD. | `_probe` → `which_or_skip` → `hard_failures`. Covered by `test_missing_claude_classifies_hard`. |
| Missing MCP server classifies SOFT-SKIP under `--no-mcp`. | `_probe` → `mcp_server_reachable` → `soft_skips`. Covered by `test_missing_mcp_server_classifies_soft_skip` + `test_no_mcp_flag_skips_even_when_servers_are_reachable`. |
| `check_all()` is idempotent. | Pure read against PATH / probe; covered by `test_check_all_is_idempotent`. |
| `spec.md` documents the binary roster and HARD/SOFT semantics. | This file. |

## Out of scope for T01.11

- `claude` minimum-version check (`>=0.5.0`) — lands in `eval doctor` (T01.13).
- `~/.claude/` directory existence check — T01.13.
- Vendored ptytest presence check — T01.13.
- Coverage gate (`--check-coverage`) — M4 T04.14.
- Wiring `CapabilityGates` as the `SuiteLoader` resolver — T01.13.
- Real MCP handshake probe — M2 follow-up resolving OQ-5.
