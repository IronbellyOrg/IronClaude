# D-0076 — Evidence index (T04.15)

## Tier verification

`Tier: EXEMPT` → Verification Method: Skip verification. Per phase-4-tasklist row T04.15, no
test run is required; the deliverable is the decision-record itself in `decisions.md`.

## Linkable artifacts produced

| Artifact | Path | Purpose |
|---|---|---|
| Decision record | `.dev/releases/current/cliEval/decisions.md` § "DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)" | Canonical decision body. |
| Spec §4 flag table update | `.dev/releases/current/cliEval/design-spec.md:200` (new `--junit` row) | Closes spec-vs-implementation drift. |
| Artifact spec | `.dev/releases/current/cliEval/artifacts/D-0076/spec.md` | This deliverable's rationale + site map. |
| Artifact notes | `.dev/releases/current/cliEval/artifacts/D-0076/notes.md` | Investigation + scope. |
| Artifact evidence | `.dev/releases/current/cliEval/artifacts/D-0076/evidence.md` | This file (evidence index). |
| Evidence directory | `.dev/releases/current/cliEval/evidence/T04.15/` | T04.15-scoped evidence artefacts. |

## Implementation site cross-reference (verified at task time)

| Site | File:line | Purpose |
|---|---|---|
| `--junit` Click option | `src/superclaude/cli/eval/commands.py:1349-1352` | Flag declared, default `false`. |
| `--junit` binding | `src/superclaude/cli/eval/commands.py:1366,1593` | Passed into `Reporter(emit_junit=...)`. |
| Reporter feature gate | `src/superclaude/cli/eval/reporter.py:140-146` | `emit_junit: bool = False`. |
| `to_junit()` renderer | `src/superclaude/cli/eval/reporter.py:177-186` | Renders JUnit XML payload. |
| `write()` gate | `src/superclaude/cli/eval/reporter.py:222-225` | Writes `junit.xml` only when gated. |

These references were verified at task completion (2026-05-20) via `grep -n "junit"` over the
two source files; if a future refactor relocates the symbols, this evidence file should be
re-checked against the new line numbers.

## Acceptance-criteria → site map

| Criterion (T04.15) | Site |
|---|---|
| decisions.md contains a DOC-OQ7 entry | `decisions.md` § "DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)" |
| `superclaude eval run --junit` produces `junit.xml` (if wired) | `commands.py:1593` + `reporter.py:222-225` |
| Spec §9 no longer references `--junit` (if removed) | N/A — option B not selected |
| `artifacts/D-0076/spec.md` records the rationale | `artifacts/D-0076/spec.md` |
