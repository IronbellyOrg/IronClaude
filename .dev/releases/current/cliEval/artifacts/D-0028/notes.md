# D-0028 — Implementation notes (Task T02.07)

## Design choice: frozen dataclass + private mutable slot

DM-006 (T02.04) requires `HomeIsolation` to remain a frozen dataclass.
T02.07 adds methods that mutate process-local state (filesystem +
remembered HOME path). To square those requirements, the
implementation uses the standard frozen-dataclass escape hatch
`object.__setattr__(self, "_home_path", value)` to write one private
slot only. The four declared fields stay immutable; equality/hashing
ignore the private slot (it is never declared as a dataclass field).

Rejected alternatives:

* **Subclassing IsolationLayers** — would tie HomeIsolation lifecycle
  to the upstream record and risk breaking the COMP-012 probe.
* **Returning a separate `SetupHandle` from setup()** — would split
  the API surface across two classes, contradicting the deliverable
  language ("class HomeIsolation ... exposing setup/env/teardown/
  state_path").
* **`dataclass(frozen=False)`** — would break T02.04 explicitly and
  remove thread-safety in the parallel orchestrator (R-058 / T03.16).

## sibling-HOME concurrency

`tempfile.mkdtemp(prefix=f"{eval_id}-", dir=home_root)` is atomic on
POSIX per the CPython docs; the OS guarantees uniqueness. The 8-way
parallel test (`test_parallel_setup_does_not_collide`) exercises this
with a `threading.Barrier` to maximize collision probability and asserts
all 8 returned paths resolve to distinct directories.

## OQ-8 deferral

`time_offset_sec=0` (DM-006 default) keeps `CLAUDE_FAKE_TIME_OFFSET` out
of the env dict. This lets the FR-ISO1 plumbing land without waiting
for OQ-8 (DOC-OQ8 / T06.03). Callers that pass non-zero offsets get the
env var; everyone else gets the historic two-key dict.

## state_path lexical guard scope

Three layers of defense:
1. Reject absolute paths (`Path(suffix).is_absolute()`).
2. Reject any `..` component in the suffix parts.
3. Belt-and-braces `joined.relative_to(home_path)` check.

This is a lexical guard only — symlink-following containment is
intentionally deferred to FR-ISO2 (T02.08), where it belongs. Performing
symlink resolution here would force callers to materialize parent dirs
before calling `state_path`, which breaks the artifact-writer flow
that needs a path before the file is created.

## What changed

* `src/superclaude/cli/eval/isolation.py` — added 4 methods + `home_path`
  property + `is_set_up` predicate. Module docstring rewritten to
  document the FR-ISO1 surface alongside the DM-006 record contract.
* `tests/cli/eval/test_home_isolation_extend.py` — 35 new tests.

No changes to `src/superclaude/cli/sprint/executor.py` (the
`IsolationLayers` definition) — COMP-012 probe still green.

## Make sync-dev

Not required: this change is under `src/superclaude/cli/`, not the
distributable component directories (skills/agents/commands/core).
`make verify-sync` reports clean.
