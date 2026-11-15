# Local allocation acceptance ledger (qa/local-allocation-acceptance.md)

**Preamble for a reader with no context.** This is the ledger for Phase 1 item 1.3 of the issue-463 research task (task folder `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`; start with `HANDOFF.md` there). Item 1.3 gates the research: before any worker investigates source code, an independent verifier must PASS the plan (`qa/local-source-allocation.md`) that splits 18 files / 16,719 lines into per-worker assignments of at most 1000 lines. This ledger records each verifier's verdict, the blocking findings still open, and the gate state. Per-topic reports live at `qa/input-allocation/2.N/check-1.md` (cycle 1, against manifest v1) and `check-2.md` (cycle 2, against manifest v2). Topic numbers 2.1-2.5 are the five Phase 2 investigations: 2.1 launcher flow, 2.2 defaults/policy, 2.3 proxy request fidelity, 2.4 fallback/replay/state, 2.5 tests/packaging/callers.

**Gate status: HALTED, NOT ACCEPTED.** `[HALT-MONOTONICITY] |F|=5` (wire message kept verbatim for compatibility). No source worker may dispatch. Owner ruling needed: `OPEN-DECISIONS.md` D1.

## Gate arithmetic (task file lines 136-138 rules applied in order)

1. Regression (previously PASS now FAIL)? None: no topic passed in cycle 1.
2. Monotonicity: failing set by item ID. Cycle 1 F_1 = {2.1, 2.2, 2.4, 2.5} (2.3's check never ran: launch failure; if counted as a FAIL, |F_1| = 5). Cycle 2 F_2 = {2.1, 2.2, 2.3, 2.4, 2.5}, |F_2| = 5. Non-shrinking either way, so HALT.
3. Cap: 1 of 2 fix cycles used, 2 of 3 review rounds used; the halt, not the cap, stops the gate.
4. Finding-level counts for reference: cycle 1 = 13 (3+4+0+4+2; 2.3 unmeasured), cycle 2 = 14 (3+2+4+2+3). Topics 2.2 and 2.4 shrank (4 to 2 each); 2.1 and 2.5 did not (3 to 3; 2 to 3); 2.3 first measured.

## Per-topic ledger

| Topic | Cycle 1 | Blocking c1 | Manifest fix | Cycle 2 | Blocking c2 | Accepted |
|---|---|---|---|---|---|---|
| 2.1 | FAIL | 3 | v2 | **FAIL** (`2.1/check-2.md`; "Blocking count: 3" at line 76) | 3 | no |
| 2.2 | FAIL | 4 | v2 | **FAIL** (`2.2/check-2.md`) | 2 | no |
| 2.3 | no report (launch failed: missing node binary) | n/a | v2 written before first run | **FAIL** (`2.3/check-2.md`) | 4 | no |
| 2.4 | FAIL | 4 | v2 | **FAIL** (`2.4/check-2.md`) | 2 | no |
| 2.5 | FAIL | 2 | v2 | **FAIL** (`2.5/check-2.md`) | 3 | no |

## Register of open blocking findings (cycle 2, 14 total; fix these in manifest v3)

Line numbers below are in the source files at base commit `933cf3a4f`. Read the cited report for full evidence.

**2.1 (3)**: report `2.1/check-2.md` lines 59-62.
- B1: the "fixed context 344" per slice is not supported by the manifest's own rule; with a 100-line excerpt it is 404 and slices 1, 2, 4 total 1004, 1039, 1019 (over 1000). Estimates replaced required measurements.
- B2: the pre-parse `case` at ccsession 684-727 has no owner: slice-1 (1-560) is told it is at its tail, slice-2 is told it is slice-1's entry edge, but it sits inside slice-2's range.
- B3: three obligation-map entries name the wrong slice (permissions defaults at 137-141 unmapped and line 881 mislabelled; resume line 1298 belongs to slice-3, not 4; see report for the third).

**2.2 (2)**: report `2.2/check-2.md` lines 37-39.
- B1: seven `python3 "$CCSESSION_MODELS" ...` call sites in ccsession are in no 2.2 slice: lines 883, 895, 983, 994, 995, 1168, 1170.
- B2: the stated exclusion of ccsession 1161-1190 ("setup_shim tail") is false: setup_shim ends at 1155 and 1157-1190 is `apply_profile`; slice-4's cut also splits `apply_profile`.

**2.3 (4)**: report `2.3/check-2.md` lines 27-33.
- B1: the signed-history/thinking/tool-use fixture, `test_out_of_usage_switches_and_cools_down` (test_ccsession_tiers.py 898-1002), is in no slice.
- B2: test_ccsession_tiers.py 1215-1230 cuts `test_native_picker_uses_current_curated_rows` (def 1194, next def 1314) mid-test and mid-class.
- B3: models.py 748-830 ends mid-function; `shim_upstream_problem` runs 822-846 (the manifest claims "whole functions").
- B4: alias helpers the proxy calls (`gateway_alias` 170, `is_native_model` 174, `assign_aliases` 316, `load` 196, `tier_env` 198, `tier_mode` 199, `tier_access` and more, line numbers are in the proxy file) have no counterpart range and no exclusion evidence.

**2.4 (2)**: report `2.4/check-2.md` lines 37-43.
- B1: three ranges still cut a function or test the manifest calls whole (details at line 37 of the report).
- B2: no caller-to-callee edges declared between slice-1 (owns `switch_reason`, `retry_after_seconds`, `cool_down`, `cooling_until`, `clock`, `plain_body`, `_cooldowns`) and slice-2 (the handler that calls them).

**2.5 (3)**: report `2.5/check-2.md` lines 31-41.
- F1: manifest says boundaries are at whole-test edges; most are mid-test (e.g. test_ccsession_tiers.py 560/561 inside a parametrize list, 2257/2258 inside a call, 3050/3051 between a def and its docstring; test_ccsession_tag.py 560/561, 1100/1101, 1560/1561, 2120/2121, 3240/3241, 3800/3801, 4360/4361). The false statements are on lines 80, 81, 99 of manifest v2. True edges: F14 1686/1687 and 2552/2553, F16 160/161, F13 303/304, F17 560/561.
- F2: slice-0's caller search covers `src/` only; `tests/cli/test_install_retired_mcp.py` (776 lines; line 519 patches `superclaude.cli.install_ccsession.wire_ccsession`) is a caller in no slice. Search must cover `src tests` and the found file needs a slice or an evidenced exclusion.
- F3: per-slice aspects for 2.5 are not named; the order "slice-0 produced and accepted before slices 1-21 start" is not stated.

Minor and medium notes (not blocking, not rechecked) are in each report's own section.

## Next action

Owner answers `OPEN-DECISIONS.md` D1. If option 1 (v3 built from a mechanical def/test index with measured budgets): rewrite the manifest, emit cycle-3 check items in the `local-allocation-checks` region of the task file, dispatch five verifiers, and update this ledger. This file is the only place the cycle history is consolidated; keep earlier rows and add a cycle-3 column rather than overwriting.
