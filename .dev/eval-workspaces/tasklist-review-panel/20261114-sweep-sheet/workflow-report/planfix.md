Change list (line numbers are after the edits). P = .dev/tasks/to-do/TASK-WF-implementHomeCod-20261114-200449/TASK-WF-implementHomeCod-20261114-200449.md; SW = .dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
1. SW/DESIGN.md 69, 86, 316, 321, 325, 703, 820: K = 8 per class, K_single = 12 when only one class has candidates after find (attach runs on its top 12, so a one-class sheet holds 12; 1 for C3); 12-lookup time effect stated as unmeasured and bounded at 12 (lines 69, 316, 820); values entry now K, K_single, cap (703).
2. SW/TESTING.md 87, 190: per-class cap lines now say attach ran on the top 12 when k = 1; the DD-10 row has the two cases (8 with a second class, 12 alone) and the new test_single_class_attaches_top_12.
3. SW/TESTING.md 40, 176: override guard is by kind (paths under /tmp; SW_KILL_S a number 0.1 to 15, so 1 passes; SW_PREPASS_CMD only sleep or false); two new test names.
4. P 21, 23 (Constraints): gitcheck defined once (git add/commit/tag/push only as git -C "$SB...", printed text or a comment); Git scope names the sandbox's own git calls as non-repository writes.
5. P 28: sub-steps 0.4, 0.5, 0.6 mapped to Tasks 24, 26, 6 and 28.
6. P 36, 40, 43 (Task 1): values.json holds K, K_single, cap; override guard by kind (sw_assert_override); tests test_kill_s_is_numeric_only, test_prepass_cmd_stub_only, test_values_selection_constants.
7. P 61 (Task 3): review-suite subprocess uses the $T form (no bare uv run pytest).
8. P 122, 127 (Task 8): sandbox git writes spelled git -C "$SBT"; gitcheck $SW/bin must print nothing.
9. P 134 (Task 9): Depends on Task 3 added.
10. P 160, 163, 164 (Task 11): K / K_single rule, Ctx.scope_string, test_single_class_attaches_top_12, two attach cases.
11. P 216 (Task 16): E5 with no source reports C2 not applicable through Ctx; Task 22 writes it to prepass.json.
12. P 250, 254 (Task 19): top K per class follows the Task 11 rule; test_single_class_fills_12 states attach ran on 12 and the sheet holds 12.
13. P 286, 287 (Task 22): new test_scope_string_and_no_source_in_prepass_json; seed-2 qualifier restored (ids and statuses); scope string and no_source asserted in prepass.json.
14. P 321, 327 (Task 25): four F-REPORT fixtures created (problem_no_finding, promote_long_id, promote_short_anchor, promote_dup_id). P 336, 343 (Task 26): step 0.5 import timing folded in, writes SW/results/import-time.md. SW/IMPLEMENTATION.md 45, 114, 134: row 0.5 deferred to step 11, step 8 K note, step 11 runs 0.5.
15. P 354, 356 (Task 27): git grep check replaced by gitcheck with a probe; test_no_source_run added. P 426, 435 (Task 33): test_freeze_json_hashes_match_files moved to test_order.py, freeze.sh and check-order.sh avoid git tag, gitcheck and the opus grep re-run over the finished bin/.
