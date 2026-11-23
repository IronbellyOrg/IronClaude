# Reviewer 3 card (opus class, refactorer lens), persisted by the orchestrator

Self-reported confidence 0.80. Plan = `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/TASK-WF-buildRelease1OfT-20261111-164757.md`.

- R3-1 BLOCKING, drift (plan:140 vs spine:130): Task 8's `View` lists only display strings; AD-10 needs every frozen snapshot field (`cycle`, `generatedAt`, `producer`, `page.*`, `counts`, `scope`, `source.observedAt`, error code) in `View`, and Task 11 forbids `export.py` importing `parse.py`, so `snapshot_json(view)` cannot be built as written.
- R3-2 BLOCKING (narrow): no task carries the fixture-only `frozen` flag from the loader (plan:93) through `CycleResult` (plan:123) to the `FROZEN` marker Task 8 must render (T34).
- R3-3 MINOR: no module owns the real clock (spine:199 forbids direct `time` use); `generatedAt` and the live loop need one (suggest a `SystemClock` in `commands.py`).
- R3-4 MINOR, drift: `load_fixture` sits in `parse.py` (plan:93) although AD-7 (spine:112) says fixture-only fields are loaded by a separate loader, never by the live parser.
- R3-5 MINOR: Task 14 adds four golden files to `fixtures/`, while Task 5's test asserts the folder lists all ten variants (plan:100); golden files also become valid `--fixture` choices.
- R3-6 MINOR: Task 11 writes a new atomic writer although `swarm/atomic.py:14-39` exists; AD-11 authorizes one helper in `export.py`; `mkstemp` is already 0600.
- R3-7 MINOR: Task 6 should point at the house patterns `install_codegraph.py:43` (`Runner`) and `install_mcp.py:769` (`_bounded`, process-group kill).
- R3-8 MINOR (size): Task 8 (about 15 tests) and Task 12 (command, `--once`, platform guard, loop, snapshot writer) are large; suggest splitting.
- R3-9 NIT: Task 3 depends on Task 2 though `terminal.py` uses nothing from `sanitize.py`.
- R3-10: Tier 1 finding F1 (FixtureSource has no `source.namespace`) confirmed.

Checked with no finding: Task 13's block matches `main.py:559-561`; `tests/cli/test_cli_registration.py:31-49` checks a subset so `observe` does not break it; `_find_orca` reused unchanged; `jsonschema` and `pexpect` are dependencies (pyproject.toml:39, 41); pytest 9.2.0 (uv.lock:1161) enforces `--strict-markers`; the `--once` import chain has no POSIX-only module.
