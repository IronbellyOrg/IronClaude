# Phase 8 -- Sprint Checkpoint & Artifact Assembly

**Phase Goal:** Assemble all artifacts into a navigable deliverable and validate sprint completeness. Build the artifact index, verify the end-to-end traceability chain from every Phase 1 donor feature through to its final disposition, confirm no orphaned artifacts or dead references, and produce the sprint summary. Pass the final structural quality gate.

**Compliance Tier:** LIGHT (assembly and verification).

---

### T08.01 — Build `artifact-index.md`

**Roadmap Item IDs**: R-028
**Tier**: LIGHT
**Effort**: S
**MCP Requirements**: None (filesystem enumeration of `TASKLIST_ROOT/artifacts/`).

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/artifact-index.md`

**Deliverables:**
- `artifact-index.md` — a navigable index linking every artifact produced in Phases 1-7, grouped by phase, each with a one-line description.

**Steps:**
1. **[PLANNING]** Enumerate every file under `TASKLIST_ROOT/artifacts/` and `TASKLIST_ROOT/checkpoints/`.
2. **[EXECUTION]** Group artifacts by phase (1-7) and the checkpoints; for each artifact write a relative link and a one-line description of its role.
3. **[EXECUTION]** Mark the binding artifacts (`transfer-manifest.md`, `final-merge-plan.md`) and the terminal artifact (`rejected-features-ledger.md`) explicitly.
4. **[VERIFICATION]** Confirm every file on disk under `artifacts/` and `checkpoints/` appears in the index and every index link resolves.
5. **[COMPLETION]** Write `artifact-index.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `artifact-index.md` exists and links every artifact in Phases 1-7 plus all checkpoint reports.
2. Artifacts are grouped by phase; each has a one-line description.
3. Binding and terminal artifacts are explicitly marked.
4. Every index link resolves to a file on disk.

**Validation:**
1. Manual check: reviewer confirms every link in the index resolves and no `artifacts/` file is missing from the index.

**Dependencies**: T07.05 (Phase 7 checkpoint passed)

---

### T08.02 — Verify the end-to-end traceability chain

**Roadmap Item IDs**: R-029
**Tier**: LIGHT
**Effort**: S
**MCP Requirements**: None (cross-artifact consistency check).

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/traceability-chain-check.md`

**Deliverables:**
- `traceability-chain-check.md` — for every Phase 1 donor feature, the verified chain: catalog entry -> Phase 2 characterization -> Phase 4 debate with scored verdict -> Phase 5 manifest (ADOPT/ADAPT) or rejected-features ledger (DEFER/REJECT) -> if ADOPT/ADAPT, Phase 6 change row -> if scoped for change, Phase 7 validation verdict. Plus a dead-reference scan.

**Steps:**
1. **[PLANNING]** Load `donor-feature-catalog.md`, all `feature-*.md`, all `debate-*.md`, `stack-rank.md`, `transfer-manifest.md`, `rejected-features-ledger.md`, `merge-master.md`, `final-merge-plan.md`, `validation-report.md`.
2. **[EXECUTION]** For each donor feature, walk the full chain and record each link's presence; flag any broken link.
3. **[EXECUTION]** Scan all artifacts for dead references — links to artifacts that do not exist, or `file:line` citations that no longer resolve.
4. **[EXECUTION]** Scan for orphaned artifacts — files under `artifacts/` not reachable from any chain or the artifact index.
5. **[VERIFICATION]** Confirm every donor feature has a complete chain and zero dead/orphan references remain.
6. **[COMPLETION]** Write `traceability-chain-check.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `traceability-chain-check.md` exists and shows a complete verified chain for every Phase 1 donor feature.
2. Every chain link (catalog -> characterization -> debate -> manifest/ledger -> change row -> validation verdict) is confirmed present or its absence is justified.
3. Zero dead references and zero orphaned artifacts, or each is listed with a disposition.

**Validation:**
1. Manual check: reviewer spot-checks 3 donor features' full chains end-to-end.

**Dependencies**: T08.01

---

### T08.03 — Produce `sprint-summary.md` & pass final quality gate

**Roadmap Item IDs**: R-030
**Tier**: LIGHT
**Effort**: M
**MCP Requirements**: None.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/sprint-summary.md`

**Deliverables:**
- `sprint-summary.md` — feature counts by verdict (ADOPT/ADAPT/DEFER/REJECT), top-ranked accepted features, top rejected features with rationale, total estimated effort, recommended implementation order, and the rejected-features ledger reproduced as a permanent record. Plus the final structural quality-gate result.

**Steps:**
1. **[PLANNING]** Load `stack-rank.md`, `transfer-manifest.md`, `rejected-features-ledger.md`, `final-merge-plan.md`, `traceability-chain-check.md`.
2. **[EXECUTION]** Compute feature counts by verdict; list the top-ranked ADOPT features by Net score; list the top REJECT features with one-line rationale.
3. **[EXECUTION]** Sum the estimated effort across `final-merge-plan.md` change rows; restate the recommended implementation order.
4. **[EXECUTION]** Reproduce the rejected-features ledger inline as a permanent record so DEFER/REJECT features are not silently re-proposed in a future sprint (R-RULE-11).
5. **[EXECUTION]** Run the final structural quality gate: all artifacts present, all checkpoints `Overall: Pass`, traceability chain complete, no dead references.
6. **[VERIFICATION]** Confirm the quality-gate result is recorded and the summary is internally consistent with the binding artifacts.
7. **[COMPLETION]** Write `sprint-summary.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `sprint-summary.md` exists with feature counts by verdict, top accepted/rejected features, total effort, and recommended implementation order.
2. The rejected-features ledger is reproduced inline as a permanent record (R-RULE-11).
3. The final structural quality gate is run and its result (pass/fail) recorded.
4. The summary is internally consistent with `transfer-manifest.md` and `final-merge-plan.md`.

**Validation:**
1. Manual check: reviewer confirms the verdict counts match `stack-rank.md` and the effort total matches `final-merge-plan.md`.

**Dependencies**: T08.01, T08.02

---

### T08.04 — Checkpoint: End of Phase 8 (SPRINT EXIT GATE)

**Roadmap Item IDs**: R-028, R-029, R-030
**Tier**: LIGHT
**Effort**: XS
**MCP Requirements**: None

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P08-END.md`

**Purpose:** Final sprint exit gate — confirm all artifacts are assembled, traceable, and structurally valid.

**Checkpoint Table:**

| Acceptance Criterion | Source Task | Verification | Status |
|---|---|---|---|
| `artifact-index.md` links every Phase 1-7 artifact + checkpoints; all links resolve | T08.01 | Link-resolution check | TBD |
| End-to-end traceability chain complete for every donor feature | T08.02 | `traceability-chain-check.md` shows zero broken chains | TBD |
| Zero dead references, zero orphaned artifacts | T08.02 | Scan result clean or dispositioned | TBD |
| `sprint-summary.md` complete and consistent with binding artifacts | T08.03 | Counts + effort cross-check | TBD |
| All Phase 1-7 checkpoints are `Overall: Pass` | T08.03 | Read CP-P01..CP-P07 | TBD |
| Final structural quality gate passed | T08.03 | Gate result recorded | TBD |

**Steps:**
1. **[VERIFICATION]** Confirm all Phase 8 artifacts exist and all prior checkpoints are `Overall: Pass`.
2. **[VERIFICATION]** Confirm the traceability chain and quality-gate results.
3. **[VERIFICATION]** Write `CP-P08-END.md` with the checkpoint table and `Overall:` status.

**Acceptance Criteria:**
1. `CP-P08-END.md` exists and contains `Overall: Pass`.
2. All six checkpoint-table rows are marked Pass.
3. Report confirms the sprint deliverable is complete: binding `transfer-manifest.md` and validated `final-merge-plan.md` are in place, the rejected-features ledger is terminal and recorded, and every donor feature has a traceable final disposition.

**Validation:**
1. Manual check: reviewer confirms the checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P08-END.md` and that all eight phase checkpoints pass.

**Dependencies**: T08.01, T08.02, T08.03
