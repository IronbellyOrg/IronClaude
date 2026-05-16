# Phase 4 -- Adversarial Debate & Stack Rank (`/sc:adversarial`)

**Phase Goal:** For every donor feature from Phase 1, run a structured `/sc:adversarial` debate to determine whether it should be absorbed into `/task`, then stack-rank the survivors. This is the core mechanism of the sprint. Each debate produces Position A (steelman for inclusion), Position B (steelman against), evidence-based weighing, and a scored verdict via the binding rubric Net = (V x C) / K. The anti-sycophancy gate (R-RULE-04) and the invariant gate (R-RULE-05) are applied before any verdict is final.

**Compliance Tier:** STANDARD (adversarial debate produces binding, auditable artifacts; V/C/K scoring must be reproducible).

**Scoring rubric (binding, R-RULE-07):**
- **V (Value, 1-5)** — capability gain for `/task` if absorbed.
- **C (Complementarity, 1-5)** — fit with the F1 loop and phase-gate model. 5 = native fit at an existing extension point with no F1 changes; 3 = lives at a recipient extension point but needs a new field or hook; 1 = requires changing F1 invariants (auto-REJECT).
- **K (Cost, 1-5)** — integration + ongoing maintenance cost.
- **Net = (V x C) / K** — stack-rank descending.
- **Verdicts**: ADOPT (Net >= 5), ADAPT (3 <= Net < 5), DEFER (1.5 <= Net < 3), REJECT (Net < 1.5 OR violates any INV-NN).

---

### T04.01 — `/sc:adversarial` debates: tier classification & classification header emission

**Roadmap Item IDs**: R-011
**Tier**: STANDARD
**Effort**: L
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary for evidence re-resolution. Sequential — required (adversarial reasoning).

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/debate-tier-classification.md`
- `TASKLIST_ROOT/artifacts/debate-classification-header.md`

**Deliverables:**
- One `debate-{feature-slug}.md` per feature: Position A, Position B, evidence-based weighing, and a scored verdict (V, C, K, Net, verdict).

**Steps:**
1. **[PLANNING]** Load `feature-tier-classification.md` and `feature-classification-header.md` (Phase 2) and `invariant-bounds.md` + `extension-point-contracts.md` (Phase 3) as the two source documents for each debate.
2. **[EXECUTION]** Invoke `/sc:adversarial` for the tier-classification feature: Position A steelmans inclusion (cites Phase 2 `file:line` evidence; shows the integration sketch — which extension point, what shape of change); Position B steelmans rejection (invariant-violation risk, duplication, maintenance/cognitive cost, at least one realistic failure mode introduced).
3. **[EXECUTION]** Run evidence-based weighing: each side answers the other's strongest point directly; unanswered points count against that side.
4. **[EXECUTION]** Score with the rubric — V, C (anchored to the extension-point Complementarity band from T03.02), K, Net = V x C / K; assign verdict.
5. **[EXECUTION]** Repeat steps 2-4 for classification header emission.
6. **[VERIFICATION]** Confirm both debate files have all four sections and a scored, auditable verdict; confirm C-band traces to `extension-point-contracts.md`.
7. **[COMPLETION]** Write both `debate-*.md` files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `debate-tier-classification.md` and `debate-classification-header.md` exist, each with Position A, Position B, evidence-based weighing, and a scored verdict.
2. Position A cites Phase 2 `file:line` evidence and includes an integration sketch (extension point + shape of change).
3. Position B cites invariant-violation risk (if any), duplication (if any), maintenance cost, and at least one realistic failure mode.
4. The V/C/K/Net computation is shown explicitly and the C value traces to a Complementarity band in `extension-point-contracts.md` (R-RULE-07).

**Validation:**
1. Manual check: reviewer recomputes Net = V x C / K and confirms the verdict matches the threshold.
2. Manual check: reviewer confirms each side answered the other's strongest point.

**Dependencies**: T03.04 (Phase 3 checkpoint passed)

---

### T04.02 — `/sc:adversarial` debates: TFEP & per-tier flow branching

**Roadmap Item IDs**: R-012
**Tier**: STANDARD
**Effort**: L
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary. Sequential — required.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/debate-tfep.md`
- `TASKLIST_ROOT/artifacts/debate-per-tier-branching.md`

**Deliverables:**
- One `debate-{feature-slug}.md` per feature with the four-section structure and scored verdict.

**Steps:**
1. **[PLANNING]** Load `feature-tfep.md` and `feature-per-tier-branching.md` plus the Phase 3 invariant bounds and extension-point contracts.
2. **[EXECUTION]** Invoke `/sc:adversarial` for TFEP: Position A steelmans inclusion with integration sketch; Position B steelmans rejection — pay specific attention to whether TFEP's forensic-pipeline trigger can attach at a post-completion hook without touching the F1 loop (INV-01) or the phase-gate `rf-qa` invariant (INV-03).
3. **[EXECUTION]** Run evidence-based weighing; score with the rubric; assign verdict.
4. **[EXECUTION]** Repeat for per-tier flow branching — Position B must specifically address whether branching the execution flow by tier collides with INV-01 (F1 loop semantics: EXECUTE exactly as written) or INV-05 (refusal-of-definition).
5. **[VERIFICATION]** Confirm both debate files complete; confirm any invariant-collision finding is surfaced explicitly, not papered over (R-RULE-05).
6. **[COMPLETION]** Write both `debate-*.md` files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `debate-tfep.md` and `debate-per-tier-branching.md` exist with the full four-section structure and scored verdicts.
2. The TFEP debate explicitly addresses INV-01 and INV-03 attachment safety.
3. The per-tier-branching debate explicitly addresses INV-01 and INV-05 collision risk.
4. Any invariant collision is surfaced in the debate text, not hidden (R-RULE-05); if a collision exists the verdict is REJECT regardless of V.

**Validation:**
1. Manual check: reviewer confirms invariant-collision analysis is present and the verdict honors R-RULE-05.
2. Manual check: reviewer recomputes Net and confirms verdict.

**Dependencies**: T03.04

---

### T04.03 — `/sc:adversarial` debates: MCP, persona, allowed-tools, compliance gating, triggering surface

**Roadmap Item IDs**: R-013
**Tier**: STANDARD
**Effort**: XL
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary. Sequential — required.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/debate-mcp-declarations.md`
- `TASKLIST_ROOT/artifacts/debate-persona-activation.md`
- `TASKLIST_ROOT/artifacts/debate-allowed-tools.md`
- `TASKLIST_ROOT/artifacts/debate-compliance-gating.md`
- `TASKLIST_ROOT/artifacts/debate-triggering-surface.md`

**Deliverables:**
- Five `debate-{feature-slug}.md` files, each with the four-section structure and scored verdict.

**Steps:**
1. **[PLANNING]** Load the five Phase 2 `feature-*.md` files from T02.03 plus the Phase 3 constraints.
2. **[EXECUTION]** Invoke `/sc:adversarial` per feature. Position B must apply R-RULE-06 ("absorb patterns, not implementation mass") aggressively here — MCP declarations, persona auto-activation, and declared allowed-tools are prime candidates for "ceremony without behavioral teeth" if Phase 2 found them declared-but-never-load-bearing.
3. **[EXECUTION]** For each feature run evidence-based weighing; score V/C/K/Net; assign verdict.
4. **[EXECUTION]** For any feature tagged DUPLICATE-OF-EXISTING in Phase 1, Position A must argue the *net upgrade* over `/task`'s existing capability, not raw value; if there is no net upgrade the verdict is REJECT.
5. **[VERIFICATION]** Confirm all five debate files complete with scored verdicts; confirm R-RULE-06 was applied to ceremony-suspect features.
6. **[COMPLETION]** Write all five `debate-*.md` files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. All five `debate-*.md` files exist with the full four-section structure and scored verdicts.
2. Features Phase 2 found declared-but-never-load-bearing are debated under R-RULE-06; ceremony with no behavioral teeth is REJECTed.
3. DUPLICATE-OF-EXISTING features are debated on net-upgrade value, not raw value.
4. Every V/C/K/Net computation is explicit and auditable (R-RULE-07).

**Validation:**
1. Manual check: reviewer confirms R-RULE-06 reasoning is present for ceremony-suspect features.
2. Manual check: reviewer recomputes Net for all five and confirms verdicts.

**Dependencies**: T03.04

---

### T04.04 — Apply anti-sycophancy gate & invariant gate; re-debate failures

**Roadmap Item IDs**: R-014
**Tier**: STANDARD
**Effort**: M
**MCP Requirements**: auggie MCP optional (evidence re-resolution). Sequential — required for any re-debate.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/gate-pass-report.md`
- `TASKLIST_ROOT/artifacts/debate-*.md` (any file sent back is re-debated and updated in place)

**Deliverables:**
- `gate-pass-report.md` — per-debate result of the anti-sycophancy gate and the invariant gate, plus a re-debate ledger for any debate sent back.

**Steps:**
1. **[PLANNING]** Collect all nine `debate-*.md` files from T04.01-T04.03.
2. **[EXECUTION]** Apply the anti-sycophancy gate (R-RULE-04): any debate whose Position A lacks at least one trade-off acknowledgment is sent back for re-debate.
3. **[EXECUTION]** Apply the invariant gate (R-RULE-05): any feature requiring an INV-01..INV-05 break is auto-REJECTed regardless of V; confirm the debate surfaced the violation rather than papering over it.
4. **[EXECUTION]** Re-debate every file sent back; update it in place; record the before/after in the re-debate ledger.
5. **[VERIFICATION]** Confirm zero remaining anti-sycophancy violations and that every invariant-violating feature carries a REJECT verdict.
6. **[COMPLETION]** Write `gate-pass-report.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `gate-pass-report.md` exists and lists the anti-sycophancy and invariant gate result for all nine debates.
2. Every debate that failed the anti-sycophancy gate was re-debated and now passes (R-RULE-04).
3. Every feature requiring an invariant break carries a REJECT verdict (R-RULE-05).
4. The re-debate ledger records what changed for each sent-back debate.

**Validation:**
1. Manual check: reviewer confirms no Position A lacks a trade-off acknowledgment.
2. Manual check: reviewer confirms every invariant-violating feature is REJECTed.

**Dependencies**: T04.01, T04.02, T04.03

---

### T04.05 — Stack-rank all features by Net score

**Roadmap Item IDs**: R-015
**Tier**: STANDARD
**Effort**: M
**MCP Requirements**: auggie MCP optional. Sequential — recommended.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/stack-rank.md`

**Deliverables:**
- `stack-rank.md` — all donor features sorted by Net score descending, with columns V, C, K, Net, verdict, link to the debate artifact, and the integration sketch for every ADOPT and ADAPT feature.

**Steps:**
1. **[PLANNING]** Collect the post-gate verdicts from all nine debates and the `gate-pass-report.md`.
2. **[EXECUTION]** Build the stack-rank table: one row per feature, sorted by Net descending, with V/C/K/Net/verdict, a link to `debate-{slug}.md`, and (for ADOPT/ADAPT) the integration sketch.
3. **[EXECUTION]** Confirm verdict thresholds were applied consistently (ADOPT >= 5, ADAPT 3-5, DEFER 1.5-3, REJECT < 1.5 or invariant violation); flag any subjective override as a candidate "manifest exception" for Phase 5 (R-RULE-07).
4. **[VERIFICATION]** Confirm every feature appears exactly once and every ADOPT/ADAPT row has an integration sketch.
5. **[COMPLETION]** Write `stack-rank.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `stack-rank.md` exists with every donor feature appearing exactly once, sorted by Net descending.
2. Each row shows V, C, K, Net, verdict, and a link to its `debate-*.md`.
3. Every ADOPT and ADAPT row carries an integration sketch.
4. Verdict thresholds are applied consistently; any subjective override is flagged for a Phase 5 manifest exception (R-RULE-07).

**Validation:**
1. Manual check: reviewer recomputes 3 Net scores and confirms ordering and verdicts.
2. Manual check: reviewer confirms 1:1 coverage with the donor feature catalog.

**Dependencies**: T04.04

---

### T04.06 — Checkpoint: End of Phase 4

**Roadmap Item IDs**: R-011, R-012, R-013, R-014, R-015
**Tier**: LIGHT
**Effort**: XS
**MCP Requirements**: None

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-END.md`

**Purpose:** Confirm every donor feature has a gated, scored verdict and that the stack rank is complete before Phase 5 synthesis.

**Checkpoint Table:**

| Acceptance Criterion | Source Task | Verification | Status |
|---|---|---|---|
| One `debate-*.md` per donor feature, four-section structure, scored verdict | T04.01-T04.03 | Count debates vs catalog; spot-check structure | TBD |
| Anti-sycophancy gate passed for all debates | T04.04 | `gate-pass-report.md` shows zero violations | TBD |
| Invariant gate: every invariant-violating feature REJECTed | T04.04 | Cross-check verdicts vs invariant findings | TBD |
| `stack-rank.md` complete, 1:1 with catalog, sorted by Net | T04.05 | Coverage + ordering check | TBD |
| Every ADOPT/ADAPT row has an integration sketch | T04.05 | Spot-check ADOPT/ADAPT rows | TBD |

**Steps:**
1. **[VERIFICATION]** Confirm all nine debate files, the gate-pass report, and the stack rank exist.
2. **[VERIFICATION]** Recompute a sample of Net scores; confirm gate enforcement.
3. **[VERIFICATION]** Write `CP-P04-END.md` with the checkpoint table and `Overall:` status.

**Acceptance Criteria:**
1. `CP-P04-END.md` exists and contains `Overall: Pass`.
2. All five checkpoint-table rows are marked Pass.
3. Report confirms Phase 5 has a complete, gated, scored stack rank as input.

**Validation:**
1. Manual check: reviewer confirms the checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P04-END.md`.

**Dependencies**: T04.01, T04.02, T04.03, T04.04, T04.05
