# D-0029 — T03.04 Spec: Self-Audit Schema Requirement + INV-019 + K-003

**Task:** T03.04 (Phase 3)
**Roadmap items:** R-055, R-058
**Date:** 2026-05-17
**Status:** PASS

---

## 1. Scope

T03.04 appends a normative `## Self-Audit Schema Requirement (INV-019,
K-003 Audit-Target)` section at the EOF of `rf-qa-qualitative.md`. The
section:

1. Names `## Self-Audit` as the mandatory output-schema subsection that
   every rf-qa-qualitative report MUST emit (realised in the embedded
   Output Format template as the
   `## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)`
   subsection landed by T03.01).
2. Specifies the two content categories that subsection MUST populate:
   (a) reliance list of rf-qa PASS items skipped, (b) ≥1 independent
   semantic check with tool evidence.
3. Documents the INV-019 enforcement rule: zero entries in category (b)
   is a violation regardless of category (a).
4. Documents K-003 as the audit-target: first 5 rf-qa-qualitative runs
   after FR-CONV.3 lands are the K-003 audit window
   (release-spec §8.3 row 4); FAIL disables
   `FF_INHERITED_STRUCTURAL_VERDICT` and triggers FR-CONV.3 rollback
   per release-spec §19.4.
5. Cross-references the producer (SKILL.md §A.10.5), consumer (Critical
   Rule #11), anti-inflation block (rf-qa-qualitative.md:766-775),
   runbook (OPS-001 / M7), KPI (Self-Audit coverage post-FR-CONV.3),
   and fixture (TEST-009 / T03.14).

## 2. Roadmap items covered

| Item   | Title                                             | Coverage |
|--------|---------------------------------------------------|----------|
| R-055  | `## Self-Audit` output section (M3)               | New EOF section formalises the schema requirement and cites the embedded template realisation already landed by T03.01. |
| R-058  | INV-019 Self-Audit consumer obligation            | "INV-019 enforcement" subsection makes the zero-category-(b) violation observable via grep + content inspection. |

K-003 is documented as the audit-target for INV-019 (release-spec §8.3
row 4; OPEN-X-002 mitigation).

## 3. Edits landed

| File                                              | Change                                              |
|---------------------------------------------------|-----------------------------------------------------|
| `src/superclaude/agents/rf-qa-qualitative.md`     | Appended `## Self-Audit Schema Requirement (INV-019, K-003 Audit-Target)` section at EOF (lines 822-889; 70 insertions, 0 deletions). |
| `.claude/agents/rf-qa-qualitative.md`             | Synced byte-identical via direct copy (verified by `diff -q`). |

`make verify-sync` PASS post-edit (all components in sync).

## 4. Byte stability of anti-inflation block (rf-qa-qualitative.md:766-775)

Required by T03.08 (preservation) but verified now for early defence:

| Snapshot         | SHA-256                                                          |
|------------------|------------------------------------------------------------------|
| Pre-T03.04 edit  | `0570c6b474686734d8a69e62adcd825d3c0b3e421ef4a12ef114703d1deec59c` |
| Post-T03.04 edit | `0570c6b474686734d8a69e62adcd825d3c0b3e421ef4a12ef114703d1deec59c` |

**Result:** byte-identical (diff: 0). T03.04 appends only at EOF; it
does not touch lines 766-775.

## 5. Schema location summary

| Surface                                                       | Heading                                                                                       | Role                                                  |
|---------------------------------------------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------------|
| Embedded Output Format template (line ~728, landed by T03.01) | `## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)`                           | What the agent emits in each report.                  |
| Per-phase QA checklists (lines 184, 232, 300, 364, 432, 496, 601, 636) | `### Self-Audit (MANDATORY before writing verdict)`                                  | Pre-verdict self-check inside each QA phase.          |
| File EOF (lines 823-889, landed by T03.04 — THIS task)        | `## Self-Audit Schema Requirement (INV-019, K-003 Audit-Target)`                              | Normative spec naming INV-019 obligation + K-003 audit-target. |

The literal `## Self-Audit` heading now appears at line 823 of
`rf-qa-qualitative.md` (and at lines 825, 851, 858, 887 as in-prose
mentions), satisfying the AC `grep -n "## Self-Audit" ... ≥ 794` with
margin.

## 6. INV-019 enforcement (audit recipe)

A run is **inflation-positive** (INV-019 violation) when any of the
following is true:

1. The emitted report omits the `## Self-Audit` subsection entirely
   (`grep -c "## Self-Audit"` against the emitted report file returns
   0).
2. The `## Self-Audit` subsection contains category-(a) bullets only
   (zero category-(b) bullets — no independent semantic check).
3. Category-(b) bullets restate rf-qa PASS items verbatim without
   independent tool evidence (e.g., no file:line citation, no grep
   output, no Read excerpt).

Detection commands:

```bash
# (1) Self-Audit present?
grep -c "^## Self-Audit\|^## Inherited Structural Verdict" <report>

# (2) Category-(b) bullets present?
sed -n '/^## \(Self-Audit\|Inherited Structural Verdict\)/,/^## /p' <report> \
  | grep -c "semantic counterpart verified"
```

A category-(b) count of `0` against criterion (2) triggers the
INV-019 violation flag.

## 7. K-003 audit-target

| Field                  | Value                                                                                                                   |
|------------------------|-------------------------------------------------------------------------------------------------------------------------|
| Audit window           | First 5 rf-qa-qualitative runs after FR-CONV.3 lands (M7).                                                              |
| Source                 | release-spec.md §8.3 row 4 "Audit-after-FR-CONV.3-lands"; OPEN-X-002 (TDD §22); R-007 (roadmap risk table).             |
| Pass criterion         | All 5 reports carry `## Self-Audit` with ≥1 category-(b) entry; no inflation detected.                                  |
| Fail action            | Disable `FF_INHERITED_STRUCTURAL_VERDICT`; roll back FR-CONV.3 per release-spec §19.4 (fallback to independent structural re-checking). |
| Runbook                | OPS-001 (M7).                                                                                                           |
| KPI                    | "Self-Audit coverage post-FR-CONV.3" — target 100% on first 5 runs.                                                     |
| Fixture (lab-time)     | TEST-009 (T03.14) asserts `## Self-Audit` + ≥1 category-(b) entry; negative-case variant (zero category-(b)) MUST fail. |
| Owner                  | QA Lead.                                                                                                                |

## 8. Acceptance-criterion mapping

| AC | Criterion                                                                                              | Verification                                                                                                                    |
|----|--------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| 1  | `grep -n "## Self-Audit" src/superclaude/agents/rf-qa-qualitative.md` returns match at or after line 794 | Match at line 823 (and 825, 851, 858, 887). See `evidence.md` §2.                                                                |
| 2  | Self-Audit output includes both rf-qa PASS reliance list AND ≥1 documented semantic check               | New section §"Required content (both categories MUST be populated)" mandates both (a)+(b); embedded template also enforces both. |
| 3  | A run with 0 entries in semantic-check category is flagged as INV-019 violation                         | New section §"INV-019 enforcement" states the rule explicitly; §6 of this spec provides detection commands.                      |
| 4  | Evidence at `TASKLIST_ROOT/artifacts/D-0029/evidence.md`                                                | This file's sibling `evidence.md` (created in same commit).                                                                      |

## 9. Dependencies / forward-references

- **Depends on:** T03.03 (API-002-M3 splice operational at SKILL.md §A.10.5).
- **Forward-references:**
  - T03.08 — anti-inflation block byte-stability check at :766-775 (this
    task pre-validates the hash; T03.08 captures the canonical pre/post
    diff across all M3 work).
  - T03.10 — "Handling the Inherited Structural Verdict" section append
    + `## Self-Audit` reference inside the embedded template at line 794
    region (further specifies the consumer behaviour; this task supplies
    the normative spec).
  - T03.14 — TEST-009 INV-019 fixture (runtime sample verification);
    deferred per phase-3 tasklist Notes.
  - M7 / OPS-001 — K-003 audit runbook + first-5-runs audit window
    (operational realisation of the spec landed here).

## 10. Rollback

Per phase-3 roadmap: disable `FF_INHERITED_STRUCTURAL_VERDICT`
passthrough flag and fall back to independent structural re-checking
inside rf-qa-qualitative. Removing the EOF section landed here is
**not** a rollback path — the spec is informational; the operational
behaviour is governed by SKILL.md §A.10.5 (producer) + Critical Rule
#11 (consumer wiring).
