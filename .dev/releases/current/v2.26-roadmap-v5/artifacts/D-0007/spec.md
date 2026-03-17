# D-0007: Implementation Decision Log — v2.26

**Consolidated from:** T01.01 (D-0001) through T01.06 (D-0006)
**Date:** 2026-03-16
**Status:** COMPLETE

---

## OQ-A: GateCriteria.aux_inputs Field

**Decision:** Option B — Frontmatter Embedding
**Rationale:** `GateCriteria` has no `aux_inputs` field. Adding one would require modifying `pipeline/models.py`, violating architecture constraint AC-1 (no generic pipeline layer modifications). FR-079 implementation uses frontmatter embedding instead.
**Source:** D-0001
**Cascading:** Determines OQ-B and OQ-C resolution paths

---

## OQ-B: FR-088 Extended Validation Deferral

**Decision:** FR-088 extended validation reads from step output frontmatter fields; no new GateCriteria fields needed
**Rationale:** Follows from OQ-A Option B. Existing `required_frontmatter_fields` mechanism on GateCriteria is sufficient. No gate enforcement layer modification required.
**Source:** D-0001
**Cascading:** None — deferral remains valid

---

## OQ-C: PRE_APPROVED ID Extraction Method

**Decision:** Frontmatter field parsing in sprint-layer only
**Rationale:** No `PRE_APPROVED` mechanism exists in codebase. Extraction will parse YAML frontmatter of step output files. Belongs in sprint-specific layer, not pipeline layer.
**Source:** D-0001

---

## OQ-D: (Not explicitly listed in tasklist — no open question tracked)

N/A — OQ-D was not assigned in Phase 1 task scope.

---

## OQ-E: `_extract_fidelity_deviations()` Signature

**Decision:** Function does not exist — requires creation in `fidelity.py`
**Rationale:** `fidelity.py` contains only `Severity` enum and `FidelityDeviation` dataclass. No extraction helpers exist. Must be created in Phase 2.
**Planned signature:** `def _extract_fidelity_deviations(content: str) -> list[FidelityDeviation]`
**Source:** D-0002

---

## OQ-F: `_extract_deviation_classes()` Signature

**Decision:** Function does not exist — requires creation in `fidelity.py`
**Rationale:** Same as OQ-E. No deviation grouping/classification helper exists.
**Planned signature:** `def _extract_deviation_classes(deviations: list[FidelityDeviation]) -> dict[str, list[FidelityDeviation]]`
**Source:** D-0002
**Phase 2 Files Modified:** `src/superclaude/cli/roadmap/fidelity.py` — add two functions; no other changes

---

## OQ-G: `build_remediate_step()` Module Location

**Decision:** Create in `src/superclaude/cli/roadmap/remediate.py`
**Rationale:** `build_remediate_step()` does not exist. `remediate.py` is the natural home (contains all remediation logic). No circular import risk. No new file needed.
**Source:** D-0003

---

## OQ-H: `roadmap_run_step()` Hash Injection Interface

**Decision:** Use existing post-sanitize conditional block pattern (same as `_inject_pipeline_diagnostics`)
**Rationale:** `roadmap_run_step()` has an established pattern for post-step injection at lines 255–258. `roadmap_hash` injection follows the same pattern — add a conditional block after sanitization. No signature change required.
**Source:** D-0003

---

## OQ-I: `token_count` Field Availability

**Decision:** Best-effort fallback — output file size as proxy; `token_count` field = `Optional[int] = None`
**Rationale:** Claude is launched as CLI subprocess with text output. No API response parsing occurs. Token counts are not available from the subprocess model. File size proxy is the best available metric.
**Source:** D-0003

---

## OQ-J: FR-077 Dual-Budget-Exhaustion Handling

**Decision:** Placeholder behavior in v2.26; full implementation deferred to Phase 4 T04.07
**v2.26 behavior:** `_print_terminal_halt()` logs whichever budget was exhausted first; no dual-exhaustion distinction
**v2.26 target:** T04.07 adds `DUAL_BUDGET_EXHAUSTED` status detection and distinct terminal output
**Source:** D-0004

---

## Architecture Constraint Summary

All 4 architecture constraints verified as HOLDING:

| Constraint | Status |
|------------|--------|
| AC-1: No modifications to `pipeline/executor.py` and `pipeline/models.py` | PASS |
| AC-2: No new executor primitives | PASS |
| AC-3: No normal reads of `dev-*-accepted-deviation.md` | PASS |
| AC-4: Acyclic module dependency hierarchy | PASS |

**Source:** D-0005

---

## `_parse_routing_list()` Placement

**Decision:** Place in `src/superclaude/cli/roadmap/remediate.py`
**Rationale:** Natural home for routing/remediation logic; no new dependencies; no new file; tie-breaker applied per roadmap rules
**Source:** D-0006
