# Phase 1 -- Deviation Analysis Classification Fix

Fix the semantically hollow deviation analysis step. Registry findings lack `deviation_class` and use hex stable_ids instead of gate-compliant DEV-N IDs. This phase adds classification logic and ID generation so the deviation-analysis step produces meaningful counts and gate-passing output.

---

### T01.01 -- Classify registry findings by deviation_class in _run_deviation_analysis

| Field | Value |
|---|---|
| Why | Registry findings have `status: "ACTIVE"`, `severity: "HIGH"`, `source_layer: "structural"` but no `deviation_class`. All classification counts (slip, intentional, pre_approved, ambiguous) are 0 despite 14 active findings, making the deviation report meaningless. |
| Effort | S |
| Risk | Low |
| Risk Drivers | data-flow |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Verification Method | Unit test + manual inspection |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | No |

**File:** `src/superclaude/cli/roadmap/executor.py`
**Lines:** ~1100-1115 (inside `_run_deviation_analysis`, after `records` is loaded, before aggregation block)

**Deliverables:**
1. Classification loop that sets `deviation_class` on each record based on available fields
2. Classification mapping is deterministic and documented

**Steps:**
1. **[PLANNING]** Read current `_run_deviation_analysis` function (executor.py:1090-1161) to confirm record structure
2. **[PLANNING]** Read sample registry data (deviation-registry.json) to confirm available fields: `status`, `severity`, `source_layer`, `debate_verdict`
3. **[EXECUTION]** Add classification loop after line ~1112 (after `records` is populated), before the aggregation block at line ~1114:
   - `status == "ACTIVE"` and `debate_verdict` is None/null → `"SLIP"`
   - `debate_verdict` is not None → `"INTENTIONAL"`
   - All other cases → `"AMBIGUOUS"`
4. **[VERIFICATION]** Confirm counts now reflect actual findings (14 SLIP expected for current data)

**Acceptance Criteria:**
- Records written to `spec-deviations.json` sidecar have `deviation_class` set on every record
- `slip_count` in `spec-deviations.md` frontmatter equals number of ACTIVE findings with no debate_verdict
- No records have `deviation_class: "UNCLASSIFIED"` after classification

**Dependencies:** None
**Rollback:** Remove classification loop; records revert to no `deviation_class` field

---

### T01.02 -- Assign gate-compliant DEV-N IDs to deviation records

| Field | Value |
|---|---|
| Why | DEVIATION_ANALYSIS_GATE `_routing_ids_valid` check requires DEV-\d+ pattern IDs. Registry findings use hex stable_ids (e.g., `cb46b85f46821f30`). Routing fields in frontmatter must contain DEV-N format IDs for the gate to pass. |
| Effort | S |
| Risk | Low |
| Risk Drivers | determinism across resume runs |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Verification Method | Unit test + gate validation |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | No |

**File:** `src/superclaude/cli/roadmap/executor.py`
**Lines:** ~1100-1128 (same function, alongside T01.01 classification loop)

**Deliverables:**
1. DEV-N ID assignment on each record (sorted by stable_id for determinism)
2. `id_mapping` dict in sidecar JSON mapping DEV-N → stable_id
3. Routing frontmatter fields use DEV-N IDs

**Steps:**
1. **[PLANNING]** Confirm routing ID construction at lines 1123-1124: `routing_fix` and `routing_no_action` use `r.get("stable_id")`
2. **[EXECUTION]** Sort records by `stable_id` before classification loop for deterministic ordering
3. **[EXECUTION]** In classification loop, assign `record["id"] = f"DEV-{i+1}"` for each record (1-indexed)
4. **[EXECUTION]** Build `id_mapping = {record["id"]: record["stable_id"] for record in records}` and include in sidecar JSON output at line ~1235
5. **[VERIFICATION]** Confirm routing frontmatter fields contain DEV-N format IDs
6. **[VERIFICATION]** Confirm same stable_id always maps to same DEV-N across resume runs (sorted order guarantee)

**Acceptance Criteria:**
- All routing IDs in `spec-deviations.md` frontmatter match `DEV-\d+` pattern
- `spec-deviations.json` sidecar contains `id_mapping` dict
- Re-running deviation-analysis produces identical DEV-N assignments for same registry data

**Dependencies:** T01.01 (classification must happen in same loop)
**Rollback:** Remove ID assignment; routing fields revert to empty strings

---

### T01.03 -- Test deviation analysis fixes

| Field | Value |
|---|---|
| Why | Verify that classification and ID assignment don't regress existing tests and that the gate passes with the new output format. |
| Effort | S |
| Risk | Low |
| Tier | STANDARD |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Verification Method | pytest |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | No |

**Steps:**
1. **[EXECUTION]** Run `uv run pytest tests/roadmap/ -v --tb=short` to check for regressions in roadmap tests
2. **[EXECUTION]** Run `uv run pytest tests/ -v --tb=short -q` for full suite regression check
3. **[VERIFICATION]** Confirm 4971+ tests pass, 0 new failures

**Acceptance Criteria:**
- No new test failures introduced by T01.01 or T01.02
- Pre-existing 3 failures remain unchanged

**Dependencies:** T01.01, T01.02
**Rollback:** N/A (test-only task)
