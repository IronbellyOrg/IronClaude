# D-0008 — Capability dataclass spec

**Task:** T01.09 (Phase 1, Roadmap DM-007 / R-008)
**Module:** `src/superclaude/cli/eval/capabilities.py`
**Status:** Implemented 2026-05-20

## Field schema (5-field contract)

| Field | Type | Default | Purpose |
|---|---|---|---|
| `name` | `str` | required | Capability identifier (e.g. `binary.claude`, `mcp_server.auggie`). |
| `check` | `Callable[[], bool]` | required | Zero-arg callable returning `True` when the capability is satisfied. Not invoked at construction time; evaluated by `CapabilityGates.check_all()` (T01.11). |
| `failure_mode` | `Literal["hard", "skip", "xfail"]` | required | Gate tier per design-spec §11: `hard` aborts the run, `skip` marks gated evals SKIPPED, `xfail` marks them expected-fail. |
| `skip_flag` | `Optional[str]` | `None` | CLI flag (e.g. `--no-mcp`) that forces SOFT-SKIP behaviour even when the check would otherwise pass. |
| `description` | `str` | `""` | Human-readable label used by `eval doctor` output. |

## Invariants

- `@dataclass(frozen=True)` — mutation raises `dataclasses.FrozenInstanceError`.
- `__post_init__` validates `failure_mode` membership against the literal
  set `{"hard", "skip", "xfail"}` and raises `ValueError` for any other
  value (including `"HARD"`, `"hard "`, `""`, `"soft"`, etc.). This guards
  against typos in the static `CAPABILITIES` table that COMP-009 will
  declare in T01.11.
- Two instances built from identical arguments compare equal via the
  `@dataclass`-generated `__eq__`.
- The `check` callable is **not** invoked at construction time. Gate
  evaluation is deferred to `CapabilityGates.check_all()` so doctor
  output can stamp PASS/FAIL per capability rather than crashing at
  module import.

## `failure_mode` semantics (design-spec §11 cross-reference)

| Mode | Trigger | Run behaviour |
|---|---|---|
| `hard` | `check()` returns `False` for a HARD capability (e.g. `which claude` empty) | Abort run with exit code 2. |
| `skip` | `check()` returns `False`, **or** the user passes the descriptor's `skip_flag` (e.g. `--no-mcp`) | Mark gated evals SKIPPED with reason; continue. |
| `xfail` | Manifest declares `xfail_if:` and condition matched | Run, but expected-fail (status becomes XPASS if it passes anyway). |

## Caller contract (downstream consumers)

- COMP-009 `CapabilityGates` (T01.11) — instantiates a static
  `CAPABILITIES` list of these descriptors and iterates them in
  `check_all()`.
- `CapabilityReport` (T01.10) — collects PASS/FAIL per `Capability.name`
  and groups blocked evals by `failure_mode`.
- `eval doctor` (T01.13) — renders the green checklist using
  `description` and `failure_mode`.

## Acceptance criteria → implementation map

| AC bullet (T01.09) | Implementation site |
|---|---|
| Class `Capability` is a frozen dataclass exposing the 5 fields. | `capabilities.py` — `@dataclass(frozen=True) class Capability` |
| Instantiation with an invalid `failure_mode` raises `ValueError`. | `Capability.__post_init__` (covered by `test_capability_rejects_invalid_failure_modes`). |
| Two instances built from the same arguments compare equal. | `@dataclass`-generated `__eq__` (covered by `test_capability_deterministic_equality`). |
| `spec.md` records the 5-field contract. | This file. |

## Out of scope for T01.09

- The static `CAPABILITIES` table (`binary.claude`, `binary.jq`,
  `mcp_server.auggie`, …) — lives in COMP-009 (T01.11).
- `CapabilityReport` aggregate model — T01.10 (DM-008).
- `which_or_skip` / `mcp_server_reachable` implementations — T01.11.
- Wiring of `--no-mcp` CLI flag — T01.13.
