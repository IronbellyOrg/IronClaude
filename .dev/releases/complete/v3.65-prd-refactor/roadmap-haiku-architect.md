---
spec_source: "prd-refactor-spec.md"
complexity_score: 0.45
primary_persona: architect
---

## 1) Executive summary

This roadmap delivers a **behavior-preserving decomposition** of `.claude/skills/prd/SKILL.md` into a lean orchestrator file plus 4 lazy-loaded `refs/` files, while enforcing strict fidelity and token-budget constraints.

**Architect priorities**
1. Preserve behavior and content integrity first (FR-PRD-R.7, NFR-PRD-R.4).
2. Make wiring explicit at phase boundaries (FR-PRD-R.6, NFR-PRD-R.2).
3. Keep rollback atomic (single-commit implementation constraint).
4. Validate with diff-based evidence, not interpretation.

**Scope anchors**
- Functional: 7 requirements (FR-PRD-R.1..R.7)
- Non-functional: 4 requirements (NFR-PRD-R.1..R.4)
- Complexity: MEDIUM (0.45), mostly precision and cross-reference risk, not architecture novelty.

---

## 2) Phased implementation plan with milestones

### Phase 0 — Baseline and control setup
**Objective:** Freeze source of truth and establish fidelity baseline before edits.

**Tasks**
1. Snapshot current `SKILL.md` structure and line map for all movable blocks.
2. Confirm/prepare fidelity index at `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md` (FR-PRD-R.7 prerequisite).
3. Define acceptance diff rules (including whitespace normalization scope decision).
4. Confirm open-question decisions that affect acceptance gates.

**Milestones**
- M0.1: Fidelity index is present and complete for all target ranges.
- M0.2: Open-question decisions recorded (token precedence, whitespace scope, B30 naming coexistence).

**Requirements addressed**
- FR-PRD-R.7 (setup)
- Risk 1, 2, 7 prevention

---

### Phase 1 — Create refs/ artifacts (content relocation only)
**Objective:** Materialize all 4 `refs/` files with word-for-word content movement.

**Tasks**
1. Implement `FR-PRD-R.2`  
   - Create `.claude/skills/prd/refs/agent-prompts.md` with all 8 templates and required intro/list.
2. Implement `FR-PRD-R.3`  
   - Create `.claude/skills/prd/refs/validation-checklists.md` with required checklist/process/table blocks.
3. Implement `FR-PRD-R.4`  
   - Create `.claude/skills/prd/refs/synthesis-mapping.md` with output structure + synthesis mapping table.
4. Implement `FR-PRD-R.5`  
   - Create `.claude/skills/prd/refs/build-request-template.md`, applying only documented SKILL CONTEXT FILE path updates.

**Milestones**
- M1.1: 4 files exist and match required path/name.
- M1.2: Per-file block diffs pass with zero semantic/content drift.

**Requirements addressed**
- FR-PRD-R.2, FR-PRD-R.3, FR-PRD-R.4, FR-PRD-R.5

---

### Phase 2 — Refactor orchestrator SKILL.md
**Objective:** Reduce `SKILL.md` to behavioral protocol and explicit load declarations.

**Tasks**
1. Implement `FR-PRD-R.1`  
   - Remove moved HOW/template/checklist/table content.  
   - Keep required behavioral sections and stage flow.
2. Implement `FR-PRD-R.6`  
   - Add explicit A.7 loading declaration with orchestrator vs builder split.  
   - Ensure A.1-A.6 and Stage B do not load extra refs.
3. Update cross-references formerly pointing to local sections to `refs/...` paths.

**Milestones**
- M2.1: `SKILL.md` is 430–500 lines.
- M2.2: A.7 loading declarations present and concrete.
- M2.3: No stale section-name references remain.

**Requirements addressed**
- FR-PRD-R.1, FR-PRD-R.6
- NFR-PRD-R.1, NFR-PRD-R.2

---

### Phase 3 — Fidelity verification and regression validation
**Objective:** Prove zero-loss decomposition and unchanged behavior.

**Tasks**
1. Execute full fidelity verification matrix (FR-PRD-R.7 success checks 1–11).
2. Run E2E invocation for NFR-PRD-R.4 behavioral equivalence.
3. Validate combined line count and token budget targets.
4. Validate sync workflow (`make sync-dev`, `make verify-sync`) per architectural constraint.

**Milestones**
- M3.1: All content-fidelity checks pass.
- M3.2: Behavior regression check passes end-to-end.
- M3.3: Sync validation passes across `src/superclaude/` and `.claude/`.

**Requirements addressed**
- FR-PRD-R.7
- NFR-PRD-R.3, NFR-PRD-R.4

---

### Phase 4 — Release packaging and rollback readiness
**Objective:** Deliver as an atomic, reversible change set.

**Tasks**
1. Consolidate into single commit with traceable acceptance evidence.
2. Include fidelity evidence references in commit/PR body.
3. Prepare rollback instructions (`git revert` single commit).

**Milestones**
- M4.1: Single atomic commit exists.
- M4.2: Rollback procedure validated.

---

## 3) Integration points (explicit wiring mechanisms)

### IP-1: Stage A.7 loading declaration mechanism
- **Named Artifact:** `SKILL.md` Stage A.7 loading declaration block  
- **Wired Components:**  
  - Orchestrator → `refs/build-request-template.md`  
  - Builder subagent context (via BUILD_REQUEST) → `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`
- **Owning Phase:** Phase 2  
- **Cross-Reference:** Consumed in Phase 3 E2E validation

### IP-2: BUILD_REQUEST context-file mapping mechanism
- **Named Artifact:** `refs/build-request-template.md` SKILL CONTEXT FILE references  
- **Wired Components:** Section references rewired to concrete `refs/...` paths; Tier Selection remains in `SKILL.md`
- **Owning Phase:** Phase 1 (FR-PRD-R.5)  
- **Cross-Reference:** Consumed by Phase 2 (`SKILL.md` refactor) and Phase 3 fidelity checks

### IP-3: Fidelity index registry mechanism
- **Named Artifact:** `.dev/releases/backlog/prd-skill-refactor/fidelity-index.md`  
- **Wired Components:** Source line ranges ↔ destination files for every moved/retained block
- **Owning Phase:** Phase 0  
- **Cross-Reference:** Consumed by Phase 1/2 implementation audits and Phase 3 final verification

### IP-4: Artifact locations merge strategy (B05/B30)
- **Named Artifact:** Merged artifact-locations table inside refactored content set  
- **Wired Components:** B05 base entries + appended B30 QA paths (without cosmetic naming normalization)
- **Owning Phase:** Phase 1  
- **Cross-Reference:** Consumed by Phase 3 content-fidelity validation

### IP-5: Component sync pipeline
- **Named Artifact:** `make sync-dev` / `make verify-sync` workflow  
- **Wired Components:** `.claude/skills/prd/*` changes ↔ `src/superclaude/skills/prd/*` source-of-truth parity
- **Owning Phase:** Phase 3  
- **Cross-Reference:** Consumed by Phase 4 release readiness

---

## 4) Risk assessment and mitigation strategies

1. **Content loss during decomposition** (HIGH)  
   - Mitigation: line-range fidelity index + per-block diffs + first/last marker checks.
2. **Cross-reference breakage** (HIGH)  
   - Mitigation: explicit cross-reference map; grep for stale prose section refs post-edit.
3. **Wrong loading order/phase** (MEDIUM)  
   - Mitigation: enforce “A.7-only loads refs” rule; phase-to-ref matrix gate.
4. **Builder cannot resolve refs paths** (MEDIUM)  
   - Mitigation: path resolution test from skill directory context in E2E.
5. **B30/B05 merge errors** (LOW)  
   - Mitigation: deterministic merge rule (append-only for B30 unique entries).
6. **Missing/renamed refs file** (MEDIUM)  
   - Mitigation: existence checks + fail-fast runtime + single-commit rollback.
7. **Spec freshness drift** (MEDIUM)  
   - Mitigation: lock baseline early; if source changed, regenerate line mappings before merge.

**Risk burn-down checkpoints**
- After Phase 1: risks 1, 5, 6 largely retired.
- After Phase 2: risks 2, 3 retired.
- After Phase 3: risks 4, 7 retired.

---

## 5) Resource requirements and dependencies

### Roles
1. **Architect/Lead editor (1):** controls decomposition boundaries and wiring correctness.
2. **Verification reviewer (1):** independently runs fidelity and regression checks.
3. **Optional QA support (1):** assists with E2E behavior parity checks.

### Tooling and dependency plan
1. **Template architecture dependency:** `.claude/skills/sc-adversarial-protocol/` (reference pattern only).
2. **Policy dependency:** `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`.
3. **Verification dependency:** fidelity index file availability.
4. **Runtime dependency:** `rf-task-builder` must resolve relative refs paths.
5. **Downstream compatibility dependency:** `/task` skill remains unaffected.
6. **Build/process dependency:** `make sync-dev`, `make verify-sync`.

### Gated dependency order
- Gate D1: Fidelity index exists before Phase 1.
- Gate D2: `refs/` files complete before `SKILL.md` cross-reference rewiring.
- Gate D3: Sync verification before release finalization.

---

## 6) Success criteria and validation approach

### Requirement-level validation matrix
1. **FR-PRD-R.1:** `SKILL.md` line count 430–500; required sections present; moved sections absent.
2. **FR-PRD-R.2:** `refs/agent-prompts.md` exists; 8 prompts + headers + topic list; zero-content-change diffs.
3. **FR-PRD-R.3:** `refs/validation-checklists.md` exists; required blocks and notes retained; zero-content-change diffs.
4. **FR-PRD-R.4:** `refs/synthesis-mapping.md` exists; output structure + 9-row map retained.
5. **FR-PRD-R.5:** `refs/build-request-template.md` exists; only documented path changes present.
6. **FR-PRD-R.6:** A.7 loading declaration is explicit and scoped correctly.
7. **FR-PRD-R.7:** all original instructional content accounted for; combined lines 1,370–1,400.

### Non-functional validation
1. **NFR-PRD-R.1:** Estimate invocation tokens from final `SKILL.md`; record margin/risk if >2,000 estimate.
2. **NFR-PRD-R.2:** Verify max refs loaded concurrently by orchestrator ≤2.
3. **NFR-PRD-R.3:** Session start cost unchanged (frontmatter/name/description behavior preserved).
4. **NFR-PRD-R.4:** E2E run confirms identical stage behavior and output placement.

### Evidence artifacts
- Fidelity index with block mappings.
- Diff logs per moved block family.
- Grep outputs for stale refs and A.7 declarations.
- E2E execution transcript and output structure comparison.

---

## 7) Timeline estimates per phase

1. **Phase 0 — Baseline/control:** 0.5 day  
2. **Phase 1 — refs creation:** 1.0–1.5 days  
3. **Phase 2 — SKILL refactor + wiring:** 0.5–1.0 day  
4. **Phase 3 — fidelity + regression validation:** 1.0 day  
5. **Phase 4 — release/rollback packaging:** 0.5 day  

**Total estimated duration:** **3.5–4.5 working days**

---

## 8) Open-question resolutions required before final sign-off

1. **Token ceiling precedence (Open Q1):** confirm whether 500-line cap or <=2,000 token target is authoritative when in conflict.  
2. **B30 naming inconsistency (Open Q2):** explicitly accept coexistence of naming conventions in merged table.  
3. **Fidelity index prerequisite (Open Q3):** confirm whether index creation is in-scope if absent.  
4. **Whitespace normalization scope (Open Q4):** define allowed normalization boundaries for acceptance diffs.
