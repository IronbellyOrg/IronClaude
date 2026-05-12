---
spec_source: "prd-refactor-spec-v2.md"
complexity_score: 0.45
primary_persona: architect
---

## 1) Executive summary

This is a **medium-complexity structural refactor** focused on enforcing mandated architecture (Command → Skill → refs/agents) with **zero behavioral change**.  
Primary architectural outcomes:

1. Add missing thin command layer (`FR-PRD-R.0`) at `.claude/commands/sc/prd.md`.
2. Reduce monolithic SKILL to behavioral protocol only (`FR-PRD-R.1`, `NFR-PRD-R.1`).
3. Finalize/verify refs decomposition (`FR-PRD-R.2`–`FR-PRD-R.5`) with strict fidelity.
4. Encode per-phase lazy-loading contracts (`FR-PRD-R.6`, `NFR-PRD-R.2`).
5. Pass fidelity/behavioral regression gate before merge (`FR-PRD-R.7`, `NFR-PRD-R.4`).

**Architectural priority order:**  
governance compliance → fidelity preservation → wiring correctness → token/line budgets → sync integrity.

---

## 2) Phased implementation plan with milestones

### Phase 0 — Baseline & governance lock (Sprint Slot 1)
**Goals**
- Freeze source baseline and verification artifacts before edits.
- Confirm constraints from developer guide and source-of-truth workflow.

**Actions**
1. Baseline original `.claude/skills/prd/SKILL.md` and existing refs files.
2. Confirm architectural constraints (500-line ceiling, activation pattern, thin command rule, no behavior change).
3. Prepare/update fidelity map target at `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md` (`FR-PRD-R.7a`).

**Milestone M0**
- Baseline checkpoints documented; acceptance matrix created for `FR-PRD-R.0`–`FR-PRD-R.8`, `NFR-PRD-R.1`–`NFR-PRD-R.5`.

---

### Phase 1 — Command layer creation (Sprint Slot 1)
**Owned requirements**
- `FR-PRD-R.0a`–`FR-PRD-R.0l`
- `FR-PRD-R.8a`, `FR-PRD-R.8b` (destination side)
- `NFR-PRD-R.5`

**Actions**
1. Create `.claude/commands/sc/prd.md` as thin command.
2. Add required sections: Required Input, Usage, Arguments, Options (7 flags), Behavioral Summary, Examples, Activation, Boundaries, Related Commands.
3. Migrate B03 examples and B04 tier table content into command file exactly as required.
4. Ensure **zero protocol logic** in command.

**Milestone M1**
- Command file line budget 100–170 satisfied and activation contract present (`Skill prd`, “Do NOT proceed”).

---

### Phase 2 — SKILL decomposition & refs completion (Sprint Slot 2)
**Owned requirements**
- `FR-PRD-R.1a`–`FR-PRD-R.1f`
- `FR-PRD-R.2a`–`FR-PRD-R.2e`
- `FR-PRD-R.3a`–`FR-PRD-R.3g`
- `FR-PRD-R.4a`–`FR-PRD-R.4e`
- `FR-PRD-R.5a`–`FR-PRD-R.5f`
- `FR-PRD-R.8c`, `FR-PRD-R.8d`, `FR-PRD-R.8e`
- `NFR-PRD-R.1`

**Actions**
1. Trim SKILL.md to behavioral protocol only (400–500 lines).
2. Verify existing refs fidelity for:
   - `refs/agent-prompts.md`
   - `refs/validation-checklists.md`
   - `refs/synthesis-mapping.md`
3. Create/complete `refs/build-request-template.md` from original lines 347–508 with only 6 documented path updates.
4. Merge B30 into B05 within SKILL.md per requirement.
5. Remove duplicated interface content from SKILL.md (examples/table moved to command).

**Milestone M2**
- SKILL.md in bounds, refs complete (exactly 4 `.md` refs), no duplicated content between command and SKILL.

---

### Phase 3 — Integration wiring & loading contracts (Sprint Slot 2)
**Owned requirements**
- `FR-PRD-R.6a`–`FR-PRD-R.6d`
- `NFR-PRD-R.2`
- Activation part of `FR-PRD-R.0h`

**Actions**
1. Encode Stage A.7 loading declarations exactly:
   - Orchestrator: `refs/build-request-template.md`
   - Builder subagent: `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`
2. Ensure no other SKILL phases load refs.
3. Confirm orchestrator max file load remains within 2-file limit.

**Milestone M3**
- Explicit per-phase loading contract validated; runtime wiring is deterministic and bounded.

---

### Phase 4 — Fidelity, regression, and sync gate (Sprint Slot 3)
**Owned requirements**
- `FR-PRD-R.7a`–`FR-PRD-R.7h`
- `NFR-PRD-R.3`, `NFR-PRD-R.4`
- Success criteria 1–12

**Actions**
1. Run block-level diffs for all migrated artifacts.
2. Verify BUILD_REQUEST has only 6 allowed reference-path edits.
3. Verify combined line count target (1380–1520).
4. Execute `/sc:prd` invocation validation and output structure comparison for regression check.
5. Run sync workflow (`make sync-dev`, `make verify-sync`).

**Milestone M4 (Release Gate)**
- Zero content loss, zero semantic drift, zero behavioral regression, sync verification passes.

---

## 3) Risk assessment and mitigation strategies

1. **[HIGH] Content loss during SKILL trimming**  
   - Mitigation: fidelity index + first/last marker checks + per-block diff (`FR-PRD-R.7` gate).
2. **[HIGH] BUILD_REQUEST cross-reference breakage**  
   - Mitigation: enforce exact 6 path remaps only (`FR-PRD-R.5c`, `FR-PRD-R.5f`).
3. **[HIGH] Activation miswire in command**  
   - Mitigation: explicit `## Activation` pattern and manual `/sc:prd` trigger validation (`FR-PRD-R.0h`, success criterion 12).
4. **[MEDIUM] Scope creep during migration**  
   - Mitigation: “move, don’t improve” rule; reject non-required edits in review.
5. **[MEDIUM] Existing refs drift from original**  
   - Mitigation: re-verify refs line-range fidelity before accepting decomposed SKILL.
6. **[MEDIUM] Prompt examples lose context after move**  
   - Mitigation: ensure example framing exists in command Examples section (`FR-PRD-R.0g`).
7. **[MEDIUM] Tier docs/rules divergence**  
   - Mitigation: command holds reference table; SKILL holds decision logic; no duplication (`FR-PRD-R.8d/e`).
8. **[MEDIUM] Builder cannot resolve refs path**  
   - Mitigation: Stage A.7 declarations + integration test for builder subagent read-paths.
9. **[LOW] B30→B05 merge drops QA paths**  
   - Mitigation: explicit row-level verification of 6 specific QA paths (`FR-PRD-R.1f`).

---

## 4) Resource requirements and dependencies

### Team roles
1. **Architect/Tech Lead**: acceptance gates, architecture compliance, risk signoff.
2. **Docs/Skill Engineer**: command + SKILL + refs migration execution.
3. **QA/Validation Engineer**: diff/fidelity/regression/sync verification.

### Dependency plan (from extraction inventory)
1. `.claude/commands/sc/adversarial.md` (template baseline)
2. Original `.claude/skills/prd/SKILL.md` (source truth for migrated content)
3. `.dev/releases/complete/v3.65-prd-refactor/fidelity-index.md` (verification authority)
4. `make sync-dev` (propagation)
5. `make verify-sync` (consistency gate)
6. `/task` skill (Stage B runtime delegation)
7. `rf-task-builder` agent (Stage A.7 runtime dependency)
8. `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (governance authority)

---

## 5) Success criteria and validation approach

### Validation matrix (must pass all)
1. `FR-PRD-R.0` command structure/content/activation/line budget.
2. `FR-PRD-R.1` SKILL decomposition and line budget.
3. `FR-PRD-R.2`–`FR-PRD-R.4` refs fidelity zero-drift.
4. `FR-PRD-R.5` BUILD_REQUEST only-allowed-path-edits.
5. `FR-PRD-R.6` loading declarations and phase boundaries.
6. `FR-PRD-R.7` complete fidelity gate and aggregate line count.
7. `FR-PRD-R.8` migration correctness and non-duplication.
8. `NFR-PRD-R.1`–`NFR-PRD-R.5` token, load, behavior, and line constraints.

### Measurable checks
- `wc -l` for SKILL and command budgets.
- Refs count check = 4 `.md` files.
- Grep checks for stale section references and duplication.
- Line-range diff checks against original source blocks.
- Manual invocation regression: `/sc:prd` activation + output structure parity.
- Sync check: `make verify-sync` pass required before merge.

---

## 6) Timeline estimates per phase

1. **Phase 0 (Sprint Slot 1)**: Baseline and gate setup.  
2. **Phase 1 (Sprint Slot 1)**: Command layer implementation and interface migration.  
3. **Phase 2 (Sprint Slot 2)**: SKILL decomposition + refs completion/fidelity updates.  
4. **Phase 3 (Sprint Slot 2)**: Loading declarations and integration wiring hardening.  
5. **Phase 4 (Sprint Slot 3)**: Full fidelity/regression/sync gate and release readiness.

**Critical path:** Phase 1 → Phase 2 → Phase 3 → Phase 4  
**Parallelizable work:** In Phase 2, refs fidelity checks (`FR-PRD-R.2/3/4`) can run in parallel with SKILL trimming once source baselines are fixed.

---

## Integration points (explicit wiring inventory)

1. **Named Artifact**: `## Activation` handoff in `.claude/commands/sc/prd.md`  
   - **Wired Components**: `/sc:prd` command entrypoint → `Skill prd`  
   - **Owning Phase**: Phase 1  
   - **Cross-Reference**: Consumed in Phase 4 activation correctness/regression validation

2. **Named Artifact**: `Stage A.7 Orchestrator Loading Declaration` in `SKILL.md`  
   - **Wired Components**: Orchestrator context + `refs/build-request-template.md`  
   - **Owning Phase**: Phase 3  
   - **Cross-Reference**: Consumed in Phase 4 (`NFR-PRD-R.2`, `FR-PRD-R.6a/d` checks)

3. **Named Artifact**: `Stage A.7 Builder Subagent Loading Declaration` in `SKILL.md`  
   - **Wired Components**: `rf-task-builder` + `refs/agent-prompts.md` + `refs/synthesis-mapping.md` + `refs/validation-checklists.md`  
   - **Owning Phase**: Phase 3  
   - **Cross-Reference**: Consumed in Phase 4 path-resolution and fidelity/regression checks

4. **Named Artifact**: `Stage B Delegation Contract` in `SKILL.md`  
   - **Wired Components**: PRD skill Stage B → `/task` skill execution  
   - **Owning Phase**: Phase 2 (retained during decomposition), validated in Phase 4  
   - **Cross-Reference**: Consumed by runtime behavior verification (`NFR-PRD-R.4`)

5. **Named Artifact**: `BUILD_REQUEST SKILL CONTEXT FILE references` in `refs/build-request-template.md`  
   - **Wired Components**: BUILD_REQUEST template → refs file paths (6 remapped targets + unchanged Tier Selection reference)  
   - **Owning Phase**: Phase 2  
   - **Cross-Reference**: Consumed in Phase 3 loading validation and Phase 4 diff gate (`FR-PRD-R.5f`, `FR-PRD-R.7e`)
