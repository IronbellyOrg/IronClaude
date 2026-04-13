---
spec_source: "tdd-refactor-spec.md"
complexity_score: 0.53
primary_persona: architect
---

## 1) Executive Summary

This roadmap delivers a **behavior-preserving decomposition** of the TDD skill into a lean orchestration `SKILL.md` plus phase-loaded `refs/` files, while enforcing strict fidelity and phase-loading contracts.

### Strategic goals
1. Achieve **structural separation of concerns** (protocol vs. payload) to satisfy **FR-TDD-R.1** and **NFR-TDD-R.1/NFR-TDD-R.4**.
2. Execute **verbatim content migration** with controlled allowlisted path rewrites only (**FR-TDD-R.2–FR-TDD-R.5, FR-TDD-R.8, FR-TDD-R.7, NFR-TDD-R.2**).
3. Enforce **deterministic loading discipline** and no forbidden loads (**FR-TDD-R.6, NFR-TDD-R.3**).
4. Close with measurable gates across sync, parity, fidelity, and behavioral invariants (14 success criteria).

### Architecture priorities (architect lens)
- **Contract-first sequencing**: establish loading/wiring contracts before migration to avoid latent integration defects.
- **Fidelity as a release gate**: content drift is treated as a blocking defect.
- **Single source of truth discipline**: canonical edits in `src/superclaude/skills/tdd/` only; sync/verify as mandatory checkpoints.
- **Ambiguity burn-down early**: resolve OQ-1/2/5 before migration to prevent rework and invalid line mapping.

---

## 2) Phased Implementation Plan with Milestones

## Phase 0 — Discovery, Contract Baseline, and Ambiguity Resolution
**Objective:** eliminate mapping ambiguity before any refactor.

### Scope
- Validate source anchoring to **1,364 lines** and reconcile with prompt-cited 1,387 (OQ-1).
- Confirm boundary integrity between:
  - validation checklists: lines 1106–1245
  - operational guidance: lines 1246–1364 (OQ-2)
- Resolve unmapped segment disposition (lines 493–536; OQ-5).
- Confirm frontmatter inclusion in fidelity inventory (OQ-4).

### Deliverables / Milestones
1. **M0.1**: Ratified line-range map for all migrated blocks.
2. **M0.2**: Approved transformation allowlist baseline (Section 12.2 references).
3. **M0.3**: Phase contract matrix baseline for declared/forbidden loads.

### Requirements covered
- Enables correct execution of **FR-TDD-R.2–FR-TDD-R.8**, **FR-TDD-R.7**, **NFR-TDD-R.2**.

---

## Phase 1 — Refs Artifact Creation (Verbatim Payload Extraction)
**Objective:** create all target refs files in canonical source tree.

### Scope
- Implement:
  - `refs/agent-prompts.md` (**FR-TDD-R.2**)
  - `refs/synthesis-mapping.md` (**FR-TDD-R.4**)
  - `refs/validation-checklists.md` (**FR-TDD-R.3**)
  - `refs/build-request-template.md` (**FR-TDD-R.5**, with allowlisted path updates only)
  - `refs/operational-guidance.md` (**FR-TDD-R.8**)

### Milestones
1. **M1.1**: 5/5 canonical refs files exist with expected section boundaries.
2. **M1.2**: Path-reference updates restricted to allowlist in build-request template.
3. **M1.3**: Initial content checksum markers prepared for fidelity index integration.

### Requirements covered
- **FR-TDD-R.2, FR-TDD-R.3, FR-TDD-R.4, FR-TDD-R.5, FR-TDD-R.8**
- Supports **NFR-TDD-R.2, NFR-TDD-R.4**

---

## Phase 2 — SKILL.md Decomposition and Load-Contract Encoding
**Objective:** reduce `SKILL.md` to protocol-only orchestration under hard line budget.

### Scope
- Preserve frontmatter, metadata comment, Purpose/Input/Tier, Stage A/B, boundaries, explicit load declarations.
- Remove HOW payload from `SKILL.md`; retain behavior and interface.
- Encode phase declarations and forbidden-load constraints.

### Milestones
1. **M2.1**: `SKILL.md` under 500 lines (**FR-TDD-R.1a**).
2. **M2.2**: Stage A/B parity and interface invariants preserved (**FR-TDD-R.1c, FR-TDD-R.1d**).
3. **M2.3**: Explicit per-phase loading declarations complete (**FR-TDD-R.1e, FR-TDD-R.6a/6b/6c/6d**).

### Requirements covered
- **FR-TDD-R.1, FR-TDD-R.6**
- **NFR-TDD-R.1, NFR-TDD-R.3**

---

## Phase 3 — Integration, Sync, and Contract Validation
**Objective:** verify canonical-to-dev propagation and runtime reference integrity.

### Scope
- Run `make sync-dev` and validate `.claude` mirrors.
- Run `make verify-sync`.
- Validate BUILD_REQUEST cross-reference resolution and phase contract conformance.

### Milestones
1. **M3.1**: Dev refs files present 5/5 after sync.
2. **M3.2**: `make verify-sync` passes with zero drift.
3. **M3.3**: Contract validation passes:
   - `declared_loads ∩ forbidden_loads = ∅`
   - `runtime_loaded_refs ⊆ declared_loads`

### Requirements covered
- **FR-TDD-R.2b, FR-TDD-R.3b, FR-TDD-R.4b, FR-TDD-R.5b, FR-TDD-R.8b, FR-TDD-R.6**
- **NFR-TDD-R.3**

---

## Phase 4 — Fidelity Certification and Release Readiness
**Objective:** prove zero content loss and zero semantic drift.

### Scope
- Complete fidelity index coverage for lines 1–1364.
- Run normalized diff policy checks.
- Validate forbidden transformation constraints.
- Ensure no sentinels/placeholders remain.
- Perform behavior parity dry run of Stage A/B semantics and `/task` delegation.

### Milestones
1. **M4.1**: Fidelity index 100% mapped with checksum markers.
2. **M4.2**: Verbatim diff checks pass (except allowed normalization and allowlisted rewrites).
3. **M4.3**: Success criteria closure report (all 14 criteria).

### Requirements covered
- **FR-TDD-R.7a–7f**
- **NFR-TDD-R.2**
- Success Criteria #1–#14

---

## 3) Integration Points (Explicit Wiring/Dispatch Mechanisms)

## IP-1: Phase Load Contract Matrix
- **Named Artifact:** `Phase Contract Matrix` (declared/forbidden refs per phase; spec Section 5.3 reference)
- **Wired Components:**
  - Stage A.7 orchestrator load: `refs/build-request-template.md`
  - Builder loads: `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md`
- **Owning Phase:** Phase 2 (definition in `SKILL.md` + contract encoding)
- **Cross-Reference:** Consumed in Phase 3 (contract conformance audit) and Phase 4 (final certification)

## IP-2: BUILD_REQUEST Cross-Reference Map
- **Named Artifact:** `BUILD_REQUEST SKILL CONTEXT Cross-Reference Map` (allowlisted path rewrites)
- **Wired Components:**
  - Agent Prompt Templates → `refs/agent-prompts.md`
  - Synthesis Mapping Table → `refs/synthesis-mapping.md`
  - Synthesis Quality Review Checklist / Assembly Process / Validation Checklist / Content Rules → `refs/validation-checklists.md`
  - Tier Selection remains in `SKILL.md`
- **Owning Phase:** Phase 1 (template migration + rewrites)
- **Cross-Reference:** Consumed in Phase 3 (reference resolution checks) and Phase 4 (allowlist compliance gate)

## IP-3: Stage B Delegation Wiring
- **Named Artifact:** `Stage B /task Delegation Interface` (behavioral contract retained in `SKILL.md`)
- **Wired Components:**
  - Orchestrator stage semantics
  - `/task` skill runtime invocation path
  - `rf-task-builder` consumption of BUILD_REQUEST + refs context
- **Owning Phase:** Phase 2 (behavioral protocol preservation)
- **Cross-Reference:** Consumed in Phase 4 (functional parity dry run; success criterion #13)

## IP-4: Canonical→Dev Sync Registry
- **Named Artifact:** `sync-dev / verify-sync pipeline`
- **Wired Components:**
  - Canonical artifacts in `src/superclaude/skills/tdd/refs/*`
  - Dev mirror artifacts in `.claude/skills/tdd/refs/*`
- **Owning Phase:** Phase 3
- **Cross-Reference:** Consumed in Phase 4 (release-readiness evidence pack)

---

## 4) Risk Assessment and Mitigation Strategies

1. **Content loss during decomposition (HIGH)**  
   - Mitigation:
     - Mandatory fidelity index coverage (1–1364) with first/last-10-word markers.
     - Block-wise diff checks as release gate.
   - Owner: QA/reviewer in Phase 4.

2. **BUILD_REQUEST cross-reference breakage (HIGH)**  
   - Mitigation:
     - Closed allowlist for path rewrites.
     - Reference resolution test against file existence + grep validation.
   - Owner: implementation lead in Phase 1; validated Phase 3.

3. **Wrong loading order / missing refs at runtime (MEDIUM)**  
   - Mitigation:
     - Explicit phase contract declarations in `SKILL.md`.
     - Contract invariants enforced in audit checks.
   - Owner: architect + reviewer in Phase 2/3.

4. **Semantic drift in checklists/quality gates (HIGH)**  
   - Mitigation:
     - No renumbering/no reorder/no header rename rule.
     - Structural diff validation for checklist/table schemas.
   - Owner: QA in Phase 4.

5. **Line-count discrepancy creates mapping errors (MEDIUM)**  
   - Mitigation:
     - Resolve OQ-1 before migration.
     - Treat unresolved mapping ambiguity as blocker at Phase 0 exit.
   - Owner: architect/spec steward.

---

## 5) Resource Requirements and Dependencies

### Roles
- **Architect/Lead:** contract design, phase sequencing, risk governance.
- **Implementation engineer:** verbatim extraction/migration and `SKILL.md` decomposition.
- **QA/reviewer:** fidelity checks, contract audit, parity validation.
- **Optional toolsmith:** automate diff/checksum/sentinel scanning.

### Tooling dependencies (from extraction)
1. `make sync-dev`
2. `make verify-sync`
3. `/task` runtime dependency
4. `rf-task-builder`
5. Developer Guide sections 5.6/9.3/9.7 (refs pattern authority)
6. `sc-adversarial-protocol/refs/` pattern reference
7. `.dev/releases/backlog/tdd-skill-refactor/fidelity-index.md`

### Architectural constraints to enforce
- Canonical edits only in `src/superclaude/`.
- No behavior/interface changes.
- Strict `<500` lines for `SKILL.md`.
- Allowlisted transform policy only.

---

## 6) Success Criteria and Validation Approach

Validation is executed as **gated checkpoints**, not advisory checks.

### Gate A — Structural completeness
- Verify criteria #1, #2, #3 (line budget + 5/5 refs in canonical/dev).

### Gate B — Sync and contract integrity
- Verify criteria #4, #9, #10 (`verify-sync`, phase contracts, reference resolution).

### Gate C — Fidelity and semantic immutability
- Verify criteria #5, #6, #7, #8, #11, #12 (index coverage, drift policy, allowlist-only, sentinel-free, prompt/checklist integrity).

### Gate D — Runtime behavioral parity
- Verify criteria #13, #14 (Stage A/B parity + token footprint reduction).

### Requirement traceability matrix (high level)
- **FR-TDD-R.1 / FR-TDD-R.6** → Phase 2 + Gate B/D  
- **FR-TDD-R.2/3/4/5/8** → Phase 1 + Gate A/C  
- **FR-TDD-R.7** → Phase 4 + Gate C  
- **NFR-TDD-R.1/2/3/4** → Gate D/C/B/C respectively

---

## 7) Timeline Estimates per Phase

Given **MEDIUM complexity (0.53)** and high fidelity rigor:

1. **Phase 0 (Discovery/ambiguity burn-down):** 0.5–1 day  
2. **Phase 1 (Refs extraction/migration):** 1–1.5 days  
3. **Phase 2 (SKILL.md decomposition + contract encoding):** 0.5–1 day  
4. **Phase 3 (Sync/integration/contract validation):** 0.5 day  
5. **Phase 4 (Fidelity certification + parity validation):** 1 day  

**Total estimated implementation window:** **3.5–5 days** (including validation hardening and rework buffer for OQ-driven corrections).

---

## 8) Open-Question Closure Plan (Execution Prerequisite)

Before Phase 1 starts, formally resolve:

1. **OQ-1:** authoritative line-range anchor (1,364 vs 1,387).  
2. **OQ-2:** confirm 1246–1364 as complete `operational-guidance` span.  
3. **OQ-5:** assign lines 493–536 to explicit destination(s).  
4. **OQ-4:** ensure frontmatter is represented in fidelity accounting.

**Go/No-Go rule:** if any of OQ-1/2/5 remains unresolved, do not proceed past Phase 0.
