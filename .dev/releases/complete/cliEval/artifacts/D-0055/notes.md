# D-0055 — Implementation notes (T03.13)

## Design decisions

### Reporter delegates to module-level renderers

The four `to_*` methods are thin shims over `render_summary_markdown`,
`render_summary_yaml`, `render_summary_json`, and `render_junit_xml`.
Rationale:

* The `_check_invariant` guard already exists at the entry of each
  module-level renderer (landed in T03.11). Delegating keeps a single
  source of truth for the FR-RPT1 N'-vs-K invariant — adding a second
  guard layer in the class would risk drift between the two.
* The module-level renderers are also the function-call API
  `write_aggregated_report` uses; keeping the class on top of them
  means the class output is byte-identical to the writer's file
  content (verified by `test_to_*_matches_module_renderer`).
* The frozen-dataclass shape reads as a value object: `Reporter` is a
  view over a `RunSummary` plus a feature flag, not a state machine.

### Reporter is a frozen dataclass, not a regular class

Three reasons to freeze the class:

1. **Byte-stability**: a Reporter consumer cannot swap `self.summary`
   between two `to_markdown()` calls, so the byte-stable property
   holds structurally rather than by convention.
2. **Equality / hashability**: callers that cache reports by Reporter
   instance get free deduplication.
3. **Mirrors `AggregatedPhaseReport`** (the sprint executor's pattern
   reference) which is also `@dataclass`. The probe test in T03.14
   pins the upstream class shape; matching the dataclass convention
   keeps the two surfaces visually congruent.

### YAML renderer uses `sort_keys=False` + `default_flow_style=False`

* `sort_keys=False` preserves the DM-004 declaration order
  `summary.to_dict()` produces. The acceptance criteria emphasise
  byte stability — sorting would change with future field additions
  whereas declaration order is stable across schema bumps.
* `default_flow_style=False` produces canonical block style (one key
  per line) which diffs cleanly in code review and matches the
  convention `AggregatedPhaseReport.to_yaml()` follows in the sprint
  executor.
* `allow_unicode=True` ensures emoji-rich titles round-trip without
  escape sequences.

### `Reporter.write` writes summary.yaml too

The acceptance criterion lists four emitter methods, not four output
files. The decision is whether `write()` emits the YAML to disk by
default. Two options were considered:

* **A**: `write()` emits markdown + JSON only (matches the existing
  `write_aggregated_report`); YAML stays a `to_yaml()`-only string.
* **B**: `write()` emits markdown + JSON + YAML; JUnit XML stays gated.

Picked **B** because:
* The four emitter methods all return strings — having three of the
  four writable to disk by default and one (YAML) string-only would
  read as an oversight rather than a design choice.
* YAML's role per design-spec §9 is the human-editable summary
  format; emitting it next to summary.md / summary.json keeps the
  three artefacts available for consumers without composing four
  separate calls.
* The feature gate the acceptance criterion calls out is for JUnit
  XML specifically, not YAML.

`write_aggregated_report` (T03.11) is unchanged — it remains the
function-call API for callers that want only markdown + JSON +
optional JUnit. The class adds the YAML artefact on top.

## Pattern-reference fidelity

The sprint executor reference (`cli/sprint/executor.py:190-335`)
shows `AggregatedPhaseReport` with these shape properties the cliEval
Reporter mirrors:

| Property                              | sprint `AggregatedPhaseReport`           | cliEval `Reporter`                          |
|---------------------------------------|------------------------------------------|---------------------------------------------|
| `@dataclass`                          | yes                                      | yes (`frozen=True`)                         |
| Wraps an aggregate record             | per-task fields + list of `TaskResult`   | `RunSummary` (DM-004)                       |
| `to_yaml` method                      | yes                                      | yes                                         |
| `to_markdown` method                  | yes                                      | yes                                         |
| YAML block style                      | hand-rolled string concat                | `yaml.safe_dump(default_flow_style=False)`  |
| Status / exit recommendation property | yes                                      | not needed (Reporter does not own exit code)|

The cliEval reporter does *not* own status/exit-code logic — that
remains in the orchestrator + signal handler (T03.07) and exits are
driven by `EvalOutcome` aggregates. The Reporter is strictly a
render-and-write surface.

## Files touched

* New: `src/superclaude/cli/eval/reporter.py` (Reporter class + YAML
  renderer + AggregatedRunReport alias).
* Updated: `src/superclaude/cli/eval/__init__.py` (re-exports
  `Reporter`, `AggregatedRunReport`, `render_summary_yaml`).
* New: `tests/cli/eval/test_reporter.py` (25 tests).
* New: `.dev/releases/current/cliEval/artifacts/D-0055/{spec,notes,evidence}.md`
* New: `.dev/releases/current/cliEval/evidence/T03.13/{SUMMARY.md, test-output.txt, pytest-regression.txt}`
