# QA Report: 2.4 allocation page check (check-1)

Verifier: rf-qa, report-only, Tier1b. Run run_c974cafd0eb6. Date 2026-11-13. Object: topic 2.4 section of `qa/local-source-allocation.md` (lines 78-87). Revision: worktree HEAD 933cf3a4f.

VERDICT: FAIL

Blocking findings: 4. Minor notes: 3.

## Inputs read
- TASK lines 140-161 (procedure). `qa/input-bindings.md` (32 lines; no 2.4 rows, zero consuming additions for 2.4, valid). `qa/local-source-allocation.md` lines 1-40 and 70-117.
- Item 2.4 producer spec: it is at TASK line 230, not 219 (line 219 is not that item; line 228 is 2.3). Minor drift in the dispatch brief. Read from "PRODUCER-ONLY" to the Ensure-sentence start.
- Metadata only: `wc -l` and symbol greps (below). No full source reads.

## Metadata verification (confirmed)
- wc -l: F10 906, F01 1975, F05 1111, F14 3399, F15 4823; scope-02 142, scope-03 92, research-notes 112. All match the manifest.
- Slice arithmetic recomputed: s1 629, s2 665, s3 457, s4 521. All correct and all <=1000, even if the brief is larger than 55.
- Range lengths 962-1155 (194), 771-820 (50), 1025-1160 (136), 1414-1560 (147), 1441-1470 (30), 3306-3460 (155) are right.
- F10 union 1-460 + 461-906 = 906, no gap, no overlap. Slices 1-2 cover the whole file.

## Findings

### Coverage table
| Check | Result |
|---|---|
| (a) F10 complete line coverage | PASS (1-906, but see B1 for the split point) |
| (a) counterpart ranges internally | no gaps/overlaps among 2.4 slices; ends cut test bodies (B2) |
| (b) counterparts labeled | PASS: F14/F15 explicitly labeled counterpart, full coverage left to 2.5; F01/F05 are not given a full-coverage owner in this page (minor note N1) |
| (c) keyword to aspect mapping | FAIL (B3) |
| (d) lifetime <=1000 | PASS (max 665) |
| (e) unique output per slice | FAIL (B4) |
| (f) producer-before-consumer | PASS (manifest lines 111-113 put checks before source dispatch) |

### Blocking
B1. Slice 1/2 boundary splits `with_note` (F10:452-~478, the error-body handling the spec names) inside its body: slice 1 ends at 460 (`except (ValueError, TypeError):`), slice 2 starts at 461 (`return raw + ...`). No shared boundary lines and no declared cross-slice edge. Slice 2 owns `Handler`/`_forward_tier`/`_stream` (480+) while slice 1 owns the callees `switch_reason` (393), `retry_after_seconds` (404), `cool_down` (419), `plain_body` (436), `with_note`. The manifest declares none of these caller-to-callee edges, which the procedure (line 152) requires. Fix: move the boundary to a function edge (451 or 480) or declare a 1-line overlap, and list the entry/exit edges.

B2. Counterpart ranges start or end inside test bodies, so tests the spec names are cut: F14 1025 is inside `test_all_models_out...`'s predecessor (`test_no_backup_can_hold...` runs 1018-1031); F14 1160 cuts `test_cooldown_with_an_injected_clock` (1151-1174), a cooldown test the spec names; F14 1560 cuts the test at 1554; F15 1470 cuts `test_every_launch_restores_grep_and_glob` (1467); F15 3460 cuts `test_orca_starts_untagged_when_the_name_list...` (3456-3473). Fix: round every range to whole test functions.

B3. The 2.4 page assigns no aspect to any slice (ranges only), so check (c) cannot be satisfied. Several spec keywords have no located source: "replay" does not appear in F10 (grep), and the F15 ranges chosen as "replay/state" (1441-1470 label/transcript resume; 3306-3460 orca naming) are not shown to be about replay; "health/fingerprint/audit": F01 `shim_health_status` (936-961) and `shim_listener_pid` (922) sit outside 962-1155; F05 771-820 starts mid `_settings_key` (748-779) and the actual fingerprint pair `settings_digest`/`code_digest` is 780-800, so it is covered, but without a stated aspect. Fix: add an aspect line per slice mapping each keyword (switch_reason, cooldown/Retry-After, _FirstByteResponse, first-byte vs connect failure, error-body/truncation/context, no retry after stream start, health/fingerprint/audit, actual-backend limits, replay, process-local vs session state, launch isolation) to a slice.

B4. No unique per-slice output path for 2.4 is recorded. Only the topic output `research/04-fallback-state.md` is named; the procedure requires `research/source-slices/<consumer>/` unique outputs. Fix: list the four slice output paths.

### Minor notes
N1. F15 3136-3305 is excluded with no stated relevance justification (manifest line 85: "3136-3460 ... selected 3306-3460"). Procedure line 152 requires a source-backed reason for exact exclusions; I could not confirm relevance either way without source reads. Treated as part of B3 (aspect/relevance) and noted here.
N2. Slices 1-4 do not all carry `research-notes`/`scope-03` that the producer spec says to read; acceptable only if each slice's brief carries the relevant digest rows. Brief size 55 is an estimate; the full producer prompt (~8.9k chars) is not itemized.
N3. F01 962-1155 ends at line 1155; `apply_profile` starts at 1157, so 1156 is presumably the closing brace; verify when fixing.

## Self-Audit
Attempted disproof of PASS by: recomputing every slice total and range length; checking `wc -l` for all 8 files; grepping function/test boundaries at every range edge (F10 393-535, F01 922-1157, F05 748-822, F14 1003-1175 and 1414-1554, F15 1441-1484 and 3136-3474); grepping for replay/fingerprint/audit/health in F10, F14, F15; reading F10 452-463. Passing checks: F10 union, arithmetic, <=1000, counterpart labeling, ordering. Confidence denominator: 6 checks (a-f) against 4 slices and 11 spec keywords; 3 of 6 checks pass.

Not verified: F14/F15 relevance of the excluded ranges (no source reads allowed).
