# QA Report: 2.3 allocation page check, cycle 2 (manifest v2)

Status: Complete. Date: 2026-11-13. Verifier: report-only rf-qa, Tier1b, fix_authorization false. Run: run_c974cafd0eb6. Object: topic 2.3 section of `qa/local-source-allocation.md` (lines 52-60, plus shared context lines 19-28 and 101-103).

## Verdict

VERDICT: FAIL

Four blocking findings (B1-B4). Slices 1 and 2 pass; slices 3, 4 and 5 each carry a boundary or counterpart defect.

## Inputs read

TASK lines 140-161 (22) and line 184-192 and 228 (item 2.3 producer spec, one physical line); `qa/local-source-allocation.md` (107); `qa/input-bindings.md` (32; zero 2.3 rows, so zero consuming additions, valid). `qa/input-allocation/2.3/check-1.md` does not exist (the dispatch said 0 lines; the manifest confirms the first 2.3 check launch-failed). Bounded metadata only: `wc -l`, `grep -n` of def/class lines in the proxy, `models.py` and the two test files, and about 30 lines of test text to confirm test edges.

## Check results

- (a) Cycle-1 findings: none exist for 2.3, so nothing to carry over. I instead checked the v1 defects the manifest says it fixed. Proxy cut at 460 is fixed (plain_body 436-451, `with_note` def at 452, confirmed). F05 start at 771 is fixed (start 748 = `_settings_key` def). But the fix introduced a new mid-function END cut (B3), and F14 ranges were narrowed without exclusion evidence (B1). PARTIAL.
- (b) Coverage: F10 = 451 + 222 + 233 = 906, matches `wc -l` 906. Edges 451/452 and 673/674 are def edges (`with_note` 452, `_open_upstream` 674 confirmed). FAIL on counterpart ranges, see B1-B3.
- (c) Obligations: _post, _proxy, malformed JSON, Content-Length, headers, method/query map to slice-2; _open_upstream, _forward_tier, _stream, aliases/suffix/rewriting map to slice-3. "Effort/thinking/tools fixtures" and the spec's "mock signed-history/tool assertions" map to no slice (B1). "models.py helper calls" are only partly covered (B4).
- (d) Arithmetic recomputed: slice-1 451+40+344 = 835; slice-2 222+30+344 = 596; slice-3 233+83+20+344 = 680; slice-4 211+14+30+344 = 599; slice-5 269+16+140+57+20+344 = 846. All source line counts match their ranges. All are at most 1000. The fixed-context 344 does not reproduce, see M1.
- (e) Outputs `research/source-slices/2.3/slice-1..5.md` are unique and do not collide with the 2.4 paths.
- (f) Ordering: TASK line 184 bars source dispatch until the allocation check PASSes and manifest Registration says acceptance only on PASS. Coverage-check output paths for 2.3 are named only by pattern (`2.x-coverage-N`), minor note N1.
- (g) Edge declarations: only slice-5 with 2.4-slice-4 is declared for 2.3 (line 103). F10 internal joins have none (M2). Exclusion evidence is missing for the F14 898-1002 gap and the F05 alias helpers.

## Blocking findings

**B1. The signed-history, thinking and tool fixture is in no 2.3 slice.** `test_out_of_usage_switches_and_cools_down` (F14 898-1002, next def 1003) holds a request with `thinking`, `signature: sig-from-claude`, `tool_use` and `tool_result` blocks (lines 902-929 by grep). Slice-4 stops at 864 and restarts at 1018; slice-5 takes 1215-1230, 1414-1553 and 2296-2352. The 2.3 producer spec names "effort/thinking/tool fields" and "mock signed-history/tool assertions", and the manifest obligation map (line 60) says thinking/tools fixtures go to slice-5. Slice-5's stated aspect has no such fixture, so that claim is false. The only owner of 898-1002 is 2.5-slice-2 (561-1160). No exclusion evidence was written. Fix: add F14 898-1002 (105 lines) to a 2.3 slice. Slice-4 would be 599+105 = 704, within budget.

**B2. F14 1215-1230 cuts a test in the middle.** Lines 1215-1230 sit inside `test_native_picker_uses_current_curated_rows` (def 1194, next top-level def at 1314), and line 1230 is mid-class `Models`. The manifest says "whole-test boundaries throughout" and labels the range "effort settings"; line 1215 is only a `{"effortLevel":"high"}` setting passed to a picker test. Fix: take the whole test, 1181-1313 (133 lines with its parametrize block), or drop the range with evidence.

**B3. F05 748-830 ends mid-function, and the manifest says "whole functions".** `shim_upstream_problem` starts at 822 and `resolve` at 847 (confirmed). Range ends at 830, so 831-846 of a function the proxy path depends on (upstream equals self, line 76 of the proxy) is cut. Fix: 748-846 (99 lines); slice-3 becomes 696.

**B4. The alias helpers the proxy calls have no counterpart range and no exclusion evidence.** The proxy calls `model_data.gateway_alias` (170), `is_native_model` (174), `assign_aliases` (316), `load` (196), `tier_env` (198), `tier_mode` (199), `tier_access` (204), `unavailable` (728) and `DEFAULT_WINDOW` (334). Their definitions are in F05 at 110, 233, 336-360 (`gateway_alias`, `is_native_model`), 361-458 (`assign_aliases`), 459, 474, 628 and 635. Slice-3's F05 counterpart covers only the three digest/port functions. The spec asks for the proxy's "models.py helper calls" and for alias/literal-suffix/model rewriting. Either add F05 336-458 (123 lines; slice-3 becomes about 819 with B3 fixed) or record that these are UNVERIFIED pending 2.2 acceptance, with the exclusion stated in the manifest.

## Medium follow-up candidates and minor notes

- M1. Fixed context 344 is said to come from trimming role/template to a 100-line excerpt. The listed parts give 22 + 70 + 180 + 100 + 32 = 404, not 344 (344 equals 424 minus the role's 80 lines, so the role is charged zero). With 404 every 2.3 slice still fits (largest, slice-5, is 906; with B1-B4 fixes slice-3 about 879), so no budget breach, but the number must be corrected before dispatch. Brief (70) and prompt (180) are estimates, not measurements.
- M2. No declared cross-slice edges for F10 slices 1-3: `_proxy` (646, slice-2) calls `_forward_tier`/`_open_upstream` (slice-3), and `switch_reason`/`cool_down` (slice-1) are used by `_forward_tier`. Add one-line cross-cite declarations.
- N1. 2.3 coverage-check output paths (`qa/input-allocation/2.3/coverage-1..5.md`) are not named in the manifest.
- N2. Scope/research-notes context is charged as "rows" with no inclusive ranges (same pattern as the 2.4 cycle-1 note N2).
- N3. Slice-5's range 882-1150 includes installer tests 1068-1150 that are not proxy fixtures, and 2296-2352 includes two unrelated tests at 2321-2352. Wasteful, not wrong.
- N4. Slice-1 and slice-2 aspects do not name `curation`/`transform_models`/`SWITCH_RULES` (190-392) or `_handle_models` (621); they are inside the ranges, so coverage holds.

## Coverage rows and confidence

F10 1-451 slice-1 OK; 452-673 slice-2 OK; 674-906 slice-3 OK (906 of 906 lines). F05 counterpart 748-830 partial (B3, B4). F14 654-864 OK; 1018-1031 OK; 1414-1553 OK (edges 1414, 1553/1554 confirmed); 2296-2320 OK; 898-1002 absent (B1); 1215-1230 mid-test (B2). F15 882-1150 OK at edges (test at 882, next def 1152). Confidence in the FAIL: high for B1-B3 (each checked against def lines and test text); medium-high for B4 (spec text permits an UNVERIFIED attribution).

## Self-Audit

Attempted to disprove each blocking finding. B1: searched all of F14 for thinking/signature/tool_use; the only hits are 902-929 (inside test 898) and 1482 (a comment in slice-5's stream test), so no other slice covers it. B2: read 1205-1232 and the def list; 1194 is the enclosing def, so the cut is mid-test. B3: grep of defs in `models.py` shows 822 and 847, so 830 is inside the function. B4: grep of the proxy shows all nine `model_data.` calls; slice-3's F05 range contains none of their definitions. Not attempted: reading full source to judge how much slice-4 and slice-5 content duplicates 2.4 (outside a metadata check).
