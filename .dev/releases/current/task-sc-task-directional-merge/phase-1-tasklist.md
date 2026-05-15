# Phase 1 -- Recipient & Donor Inventory

**Phase Goal:** Build an asymmetric inventory -- recipient extension points on one side, donor feature surface on the other. The recipient side maps where new capability can attach without disturbing the F1 loop; the donor side enumerates every concrete feature of `/sc:task` with file:line evidence and a first-pass transferability tag. This phase is read-only (EXEMPT) and produces the inputs every later phase consumes.

**Compliance Tier:** EXEMPT (read-only inventory).

---

### T01.01 — Enumerate `/task` recipient extension points

**Roadmap Item IDs**: R-001
**Tier**: EXEMPT
**Effort**: M
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary. Serena optional for symbol-level resolution of the subagent dispatcher.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/recipient-extension-points.md`

**Deliverables:**
- `recipient-extension-points.md` — one row per extension point, each with: extension-point name, location (`file:line`, side-tagged `src/` vs `.claude/`), what kind of capability can attach there, and whether attaching disturbs the F1 loop.

**Steps:**
1. **[PLANNING]** Use auggie MCP to locate `task/SKILL.md` on both sides (`src/superclaude/skills/task/` and `.claude/skills/task/`); confirm which is source of truth per R-RULE-10.
2. **[EXECUTION]** Use auggie MCP to enumerate `/task` extension points: pre-loop hooks, per-item hooks, phase-gate hooks, post-completion hooks, MDTM frontmatter slots, the prohibited-actions list (the negative space — what is explicitly disallowed defines where features may NOT attach), and the subagent dispatcher.
3. **[EXECUTION]** For each extension point, capture `file:line` evidence and tag the side (`src/superclaude/` vs `.claude/`) per R-RULE-10.
4. **[EXECUTION]** For each extension point, write a one-line statement of what shape of capability it can absorb and whether attaching there touches the F1 loop.
5. **[VERIFICATION]** Confirm every row has `file:line` evidence and a side tag; confirm the prohibited-actions negative space is represented as its own row(s).
6. **[COMPLETION]** Write `recipient-extension-points.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `recipient-extension-points.md` exists with one row per extension point.
2. Every row cites `file:line` evidence with an explicit `src/` vs `.claude/` side tag (R-RULE-03, R-RULE-10).
3. Pre-loop, per-item, phase-gate, and post-completion hook categories are each represented; MDTM frontmatter slots and the subagent dispatcher each have at least one row.
4. The prohibited-actions list is captured as negative-space rows (places a feature may NOT attach).

**Validation:**
1. Manual check: reviewer confirms each extension point row resolves to the cited `file:line`.
2. Manual check: reviewer confirms the F1-loop-disturbance column is populated for every row.

**Dependencies**: None

---

### T01.02 — Enumerate `/sc:task` donor features with transferability tags

**Roadmap Item IDs**: R-002
**Tier**: EXEMPT
**Effort**: L
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/donor-feature-catalog.md`

**Deliverables:**
- `donor-feature-catalog.md` — one row per donor feature (not one row per file). Each row records: feature name, `file:line` evidence (side-tagged), current behavior, observable outputs, and a first-pass transferability tag (TRANSFERABLE | ADAPTABLE | NON-TRANSFERABLE | DUPLICATE-OF-EXISTING).

**Steps:**
1. **[PLANNING]** Use auggie MCP to locate the donor surface: `commands/sc/task.md` and `skills/sc-task-protocol/SKILL.md` on both `src/superclaude/` and `.claude/` sides.
2. **[EXECUTION]** Use auggie MCP to enumerate donor features at concrete granularity — one row per feature: triggering surface, STRICT/STANDARD/LIGHT/EXEMPT tier classification model, classification header emission, per-tier flow branching, TFEP, MCP server declarations, persona auto-activation, declared allowed-tools, compliance gating, and any others surfaced.
3. **[EXECUTION]** For every donor feature record `file:line` evidence (side-tagged per R-RULE-10), current behavior, and observable outputs (artifact, header, side effect, escalation).
4. **[EXECUTION]** Assign each feature a first-pass transferability tag: TRANSFERABLE, ADAPTABLE, NON-TRANSFERABLE, or DUPLICATE-OF-EXISTING.
5. **[VERIFICATION]** Confirm the catalog is feature-granular (no row that is really "a whole file"); confirm every row has evidence and a tag.
6. **[COMPLETION]** Write `donor-feature-catalog.md` to `TASKLIST_ROOT/artifacts/`.

**Acceptance Criteria:**
1. `donor-feature-catalog.md` exists with one row per donor feature, feature-granular (not file-granular).
2. Every feature has `file:line` evidence with side tag, current behavior, observable outputs, and a transferability tag.
3. The tier classification model, classification header emission, per-tier branching, and TFEP each appear as distinct rows.
4. No behavioral claim is unsupported by `file:line` evidence (R-RULE-03).

**Validation:**
1. Manual check: reviewer spot-checks 5 rows and confirms each `file:line` resolves and the behavior description matches.
2. Manual check: reviewer confirms every row carries one of the four transferability tags.

**Dependencies**: None

---

### T01.03 — Flag DUPLICATE-OF-EXISTING donor features

**Roadmap Item IDs**: R-003
**Tier**: EXEMPT
**Effort**: S
**MCP Requirements**: auggie MCP (`mcp__auggie-mcp__codebase-retrieval`, `directory_path: /config/workspace/IronClaude`) — primary.

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/donor-feature-catalog.md` (updated — duplicate flags merged in)

**Deliverables:**
- Updated `donor-feature-catalog.md` rows: every donor feature that `/task` already provides in some form is re-tagged DUPLICATE-OF-EXISTING with a pointer to the equivalent `/task` capability (`file:line`, side-tagged).

**Steps:**
1. **[PLANNING]** Take the donor catalog from T01.02 and the recipient extension-point inventory from T01.01 as inputs.
2. **[EXECUTION]** For each donor feature, use auggie MCP to search `/task` and `task-builder` for an equivalent capability.
3. **[EXECUTION]** Where `/task` already provides the capability, re-tag the donor row DUPLICATE-OF-EXISTING and add a pointer to the `/task` equivalent (`file:line`, side-tagged).
4. **[EXECUTION]** Where the match is partial (`/task` has a weaker or differently-shaped version), note it in the row so Phase 4 can debate whether the donor version is a net upgrade rather than a pure duplicate.
5. **[VERIFICATION]** Confirm every DUPLICATE-OF-EXISTING tag has a resolving `/task` `file:line` pointer.
6. **[COMPLETION]** Save the updated `donor-feature-catalog.md`.

**Acceptance Criteria:**
1. Every donor feature that `/task` already provides is tagged DUPLICATE-OF-EXISTING in `donor-feature-catalog.md`.
2. Each DUPLICATE-OF-EXISTING row carries a resolving `/task` `file:line` pointer with side tag.
3. Partial matches are annotated (not silently tagged as full duplicates) so Phase 4 can debate net-upgrade value.
4. No donor feature is left without a transferability tag after this task.

**Validation:**
1. Manual check: reviewer confirms each DUPLICATE-OF-EXISTING pointer resolves to a real `/task` capability.
2. Manual check: reviewer confirms partial-match annotations are present where applicable.

**Dependencies**: T01.01, T01.02

---

### T01.04 — Checkpoint: End of Phase 1

**Roadmap Item IDs**: R-001, R-002, R-003
**Tier**: LIGHT
**Effort**: XS
**MCP Requirements**: None

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`

**Purpose:** Confirm the asymmetric inventory is complete and evidence-backed before Phase 2 characterization begins.

**Checkpoint Table:**

| Acceptance Criterion | Source Task | Verification | Status |
|---|---|---|---|
| `recipient-extension-points.md` exists, one row per extension point, all evidence side-tagged | T01.01 | File present; spot-check 3 rows resolve | TBD |
| Prohibited-actions negative space represented as rows | T01.01 | Negative-space rows present | TBD |
| `donor-feature-catalog.md` exists, feature-granular, all rows tagged + evidenced | T01.02 | File present; spot-check 5 rows | TBD |
| Every donor feature `/task` already has is tagged DUPLICATE-OF-EXISTING with resolving pointer | T01.03 | All such rows carry `/task` `file:line` | TBD |
| No unsupported behavioral claims (R-RULE-03) | T01.01-T01.03 | Spot-check evidence column | TBD |

**Steps:**
1. **[VERIFICATION]** Confirm both inventory artifacts exist under `TASKLIST_ROOT/artifacts/`.
2. **[VERIFICATION]** Spot-check evidence resolution for a sample of recipient and donor rows.
3. **[VERIFICATION]** Write `CP-P01-END.md` with the checkpoint table and `Overall: Pass|Fail|TBD`.

**Acceptance Criteria:**
1. `CP-P01-END.md` exists and contains `Overall: Pass`.
2. All five checkpoint-table rows are marked Pass.
3. Report enumerates task IDs T01.01, T01.02, T01.03.

**Validation:**
1. Manual check: reviewer confirms the checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P01-END.md`.

**Dependencies**: T01.01, T01.02, T01.03
