# D-0064 — FR-EXP1 `Expect.*` primitive package spec

**Task:** T04.01 (Phase 4, Roadmap FR-EXP1 / COMP-010 / R-064)
**Module:** `src/superclaude/cli/eval/expect.py`
**Status:** Implemented 2026-05-20

## Surface

`Expect` is a static-method namespace exposing **seven** primitives,
each returning an `ExpectCallable = Callable[[EvalContext], ExpectResult]`:

| Primitive | COMP | Kwargs |
|---|---|---|
| `Expect.file` | COMP-010.1 | `path`, `exists`, `contains`, `regex`, `equals` |
| `Expect.jsonl` | COMP-010.2 | `path`, `line_count`, `filter`, `assert_each`, `assert_any` |
| `Expect.settings_json` | COMP-010.3 | `path`, `key_path`, `equals`, `exists` |
| `Expect.exit_code` | COMP-010.4 | `equals` (default 0), `in_set`, `not_equals` |
| `Expect.stderr` | COMP-010.5 | `contains`, `regex`, `not_contains` |
| `Expect.stdout` | COMP-010.5 | `contains`, `regex`, `not_contains` |
| `Expect.duration` | COMP-010.6 | `max_sec`, `min_sec` |

`PRIMITIVE_NAMES: tuple[str, ...]` enumerates the names in declaration
order and is the registry both `Expect.from_mapping` and the test surface
key off of.

## Invocation forms

Both forms produce equivalent `ExpectCallable`s:

* **Programmatic** — `Expect.exit_code(equals=0)`.
* **Declarative** — `Expect.from_mapping({"exit_code": {"equals": 0}})`.
  The mapping must have exactly one key (a primitive name); its value is
  forwarded verbatim as keyword arguments. Empty mapping values
  (`{"exit_code": {}}`) invoke the primitive with defaults.

`from_mapping` raises `ValueError` for unknown primitives or multi-key
mappings so manifest authors get a deterministic loader error rather
than a downstream TypeError at runtime.

## Result contract

Every primitive's returned callable wraps its body in `_timed_result`,
emitting an `ExpectResult` (DM-009) with the six fields populated:

* `name` — the primitive name (e.g. `"exit_code"`).
* `passed` — boolean.
* `message` — terse human-readable summary.
* `details` — JSON-shaped mapping (path / actual / observed_sec / etc.).
* `duration_sec` — wall-clock seconds the assertion took.
* `failure` — `ExpectFailure` (DM-005) on failure, `None` on pass.

Closures preserve `__name__` via `_named_callable(name, fn)` so the
runner's JSONL log wrapper (T03.08) records the primitive name verbatim.

## Path resolution

* Absolute paths are returned untouched.
* Relative paths resolve against `ctx.home_path` (per-eval HOME via
  `HomeIsolation` / DM-006).
* `Expect.jsonl` additionally checks `ctx.jsonl_paths` first; a manifest
  can address `{path: "hook_log"}` and the primitive resolves that
  through the named registry before falling back to filesystem
  resolution.

## Exit code mutual-exclusion guard

`Expect.exit_code(equals=..., in_set=...)` raises `ValueError` at
construction time. The default `equals=0` does **not** trigger the
guard — only explicit kwargs (detected via a module-level
`_SENTINEL` sentinel) count.

## Stream ANSI stripping

`Expect.stdout` / `Expect.stderr` re-strip ANSI escape sequences via
`pty_stream.ANSI_ESCAPE_RE` defensively, even though `PtyStream` already
strips on capture (T02.17). This keeps the primitives correct when
manifest authors feed raw transcript fixtures from `transcript_path`
into a custom predicate.

## Deferred coverage

Per-primitive negative cases and edge coverage land in T04.02..T04.08:

* T04.02 — `file.contains` substring negative cases + UTF-8 round-trip.
* T04.03 — `file.regex` pattern matching + invalid regex error path.
* T04.04 — `jsonl.line_count` / `assert_each` / `assert_any` matrices.
* T04.05 — `exit_code` boundary cases (already prototyped in T04.01).
* T04.06 — `stderr` / `stdout` ANSI stripping regression.
* T04.07 — `duration` `max_sec` / `min_sec` boundary precision.
* T04.08 — `settings_json` deep `key_path` traversal + None-vs-missing.
