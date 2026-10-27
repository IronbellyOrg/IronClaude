# D-0028 — HomeIsolation FR-ISO1 method surface (Task T02.07)

## Scope

Extend `superclaude.cli.eval.isolation.HomeIsolation` (the DM-006 frozen
dataclass landed in T02.04) with the four COMP-006 methods that FR-ISO1
requires the per-eval HOME primitive to expose:

| Method | Signature | Responsibility |
|---|---|---|
| `setup` | `() -> Path` | `mkdtemp` under `home_root` with `eval_id-` prefix; record on private slot; return path. One-shot per setup call. |
| `env` | `() -> dict[str, str]` | Return `{HOME, CLAUDE_SESSION_ID}` always; add `CLAUDE_FAKE_TIME_OFFSET` only when `time_offset_sec != 0`. |
| `teardown` | `(keep: bool) -> None` | `keep=True` preserves the directory; `keep=False` removes it. Always clears the private slot. No-op if `setup` never ran. |
| `state_path` | `(suffix: str) -> Path` | Join `suffix` under the active per-eval HOME after rejecting absolute paths and `..` components. |

## Method contract

* DM-006 invariants preserved — the four declared fields
  (`eval_id`, `home_root`, `session_id`, `time_offset_sec`) remain
  immutable, equality and hashing unchanged. The dynamic HOME path
  lives on a private `_home_path` slot written via
  `object.__setattr__`, the documented escape hatch for frozen
  dataclasses.
* `setup` calls `home_root.mkdir(parents=True, exist_ok=True)` and then
  `tempfile.mkdtemp(prefix=f"{eval_id}-", dir=home_root)`. The
  `mkdtemp` atomicity guarantee gives sibling-HOME concurrency for free
  — see the parallel-setup test
  (`tests/cli/eval/test_home_isolation_extend.py::test_parallel_setup_does_not_collide`).
* Calling `setup` twice on the same instance raises `RuntimeError` so
  the atomic-setup wrapper in T02.13 has a clean failure surface. After
  `teardown` clears the slot, `setup` may be re-invoked.
* `env` is a pure function over the current record + dynamic
  `home_path`. It returns a fresh dict each call (no caller-visible
  aliasing).
* `teardown` always clears the private slot, even on `keep=True`,
  even if `rmtree` raises — ownership of the HOME relinquishes once
  teardown begins.
* `state_path` performs a lexical containment check (`is_absolute`
  + `'..' not in parts` + final `relative_to(home_path)` belt-and-
  braces). Full symlink-resolution containment lands in T02.08
  (FR-ISO2).

## Upstream `IsolationLayers` preservation

`HomeIsolation` does NOT subclass or mutate the four-layer record at
`src/superclaude/cli/sprint/executor.py:107-182`. The COMP-012 probe
(`tests/cli/eval/test_isolation_layers_probe.py`, T02.05) re-runs green
after this change — verified directly by
`tests/cli/eval/test_home_isolation_extend.py::test_isolation_layers_probe_still_passes_after_extension`,
which imports the probe and re-invokes every assertion. The env-var
keysets are disjoint:

* `IsolationLayers.env_vars` —
  `{CLAUDE_WORK_DIR, GIT_CEILING_DIRECTORIES, CLAUDE_PLUGIN_DIR, CLAUDE_SETTINGS_DIR}`
* `HomeIsolation.env()` —
  `{HOME, CLAUDE_SESSION_ID}` (+ optional `CLAUDE_FAKE_TIME_OFFSET`)

The orchestrator (T03.16) merges both dicts without coercion;
disjoint keys make the merge deterministic.

## OQ-8 (`CLAUDE_FAKE_TIME_OFFSET`) gating

`time_offset_sec=0` (DM-006 default) keeps the variable out of the env
dict. Only callers that explicitly pass a non-zero offset get the env
var; on hosts where OQ-8 has not yet resolved, leaving `time_offset_sec`
at default makes the wiring inert. Acceptance criterion
"env() returns a dict containing HOME, CLAUDE_SESSION_ID, optional
CLAUDE_FAKE_TIME_OFFSET" is satisfied.

## Test coverage (D-0028 evidence)

`tests/cli/eval/test_home_isolation_extend.py` (35 tests):

* setup / mkdtemp behavior (5 tests).
* sibling-HOME isolation + 8-way parallel setup (2 tests).
* env() contract — required keys, OQ-8 gating, fresh dict, type pinning (7 tests).
* state_path lexical containment (10 tests).
* teardown keep/remove + slot lifecycle (6 tests).
* DM-006 invariants preserved (3 tests).
* IsolationLayers probe re-verification + env-key disjointness (2 tests).

All tests pass — full eval suite: 402 passed in 1.00s.

## Cross-links

* DM-006 record contract: `tests/cli/eval/test_isolation_dataclass.py` (T02.04).
* COMP-012 probe pin: `tests/cli/eval/test_isolation_layers_probe.py` (T02.05).
* FR-ISO2 containment guard: T02.08 (D-0029).
* COMP-006 full assembly: T02.11 (D-0032).
* NFR-ISO2 atomic setup: T02.13 (D-0033).
* Hook adapter idempotency: T02.14 (D-0034).
