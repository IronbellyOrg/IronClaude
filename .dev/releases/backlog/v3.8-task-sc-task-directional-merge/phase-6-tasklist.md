# Phase 6 -- Directional Merge Plan

**Phase Goal:** Convert the Phase 5 transfer manifest into a concrete, sequenced refactoring plan that edits `/task` to absorb the ADOPT/ADAPT features and deprecates `/sc:task`. Every change row names a verified file path, the change, the manifest feature it implements, priority, effort, dependencies, acceptance criteria, and a risk assessment. Includes the `/sc:task` deprecation plan, the distribution surface refactor, and the unified `merge-master.md`.

**Compliance Tier:** STRICT (refactoring plan that will drive code changes; all file references must be verified via auggie before they are written into the plan).

---

### T06.01 — Convert manifest to implementation roadmap with dependency graph

**Roadmap Item IDs**: R-019
**Tier**: STRICT
**Effort**: L
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary, to verify every file path exists before it enters the plan. Sequential — required. Serena — optional for symbol-level call-site resolution.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/merge-roadmap.md`

**Deliverables:**
- `merge-roadmap.md` — the transfer manifest expressed as an implementation roadmap with a dependency graph: milestones, ordered change-sets, and inter-change dependencies.

**Steps:**
1. **[PLANNING]** Load `transfer-manifest.md` and `rejected-features-ledger.md` (Phase 5). Confirm no ledger entry is being re-proposed (R-RULE-11).
2. **[EXECUTION]** Use `/sc:roadmap` patterns to convert the manifest into a roadmap: group ADOPT/ADAPT features into milestones, order change-sets, draw the dependency graph.
3. **[EXECUTION]** Use auggie MCP to verify every file path referenced by the roadmap exists; tag each path `src/superclaude/` vs `.claude/` (R-RULE-10).
4. **[EXECUTION]** Surface any `src/` vs `.claude/` drift discovered during verification as an explicit roadmap finding (R-RULE-10).
5. **[VERIFICATION]** Confirm every roadmap node traces to a manifest feature and every file path is verified-present.
6. **[COMPLETION]** Write `merge-roadmap.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `merge-roadmap.md` exists with milestones, ordered change-sets, and a dependency graph.
2. Every file path in the roadmap is verified to exist via auggie MCP and is side-tagged (R-RULE-10).
3. Every roadmap node traces to a `transfer-manifest.md` feature; no `rejected-features-ledger.md` entry is re-proposed (R-RULE-11).
4. Any `src/` vs `.claude/` drift is recorded as an explicit finding.

**Validation:**
1. Sub-agent verification: an `Explore` or `general-purpose` agent independently confirms every roadmap file path exists.
2. Manual check: reviewer confirms node-to-manifest traceability.

**Dependencies**: T05.04 (Phase 5 checkpoint passed)

---

### T06.02 — Refactor plans: `/task` skill edits & MDTM frontmatter extensions

**Roadmap Item IDs**: R-020
**Tier**: STRICT
**Effort**: L
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary. Sequential — required. Serena — optional.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/refactor-task-skill.md`
- `TASKLIST_ROOT/artifacts/refactor-mdtm-frontmatter.md`

**Deliverables:**
- `refactor-task-skill.md` — every change to the `/task` skill package (`src/superclaude/skills/task/` and the `.claude/` dev copy) implied by ADOPT/ADAPT features, as change rows.
- `refactor-mdtm-frontmatter.md` — every new MDTM frontmatter field introduced by the manifest, with the compat treatment for existing `.dev/tasks/to-do/TASK-*/` files.

**Steps:**
1. **[PLANNING]** Load `transfer-manifest.md` and `merge-roadmap.md`; isolate the manifest features that land in the `/task` executor or in MDTM frontmatter.
2. **[EXECUTION]** For each `/task` skill change, write a change row: file path (auggie-verified, side-tagged), what changes (edit-in-place / add hook / rename / delete), which manifest feature it implements (one-to-many traceability), priority tier (P0-P3), effort (XS-XL), dependencies, acceptance criteria (observable post-condition), risk assessment (which INV-NN the change could violate if applied wrong + mitigation).
3. **[EXECUTION]** For each new MDTM frontmatter field, write a change row plus the backward-compat treatment: how existing MDTM files without the field behave (must remain valid — INV-04 resumability).
4. **[EXECUTION]** Confirm every change cites the control pattern from the manifest, not donor ceremony (R-RULE-06).
5. **[VERIFICATION]** Confirm every change row has all eight columns and every file path is verified-present.
6. **[COMPLETION]** Write both `refactor-*.md` files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `refactor-task-skill.md` and `refactor-mdtm-frontmatter.md` exist; every change row has file path, change, manifest-feature ref, priority, effort, dependencies, acceptance criteria, risk assessment.
2. Every file path is auggie-verified and side-tagged (R-RULE-10).
3. Every MDTM frontmatter addition specifies the backward-compat behavior for existing `TASK-*` files (INV-04).
4. Every risk assessment names the INV-NN at risk and its mitigation.

**Validation:**
1. Sub-agent verification: an agent independently confirms file paths and that no change row breaks an INV-NN.
2. Manual check: reviewer confirms one-to-many traceability from change rows to manifest features.

**Dependencies**: T06.01

---

### T06.03 — Refactor plans: `/sc:task` deprecation & references

**Roadmap Item IDs**: R-021
**Tier**: STRICT
**Effort**: L
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary. Serena — required for exhaustive call-site / reference resolution. Sequential — required.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/refactor-sctask-deprecation.md`
- `TASKLIST_ROOT/artifacts/refactor-references.md`

**Deliverables:**
- `refactor-sctask-deprecation.md` — the deprecation plan for `/sc:task`: soft-deprecation (command emits a redirect to `/task` and exits) vs hard-deprecation (file removed), chosen per artifact and justified, covering `commands/sc/task.md`, `commands/task.md`, `skills/sc-task-protocol/` on both `src/` and `.claude/` sides, plus the never-load-bearing MCP servers and personas.
- `refactor-references.md` — every reference to `sc:task`, `task-unified`, `sc-task-protocol` across `.dev/releases/backlog/*` and elsewhere, with the treatment for each.

**Steps:**
1. **[PLANNING]** Load `transfer-manifest.md` (what was absorbed) so deprecation only removes what is now redundant.
2. **[EXECUTION]** For each `/sc:task` artifact, choose soft- vs hard-deprecation and justify: `commands/sc/task.md`, `src/superclaude/commands/task.md`, `.claude/skills/sc-task-protocol/`, `src/superclaude/skills/sc-task-protocol/`.
3. **[EXECUTION]** Plan the treatment of declared MCP servers and personas that were never load-bearing (per Phase 2/4 findings) — removed, not silently orphaned.
4. **[EXECUTION]** Use auggie MCP + Serena to exhaustively enumerate references to `sc:task`, `task-unified`, `sc-task-protocol` across `.dev/releases/backlog/*` and the wider repo; write a treatment row for each (update redirect / remove / leave with note).
5. **[EXECUTION]** Each row carries the standard eight columns including risk assessment.
6. **[VERIFICATION]** Confirm no absorbed capability is lost by deprecation; confirm every enumerated reference has a treatment.
7. **[COMPLETION]** Write both `refactor-*.md` files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `refactor-sctask-deprecation.md` exists; every `/sc:task` artifact has a soft/hard deprecation decision with justification, side-tagged.
2. Never-load-bearing MCP servers and personas have an explicit removal plan.
3. `refactor-references.md` enumerates every reference to `sc:task` / `task-unified` / `sc-task-protocol` with a treatment row.
4. The plan confirms no manifest-absorbed capability is lost by deprecation.

**Validation:**
1. Sub-agent verification: an agent re-runs the reference enumeration and confirms no reference was missed.
2. Manual check: reviewer confirms each deprecation decision is justified.

**Dependencies**: T06.01

---

### T06.04 — Refactor plans: distribution surface & documentation

**Roadmap Item IDs**: R-022
**Tier**: STRICT
**Effort**: M
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary. Sequential — required.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/refactor-distribution.md`
- `TASKLIST_ROOT/artifacts/refactor-documentation.md`

**Deliverables:**
- `refactor-distribution.md` — change rows for `superclaude install` behavior, `make sync-dev` filter rules, and README rows affected by absorbing `/sc:task` into `/task` and deprecating the donor.
- `refactor-documentation.md` — change rows for every doc that describes `/sc:task` or the two-surface model.

**Steps:**
1. **[PLANNING]** Load `refactor-sctask-deprecation.md` and `refactor-task-skill.md` so the distribution changes match the artifact-level decisions.
2. **[EXECUTION]** Use auggie MCP to locate the `superclaude install` component-install logic, the `make sync-dev` filter rules, and README rows referencing `/sc:task` or `sc-task-protocol`.
3. **[EXECUTION]** Write change rows (eight columns each) for: install behavior (stop installing the deprecated command/skill), `make sync-dev` filter (stop syncing deprecated paths), README updates.
4. **[EXECUTION]** Write change rows for documentation: user-guide / developer-guide / reference docs that mention `/sc:task` or the two-surface model.
5. **[VERIFICATION]** Confirm every change row has verified file paths and the standard columns.
6. **[COMPLETION]** Write both `refactor-*.md` files to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `refactor-distribution.md` exists with change rows for `superclaude install`, `make sync-dev`, and README, all paths auggie-verified and side-tagged.
2. `refactor-documentation.md` exists with a change row for every doc referencing `/sc:task` or the two-surface model.
3. Distribution changes are consistent with the artifact-level deprecation decisions in T06.03.
4. Every change row carries the standard eight columns including risk assessment.

**Validation:**
1. Sub-agent verification: an agent confirms the distribution file paths and the doc reference enumeration.
2. Manual check: reviewer confirms consistency with T06.03.

**Dependencies**: T06.02, T06.03

---

### T06.05 — Produce `merge-master.md` unified plan

**Roadmap Item IDs**: R-023
**Tier**: STRICT
**Effort**: L
**MCP Requirements**: auggie MCP optional (final path re-verification). Sequential — required.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/merge-master.md`

**Deliverables:**
- `merge-master.md` — the unified merge plan: all change rows from the five `refactor-*.md` files consolidated, with a single dependency graph and a recommended execution order.

**Steps:**
1. **[PLANNING]** Load all five `refactor-*.md` files (`refactor-task-skill`, `refactor-mdtm-frontmatter`, `refactor-sctask-deprecation`, `refactor-references`, `refactor-distribution`, `refactor-documentation`) and `merge-roadmap.md`.
2. **[EXECUTION]** Consolidate every change row into a single ordered table; merge the per-area dependency edges into one dependency graph.
3. **[EXECUTION]** Derive the recommended execution order: ADOPT/ADAPT absorption into `/task` before `/sc:task` deprecation before distribution/doc changes, respecting all dependency edges.
4. **[EXECUTION]** Confirm every manifest feature has at least one change row and every change row traces to a manifest feature (one-to-many traceability both directions).
5. **[VERIFICATION]** Confirm the dependency graph is acyclic and the execution order respects it.
6. **[COMPLETION]** Write `merge-master.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `merge-master.md` exists with every change row from the five refactor files consolidated into one ordered table.
2. A single acyclic dependency graph and a recommended execution order are present.
3. Every `transfer-manifest.md` feature maps to at least one change row; every change row traces to a manifest feature.
4. Execution order sequences `/task` absorption before `/sc:task` deprecation before distribution/doc changes.

**Validation:**
1. Sub-agent verification: an agent confirms the dependency graph is acyclic and traceability is complete both directions.
2. Manual check: reviewer confirms the execution order is dependency-consistent.

**Dependencies**: T06.02, T06.03, T06.04

---

### T06.06 — Checkpoint: End of Phase 6

**Roadmap Item IDs**: R-019, R-020, R-021, R-022, R-023
**Tier**: LIGHT
**Effort**: XS
**MCP Requirements**: None

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P06-END.md`

**Purpose:** Confirm the merge plan is concrete, file-verified, and fully traceable before the Phase 7 adversarial re-review.

**Checkpoint Table:**

| Acceptance Criterion | Source Task | Verification | Status |
|---|---|---|---|
| `merge-roadmap.md` has milestones, change-sets, dependency graph; all paths verified | T06.01 | Spot-check 5 paths exist | TBD |
| `/task` skill + MDTM frontmatter refactor rows have all eight columns | T06.02 | Spot-check rows; INV-04 compat present | TBD |
| `/sc:task` deprecation decisions justified; references exhaustively enumerated | T06.03 | Spot-check references; no capability lost | TBD |
| Distribution + documentation refactor rows consistent with T06.03 | T06.04 | Consistency check | TBD |
| `merge-master.md` consolidated, acyclic graph, full two-way traceability | T06.05 | Traceability + acyclicity check | TBD |
| No `rejected-features-ledger.md` entry re-proposed (R-RULE-11) | T06.01-T06.05 | Cross-check against ledger | TBD |

**Steps:**
1. **[VERIFICATION]** Confirm all Phase 6 artifacts exist; spot-check file-path verification.
2. **[VERIFICATION]** Cross-check the plan against `rejected-features-ledger.md` for re-litigation.
3. **[VERIFICATION]** Write `CP-P06-END.md` with the checkpoint table and `Overall:` status.

**Acceptance Criteria:**
1. `CP-P06-END.md` exists and contains `Overall: Pass`.
2. All six checkpoint-table rows are marked Pass.
3. Report confirms Phase 7 has a complete, file-verified merge plan as input.

**Validation:**
1. Manual check: reviewer confirms the checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P06-END.md`.

**Dependencies**: T06.01, T06.02, T06.03, T06.04, T06.05
