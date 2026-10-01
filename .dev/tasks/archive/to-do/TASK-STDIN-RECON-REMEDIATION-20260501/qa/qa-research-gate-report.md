# QA Report — Research Gate

**Topic:** TASK-STDIN-RECON-REMEDIATION-20260501 — Builder readiness verification
**Date:** 2026-04-30
**Phase:** research-gate
**Fix cycle:** N/A
**Adversarial stance:** Assume errors. Verify every claim. Find what was missed.

---

## Tool Engagement Log

- Read calls: 11 (5 research files + refactor-plan + RECONCILED_DESIGN.md ×2 + pipeline/process.py ×2 + prd/process.py + test_process_stdin.py + reference TASK-RF + template + research-notes.md)
- Bash calls: 5 (ls research dir, git rev-parse, wc -l files, find BUILD, ls task dir, grep refactor-plan)
- Glob/Grep equivalent: covered via Bash grep
- Total: 16 tool calls across 10 checklist items — exceeds minimum

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory — 5 files exist with Status:Complete + Summary | PASS | `ls -la` shows all 5 files (sizes 17-46 KB). Each file's `Status:` field: R1 line 467 "Status: Complete", R2 line 5 "Status: Complete", R3 line 626 "Status: Complete", R4 line 419 "Status: Complete", R5 line 575 "Status: Complete." Each has Summary section. R1 actually has both "**Status:** In Progress" at L4 AND "**Status:** Complete" at L467 — the header was not updated to "Complete" but final summary marks it complete. MINOR INCONSISTENCY in R1 only. |
| 2 | Evidence density — verify R1 line citations | PASS | Spot-checked: P-009 anchor at pipeline/process.py L27-29 = exact match (`PROMPT_MAX_BYTES: int = int(os.environ.get(...)`); P-011 init body L88-90 = exact match (`self._stdout_fh = None\n self._stderr_fh = None`); P-012 spawn debug at L181-186 = exact match; T-012 silent break at L216-218 = exact match (`if n <= 0:` `break`); P-006 prd/process.py `_close_handles()` = at L279 (R1's drift call correct, refactor-plan said L277 which is `if self._on_exit`); R2's T-011 at L262-285 verified verbatim — matches R2's claim exactly. R1 evidence density = DENSE (>90% evidenced with line numbers + verbatim source). |
| 3 | Scope coverage — 18 items, 4 doc sources, MDTM template | PASS | R3 extracts 18 records (P-006..P-016 + T-012..T-016 + P-014..P-016 + T-015/T-016 = 18). R4 cross-extracts RECONCILED_DESIGN §3.2/§4/§11, merged-output §5.3, F-strict-review. R5 reads MDTM Template 02 PART 1 (lines 1-866) and finds reference example. All 4 doc sources covered. |
| 4 | Documentation cross-validation — tags applied | PARTIAL | R1 does NOT use literal `[CODE-VERIFIED]` tags but provides explicit verdicts (VERIFIED / DRIFT / SEVERE DRIFT) per anchor — equivalent semantics, different tag form. R4 does NOT tag claims with `[CODE-VERIFIED]` either, but every claim cites file path + line number. The explicit-tag convention is missing across all 5 files. MINOR — claims are evidenced but not tagged in standardized form. |
| 5 | Contradiction resolution — D-FOLLOW count + T-015/T-016 phase | PARTIAL | R4's reconciliation of 12-vs-13 D-FOLLOW is sound (10 match exactly, +1 W-M10, +2 merged-only T-015/T-016, -2 refactor-only D-FOLLOW-011/-012 absorbed by P-014). The §3.2 SUPERSEDED count "16 IDs" is correctly derived (verified independently against RECONCILED_DESIGN.md L121-126: 2+8+5+1=16 ✓). R3's Phase 5 default for T-015/T-016 is FLAGGED ("ambiguous; builder decision required") but NOT RESOLVED. This is an open gap. |
| 6 | Gap severity assessment | See Issues Found section below | Several flagged gaps — see issues. |
| 7 | Depth appropriateness — Standard tier (5 researchers) | PASS | 5 researchers covered: source verification, test infra, content lift, doc extraction, template/examples. R3 over-delivers (extensive metadata reconciliation arithmetic at end). R5 over-delivers (5 fillable B2 templates). Both are useful, not waste. R1 under-delivers on tag-form but covers content. |
| 8 | Integration point coverage | PASS | P-014 sources §3.2 verified; P-015 sources §11 verified (5 patches + 11 tests + 9 commits captured); Phase 5 sources merged-output §5.3 verified (13 rows captured). Cross-references resolved. |
| 9 | Pattern documentation | PASS | R2 captures `_stdin_echo_argv()` (lines 31-37), `patch.object(...)` with-block style, `caplog.at_level(...)` canonical incantation, `monkeypatch.setattr("superclaude.cli.pipeline.process.PROMPT_MAX_BYTES", val)` full-dotted-path style, `tmp_path` universal fixture, threading.Timer + time.monotonic patterns, `--strict-markers` constraint. 11 universal style rules enumerated. |
| 10 | Incremental writing compliance | PASS | All 5 files show iterative structure: R1 uses Per-Anchor sections, R3 uses one yaml block per item, R4 uses numbered sections with cross-references. R3's Status Summary section at L626-656 contains visible recount/correction passes ("Wait — re-counting:" R4 L41, R3 type-distribution corrections at L649-656) — strong evidence of incremental writing not one-shot. |

---

## Specific Verifications Requested by Prompt

| Verification | Result | Evidence |
|---|---|---|
| R1 line citations spot-check (3+) | PASS — 6/6 verified | P-006 L279 ✓, P-009 L27-29 ✓, P-011 L88-90 ✓, P-012 L181-186 ✓, T-012 L216-218 ✓, P-013 L262-285 ✓ — all exact |
| R2 T-011 line range L262-285 | PASS | Read tests/pipeline/test_process_stdin.py:260-289; def starts at L262, conditional at L282-285, function ends at L285. EXACT match. |
| R4 §3.2 SUPERSEDED count "16" | PASS | RECONCILED_DESIGN.md L121-126: D-002,D-004(2) + D-017,D-018,D-019,D-023,D-024,D-028,D-042,D-109(8) + D-050,D-053,D-054,D-055,D-057(5) + D-075(1) = 16 IDs. R4's recount matches; banner "12" undercount is correctly identified. |
| R5 reference TASK-RF-20260402-baseline-repo exists | PASS | `ls` confirms file at expected path, 55KB, well-formed, status:Done; frontmatter matches R5's verbatim quote. |
| P-013 200-line drift documented | PASS | R1 §"Drift Summary" + builder-paste-ready yaml block both clearly state "Refactor-plan cites L465-488, actual is L262-285 (drift ~200 lines)" — builder cannot miss this. |
| P-006 L277 vs L279 drift documented | PASS | R1 §P-006 "DRIFT — refactor-plan cites L277, actual `_close_handles()` final call site is L279" — explicit. |
| R3 T-015/T-016 Phase 5 default | FAIL | See CRITICAL issue below. |
| R5 Phase 6 = 6 items vs BUILD_REQUEST 4 items | OPEN | R5 calls this out explicitly at L550 — "If user's 18-item count INCLUDES Phase 6's items, builder must re-budget — recommend confirming with build request." Properly flagged but UNRESOLVED. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | R3 §"Phase 5 — LOW priority items NOT in Phase 1-4 scope" (L496-559) | T-015 and T-016 are NEW-TEST items requiring actual code execution (write `def test_*` functions, run pytest) but R3 places them in "Phase 5 (Deferred / out-of-Phase-1-4)" alongside the Phase 5 GH-issue-filing items. Per research-notes.md L171-180 and the BUILD_REQUEST, Phase 5 = "GH issue filing (13 D-FOLLOW items as ONE collapsed item)". Mixing executable test additions into a phase whose semantic meaning is "file as GH issues" will cause the builder to either (a) collapse them into the gh-issue-batch item (silently dropping the real tests) or (b) place them in a phase that contradicts its purpose statement. R3 itself flags this: "Phase mapping ambiguous — BUILD_REQUEST lists T-015 in MEDIUM list but refactor-plan classifies LOW. Builder decision required." | Reclassify T-015 and T-016 to Phase 3 (NICE) per refactor-plan.md severity LOW (which sits below MEDIUM=Phase 2, above tracking=Phase 4). Alternatively explicitly create a new "Phase 3.5" or fold to Phase 2 per refactor-plan §LOW grouping. The current Phase 5 placement is semantically wrong. R3 must update phase_assignment fields for both records, OR builder must be explicitly directed in research output to choose a non-Phase-5 placement. |
| 2 | IMPORTANT | All 5 research files | Documentation tagging convention (`[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]`) is NOT applied. R1 uses verdicts (VERIFIED / DRIFT / SEVERE DRIFT) but not the standard tag form requested by the QA checklist (item 4). R4's doc-cross-claims (e.g., "merged-output banner '12' undercounts") are evidenced but un-tagged. | Either (a) accept R1's equivalent verdict-form as satisfying this check (recommended — semantic equivalence is achieved), or (b) require all researchers to add explicit `[CODE-VERIFIED]` tags in a fix cycle. Recommend (a); document the alternate-form convention in QA report. |
| 3 | IMPORTANT | R5 §3.8 "Verification-Gate Item Pattern" L508-548 | R5 specifies Phase 6 should have 6 items (4 gates + 1 aggregator + 1 frontmatter close-out) but the BUILD_REQUEST per research-notes.md L171 says "Phase 6 itself is the final integration verification" and the user's spec is implied to be 4 gates. R5 explicitly flags this as a gap requiring builder/user clarification. The 18-item count in the user's BUILD_REQUEST refers to the 18 P/T-NNN items; Phase 6's verification items are likely additional. Without explicit confirmation, builder may build the wrong shape. | Builder MUST treat Phase 6 verification items as ADDITIONAL to the 18-item count (not subtractive). R5's recommendation of 6-item Phase 6 (4 I17 gates + aggregator + frontmatter close-out) is the right shape per Template 02 I17 + reference example. Add an explicit note in research-notes.md or task overview clarifying: "18 items refers to Phases 1-5 P/T-NNN items only; Phase 6 adds 6 verification/close-out items for total 24." |
| 4 | IMPORTANT | R3 §"Status Summary" type-distribution arithmetic L644-656 | R3 visibly fumbles the type counts in iterative passes (multiple "wait, recount" passages) before reaching the final "Definitive type counts: CODE-FIX=6, NEW-TEST=6, SPEC-AMENDMENT=1, DEFERRED-WITH-OWNER=3, plus T-015/T-016 (NEW-TEST) bringing NEW-TEST=8. Total = 6+8+1+3 = 18." This is correct but the visible thrashing in the file makes the final number harder to trust. The breakdown is also internally inconsistent: at L630-634 R3 says "Phase 2: 5 records — P-011, P-013, T-012, T-013, T-014" and "Phase 3: 3 records — P-008, P-010, P-012", but P-013 is targeted at a test file (test_process_stdin.py) so its CODE-FIX classification is logically defensible but the type label "CODE-FIX" applied to a test-file edit is semantically unusual. | Builder should recompute the type distribution independently when populating each item's metadata; do not rely on R3's fumbled summary. The per-record yaml blocks (L26-559) are individually authoritative — use those, not the aggregate. |
| 5 | MINOR | R1 frontmatter L4 | R1 header says `**Status:** In Progress` but the file is complete (final summary at L463 reads "5 of 7... VERIFIED... 1 minor drift, 1 severe drift"; closing line L467 reads "**Status:** Complete"). Header was not updated when finalizing. | Update R1 L4 from "In Progress" to "Complete" for consistency with closing status. |
| 6 | MINOR | R3 §Record P-007 acceptance L80-86 | R3's P-007 record cites mocking strategy as "monkeypatch `os.write` to raise BrokenPipeError" but R2's pattern catalog says the canonical pattern in this test file is `patch.object(ClaudeProcess, "build_command", return_value=early_exit)` for child-exit simulation. R3 inherits the strategy from refactor-plan verbatim, but builder needs to reconcile: P-006/P-007 surface BrokenPipe on the PRD subclass — a `monkeypatch.setattr(os, "write", ...)` is the right tool here (P-013 uses the same approach), so R3 is correct. The MINOR concern is the test file (P-007 is in `test_prd_process_stdin.py` NEW file) needs to import `os` and `monkeypatch` fixture — R3 doesn't enumerate the imports, only the test logic. | Builder should add to P-007 item body: required imports (`import os`, `from unittest.mock import patch` if needed for `patch.object`), required pytest fixtures (`tmp_path`, `caplog`, `monkeypatch`). R2's universal style rule #11 (L191) lists the canonical imports; builder copies that. |
| 7 | MINOR | R3 §Record P-008 (Owner: spec-keeper) and P-010 (Owner: spec-keeper) | R3 records spec-keeper as owner for two records but the BUILD_REQUEST does not establish a "spec-keeper persona" in this repo. Builder must decide whether to embed persona-tagging in item bodies or treat ownership as informational only. | Builder treats owner as informational metadata (added to the item body as commentary like "Owner per refactor-plan: spec-keeper") and does NOT spawn a persona-specific subagent unless the user's pipeline supports it. R5 §1.9 L306 confirms social ownership is item-text only, not L-pattern handoff. Acceptable as-is. |
| 8 | MINOR | R4 §1b L41-49 visible recount | R4 contains the same kind of visible "wait — re-counting" arithmetic as R3 (good evidence of incremental writing but messy). The final answer (16 SUPERSEDED IDs) is correct (verified independently). | No fix required; minor readability concern only. |

---

## Builder-Trip Risk Assessment

The QA prompt explicitly asks: what could trip the builder?

1. **P-013 200-line drift** — Documented well (R1 + R2 both spell it out; R1's drift_warning yaml field will surface in the builder's paste). LOW RISK.
2. **P-006 L277→L279 drift** — Documented well (R1 explicit note + builder-paste-ready yaml with `verified_at_line: 279`). LOW RISK.
3. **T-015/T-016 phase placement** — HIGH RISK. R3 defaults to Phase 5 which contradicts Phase 5's "file as GH issues" semantic. Builder may either silently lose these tests or place them wrong. Issue #1 above. CRITICAL.
4. **§3.2 SUPERSEDED count discrepancy (12 banner vs 16 actual)** — Documented well by R4. R4 explicitly directs builder to use the 16-ID list, not the banner. LOW RISK.
5. **Reference example (TASK-RF-20260402-baseline-repo) existence** — Verified exists, well-formed (Done status). LOW RISK.
6. **Phase 6 = 6 items vs 4 items** — MEDIUM RISK. R5 flags it explicitly but does not resolve. Builder should use 6-item Phase 6 per R5's recommendation (4 gates + aggregator + close-out). Issue #3 above.

---

## Confidence Gate Computation

- TOTAL checklist items: 10 (Research Gate)
- VERIFIED [x]: 8 (file inventory, evidence density, scope coverage, depth, integration, pattern doc, incremental writing, contradiction-resolution-on-D-FOLLOW)
- PARTIAL/UNCHECKED: 2 (item 4 doc-tagging convention is partial, item 5 contradiction resolution is partial because T-015/T-016 phase issue is unresolved)
- UNVERIFIABLE: 0

confidence = 8 / (10 - 0) * 100 = **80%**

Below 95% threshold due to:
- Item 4: Standardized `[CODE-VERIFIED]` tag form is missing (treated as IMPORTANT not CRITICAL — semantic equivalence achieved)
- Item 5: T-015/T-016 phase resolution is open

Both are documented as Issues. Re-verification rounds would not raise confidence further without research file modifications.

---

## Summary

- Checks passed: 8/10 fully + 2/10 partial
- Checks failed: 0 fully (2 partial = downgrade to FAIL per zero-tolerance rule)
- Critical issues: 1 (T-015/T-016 Phase 5 misclassification)
- Important issues: 3 (tag convention, Phase 6 size ambiguity, R3 type arithmetic thrashing)
- Minor issues: 4 (R1 header status, P-007 import enumeration, owner persona handling, R4 recount visibility)
- Issues fixed in-place: 0 (fix_authorization=false)

---

## Recommendations

Before greenlighting Phase 4 (synthesis/build), the following actions should be taken:

1. **CRITICAL: Resolve T-015/T-016 phase placement.** Either (a) escalate to user for explicit ruling, OR (b) adopt R3's flagged-default of "Phase 5 with deviation note" and document the deviation explicitly in the task file's `### Deviations from Process` section per R5 §3.7. Recommend (a) — user clarification preferred, but (b) is acceptable if no user available.

2. **IMPORTANT: Confirm Phase 6 size.** R5 recommends 6 items (4 I17 gates + aggregator + close-out). Builder should adopt this and treat the 18-item count as P/T-NNN items only (Phases 1-5).

3. **IMPORTANT: Use R3's per-record yaml blocks as authoritative**, not its fumbled type-distribution summary. The per-record metadata (severity, owner, risk, LOC, before/after) is correct in each yaml block.

4. **MINOR: Update R1 status header from "In Progress" to "Complete"** for consistency. Non-blocking.

5. Builder must propagate R1's drift warnings (P-013 200-line drift, P-006 L277→L279 drift) verbatim into the corresponding task items so the executor cannot miss them.

---

# VERDICT: FAIL

**Reason:** 1 CRITICAL issue (T-015/T-016 Phase 5 misclassification — could cause builder to silently drop two NEW tests or assign them a phase whose semantic purpose contradicts test-execution) plus 3 IMPORTANT issues that reduce builder reliability. Per zero-tolerance rule (all gaps must be resolved before synthesis), the research is not yet ready for Phase 4 builder-spawn.

**Adversarial conclusion:** The research is high-quality on the verifiable-line-citation axis (every spot-check passed) and content-extraction axis (16 SUPERSEDED IDs correct, 13 D-FOLLOW reconciled, 18 records lifted with full metadata). The failure mode is **phase semantics** — R3 punted on T-015/T-016 phase assignment and the punted default conflicts with the user's BUILD_REQUEST Phase 5 semantics. This is exactly the kind of soft gap that a "looks fine" QA pass would miss.

If the orchestrator chooses to proceed despite FAIL, T-015/T-016 must be explicitly relocated by the builder (not left to default) and the deviation surfaced in the task file's Task Log / Notes.

## QA Complete
