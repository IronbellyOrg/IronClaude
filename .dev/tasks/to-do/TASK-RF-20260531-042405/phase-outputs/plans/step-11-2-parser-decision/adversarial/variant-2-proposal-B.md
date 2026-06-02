# Variant 2 — Proposal B: Thread the envelope into the semantic-check dispatch

## Problem being solved
Same as Variant 1: the 24 in-gate semantic checks receive only `content: str`; Step 11.2(d) wants them to read `envelope.frontmatter`.

## Mechanism
1. **Widen `SemanticCheck.check_fn`** from `Callable[[str], bool|str]` to accept the envelope (e.g. `Callable[..., object]` or `(content, envelope) -> bool|str`) in `cli/pipeline/models.py`.
2. **Change `gate_passed`** (`pipeline/gates.py:82-84`) to pass the envelope into every semantic check: `check.check_fn(content, envelope)`.
3. **Thread the envelope into `execute_pipeline`'s gate call** (`pipeline/executor.py:267`, currently `gate_passed(gate_target, step.gate)` with no envelope) so the envelope reaches the dispatch at all.
4. **Reorder** so the post-step extractor populates `envelope.frontmatter` for the current step BEFORE its gate runs (currently the extractor runs AFTER the step impl, `executor.py:1491`).
5. **Rewrite the 24 checks** to read `envelope.frontmatter` instead of parsing `content`.
6. Delete the 6 parser variants; populate `envelope.frontmatter` from the post-step extractor.

## How it claims to satisfy the contracts
- **11.2(d) literal:** checks read `envelope.frontmatter` (true dependency injection, no re-parsing) — the most literal reading of the clause.
- **Contract #6 / §MVR §1:** one parser, state via envelope.

## Blast radius (the cost)
- **`SemanticCheck` is a SHARED dataclass consumed by 8 gate modules**: `roadmap/gates.py`, `roadmap/validate_gates.py`, `prd/gates.py`, `tasklist/gates.py`, `cleanup_audit/gates.py`, `cli_portify/gates.py`, `audit/wiring_gate.py`, `audit/reachability.py`. Widening its signature forces a migration of EVERY check in ALL 8 modules, not just roadmap's 24.
- **`execute_pipeline` / `gate_passed` are shared with sprint** (`sprint/executor.py`). Threading envelope through the generic gate call at `pipeline/executor.py:267` changes the sprint pipeline's gate path too.
- **NFR-007 hazard:** `pipeline.*` MUST NOT import `roadmap.*`. `PipelineEnvelope` lives in `cli/roadmap/envelope.py`. Making `SemanticCheck` (in `pipeline/models.py`) carry a `PipelineEnvelope` re-introduces the forward-ref gymnastics that `CodeAssertion` already had to use, and pushes the pipeline→roadmap boundary.
- **Ordering rewrite:** moving the extractor before the gate is a control-flow change to per-step execution, with resume/state-persistence implications.

## Duplication of an existing mechanism
The codebase ALREADY has the envelope-aware gate tier: `CodeAssertion` (`models.py:108`), signature `(PipelineEnvelope, Path) -> Finding|None`, docstring "Unlike `SemanticCheck` (which inspects the rendered string content of an output file), a `CodeAssertion` inspects the live code graph." Envelope-aware gating is the deliberate job of `CodeAssertion` (R1.3 / §MVR §2). Proposal B makes `SemanticCheck` do what `CodeAssertion` was built to do, blurring the two-tier model.

## Feasibility problem
At gate-evaluation time the envelope is NOT passed to semantic checks (`pipeline/executor.py:267`), AND `envelope.frontmatter` for the current step is not yet populated (extractor runs later, `executor.py:1491`). So B is not a localized change — it is infeasible WITHOUT both the generic-pipeline dispatch change (step 3) and the reorder (step 4).

## Risks
- 8-module migration; shared-substrate change; sprint-pipeline impact; NFR-007 pressure; control-flow reorder with resume implications. High regression surface for a problem that is local file validation.
