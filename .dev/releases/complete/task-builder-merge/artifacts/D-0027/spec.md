# D-0027 — T03.02 Spec: DM-002-M3 Schema (3 Sub-Fields)

**Task:** T03.02 (Phase 3)
**Roadmap items:** R-050, R-051, R-052, R-053
**Date:** 2026-05-17
**Status:** PASS (sub-agent verified)

---

## 1. Scope

T03.02 implements the DM-002 (Inherited Structural Verdict Block)
entity per the M1 contract-freeze (T01.13 / D-0011 § DM-002; PRD §25.2).
DM-002 is the data-model schema that A.10.5 emits into every
rf-qa-qualitative spawn prompt. Three fields are populated, two of them
as fixed verbatim strings frozen as wire ABI:

1. **`rf_qa_table_verbatim`** — byte-exact copy of rf-qa task-integrity
   "Items Reviewed" PASS/FAIL table at spawn time. No editing /
   summarising / renaming / re-ordering. Diff against the producer's
   table (`${TASK_DIR}qa/qa-task-validation-report.md`) = zero bytes.
2. **`prompt_directive`** — fixed string (verbatim, frozen):
   `"PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."`
3. **`reinjection_rule`** — fixed string (verbatim, frozen):
   `"On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."`

The implementation lands at two distinct sites in
`src/superclaude/skills/task-builder/SKILL.md`:

| Site | Lines (post-T03.02) | Purpose |
|---|---|---|
| A.10.5 spawn-prompt template | 1111-1138 | Emits the DM-002 instance at every rf-qa-qualitative spawn. Carries `DM-002.rf_qa_table_verbatim` placeholder + verbatim `DM-002.prompt_directive` line + verbatim `DM-002.reinjection_rule` line + paraphrase as expanded guidance below. |
| A.10.7 published schema | 1265-1308 | Source-of-truth wire contract: YAML showing the 3 fields, field-by-field semantics table, versioning binding to DM-005 `schema_version: 1.0.0`, cross-references. Parallel to A.10.6 (DM-005 phase contract). |

Mirror parity maintained via `make sync-dev`; src ↔ `.claude/`
byte-identical.

## 2. Why this is a critical-path task

Per phase-3-tasklist L103: "DM-002 wire shape governs M3+M4
composition." DM-002 is the entity that DM-005 carries and that A.10.5
emits at runtime. Without the 3-field schema landed, T03.03 (API-002-M3
spawn-prompt injection) has no defined output shape, T03.05 (INV-002
freshness fixture) has no `reinjection_rule` to enforce, and T03.16
(MIG-003 landing) has no contract to ship.

## 3. Schema (verbatim, as landed at A.10.7)

```yaml
# DM-002 — Inherited Structural Verdict Block
# Frozen: M1 (T01.13 / D-0011 § DM-002)
# Implemented: M3 (T03.02 / D-0027)
# Consumed: M3 (FR-CONV.3 / PR-04, A.10.5 spawn-prompt injection)
"## Inherited Structural Verdict":
  rf_qa_table_verbatim: <byte-exact copy of rf-qa task-integrity "Items Reviewed" table at spawn time>
  prompt_directive: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."
  reinjection_rule: "On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."
```

## 4. Field semantics (1.0.0 wire ABI)

Bound to DM-005 `schema_version: 1.0.0` (A.10.6). Major-version bump
required for any field rename, add, semantic shift, or value-type
change.

| Field | Wire Value | Meaning |
|---|---|---|
| rf_qa_table_verbatim | Byte-exact table copy | Verbatim copy of rf-qa task-integrity "Items Reviewed" PASS/FAIL table extracted from `${TASK_DIR}qa/qa-task-validation-report.md` at spawn time. No editing/summarising/renaming/re-ordering. Diff = zero bytes. Extraction is contiguous (single span between `## Items Reviewed` heading and the next `## ` heading). |
| prompt_directive | Fixed string (verbatim) | The verbatim string MUST appear in every emitted DM-002 instance. Treated as frozen wire ABI. A.10.5 MAY include an expanded human-readable paraphrase BELOW the verbatim anchor, but the verbatim string MUST be present. |
| reinjection_rule | Fixed string (verbatim) | The verbatim string MUST appear in every emitted DM-002 instance. INV-002 enforces at every fix-cycle spawn boundary (re-read producer artifact → re-extract table → re-emit DM-002 with cycle-N values). |

## 5. Invariants preserved/enforced

| Invariant | Site | DM-002 guarantee |
|---|---|---|
| INV-002 (freshness) | A.10.5:1100 + reinjection_rule verbatim | Stale verdicts forbidden across fix cycles. T03.05 + TEST-008 enforce mechanically. |
| INV-010 (dynamic TB-Add enumeration) | A.10.5:1100 | Orchestrator pulls TB-Add catalogue live from rf-qa.md. T03.07 + TEST-010 enforce. |
| INV-019 (consumer Self-Audit obligation) | A.10.5:1132 + DM-005 consumer_obligation | rf-qa-qualitative MUST emit Self-Audit with (a) PASS reliance list + (b) ≥1 semantic check. T03.04 + TEST-009 enforce. |
| Anti-inflation byte-stability | rf-qa-qualitative.md:766-775 (untouched) | Block byte-identical pre/post T03.02. T03.08 captures formal byte-diff. |
| Wire ABI freeze (DM-005 schema_version 1.0.0) | A.10.7 versioning note | DM-002 field changes require coordinated DM-005 major-version bump + migration note. |

## 6. Rollback

Per roadmap row R-049 / R-050: disable passthrough flag
(`FF_INHERITED_STRUCTURAL_VERDICT`), fall back to independent
structural re-checking. Mechanically (additive to T03.01 rollback):

1. Comment out A.10.5 spawn-prompt lines 1116 + 1118 (the verbatim
   `DM-002.prompt_directive` and `DM-002.reinjection_rule` anchor
   lines). Wrapper continues to emit verdict table; consumer treats
   absence as fall-back-to-paraphrase.
2. A.10.7 published schema can remain in place — it is documentation,
   not runtime behaviour. Marking the section as `(deprecated under
   FF_INHERITED_STRUCTURAL_VERDICT=off)` is sufficient.
3. DM-005 (A.10.6) is unaffected; the phase contract still names
   `Inherited Structural Verdict block` as the artifact.

`FF_INHERITED_STRUCTURAL_VERDICT` cleanup is consolidated in M7 (release
spec §8.3 row 4).

## 7. Cross-references

- Phase 3 task spec: `.dev/releases/current/task-builder-merge/phase-3-tasklist.md` T03.02 (L55-103)
- M1 contract-freeze parent: T01.13 / D-0011 § DM-002
- PRD canonical: `PRD_TASK_BUILDER_CONVERGENCE.md` §25.2 (L956-963)
- Roadmap rows: R-050 (DM-002-M3 entity), R-051 (rf_qa_table_verbatim), R-052 (prompt_directive), R-053 (reinjection_rule)
- Sibling phase contract: A.10.6 / DM-005 (`SKILL.md` L1201-1257)
- Producer source: `rf-qa.md` § "Items Reviewed" (L361-364)
- Consumer source: `rf-qa-qualitative.md` Critical Rule #11 + Reliance Audit subsection
- Quality-engineer verdict: `D-0027/quality-engineer-report.md` (PASS)
- Sub-agent evidence: `D-0027/evidence.md`
