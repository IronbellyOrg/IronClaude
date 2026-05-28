# D-0034 — T03.10 Spec: COMP-004-M3 rf-qa-qualitative EOF Append

**Task:** T03.10 (Phase 3)
**Roadmap items:** R-062
**Date:** 2026-05-17
**Component edited:** `src/superclaude/agents/rf-qa-qualitative.md`
**Mirror:** `.claude/agents/rf-qa-qualitative.md` (synced via `make sync-dev`)

---

## 1. Edit-site specification

| Field | Value |
|---|---|
| Surface | `rf-qa-qualitative.md` EOF append |
| New section heading | `## Handling the Inherited Structural Verdict` |
| Output-schema heading added | `## Self-Audit` (literal, inside the new section's schema fence) |
| Pre-edit file length | 889 lines |
| Post-edit file length | 964 lines (appended 75 lines including blank-line and `---` separator) |
| Byte-stable region | rf-qa-qualitative.md:766-775 (Confidence Gate Protocol — Step 1 markers + Step 2 count) |

The phase-3 tasklist (L455-503) names the byte-stable region as the "anti-inflation block" / "Prohibited Behaviors block at :766-775". The actual *Prohibited Behaviors* heading in the current file lives at line 791 (post-T03.04 line numbering); the cited :766-775 range covers the Step 1 categorisation markers and Step 2 count block of the Confidence Gate Protocol — both of which are the structural scaffolding the anti-inflation rule operates on. T03.10 preserves that scaffolding byte-for-byte and appends new consumer-handling content well past EOF (line 890+), guaranteeing zero byte-diff in the cited region.

## 2. Content appended at EOF (lines 890-964)

Two structural surfaces:

1. **`## Handling the Inherited Structural Verdict`** (line 893) — new H2 section documenting the consumer-side handling rules required when FR-CONV.3 / PR-04 Gate Results Passthrough is active. Five numbered behaviours: PASS reliance + semantic counterpart, FAIL escalation, missing/malformed fallback, INV-002 fix-cycle freshness, INV-019 Self-Audit obligation.
2. **`## Self-Audit` schema fence** (line 935, inside the fenced code block of the new section) — literal `## Self-Audit` heading inside a markdown fence so the consumer schema is unambiguous and `grep -n "## Self-Audit"` finds the canonical output-template realisation alongside the existing `## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)` entry in the live Output Format template (line 728).

The new section closes with an **Anti-inflation invariant (T03.08, byte-stable)** stanza that cites the :766-775 region by line range and forbids weakening, removing, paraphrasing, or relocating the Prohibited Behaviors block.

## 3. Rollback procedure

Per release-spec §19.4 (passthrough flag disable):

1. Disable `FF_INHERITED_STRUCTURAL_VERDICT` in feature-flag governance (MIG-003 / T03.16 single-commit landing controls the flag wire-up).
2. The agent falls back to independent structural re-checking (Critical Rule #11 standalone clause).
3. The appended sections at EOF can remain (they are inert when the flag is OFF — they only describe consumer behaviour for active-flag runs).
4. Alternatively, revert the single commit landing this edit (no other surface dependencies).

## 4. Cross-references

- Anti-inflation invariant authority: T03.08 (D-0032) preservation gate.
- Producer-side splice: T03.09 (D-0033) — SKILL.md §A.10.5 `## Inherited Structural Verdict` block.
- Output schema realisation: `## Output Format (All Phases)` → `## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)` at rf-qa-qualitative.md:728.
- INV-019 fixture: TEST-009 (T03.14) — `tests/audit/test_self_audit_inv_019.py`.
- Critical Rule #11 (rf-qa-qualitative.md:819): consumer obligation pointer.
- Self-Audit Schema Requirement section (rf-qa-qualitative.md:823) — T03.04 / D-0029 prior surface.
