# T02.11 — Evidence (Implement COMP-006 HomeIsolation full component)

**Deliverable**: D-0032 (see
`.dev/releases/current/cliEval/artifacts/D-0032/`).

## Test command

```
uv run pytest tests/cli/eval/test_home_isolation.py -v
```

**Result**: `27 passed in 0.15s` — see `pytest-T02.11.log`.

## Phase-2 isolation suite (no regression)

```
uv run pytest tests/cli/eval/test_home_isolation_extend.py \
  tests/cli/eval/test_path_containment.py \
  tests/cli/eval/test_defense_in_depth.py \
  tests/cli/eval/test_hard_guard_real_home.py \
  tests/cli/eval/test_home_isolation.py -v
```

**Result**: `137 passed in 0.32s`.

## Acceptance criteria → test mapping

See `.dev/releases/current/cliEval/artifacts/D-0032/spec.md`
("Acceptance criteria → test mapping" table) for the full per-AC
test pointer table.

## Files

* `tests/cli/eval/test_home_isolation.py` (new, 27 tests).
* `.dev/releases/current/cliEval/artifacts/D-0032/{spec,notes,evidence}.md`.
* `.dev/releases/current/cliEval/evidence/T02.11/pytest-T02.11.log`.

No `src/` code change — see D-0032 notes for rationale (COMP-006
finalization is a test-only gate that confirms the FR-ISO1 + FR-ISO2
integrated contract; the install_hooks adapter consumes the existing
public `HomeIsolation.home_path` property and lands in T02.14 / D-0034).
