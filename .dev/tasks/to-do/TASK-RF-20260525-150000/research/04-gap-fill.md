# Research: Gap-Fill Addendum (corrections + empirical fixture findings)

**Topic type:** Gap-Fill
**Scope:** Corrections to research files 01-03 per rf-qa research-gate report (7 MINORs)
**Status:** Complete
**Date:** 2026-05-25
**Source verdict:** rf-qa research-gate FAIL (7 MINOR, 0 CRITICAL, 0 IMPORTANT — substantive content verified correct)

---

## 1. CLAUDE.md citation corrections (addresses minors in 02-patterns-conventions.md §3.1-§3.4 + §5)

Verified by `grep -n` against `/config/workspace/IronClaude/CLAUDE.md`:

| Convention | Cited in 02-patterns-conventions.md | Actual line |
|---|---|---|
| UV-only Python ops ("CRITICAL: this project uses UV for all Python operations…") | "lines 5-15" | **line 7** |
| `.claude/` gitignored sync-dev output ("`.claude/{skills,commands,agents,hooks,templates}/*` is gitignored sync-dev output of `src/superclaude/`") | "lines 21-39" | **line 18** (rule starts) → **lines 18-31** (rule + rationale block) |
| `make sync-dev` workflow ("Run `make sync-dev` to copy changes to `.claude/`") | "lines 86-101" | **lines 95-96** (commands), **lines 117-122** (workflow steps), **line 127** (revert path) |
| Component Sync section heading | "lines 86-101" | starts ~**line 112** |
| Branch policy (feature/fix/docs branches) | "lines 233-241" | (need to re-verify; this section is in the Git Workflow heading further down) |

**Action for builder:** Use the corrected line numbers above when citing CLAUDE.md rules in task items. The rule TEXT in 02-patterns-conventions.md is verbatim-correct; only the line citations drift. None of this affects the implementation — it affects the precision of evidence trails in the generated task file.

## 2. Template line-count correction (addresses minor in 03-template-examples.md line 14)

`wc -l /config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` → **1204 lines** (not 1205). Pure off-by-one in the citation; substance unchanged.

## 3. TUIBBS_HUB_SPEC fixture identifier-content derivation (addresses 01-file-inventory.md §C.2 under-specification) — **CRITICAL ENGINEERING FINDING**

The merged-output.md §3 test t1 asserts "1 hub-dispatch contract" after the merged Fix B's signature-subsumption dedup runs against the TUIBBS hub-dispatch context windows. **Empirical verification of this assertion against the actual TUIBBS-scp epics.md reveals the fixture identifier sets do NOT overlap as the merged spec assumed.** The builder MUST address this in the test fixture or the assertion will fail.

### Identifier sets in the actual TUIBBS context windows

`_extract_identifiers` uses two regexes:
- UPPER_SNAKE_CASE: `\b[A-Z][A-Z0-9_]{2,}\b` (requires 3+ uppercase chars total)
- PascalCase: `\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b` (requires 2+ camelHumps)

Applied to the 7-line context windows around each hub-dispatch evidence line in TUIBBS-scp epics.md:

| IC | Spec line | Context lines | UPPER_SNAKE matches | PascalCase matches | Combined identifier set |
|---|---|---|---|---|---|
| IC-005 | 200 | 197-205 | `ADR`, `WAL`, `MCP`, `ACS`, `NFR`, `S10` (from `FR-S10-02`) | (none multi-hump) | `{ADR, WAL, MCP, ACS, NFR, S10}` |
| IC-008 | 430 | 427-435 | (none — `Interactive`/`Coalescible`/`Bulk`/`Acceptance`/`Criteria` are single-cap) | (none multi-hump) | `∅` (empty set) |
| IC-010 | 1001 | 998-1006 | (TBC by builder — likely contains `FR-S10` IDs and similar) | (likely none) | (TBC) |
| IC-011 | 1031 | 1028-1036 | (none — `Given`/`When`/`Then`/`And` are single-cap) | `PresenceUpdates` (P-resence-U-pdates) | `{PresenceUpdates}` |

### Consequence for merged Fix B subsumption dedup

`_signature_subsumed` collapses sig B into seen sig A iff `B.mechanism == A.mechanism AND B.idents ⊆ A.idents AND B.idents ∩ A.idents ≠ ∅` (OR exact equality). With the empirical TUIBBS sets:
- IC-005 inserted (cardinality 1)
- IC-008 (∅): empty-ident path → `if not idents: return sig in seen` → `(dispatch_table, ∅)` not in seen → INSERTED (cardinality 2)
- IC-011 (`{PresenceUpdates}`): non-empty; `{PresenceUpdates}.issubset({ADR,WAL,MCP,ACS,NFR,S10})` is False; not subsumed by IC-005's empty set either → INSERTED (cardinality 3)

**Result: 3 hub-dispatch contracts survive merged Fix B's dedup against raw TUIBBS-scp content, not 1.**

The gate STILL passes because Layer 1 of the coverage check (dispatch_family regex) matches `class-priority dispatch` on roadmap.md:392 → all 3 contracts are COVERED → uncovered_count=0. **The diagnosis-time empirical claim ("Fix B greens the TUIBBS-scp case") holds, but for a different reason than merged-output.md §2.3 documented.**

### Builder remediation options (pick ONE in Phase 2 implementation):

| Option | What it does | Trade-off |
|---|---|---|
| **A. Fixture-engineered (recommended)** | Author `TUIBBS_HUB_SPEC` as a 30-40 line synthetic fixture that REUSES TUIBBS prose but adds at least 1 shared UPPER_SNAKE identifier (e.g., `FR-S10-02`, `HUB_CLASS`, `ADR_X1`) in every hub-dispatch context window so subsumption fires. Test t1 asserts "1 hub-dispatch contract" as merged-output.md specified. | Fixture is synthetic, not verbatim; the test verifies the design's INTENT not the empirical TUIBBS-scp case. |
| **B. Assertion-relaxed** | Use verbatim TUIBBS-scp excerpts; assert "≤4 hub-dispatch contracts (down from raw extractor's 4)" and assert `uncovered_count == 0` (the load-bearing claim). Add a separate test on synthetic fixture for the "1 contract per mechanism" intent. | More tests; assertion t1 weakens to a bound rather than equality. |
| **C. Implementation-strengthened** | Extend `_signature_subsumed` so empty-identifier sets get subsumed by ANY same-mechanism sig (not just other empty ones). | Changes the merged-output.md spec; needs adversarial re-validation. |

**Builder recommendation: Option A.** Synthetic fixture with explicit shared identifiers most faithfully tests merged-output.md §2.3 intent without diluting test signal. Document the choice in the task file's "Resolved Questions" section.

### Specific identifier-shape constraint for the synthetic fixture (if Option A)

Include `FR-S10-02` (or any 3+ char UPPER_SNAKE token) in each of the 3-4 hub-dispatch evidence-line windows in `TUIBBS_HUB_SPEC`. The shared identifier set across all windows must have at least one element; subsumption then fires regardless of asymmetric additions in any single window.

## 4. Builder-facing instruction

When generating the task file, the builder MUST:

1. Use the corrected CLAUDE.md line numbers from §1 above in any task items that cite project rules.
2. Use 1204 (not 1205) when citing the Template 02 line count.
3. Surface the §3 finding in a "Resolved Questions" section near the top of the task file. Cite all three remediation options and lock in Option A (fixture-engineered) unless the executor explicitly chooses otherwise during execution.
4. Make the t1 fixture-authoring item explicit about the identifier-shape constraint (`FR-S10-02` or equivalent in every window).
5. Add a Phase-2 verification item that re-runs the live integration_contracts check against the actual TUIBBS-scp epics.md/roadmap.md (BEFORE Fix A) and asserts `uncovered_count == 0` — this verifies the END-TO-END behavior, while t1-t7 verify the INTENDED design behavior on synthetic fixtures.

## Summary

7 MINOR rf-qa findings addressed:
- 5 line-number citation corrections (cosmetic; rule text correct)
- 1 template line-count off-by-one (cosmetic)
- 1 fixture identifier under-specification → escalated to ENGINEERING finding requiring builder decision (Option A recommended)

The substantive content of research files 01-03 remains correct and actionable. The builder may proceed to A.9 with this addendum loaded alongside the original files.
