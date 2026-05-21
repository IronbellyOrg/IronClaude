# D-0027 — Implementation notes (T02.05)

## Design choices

* **Read-only via `inspect.getattr_static`.** Using `getattr` on the
  class would have invoked the property descriptor and required an
  instance. `inspect.getattr_static` returns the raw `property` object,
  so the probe can assert `isinstance(attr, property)` without touching
  any state. This is the discipline the task description called for
  ("probe is read-only; no IsolationLayers state is touched").
* **Return-annotation pinning over body inspection.** Pinning return
  annotations (`get_type_hints(fget)["return"]`) catches the kind of
  refactor most likely to break HomeIsolation extension (a developer
  changing the dict shape or list type to satisfy a new caller) without
  forcing the probe to re-implement the property's behaviour.
* **Parametrised field-type check.** Each field gets its own parametrise
  id so a partial regression (e.g., one field switched from `Path` to
  `str`) lights up the offending field by name in the test report.
* **No instance construction.** `setup_isolation` is pinned by
  `inspect.signature` rather than by calling it; this avoids a
  dependency on `SprintConfig` fixturing inside what is meant to be a
  static-surface probe.

## Why these particular pins

The four fields and two properties are the *load-bearing* surface for
HomeIsolation extension:

* `scoped_work_dir`, `git_boundary`, `plugin_dir`, `settings_dir` —
  the 4 existing isolation guarantees referenced by FR-ISO1 acceptance
  criteria; HomeIsolation must preserve all four when it adds the HOME
  layer. If a rename happens here, COMP-006 silently loses an isolation
  guarantee.
* `env_vars` — the canonical merge point that HomeIsolation's `env()`
  must layer over (HOME, CLAUDE_SESSION_ID, optional
  CLAUDE_FAKE_TIME_OFFSET on top of the 4 existing env keys). Drift in
  the return type would break a `dict.update` merge.
* `layers_active` — used by the IsolationLayers probe and downstream
  verification to confirm the layers are present on disk; HomeIsolation
  contributes an additional "home_root" layer via the same pattern.

The `setup_isolation` factory pin guards the construction signature so
the parallel orchestrator (T03.16) can keep its call-site stable while
the HomeIsolation extension lands.

## Mutation evidence

A dry-run mutation on 2026-05-20 renamed
`IsolationLayers.layers_active` → `layers_activeX`. The probe lit up
with two `AttributeError: layers_active` failures (one for the property
check, one for the return-annotation check). Pristine `executor.py` was
restored via byte-identical `diff` comparison and the probe returned
green (13/13). This satisfies the "fails on a synthetic mutation"
acceptance bullet.

## Risks / open items

* If `executor.py` is reorganised so that `IsolationLayers` moves to a
  dedicated module before HomeIsolation extension lands, the import
  pins and `__module__` assertion will trip. That is the intended
  behaviour — the rename should be re-pinned deliberately, not
  silently followed.
* `_EXPECTED_FIELDS` lives in the test file (no shared catalogue with
  `executor.py`). This duplication is intentional: the probe must
  capture the *expected* surface, not derive it from the live module.
