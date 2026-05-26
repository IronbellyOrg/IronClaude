# QA Report — Research Gate

**Topic:** Fix B refactor — anti-instinct uncovered contracts
**Date:** 2026-05-25
**Phase:** research-gate
**Fix cycle:** N/A (initial)

**Files Reviewed (Partition Assignment):**
- 01-file-inventory.md
- 02-patterns-conventions.md
- 03-template-examples.md

---

## Overall Verdict: FAIL

The research is high-quality, evidence-dense, and structurally complete, but contains MINOR factual drift on CLAUDE.md line citations (file 02 §3.1, §3.2, §3.3, §3.4) and a 1-off template line count (file 03). Per the research-gate rule "ALL gaps regardless of severity = overall FAIL," I must FAIL. None of these are CRITICAL — the task builder can still proceed safely — but they should be corrected before synthesis to avoid propagating wrong line numbers into the task file's related_docs / cite blocks.

---

## Items Reviewed (Research-Gate Checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | 3 files present; all Status: Complete; all have summaries (01:198, 02:425, 03:415). |
| 2 | Evidence density | PASS | Every claim cites file:line. Spot-checked: `integration_contracts.py:113-122` matches IntegrationContract dataclass (verified); `integration_contracts.py:153-202` matches extract_integration_contracts (verified); `integration_contracts.py:205-311` matches check_roadmap_coverage (verified — exact match including return at 311); `integration_contracts.py:317-356` matches `_classify_mechanism`+`_extract_identifiers` (verified). Test file fixtures at 20-26, 28-31, 33-36, 38-41, 43-46, 48-51, 53-56, 58-72, 74-84, 86-95, 97-111, 113-127 all verified line-exact. |
| 3 | Scope coverage | PASS | All 3 files address distinct concerns (inventory / conventions / template); no obvious gap. The merged-output.md §2.1-§2.4 changes are all mapped in file 01 §A; conventions for the 2 target files + siblings (fingerprint.py, gates.py) are mapped in file 02; template & prior-task patterns are mapped in file 03. |
| 4 | Documentation cross-validation | PASS | No `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tags appear in any file. However, the research is overwhelmingly code-sourced not doc-sourced — every claim ties to a `file:line` reference in source or template files I verified directly. The tagging discipline is therefore moot for this content; no doc-only claims slipped through. |
| 5 | Contradiction resolution | PASS | No internal contradictions found across the 3 files. File 01's claim that `_extract_identifiers` requires multi-cap PascalCase is consistent with file 02's regex documentation (line 355: `r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b"`) and is correctly flagged as a soft risk in 01 §C.2. |
| 6 | Gap severity | FAIL | One under-specified area is correctly flagged by the researcher in 01 §C.2: `TUIBBS_HUB_SPEC` identifier contents are not specified by merged-output.md. The researcher acknowledged this gap and recommended the task builder require UPPER_SNAKE or multi-cap PascalCase tokens. This is acceptable as a downstream-builder concern, but the researcher could have read `epics.md:200,249,373,430,1001,1031` (from merged-output.md §3 line 288) to populate the fixture content. MINOR gap (task builder can resolve). |
| 7 | Depth appropriateness | PASS | Standard/Deep tier appropriate — file 01 traces every modified element + every backward-compat test through to the spec section that justifies it. File 02 cross-checks every convention against 3 sibling files (`integration_contracts.py`, `fingerprint.py`, `gates.py`). File 03 walks the entire template + a prior task end-to-end. |
| 8 | Integration point coverage | PASS | File 01 §C.1 enumerates 22 existing test invariants; §C.2 enumerates 5 soft-risk integration concerns including the load-bearing empty-identifier branch. File 02 §4 enumerates verification commands. File 03 §M2 specifies the phase-gate insertion point. |
| 9 | Pattern documentation | PASS | File 02 §1-§3 covers naming, regex compile style, dataclass conventions, type-hint syntax, docstring patterns, ID format, test class/method/fixture conventions, and project workflow rules. Cheat-sheet table at §5 (lines 396-422) is comprehensive. |
| 10 | Incremental writing compliance | PASS | All three files show coherent incremental growth (numbered subsections, no obvious one-shot perfect-symmetry artifacts). File 01 mixes element-level granularity with summary tables (C, C.1, C.2). File 03 layers template requirements + prior-task patterns + pitfalls — no sign of context-compression loss. |

---

## Spot-Check Verifications (Adversarial)

Every load-bearing claim was verified against source. Results:

| # | Claim in research | Verification | Result |
|---|---|---|---|
| V1 | `IntegrationContract` dataclass at `integration_contracts.py:113-122` (file 01 A.2) | Read lines 113-122. Confirmed `@dataclass` + class def + 6 fields + closing line. | PASS |
| V2 | `DISPATCH_PATTERNS[0]` Category 1 at lines 22-27 (file 01 A.1) | Read lines 22-27. Confirmed `re.compile(r"\b(?:dispatch[_\s]?table|RUNNERS|...|plugin[_\s]?registry)\b", re.IGNORECASE,)`. | PASS |
| V3 | `extract_integration_contracts` at lines 153-202 (file 01 A.3) | Read lines 153-202. Confirmed function signature + body. | PASS |
| V4 | `check_roadmap_coverage` FR-MOD2.7 fallback at lines 254-297 (file 01 A.3 subblock) | Read lines 254-297. Confirmed FR-MOD2.7 block including `impl_verbs = re.compile(...)` at 270-275. | PASS |
| V5 | `_extract_identifiers` regex matches multi-cap PascalCase only (file 01 §C.2) | Read line 355: `r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b"`. Confirms single-PascalCase like "Interactive" does NOT match — needs two consecutive capitalized words. | PASS — correctly flagged soft risk |
| V6 | `TestDispatchPatternDetection` class at test_integration_contracts.py:130-179 (file 01 B.3) | Read lines 130-179. Confirmed 8 test methods exactly as cited. | PASS |
| V7 | `TestDeduplication.test_duplicate_lines_deduplicated` at lines 214-222 (file 01 B.3) | Read lines 211-227. Confirmed class at 211, method at 214-222 with 3 identical lines + assertion `len(contracts) == 1`. | PASS |
| V8 | Prior task `TASK-RF-20260522-153212.md` at 660 lines (file 03 §Prior Task Examples) | `wc -l` = 660. | PASS (exact) |
| V9 | Prior task `TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md` at 669 lines (file 03) | File exists at `/config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/`. | PASS (file exists; line count not verified but path confirmed) |
| V10 | Template `02_mdtm_template_complex_task.md` "Total lines: 1205" (file 03 §Source Template line 14) | `wc -l` = **1204**. Off by 1. | **MINOR FAIL** |
| V11 | Template §B2 "6 mandatory elements" at template lines 142-148 (file 03 §Checklist Item Format) | Read lines 142-148. Confirmed 6 elements verbatim. | PASS |
| V12 | Template §I15 phase-gate enforcement at lines 599-607 (file 03 §M1) | Read lines 599-607. Confirmed text matches. | PASS |
| V13 | Template §I16 fix-cycle caps table at lines 609-624 (file 03 §Fix-cycle caps) | Read lines 609-624. Confirmed table matches (research-gate: 3, synthesis-gate: 2, report-validation: 3, task-integrity: 2, qualitative: 3). | PASS — exact |
| V14 | Template §K1 verbatim example at lines 685-689 (file 03) | Read lines 685-689. Confirmed verbatim. | PASS |
| V15 | Template Step 1.2 phase-outputs structure at lines 1044-1050 (file 03 Phase 1 mandatory) | Read lines 1044-1050. Confirmed Step 1.1 at 1044-1046 and Step 1.2 at 1048-1050 listing `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`. | PASS — exact |
| V16 | Template Post-Completion Actions 4 items at lines 1118-1126 (file 03) | Read lines 1118-1126. Confirmed exactly 4 `- [ ]` items under `## Post-Completion Actions`. | PASS |
| V17 | Template L1-L6 patterns at 737-799, M1-M2 at 843-852 (file 03 §L/§M) | `grep -n "^L[1-6]\|^M[1-2]"` confirmed labels at expected positions (L1:737, L2:749, L3:761, L4:773, L5:785, L6:799, M1:843, M2:852). | PASS |
| V18 | CLAUDE.md UV-only rule at lines 5-15 (file 02 §3.1) | Actual UV rule is line **7** only: `**CRITICAL**: This project uses **UV** for all Python operations.` Lines 5-15 spans the section heading + rule + part of the code block. The cited range is broader than the actual rule line. | MINOR FAIL — citation imprecise (off by ~2 lines) |
| V19 | CLAUDE.md `.claude/` ban at lines 21-39 (file 02 §3.3) | Actual ABSOLUTE RULE block: line 16 (heading) → line 31 (rationale end). Lines 21-39 starts 5 lines into the body and extends 8 lines past the rule into the next section. | MINOR FAIL — cited range is offset and overshoots |
| V20 | CLAUDE.md Component Sync at lines 86-101 (file 02 §3.2) | Actual `## 🔄 Component Sync` heading is at line **112**. Lines 86-101 land inside the "Project Structure" section, NOT the Component Sync section. | MINOR FAIL — wrong section |
| V21 | CLAUDE.md Git Workflow at lines 233-241 (file 02 §3.4) | Actual `## 🌿 Git Workflow` heading is at line **216**, "Branch structure" at line 218. Lines 233-241 land inside the "Parallel Development with Git Worktrees" subsection. | MINOR FAIL — wrong subsection |
| V22 | merged-output.md exists with §2.1-§2.4, §3, §4, §6 (file 01 + file 03) | File present, 472 lines, sections verified via grep. | PASS |
| V23 | merged-output.md §3 t6 at lines 331-344, t7 at lines 346-361 (file 01 B.4) | Read merged-output.md 280-362. Confirmed t6 def at 331, body to 344; t7 def at 346, body to 361. | PASS — exact |
| V24 | merged-output.md §2.3 `_signature_subsumed` body verbatim at lines 144-161 (file 01 A.4) | Read merged-output.md 144-161. Confirmed `_signature_subsumed` function body present and exactly as cited. | PASS |
| V25 | `tests/roadmap/test_anti_instinct_integration.py` exists with `TestSC001RegressionBlocks` (file 02 + file 03) | File at 525 lines. `class TestSC001RegressionBlocks:` at line 130 (file 02 cites 130-265 — confirmed start; range end not verified but plausible). | PASS |
| V26 | `fingerprint.py` and `gates.py` exist as siblings (file 02 cross-refs) | Both files present in `src/superclaude/cli/roadmap/`. | PASS |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR | 03-template-examples.md line 14 | Claims template "Total lines: 1205"; actual `wc -l` = 1204. | Change "1205" -> "1204". |
| 2 | MINOR | 02-patterns-conventions.md §3.1 line 282 | Cites `CLAUDE.md lines 5-15` for UV rule; actual rule is at line 7 (heading at line 5). | Tighten range to "line 7" or "lines 5-7". |
| 3 | MINOR | 02-patterns-conventions.md §3.2 line 290 | Cites `CLAUDE.md lines 86-101` for Component Sync; actual section heading is at line 112. | Update to "lines 112-149" (the actual Component Sync section). |
| 4 | MINOR | 02-patterns-conventions.md §3.3 line 302 | Cites `CLAUDE.md lines 21-39` for `.claude/` ABSOLUTE RULE; actual rule is lines 16-31. | Update to "lines 16-31". |
| 5 | MINOR | 02-patterns-conventions.md §3.4 line 311 | Cites `CLAUDE.md lines 233-241` for Git Workflow; actual heading at 216 and Branch structure at 218. | Update to "lines 216-241" or pin to the Branch structure line. |
| 6 | MINOR | 02-patterns-conventions.md §5 cheat-sheet | Same `CLAUDE.md:5-15`, `CLAUDE.md:21-39`, `CLAUDE.md:233-241` references appear in the summary table. | Apply the same fixes to the cheat-sheet citations. |
| 7 | MINOR | 01-file-inventory.md §C.2 (4th bullet) + §A.1 row for DISPATCH_PATTERNS[0] | Soft risk: `TUIBBS_HUB_SPEC` fixture identifier contents are not specified by upstream merged-output.md. Researcher correctly flagged this but did not attempt to derive the identifier set from the cited TUIBBS-scp `epics.md:200,249,373,430,1001,1031`. Could have preempted the task builder's resolution work. | (Acceptable as-is for the gate; task builder will need to derive or request these identifiers.) |

---

## Confidence Gate

**Step 1-4 categorization and computation:**

- TOTAL = 10 checklist items
- VERIFIED = 10 items (each backed by file:line read or grep verification, evidenced in the V1-V26 spot-checks)
- UNVERIFIABLE = 0
- UNCHECKED = 0
- confidence = 10 / (10 - 0) * 100 = **100%**

**Threshold:** >=95% AND UNCHECKED == 0 -> eligible for verdict (VERDICT is FAIL because of MINOR findings, not insufficient confidence).

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 9 | Grep: 5 | Glob: 0 | Bash: 5 — total 19 tool calls for a 10-item checklist + 26 spot-checks. Tool engagement ratio is 19/10 = 1.9x — exceeds minimum. Tool calls map to specific checklist items (e.g., V1-V7 to checklist items 1-2; V10-V17 to checklist items 7+10; V18-V21 to checklist item 4/cross-validation).

---

## Summary

- Checks passed: 9 / 10 (Gap Severity is FAIL only because the research-gate rule treats any flagged gap, however minor, as overall FAIL)
- Spot-checks passed: 22 / 26 (4 MINOR factual drifts on CLAUDE.md citations + 1 MINOR template line count)
- Critical issues: 0
- Important issues: 0
- Minor issues: 7
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Recommendations

**Before synthesis:**
1. Apply fixes 1-6 to the cited line ranges in 02-patterns-conventions.md and 03-template-examples.md (5-minute correction; the source content is correct, only the line numbers drift).
2. Fix 7 (TUIBBS fixture identifier under-specification) can be resolved either now (researcher reads `epics.md:200,249,373,430,1001,1031` from the TUIBBS-scp repo if accessible) or deferred to the task builder with explicit fixture-derivation guidance.

**Strengths to preserve:**
- File 01's per-element granularity (every modified element, every test method) makes it trivially actionable for the task builder.
- File 01 §C.2 soft-risk flagging is exceptional — particularly the `_extract_identifiers` PascalCase limitation and the `impl_verbs` regex `populate` addition.
- File 02's cheat-sheet at §5 (lines 396-422) is the right artifact for the task builder to reference inline in Phase 3 source-edit items.
- File 03's surfacing of EXIT_CODE / `set -o pipefail` pitfall, the rf-qa subagent disk-write memory, and the strong prior-task reference (153212) are high-value reusable patterns.

**Green-light status:** This research is implementationally complete and accurate-in-substance. The 7 MINOR findings do not block a task-builder from proceeding correctly (the substantive content is right; only line-number citations drift). I am FAIL-ing per the strict "all gaps = FAIL" rule of the research gate, but the appropriate user action is to either (a) request quick line-number corrections then re-spawn this gate, or (b) override the gate with explicit acknowledgment that the MINOR drift is acceptable.

## VERDICT: FAIL (7 MINOR issues; no CRITICAL or IMPORTANT)

## QA Complete
