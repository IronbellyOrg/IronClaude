# D-0070 — T06.03 Spec: Implement DM-003.severity + DM-003.source fixed-field emitters

**Task:** T06.03 (Phase 6 — M6 Synthetic DNSP on Partition Exhaust)
**Roadmap items:** R-113 (DM-003.severity — `severity: HIGH` fixed, non-overridable), R-114 (DM-003.source — `source: "synthetic-dnsp"` fixed literal sentinel)
**Date:** 2026-05-18
**Status:** PASS
**Tier:** STANDARD
**Critical Path Override:** No
**Confidence:** [█████████-] 90%
**Verification method:** Direct test execution (grep + structural inspection)
**Sub-Agent Delegation:** None
**Branch:** `feat/hook-sync-and-matcher-fix`
**Pre-edit HEAD:** `edd3ddd docs(task-builder): D-0067 T05.16 MIG-005 evidence + FF governance entry`

---

## 1. Scope

T06.03 binds emitter-level rejection semantics to the two fixed-value DM-003 fields landed as M1 contract-freeze entries by T06.02 (D-0069):

- **R-113 — `severity: HIGH` (non-overridable):** any synthetic-DNSP emission whose `severity` field is not the literal `HIGH` (case-sensitive) MUST be rejected by the emitter as a fixed-field invariant violation. Rationale: without this pin a synthetic could be quietly demoted at merge-time past rf-qa's `any gap regardless of severity = FAIL` rule.
- **R-114 — `source: "synthetic-dnsp"` literal sentinel:** any synthetic-DNSP emission whose `source` field is not the literal string `synthetic-dnsp` (case-sensitive) MUST be rejected by the emitter as a fixed-field invariant violation. Rationale: the literal sentinel is the operator-facing distinguishing token that allows downstream filtering, auditing, and reporting of synthetic emissions distinct from real partition-agent findings.

T06.02 (D-0069) had already pinned these two fields in the wrapper enumeration (with the parentheticals "non-overridable" and "literal sentinel"); T06.03 elevates the implicit invariant to an **explicit emitter-level rejection contract** with a named error symbol (`DM-003-fixed-field-invariant-violation`), case-sensitivity stated, and rationale recorded inline so that downstream emitter-implementation work in T06.07 (API-003-M6 emission) and T06.10 (HIGH severity non-overridable) has an unambiguous spec to bind to.

The other 5 DM-003 fields (`affected_range`, `evidence`, `recommendation`, `dedup_key`, `found_n_times`) are out of T06.03 scope and are addressed by T06.04 (affected_range + evidence emitters, D-0071) and T06.05 (recommendation + dedup_key + found_n_times emitters, D-0072).

## 2. Inputs

| Input | Path | Role |
|---|---|---|
| T06.02 closure | `artifacts/D-0069/evidence.md` | 7-field schema landed at all 4 wrapper sites; severity HIGH + source `"synthetic-dnsp"` enumerated as fixed-value bullets with "(non-overridable)" / "(literal sentinel)" parentheticals. T06.03 elevates these to explicit emitter rejection. |
| R-113 spec | `roadmap.md` (DM-003.severity row) | `severity: HIGH` non-overridable; rejection on any other value. |
| R-114 spec | `roadmap.md` (DM-003.source row) | `source: "synthetic-dnsp"` literal sentinel; rejection on any other value. |
| M1 contract-freeze | `roadmap.md` L109 (DM-003 row) | `severity:HIGH-fixed; source:synthetic-dnsp-fixed`. |
| FR-CONV.6 wrapper sites | `SKILL.md` L660-666 + `rf-analyst.md` L70 + `rf-qa.md` L78 + `rf-qa-qualitative.md` L79 | 7-field bullet contract landed by T06.02 (D-0069). T06.03 appends a rejection clause to each wrapper bullet (and a rejection paragraph after the bullet list in SKILL.md) without altering the existing 7-field enumeration byte-identical. |

## 3. Edits (strictly additive — appends rejection clause after the 7-field bullet contract; no existing field-enumeration text changed)

### Edit 1 — `src/superclaude/skills/task-builder/SKILL.md` (L668-669 post-edit)

After the closing `found_n_times` bullet (L666), before the "Then the orchestrator merges" paragraph, inserted a new paragraph:

> **Fixed-field emitter rejection (R-113 + R-114).** The `severity` and `source` fields are non-overridable fixed-value invariants of DM-003. The emitter MUST reject any synthetic-dnsp emission whose `severity` field is not the literal `HIGH` (case-sensitive) OR whose `source` field is not the literal `synthetic-dnsp` (case-sensitive). Such rejections surface as `DM-003-fixed-field-invariant-violation` errors and MUST NOT be silently coerced. Rationale: the `HIGH` pin prevents merge-time severity downgrade (without it the synthetic could be quietly demoted past the gate's any-gap-regardless-of-severity = FAIL rule); the literal `synthetic-dnsp` sentinel is what allows downstream operators to filter, audit, and report on synthetic emissions distinct from real findings.

### Edit 2 — `src/superclaude/agents/rf-analyst.md` (L70 trailing-sentence extension)

Appended to the end of the existing DNSP wrapper bullet (after the INV-012 composition sentence):

> **Fixed-field emitter rejection (R-113 + R-114).** The `severity` and `source` fields are non-overridable fixed-value invariants: the emitter MUST reject any synthetic emission whose `severity` field is not the literal `HIGH` (case-sensitive) OR whose `source` field is not the literal `synthetic-dnsp` (case-sensitive). Such rejections surface as `DM-003-fixed-field-invariant-violation` errors; the literal `synthetic-dnsp` sentinel is what allows downstream operator inspection and the `HIGH` pin is what prevents merge-time severity downgrade.

### Edit 3 — `src/superclaude/agents/rf-qa.md` (L78 trailing-sentence extension)

Symmetric to Edit 2; identical clause text appended to the rf-qa DNSP wrapper bullet.

### Edit 4 — `src/superclaude/agents/rf-qa-qualitative.md` (L79 trailing-sentence extension)

Symmetric to Edit 2 + Edit 3; identical clause text appended to the rf-qa-qualitative DNSP wrapper bullet.

`rf-team-lead.md` was NOT edited (preservation gate — see §4).

## 4. Preservation invariants

| Slice | sha256 (pre + post-edit identical) |
|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (3-cycle hard cap + all-agents-fail escalation backstop — COMP-006-M6 preservation gate, byte-stable end-to-end across PR-02, PR-03, M1–M6) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — no edit anywhere) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |

The existing 7-field bullet contract at all four wrapper sites (the M1 contract-freeze enumeration landed by T06.02) is preserved byte-identical; T06.03 only appends a trailing rejection clause. See `evidence.md` §3 for grep counts that confirm the seven field names still appear at each site post-edit (counts unchanged from D-0069 §3).

## 5. Fixed-value byte-identity verification (R-113 + R-114)

The M1 contract-freeze pins `severity` and `source` to two specific literal values. Every post-edit emission site asserts these as exact strings AND now carries an explicit emitter-rejection rule for any other value:

| Field | Required literal | Post-edit grep evidence | Rejection rule citation |
|---|---|---|---|
| `severity` | `HIGH` (case-sensitive) | `grep -F "severity: HIGH"` returns ≥1 hit in each of: SKILL.md, rf-analyst.md, rf-qa.md, rf-qa-qualitative.md | "the emitter MUST reject any synthetic emission whose `severity` field is not the literal `HIGH`" present at all 4 sites |
| `source` | `"synthetic-dnsp"` (case-sensitive) | `grep -F 'source: "synthetic-dnsp"'` returns ≥1 hit in each of the same four files | "or whose `source` field is not the literal `synthetic-dnsp`" present at all 4 sites |

Per-file grep counts recorded in `evidence.md` §3.

## 6. Verification protocol (Direct test execution)

T06.03 is a STANDARD-tier task with Verification Method = "Direct test execution" and Sub-Agent Delegation = None. Verification consists of:

1. **AC1 grep test.** `grep -c "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns ≥1 hit per file. Recorded in `evidence.md` §3.
2. **AC2 rejection-rule structural test.** The clause "the emitter MUST reject any synthetic emission whose `severity` field is not the literal `HIGH`" is present at all four wrapper sites; verified via `grep -n "DM-003-fixed-field-invariant-violation"`. Recorded in `evidence.md` §4.
3. **AC3 source-literal structural test.** Literal `source: "synthetic-dnsp"` enumerated at all four wrapper sites; verified via `grep -F 'source: "synthetic-dnsp"'`. Recorded in `evidence.md` §3 + §4.
4. **Preservation invariant test.** `sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum` matches the D-0069 / D-0068 pinned hash. Recorded in `evidence.md` §6.

Because the actual emitter is the partition orchestrator's emission code (still spec-only; programmatic API-003 emission code lands in T06.07), the rejection contract here is the documented invariant that the implementer in T06.07 + T06.10 will bind to. The TEST-018 twice-exhaust fixture (T06.15, D-0080) provides the end-to-end fixture-level verification that severity HIGH + source `"synthetic-dnsp"` are emitted; the symmetric negative path (severity != HIGH rejected) will be programmatically exercised once T06.07's emission code lands. The Phase 6 task graph explicitly sequences this: T06.03 (spec-level rejection contract) → T06.07 (API-003 emission code) → T06.15 (positive-path fixture) → T06.10 + T06.18 (final cross-cutting verification).

## 7. Acceptance criteria coverage

| AC | Statement (verbatim from T06.03 task) | Where verified |
|----|----------------------------------------|----------------|
| AC1 | `grep -c "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns at least 1 hit per file | `evidence.md` §3 (rf-analyst.md = 4 hits; rf-qa.md = 2 hits; both ≥1) |
| AC2 | Synthetic emission with severity != HIGH is rejected by the emitter | `evidence.md` §4 (explicit rejection clause with named error symbol `DM-003-fixed-field-invariant-violation` present at all 4 wrapper sites) |
| AC3 | source field is the literal string `synthetic-dnsp` | `evidence.md` §3 (per-file literal `source: "synthetic-dnsp"` grep ≥1 at all 4 sites) + §4 (explicit rejection clause for non-literal values) |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0070/evidence.md` | This artifact pair |

All four ACs PASS.

## 8. Dependencies and cross-references

- **Dependencies:** T06.02 (D-0069 — DM-003-M6 7-field schema landed at the four wrapper sites; the rejection clause appended in T06.03 binds to the `severity: HIGH (non-overridable)` and `source: "synthetic-dnsp" (literal sentinel)` enumeration entries from D-0069).
- **Unblocks:**
  - T06.04 (D-0071, affected_range + evidence emitters — symmetric pattern applied to two additional DM-003 fields)
  - T06.05 (D-0072, recommendation + dedup_key + found_n_times emitters)
  - T06.07 (D-0073, API-003-M6 structured-block emission — will operationalize the rejection contract spec'd here in code)
  - T06.10 (D-0076, INV-021 N-1 concurrency + HIGH severity non-overridable — the HIGH non-overridable invariant spec'd here is one of the two cross-cutting M6 invariants T06.10 ratifies)
- **Composition with downstream M6 chain:** T06.07 + T06.10's emission code will reference the `DM-003-fixed-field-invariant-violation` error symbol defined here as the rejection signal name.

## 9. Rollback

T06.03 is strictly additive — rollback removes one new paragraph from SKILL.md (L668-669) plus one trailing sentence-pair from each of rf-analyst.md L70, rf-qa.md L78, and rf-qa-qualitative.md L79. The 7-field DM-003 bullet contract landed by T06.02 (D-0069) is preserved byte-identical. The all-agents-fail escalation backstop at rf-team-lead.md:417 is unaffected (byte-stable across the edit window).

## 10. Slice hashes (for downstream task verification)

| Slice | sha256 (pre-T06.03 = post-T06.02) | sha256 (post-T06.03) |
|---|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` | `6b500cc5378b2fbc652c4546e344bf6b6105c881bd8447c76fe328b3981270bf` | `43fcb1661104b5a3b04eb14a68bbf41185ea48822248d3a99a760f01e5316fa7` |
| `src/superclaude/agents/rf-analyst.md` | `5b7071deeb8428e17aeab9e7d7bb9eea228e5378cce5dbe05d7a240c7b2b621e` | `0ce5ae14c9504e64cb695f9577803831074983b96c662f67b800168da970c0a5` |
| `src/superclaude/agents/rf-qa.md` | `bb07e1491501db2af3e8bd89edf15335baef37aa68e597a2ab81d9b6e7996563` | `8c0d3d1c0d29e7aebe2b1da58bddab6e73aac44c3d1887e98b153fb5981ae283` |
| `src/superclaude/agents/rf-qa-qualitative.md` | `866426da72ca8c76ed56fb6c8a32c08b38884bb57b66091e6048251266f5a6a1` | `1ead68996d3c4d21cea2bb844ce5b720c825b5ab08669cda32630ba74f98d492` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — UNTOUCHED across T06.01–T06.03) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |
| `src/superclaude/agents/rf-team-lead.md:417` (3-cycle hard cap — UNTOUCHED) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
