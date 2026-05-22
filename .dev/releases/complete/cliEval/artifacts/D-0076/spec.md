# D-0076 — DOC-OQ7 `--junit` flag wiring decision

**Roadmap row:** R-076 (DOC-OQ7) — `cli` slice, dependency on OQ-7.
**Task:** T04.15 (Phase 4 tasklist).
**Tier:** EXEMPT (documentation / ADR closure).
**Decision date:** 2026-05-20.
**Resolution status:** RESOLVED — Option A (wire `--junit`).

## Rationale

See `decisions.md` → "DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)" for the full
options table, rationale, and consequences. This artifact records the decision summary, the
implementation site map, and the spec/code consistency state after closure.

## Decision (summary)

Wire `--junit` into FR-CLI1. The CLI exposes `superclaude eval run --junit`; when set, the
Reporter writes `junit.xml` into the run's output directory in addition to `summary.{md,json}`.
Spec §9 conditional language ("Generated only when `--junit` is passed") stands. Spec §4 flag
table is updated in the same commit to list `--junit` so all three sources of truth (§4 table,
FR-CLI1 row R-072, implementation) agree.

## Implementation site map

| Layer | Site | Purpose |
|---|---|---|
| CLI flag declaration | `src/superclaude/cli/eval/commands.py:1349-1352` | Click `--junit` option; default `false`. |
| CLI flag binding | `src/superclaude/cli/eval/commands.py:1366,1593` | Pass-through to `Reporter(emit_junit=...)`. |
| Reporter constructor | `src/superclaude/cli/eval/reporter.py:140-146` | `emit_junit: bool = False` dataclass field. |
| Reporter renderer | `src/superclaude/cli/eval/reporter.py:177-186` | `to_junit() → str` returns JUnit XML payload. |
| Reporter writer gate | `src/superclaude/cli/eval/reporter.py:222-225` | `if self.emit_junit: write junit.xml`. |
| Spec §4 flag table | `design-spec.md:200` | Updated 2026-05-20 to include `--junit BOOL` row. |
| Spec §9 artifacts | `design-spec.md:591-593` | `junit.xml (optional, for future CI plumbing)` section retained. |
| Spec §10 reuse | `design-spec.md:621` | `to_junit()` reuse from `AggregatedPhaseReport` retained. |

## Acceptance criteria evidence

| Criterion (T04.15) | Status | Evidence |
|---|---|---|
| File `.dev/releases/current/cliEval/decisions.md` contains a DOC-OQ7 entry recording the decision (wire or remove). | ✅ MET | New section "DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)" appended to `decisions.md`. |
| If wired, `superclaude eval run --junit` produces `junit.xml` under the run directory. | ✅ MET | `commands.py:1593` invokes `Reporter(..., emit_junit=junit).write(resolved_output)`; `reporter.py:222-225` writes `junit.xml` to `out / "junit.xml"` when `emit_junit` is True. |
| If removed, spec §9 no longer references `--junit`. | N/A | Option B (removal) was not selected; §9 retains `--junit` reference by design. |
| `TASKLIST_ROOT/artifacts/D-0076/spec.md` records the rationale. | ✅ MET | This file. |

## OPS-001 table update

The OPS-001 Open-Questions table (`decisions.md` §B) listed OQ-7 as `OPEN` as of the OPS-001
closure date. With this decision the row flips to `RESOLVED — 2026-05-20`. The table is not
re-rendered in place; the `DOC-OQ7 Closure` section above is canonical and supersedes the prior
`OPEN` row by date precedence.

## Downstream impact

- T04.10 (FR-CLI1) — already implements the 12-flag set; no further work required.
- T04.13 (FR-G4 artifact layout) — `junit.xml` belongs to the per-run output directory only when
  `emit_junit=True`; absence is not a layout violation.
- T04.17 (TEST-007 reporter contract) — schema-fidelity test exercises `to_json()`; a JUnit-XML
  invariant test may be added later (out of scope for T04.15).
- M5 single-command runnability (T04.11) — `--junit` is opt-in; the smoke test path
  (`uv run superclaude eval run --suite real --eval E1`) does not require it.

## Out of scope for T04.15

- Adding a JUnit-XML schema-conformance test (would belong with TEST-007 or a new TEST row).
- Adding a CI workflow that consumes `junit.xml` (would belong with NFR-OPS or release-engineering).
- Modifying the JUnit XML renderer itself (lives in `reporter.py` and was landed under T03.13).
