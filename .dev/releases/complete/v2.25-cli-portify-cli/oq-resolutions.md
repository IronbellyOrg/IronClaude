# v2.25-cli-portify — Open Question Resolutions
# Pre-determined by cross-release conflict analysis (v2.24.2, v2.24.5, v2.25.5, v2.25.5-pass-no-report-fix)
# Date: 2026-03-16

## OQ-008 — --file subprocess behavior
**Status: CLOSED — resolved by v2.24.5 empirical testing**

`claude --file <path>` does NOT reliably deliver content to the model.
v2.24.5 (SpecFidelity) empirically tested and replaced `--file` with inline embedding
across all executors in `cli/roadmap/` and `cli/tasklist/`.

**Resolution**: Use inline `-p` embedding exclusively. For content exceeding
`_EMBED_SIZE_LIMIT` (120 * 1024 bytes), raise `PortifyValidationError`. Do NOT use `--file`.

**Impact on Phase 6**: Step T07.06 in resume-tasklist.md reflects this amendment.
Original roadmap Phase 6 Action 7 is superseded.

**Reference**: v2.24.5 Phase 1.5 — `fix(executors): replace --file fallback with inline embedding`

---

## OQ-013 — PASS_NO_SIGNAL retry behavior
**Status: CLOSED — confirmed by v2.25.5-pass-no-report-fix analysis**

Distinction confirmed:
- `PASS_NO_SIGNAL` (result file present, no `EXIT_RECOMMENDATION` marker) → DOES trigger retry
- `PASS_NO_REPORT` (artifact produced, no result file at all) → does NOT trigger retry; treated as pass

This is already documented in roadmap.md Phase 3 gate note (line 189).
The sprint executor implementation in `src/superclaude/cli/sprint/executor.py` is the reference.

**Impact**: Gate retry logic in `gates.py` Phase 4 (T04.15) must implement this distinction.

---

## D-008 — Framework base type stability
**Status: CONFIRMED STABLE**

Verified 2026-03-16:
- `from superclaude.cli.pipeline.process import ClaudeProcess` → OK
- `from superclaude.cli.pipeline.models import PipelineConfig, Step, StepResult` → OK
- `from superclaude.cli.pipeline.models import GateCriteria, GateMode, SemanticCheck` → OK

Note: GateCriteria, GateMode, SemanticCheck live in `superclaude.cli.pipeline.models`,
NOT in `superclaude.cli.sprint.models`. Update any imports that assumed sprint.models.

---

## --tools default (FIX-001 from v2.24.5)
**Status: ALREADY INHERITED — no action needed**

`ClaudeProcess.build_command()` in `src/superclaude/cli/pipeline/process.py` line 79-80
already includes `--tools`, `default` in the command list.

`PortifyProcess` in `src/superclaude/cli/cli_portify/process.py` line 187 calls
`super().build_command()` — inherits `--tools default` for free.

No code change required.

---

## PyYAML
**Status: PRESENT — pyyaml 6.0.3 installed**

Added by v2.24.2 (Accept-Spec-Change). Phase 4-5 YAML approval file parsing
(phase1-approval.yaml, phase2-approval.yaml) can use PyYAML directly.

---

## Portify Test State
**Status: EXPECTED ERRORS — modules not yet built**

All 16 test files in `tests/cli_portify/` fail at collection with ModuleNotFoundError.
These tests reference modules to be built in Phases 4–10:
- `contract`, `gates`, `prompts`, `steps.synthesize_spec`, `steps.analyze_workflow`, etc.

This is the expected state after Phase 3 interrupt. Tests are pre-written and will
pass as their corresponding modules are implemented.

Sprint baseline: `tests/sprint/` — 713 passed, 0 failures (verified 2026-03-16).
