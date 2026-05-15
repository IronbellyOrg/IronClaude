# Phase 7 -- Validation & Adversarial Re-Review

**Phase Goal:** Validate the Phase 6 merge plan adversarially. Run a `/sc:adversarial` debate on the plan itself with an Invariant Defender and a Manifest Auditor, re-verify every file reference, check compat hazards, check traceability gaps, demonstrate invariant survival with a worked example, and re-score any feature where Phase 6 implementation drifted from the Phase 5 manifest. Produce the validated `final-merge-plan.md`.

**Compliance Tier:** STRICT (adversarial validation of a plan that will drive code changes).

---

### T07.01 — `/sc:adversarial` review of the merge plan

**Roadmap Item IDs**: R-024
**Tier**: STRICT
**Effort**: L
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary for evidence re-resolution. Sequential — required.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/plan-adversarial-review.md`

**Deliverables:**
- `plan-adversarial-review.md` — a `/sc:adversarial` debate of the merge plan with two roles: **Invariant Defender** (scans every Phase 6 change for invariant impact, cites INV-NN evidence) and **Manifest Auditor** (cross-checks every manifest feature against the Phase 6 plan, flags drops, unauthorized scope expansion, implementation drift).

**Steps:**
1. **[PLANNING]** Load `merge-master.md`, the five `refactor-*.md` files, `transfer-manifest.md`, and `invariant-bounds.md`.
2. **[EXECUTION]** Invoke `/sc:adversarial`. Invariant Defender role: walk every Phase 6 change row, assess INV-01..INV-05 impact, cite the specific `file:line` from `invariant-bounds.md` for any change that touches an invariant surface.
3. **[EXECUTION]** Manifest Auditor role: walk every `transfer-manifest.md` feature, confirm it maps to a Phase 6 change row; flag any dropped feature, any Phase 6 change with no manifest origin (unauthorized scope expansion), and any change whose shape drifted from the Phase 5 integration sketch.
4. **[EXECUTION]** Each role answers the other directly; unanswered points are recorded as open findings.
5. **[VERIFICATION]** Confirm every Phase 6 change row received an Invariant Defender assessment and every manifest feature received a Manifest Auditor assessment.
6. **[COMPLETION]** Write `plan-adversarial-review.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `plan-adversarial-review.md` exists with both roles' assessments.
2. Every Phase 6 change row has an Invariant Defender assessment citing INV-NN evidence where an invariant surface is touched.
3. Every `transfer-manifest.md` feature has a Manifest Auditor assessment (mapped / dropped / drifted).
4. All unauthorized scope expansions and implementation drifts are recorded as open findings.

**Validation:**
1. Sub-agent verification: an agent independently spot-checks 5 change rows for invariant impact.
2. Manual check: reviewer confirms both roles answered each other's strongest points.

**Dependencies**: T06.06 (Phase 6 checkpoint passed)

---

### T07.02 — Re-verify file references & check compat hazards

**Roadmap Item IDs**: R-025
**Tier**: STRICT
**Effort**: M
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary. Serena — optional for call-site resolution. Sequential — required.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/file-reference-reverification.md`
- `TASKLIST_ROOT/artifacts/compat-hazard-report.md`

**Deliverables:**
- `file-reference-reverification.md` — every file reference in the merge plan re-verified to exist (or flagged), side-tagged.
- `compat-hazard-report.md` — assessment of whether the plan breaks any in-flight MDTM file under `.dev/tasks/to-do/`, any sprint already in `.dev/releases/current/`, or any documented `/sc:task` workflow.

**Steps:**
1. **[PLANNING]** Collect every file path referenced across `merge-master.md` and the five `refactor-*.md` files.
2. **[EXECUTION]** Use auggie MCP to re-verify each path exists; flag any path that does not resolve; re-confirm side tags (R-RULE-10).
3. **[EXECUTION]** Check compat hazards: does any planned MDTM frontmatter change break an existing `.dev/tasks/to-do/TASK-*/TASK-*.md` file (INV-04 resumability)? Does the `/sc:task` deprecation strand any sprint in `.dev/releases/current/`? Does it strand any documented workflow?
4. **[EXECUTION]** For each hazard found, record severity and a mitigation.
5. **[VERIFICATION]** Confirm every plan file reference is accounted for and every hazard has a mitigation.
6. **[COMPLETION]** Write both files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `file-reference-reverification.md` exists; every plan file reference is re-verified or explicitly flagged, side-tagged.
2. `compat-hazard-report.md` exists and assesses in-flight MDTM files, current sprints, and documented workflows.
3. Every hazard found carries a severity and a mitigation.
4. No planned MDTM frontmatter change breaks an existing `TASK-*` file without a mitigation (INV-04).

**Validation:**
1. Sub-agent verification: an agent independently re-verifies a sample of file paths.
2. Manual check: reviewer confirms the compat-hazard assessment covers all three hazard classes.

**Dependencies**: T06.06

---

### T07.03 — Traceability gap check & invariant-survival walkthrough

**Roadmap Item IDs**: R-026
**Tier**: STRICT
**Effort**: M
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary. Sequential — required.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/traceability-gap-report.md`
- `TASKLIST_ROOT/artifacts/invariant-survival-walkthrough.md`

**Deliverables:**
- `traceability-gap-report.md` — confirms every ADOPT/ADAPT manifest feature maps to >= 1 Phase 6 change and every Phase 6 change traces back to >= 1 manifest feature; lists any gap.
- `invariant-survival-walkthrough.md` — a worked example run through the *merged* `/task` showing INV-01..INV-05 still hold.

**Steps:**
1. **[PLANNING]** Load `transfer-manifest.md`, `merge-master.md`, and `invariant-bounds.md`.
2. **[EXECUTION]** Build the two-way traceability check: manifest feature -> Phase 6 change(s), and Phase 6 change -> manifest feature(s); list every gap (orphan change, unimplemented feature).
3. **[EXECUTION]** Construct a worked example: take a representative MDTM file, run it through the merged `/task` surface step by step, and demonstrate at each step that INV-01 (F1 loop semantics), INV-02 (prohibited actions), INV-03 (phase-gate `rf-qa`), INV-04 (resumability), and INV-05 (refusal-of-definition) still hold.
4. **[EXECUTION]** Where an absorbed feature interacts with an invariant surface, show the interaction explicitly in the walkthrough.
5. **[VERIFICATION]** Confirm zero unexplained traceability gaps and all five invariants demonstrated in the walkthrough.
6. **[COMPLETION]** Write both files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `traceability-gap-report.md` exists; every ADOPT/ADAPT manifest feature maps to >= 1 Phase 6 change and every Phase 6 change traces to >= 1 manifest feature.
2. Any gap is listed explicitly with a disposition (close it, or justify).
3. `invariant-survival-walkthrough.md` runs a worked example through the merged `/task` and demonstrates INV-01..INV-05 each still hold.
4. Interactions between absorbed features and invariant surfaces are shown explicitly.

**Validation:**
1. Sub-agent verification: an agent independently re-runs the two-way traceability check.
2. Manual check: reviewer confirms the walkthrough demonstrates all five invariants, not just asserts them.

**Dependencies**: T07.01

---

### T07.04 — Re-score drifted features; produce `validation-report.md` & `final-merge-plan.md`

**Roadmap Item IDs**: R-027
**Tier**: STRICT
**Effort**: L
**MCP Requirements**: auggie MCP optional. Sequential — required.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/validation-report.md`
- `TASKLIST_ROOT/artifacts/final-merge-plan.md`

**Deliverables:**
- `validation-report.md` — pass/fail per plan item and per manifest feature, consolidating the findings of T07.01-T07.03.
- `final-merge-plan.md` — the validated, corrected master plan: `merge-master.md` with all Phase 7 corrections applied.

**Steps:**
1. **[PLANNING]** Load `plan-adversarial-review.md`, `compat-hazard-report.md`, `traceability-gap-report.md`, `invariant-survival-walkthrough.md`, and `merge-master.md`.
2. **[EXECUTION]** For every feature whose Phase 6 implementation drifted from the Phase 5 integration sketch, re-apply the V/C/K rubric — the verdict may now change (e.g., a drift that adds an F1 change drops C to 1 and forces REJECT). Record re-scores.
3. **[EXECUTION]** Build `validation-report.md`: pass/fail per Phase 6 plan item and per manifest feature, with the finding source (T07.01/02/03).
4. **[EXECUTION]** Apply every correction (close traceability gaps, mitigate compat hazards, drop or re-scope drifted features) to produce `final-merge-plan.md`.
5. **[EXECUTION]** Confirm no `rejected-features-ledger.md` entry was re-introduced and any re-score that changes a verdict carries an explicit re-debate note (R-RULE-11).
6. **[VERIFICATION]** Confirm `final-merge-plan.md` has zero open findings and every re-score is documented.
7. **[COMPLETION]** Write both files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `validation-report.md` exists with a pass/fail verdict per Phase 6 plan item and per manifest feature, each tied to its finding source.
2. Every drifted feature is re-scored with the V/C/K rubric and the re-score is documented (R-RULE-07).
3. `final-merge-plan.md` exists with all Phase 7 corrections applied and zero open findings.
4. No `rejected-features-ledger.md` entry is re-introduced; any verdict change carries a re-debate note (R-RULE-11).

**Validation:**
1. Sub-agent verification: an agent confirms `final-merge-plan.md` has no open findings and every correction traces to a Phase 7 artifact.
2. Manual check: reviewer recomputes a sample of re-scores.

**Dependencies**: T07.01, T07.02, T07.03

---

### T07.05 — Checkpoint: End of Phase 7

**Roadmap Item IDs**: R-024, R-025, R-026, R-027
**Tier**: LIGHT
**Effort**: XS
**MCP Requirements**: None

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P07-END.md`

**Purpose:** Confirm the merge plan is adversarially validated, file-verified, traceable, and invariant-safe before final assembly.

**Checkpoint Table:**

| Acceptance Criterion | Source Task | Verification | Status |
|---|---|---|---|
| `plan-adversarial-review.md` covers every change row + every manifest feature | T07.01 | Coverage check | TBD |
| Every plan file reference re-verified; compat hazards have mitigations | T07.02 | Spot-check paths + hazard table | TBD |
| Two-way traceability complete; invariant-survival walkthrough demonstrates INV-01..INV-05 | T07.03 | Gap report empty; walkthrough complete | TBD |
| Drifted features re-scored; `final-merge-plan.md` has zero open findings | T07.04 | Re-scores documented; findings closed | TBD |
| No `rejected-features-ledger.md` entry re-introduced (R-RULE-11) | T07.01-T07.04 | Cross-check against ledger | TBD |

**Steps:**
1. **[VERIFICATION]** Confirm all Phase 7 artifacts exist under `TASKLIST_ROOT/artifacts/`.
2. **[VERIFICATION]** Confirm `final-merge-plan.md` has zero open findings and the ledger was not re-litigated.
3. **[VERIFICATION]** Write `CP-P07-END.md` with the checkpoint table and `Overall:` status.

**Acceptance Criteria:**
1. `CP-P07-END.md` exists and contains `Overall: Pass`.
2. All five checkpoint-table rows are marked Pass.
3. Report confirms `final-merge-plan.md` is the validated binding plan for any downstream implementation sprint.

**Validation:**
1. Manual check: reviewer confirms the checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P07-END.md`.

**Dependencies**: T07.01, T07.02, T07.03, T07.04
