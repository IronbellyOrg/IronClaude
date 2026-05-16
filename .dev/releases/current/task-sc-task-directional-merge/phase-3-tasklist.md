# Phase 3 -- Recipient Integration Surface & Invariant Bound

**Phase Goal:** For each load-bearing invariant of `/task` (INV-01..INV-05), produce a precise, testable definition the Phase 4 adversarial debate can use as a hard constraint. Also produce the extension-point contract for each Phase 1 extension point — what shape of donor feature it can absorb and what it cannot — and analyze the `task-builder` adjacent surface so work-definition transfers route correctly.

**Compliance Tier:** EXEMPT (read-only invariant extraction).

---

### T03.01 — Define invariant bounds INV-01..INV-05

**Roadmap Item IDs**: R-008
**Tier**: EXEMPT
**Effort**: M
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary, using `/sc:analyze --focus architecture` patterns on `/task`.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/invariant-bounds.md`

**Deliverables:**
- `invariant-bounds.md` — one section per INV-NN. Each section: the behavioral rule (precise, testable), the `file:line` where it is enforced or stated (side-tagged), the failure mode it prevents (with a worked example), and the typology of donor features that would violate it.

**Steps:**
1. **[PLANNING]** Take INV-01..INV-05 from the sprint specification as the section skeleton.
2. **[EXECUTION]** Use auggie MCP to locate the enforcement/statement site for each invariant in `task/SKILL.md` (and `task-builder/SKILL.md` where relevant): INV-01 F1 loop semantics, INV-02 prohibited-actions catalog, INV-03 phase-gate `rf-qa` + post-completion `rf-qa`/`rf-qa-qualitative`, INV-04 resumability from disk, INV-05 refusal-of-definition.
3. **[EXECUTION]** For each invariant write the precise testable rule, the side-tagged `file:line`, the failure mode prevented, and a worked example of that failure.
4. **[EXECUTION]** For each invariant write the *typology* (not enumeration) of donor features that would violate it — the kind of feature, so Phase 4 can pattern-match.
5. **[VERIFICATION]** Confirm all five sections complete with evidence, worked example, and violating typology.
6. **[COMPLETION]** Write `invariant-bounds.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `invariant-bounds.md` exists with one section per INV-01..INV-05.
2. Each section states a precise, testable behavioral rule and cites side-tagged `file:line` enforcement evidence (R-RULE-03, R-RULE-10).
3. Each section includes a worked example of the failure mode the invariant prevents.
4. Each section gives a violating-feature typology usable as a Phase 4 pattern-match.

**Validation:**
1. Manual check: reviewer confirms each invariant's `file:line` resolves to enforcing/stating text.
2. Manual check: reviewer confirms each worked example concretely demonstrates the failure mode.

**Dependencies**: T02.05 (Phase 2 checkpoint passed)

---

### T03.02 — Document extension-point contracts

**Roadmap Item IDs**: R-009
**Tier**: EXEMPT
**Effort**: M
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/extension-point-contracts.md`

**Deliverables:**
- `extension-point-contracts.md` — one row per Phase 1 extension point, each with explicit admit criteria (what shape of donor feature it can absorb) and reject criteria (what it cannot), cross-referenced to the invariant bounds from T03.01.

**Steps:**
1. **[PLANNING]** Take `recipient-extension-points.md` (T01.01) and `invariant-bounds.md` (T03.01) as inputs.
2. **[EXECUTION]** For each extension point, use auggie MCP to confirm its current contract surface, then write admit criteria: the shape of donor feature it can absorb without an F1 change.
3. **[EXECUTION]** For each extension point, write reject criteria: what it cannot absorb, cross-referenced to the specific INV-NN that would be violated.
4. **[EXECUTION]** Mark each extension point with the Complementarity band it maps to (native fit = C5, new field/hook required = C3, requires F1 change = C1) so Phase 4 scoring has a deterministic anchor.
5. **[VERIFICATION]** Confirm every extension point has both admit and reject criteria and an invariant cross-reference.
6. **[COMPLETION]** Write `extension-point-contracts.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `extension-point-contracts.md` exists with one row per Phase 1 extension point.
2. Every row has explicit admit criteria and reject criteria.
3. Every reject criterion cross-references the INV-NN it protects.
4. Every row carries a Complementarity band (C5/C3/C1) to anchor Phase 4 scoring.

**Validation:**
1. Manual check: reviewer confirms 1:1 coverage with `recipient-extension-points.md`.
2. Manual check: reviewer confirms reject criteria cite real INV-NN sections.

**Dependencies**: T03.01

---

### T03.03 — Analyze `task-builder` adjacent surface

**Roadmap Item IDs**: R-010
**Tier**: EXEMPT
**Effort**: S
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/task-builder-adjacency.md`

**Deliverables:**
- `task-builder-adjacency.md` — defines which classes of donor feature affect work-*definition* (and therefore land in `task-builder`) versus work-*execution* (which land in the `/task` executor), with `file:line` evidence for the builder's responsibilities.

**Steps:**
1. **[PLANNING]** Use auggie MCP to locate `task-builder/SKILL.md` on both sides; confirm source of truth per R-RULE-10.
2. **[EXECUTION]** Characterize the builder's responsibilities: what it produces, what MDTM structure it owns, where its boundary with the executor sits.
3. **[EXECUTION]** Define the routing rule: a donor feature that shapes *what* work is defined routes to `task-builder`; a donor feature that shapes *how* work executes routes to the `/task` executor.
4. **[EXECUTION]** Cross-reference INV-05 (refusal-of-definition) — features touching definition must not leak into the executor.
5. **[VERIFICATION]** Confirm the routing rule is unambiguous and evidence-backed.
6. **[COMPLETION]** Write `task-builder-adjacency.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `task-builder-adjacency.md` exists and documents the builder's responsibilities with side-tagged `file:line` evidence.
2. An unambiguous definition-vs-execution routing rule is stated.
3. The routing rule cross-references INV-05.

**Validation:**
1. Manual check: reviewer confirms the routing rule resolves a sample donor feature to exactly one surface.

**Dependencies**: T03.01

---

### T03.04 — Checkpoint: End of Phase 3

**Roadmap Item IDs**: R-008, R-009, R-010
**Tier**: LIGHT
**Effort**: XS
**MCP Requirements**: None

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-END.md`

**Purpose:** Confirm the invariant bounds and extension-point contracts are precise enough to serve as hard constraints in the Phase 4 adversarial debate.

**Checkpoint Table:**

| Acceptance Criterion | Source Task | Verification | Status |
|---|---|---|---|
| `invariant-bounds.md` has one evidenced section per INV-01..INV-05 | T03.01 | Five sections present; spot-check evidence | TBD |
| Each invariant section has a worked failure-mode example | T03.01 | Examples present and concrete | TBD |
| `extension-point-contracts.md` has admit + reject criteria per extension point | T03.02 | 1:1 coverage with Phase 1 inventory | TBD |
| Every reject criterion cross-references an INV-NN | T03.02 | Spot-check cross-references | TBD |
| `task-builder-adjacency.md` states an unambiguous definition-vs-execution routing rule | T03.03 | Rule present, INV-05 cross-referenced | TBD |

**Steps:**
1. **[VERIFICATION]** Confirm all three Phase 3 artifacts exist under `TASKLIST_ROOT/artifacts/`.
2. **[VERIFICATION]** Spot-check invariant evidence resolution and extension-point coverage.
3. **[VERIFICATION]** Write `CP-P03-END.md` with the checkpoint table and `Overall:` status.

**Acceptance Criteria:**
1. `CP-P03-END.md` exists and contains `Overall: Pass`.
2. All five checkpoint-table rows are marked Pass.
3. Report confirms Phase 4 has both its hard-constraint inputs (invariant bounds, extension-point contracts).

**Validation:**
1. Manual check: reviewer confirms the checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P03-END.md`.

**Dependencies**: T03.01, T03.02, T03.03
