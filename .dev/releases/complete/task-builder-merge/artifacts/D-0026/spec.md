# D-0026 — T03.01 Spec: FR-CONV.3 Inherited Verdict + Self-Audit Wrapper

**Task:** T03.01 (Phase 3)
**Roadmap items:** R-049
**Date:** 2026-05-17
**Status:** PASS (wrapper already landed at commit `3a57a0d`; verified for M3 entry)

---

## 1. Scope

T03.01 lands the FR-CONV.3 wrapper across `SKILL.md` (A.10.5 spawn-prompt
block) and `rf-qa-qualitative.md` (Critical Rule #11 + output-schema
Reliance Audit subsection). The wrapper operationalises the
`## Inherited Structural Verdict` passthrough between rf-qa (A.10
producer) and rf-qa-qualitative (A.10.5 consumer), and introduces the
`## Self-Audit` consumer-side reliance-vs-verification accounting
required by INV-019.

The wrapper IS the framework that subsequent Phase-3 tasks fill in:
- **T03.02 / DM-002-M3** populates the wrapper's 3-field schema
  (`rf_qa_table_verbatim`, `prompt_directive`, `reinjection_rule`).
- **T03.03 / API-002-M3** wires orchestrator extraction + splice at
  SKILL.md §A.10.5.
- **T03.04 / Self-Audit schema** formalises the consumer obligation
  inside rf-qa-qualitative's output template.
- **T03.05 / INV-002 freshness** enforces cycle-N re-injection.
- **T03.08 / anti-inflation preservation** asserts the Prohibited
  Behaviors block stays byte-stable.

T03.01 itself is the "wrapper is present and zero-trust-preserving"
gate that unblocks all of the above.

## 2. Wrapper anatomy

### 2.1 Producer side — SKILL.md §A.10.5

Three insertion regions, all landed at commit `3a57a0d`:

| Region | Lines (post-MIG-002) | Purpose |
|---|---|---|
| Directive prose | 1100 | Orchestrator instruction: read rf-qa report, extract Items Reviewed table verbatim, embed as `## Inherited Structural Verdict`, INV-010 dynamic enumeration, INV-002 freshness re-injection, fallback path |
| Embedded prompt heading | 1111 | `## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)` inside the spawn-prompt block |
| Anti-inflation directive | 1126-1132 | `ANTI-INFLATION RULE: ... Reliance is not verification. Your Self-Audit MUST list (a) ... and (b) at least one semantic check where rf-qa PASS was INSUFFICIENT ... (INV-019).` |

Additionally, lines 1226 + 1242 publish the DM-005 phase-contract
references to the `Inherited Structural Verdict block` artifact name
(M2 publication consumed by M3, per phase-3 M3 entry condition).

### 2.2 Consumer side — rf-qa-qualitative.md

Two insertion regions, both landed at commit `3a57a0d`:

| Region | Lines (post-MIG-002) | Purpose |
|---|---|---|
| Output-schema Reliance Audit | 728-733 | `## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)` mandatory subsection; lists relied-on rf-qa PASS items + named semantic counterpart verified by own tool engagement |
| Critical Rule #11 rewrite | 819 | Pre-wrapper Rule #11 was an aspirational "complement, don't replace" division-of-labour statement; post-wrapper rule names the concrete `## Inherited Structural Verdict` delivery mechanism, escalates FAIL handling to HIGH severity, binds reliance≠verification to Self-Audit format (a)+(b), preserves standalone fallback |

The pre-existing **anti-inflation language** in the `### Prohibited
Behaviors` block of the Confidence Gate Protocol (lines 791-800,
specifically line 795: "NEVER mark an item VERIFIED if you only read
about it in another report — that is RELIANCE, not VERIFICATION") is
**not touched** by the wrapper hunks; the wrapper reinforces this rule
from the spawn-prompt side rather than restating it on the consumer
side.

## 3. Invariants enforced by the wrapper

| Invariant | Enforcement site | Wrapper guarantee |
|---|---|---|
| INV-002 (freshness) | SKILL.md 1100 directive | Orchestrator re-reads `qa-task-validation-report.md` on every fix-cycle re-spawn; stale verdicts forbidden. T03.05 + TEST-008 enforce. |
| INV-010 (dynamic enumeration) | SKILL.md 1100 directive | Wrapper enumerates TB-Add-* live from rf-qa.md checklist rather than hard-coding the list. T03.07 + TEST-010 enforce. |
| INV-019 (Self-Audit obligation) | SKILL.md 1126-1132 + rf-qa-qualitative.md 728-733 | Consumer output MUST list (a) relied-on PASS items + (b) ≥1 semantic check where PASS was insufficient. T03.04 + TEST-009 enforce. |
| Anti-inflation preservation | rf-qa-qualitative.md 791-800 (untouched by wrapper) | Prohibited Behaviors block byte-stable; reliance ≠ verification rule survives wrapper landing. T03.08 enforces. |
| Fallback when verdict missing | SKILL.md 1100 directive | rf-qa-qualitative falls back to standalone behavior; passthrough is "optimization, not a dependency". |

## 4. Why the wrapper was already landed at `3a57a0d`

Commit `3a57a0d` ("PR-04 gate-results passthrough") landed the wrapper
during the prompt-refactor cycle that fed this release. The release
spec calls this out: M3 builds on the wrapper that PR-04 established.
T03.01 is the formal verification gate that the wrapper is present,
unchanged in src↔mirror parity, and zero-trust-preserving as required
by Phase 3's entry conditions.

Any future modification to the wrapper structure must go through one of
the subsequent Phase-3 tasks (T03.02–T03.10), each of which has its own
acceptance criteria and sub-agent verification.

## 5. Rollback path

As stated in roadmap row R-049: **disable passthrough flag; fall back
to independent structural re-checking.** Mechanically:

1. In SKILL.md §A.10.5, comment out the "Inherited Structural Verdict"
   directive paragraph (line 1100) and the embedded `## Inherited
   Structural Verdict` block inside the QA prompt (lines 1111-1132).
2. The rf-qa-qualitative output template's Reliance Audit subsection
   (lines 728-733) becomes inert when the spawn prompt no longer
   carries an Inherited Structural Verdict — the subsection wording
   already conditions on its presence ("Required when the spawn prompt
   included an `## Inherited Structural Verdict` section").
3. Critical Rule #11 at line 819 retains the strengthened wording but
   loses its enforcement hook — consumer falls back to the pre-wrapper
   complement-don't-replace behavior.

`FF_INHERITED_STRUCTURAL_VERDICT` is the logical feature-flag governing
this passthrough; cleanup is consolidated in M7 (release-spec §8.3 row 4).

## 6. Cross-references

- Phase 3 task spec: `.dev/releases/current/task-builder-merge/phase-3-tasklist.md` T03.01
- Roadmap row: `roadmap.md` line 208 (M3 row 1) + lines 217-218 (INV-019, anti-inflation preservation)
- Release spec: `release-spec.md` §4.6 (sequencing), §8.3 (governance)
- Quality-engineer verdict: `D-0026/quality-engineer-report.md` (PASS)
- Sub-agent evidence: `D-0026/evidence.md`
