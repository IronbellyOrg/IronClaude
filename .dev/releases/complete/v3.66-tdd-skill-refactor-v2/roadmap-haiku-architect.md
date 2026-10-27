---
spec_source: "tdd-command-layer-spec.md"
complexity_score: 0.25
primary_persona: architect
---

## 1) Executive Summary

This is a **low-complexity architectural refactor** to restore three-tier separation (Command → Skill → refs/) without behavioral change.  
Primary objective: implement a thin `/sc:tdd` command layer and migrate interface-only content out of `SKILL.md` while preserving execution protocol integrity.

**Architectural priorities:**
1. Enforce strict layer boundaries (FR-TDD-CMD.1m, NFR-TDD-CMD.2).
2. Preserve behavior exactly (FR-TDD-CMD.3d, FR-TDD-CMD.3e, NFR-TDD-CMD.5).
3. Maintain source-of-truth and sync guarantees (Architectural Constraints #2 and #7; SC-12).

---

## 2) Phased Implementation Plan with Milestones

### Phase 0 — Baseline & Control Setup
**Goals**
- Freeze current baseline for precise migration/fidelity checks.
- Confirm template and scope boundaries before edits.

**Tasks**
1. Read/lock references:
   - `src/superclaude/commands/adversarial.md` (gold template)
   - `src/superclaude/skills/tdd/SKILL.md` (migration source/target)
   - `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`
2. Capture pre-migration snapshots for:
   - SKILL behavioral sections (Stage A/B, critical rules, session management) → for FR-TDD-CMD.3d/NFR-TDD-CMD.5
   - SKILL loading declarations + phase loading contract → for FR-TDD-CMD.3e
   - refs/ files checksums → for FR-TDD-CMD.3f

**Milestone M0**
- Baseline evidence set exists and is reviewable.

**Requirement coverage**
- FR-TDD-CMD.3d, FR-TDD-CMD.3e, FR-TDD-CMD.3f, NFR-TDD-CMD.5

---

### Phase 1 — Thin Command Layer Creation
**Goals**
- Create canonical command file and dev copy with strict thin-layer structure.

**Tasks**
1. Create `src/superclaude/commands/tdd.md` and sync copy `.claude/commands/sc/tdd.md` (FR-TDD-CMD.1a).
2. Implement command sections and constraints:
   - Frontmatter (FR-TDD-CMD.1b)
   - Required Input (FR-TDD-CMD.1c)
   - Usage (FR-TDD-CMD.1d)
   - Arguments (FR-TDD-CMD.1e)
   - Options with all 7 flags (FR-TDD-CMD.1f)
   - Behavioral Summary (FR-TDD-CMD.1g)
   - Examples (FR-TDD-CMD.1h)
   - Activation with guard language (FR-TDD-CMD.1i)
   - Boundaries (FR-TDD-CMD.1j)
   - Related commands table (FR-TDD-CMD.1k)
3. Enforce line budget and no protocol leakage:
   - FR-TDD-CMD.1l, FR-TDD-CMD.1m
   - NFR-TDD-CMD.1, NFR-TDD-CMD.2, NFR-TDD-CMD.4

**Milestone M1**
- `/sc:tdd` command file complete, thin, and structurally compliant.

**Requirement coverage**
- FR-TDD-CMD.1a–1m, NFR-TDD-CMD.1, NFR-TDD-CMD.2, NFR-TDD-CMD.4

---

### Phase 2 — Content Migration & Layer Cleanup
**Goals**
- Move interface content from SKILL to command; retain only protocol-relevant skill content.

**Tasks**
1. Migrate prompt examples from SKILL lines 48–63 into command examples (FR-TDD-CMD.2a).
2. Migrate tier table from SKILL lines 82–88 into command options (`--tier`) (FR-TDD-CMD.2b).
3. Retain mandated SKILL content:
   - 4-input description + incomplete prompt template (FR-TDD-CMD.2c)
   - tier intro + selection rules, but not full table (FR-TDD-CMD.2d)
4. Remove duplication between command and SKILL (FR-TDD-CMD.2e).
5. Maintain SKILL line budget 400–440 (FR-TDD-CMD.2f, NFR-TDD-CMD.3).

**Milestone M2**
- Migration complete with clean command/skill responsibility split.

**Requirement coverage**
- FR-TDD-CMD.2a–2f, NFR-TDD-CMD.3

---

### Phase 3 — Fidelity Verification & Regression Gates
**Goals**
- Prove migration correctness and zero behavioral regression.

**Tasks**
1. Verify example fidelity:
   - 3 strong examples present (FR-TDD-CMD.3a)
   - 2 weak examples present and annotated (FR-TDD-CMD.3b)
2. Verify tier table rows in command (FR-TDD-CMD.3c).
3. Verify no SKILL behavioral or loading declaration changes (FR-TDD-CMD.3d, FR-TDD-CMD.3e, NFR-TDD-CMD.5).
4. Verify refs files untouched (FR-TDD-CMD.3f).
5. Validate zero leakage and activation correctness (NFR-TDD-CMD.2, NFR-TDD-CMD.4).

**Milestone M3**
- All fidelity gates pass; no collateral edits.

**Requirement coverage**
- FR-TDD-CMD.3a–3f, NFR-TDD-CMD.2, NFR-TDD-CMD.4, NFR-TDD-CMD.5

---

### Phase 4 — Sync, Audit, and Release Readiness
**Goals**
- Ensure canonical/dev parity and completion against measurable success criteria.

**Tasks**
1. Run component sync pipeline (`make sync-dev`, `make verify-sync`) (SC-12).
2. Execute full structural validation (SC-1..SC-11).
3. Produce short evidence report mapping SC and FR/NFR to checks.

**Milestone M4**
- Release-ready refactor with traceable compliance evidence.

---

## 3) Integration Points (Explicit Wiring Mechanisms)

1. **Named Artifact:** Activation Handoff (`## Activation` + `> Skill tdd`)  
   - **Wired Components:** `.claude/commands/sc/tdd.md` → `.claude/skills/tdd/SKILL.md`  
   - **Owning Phase:** Phase 1  
   - **Cross-Reference:** Consumed in Phase 3 (NFR-TDD-CMD.4 verification)

2. **Named Artifact:** Component Sync Pipeline (`make sync-dev` + `make verify-sync`)  
   - **Wired Components:** `src/superclaude/commands/tdd.md` ↔ `.claude/commands/sc/tdd.md`; related skill file parity  
   - **Owning Phase:** Phase 4  
   - **Cross-Reference:** Consumed by all prior phases as release gate (SC-1, SC-12)

3. **Named Artifact:** Related Commands Interface Table (`/sc:prd`, `/sc:design`, `/sc:workflow`, `/sc:brainstorm`)  
   - **Wired Components:** tdd command discoverability links to adjacent command interfaces  
   - **Owning Phase:** Phase 1  
   - **Cross-Reference:** Consumed in user-facing command navigation after release

---

## 4) Risk Assessment and Mitigation Strategies

1. **RISK-01: Content loss during migration (Low)**
   - Mitigation: block-level moves + post-move diff checks on migrated ranges.
   - Gate: FR-TDD-CMD.3a/3b/3c + SC-6/SC-7/SC-8.

2. **RISK-02: Protocol leakage into command (Medium)**
   - Mitigation: prohibit Stage/agent terms in command; enforce grep zero-match gate.
   - Gate: FR-TDD-CMD.1m + NFR-TDD-CMD.2 + SC-5.

3. **RISK-03: Scope creep into skill improvements (Medium)**
   - Mitigation: explicit “no behavior changes” acceptance gate.
   - Gate: FR-TDD-CMD.3d/3e/3f + NFR-TDD-CMD.5 + SC-10/SC-11.

4. **RISK-04: Sync failure / wrong source edited (Low)**
   - Mitigation: canonical-first edits under `src/superclaude/`; mandatory sync verification.
   - Gate: FR-TDD-CMD.1a + SC-1 + SC-12.

5. **RISK-05: Example context degradation (Low)**
   - Mitigation: preserve semantic intent while adapting syntax to `/sc:tdd`.
   - Gate: FR-TDD-CMD.3a/3b + SC-6.

---

## 5) Resource Requirements and Dependencies

### Team / Roles
1. **Architect/maintainer (primary):** owns phase sequencing, boundary enforcement.
2. **Reviewer (secondary):** performs fidelity and regression checks.
3. **CI/automation:** runs grep/wc/diff/make sync verification gates.

### Dependency Plan
**Internal dependencies**
1. `commands/sc/adversarial.md` (template source)
2. `skills/tdd/SKILL.md` (migration source)
3. `make sync-dev` / `make verify-sync` (parity enforcement)
4. Developer Guide architecture rules (authoritative constraints)

**External dependencies**
- None (explicitly zero).

---

## 6) Success Criteria and Validation Approach

### Validation Matrix (SC-1 to SC-12)
1. **SC-1:** file presence at canonical + dev paths.
2. **SC-2:** command line count 100–170.
3. **SC-3:** all 7 flags present in options.
4. **SC-4:** activation contains `Skill tdd`.
5. **SC-5:** zero protocol leakage keywords.
6. **SC-6:** 3 strong + 2 weak examples in command.
7. **SC-7:** tier rows Lightweight/Standard/Heavyweight present.
8. **SC-8:** migrated example strings removed from SKILL.
9. **SC-9:** SKILL line count 400–440.
10. **SC-10:** behavioral protocol sections unchanged.
11. **SC-11:** refs/ files unchanged.
12. **SC-12:** `make verify-sync` passes.

### Traceability Rule
- Every phase closes with explicit FR/NFR/SC mapping before progressing.

---

## 7) Timeline Estimates per Phase

Given **LOW complexity (0.25)** and no external dependencies:

1. **Phase 0 (Baseline):** 0.25 day  
2. **Phase 1 (Command creation):** 0.5 day  
3. **Phase 2 (Migration):** 0.5 day  
4. **Phase 3 (Fidelity verification):** 0.5 day  
5. **Phase 4 (Sync + release readiness):** 0.25 day  

**Total estimate:** ~2.0 working days.

### Milestone cadence
- **Day 1:** M0 + M1  
- **Day 2:** M2 + M3 + M4

---

## 8) Open Questions Handling

- Extraction indicates no open questions; treat scope as fully specified.
- Any newly discovered ambiguity should be logged as a change request, not solved by in-scope expansion (protects FR-TDD-CMD.3d-f and NFR-TDD-CMD.5).
