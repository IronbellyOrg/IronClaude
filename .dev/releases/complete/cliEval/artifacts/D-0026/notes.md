# D-0026 — implementation notes

## Decisions made during build

1. **Module location.** Added `HomeIsolation` to a new
   `src/superclaude/cli/eval/isolation.py` rather than to `models.py`
   alongside `EvalSpec` / `ExpectResult` / `ExpectFailure`. The phase-2
   tasklist (T02.04) explicitly names `isolation.py` as the destination
   and downstream COMP-006 work (T02.07, T02.08, T02.11) will land more
   methods and the `containment_guard` function in the same module. Co-
   locating the dataclass with the methods that operate on it keeps the
   import surface clean and avoids a circular import between `models` and
   the future `containment_guard` (which would otherwise need to import
   the record from `models`).

2. **`__post_init__` calls `validate_eval_id`.** DM-006 does not
   explicitly mandate validation in the dataclass, but the T02.04
   acceptance criteria require "Construction with an unsafe `eval_id`
   raises `InvalidEvalId` (delegated to `validate_eval_id`)". Delegating
   to the existing FR-SCH2 guard (T01.05) rather than re-implementing
   the regex avoids drift: there is one source of truth for the
   acceptable-id surface, and any future tightening of the regex flows
   through to this dataclass automatically.

3. **`home_root` typed as `pathlib.Path`, stored verbatim.** DM-006
   declares the field as `Path`. The dataclass does not call
   `resolve()`, `expanduser()`, or any containment check at construction
   time — that is FR-ISO2's job (T02.08) and adding it here would force
   the unit tests to mkdtemp a real directory just to construct a record,
   which slows the test suite and conflates the record contract with the
   guard contract.

4. **`time_offset_sec` kept regardless of OQ-8 state.** The DOC-OQ8
   resolution (T06.03) decides whether `CLAUDE_FAKE_TIME_OFFSET` is
   actually plumbed through to the subprocess env. Either way the
   record's contract is stable — the field stays at type `int`, default
   `0`. If OQ-8 closes "no", downstream `HomeIsolation.env()` (T02.07)
   simply omits the env var; the dataclass surface does not need to
   change.

5. **No `to_dict()` method.** Unlike `ExpectResult` / `ExpectFailure`,
   `HomeIsolation` is not serialised into the JSON report. It is an
   internal handle threaded through the orchestrator → runner pipeline.
   Adding `to_dict()` now would be speculative; if a reporter ever needs
   to render isolation state (e.g. for a "what HOME ran this eval" line)
   the addition will be non-breaking (frozen-dataclass plus a new
   method).

6. **Re-validation cost is acceptable.** `validate_eval_id` does a
   single compiled-regex `fullmatch` plus a type check. On the orchestrator
   hot path each eval allocates exactly one `HomeIsolation`, so the
   amortised cost is negligible. The defence-in-depth benefit (loader
   bypass cannot smuggle an unsafe id into the record) outweighs the
   micro-cost.

7. **Package re-export.** Added `HomeIsolation` to
   `src/superclaude/cli/eval/__init__.py`'s `__all__` so callers can
   `from superclaude.cli.eval import HomeIsolation` — symmetric with
   `EvalSpec`, `ExpectResult`, and `ExpectFailure`. Locked by
   `test_home_isolation_importable_from_package`.

8. **Test file naming.** `tests/cli/eval/test_isolation_dataclass.py`
   matches the verification command named in the T02.04 step list. The
   broader `test_home_isolation.py` (T02.11) and
   `test_home_isolation_extend.py` (T02.07) modules will land alongside
   later; keeping the per-task test surfaces in separate files avoids
   noisy merge conflicts as the COMP-006 implementation grows.

## Things deliberately NOT in scope of T02.04

- `HomeIsolation.setup() / env() / teardown(keep) / state_path(suffix)` —
  COMP-006 (T02.07 FR-ISO1, T02.11).
- Path containment guard (`containment_guard`) — FR-ISO2 / T02.08.
- Real `CLAUDE_FAKE_TIME_OFFSET` env wiring — gated on OQ-8 (DOC-OQ8 /
  T06.03).
- Defence-in-depth tests for symlink escape / scratch-root escape —
  NFR-SEC2 / T02.09.
- Hard-guard tests against real `~/.claude/` — NFR-SEC3 / T02.10.

## Risks observed during build

- **Type-annotation string form.** The dataclass uses
  `from __future__ import annotations` so `dataclasses.fields(...).type`
  returns the annotation string (`"Path"`, not the actual `Path` class).
  The test asserts the string form on purpose; a future shift to PEP 649
  / runtime annotations would change this and the assertion can be
  switched to `typing.get_type_hints(HomeIsolation)` if/when that lands.

- **`InvalidEvalId` is a plain `Exception` (T01.05).** The dataclass does
  not wrap it in a more specific isolation error. Callers downstream
  (COMP-006 / T02.07) may decide to convert it into a richer
  `HomeContainmentViolation`; doing so here would couple the record
  contract to a not-yet-landed exception class.
