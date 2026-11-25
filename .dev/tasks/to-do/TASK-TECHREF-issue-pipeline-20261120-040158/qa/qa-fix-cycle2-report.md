# Gate 3 fix report (cycle 2)

**Phase:** report-validation fix (cycle 2)
**Date:** 2026-11-20
**Status:** Complete
**Work list:** qa/qa-consolidated-findings-c2.md (one BLOCKING finding: N-1)
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md

## Claim check against the snapshot (read-only)

- `src/superclaude/hooks/scripts/launch-level-guard.sh:487-490` (snapshot /home/coder/.cache/ic-snap-20261120/master): when the verb words are not on the allow-list (`:480-484`) and not `- -` (`:486`), a call whose last word is `--help` or `-h` is allowed if there is no glob character (`LL_GLOB = 0`) and `${#ws[@]} - i <= 4` (at most four words counting from `orca`; the code comment says "help only on a short call: orca, two verb words, help"); every other such call is ESCAPE (`:489`).
- `tests/hooks/test_launch_level_guard_worker.py:226-230`: `test_the_read_only_orca_forms_stay_allowed_for_a_bound_worker` pins `orca list --help` and `orca agent launch -h` as allowed.
- Result: the universal claim "every other orca call is ESCAPE" is false; the allow-list is exhaustive except for a short help call.

## Fix summary

Blocking findings: 1 (N-1). FIXED: 1 (applied at the 3 named places plus 1 further place that repeated the claim). UNFIXABLE-FROM-EVIDENCE: 0.

## Fixes (one entry per place)

| # | Finding | Document line (after edit) | Change | Evidence |
|---|---|---|---|---|
| 1 | N-1 | 354 (2.4 row 6) | "every other `orca` verb off the allow-list is blocked" now reads "... is blocked, except a short help call (`<verb words> --help` or `-h`, at most four words counting from `orca`, no glob character; `orca list --help` and `orca agent launch -h` pass), and only for the command word `orca`"; evidence cell gained "help call `launch-level-guard.sh:487-490`, pinned by `tests/hooks/test_launch_level_guard_worker.py:226-230`" | `src/superclaude/hooks/scripts/launch-level-guard.sh:487-490`; `tests/hooks/test_launch_level_guard_worker.py:226-230` |
| 2 | N-1 | 1258 (5.3 G2 rule 2 paragraph) | "every other orca call is ESCAPE (`GD:480-491`)" now followed by ", except a short help call: a call whose last word is `--help` or `-h`, with no glob character and at most four words counting from `orca` (`orca, two verb words, help`), is allowed (`GD:487-490`; pinned by `test_the_read_only_orca_forms_stay_allowed_for_a_bound_worker`, `orca list --help` and `orca agent launch -h`, `T/hooks/test_launch_level_guard_worker.py:226-230`)" | same as row 1 |
| 3 | N-1 | 1448 (8.1 guard-stack row) | "every other `orca` call is ESCAPE" now ", except a short help call (`<verb words> --help` or `-h`, at most four words counting from `orca`, no glob character)"; evidence cell gained "`:487-490` (short help call, pinned by `tests/hooks/test_launch_level_guard_worker.py:226-230`)" | same as row 1 |
| 4 | N-1 (other repeat found by grep) | 2241 (Appendix test inventory, `test_launch_level_guard_worker.py` row) | "other workers, groups and orca verbs blocked" now "orca verbs off the allow-list blocked (a short `--help` or `-h` call stays allowed, `:226-230`)" | `tests/hooks/test_launch_level_guard_worker.py:226-230` |

## Checks after the edits

- Grep for `every other` and `allow-list`: no other place states the universal claim (lines 646, 1236, 1321 and 2138 name the allow-list without saying every other call is blocked; lines 1911 and 2214 are unrelated uses of "every other").
- PR 686: still exactly one sentence (line 218, Section 1). `docs/designs/orchestrator.md` is not cited.
- Only the document and this log were written; nothing under the snapshot was written.

Status: Complete
