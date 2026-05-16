# Phase 5 -- Synthesis: Ranked Feature Transfer Manifest

**Phase Goal:** Convert the Phase 4 per-feature verdicts into a single, ordered feature transfer manifest that drives the merge. Resolve inter-feature dependencies, lock the integration sketch for every ADOPT feature, define the explicit modification for every ADAPT feature, and define the re-enabling precondition for every DEFER feature. Produce the binding `transfer-manifest.md` and the terminal `rejected-features-ledger.md`.

**Compliance Tier:** STANDARD (synthesis produces the binding manifest).

---

### T05.01 — Merge verdicts & reconcile inter-feature dependencies

**Roadmap Item IDs**: R-016
**Tier**: STANDARD
**Effort**: M
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary for evidence re-resolution. Sequential — recommended (`/sc:adversarial --depth deep` merge patterns).

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/feature-dependency-matrix.md`

**Deliverables:**
- `feature-dependency-matrix.md` — every inter-feature dependency surfaced: features where an ADOPT depends on a DEFER, or where ADOPT(A) implies REJECT(B), with an explicit precedence resolution per conflict.

**Steps:**
1. **[PLANNING]** Load `stack-rank.md` and all nine `debate-*.md` files from Phase 4.
2. **[EXECUTION]** Use `/sc:adversarial --depth deep` merge patterns to scan for inter-feature dependencies: an ADOPT feature that requires a DEFER or REJECT feature to function; two ADOPT features that conflict; an ADAPT whose modification depends on another feature's verdict.
3. **[EXECUTION]** For every conflict, resolve with explicit precedence — state which feature wins, why, and what happens to the loser (e.g., DEFER precondition tightened, or the dependent ADOPT downgraded to DEFER).
4. **[EXECUTION]** Confirm no resolution silently re-litigates a Phase 4 verdict; any verdict change requires an explicit re-debate note (R-RULE-11).
5. **[VERIFICATION]** Confirm every dependency and conflict has a precedence resolution.
6. **[COMPLETION]** Write `feature-dependency-matrix.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `feature-dependency-matrix.md` exists and lists every inter-feature dependency and conflict from the Phase 4 verdict set.
2. Every conflict has an explicit precedence resolution naming winner, rationale, and consequence for the loser.
3. No Phase 4 verdict is silently changed; any change carries an explicit re-debate note (R-RULE-11).

**Validation:**
1. Manual check: reviewer confirms each ADOPT feature's dependencies are either also ADOPT or have a resolved precedence.
2. Manual check: reviewer confirms no silent re-litigation.

**Dependencies**: T04.06 (Phase 4 checkpoint passed)

---

### T05.02 — Lock integration sketches, ADAPT modifications, DEFER preconditions

**Roadmap Item IDs**: R-017
**Tier**: STANDARD
**Effort**: L
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary. Sequential — recommended.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/integration-sketches.md`

**Deliverables:**
- `integration-sketches.md` — for each ADOPT feature: the locked integration sketch (exact extension point, shape of change, new fields/hooks introduced, observable post-condition). For each ADAPT feature: the explicit modification (what changes vs the donor, what is dropped, what is retained). For each DEFER feature: the precondition that would re-enable it.

**Steps:**
1. **[PLANNING]** Load `stack-rank.md`, `feature-dependency-matrix.md`, and `extension-point-contracts.md` (Phase 3).
2. **[EXECUTION]** For each ADOPT feature, lock the integration sketch: name the exact extension point (from `extension-point-contracts.md`), the shape of change, any new MDTM frontmatter field or hook introduced, and the observable post-condition.
3. **[EXECUTION]** For each ADAPT feature, define the explicit modification: what changes versus the donor implementation, what donor ceremony is dropped (R-RULE-06), what control pattern is retained.
4. **[EXECUTION]** For each DEFER feature, define the named precondition that would re-enable it (e.g., "after MDTM frontmatter gains a `tier:` field").
5. **[EXECUTION]** Confirm every ADOPT sketch respects the admit criteria of its target extension point and breaks no INV-NN.
6. **[VERIFICATION]** Confirm every ADOPT/ADAPT/DEFER feature has its respective locked detail.
7. **[COMPLETION]** Write `integration-sketches.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `integration-sketches.md` exists with a locked integration sketch for every ADOPT feature (extension point, shape of change, new fields/hooks, observable post-condition).
2. Every ADAPT feature has an explicit modification spec naming what changes, what is dropped, what is retained.
3. Every DEFER feature has a named re-enabling precondition.
4. Every ADOPT sketch respects its target extension point's admit criteria and breaks no INV-NN.

**Validation:**
1. Manual check: reviewer confirms each ADOPT sketch maps to a real extension point and its admit criteria.
2. Manual check: reviewer confirms ADAPT specs explicitly drop donor ceremony per R-RULE-06.

**Dependencies**: T05.01

---

### T05.03 — Produce `transfer-manifest.md` and `rejected-features-ledger.md`

**Roadmap Item IDs**: R-018
**Tier**: STANDARD
**Effort**: L
**MCP Requirements**: auggie MCP optional. Sequential — recommended.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/transfer-manifest.md`
- `TASKLIST_ROOT/artifacts/rejected-features-ledger.md`

**Deliverables:**
- `transfer-manifest.md` — the ordered, locked manifest (the binding output of this sprint): every ADOPT and ADAPT feature in execution order, each with its integration sketch / modification, dependencies, and observable post-condition. Any subjective override carries an explicit "manifest exception" entry with named justification.
- `rejected-features-ledger.md` — every REJECT and DEFER feature with terminal rationale, so they are not silently re-proposed.

**Steps:**
1. **[PLANNING]** Load `stack-rank.md`, `feature-dependency-matrix.md`, and `integration-sketches.md`.
2. **[EXECUTION]** Build `transfer-manifest.md`: ADOPT and ADAPT features in execution order (respecting the dependency matrix), each with integration sketch / modification spec, dependencies, observable post-condition.
3. **[EXECUTION]** Apply the "absorb patterns, not implementation mass" principle (R-RULE-06) — the manifest records control patterns to extract, not donor ceremony to copy.
4. **[EXECUTION]** Record any subjective override as a "manifest exception" entry with a named justification (R-RULE-07).
5. **[EXECUTION]** Build `rejected-features-ledger.md`: every REJECT feature with terminal rationale; every DEFER feature with its precondition. This ledger is terminal — Phase 6/7 may not silently re-propose its entries (R-RULE-11).
6. **[VERIFICATION]** Confirm every Phase 4 feature appears in exactly one of the two documents; confirm execution order honors the dependency matrix.
7. **[COMPLETION]** Write both files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `transfer-manifest.md` exists, lists every ADOPT/ADAPT feature in dependency-respecting execution order, each with sketch/modification, dependencies, and observable post-condition.
2. `rejected-features-ledger.md` exists, lists every REJECT (terminal rationale) and DEFER (precondition) feature.
3. Every Phase 4 donor feature appears in exactly one of the two documents — no orphans, no duplicates.
4. Any subjective override is recorded as a "manifest exception" with named justification (R-RULE-07).

**Validation:**
1. Manual check: reviewer confirms 1:1 partition of all donor features across the two documents.
2. Manual check: reviewer confirms the manifest's execution order does not violate the dependency matrix.

**Dependencies**: T05.02

---

### T05.04 — Checkpoint: End of Phase 5

**Roadmap Item IDs**: R-016, R-017, R-018
**Tier**: LIGHT
**Effort**: XS
**MCP Requirements**: None

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P05-END.md`

**Purpose:** Confirm the binding transfer manifest and terminal rejected-features ledger are complete and consistent before the Phase 6 merge plan.

**Checkpoint Table:**

| Acceptance Criterion | Source Task | Verification | Status |
|---|---|---|---|
| `feature-dependency-matrix.md` resolves every inter-feature conflict with explicit precedence | T05.01 | All conflicts have a resolution | TBD |
| `integration-sketches.md` has locked detail for every ADOPT/ADAPT/DEFER feature | T05.02 | 1:1 coverage with verdicts | TBD |
| `transfer-manifest.md` lists ADOPT/ADAPT in dependency-respecting order | T05.03 | Order honors dependency matrix | TBD |
| `rejected-features-ledger.md` lists every REJECT/DEFER with rationale/precondition | T05.03 | 1:1 coverage of REJECT/DEFER | TBD |
| Every donor feature appears in exactly one of manifest/ledger | T05.03 | 1:1 partition confirmed | TBD |

**Steps:**
1. **[VERIFICATION]** Confirm all four Phase 5 artifacts exist under `TASKLIST_ROOT/artifacts/`.
2. **[VERIFICATION]** Confirm the manifest/ledger partition covers every donor feature exactly once.
3. **[VERIFICATION]** Write `CP-P05-END.md` with the checkpoint table and `Overall:` status.

**Acceptance Criteria:**
1. `CP-P05-END.md` exists and contains `Overall: Pass`.
2. All five checkpoint-table rows are marked Pass.
3. Report confirms Phase 6 has the binding manifest as its driving input.

**Validation:**
1. Manual check: reviewer confirms the checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P05-END.md`.

**Dependencies**: T05.01, T05.02, T05.03
