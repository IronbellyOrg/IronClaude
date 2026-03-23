---
title: "Validate-Roadmap CLI Integration — Analysis Brief"
status: backlog
created: 2026-03-23
source: conversation-analysis (sc:analyze session)
decision: Option 3 — Single source, slash command wraps CLI
next_step: spec or roadmap generation
---

# Validate-Roadmap CLI Integration

## Decision Summary

Integrate `sc:validate-roadmap` into the `superclaude roadmap` CLI pipeline as the authoritative spec-fidelity engine. The slash command becomes a thin wrapper invoking the CLI. The roadmap pipeline's spec-fidelity step calls the same Python logic internally.

**Decision rationale**: Avoids a fork where the SKILL.md protocol and Python implementation diverge independently. Follows the established pattern where `sc:roadmap` maps to `superclaude roadmap run`.

---

## 1. Current Architecture (As-Is)

### Three overlapping validation systems exist today:

#### A. Roadmap Pipeline Spec-Fidelity Step (Step 8)
- **Location**: `src/superclaude/cli/roadmap/executor.py:891-900`
- **Prompt builder**: `src/superclaude/cli/roadmap/prompts.py:312` (`build_spec_fidelity_prompt`)
- **Gate**: `SPEC_FIDELITY_GATE` in `src/superclaude/cli/roadmap/gates.py:916-939`
- **Two modes**:
  - **LLM mode** (default): Single Claude subprocess comparing spec vs roadmap across 6 dimensions (signatures, data models, gates, CLI options, NFRs, integration wiring). Produces `spec-fidelity.md`.
  - **Convergence mode** (`--convergence`): Python-orchestrated structural checkers + semantic layer + convergence engine (max 3 runs) with TurnLedger budget. Auto-remediates HIGH findings. Uses `src/superclaude/cli/roadmap/convergence.py`, `structural_checkers.py`, `semantic_layer.py`.
- **Gate requirements**: `high_severity_count: 0`, `tasklist_ready` consistent with severity counts and `validation_complete`
- **Output**: Single `spec-fidelity.md` file
- **Runtime**: ~5 min (LLM) or ~10 min (convergence)
- **Downstream chain**: `spec-fidelity` → `wiring-verification` → `deviation-analysis` → `remediate` → `certify`

#### B. Roadmap Pipeline Wave 4 / `superclaude roadmap validate`
- **Location**: `src/superclaude/cli/roadmap/validate_executor.py`
- **CLI command**: `superclaude roadmap validate <output_dir>`
- **Purpose**: Artifact quality validation (NOT spec-fidelity)
- **What it does**: Runs 1-N reflection agents on roadmap.md, test-strategy.md, extraction.md
- **Checks**: Completeness, consistency, traceability, test strategy quality
- **Scoring**: quality-engineer (0.55 weight) + self-review (0.45 weight)
- **Thresholds**: PASS >= 85%, REVISE 70-84%, REJECT < 70%
- **Output**: `validate/validation-report.md` with blocking/warning/info counts
- **Key limitation**: Does NOT extract requirement universe from spec, does NOT do per-requirement coverage analysis

#### C. `sc:validate-roadmap` Slash Command + Protocol
- **Command**: `src/superclaude/commands/validate-roadmap.md`
- **Protocol**: `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`
- **Purpose**: Full adversarial spec-to-roadmap fidelity audit
- **6 phases**: Requirement extraction → Domain decomposition → Parallel agent validation → Consolidation → Adversarial review → Remediation planning
- **Battle-tested**: Real outputs exist at `.dev/releases/current/turnledger-integration/v3.3-TurnLedger-Validation/validation/`
- **Runtime**: 20-60 min depending on spec size and `--depth`

### Key differences: Pipeline Step 8 vs sc:validate-roadmap

| Dimension | Pipeline Spec-Fidelity (Step 8) | sc:validate-roadmap |
|---|---|---|
| Scope | Single-pass 6-dimension comparison | Full requirement universe extraction + multi-agent domain validation |
| Agent count | 1 LLM call (or convergence loop) | N domain agents + 4 cross-cutting + adversarial reviewer |
| Evidence standard | Quote both documents per deviation | Quote + line range + search terms attempted + substance matching |
| Coverage model | Binary (deviation or not) | 5-status: COVERED / PARTIAL / MISSING / CONFLICTING / IMPLICIT |
| Adversarial | No | Yes — fresh-eye pass challenges all COVERED claims |
| Remediation | Convergence mode auto-remediates | Plans remediation but does NOT execute |
| Artifacts | 1 file (spec-fidelity.md) | 11 files in validation/ directory |
| Gate integration | SPEC_FIDELITY_GATE with frontmatter checks | Own verdict system (GO / CONDITIONAL_GO / NO_GO) |
| Runtime | ~5-10 min | ~20-60 min |

---

## 2. Target Architecture (To-Be)

### Option 3: Single source — slash command wraps CLI

```
superclaude roadmap run <spec>
  └─ Step 8 (spec-fidelity) calls validate-fidelity executor internally
       └─ Same Python logic as CLI subcommand

superclaude roadmap validate-fidelity <output_dir> --specs <spec1,spec2>
  └─ Standalone CLI entry point for the same executor

/sc:validate-roadmap <roadmap> --specs <spec>
  └─ Thin wrapper that invokes superclaude roadmap validate-fidelity
```

**Authority flow**: Python executor is authoritative → CLI exposes it → slash command wraps CLI → SKILL.md becomes documentation (not behavior)

### What must be built

A new Python executor (e.g., `validate_fidelity_executor.py`) implementing the 6 phases of `sc:validate-roadmap` as orchestrated pipeline steps:

| Phase | Protocol Phase | Pipeline Step | Agent(s) | Output |
|---|---|---|---|---|
| 0 | Document ingestion + requirement universe extraction | `req-extract` | 1 LLM | `00-requirement-universe.md`, `00-roadmap-structure.md`, `00-domain-taxonomy.md` |
| 1 | Domain/cross-cutting agent decomposition | `decompose` | 0 (deterministic) | `00-decomposition-plan.md` |
| 2 | Parallel domain validation | `validate-{domain}` (parallel group) | N domain + 4 cross-cutting | `01-agent-*.md` |
| 3 | Consolidation + coverage matrix | `consolidate` | 1 LLM | `02-unified-coverage-matrix.md`, `02-consolidated-report.md` |
| 4 | Adversarial review | `adversarial-review` | 1 LLM | `03-adversarial-review.md` |
| 5 | Remediation plan | `remediation-plan` | 1 LLM | `04-remediation-plan.md` |
| 6 | Summary + verdict | `summary` | 0 (deterministic) | `05-validation-summary.md` |

### Adapter layer needed

The summary step must produce a `spec-fidelity.md` compatible with `SPEC_FIDELITY_GATE`:

```yaml
# Map from validate-roadmap verdict to SPEC_FIDELITY_GATE frontmatter
GO → high_severity_count: 0, tasklist_ready: true, validation_complete: true
CONDITIONAL_GO → high_severity_count: 0, tasklist_ready: true (with warnings)
NO_GO → high_severity_count: >0, tasklist_ready: false
```

---

## 3. Risk Register

### R-001: Runtime cost (HIGH)
- **Risk**: N+4 parallel agents + adversarial pass adds 20-60 min to a pipeline already taking 30-60 min
- **Mitigation**: Add `--deep-fidelity` flag; default to current fast path; deep validation opt-in
- **Mitigation**: Retain structural checkers as pre-filter — skip heavy validation if structural checks already pass clean

### R-002: Artifact format mismatch (MEDIUM)
- **Risk**: `SPEC_FIDELITY_GATE` expects specific frontmatter; validate-roadmap produces different schema
- **Mitigation**: Adapter layer in summary step translates verdict to gate-compatible frontmatter
- **Consideration**: Do we also update `SPEC_FIDELITY_GATE` to understand the richer schema, or keep the adapter?

### R-003: Remediation gap (MEDIUM)
- **Risk**: sc:validate-roadmap only PLANS remediation, never executes it. Current convergence mode auto-remediates. Pipeline downstream steps (deviation-analysis, remediate, certify) expect fidelity issues to have been attempted.
- **Mitigation options**:
  - A) Wire remediation plan output into existing `remediate` step
  - B) Add remediation execution to the new fidelity executor
  - C) Keep convergence engine's auto-remediation as a separate post-step

### R-004: Execution model mismatch (MEDIUM)
- **Risk**: sc:validate-roadmap is inference-based (runs in Claude Code conversation). CLI pipeline spawns isolated `claude` subprocesses via `ClaudeProcess`. Each phase's prompt needs to be extracted and templated.
- **Mitigation**: This is exactly what `sc:cli-portify` is designed for — porting inference protocols to CLI pipelines

### R-005: Gate chain disruption (LOW-MEDIUM)
- **Risk**: Downstream steps depend on spec-fidelity output:
  - `wiring-verification` uses `spec-fidelity` output file as input
  - `deviation-analysis` checks spec-fidelity result hash for staleness
  - Existing `.roadmap-state.json` tracking of `fidelity_status`
- **Mitigation**: Adapter produces `spec-fidelity.md` in expected location with expected schema. Validation artifacts go to `validation/` subdirectory alongside it.

### R-006: Convergence engine loss (LOW)
- **Risk**: Structural checkers (Python, deterministic) catch code-level issues that LLM-based protocol might miss or hallucinate
- **Mitigation**: Retain structural checkers as Phase 0 pre-filter; merge their findings into the requirement universe extraction

### R-007: Scope creep (LOW)
- **Risk**: Building a 7-step sub-pipeline within a 14-step parent pipeline
- **Mitigation**: Clear boundaries — validate-fidelity is a self-contained executor called by Step 8, like how convergence mode already works

---

## 4. Rewards

### High value
- **Dramatically deeper coverage**: Requirement universe extraction catches implicit, process, cross-cutting, and integration requirements the current single-prompt misses
- **Adversarial rigor**: Fresh-eye pass challenging COVERED claims — the current pipeline trusts its own LLM output
- **Evidence trail**: 11 artifacts with per-requirement evidence vs 1 summary file

### Medium value
- **Domain specialization**: Parallel domain agents provide expertise (security agent for security reqs, etc.)
- **Battle-tested**: Real production runs exist (v3.3 TurnLedger validation artifacts prove it works)
- **Unified validation vocabulary**: Eliminates confusion about which of the three validators is authoritative
- **Single source of truth**: Protocol changes propagate automatically — no fork maintenance

---

## 5. Key Files Reference

### Slash command + protocol (source of requirements)
- `src/superclaude/commands/validate-roadmap.md`
- `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`

### Current pipeline spec-fidelity (to be replaced/augmented)
- `src/superclaude/cli/roadmap/executor.py` — main pipeline executor, spec-fidelity at lines 891-900, convergence at 539-675
- `src/superclaude/cli/roadmap/prompts.py:312` — `build_spec_fidelity_prompt`
- `src/superclaude/cli/roadmap/gates.py:916-939` — `SPEC_FIDELITY_GATE`
- `src/superclaude/cli/roadmap/convergence.py` — convergence engine
- `src/superclaude/cli/roadmap/structural_checkers.py` — deterministic checkers
- `src/superclaude/cli/roadmap/semantic_layer.py` — semantic analysis layer

### Current validate CLI (quality validation, separate concern)
- `src/superclaude/cli/roadmap/commands.py:215-290` — `validate` subcommand
- `src/superclaude/cli/roadmap/validate_executor.py` — reflection-based quality validator
- `src/superclaude/cli/roadmap/validate_gates.py` — `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`

### Pipeline infrastructure (reusable)
- `src/superclaude/cli/pipeline/executor.py` — `execute_pipeline()` generic orchestrator
- `src/superclaude/cli/pipeline/models.py` — `Step`, `StepResult`, `GateCriteria`, `PipelineConfig`
- `src/superclaude/cli/pipeline/process.py` — `ClaudeProcess` subprocess wrapper

### Gate chain (must remain compatible)
- Gate order: extract → generate-A/B → diff → debate → score → merge → anti-instinct → test-strategy → **spec-fidelity** → wiring-verification → deviation-analysis → remediate → certify
- All gates defined in `src/superclaude/cli/roadmap/gates.py:1076-1091` (`ALL_GATES`)

### Production validation artifacts (evidence it works)
- `.dev/releases/current/turnledger-integration/v3.3-TurnLedger-Validation/validation/`

---

## 6. Integration Design Decisions (Open)

These need resolution during spec/roadmap generation:

1. **New subcommand or extend existing?** — `superclaude roadmap validate-fidelity` (new) vs expanding `superclaude roadmap validate` (existing, currently does quality validation)

2. **Default behavior** — Should `superclaude roadmap run` use the deep fidelity validator by default, or only when `--deep-fidelity` is passed? Current fast path is valuable for iteration speed.

3. **Structural checkers integration** — Keep as pre-filter before LLM phases, merge into Phase 0, or run alongside Phase 2 agents?

4. **Remediation execution** — Who executes the remediation plan? The fidelity executor (self-contained), the existing `remediate` pipeline step (preserves chain), or a new step inserted between them?

5. **Gate evolution** — Update `SPEC_FIDELITY_GATE` to understand the richer 11-artifact schema, or keep an adapter that maps to the current simple schema?

6. **Convergence engine fate** — Retain alongside the new validator (two modes: fast/deep), deprecate in favor of deep-only, or merge convergence loop into the new executor?

7. **Agent budget** — The protocol allows 4-20 parallel agents. The pipeline needs a sensible default and a `--max-agents` flag.

8. **`sc:validate-roadmap` wrapper implementation** — Does the slash command invoke `superclaude roadmap validate-fidelity` via Bash tool, or does it use a different mechanism?

---

## 7. Suggested Phasing

### Phase A: Build the executor
- Port `sc:validate-roadmap` 6-phase protocol to Python (`validate_fidelity_executor.py`)
- Reuse `execute_pipeline()`, `ClaudeProcess`, `Step`, `GateCriteria` infrastructure
- Build prompt templates for each phase
- Build gates for each phase
- Write adapter that produces `spec-fidelity.md` compatible with `SPEC_FIDELITY_GATE`

### Phase B: Wire into roadmap pipeline
- Replace/augment spec-fidelity step in `executor.py` to call the new executor
- Add `--deep-fidelity` flag to `superclaude roadmap run`
- Ensure downstream chain (wiring-verification, deviation-analysis, remediate, certify) works with new output

### Phase C: Create CLI subcommand
- Add `superclaude roadmap validate-fidelity` to `commands.py`
- Accept `--specs`, `--depth`, `--max-agents`, `--skip-adversarial`, `--skip-remediation`

### Phase D: Thin-wrap the slash command
- Update `sc:validate-roadmap` command to invoke CLI
- Update `sc-validate-roadmap-protocol/SKILL.md` to document-only role
- Verify existing production workflows still work

### Phase E: Deprecation + cleanup
- Deprecate convergence mode or merge its structural checkers into Phase 0
- Remove or archive `build_spec_fidelity_prompt` (LLM mode)
- Update tests
