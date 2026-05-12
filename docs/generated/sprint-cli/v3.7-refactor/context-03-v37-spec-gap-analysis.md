---
title: "Context Document 3: v3.7 Spec Gap Analysis — What It Addresses vs What It Misses"
generated: 2026-04-03
purpose: Map v3.7-task-unified-v2 spec coverage against identified deficiencies
source: v3.7-UNIFIED-RELEASE-SPEC-merged.md cross-referenced with context docs 1-2
---

# v3.7 Spec Gap Analysis

## The Core Problem

The v3.7 spec invests its improvements exclusively into Path B (`build_prompt()` in process.py), which is the fallback path for malformed/legacy phase files. Path A (`_run_task_subprocess()` in executor.py:1064-1068), which handles every properly structured production sprint, receives none of the improvements.

**All production sprints using `sc-tasklist-protocol`-generated tasklists execute via Path A.**

## What v3.7 Addresses (Path B Only)

| Feature | Spec Section | Target File | Path |
|---------|-------------|-------------|------|
| Checkpoint prompt instructions | T01.01 | `process.py:build_prompt()` | B only |
| Post-phase checkpoint gate | T01.02 | `executor.py` (post-phase) | Both (phase-level) |
| Checkpoint manifest + CLI verify | Wave 3 | New `checkpoints.py` | Both (phase-level) |
| TUI v2 (10 features) | Section 3.2 | `tui.py`, `monitor.py`, new modules | Both (outer loop) |
| Token/turn tracking on PhaseResult | Section 7 | `models.py` | Both (phase-level) |
| Naming consolidation | Section 3.3 | `process.py:170`, 21 files | B primarily |
| Haiku post-phase summaries | F8 | New `summarizer.py` | Both (post-phase) |
| Release retrospective | F10 | New `retrospective.py` | Both (post-sprint) |

## What v3.7 Does NOT Address (Path A Gaps)

### Gap 1: Per-Task Prompt Enrichment
**Not mentioned in spec.** `_run_task_subprocess()` at executor.py:1064-1068 is never referenced.
- No per-task block extraction
- No scope boundary
- No sprint context injection
- No skill invocation (`/sc:task-unified`)

### Gap 2: TurnLedger Reimbursement Bugs
**Not mentioned in spec.**
- `turns_consumed` returns 0 (executor.py:1091)
- `TaskResult.output_path` never set (executor.py:1017-1025)
- `gate_rollout_mode` defaults to "off"
- The economic feedback loop is mathematically zeroed out

### Gap 3: Evidence/Deliverable Verification
**Not mentioned in spec.** No post-task check that `artifacts/D-XXXX/evidence.md` or deliverable files exist.

### Gap 4: `build_task_context()` Wiring
**Not mentioned in spec.** Dead code remains dead.

### Gap 5: Task Dependency Enforcement
**Not mentioned in spec.** Parsed but not used for ordering.

### Gap 6: Task-Level Resume
**Not mentioned in spec.** Phase-level only.

## Refactoring Principles for v3.7 Revision

### Principle 1: Path A Is the Production Path
Every improvement that targets `build_prompt()` should be evaluated for Path A applicability. If it brings value to per-task execution, it must be adapted for that path.

### Principle 2: Don't Force-Fit Path B Patterns onto Path A
Some Path B patterns (result file contract, stop-on-STRICT-fail) are architecturally unnecessary for Path A due to subprocess isolation. These should NOT be ported.

### Principle 3: Fix the Three Reimbursement Bugs
The TurnLedger system is the existing intra-task QA mechanism. Fixing three input-side bugs (`turns_consumed`, `output_path`, `gate_rollout_mode` default) activates an already-tested economic feedback loop.

### Principle 4: Low-Cost High-Impact First
Per-task prompt enrichment (~280 tokens) and `output_path` wiring (1 line change) are trivially cheap relative to their impact on task execution quality.

## Spec Chunks for Parallel Refactor Analysis

The v3.7 spec naturally decomposes into these analysis units:

| Chunk | Spec Sections | Key Question |
|-------|--------------|--------------|
| **Checkpoint Enforcement** | 3.1, 4.1 (Waves 1-4) | Which checkpoint improvements apply to Path A? Prompt instructions (Wave 1) target `build_prompt()` — does Path A need equivalent? |
| **Sprint TUI v2** | 3.2, 4.2 | TUI operates on outer loop — most features work for both paths. Which features assume Path B's data model (e.g., prompt_preview)? |
| **Naming Consolidation** | 3.3, 4.3 | Rename targets `process.py:170` (Path B). Path A at `executor.py:1064` doesn't invoke `/sc:task-unified` — should it? |
| **Data Model Changes** | Section 7 | New PhaseResult fields (turns, tokens_in/out) — do these need per-task equivalents on TaskResult? |
| **Cross-Cutting + Gaps** | Sections 6, 14 | Open questions that intersect with Path A deficiencies |
| **Path A Enrichment** (NEW) | Not in spec | Per-task prompt enrichment, reimbursement bug fixes, evidence verification, `build_task_context()` wiring |
