---
total_diff_points: 12
shared_assumptions_count: 9
---

## Shared Assumptions and Agreements

1. **Source file is the authority** — Both variants treat `src/superclaude/skills/tdd/SKILL.md` as the canonical source and agree content must flow through `make sync-dev`.
2. **5 refs files** — Identical target decomposition: `agent-prompts.md`, `validation-checklists.md`, `synthesis-mapping.md`, `build-request-template.md`, `operational-guidance.md`.
3. **Fidelity as blocking gate** — Both treat textual drift as a release-blocking defect, not advisory.
4. **Line-count discrepancy must resolve first** — OQ-1 (1,364 vs 1,387) is a prerequisite before migration in both variants.
5. **BUILD_REQUEST cross-reference is highest integration risk** — Both identify the 6 allowlisted path rewrites as a critical wiring point.
6. **Phase loading contract** — Both define the same declared/forbidden load matrix (orchestrator loads build-request at A.7; builder loads the other 4 refs).
7. **14 success criteria** — Both reference the same SC-1 through SC-14 checklist from the spec.
8. **Verbatim extraction policy** — Both enforce zero drift with checksum markers (first/last 10 words per block).
9. **Same 5 risks identified** — Content loss (HIGH), cross-reference breakage (HIGH), wrong loading order (MEDIUM), semantic drift in quality gates (HIGH), line-count discrepancy (MEDIUM).

---

## Divergence Points

### 1. Phase Count and Granularity

- **Opus**: 5 phases (Baseline → Migration → BUILD_REQUEST Wiring → SKILL.md Reduction → Sync/Fidelity Gate)
- **Haiku**: 5 phases numbered 0–4 (Discovery → Refs Extraction → SKILL.md Decomposition → Integration/Sync → Fidelity Certification)
- **Impact**: Opus separates BUILD_REQUEST wiring (Phase 3) from content migration (Phase 2), giving it a dedicated phase with its own gate. Haiku bundles the allowlisted path rewrites into Phase 1 alongside extraction. Opus's separation reduces blast radius if wiring fails; Haiku's bundling is faster but couples extraction success with wiring success.

### 2. BUILD_REQUEST Wiring Timing

- **Opus**: Defers path-reference updates to Phase 3, after all destination files exist. Phase 2 extracts verbatim only.
- **Haiku**: Applies allowlisted path updates during Phase 1 extraction itself (M1.2).
- **Impact**: Opus's approach is safer — you can't wire references to files that don't exist yet. Haiku risks a partial-state failure if extraction of a referenced target file fails while the build-request template already has rewritten paths.

### 3. Line-Count Anchor Position

- **Opus**: Asserts the actual file is 1,387 lines and treats 1,364 as the fidelity index error. All ranges re-anchored to 1,387.
- **Haiku**: Treats OQ-1 as still open, references "1,364 lines" throughout (e.g., "fidelity index coverage for lines 1–1364"), and defers resolution to Phase 0.
- **Impact**: Opus takes a definitive stance that could be wrong but enables concrete planning. Haiku is more cautious but carries the 1,364 assumption into later phases (Phase 4 still says "lines 1–1364"), which would be incorrect if the file is indeed 1,387 lines.

### 4. Parallelization Strategy

- **Opus**: Explicitly marks Phase 2's 5 extraction tasks as parallelizable with rationale (non-overlapping line ranges, separate destination files).
- **Haiku**: Does not discuss parallelization within phases.
- **Impact**: Opus's explicit parallel guidance enables a ~3x speedup on the largest phase. Haiku leaves execution strategy to the implementer.

### 5. Timeline Estimation

- **Opus**: 3–4 hours hands-on, with per-phase minute estimates.
- **Haiku**: 3.5–5 days, with per-phase day estimates.
- **Impact**: An order-of-magnitude difference. Opus treats this as a single-session mechanical refactor. Haiku's estimate suggests a multi-day effort with review cycles and rework buffer. The spec's complexity score (0.53, MEDIUM) and the procedural nature of the work favor Opus's estimate, but Haiku's buffer accounts for discovery surprises.

### 6. Roles and Staffing Model

- **Opus**: Implicitly single-operator (the Claude agent executing the refactor).
- **Haiku**: Defines 4 roles — Architect/Lead, Implementation Engineer, QA/Reviewer, Optional Toolsmith.
- **Impact**: Haiku's multi-role model is more appropriate for a team setting but adds coordination overhead. Opus's model matches the likely execution context (a single Claude session).

### 7. Discovery Phase Naming and Scope

- **Opus**: Phase 1 "Baseline Verification & Line-Range Anchoring" — focused on line counts, fidelity index correction, and OQ resolution.
- **Haiku**: Phase 0 "Discovery, Contract Baseline, and Ambiguity Resolution" — adds contract baseline (M0.2: transformation allowlist, M0.3: phase contract matrix) to the discovery phase.
- **Impact**: Haiku front-loads contract design into Phase 0, meaning the loading/wiring contracts are defined before any content moves. Opus defines contracts in Phase 4 (when SKILL.md is being rewritten). Haiku's approach catches contract design errors earlier.

### 8. Verification Gate Structure

- **Opus**: Per-phase verification gates with specific pass/fail criteria inline.
- **Haiku**: 4 named gates (A–D) spanning multiple phases: Structural completeness → Sync/contract → Fidelity/semantic → Runtime parity.
- **Impact**: Opus's gates are more actionable (tied to specific phase outputs). Haiku's gates are more auditable (cross-cutting concerns grouped logically). Opus is better for execution; Haiku is better for review.

### 9. Precedent Pattern Assessment

- **Opus**: Explicitly identifies Risk R6 — the adversarial-protocol refs pattern "does not yet exist in the codebase" and this refactor pioneers it.
- **Haiku**: References `sc-adversarial-protocol/refs/` as a tooling dependency (Section 5) without questioning its existence.
- **Impact**: Opus's observation is architecturally important. If the pattern doesn't exist, there's no validated precedent to follow, and the refactor is establishing convention rather than following it. Haiku's assumption could lead to confusion if implementers look for a non-existent reference implementation.

### 10. OQ-3 Handling

- **Opus**: Declares OQ-3 (missing FR for operational-guidance) as already resolved — addressed by FR-TDD-R.8.
- **Haiku**: Does not mention OQ-3 at all.
- **Impact**: Minor. Opus provides explicit closure; Haiku omits it, which could leave reviewers wondering about its status.

### 11. Task-Level Specificity

- **Opus**: Provides exact block IDs (B01–B34), approximate line ranges, and specific acceptance criteria per extraction task.
- **Haiku**: Describes scope at the requirement level (FR-TDD-R.2, etc.) without block-level mapping in the phase descriptions.
- **Impact**: Opus is directly executable — an implementer can start extracting without re-reading the spec. Haiku requires cross-referencing the spec and fidelity index to determine what to extract.

### 12. Integration Point Documentation

- **Opus**: Embeds integration points inline within their owning phases, with cross-reference tables.
- **Haiku**: Dedicates a separate Section 3 with 4 named integration points (IP-1 through IP-4), each with Named Artifact / Wired Components / Owning Phase / Cross-Reference.
- **Impact**: Haiku's standalone section is easier to audit as a cross-cutting concern. Opus's inline placement is better for execution flow but harder to review holistically.

---

## Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:

- **Executability**: Per-phase minute estimates, parallelization guidance, block-level task descriptions, and inline verification steps make it directly actionable without cross-referencing.
- **BUILD_REQUEST wiring safety**: Deferring path rewrites until destination files exist (Phase 3 after Phase 2) eliminates a class of partial-state failures.
- **Line-count resolution**: Taking a definitive position on 1,387 lines enables concrete range planning rather than carrying ambiguity forward.
- **Precedent awareness**: Identifying that the refs pattern is being pioneered, not followed, is an important architectural insight.
- **Realistic timeline**: 3–4 hours matches the mechanical, procedural nature of the work at complexity 0.53.

### Haiku is stronger in:

- **Contract-first sequencing**: Front-loading contract design (Phase 0, M0.2/M0.3) before migration ensures the loading discipline is designed before content moves.
- **Integration point documentation**: Dedicated IP-1 through IP-4 section with structured fields is more auditable and reusable.
- **Gated validation structure**: Named gates A–D that group cross-cutting concerns (structural, sync, fidelity, runtime) are cleaner for review workflows.
- **Requirement traceability**: Explicit FR→Phase→Gate mapping in Section 6 makes compliance auditing straightforward.

---

## Areas Requiring Debate to Resolve

1. **When to define the phase loading contract** — Opus defers to Phase 4 (alongside SKILL.md reduction); Haiku front-loads to Phase 0. The debate: is it better to design contracts before you know the exact content boundaries, or after extraction proves what the boundaries actually are?

2. **When to apply BUILD_REQUEST path rewrites** — Opus says after all targets exist (Phase 3); Haiku says during extraction (Phase 1). The safety argument favors Opus, but Haiku avoids a second pass over the same file. Worth debating whether the risk justifies the extra phase.

3. **Timeline calibration** — 3–4 hours vs 3.5–5 days. This needs resolution based on execution context: single Claude session (Opus is right) vs. multi-person team with review gates (Haiku is right). The spec doesn't specify.

4. **Line-count authority** — Opus commits to 1,387; Haiku keeps OQ-1 open. A simple `wc -l` resolves this, but the debate matters for planning: should a roadmap commit to an assumed answer or defer all assumptions?
