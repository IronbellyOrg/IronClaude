# CLI-Portify Executor No-Op Bug — Forensic Root-Cause Report

**Date**: 2026-03-17
**Produced by**: 6-agent parallel forensic investigation + manual validation
**Status**: Validated findings — ready for remediation planning
**Scope**: Bug origin tracing, spec/roadmap/tasklist pipeline failure analysis, systemic mitigation

---

## Table of Contents

1. [Bug Description](#1-bug-description)
2. [User Command Validation](#2-user-command-validation)
3. [Origin Timeline](#3-origin-timeline)
4. [Spec-Implementation Divergence](#4-spec-implementation-divergence)
5. [Fidelity Chain Failure Analysis](#5-fidelity-chain-failure-analysis)
6. [Tasklist Forensics](#6-tasklist-forensics)
7. [Pipeline Gate Audit](#7-pipeline-gate-audit)
8. [Unified Audit Gating v1.2.1 Evaluation](#8-unified-audit-gating-v121-evaluation)
9. [Validated Root Causes](#9-validated-root-causes)
10. [Recommended Mitigations](#10-recommended-mitigations)
11. [Key File References](#11-key-file-references)
12. [Appendix A: Mock Test Analysis](#appendix-a-mock-test-analysis--why-mocks-were-specified-and-where-that-went-wrong)
13. [Appendix B: v2.24.1 Release Findings](#appendix-b-v2241-release--full-findings)
14. [Appendix C: Fidelity Gate Technical Details](#appendix-c-fidelity-gate-technical-details)

---

## 1. Bug Description

Two defects prevent `superclaude cli-portify run` from performing any real work:

### Defect 1: No-Op Executor Default (Critical)

`PortifyExecutor._execute_step()` at `executor.py:393-415` has a no-op fallback:

```python
def _execute_step(self, step: PortifyStep) -> PortifyStatus:
    if self._step_runner is not None:
        exit_code, stdout, timed_out = self._step_runner(step)
    else:
        # Default: no-op (real subprocess invocation belongs in process.py)
        exit_code, stdout, timed_out = 0, "", False
```

`run_portify()` at `executor.py:1395-1401` constructs `PortifyExecutor` **without passing `step_runner`**:

```python
executor = PortifyExecutor(
    steps=steps,
    workdir=workdir,
    dry_run=config.dry_run,
    resume_from=getattr(config, "resume_from", "") or "",
    turn_budget=config.max_turns,
)
# step_runner is NEVER provided
return executor.run()
```

**Effect**: Every step returns `(exit_code=0, stdout="", timed_out=False)`. The pipeline races through all 12 steps in milliseconds, writes `return-contract.yaml` showing `outcome: SUCCESS` with all steps "completed", and exits. No real work is performed.

Real step implementations exist in `src/superclaude/cli/cli_portify/steps/` (8 modules: `validate_config.py`, `discover_components.py`, `analyze_workflow.py`, `design_pipeline.py`, `synthesize_spec.py`, `brainstorm_gaps.py`, `panel_review.py`, `gates.py`) and as standalone functions in `executor.py` itself (e.g., `execute_protocol_mapping_step()` at line 494). **None are ever called.**

### Defect 2: Missing Config Validation (High)

`commands.py:run()` at lines 95-109 calls `load_portify_config()` then immediately calls `run_portify(config)`. It **never calls `validate_portify_config()`**.

The `load_portify_config()` docstring explicitly warns: `"Does NOT validate — call validate_portify_config() separately."` The validation function exists at `config.py:125` but is never invoked from either `commands.py` or `cli.py`.

**Effect**: Invalid workflow paths (nonexistent directories, missing `SKILL.md`) are silently accepted. Combined with Defect 1, the pipeline silently "succeeds" against nonexistent inputs.

### Observed Behavior

Running:
```bash
superclaude cli-portify run sc-tasklist --output .dev/releases/backlog/portify-tasklist --name tasklist
```

Produces only `return-contract.yaml`:
```yaml
completed_steps:
- validate-config
- discover-components
- protocol-mapping
- analysis-synthesis
- user-review-p1
- step-graph-design
- models-gates-design
- prompts-executor-design
- pipeline-spec-assembly
- user-review-p2
- release-spec-synthesis
- panel-review
outcome: SUCCESS
remaining_steps: []
resume_command: ''
suggested_resume_budget: 0
```

**User command was verified as correct.** The TARGET, `--output`, and `--name` flags are all used properly per the CLI interface. The bug is entirely in the code.

---

## 2. User Command Validation

The command `superclaude cli-portify run sc-tasklist --output <path> --name tasklist` was verified against:

- `commands.py` Click interface: `@click.argument("workflow", metavar="WORKFLOW")` accepts the target
- `--output` maps to `output_dir` parameter (line 39)
- `--name` maps to `name` parameter (line 36)
- No required flags are missing

The `sc-tasklist` target resolves to `Path("sc-tasklist").resolve()` which becomes `/config/workspace/IronClaude/sc-tasklist` (nonexistent). The actual skill directory is `src/superclaude/skills/sc-tasklist-protocol/`. However, this resolution failure is a **consequence of Defect 2** (missing validation), not a user error. The CLI accepts bare skill names per its documented interface.

---

## 3. Origin Timeline

Established via `git log` analysis across all branches:

| Date | Commit | What Happened |
|------|--------|---------------|
| 2026-03-14 | `c39fa91` | **Steps created first** — `steps/analyze_workflow.py` and other step modules built as part of v2.24.1 |
| 2026-03-15 | `2c6e59b` | **Executor scaffolding created** — `executor.py` introduced with the no-op default from line 1 of its existence. Session errored at Phase 3. Comment reads: `"real subprocess invocation belongs in process.py"` |
| 2026-03-16 | `c4fa7f4` | **v2.25 marked "complete"** — `run_portify()`, `STEP_REGISTRY`, `commands.py` added. More step functions added inside `executor.py` itself. **Wiring between executor and step implementations was never attempted.** |

**Key findings:**
- The no-op was a **development placeholder** that became the production behavior
- Steps were created **before** the executor (day before)
- No commit ever wired them together — there is no revert, no deleted dispatch code
- Two parallel development tracks (executor skeleton vs step implementations) were built independently and never joined

---

## 4. Spec-Implementation Divergence

### What the Specs Defined (Correct Design)

All three release specs (v2.24, v2.24.1, v2.25) specified the same correct architecture:

**v2.24 spec** (Appendix D, lines 1444-1652):
- Three-way dispatch: `_run_programmatic_step()`, `_run_claude_step()`, `_run_convergence_step()`
- `PROGRAMMATIC_RUNNERS` dictionary mapping step IDs to real Python functions
- Module dependency graph: `executor.py ──> steps/validate_config.py`, `executor.py ──> steps/discover_components.py`, etc.

**v2.25 spec** (Section 6, "Executor Design"):
- Identical three-way dispatch with explicit pseudocode:
```python
if step.is_programmatic:
    step_result = _run_programmatic_step(step, config)
elif step.phase_type == PortifyPhaseType.USER_REVIEW:
    step_result = _run_review_gate(step, config, result)
else:
    step_result = _run_claude_step(step, config, handler, monitor, tui, ledger)
```
- Integration test `test_programmatic_step_routing`: "Programmatic steps call Python functions, not Claude subprocesses"

### What the Implementation Did (Diverged)

The implementation replaced the spec's direct dispatch model with a `step_runner` callback injection pattern. The `step_runner` parameter was intended for testing (docstring: "Used for testing; real runs use subprocess"). The production code path — when `step_runner is None` — was left as a no-op placeholder.

The `STEP_REGISTRY` was implemented as a **metadata-only** dictionary (step IDs, timeouts, phase types, retry limits) with **no function references**. It provides step configuration, not step dispatch.

### The Divergence Was Never Detected

The spec's three-way dispatch, `PROGRAMMATIC_RUNNERS`, module dependency graph, and `test_programmatic_step_routing` integration test were all specified but:
- Not captured in the roadmap
- Not decomposed into tasklist tasks
- Not implemented in the code
- Not caught by any gate

---

## 5. Fidelity Chain Failure Analysis

### The Transitive Trust Chain Strategy

The pipeline uses a layered fidelity model:
```
Spec ──[SPEC_FIDELITY_GATE]──> Roadmap ──[TASKLIST_FIDELITY_GATE]──> Tasklist ──[???]──> Code
```

Each layer validates only against its immediate parent. If every link is trustworthy, the chain is trustworthy. This strategy is **architecturally sound** but failed in practice because **Link 1 dropped the critical requirement**.

### Link 1: Spec → Roadmap — FAILED

| Spec Requirement | Present in Roadmap? |
|-----------------|-------------------|
| Three-way dispatch (`_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step`) | **NO** — roadmap says only "sequential execution" |
| `PROGRAMMATIC_RUNNERS` dictionary | **NO** — zero mentions |
| `executor.py ──> steps/*.py` import chain | **NO** — not mentioned |
| `test_programmatic_step_routing` integration test | **NO** — not in any roadmap phase |
| "mocked steps" vs real dispatch | Roadmap explicitly says "mocked steps" at Milestone M2 |

The roadmap Phase 2, Key Action 4 reduced the spec's executor design to:
> "Implement executor: sequential execution only, `--dry-run`, `--resume <step-id>`, signal handling"

And Milestone M2:
> "Sequential pipeline runs end-to-end with **mocked steps**"

The `SPEC_FIDELITY_GATE` either did not catch this or classified it as non-blocking.

### Link 2: Roadmap → Tasklist — PASSED (Vacuously)

The tasklist faithfully reproduced the roadmap's already-incomplete executor description:

- **Roadmap**: "sequential execution with mocked steps"
- **Tasklist T03.04 Step 4**: "Sequential loop: iterate STEP_REGISTRY; execute each step"
- **Tasklist Checkpoint**: "Sequential executor core runnable with mocked steps"

The tasklist was faithful to its parent. But its parent was already missing the critical requirement. The corruption propagated cleanly.

### Link 3: Tasklist → Code — DOES NOT EXIST

No programmatic gate verifies that code output satisfies tasklist acceptance criteria. The sprint runner checks:
- Claude subprocess exit code (0 = pass)
- Upstream fidelity status propagation (spec→roadmap only)
- Prompt-level instructions to the agent (advisory, not enforced)

Even if Link 3 existed, the tasklist didn't require dispatch wiring, so the code's no-op would have satisfied the tasklist's acceptance criteria.

### Where the Fidelity Gate Infrastructure Exists

| Gate | Location | What It Checks | Blocking? |
|------|----------|---------------|-----------|
| `SPEC_FIDELITY_GATE` | `roadmap/gates.py:633-656` | LLM-generated severity report; Python enforces `high_severity_count == 0` in YAML frontmatter | Yes |
| `TASKLIST_FIDELITY_GATE` | `tasklist/gates.py:20-43` | LLM-generated severity report; Python enforces `high_severity_count == 0` in YAML frontmatter | Yes |
| Code fidelity gate | Does not exist | N/A | N/A |

**Critical weakness in Links 1-2**: The Python gates validate the **report's metadata** (frontmatter severity counts), not the actual spec-to-roadmap or roadmap-to-tasklist comparison. The semantic comparison is entirely LLM-generated. If the LLM misses a deviation or mis-classifies severity, the gate passes. There are **no programmatic cross-reference checks** (e.g., parsing `FR-NNN` IDs from spec and verifying each appears in roadmap).

---

## 6. Tasklist Forensics

**31 tasklist files** were searched across v2.24 (10 files), v2.24.1 (7 files), and v2.25 (14 files).

### Search Results

| Search Term | v2.24 | v2.24.1 | v2.25 |
|------------|-------|---------|-------|
| `step_runner` | Not found | Not found | Not found |
| `dispatch` (executor context) | Not found | Not found | Not found |
| `PROGRAMMATIC_RUNNERS` | Not found | Not found | Not found |
| `run_portify` wiring | Not found | Not found | T10.01 mentions it but only says "Command body calls `run_portify(config)`" — no dispatch requirement |
| `STEP_REGISTRY` | Not found | Not found | T03.03 — but registry is metadata-only (step_id, phase_type, timeout_s, retry_limit), no function references |
| E2E smoke test | Partial (mocked) | Partial (mocked) | T11.05 defines 5 sample runs but acceptance criteria check outcomes only, not artifact content |
| Step wiring task | **Not found** | **Not found** | **Not found** |

### The Gap

Two parallel development tracks existed across all three releases:

1. **Track A: Executor infrastructure** — `PortifyExecutor` class, `STEP_REGISTRY` (metadata), `run()` loop, signal handling, resume logic, `run_portify()` entry point
2. **Track B: Step implementations** — `steps/validate_config.py`, `steps/analyze_workflow.py`, etc., plus standalone `execute_*` functions in `executor.py`

**No tasklist in any release contained a task to connect Track A to Track B.**

The closest was T03.04 Step 4: "execute each step" — but this was implemented as the no-op default, and acceptance criteria only verified sequential flow, resume, and interrupt behavior, not that steps performed actual work.

---

## 7. Pipeline Gate Audit

### Gates That Exist Today

The pipeline has a mature gate infrastructure — all operating on **document content validation**:

| Gate System | Location | What It Validates |
|-------------|----------|-------------------|
| Pipeline gates (EXEMPT/LIGHT/STANDARD/STRICT) | `pipeline/gates.py` | File existence, min lines, YAML frontmatter fields, semantic check functions |
| Roadmap gates (12 named) | `roadmap/gates.py` | EXTRACT, GENERATE, DIFF, DEBATE, SCORE, MERGE, TEST_STRATEGY, SPEC_FIDELITY, DEVIATION_ANALYSIS, REMEDIATE, CERTIFY |
| Tasklist gates | `tasklist/gates.py` | TASKLIST_FIDELITY_GATE: severity counts, tasklist_ready consistency |
| CLI-Portify gates (G-000 through G-011) | `cli_portify/gates.py`, `steps/gates.py` | Per-step artifact checks: section headers, frontmatter, EXIT_RECOMMENDATION markers |
| Trailing gates | `pipeline/trailing_gate.py` | Async gate evaluation with deferred remediation, retry-once semantics |
| Dead code detection | `audit/dead_code.py` | Cross-boundary dead code candidates using 3-tier dependency graphs |

### The Systemic Blind Spot

**Every gate follows the signature `(content: str) -> bool` or `(output_file: Path, criteria) -> tuple[bool, str|None]`.** They validate that generated documents have correct structure.

**No gate anywhere asks: "Does the code connect its components?"**

The pipeline treats everything as a document generation problem. But cli-portify generates code, and code requires wiring that document-level gates cannot verify.

### Gates That SHOULD Have Caught This

| Missing Gate | What It Would Detect |
|-------------|---------------------|
| Constructor Parameter Coverage | `step_runner=None` defaults to no-op → FAIL unless explicitly provided |
| Step Implementation Reachability | Every `STEP_REGISTRY` entry must have an import path to a corresponding step function |
| No-Op Fallback Detection | Code paths where a callable defaults to no-op and returns success |
| Cross-Module Wiring Verification | After tasklist generation, verify integration tasks exist for all injectable dependencies |
| Smoke Test Gate | Run `run_portify()` with minimal config, assert at least one step implementation fires |

### Deviation Analysis Already Found This Pattern

Delta 2.2 and Delta 2.6 in the `unified-audit-gating-v1.2.1/delta-analysis-post-v2.26.md` document the exact same pattern:

- **D2.2**: `DEVIATION_ANALYSIS_GATE` is fully defined in `roadmap/gates.py:712-758` but `_build_steps()` does not include a `deviation-analysis` step. **Gate exists, wiring doesn't.**
- **D2.6**: Trailing gate framework exists in `pipeline/trailing_gate.py` but sprint's `execute_sprint()` never calls it. `SprintGatePolicy` exists as a stub but is unwired.

The audit gate team identified "defined but not wired" as a recurring pattern but **did not create a gate to detect it programmatically**.

---

## 8. Unified Audit Gating v1.2.1 Evaluation

The backlog spec at `.dev/releases/backlog/unified-audit-gating-v1.2.1/` was evaluated for its likelihood of catching this bug class.

### Score: 4/10 (as currently specified)

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Would catch missing artifacts from a no-op pipeline | 7/10 | Task gate validates artifact existence at STRICT tier |
| Would catch spec-vs-code divergence | 2/10 | Gates check document schema, not code fidelity to spec |
| Would block release via gated E2E tests | 5/10 | Tests might still pass with mocked steps |
| Would detect silent success / no-op fallback | 1/10 | Pipeline returns SUCCESS; gate sees successful outcome and approves |
| **Weighted total** | **4/10** | |

### Why Not Higher

The audit gate validates **workflow state transitions** (task → audit → pass → complete) with **artifact-level validation** (existence, schema, drift). The cli-portify bug produces a pipeline that *appears* to succeed — all steps "complete", `return-contract.yaml` shows SUCCESS. The gate system validates process, not product wiring.

### What Would Make It 8+/10

1. **Code-fidelity gate**: Compare spec dispatch tables against actual code imports and call paths
2. **No-op detection gate**: Flag production code paths where `None`-defaulting callables return success stubs
3. **Artifact content validation**: Check output artifacts contain real content, not just that files exist
4. **Smoke test gate at release tier**: Run the pipeline against a test input and verify real artifacts are produced

### With Link 3 (Tasklist → Code fidelity gate) Implemented

| Scenario | Score |
|----------|-------|
| Audit gating v1.2.1 as currently specified | 4/10 |
| With Link 3 (task gate blocks completion unless code satisfies acceptance criteria) | 8/10 |
| Full chain with deterministic ID cross-refs at Links 1-2 plus Link 3 | 9/10 |

---

## 9. Validated Root Causes

### Primary: Spec-to-Roadmap Fidelity Failure

The spec's three-way dispatch design was dropped during roadmap generation. The `SPEC_FIDELITY_GATE` (LLM-dependent semantic comparison) did not catch or did not escalate this as a HIGH severity deviation. The roadmap reduced the executor to "sequential execution with mocked steps" and the corruption propagated through the tasklist into the code.

### Secondary: No-Op Placeholder in Production Code Path

The `_execute_step()` no-op was a development placeholder introduced in commit `2c6e59b` during a session that "errored at Phase 3." It was never replaced because no task, gate, or test required real dispatch. The comment `"real subprocess invocation belongs in process.py"` documents an intention that was never tasked.

### Tertiary: Integration/E2E Tests Specified But Never Executed

The v2.25 spec defined `test_programmatic_step_routing` and E2E sample runs. These were either never written or never run against the production `run_portify()` path. The tests that exist use mocked steps and check outcome classifications, not real execution output.

### Systemic: Gate Infrastructure Validates Documents, Not Code Integration

The entire gate system operates on document content (frontmatter fields, section headings, severity counts). No gate verifies that code components are connected to their consumers. The "defined but not wired" pattern recurs across multiple systems (DEVIATION_ANALYSIS_GATE, trailing gate, SprintGatePolicy) and has been observed but never gated against.

### Systemic: Link 3 (Tasklist → Code) Does Not Exist

The transitive fidelity chain (Spec → Roadmap → Tasklist → Code) is broken at its final link. No programmatic gate verifies that code satisfies tasklist acceptance criteria. The unified-audit-gating v1.2.1 spec identifies this as a requirement but implementation is in backlog.

---

## 10. Recommended Mitigations

### Immediate Fixes (Bug Resolution)

#### Fix 1: Wire `run_portify()` to Step Dispatch

Create a step dispatch map that routes each `step_id` to the corresponding step implementation:

```python
from .steps.validate_config import run_validate_config
from .steps.discover_components import run_discover_components
from .steps.analyze_workflow import run_analyze_workflow
# ... etc

STEP_DISPATCH = {
    "validate-config": run_validate_config,
    "discover-components": run_discover_components,
    "analyze-workflow": run_analyze_workflow,
    # ...
}

def _real_step_runner(step):
    fn = STEP_DISPATCH.get(step.step_id)
    if fn is None:
        raise PortifyValidationError(f"No implementation for step: {step.step_id}")
    return fn(config)
```

Pass this to `PortifyExecutor`:

```python
executor = PortifyExecutor(
    steps=steps,
    workdir=workdir,
    step_runner=_real_step_runner,
    ...
)
```

#### Fix 2: Add Validation Call in `commands.py`

```python
config = load_portify_config(...)
errors = validate_portify_config(config)
if errors:
    for e in errors:
        click.echo(e, err=True)
    sys.exit(1)
run_portify(config)
```

### Pipeline Process Mitigations (Systemic)

#### Mitigation 1: Strengthen SPEC_FIDELITY_GATE with Programmatic Cross-References

Add deterministic checks alongside the LLM-generated report:
- Parse all `FR-NNN`, `NFR-NNN`, `SC-NNN` identifiers from the spec extraction
- Verify each appears in the roadmap body text
- Flag missing identifiers as HIGH severity regardless of LLM classification

#### Mitigation 2: Strengthen TASKLIST_FIDELITY_GATE with Deliverable ID Cross-References

- Parse all `D-NNNN` and `R-NNN` identifiers from the roadmap
- Verify each has a corresponding task in the tasklist files
- Flag missing deliverables as HIGH severity

#### Mitigation 3: Implement Link 3 (Code Fidelity Gate)

Prioritize the unified-audit-gating v1.2.1 task-level gate. At minimum:
- Task completion blocked unless acceptance criteria are verified
- Acceptance criteria verification goes beyond exit code (check artifact content, run specified tests)

#### Mitigation 4: Add "Wiring Verification" Gate Category

New gate type that detects:
- `STEP_REGISTRY` entries without corresponding importable step functions
- Constructor parameters with `Optional[Callable]` type that default to `None` and are never explicitly provided in production code paths
- Functions/classes defined in `steps/` that are never imported by the executor
- No-op fallbacks that return success codes (`0`, `True`, `PASS`)

#### Mitigation 5: Add Smoke Test Gate at Release Tier

Before any release can be marked complete:
- Run the actual CLI command against a minimal test fixture
- Verify that output artifacts contain real content (not just `return-contract.yaml`)
- Verify that at least N step implementations were actually invoked

---

## 11. Key File References

### Bug Locations

| File | Lines | What |
|------|-------|------|
| `src/superclaude/cli/cli_portify/executor.py` | 393-415 | `_execute_step()` no-op default |
| `src/superclaude/cli/cli_portify/executor.py` | 1367-1402 | `run_portify()` missing `step_runner` |
| `src/superclaude/cli/cli_portify/commands.py` | 95-109 | `run()` missing `validate_portify_config()` call |
| `src/superclaude/cli/cli_portify/config.py` | 63 | Docstring: "Does NOT validate" |
| `src/superclaude/cli/cli_portify/config.py` | 125 | `validate_portify_config()` — exists but never called |

### Orphaned Step Implementations (Never Called)

| File | Function |
|------|----------|
| `src/superclaude/cli/cli_portify/steps/validate_config.py` | `run_validate_config()` |
| `src/superclaude/cli/cli_portify/steps/discover_components.py` | `run_discover_components()` |
| `src/superclaude/cli/cli_portify/steps/analyze_workflow.py` | `run_analyze_workflow()` |
| `src/superclaude/cli/cli_portify/steps/design_pipeline.py` | `run_design_pipeline()` |
| `src/superclaude/cli/cli_portify/steps/synthesize_spec.py` | `run_synthesize_spec()` |
| `src/superclaude/cli/cli_portify/steps/brainstorm_gaps.py` | `run_brainstorm_gaps()` |
| `src/superclaude/cli/cli_portify/steps/panel_review.py` | `run_panel_review()` |
| `src/superclaude/cli/cli_portify/executor.py:494` | `execute_protocol_mapping_step()` |
| `src/superclaude/cli/cli_portify/executor.py:549` | `execute_analysis_synthesis_step()` (approx) |

### Release Artifacts Examined

| Release | Path |
|---------|------|
| v2.24 (cli-portify-cli-v4) | `.dev/releases/complete/v2.24-cli-portify-cli-v4/` |
| v2.24.1 (cli-portify-cli-v5) | `.dev/releases/complete/v2.24.1-cli-portify-cli-v5/` |
| v2.25 (cli-portify-cli) | `.dev/releases/complete/v2.25-cli-portify-cli/` |
| Cross-framework analysis | `.dev/releases/complete/cross-framework-deep-analysis/v2.25-cli-portify-cli/` |
| Audit gating spec | `.dev/releases/backlog/unified-audit-gating-v1.2.1/` |

### Gate Infrastructure

| Gate | Location |
|------|----------|
| `SPEC_FIDELITY_GATE` | `src/superclaude/cli/roadmap/gates.py:633-656` |
| Spec fidelity prompt | `src/superclaude/cli/roadmap/prompts.py:278-347` |
| `TASKLIST_FIDELITY_GATE` | `src/superclaude/cli/tasklist/gates.py:20-43` |
| Tasklist fidelity prompt | `src/superclaude/cli/tasklist/prompts.py:17-107` |
| Pipeline gate enforcer | `src/superclaude/cli/pipeline/gates.py:20-69` |
| CLI-Portify gates (G-000 to G-011) | `src/superclaude/cli/cli_portify/gates.py` |
| Dead code detection | `src/superclaude/cli/audit/dead_code.py` |
| Trailing gate infrastructure | `src/superclaude/cli/pipeline/trailing_gate.py` |

### Git Commits

| Commit | Date | Significance |
|--------|------|-------------|
| `c39fa91` | 2026-03-14 | Steps created (v2.24.1) |
| `2c6e59b` | 2026-03-15 | Executor created with no-op default |
| `c4fa7f4` | 2026-03-16 | v2.25 "complete" — `run_portify()` added, wiring never attempted |

---

## Appendix A: Mock Test Analysis — Why Mocks Were Specified and Where That Went Wrong

### What Mock Tests Legitimately Validate

Mock tests are correct for testing **orchestration mechanics in isolation**:

- Does the loop iterate steps in `STEP_REGISTRY` order?
- Does `--resume` skip completed steps?
- Does `SIGINT` produce `INTERRUPTED` outcome?
- Does budget exhaustion produce `HALTED`?
- Does `return-contract.yaml` emit on all code paths?

These are **container tests** — testing the executor loop, not the step implementations. Mocking steps makes sense here because the executor's job is sequencing, not step content.

### Why the Agent Specified Mock-Only Testing

The "mocked steps" language **did not come from the pipeline prompts**. All pipeline prompt code was searched:

| Prompt Source | Contains "mock" instructions? |
|---------------|------------------------------|
| `roadmap/prompts.py` — `build_generate_prompt()` | No |
| `roadmap/prompts.py` — `build_test_strategy_prompt()` | No — actually asks for ALL test categories (unit, integration, E2E, acceptance) |
| `tasklist/prompts.py` — `build_tasklist_fidelity_prompt()` | No |
| `sc-roadmap-protocol/SKILL.md` | No |
| `sc-tasklist-protocol/SKILL.md` | No |

The "mocked steps" framing **originated in the roadmap output itself** — it was a design decision made by the LLM agent generating the roadmap. The agent decomposed the executor work into Phase 2 with milestone: *"Sequential pipeline runs end-to-end with mocked steps."*

This is a **reasonable Phase 2 waypoint** — you build the skeleton first, then fill it in. The failure was that the agent **never created a companion milestone in a later phase** for real dispatch wiring and integration testing. The mock-test milestone became the terminal validation because "elsewhere/later" was never specified.

### The Propagation Chain

1. **Spec** said: three-way dispatch with `PROGRAMMATIC_RUNNERS` + `test_programmatic_step_routing` integration test
2. **Roadmap agent** produced milestone: "mocked steps" (reasonable Phase 2 waypoint) — but dropped the spec's dispatch design and integration test from all subsequent phases
3. **SPEC_FIDELITY_GATE** either didn't notice or didn't classify the dropped dispatch design as HIGH severity
4. **Tasklist agent** faithfully reproduced "mocked steps" into T03.04 acceptance criteria
5. **Sprint agent** faithfully built an executor with mocked step tests that pass — exactly what the tasklist asked for

Each agent was faithful to its parent. The corruption entered at step 2 and was not caught at step 3.

### The Cognitive Trap

"Mocked steps" as a milestone implies real dispatch is handled elsewhere/later. But "elsewhere/later" was never specified. The mock test became the definition of done because no subsequent milestone said "now do it for real." This is a **specification completeness failure**, not a testing methodology failure.

### Mitigation

The roadmap generation prompt should be augmented with an instruction like:

> "For any phase that introduces a skeleton, scaffold, or mock-based milestone, you MUST include a subsequent phase milestone that replaces mocks with real implementations and validates end-to-end behavior with actual component execution."

This prevents the "build skeleton with mocks" → "never fill it in" pattern.

---

## Appendix B: v2.24.1 Release — Full Findings

v2.24.1 focused exclusively on three design gaps: input target resolution (6 input forms), component tree discovery, and subprocess scoping (`PortifyProcess.additional_dirs`). It added **zero changes to executor dispatch wiring**. The executor was not listed as a modified file in any specification document. The roadmap module dependency graph omitted `executor.py` entirely. All 18 acceptance criteria were scoped to resolution, tree building, and subprocess scoping. The release inherited an unexamined assumption that the executor already works and spent its entire scope on layers that are unreachable because the executor never calls any step.

## Appendix C: Fidelity Gate Technical Details

### How SPEC_FIDELITY_GATE Works

1. **LLM comparison**: `build_spec_fidelity_prompt()` instructs Claude to compare spec vs roadmap across 5 dimensions (signatures, data models, gates, CLI options, NFRs), classify deviations as HIGH/MEDIUM/LOW, and produce YAML frontmatter with severity counts
2. **Deterministic enforcement**: Python checks `high_severity_count == 0` in frontmatter and `tasklist_ready == true` only when counts are zero and validation is complete
3. **Blocking**: Pipeline executor runs gate in BLOCKING mode; failure retries once then halts

### How TASKLIST_FIDELITY_GATE Works

1. **LLM comparison**: `build_tasklist_fidelity_prompt()` instructs Claude to compare roadmap vs tasklist across 5 dimensions (deliverable coverage, signature preservation, traceability ID validity, dependency chain correctness, acceptance criteria completeness)
2. **Validation layering guard**: Prompt explicitly tells LLM to validate roadmap-to-tasklist ONLY, not spec-to-tasklist
3. **Same enforcement**: Reuses `_high_severity_count_zero` and `_tasklist_ready_consistent` semantic checks

### What Neither Gate Does

- No programmatic parsing of requirement IDs from source document
- No cross-reference verification (every FR-NNN in spec → exists in roadmap)
- No enumeration completeness check
- No code integration verification
