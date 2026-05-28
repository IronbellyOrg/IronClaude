# Research Completeness Verification

**Topic:** Hybrid cosmetic-remediator fix — C12 (H2 parenthetical strip) + C13 (gap-driven H3 repair under Resource Requirements and Dependencies)
**Date:** 2026-05-27
**Files analyzed:** 3 (01-file-inventory.md, 02-patterns-conventions.md, 03-test-verification.md)
**Depth tier:** Quick (single-track build)
**Analyst:** rf-analyst (sole instance — no partition)

---

## Verdict: PASS (1 important gap, 3 minor gaps — see Compiled Gaps below)

---

## Checklist Evaluation (9 criteria)

### Criterion 1: Coverage audit — every key source file identified in scope appears in research

**Scope (from TRACK GOAL):** `cosmetic_remediator.py` (transformer + dispatcher), `gates.py` (`_REQUIRED_H2_SECTIONS`, `_REQUIRED_RESOURCE_SUBSECTIONS`), test infrastructure, validation REPORT context.

| Scope item | Covered by | Status |
|---|---|---|
| `src/superclaude/cli/roadmap/cosmetic_remediator.py` (831 lines) | 01-file-inventory.md §A (lines 14-82); 02-patterns-conventions.md throughout | COVERED |
| `src/superclaude/cli/roadmap/gates.py` — `_REQUIRED_H2_SECTIONS` @ 891 | 01-file-inventory.md §B.1 (line 89); 02 §6 (line 195) | COVERED |
| `src/superclaude/cli/roadmap/gates.py` — `_REQUIRED_RESOURCE_SUBSECTIONS` @ 914 | 01 §B.1 (line 91); 02 §6 (line 195) | COVERED |
| `_template_sections_present` @ gates.py:927 (the gate C12+C13 unblock) | 01 §B.2 (line 97); 03 §4 (lines 157-191) | COVERED |
| `apply_cosmetic_remediations` dispatcher | 01 §A.4 (lines 54-65); 02 §2 (lines 53-72); 02 §10 (lines 266-287) | COVERED |
| `_apply_resource_subsection_rewrites` (closest analog) | 01 §A.3 (line 51); 02 §1 (line 34); 02 §6 (line 175) | COVERED |
| `_compute_fenced_indices` / fence-skip helper | 01 §A.3 (line 41); 02 §4 (lines 102-130) | COVERED |
| `_strip_section_numbering` / `_normalize_heading` divergence | 01 §B.2 (line 96) + §C drift flag (line 118); 02 §5 | COVERED |
| `tests/roadmap/test_cosmetic_remediator.py` (428 lines, 21 tests) | 03 §1 (entire table), §3, §5 | COVERED |
| `tests/roadmap/test_gates_data.py` — `_minimal_valid_roadmap` helper | 03 §4 (line 160); 03 §8 (lines 346-360) | COVERED |
| Validation REPORT reproducer (`validation-opus-mixed-drift-20260527023700/REPORT.md`) | 03 §8 (lines 278-345) | COVERED |

**Verdict: PASS.** All in-scope files and the integration-gap evidence point are covered with `file:line` evidence.

---

### Criterion 2: Evidence quality — every finding cites specific file paths / line numbers / function names

| File | Evidenced claims | Unsupported claims | Quality |
|---|---|---|---|
| 01-file-inventory.md | 40+ (every row in §A.1-A.5, §B.1-B.3 tables has `file:line`; drift-flag §C cites grep evidence) | 0 | Strong |
| 02-patterns-conventions.md | 30+ (every §1-§10 section quotes code blocks with `file:line` headers; gotcha §11 cites both files) | 0 | Strong |
| 03-test-verification.md | 25+ (test inventory table has `file:line`; reproducer §8 cites `REPORT.md:36-47` verbatim; baseline runtime shows actual pytest output) | 0 | Strong |

**Verdict: PASS.** Zero vague/unsupported claims detected; every architectural assertion is grounded in a specific symbol/line.

---

### Criterion 3: Documentation staleness — doc-sourced claims tagged with verification status

No `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tags appear in any of the three files. However, this is **acceptable here** because every claim is sourced directly from primary code (`cosmetic_remediator.py`, `gates.py`, `test_cosmetic_remediator.py`) and the validation REPORT (a co-located evidence artifact, not stale docs). There are no docs/README/architectural-overview claims being asserted — the entire corpus is code-traced.

One borderline case: 02 §11 ("Gotcha") asserts an inconsistency between `_NONCANONICAL_DASH_PATTERN` (cosmetic_remediator.py:95) and the gate accept-set (gates.py:993-998). Both sides quote source code with `file:line` — this is code-vs-code, not doc-vs-code. Properly flagged as out-of-scope.

**Verdict: PASS.** No doc-sourced claims requiring verification tags exist in this corpus; all assertions are code-traced.

---

### Criterion 4: Completeness — Status: Complete + Summary + Gaps assessment

| File | Status header | Summary section | Gaps/Questions section | Key takeaways |
|---|---|---|---|---|
| 01-file-inventory.md | `**Status:** Complete` (line 4) | `## Summary` (line 138) | Drift flags §C serve as gap-equivalent | YES (Summary paragraph) |
| 02-patterns-conventions.md | `**Status:** Complete` (line 4); also explicit closing `## Status: Complete` (line 314) | `**Summary:**` (line 316) | "Gotcha (out of scope, flag-only)" §11 | YES (5 bullets in Summary) |
| 03-test-verification.md | `**Status:** Complete` (line 3); closing `**Status:** Complete.` (line 373) | `## Summary` (line 364) | §4 explicitly labeled "CRITICAL ABSENCE FINDING"; §2 documents helper gap | YES (6 bullets in Summary) |

**Verdict: PASS.** All three files are flagged Complete with substantive summaries; gaps are surfaced as drift flags / "critical absence" findings / "gotcha" sections rather than a literal "Gaps and Questions" heading, but they serve the same role and are clearly demarcated.

---

### Criterion 5: Cross-reference — when one file's findings reference another's domain, the cross-reference is noted

- 01 §C (drift flags) explicitly references gates.py:919-924 divergence that 02 §5 then exploits in the C12 design rationale. Both files independently arrive at the same insight (the parenthetical-strip gap), and 02 §5 mentions "Mirrors `gates._normalize_heading`'s prefix logic" — explicit cross-reference.
- 02 §6 (substring vs exact match) references `gates._REQUIRED_RESOURCE_SUBSECTIONS` (`gates.py:914-916`) as the source-of-truth set C13 must consult. This cross-references 01 §B.1.
- 03 §4 (integration gap) explicitly cross-references the validation REPORT's reproducer; 03 §8 quotes the REPORT verbatim and builds the new integration test from it.
- 03 §3 references C11 test (`test_cosmetic_remediator.py:294-316`) as the closest analog for C12+C13 — paralleling 01 §A.3's note that `_apply_resource_subsection_rewrites` is the closest existing transformer analog.

All three files converge on the same underlying insight: the alias-table approach (C11) cannot catch zero-overlap drift ("External library lockset"), and the gate (`_template_sections_present`) is the integration boundary that has never been tested against remediator output.

**Verdict: PASS.** Cross-references are present and consistent across the three files.

---

### Criterion 6: Contradiction detection — do research files contradict each other?

Direct comparison of overlapping claims:

| Claim | File A | File B | Consistent? |
|---|---|---|---|
| C12 dispatcher position relative to C11 | 01 §D recommends "between C4 (line 795) and C11 (line 799)" (i.e., BEFORE C11) | 02 §10 places C12 at "slot 2.5 (between current step 2 and step 3)" — current step 2 is C11 — placing C12 AFTER C11 | **CONTRADICTION** (ordering) |
| Closest existing transformer analog | 01 §A.3 + §D: `_apply_resource_subsection_rewrites` | 02 §1: same (`_apply_resource_subsection_rewrites`) | Consistent |
| Fence-skip is mandatory | 02 §4 | 03 (implied via C11 test pattern reuse) | Consistent |
| Idempotency contract | 02 §3 | 03 §5 | Consistent |
| Source of canonical H3 set for C13 | 01 §D: `_REQUIRED_RESOURCE_SUBSECTIONS` (gates.py:914) | 02 §6: same | Consistent |

**Contradiction detail (C12 dispatcher position):**

- 01 §D suggests C12 goes between C4 and C11 in the dispatcher (line 795 → C12 → line 799) — rationale: "C12 must precede any transformer that uses the C12-stripped H2 text for parent-section tracking" (01:128).
- 02 §10 places C12 at "slot 2.5" with the slot list showing C11 as step 2 and the new slot 2.5 AFTER C11 — but the rationale at 02:284 says "C12 modifies H2 lines whose text is consulted by C13's gap detection" (implying C12 must precede C13, but is silent on the C11 ordering).

This is a real ambiguity the implementer will hit. C11 walks H2 lines to detect the `## Resource Requirements and Dependencies` parent at `cosmetic_remediator.py:466` (which calls `_strip_section_numbering(h2m.group(1)).lower().strip()` per 02 §5); `_strip_section_numbering` does NOT strip parentheticals (01 §C confirms this — only numbering). Therefore if the parent H2 has a parenthetical (e.g., `## Resource Requirements and Dependencies (Engineering Owned)`), C11's parent-detection would fail unless C12 has already canonicalized the parent. **C12 MUST run before C11** — 01 §D is correct; 02 §10's slot-numbering is a documentation bug in file 02.

**Severity:** Important (not Critical) — both files identify C12 placement as a real ordering concern. The correct chain is C12 → C11 → C13. Synthesis must resolve to 01 §D's ordering and update 02 §10's slot list accordingly.

---

### Criterion 7: Gap compilation

**Critical gaps (block synthesis):** None.

**Important gaps (affect quality):**

1. **Dispatcher ordering contradiction between 01 §D and 02 §10** — must be resolved to C12 → C11 → C13 (rationale: C11's parent-H2 detection at cosmetic_remediator.py:466 cannot strip parentheticals, so C12 must canonicalize the parent H2 first). Task file must explicitly fix the dispatcher branch order AND the docstring step list (cosmetic_remediator.py:777-786) to the 9-step order: 1. C1-C4 milestone H3, **2. C12 (H2 parenthetical strip)**, 3. C11 (resource H3 alias), **4. C13 (gap-driven H3 repair)**, 5. C5+C6, 6. C7, 7. C8, 8. C9, 9. C10.

**Minor gaps (must still be fixed):**

2. **C13 synthesized-placeholder H3 body shape not fully specified.** 02 §11 (gotcha) flags `—` em-dash vs `--` consistency for milestone H3s; 02 §8 suggests the C13 audit-log shape. But neither file specifies: (a) Is the insertion just the H3 line, or H3 + an empty body line? (b) Where exactly under the parent H2 — immediately after the H2's blank line, or after the last canonical H3 already present? The implementer needs this pinned.

3. **Test helper sharing strategy not chosen.** 03 §8 (line 360) suggests two alternatives for the `_minimal_valid_roadmap` builder at `test_gates_data.py:357-422`: (a) lift to `tests/roadmap/conftest.py` as a fixture, or (b) cross-file import from `test_gates_data.py`. The task file should pick one to avoid implementer churn.

4. **C12 detector insertion site is a 2-line window.** 01 §D recommends "after the C10 frontmatter block (line 454) and before the C11 resource section block (line 456)" — natural but should be re-confirmed at implementation time via grep, since detector layout may shift slightly during implementation.

---

### Criterion 8: Depth assessment

**Expected depth:** Quick tier (single-track build).
**Actual depth achieved:** Quick tier well-executed. File inventory is exhaustive (every constant, helper, transformer enumerated with `file:line`); patterns research extracts 10 conventions with quoted code; test research includes baseline runtime measurement, integration-gap grep evidence across 4 test files, and a reproducer-derived integration test sketch.

**Missing depth elements:** None for Quick tier. (Deep tier would add data-flow traces through `executor.py:349-352` showing the fall-through path, but Quick tier explicitly does not require this.)

**Verdict: PASS.** Depth appropriate for the tier; sufficient for synthesis + task-file authoring.

---

### Criterion 9: No fabrication

Spot-checked claims for internal consistency:

- `_REQUIRED_H2_SECTIONS` at gates.py:891 — 8-member set quoted in 01 §B.1; consistent with 02 §6's reference.
- `_RESOURCE_SUBSECTION_ALIASES` at cosmetic_remediator.py:81 — 02 §6 quotes the 6-tuple verbatim; consistent with 01 §A.2's row count.
- `apply_cosmetic_remediations` dispatcher table line numbers (795, 799, 803, 807, 811, 815, 819) — identical in 01 §A.4 and 02 §2.
- Reproducer at REPORT.md:36-47 — 03 §8 quotes the bash block verbatim with concrete output `True 22 0 False` and breakdown `C3 × 15, C1 × 5, C7 × 1, C11 × 1`.
- Baseline pytest result `21 passed in 0.14s` in 03 §7 — plausible runtime for a 428-line unit-test file.

No fabricated content detected. Numbers, file paths, line numbers, and code quotes are internally consistent across the three files.

**Verdict: PASS.**

---

## Compiled Gaps Summary

### Critical (block synthesis)

None.

### Important (affect quality)

1. **Dispatcher ordering contradiction (Criterion 6)** — 01 §D says C12 before C11; 02 §10 says C12 after C11. Correct answer is C12 BEFORE C11 (because C11's parent-H2 detection at cosmetic_remediator.py:466 cannot match a parenthetical-bearing parent H2). Task file must explicitly resolve and document the C12 → C11 → C13 ordering in BOTH the dispatcher branch sequence and the dispatcher docstring step list at cosmetic_remediator.py:777-786.

### Minor (must still be fixed)

2. C13 synthesized-placeholder H3 body shape not pinned (insertion position relative to existing canonical H3s; H3-only vs H3+blank-body convention).
3. Test helper sharing strategy not chosen for `_minimal_valid_roadmap` (lift to conftest fixture vs cross-file import).
4. C12 detector insertion site is a 2-line window; confirm at implementation time via grep.

---

## Recommendations

1. **Synthesis must resolve the C12/C11 ordering ambiguity explicitly.** Use 01 §D's rationale and pin the 9-step order in the docstring (cosmetic_remediator.py:777-786): C1-C4, **C12**, C11, **C13**, C5+C6, C7, C8, C9, C10.
2. **Synthesis should pin C13 placeholder shape** as: `### {canonical_name}\n\n` inserted immediately after the parent H2's blank line, preceding any existing H3s under that parent. (This matches the gate's collection logic at gates.py:961-973 which appends H3 stripped text into the parent's bucket regardless of body content.)
3. **Synthesis should pin test helper strategy** as: lift `_minimal_valid_roadmap` to `tests/roadmap/conftest.py` as a fixture (avoids cross-file test-module import, which Python tooling handles poorly).
4. **Task file must include the integration test from 03 §8** verbatim or near-verbatim — it is the load-bearing regression guard against the TUIBBS failure mode the validation REPORT documents.

---

## Final Verdict

**VERDICT: PASS** (with 1 important gap requiring synthesis-time resolution and 3 minor gaps requiring task-file pinning).

The corpus is evidence-dense, internally consistent on the load-bearing claims (gate canonical sets, dispatcher pattern, fence-skip convention, idempotency contract, integration-gap evidence), and surfaces the design driver (substring-alias inadequacy for zero-overlap drift) clearly. The one ordering contradiction (Criterion 6) is real but resolvable by inspection of the C11 transformer's parent-H2 detection mechanics. Synthesis can proceed.
