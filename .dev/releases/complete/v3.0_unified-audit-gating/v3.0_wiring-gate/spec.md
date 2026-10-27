---
title: Wiring Verification Gate
release: v3.0_wiring-gate
status: draft
date: 2026-03-18
owner: architect
inputs:
  - /config/workspace/IronClaude/docs/generated/audit-wiring-detection-analysis.md
  - /config/workspace/IronClaude/docs/generated/cli-unwired-components-audit.md
  - /config/workspace/IronClaude/docs/generated/gate-system-deep-analysis.md
  - /config/workspace/IronClaude/.dev/releases/current/v3.0_unified-audit-gating/spec-refactor-plan-merged.md
scope: roadmap post-merge wiring-verification gate using existing GateCriteria/SemanticCheck substrate
---

# Wiring Verification Gate

## 1. Problem

The current gate system validates artifact structure and semantic consistency, but it does not validate whether implementation surfaces are actually connected to runtime paths.

The current repository already shows recurring wiring failures:

1. `Optional[Callable] = None` injection seams that are never populated
2. helper modules and gate layers with zero effective consumers
3. registry / dispatch tables whose entries or accessors are never used
4. gate constants and policy layers that are defined but never attached to executable flow

Representative findings already captured in generated analysis:

- `src/superclaude/cli/cli_portify/executor.py` phantom `step_runner` / `process_runner` injection seams
- `src/superclaude/cli/audit/evidence_gate.py` and `manifest_gate.py` orphan gate functions
- `src/superclaude/cli/cli_portify/gates.py` disconnected gate registry layer
- `src/superclaude/cli/sprint/executor.py` dead `SprintGatePolicy`
- `src/superclaude/cli/roadmap/gates.py` unwired `DEVIATION_ANALYSIS_GATE`

This creates a post-merge blind spot: a roadmap pipeline can emit internally consistent artifacts while still encoding disconnected implementation paths.

## 2. Objective

Design a **wiring-verification gate** that:

1. extends the existing `GateCriteria` / `SemanticCheck` / `gate_passed()` substrate
2. does **not** create parallel gate infrastructure
3. detects unwired `Optional[Callable] = None` injections
4. detects orphan modules / symbols with no effective import chain
5. detects unregistered or unreachable dispatch entries
6. reuses cleanup-audit infrastructure, especially `audit-analyzer`, instead of duplicating it
7. supports **shadow → soft → full** rollout
8. integrates into roadmap executor as a **post-merge step in `_build_steps()`**

## 3. Design Constraints

### 3.1 Preserve the existing gate substrate

This release must remain a consumer of the existing pipeline model:

- `src/superclaude/cli/pipeline/models.py:58` — `SemanticCheck`
- `src/superclaude/cli/pipeline/models.py:68` — `GateCriteria`
- `src/superclaude/cli/pipeline/gates.py:20` — `gate_passed()`
- `src/superclaude/cli/roadmap/executor.py:344` — `_build_steps()`

No signature changes to `SemanticCheck` are allowed. Semantic checks remain pure `Callable[[str], bool]` over report content.

### 3.2 Preserve layering

Allowed dependency direction:

- `audit/*` may depend on pipeline types
- `roadmap/*` may import audit helpers and gate constants
- `pipeline/*` must remain domain-agnostic and must not import `roadmap/*` or `audit/*`

### 3.3 Separate analysis from enforcement

The design must keep three layers distinct:

1. **deterministic wiring analysis** over source files
2. **artifact emission** into a markdown report with frontmatter
3. **gate enforcement** using `gate_passed(report_file, WIRING_VERIFICATION_GATE)`

That keeps the new capability compatible with the existing document-first gate architecture.

### 3.4 Extend, don’t duplicate cleanup-audit

The design must reuse existing cleanup-audit evidence and agent roles where possible.

Specifically:

- extend `audit-analyzer` evidence collection rather than creating a new wiring-analysis agent family
- reuse existing audit structural outputs as advisory inputs
- keep the roadmap wiring step authoritative through direct deterministic analysis

## 4. Current Architecture Reality

### 4.1 Existing pipeline model

Today, roadmap `_build_steps()` constructs a static post-merge chain:

1. `extract`
2. `generate-*` parallel pair
3. `diff`
4. `debate`
5. `score`
6. `merge`
7. `test-strategy`
8. `spec-fidelity`

Source: `src/superclaude/cli/roadmap/executor.py:343-475`

A new wiring step should append to this post-merge chain immediately after `spec-fidelity`.

### 4.2 Existing precedent for non-LLM post-merge steps

The repository already contains a design precedent for a post-merge deterministic step: the anti-instinct audit step is modeled as a normal `Step` in `_build_steps()` but handled specially by the executor as a non-LLM operation.

That is the correct pattern for wiring verification as well.

### 4.3 Existing trailing gate capability

Trailing gate infrastructure already exists:

- `TrailingGateRunner`
- `DeferredRemediationLog`
- `GateMode.TRAILING`

Sources:

- `src/superclaude/cli/pipeline/trailing_gate.py:88`
- `src/superclaude/cli/pipeline/trailing_gate.py:489`
- `src/superclaude/cli/pipeline/executor.py:199-214`

Important constraint: `resolve_gate_mode()` forces **release scope** gates to blocking, so rollout semantics for roadmap release validation must be explicit in roadmap wiring-step design rather than assuming generic trailing behavior will always apply automatically.

## 5. Proposed Architecture

## 5.1 New module: `src/superclaude/cli/audit/wiring_gate.py`

This is the core deterministic analysis module.

Responsibilities:

- discover Python files under configured analysis scope
- detect unwired callable injections
- detect orphan modules / symbols
- detect unregistered or unreachable dispatch entries
- optionally ingest cleanup-audit artifacts as advisory evidence
- emit normalized results
- render `wiring-verification.md`
- expose report-validation helpers used by roadmap gates

Suggested public surface:

```python
@dataclass
class WiringFinding: ...

@dataclass
class WiringReport: ...

def run_wiring_analysis(source_root: Path, *, audit_context: AuditContext | None = None) -> WiringReport: ...
def emit_wiring_report(report: WiringReport, output_file: Path) -> None: ...
def build_wiring_report(... ) -> str: ...
```

Notes:

- keep this module deterministic and pure-Python
- do not put `GateCriteria` inside `pipeline/*`
- keep parsing / AST logic here, not in roadmap executor

## 5.2 Roadmap gate definition: `src/superclaude/cli/roadmap/gates.py`

Add a new strict gate constant:

- `WIRING_VERIFICATION_GATE`

The gate validates the emitted report artifact only.

Suggested semantic checks:

- `analysis_complete_true`
- `recognized_rollout_mode`
- `finding_counts_consistent`
- `severity_summary_consistent`
- `zero_blocking_findings_for_mode`

The key rule is mode-aware enforcement:

- **shadow**: report must be structurally valid; findings do not fail the gate
- **soft**: critical findings fail only when above configured threshold / policy
- **full**: any blocking-class finding fails

Because `SemanticCheck` only accepts report content, the rollout decision must be encoded into report frontmatter and interpreted by report semantic checks.

## 5.3 Roadmap executor integration: `src/superclaude/cli/roadmap/executor.py`

Add a new post-merge step in `_build_steps()` immediately after `spec-fidelity`:

```python
Step(
    id="wiring-verification",
    prompt="",  # non-LLM deterministic step
    output_file=out / "wiring-verification.md",
    gate=WIRING_VERIFICATION_GATE,
    timeout_seconds=60,
    inputs=[config.spec_file, merge_file, spec_fidelity_file],
    retry_limit=0,
)
```

This step should be executor-special-cased the same way other deterministic audit-style steps are handled:

- run `run_wiring_analysis(...)`
- write `wiring-verification.md`
- let normal gate handling validate the artifact

### Why `_build_steps()` is the correct insertion point

The codebase has no dynamic gate registry for roadmap execution. Gates are wired statically at `Step` construction time.

So the integration point is not an external registry; it is a new `Step(...)` entry in `_build_steps()`.

## 5.4 Cleanup-audit reuse model

### Reuse principle

Use cleanup-audit as an evidence supplier, not as the enforcement mechanism.

### Direct reuse targets

#### `audit-analyzer`

`audit-analyzer` already produces the mandatory Pass 2 structural profile with these fields:

- What it does
- Nature
- References
- CI/CD usage
- Superseded by / duplicates
- Risk notes
- Recommendation
- Verification notes

This is the right place to extend structural wiring evidence.

Recommended additions to Pass 2 output:

- `wiring_surfaces`
- `registry_symbols`
- `effective_references`
- `dynamic_loading_notes`
- `wiring_assessment`

These can be added as structured subsections or appended evidence, without creating a separate agent type.

#### Existing audit evidence

Advisory reuse sources:

- dependency/reference evidence from audit analysis
- dynamic-loading suppression evidence
- known retention rationale for apparently orphaned files

### Authority rule

Use **hybrid mode**:

- direct deterministic analysis is authoritative
- cleanup-audit artifacts act as false-positive suppressors and evidence enrichment

This avoids coupling correctness to whether cleanup-audit happened to run earlier.

## 6. Detection Design

## 6.1 Detector A — Unwired `Optional[Callable] = None` injections

### Target pattern

A finding is emitted when all are true:

1. parameter annotation includes `Callable`
2. default value is `None`
3. parameter is part of a constructor or function injection seam
4. no non-`None` call site supplies the parameter in analyzed scope
5. no explicit whitelist or dynamic-loading evidence justifies retention

### Initial examples already known

- `audit/spot_check.py:81` — `reclassify_fn`
- `roadmap/executor.py:723` — `halt_fn`
- `cli_portify/executor.py:333` — `step_runner`
- `cli_portify/executor.py:513` and related — `process_runner`

### Severity policy

- **critical**: execution, dispatch, or enforcement behavior depends on the seam
- **major**: seam is dead but local fallback exists
- **info**: seam is intentionally optional and whitelisted

## 6.2 Detector B — Orphan modules / symbols

### Target pattern

A module or symbol is orphaned when it has no effective consumer path after filtering out noise such as self-reference, index-only export, or documented dynamic retention.

### Initial targets

- top-level helpers in `gates.py`
- provider modules in `steps/`, `handlers/`, `validators/`, `checks/`
- gate policy classes and helper modules
- modules whose only references are local or documentary

### Initial examples already known

- `audit/evidence_gate.py:evidence_gate()`
- `audit/manifest_gate.py:check_manifest_completeness()`
- `cli_portify/gates.py:gate_*()` family
- `sprint/executor.py:SprintGatePolicy`
- `roadmap/gates.py:DEVIATION_ANALYSIS_GATE`

### Evidence rule

A symbol is orphaned only if both are true:

1. direct analysis finds no effective import / call chain
2. cleanup-audit evidence does not justify dynamic or deferred use

## 6.3 Detector C — Unregistered / unreachable dispatch entries

### Target pattern

Detect disconnected registries in three classes:

1. **entry unresolved** — mapped target does not resolve
2. **registry unused** — registry or accessor has zero external consumers
3. **entry unreachable** — registry is live, but specific entries are never selected and have no dynamic-use evidence

### Registry heuristics

Match names like:

- `*_REGISTRY`
- `*_DISPATCH`
- `*_HANDLERS`
- `*_ROUTER`
- `*_BUILDERS`
- `*_MATRIX`

### Initial examples already known

- `cli_portify/prompts.py:PROMPT_BUILDERS`
- `cli_portify/gates.py:GATE_REGISTRY`
- `cli_portify/failures.py:FAILURE_HANDLERS`

### Severity policy

- unresolved entry => **critical**
- unused registry/accessor layer => **major**
- explicit `None` entry without proven alternate path => **major**

## 7. Report Artifact Design

## 7.1 Output file

Emit:

- `wiring-verification.md`

## 7.2 Required frontmatter

```yaml
gate: wiring-verification
analysis_scope: <path>
files_analyzed: <int>
rollout_mode: shadow|soft|full
analysis_complete: true
audit_artifacts_used: <int>
unwired_callable_count: <int>
orphan_symbol_count: <int>
unregistered_dispatch_count: <int>
critical_count: <int>
major_count: <int>
info_count: <int>
total_findings: <int>
blocking_findings: <int>
severity_summary:
  critical: <int>
  major: <int>
  info: <int>
```

## 7.3 Required body sections

1. Summary
2. Unwired Optional Callable Injections
3. Orphan Modules / Symbols
4. Unregistered Dispatch Entries
5. Suppressions and Dynamic Retention
6. Recommended Remediation
7. Evidence and Limitations

## 7.4 Why the gate validates the artifact, not the repository

This is required by the existing substrate:

- `SemanticCheck.check_fn` accepts only `content: str`
- `gate_passed()` evaluates files, not repositories
- roadmap execution is step-artifact based

Therefore the source analysis must happen before gate evaluation, and the gate must validate only the emitted report.

## 8. Rollout Model

## 8.1 Rollout states

### Shadow

- step always runs
- report always emitted
- findings visible in output
- pipeline does not fail due to findings
- used to calibrate false positives and whitelist quality

### Soft

- report always emitted
- only policy-defined blocking findings fail the gate
- major findings may remain warning-only
- deferred remediation entry may be produced

### Full

- report always emitted
- all blocking-class findings fail gate
- intended end state for release protection

## 8.2 Mapping rollout onto existing infrastructure

Use the existing substrate in two layers:

### Layer 1 — existing gate substrate

- `GateCriteria`
- `SemanticCheck`
- `gate_passed()`

### Layer 2 — existing non-blocking support where appropriate

- `GateMode.TRAILING`
- `TrailingGateRunner`
- `DeferredRemediationLog`

### Important rule

Do **not** create a second bespoke rollout framework. Shadow / soft / full is policy over the existing gate/report model.

## 8.3 Recommended rollout strategy

### v1

- roadmap wiring step added now
- deterministic report generation enabled now
- roadmap config defaults to `rollout_mode=shadow`
- gate validates artifact structure and count consistency, but findings remain non-blocking

### v1.1

- `soft` mode enabled behind config
- critical unresolved wiring failures become blocking or deferred-remediation-triggering based on explicit policy

### v1.2

- `full` mode becomes default for release-grade roadmap validation

## 9. Executor Behavior

## 9.1 Step implementation shape

Choose deterministic execution, not LLM synthesis.

### Rejected option

LLM-only report generation from pre-read analyses.

Reason: too weak for wiring assurance and too dependent on narrative interpretation.

### Chosen option

Executor-special-cased deterministic step:

1. gather source scope
2. load optional cleanup-audit artifacts
3. run wiring analysis
4. emit `wiring-verification.md`
5. validate with `gate_passed()`

## 9.2 Configuration needs

Add roadmap wiring-step config sufficient to control:

- source subtree to analyze
- rollout mode: `shadow|soft|full`
- optional thresholds for blocking findings
- optional suppression / whitelist file path
- optional cleanup-audit artifact directory

Keep config minimal. Do not introduce a new framework-level config subsystem.

## 9.3 Resume behavior

Because roadmap already resumes by gate-passing existing artifacts, the new step naturally fits current resume behavior if:

- `wiring-verification.md` is deterministic
- its gate result is reproducible
- `_get_all_step_ids()` is updated to include `wiring-verification`

## 10. False Positive Governance

## 10.1 Known noise sources

- intentionally optional lifecycle hooks
- config-driven or plugin-selected registry entries
- package re-exports and alias imports
- reflection / dynamic import patterns
- tests-only seams not used in production wiring

## 10.2 Suppression policy

Suppressions must be explicit and reviewable.

Each suppression must include:

- target symbol or file
- reason
- optional expiry / revalidation note

## 10.3 Audit-assisted suppression

If cleanup-audit already established a dynamic-use or retention reason, the wiring gate should downgrade or suppress the corresponding orphan finding instead of double-flagging it.

## 11. File Manifest

### New

- `src/superclaude/cli/audit/wiring_gate.py`
- `tests/cli/audit/test_wiring_gate.py`
- `tests/cli/roadmap/test_wiring_verification_step.py`

### Modified

- `src/superclaude/cli/roadmap/gates.py`
- `src/superclaude/cli/roadmap/executor.py`
- roadmap config module for minimal wiring-step settings
- cleanup-audit analyzer/report schema only where needed for evidence reuse

## 12. Success Criteria

The release succeeds when all are true:

1. new wiring step is inserted in `roadmap/executor.py:_build_steps()` after `spec-fidelity`
2. wiring analysis emits a deterministic `wiring-verification.md`
3. `WIRING_VERIFICATION_GATE` validates that artifact via existing gate substrate
4. unwired callable injections from `docs/generated/cli-unwired-components-audit.md` are detected
5. orphan helper/module patterns such as unused audit gates and dead gate families are detected
6. disconnected registries such as `PROMPT_BUILDERS`, `GATE_REGISTRY`, and `FAILURE_HANDLERS` are detected
7. cleanup-audit evidence is reused, with `audit-analyzer` extended rather than duplicated
8. shadow rollout works without introducing parallel infrastructure
9. soft and full rollout can be enabled by config without redesigning the substrate

## 13. Recommended Decisions

### Decision 1 — Keep enforcement artifact-based
Adopt.

### Decision 2 — Implement wiring analysis as deterministic Python, not LLM synthesis
Adopt.

### Decision 3 — Extend `audit-analyzer` evidence, do not create new audit agents
Adopt.

### Decision 4 — Integrate via `_build_steps()` as a post-merge step immediately after `spec-fidelity`
Adopt.

### Decision 5 — Treat shadow / soft / full as policy layered on existing gate/report infrastructure
Adopt.

## 14. Out of Scope for v1

- cross-language wiring verification
- runtime execution tracing
- deep reflection-heavy resolution beyond explicit static evidence
- auto-remediation of findings
- replacement of cleanup-audit dependency graph with a full program-wide symbol graph
- generic gate-registration refactor

## 15. Follow-on Tasklist Shape

Recommended implementation tracks:

1. **Analyzer track** — AST/reference detectors and normalized report model
2. **Roadmap integration track** — gate constant, deterministic step execution, `_build_steps()` insertion, resume IDs
3. **Audit reuse track** — extend `audit-analyzer` evidence fields and consume prior audit artifacts
4. **Rollout track** — shadow/soft/full policy and suppression governance

Critical path:

`deterministic wiring analyzer` → `wiring-verification.md emitter` → `WIRING_VERIFICATION_GATE` → `_build_steps()` insertion → `shadow rollout`
