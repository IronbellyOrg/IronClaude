# D-0052 — Implementation notes

## Design decisions

### Three dataclasses, not one with nested dicts

DM-004 names `counts` and `totals` as nested sub-structures, and DM-012
formalises both shapes. We model them as their own frozen dataclasses
(`RunCounts`, `RunTotals`) rather than `dict` blobs:

- **Validation locality** — the `kept_plus_skipped_equals_n_prime`
  invariant lives on `RunCounts`, but `RunSummary.__post_init__` is
  where it fires (the counts dataclass itself stays a passive value
  object). This keeps the equation guard at the boundary the orchestrator
  crosses when it builds a `RunSummary`, not inside the sub-record.
- **Reporter ergonomics** — `to_dict()` recurses naturally:
  `payload["counts"] = self.counts.to_dict()`. No manual mapping copies,
  no schema drift between in-memory and serialised shapes.
- **Symmetry with DM-001/DM-003** — `EvalOutcome` and `EvalResult`
  already use the `_FIELDS` constant + ordered-dict pattern. The new
  records inherit the same style so the module stays readable as one
  unit.

### `evals` is `tuple[EvalOutcome, ...]`, not a list

DM-004 lists `evals[]` as a sequence. We use a tuple so:

1. The frozen dataclass keeps equality + hashability (lists do not hash).
2. Mutation is structurally impossible — a downstream consumer cannot
   `.append()` an extra row in the middle of a Reporter render.
3. `to_dict()` emits a JSON-shaped list explicitly (`[item.to_dict()
   for item in value]`), so the wire format matches DM-012 verbatim.

### Equation guard fires in `__post_init__`

The acceptance bullet "RunSummary constructor validates
`counts.kept_plus_skipped_equals_n_prime` boolean and asserts the
equation holds" admits two readings:

1. **Always require the math to add up** — refuse to construct a
   `RunSummary` when `kept_k + skipped_s != expanded_n_prime`.
2. **Require the flag to mirror reality** — refuse to construct a
   `RunSummary` when the flag claims True but the math says False, or
   vice versa.

We chose reading (2). Rationale:

- FR-RPT1 (T03.11) is the canonical gate that raises
  `ReporterContractViolation` (exit 2) on N'-vs-K mismatch. Pushing the
  same guard into the data model would duplicate the policy *and* block
  the orchestrator from ever building a partial summary with mismatched
  counts.
- DM-012 explicitly enumerates `kept_plus_skipped_equals_n_prime` as a
  boolean field on the wire. The flag exists precisely so the Reporter
  can render it; the model job is to keep the flag honest, not to
  short-circuit FR-RPT1.
- Tests `test_run_summary_accepts_consistent_false_flag` pins the
  partial-summary path: a SIGINT-interrupted run that lost 1 of 5
  expanded rows can still serialise (flag = False, math = False) so the
  exit-3 path in NFR-REL1 (T03.07) can flow through the writer before
  FR-RPT1's guard fires downstream.

### No defaults on the head fields

Eight of the eleven fields are required positional arguments
(`run_id`, `started_at`, `finished_at`, `duration_sec`, `suite`,
`manifest_version`, `parallel`, `counts`, `totals`). The orchestrator
builds the summary exactly once at end-of-run; defaults would let a
caller construct a half-populated record and ship it. Only the two
sequence-typed tail fields (`evals`, `artifacts`) have defaults
(`()` and `field(default_factory=dict)`), matching the DM-001 /
DM-003 pattern.

## Cross-references

- **Tests** — `tests/cli/eval/test_run_summary.py` (22 tests, all
  passing).
- **Re-export** — `superclaude.cli.eval.__init__` lists `RunCounts`,
  `RunSummary`, `RunTotals` in both the `from .models import (...)`
  block and `__all__`. Reporter / Orchestrator import from the package
  root.
- **Field-order constants** — `_RUN_SUMMARY_FIELDS`,
  `_RUN_COUNTS_FIELDS`, `_RUN_TOTALS_FIELDS` mirror DM-004 / DM-012
  verbatim so reviewers can `git diff` the order against the spec line
  by line.

## Out-of-scope items (forward references)

- DM-012 `summary.schema.json` — T03.10. The schema will validate the
  exact serialised shape `RunSummary.to_dict()` emits today.
- FR-RPT1 `write_aggregated_report` + `ReporterContractViolation` — T03.11.
- COMP-008 Reporter emitters (`to_markdown` / `to_yaml` / `to_json` /
  `to_junit`) — T03.13.
- COMP-003 RunOrchestrator that builds the `RunSummary` — T03.15.
