# D-0001 — implementation notes

## Decisions made during build

1. **Module path:** Used `src/superclaude/cli/eval/config.py` per the task
   step `[EXECUTION] Add EvalConfig frozen dataclass module under
   src/superclaude/cli/eval/config.py`. The `cli/eval/` package was created
   fresh as this is the first cliEval landing.

2. **`allowed_scratch_roots` type → `tuple[Path, ...]`.** A tuple is the
   minimal hashable, immutable, ordered container — preferable to `list` for
   a frozen dataclass field, and preferable to `frozenset` because AC12 is
   an ordered allowlist (the first matching root wins downstream).

3. **Default factory function.** `_default_allowed_scratch_roots()` is a
   module-level function rather than an inline lambda so it remains
   introspectable from tests and from any future serialization layer.

4. **`paths` / `defaults` typed as `Mapping`.** Public-facing read-only
   protocol; concrete `dict` defaults are still constructed per-instance via
   `default_factory=dict`. This keeps the API permissive (callers may pass
   any mapping) while default behaviour is independent per instance.

5. **No I/O at import time.** EvalConfig does not call any of the AC12
   allowlist roots — it only holds the configured tuple. Resolution and
   path-containment enforcement land in T01.19 (COMP-005 path guard).

## Things deliberately NOT in scope of T01.01

- Path-containment enforcement (`is_under_allowlist`) — T01.19.
- Resolution of `--output-dir` against the allowlist — T01.19.
- `CLAUDE_FAKE_TIME_OFFSET` plumbing (OQ-8) — deferred to T06.03.
- A `from_dict()` factory loading config from disk — not required by
  T01.01 acceptance criteria; manifest loading lives in COMP-002 (T01.07).
