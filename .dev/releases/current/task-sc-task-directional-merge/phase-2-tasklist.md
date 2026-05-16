# Phase 2 -- Donor Feature Characterization

**Phase Goal:** For every donor feature in the Phase 1 catalog, produce a structured characterization deep enough to debate in Phase 4. Each characterization answers: what it is, how it works, what it produces, what invokes it, what it depends on, its standalone value claim, and its coupling cost claim. Anti-sycophancy is applied throughout — every value claim states the conditions under which it does NOT deliver value.

**Compliance Tier:** EXEMPT (read-only characterization).

---

### T02.01 — Characterize tier classification model & classification header emission

**Roadmap Item IDs**: R-004
**Tier**: EXEMPT
**Effort**: M
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary, using `/sc:analyze --focus architecture` patterns per feature.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/feature-tier-classification.md`
- `TASKLIST_ROOT/artifacts/feature-classification-header.md`

**Deliverables:**
- `feature-tier-classification.md` and `feature-classification-header.md` — each documents: what it is, how it works (mechanism + entry/exit conditions + `file:line` evidence), what it produces, what invokes it, what it depends on, standalone value claim, coupling cost claim.

**Steps:**
1. **[PLANNING]** Pull the tier-classification and classification-header rows from `donor-feature-catalog.md` (T01.02) as the scope anchor.
2. **[EXECUTION]** Use auggie MCP with `/sc:analyze --focus architecture` patterns on the STRICT/STANDARD/LIGHT/EXEMPT classification table in `sc-task-protocol/SKILL.md`; capture mechanism, entry/exit conditions, `file:line` evidence (side-tagged).
3. **[EXECUTION]** Repeat for classification header emission: what header is emitted, when, where it lands, what reads it.
4. **[EXECUTION]** For each feature, write the standalone value claim AND the coupling cost claim; apply anti-sycophancy — state the conditions under which the value claim does NOT hold.
5. **[VERIFICATION]** Confirm both files have all seven characterization fields and at least one non-value condition per value claim.
6. **[COMPLETION]** Write both `feature-*.md` files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `feature-tier-classification.md` and `feature-classification-header.md` both exist with all seven characterization fields populated.
2. Every mechanism claim cites `file:line` evidence with side tag (R-RULE-03, R-RULE-10).
3. Every standalone value claim includes at least one explicit condition under which it does NOT deliver value (R-RULE-04).
4. Every coupling cost claim names concretely what the recipient must take on to support the feature.

**Validation:**
1. Manual check: reviewer confirms all seven fields present in each file.
2. Manual check: reviewer confirms the anti-sycophancy non-value condition is concrete, not boilerplate.

**Dependencies**: T01.04 (Phase 1 checkpoint passed)

---

### T02.02 — Characterize TFEP & per-tier flow branching

**Roadmap Item IDs**: R-005
**Tier**: EXEMPT
**Effort**: M
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary, using `/sc:analyze --focus architecture` patterns.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/feature-tfep.md`
- `TASKLIST_ROOT/artifacts/feature-per-tier-branching.md`

**Deliverables:**
- `feature-tfep.md` and `feature-per-tier-branching.md` — full seven-field characterizations including escalation artifacts and branch conditions.

**Steps:**
1. **[PLANNING]** Pull the TFEP and per-tier-branching rows from `donor-feature-catalog.md`.
2. **[EXECUTION]** Use auggie MCP to characterize TFEP: trigger condition (test failure), the forensic-pipeline it invokes, entry/exit conditions, escalation artifacts produced, `file:line` evidence (side-tagged).
3. **[EXECUTION]** Characterize per-tier flow branching: which classifier branch invokes which flow, the shape of user input that selects each branch, what each branch produces.
4. **[EXECUTION]** For each, write standalone value and coupling cost claims with anti-sycophancy non-value conditions.
5. **[VERIFICATION]** Confirm both files have all seven fields, escalation/branch detail, and non-value conditions.
6. **[COMPLETION]** Write both files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `feature-tfep.md` and `feature-per-tier-branching.md` exist with all seven characterization fields.
2. TFEP characterization names the forensic-pipeline trigger and the escalation artifact it produces, with `file:line` evidence.
3. Per-tier branching characterization maps each classifier branch to its flow and the user-input shape that selects it.
4. Each value claim carries an explicit non-value condition (R-RULE-04).

**Validation:**
1. Manual check: reviewer confirms TFEP entry/exit conditions resolve to cited `file:line`.
2. Manual check: reviewer confirms branch-to-flow mapping is complete (no orphan branches).

**Dependencies**: T01.04

---

### T02.03 — Characterize MCP declarations, persona activation, allowed-tools, compliance gating, triggering surface

**Roadmap Item IDs**: R-006
**Tier**: EXEMPT
**Effort**: L
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary, using `/sc:analyze --focus architecture` patterns.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/feature-mcp-declarations.md`
- `TASKLIST_ROOT/artifacts/feature-persona-activation.md`
- `TASKLIST_ROOT/artifacts/feature-allowed-tools.md`
- `TASKLIST_ROOT/artifacts/feature-compliance-gating.md`
- `TASKLIST_ROOT/artifacts/feature-triggering-surface.md`

**Deliverables:**
- Five `feature-*.md` files, each a full seven-field characterization.

**Steps:**
1. **[PLANNING]** Pull the MCP-declaration, persona-activation, allowed-tools, compliance-gating, and triggering-surface rows from `donor-feature-catalog.md`.
2. **[EXECUTION]** Use auggie MCP to characterize each: MCP server declarations (which servers, declared where, what invokes them), persona auto-activation (trigger conditions, which personas, observable effect), declared allowed-tools (the list, where enforced), compliance gating (what it gates, on what condition), triggering surface (how `/sc:task` is invoked vs how `/task` is invoked).
3. **[EXECUTION]** For each, record `file:line` evidence (side-tagged) and all seven characterization fields.
4. **[EXECUTION]** Apply anti-sycophancy — every value claim gets a non-value condition; every coupling claim names the integration cost.
5. **[VERIFICATION]** Confirm all five files complete with evidence and non-value conditions.
6. **[COMPLETION]** Write all five files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. All five `feature-*.md` files exist with all seven characterization fields populated.
2. Every mechanism claim cites side-tagged `file:line` evidence (R-RULE-03, R-RULE-10).
3. The triggering-surface characterization contrasts `/sc:task` invocation with `/task` invocation explicitly.
4. Each value claim carries an explicit non-value condition (R-RULE-04).

**Validation:**
1. Manual check: reviewer confirms all five files have seven fields each.
2. Manual check: reviewer confirms MCP/persona/allowed-tools claims resolve to declared `file:line` (flagging any that are declared-but-never-load-bearing for Phase 4).

**Dependencies**: T01.04

---

### T02.04 — Anti-sycophancy completeness pass over all `feature-*.md`

**Roadmap Item IDs**: R-007
**Tier**: EXEMPT
**Effort**: S
**MCP Requirements**: auggie MCP optional (re-resolution of disputed evidence only).

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/feature-*.md` (all nine files, updated as needed)
- `TASKLIST_ROOT/artifacts/anti-sycophancy-pass-p2.md` (pass report)

**Deliverables:**
- A pass report confirming every `feature-*.md` value claim has a concrete non-value condition; any file that fails is corrected in place.

**Steps:**
1. **[PLANNING]** Collect all nine `feature-*.md` files from T02.01-T02.03.
2. **[EXECUTION]** For each file, verify every standalone value claim has a concrete (not boilerplate) condition under which it does NOT deliver value, and every coupling cost claim names a concrete recipient burden.
3. **[EXECUTION]** Correct any file that fails — strengthen the non-value condition or add the missing coupling cost.
4. **[VERIFICATION]** Re-scan all nine files; confirm zero remaining R-RULE-04 violations.
5. **[COMPLETION]** Write `anti-sycophancy-pass-p2.md` listing each file and pass/fail-then-corrected status.

**Acceptance Criteria:**
1. `anti-sycophancy-pass-p2.md` exists and lists all nine `feature-*.md` files.
2. Every value claim across all nine files has a concrete non-value condition (R-RULE-04).
3. Every coupling cost claim names a concrete recipient burden.
4. Any file corrected during the pass is noted in the report with what changed.

**Validation:**
1. Manual check: reviewer samples 3 files and confirms non-value conditions are concrete and specific.

**Dependencies**: T02.01, T02.02, T02.03

---

### T02.05 — Checkpoint: End of Phase 2

**Roadmap Item IDs**: R-004, R-005, R-006, R-007
**Tier**: LIGHT
**Effort**: XS
**MCP Requirements**: None

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-END.md`

**Purpose:** Confirm every donor feature in the Phase 1 catalog has a debate-ready characterization before Phase 3 invariant extraction.

**Checkpoint Table:**

| Acceptance Criterion | Source Task | Verification | Status |
|---|---|---|---|
| One `feature-*.md` per donor catalog feature, all seven fields populated | T02.01-T02.03 | Count files vs catalog rows; spot-check fields | TBD |
| Every mechanism claim cites side-tagged `file:line` | T02.01-T02.03 | Spot-check 6 claims | TBD |
| Every value claim has a concrete non-value condition | T02.04 | `anti-sycophancy-pass-p2.md` shows zero violations | TBD |
| Triggering-surface file contrasts `/sc:task` vs `/task` invocation | T02.03 | File contains explicit contrast | TBD |
| No donor catalog feature lacks a characterization | T02.01-T02.04 | 1:1 coverage confirmed | TBD |

**Steps:**
1. **[VERIFICATION]** Count `feature-*.md` files against `donor-feature-catalog.md` rows; confirm 1:1 coverage (DUPLICATE-OF-EXISTING features still get a characterization for Phase 4 net-upgrade debate).
2. **[VERIFICATION]** Spot-check evidence resolution and the anti-sycophancy pass report.
3. **[VERIFICATION]** Write `CP-P02-END.md` with the checkpoint table and `Overall:` status.

**Acceptance Criteria:**
1. `CP-P02-END.md` exists and contains `Overall: Pass`.
2. All five checkpoint-table rows are marked Pass.
3. Report confirms 1:1 coverage between donor catalog features and `feature-*.md` characterizations.

**Validation:**
1. Manual check: reviewer confirms the checkpoint report and the 1:1 coverage claim.

**Dependencies**: T02.01, T02.02, T02.03, T02.04
