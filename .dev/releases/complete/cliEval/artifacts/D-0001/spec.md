# D-0001 — EvalConfig dataclass spec

**Task:** T01.01 (Phase 1, Roadmap COMP-005 / R-001)
**Module:** `src/superclaude/cli/eval/config.py`
**Status:** Implemented 2026-05-20

## Field schema

| Field | Type | Default | Purpose |
|---|---|---|---|
| `paths` | `Mapping[str, Path]` | `{}` | Resolved filesystem locations (suites dir, output dir, etc.). |
| `defaults` | `Mapping[str, object]` | `{}` | Per-eval default knobs (timeout, isolation mode, parallelism). |
| `allowed_scratch_roots` | `tuple[Path, ...]` | `(Path("/tmp/eval-runs"), Path(".dev/eval-runs"))` | AC12 allowlist of directories where scratch HOMEs / per-eval working trees may live. Any path resolution that escapes this allowlist must be rejected before any FS write. |

## Defaults

`allowed_scratch_roots` default list (in order):
1. `/tmp/eval-runs`
2. `.dev/eval-runs`

The defaults are produced by `_default_allowed_scratch_roots()` (module-level
factory) so the immutable tuple is rebuilt for each instance — preserving
frozen-dataclass equality semantics without mutable shared state.

## Invariants

- `@dataclass(frozen=True)` — attempted mutation raises `dataclasses.FrozenInstanceError`.
- Two instances built from identical inputs compare equal (`__eq__` auto-generated).
- `allowed_scratch_roots` is a `tuple`, so it is hashable and immutable.
- `paths` and `defaults` use `field(default_factory=dict)` — each instance gets
  its own mapping, so default-only instances do not share mutable state.

## Caller contract (downstream consumers)

- COMP-002 SuiteLoader (T01.07) — reads `paths` to resolve manifest directory.
- COMP-005 path-containment guard (T01.19) — reads `allowed_scratch_roots`
  to enforce AC12 before any FS write.
- COMP-004 HomeIsolation (Phase 2) — reads `allowed_scratch_roots` for the
  scratch-root refuse-to-operate hard guard.

## OQ-8 status

OQ-8 (`CLAUDE_FAKE_TIME_OFFSET` consumption) is **not yet resolved**. Per the
phase-1-tasklist Notes for T01.01, this is acceptable here — OQ-8 may be
deferred via T06.03 decision. EvalConfig does not currently expose a field
for this offset; if OQ-8 resolves before COMP-005 close, a `time_offset`
field will be added under `defaults` rather than as a top-level attribute,
to preserve the 3-field public contract documented above.

## Acceptance criteria → implementation map

| AC | Implementation site |
|---|---|
| Module exports frozen `EvalConfig` with 3 named fields. | `config.py` — `@dataclass(frozen=True) class EvalConfig` |
| Mutation rejected. | `frozen=True` → `FrozenInstanceError` (covered by `test_evalconfig_is_frozen`). |
| Default `allowed_scratch_roots` contains `/tmp/eval-runs` and `.dev/eval-runs`. | `_default_allowed_scratch_roots()` (covered by `test_default_allowed_scratch_roots_includes_ac12_paths`). |
| Identical inputs → equal instances. | `@dataclass`-generated `__eq__` (covered by `test_deterministic_equality`). |
