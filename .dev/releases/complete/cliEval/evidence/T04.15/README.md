# T04.15 — Evidence (DOC-OQ7 `--junit` flag wiring decision)

**Task tier:** EXEMPT (documentation / ADR closure).
**Verification method per tasklist:** Skip verification.
**Completion date:** 2026-05-20.

## What this directory holds

Per the Phase-4 tasklist convention, each task's `evidence/T04.x/` directory accumulates the
linkable artefacts that prove the acceptance criteria are met. T04.15 is an EXEMPT-tier
documentation task — the binding artefact is the decision record itself in `decisions.md`.

## Acceptance-criteria evidence

| Criterion | Evidence |
|---|---|
| decisions.md contains a DOC-OQ7 entry recording the decision | `../../decisions.md` § "DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)" |
| If wired, `superclaude eval run --junit` produces `junit.xml` | `src/superclaude/cli/eval/commands.py:1593` (`Reporter(... emit_junit=junit).write(...)`) → `reporter.py:222-225` (writes `out / "junit.xml"` when gated). |
| If removed, spec §9 no longer references `--junit` | N/A — option A (wire) was chosen. |
| `artifacts/D-0076/spec.md` records the rationale | `../../artifacts/D-0076/spec.md` |

## Implementation evidence (grep snapshot, 2026-05-20)

```
src/superclaude/cli/eval/commands.py:1349:    "--junit",
src/superclaude/cli/eval/commands.py:1350:    "junit",
src/superclaude/cli/eval/commands.py:1352:    help="Also write a JUnit XML report (``junit.xml``) into ``output_dir``.",
src/superclaude/cli/eval/commands.py:1366:    junit: bool,
src/superclaude/cli/eval/commands.py:1593:    Reporter(summary=summary, emit_junit=junit).write(resolved_output)
src/superclaude/cli/eval/reporter.py:146:    emit_junit: bool = False
src/superclaude/cli/eval/reporter.py:177:    def to_junit(self) -> str:
src/superclaude/cli/eval/reporter.py:222:        if self.emit_junit:
src/superclaude/cli/eval/reporter.py:223:            junit_path = out / "junit.xml"
src/superclaude/cli/eval/reporter.py:224:            junit_path.write_text(self.to_junit(), encoding="utf-8")
src/superclaude/cli/eval/reporter.py:225:            written["junit.xml"] = junit_path
```

## Decision summary

**Resolution:** Option A — wire `--junit` into FR-CLI1.
**Rationale (short):** Implementation already on option A; option B requires deleting working
code + amending three documents for net-zero capability change. JUnit XML is the dominant CI
ingestion format. Feature-gated so default runtime cost is zero.
**Source-of-truth:** `decisions.md` § "DOC-OQ7 Closure — `--junit` flag wiring decision (T04.15)".
