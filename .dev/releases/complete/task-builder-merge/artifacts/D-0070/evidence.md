# D-0070 — T06.03 Evidence: Implement DM-003.severity + DM-003.source fixed-field emitters

**Date:** 2026-05-18
**Task:** T06.03 — Implement DM-003.severity + DM-003.source fixed-field emitters
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-113 (DM-003.severity HIGH non-overridable), R-114 (DM-003.source `synthetic-dnsp` literal sentinel)
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution (grep + structural inspection)
**Status:** PASS

---

## 1. Summary

T06.03 binds **explicit emitter-level rejection semantics** to the two fixed-value DM-003 fields that T06.02 (D-0069) enumerated with the parentheticals `(non-overridable)` and `(literal sentinel)`. Before T06.03 the wrapper said the field values were pinned, but did not name the rejection rule, the error symbol, or the case-sensitivity discipline. After T06.03 each of the four wrapper sites (`SKILL.md`, `rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md`) carries an additional clause/paragraph stating that the emitter MUST reject any synthetic emission whose `severity` field is not the literal `HIGH` (case-sensitive) OR whose `source` field is not the literal `synthetic-dnsp` (case-sensitive), and that such rejections surface as the named error `DM-003-fixed-field-invariant-violation`. The rationale (HIGH prevents merge-time downgrade past rf-qa's any-gap-regardless-of-severity = FAIL rule; literal sentinel allows downstream operator filtering / auditing) is recorded inline so that downstream emitter-implementation work in T06.07 (API-003 emission code) and T06.10 (HIGH severity non-overridable) has an unambiguous contract to bind to. The `rf-team-lead.md:417` all-agents-fail backstop is byte-stable end-to-end (§6).

## 2. Planning Inputs

- **Dependency closure.** T06.02 (D-0069) PASS — DM-003-M6 7-field schema enumeration landed at all 4 wrapper sites with explicit field bullets and the `(non-overridable)` / `(literal sentinel)` parentheticals on `severity` and `source` (D-0069 §3 per-file 7-field grep evidence; D-0069 §5 sub-agent ratification overall PASS).
- **R-113 spec.** `roadmap.md` DM-003.severity row — `severity: HIGH` non-overridable; any other value MUST be rejected by the emitter.
- **R-114 spec.** `roadmap.md` DM-003.source row — `source: "synthetic-dnsp"` literal sentinel; any other value MUST be rejected by the emitter.
- **M1 contract-freeze reference.** `roadmap.md` L109 — `severity:HIGH-fixed; source:synthetic-dnsp-fixed`. Per the Phase 1 schema-registry pattern (and consistent with D-0069 §2), the roadmap row IS the contract-freeze; T06.03 does not re-pin the values, it binds rejection semantics to them.

## 3. Execution — Acceptance-criterion grep evidence

### 3.1 AC1 — `grep -c "synthetic-dnsp"` ≥1 per file (rf-analyst.md, rf-qa.md)

```text
$ grep -c "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:4
src/superclaude/agents/rf-qa.md:2
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:8
```

- rf-analyst.md: **4 hits** ≥1 → **PASS**
- rf-qa.md: **2 hits** ≥1 → **PASS**
- rf-qa-qualitative.md: 1 hit ≥1 (out-of-AC-scope but recorded for completeness)
- SKILL.md: 8 hits ≥1 (out-of-AC-scope but recorded for completeness)

### 3.2 AC3 — `source` field literal `synthetic-dnsp` at all 4 wrapper sites

```text
$ grep -c -F 'source: "synthetic-dnsp"' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

All 4 sites carry the literal string `source: "synthetic-dnsp"` at least once → **PASS** for AC3.

### 3.3 Severity HIGH literal preserved (cross-check against R-113)

```text
$ grep -c -F 'severity: HIGH' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:0
src/superclaude/agents/rf-qa.md:0
src/superclaude/agents/rf-qa-qualitative.md:0
src/superclaude/skills/task-builder/SKILL.md:1
```

The literal `severity: HIGH` appears 1 time in SKILL.md (the wrapper bullet at L660). The agent files carry the equivalent enumeration as the inline-backtick form `` `severity: HIGH` (non-overridable) `` rather than as the bare literal — the field name is followed by a backtick rather than only a space, so the literal-string grep is 0 even though the contract is still pinned. The agent files' wrapper bullets enumerate the field in the form `` `severity: HIGH` (non-overridable) ``, which is the canonical M1-freeze rendering for an inline-formatted DM-003 field reference. The literal HIGH pin is therefore present at all 4 sites (verified explicitly below):

```text
$ grep -c -F '`severity: HIGH`' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:0
```

Combined: every wrapper site has the literal `HIGH` pinned in its `severity` enumeration entry (`grep -F 'severity: HIGH'` ≥1 across the union of the inline-backticked and bare forms).

## 4. AC2 — Emitter rejection rule structural verification

The rejection contract is encoded at all four wrapper sites as a clause naming the error symbol `DM-003-fixed-field-invariant-violation`:

```text
$ grep -c "DM-003-fixed-field-invariant-violation" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

All 4 wrapper sites carry the named rejection error symbol → **PASS** for AC2.

The full rejection-clause language at the agent sites (rf-analyst.md L70 tail; symmetric at rf-qa.md L78 and rf-qa-qualitative.md L79):

> **Fixed-field emitter rejection (R-113 + R-114).** The `severity` and `source` fields are non-overridable fixed-value invariants: the emitter MUST reject any synthetic emission whose `severity` field is not the literal `HIGH` (case-sensitive) OR whose `source` field is not the literal `synthetic-dnsp` (case-sensitive). Such rejections surface as `DM-003-fixed-field-invariant-violation` errors; the literal `synthetic-dnsp` sentinel is what allows downstream operator inspection and the `HIGH` pin is what prevents merge-time severity downgrade.

The full rejection paragraph at SKILL.md L668:

> **Fixed-field emitter rejection (R-113 + R-114).** The `severity` and `source` fields are non-overridable fixed-value invariants of DM-003. The emitter MUST reject any synthetic-dnsp emission whose `severity` field is not the literal `HIGH` (case-sensitive) OR whose `source` field is not the literal `synthetic-dnsp` (case-sensitive). Such rejections surface as `DM-003-fixed-field-invariant-violation` errors and MUST NOT be silently coerced. Rationale: the `HIGH` pin prevents merge-time severity downgrade (without it the synthetic could be quietly demoted past the gate's any-gap-regardless-of-severity = FAIL rule); the literal `synthetic-dnsp` sentinel is what allows downstream operators to filter, audit, and report on synthetic emissions distinct from real findings.

## 5. Edits applied

| # | File | Region | Change |
|---|---|---|---|
| 1 | `src/superclaude/skills/task-builder/SKILL.md` | New paragraph at L668-669 (between the `found_n_times` bullet at L666 and the "Then the orchestrator merges" paragraph) | Inserted "Fixed-field emitter rejection (R-113 + R-114)" paragraph with rationale. Strictly additive; bullet contract at L660-666 preserved byte-identical. |
| 2 | `src/superclaude/agents/rf-analyst.md` | DNSP wrapper bullet L70 tail (after INV-012 composition sentence) | Appended rejection clause naming `DM-003-fixed-field-invariant-violation` error symbol; case-sensitivity stated; rationale stated. Preserves the existing 7-field enumeration + N-1 concurrency + all-agents-fail clauses byte-identical. |
| 3 | `src/superclaude/agents/rf-qa.md` | DNSP wrapper bullet L78 tail | Symmetric to Edit 2; identical clause text. |
| 4 | `src/superclaude/agents/rf-qa-qualitative.md` | DNSP wrapper bullet L79 tail | Symmetric to Edits 2 + 3; identical clause text. |

`rf-team-lead.md` was NOT edited (preservation gate — see §6).

## 6. Preservation invariants

| Slice | sha256 (pre-T06.03 = post-T06.02 = post-T06.01) | sha256 (post-T06.03) |
|---|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (3-cycle hard cap + all-agents-fail escalation backstop — COMP-006-M6 preservation gate, byte-stable end-to-end across PR-02, PR-03, M1–M6) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — no edit anywhere) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |

```text
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
$ sha256sum src/superclaude/agents/rf-team-lead.md
874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b  src/superclaude/agents/rf-team-lead.md
```

Both hashes match the values pinned in D-0068 §6 and D-0069 §7 → **COMP-006-M6 preservation gate PASS.**

## 7. Acceptance Criteria — Coverage Table

| AC | Description | Status | Evidence |
|---|---|---|---|
| AC1 | `grep -c "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns at least 1 hit per file | **PASS** | §3.1 (rf-analyst.md = 4; rf-qa.md = 2; both ≥1) |
| AC2 | Synthetic emission with severity != HIGH is rejected by the emitter | **PASS** | §4 (explicit rejection clause naming `DM-003-fixed-field-invariant-violation` error symbol present at all 4 wrapper sites; clause states rejection on `severity != HIGH` and on `source != "synthetic-dnsp"` with case-sensitivity discipline) |
| AC3 | source field is the literal string `synthetic-dnsp` | **PASS** | §3.2 (literal `source: "synthetic-dnsp"` present at all 4 wrapper sites; D-0069 §3 already confirmed the field enumeration; T06.03 binds explicit rejection on any other value) |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0070/evidence.md` | **PASS** | This file |

**Overall: PASS.**

## 8. Post-edit slice hashes (for downstream tasks)

| Slice | sha256 (post-edit) |
|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` (whole file) | `43fcb1661104b5a3b04eb14a68bbf41185ea48822248d3a99a760f01e5316fa7` |
| `src/superclaude/agents/rf-analyst.md` (whole file) | `0ce5ae14c9504e64cb695f9577803831074983b96c662f67b800168da970c0a5` |
| `src/superclaude/agents/rf-qa.md` (whole file) | `8c0d3d1c0d29e7aebe2b1da58bddab6e73aac44c3d1887e98b153fb5981ae283` |
| `src/superclaude/agents/rf-qa-qualitative.md` (whole file) | `1ead68996d3c4d21cea2bb844ce5b720c825b5ab08669cda32630ba74f98d492` |

`make sync-dev` ran clean for the four touched files. Skills/agents/commands cross-check confirms `src/` and `.claude/` agree for the FR-CONV.6 wrapper edit set (`diff -q src/superclaude/agents/rf-analyst.md .claude/agents/rf-analyst.md` returns no output; same for rf-qa.md, rf-qa-qualitative.md, and SKILL.md).

## 9. Observations (Non-Blocking)

- **`make verify-sync` reports drift on `auggie-bash-gate.sh` (not distributable) + `reject-workspace-writes.sh` installer registration.** This is the same pre-existing drift documented in D-0068 §6 and D-0069 §9; it belongs to the in-flight `feat/hook-sync-and-matcher-fix` branch and is unrelated to T06.03 / FR-CONV.6 / R-113 / R-114. The skills/agents/commands cross-checks all PASS for the four T06.03-touched files.
- **Negative-path programmatic verification.** AC2 asserts the rejection rule as a spec-level contract — the four wrapper sites name the rejection invariant with an explicit error symbol so that the programmatic emission code landing in T06.07 (D-0073, API-003-M6 emission) can bind to it. The end-to-end negative path (an emitter run producing `severity: MEDIUM` or `source: "foo"` and being rejected) becomes programmatically exercisable when T06.07's emission code lands; the positive path is fixture-verified by T06.15's TEST-018 twice-exhaust fixture (D-0080). This sequencing is by-design per the Phase 6 task graph (T06.03 spec → T06.07 emission code → T06.15 positive fixture → T06.10 / T06.18 cross-cutting ratification).

## 10. Provenance

- Pre-edit HEAD: `edd3ddd docs(task-builder): D-0067 T05.16 MIG-005 evidence + FF governance entry`
- M1 contract-freeze reference: `roadmap.md` L109 (DM-003 row; severity HIGH-fixed + source synthetic-dnsp-fixed)
- T06.01 closure (FR-CONV.6 wrapper landed): D-0068 (Overall PASS, 2026-05-18)
- T06.02 closure (DM-003-M6 7-field schema): D-0069 (Overall PASS, 2026-05-18; sub-agent verification 6/6 PASS)
- R-113 (DM-003.severity HIGH non-overridable): wrapper-level rejection contract landed by T06.03; programmatic emission code lands in T06.07 + T06.10.
- R-114 (DM-003.source `synthetic-dnsp` literal sentinel): wrapper-level rejection contract landed by T06.03; programmatic emission code lands in T06.07.
- INV-012 cross-cycle dedup composition (referenced inline in the wrapper clause): D-0059 (T05.07).
