# QA Report: Gate B, citation-evidence lens (Phases 4 and 5)

**Topic:** issue-watch implementation, `record.py`, `launch.py` and their tests
**Date:** 2026-11-07
**Phase:** task-integrity style review, citation-evidence lens (rf-qa, `fix_authorization: false`, report only)
**Fix cycle:** 1 (first review of Gate B for this lens)

---

## Overall Verdict: FAIL

Two blocking findings (B-1, B-2). Every other finding is minor and recorded as a note.

The prompt asked me to assume at least 15 errors. I found 2 blocking and 9 minor. I did not pad the list: every design line number, decision id, open-question id and repository file:line anchor cited in the 10 files resolves and says what it claims, except the items below.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `launch.py` design line citations (D 625, 629-634, 636, 741, 8.4, 9.2, 9.3, 5.3) | PASS | Read design lines 604-636, 674-693, 741, 215-246; each cited range holds the cited text |
| 2 | `record.py` design citations (7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 5.4, 6.2 step 14, line 449) | PASS | Read design 385-533 and 357; step 14 is "Health stamp", line 449 is the dry-run.json replacement rule |
| 3 | Repository file:line anchors (`origin_repo.py` 65-69, 86-99, 156-174; `install_user_setup.py` 35, 198-221, 216-219; `swarm/atomic.py` 14, 33) | PASS | Read each file; `_NAME`/`_ORIGIN_PATTERNS` at 65-69, `parse_origin_url` at 86-99, `_ORCA_CLIS` at 35, `_find_orca` 198-221 with the `any(...)` at 219 outside the `try` (209-218), `write_prepared_bytes` def at 14 and `except Exception` at 33 |
| 4 | DF/OQ/C ids cited in `src` (DF-01, 11, 15, 17, 36, 42, 43, 54; OQ-40, 47, 48; C16, C18, C19) | PASS | Read `research/06-gap-fill-decisions.md` rows and design rows C2, C3, C4, C16, C18, C19; OQ-40, 47, 48 found at task file lines 955, 958, 959 |
| 5 | `test_record.py` citations and AC/FR/NFR name suffixes | PASS with notes | Read lines 1-190, 586-650, 750-870, 1124-1325, 1355-1630; header ranges T-1..T-3, T-4..T-9, T-10..T-13 match the tests below them; pair counts 15 allowed and 40 refused recomputed by hand; suffix notes m-1, m-2, m-3, m-8 |
| 6 | `test_launch.py` citations | PASS with notes | Read all 746 lines; "spec's seven inputs" matches spec FR-012 GWT (`9`, `"9"`, `True`, `0`, `-1`, `10**9`, `9.0`); design ranges 627-636, 629-634, 636, 689, 741 hold; finding B-2 |
| 7 | `conftest.py` citations | PASS with note | Design 7.6 crash points C1-C5 match the docstring and the DF-15 recipe table; note m-5 |
| 8 | `test_find_orca_parity.py` and `test_origin_parity.py` citations | FAIL (B-1) | C2, C3, C19 rows and `install_user_setup.py:216-219` verified; the "raises on a str, a dict" statement is false for empty values |
| 9 | `test_marker_contract.py` (DF-21, DF-46, FR-009) | PASS | `claim.md` holds the marker twice, `claim-comment.md` ends with `<!-- sc:issue:claim -->`, `CLAIM_MARKER` at `predicates.py:14`, `MARKER_JQ` at `github.py:61` |
| 10 | The two Orca `_assumed_shape` fixtures (`source` and `note` fields) | PASS | Design section 15 lines 840 and 841 hold the cited rows; both fixtures carry `"_assumed_shape": true` |
| 11 | No gh or Orca reply shape marked UNVERIFIED (design 829-847) is stated as fact outside an `_assumed_shape` fixture | FAIL (B-2) | Inline Orca reply bodies in `test_launch.py` lines 524 and 554 |
| 12 | Orca agent literal only in `launch.py` and its pin test | PASS | Grep of `claude` over `**/issue_watch/**`: `launch.py:27`, `test_launch.py` only (lines 75, 82, 112, 113, 159, 501, 743, 744); other hits are the `.claude/` directory name in `test_marker_contract.py` |
| 13 | No file reads anything under `.dev/` | PASS | Grep `\.dev` over `**/issue_watch/**`: only text mentions (`test_launch.py:501`, `test_marker_contract.py:8`) and fixture `source` strings; no `open`, `read_text` or `Path` against `.dev` |
| 14 | No model-alias string in any file | PASS | Case-insensitive grep for opus, sonnet, haiku, fable, gpt, gemini over `**/issue_watch/**`: no match |
| 15 | Change set accuracy (line counts, files, test counts, Gate A file list) | PASS with note | `wc -l` matches all 10 rows; `p4-g1-summary.md` says 1094 passed, `p5-g1-summary.md` says 1372 passed; mtimes agree with "cycle 2 changed audit.py and test_audit.py only"; note m-6 |
| 16 | Design statements about Orca help text (D 616, 625: "Orca 1.4.245 help") | UNVERIFIABLE | No Orca help text is in the repository; I did not run the binary (outside this lens) |

## Summary

- Checks passed: 13 / 16 (two with notes), failed: 2, unverifiable: 1
- Blocking findings: 2
- Minor notes: 9
- Issues fixed in place: 0 (report only)

Confidence: Verified: 15/16 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% (15 / (16 - 1))
Tool engagement: Read: 31 | Grep: 17 | Glob: 2 | Bash: 6
Tool calls (56) exceed the 16 checklist items. No web research was performed, so no tavily or fallback counts apply.

## Findings (numbered; blocking first)

| id | severity | file | evidence | expected versus actual |
|----|----------|------|----------|------------------------|
| B-1 | BLOCKING | `src/superclaude/cli/issue_watch/launch.py:148-149`; `tests/issue_watch/test_find_orca_parity.py:7-12`; decision DF-36 text it copies | `_lists_orca_cli` docstring says the original `_find_orca` "raises on a `topics` that is null, an int, a str, a dict, or holds a non-dict". The test module docstring repeats it ("a probe reply whose `topics` is null, an int, a str, a dict, or holds a non-dict element, with exit 0"). `install_user_setup.py:219` is `any(t.get("name") == "orca-cli" for t in topics)`: an empty str or empty dict iterates zero items and does not raise. The same test file pins that: `_SAME_RESULT["empty_topics_str"]` and `["empty_topics_dict"]` (lines 50-51) expect the same answer from both functions, and `_ORIGINAL_RAISES` uses only the non-empty `"orca-cli"` str and a non-empty dict | Expected: the claim names the exact shapes that raise (null, int or bool, non-empty str, non-empty dict, a list with a non-dict element). Actual: the blanket "a str, a dict" is false for `""` and `{}`, and the file's own table contradicts its docstring. Fix: narrow the sentence in both docstrings to "a non-empty str or dict" |
| B-2 | BLOCKING | `tests/issue_watch/test_launch.py:524` (`_id_reply`) and `:554` | Both build an Orca launch reply inline: `{"receipt": {"operation_id": ...}}` and `{"outcome": {"kind": "launched"}, "receipt": {}}`. Design 636 and section 15 line 840 mark the reply JSON (`outcome.kind`, `receipt.detail`, the operation id path) UNVERIFIED, and design 847 says each UNVERIFIED answer lives in an `_assumed_shape` fixture. The path `receipt.operation_id` is a proposal (the design names only `outcome.kind` and `receipt.detail`). The helper hard-codes that proposal in test code with no `_assumed_shape` marker and does not read `OPERATION_ID_PATHS[0]`, so about 15 cases (lines 568, 604-624) keep passing on the old shape after FU-1 changes the paths | Expected: the success reply body comes from `orca_launch_success.json` (or is built by walking `OPERATION_ID_PATHS[0]`), and the no-id body is derived from it. Actual: the unverified shape is written as literal fact in two helpers outside any `_assumed_shape` fixture. Runtime risk is low today; the required confirmation fails |
| m-1 | minor | `tests/issue_watch/test_record.py:1364,1371,1380` | Day-cap window tests are named `__fr016_fr023`. Spec FR-023 is the `considered` map; the half-open (now - 24 h, now] window is FR-024 (spec line 169; later tests use `fr024`). Design AC-10 maps to FR-016, FR-023, FR-024, so the label is traceable but misses FR-024 | Expected `fr016_fr024`. Actual `fr016_fr023` |
| m-2 | minor | `tests/issue_watch/test_record.py:1236` | `test_t13_reset_...__fr016_fr023_fr024`: reset moving `consumed_at` to `consumed_log` is FR-024 and FR-026; FR-016 and FR-023 are not asserted | Label wider than what the test asserts |
| m-3 | minor | `tests/issue_watch/test_origin_parity.py:113` | `test_ac16_original_module_is_not_registered_in_sys_modules__nfr003`: NFR-003 is repo and Project pinning (spec line 209); the test checks module-loading hygiene | Wrong id; no NFR covers it |
| m-4 | minor | `tests/issue_watch/test_record.py:4-5` | Docstring says "Test names carry the AC, FR and NFR ids they assert". Many tests carry none (for example `test_valid_document_loads_with_int_keys_and_aware_times` line 173, `test_lock_is_released_on_normal_exit_and_reusable` line 769, `test_save_calls_write_prepared_bytes_through_the_lazy_import` line 608) | Claim wider than the file |
| m-5 | minor | `tests/issue_watch/conftest.py:131-133` | Docstring says `test_crash_injection.py` "injects it by patching `os.replace`". Glob finds no such file at this gate (it is a Phase 8 deliverable per DF-15) | Present-tense claim about a file that does not exist yet; must be true by the Final gate |
| m-6 | minor | `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/gate-b-change-set.md:32-38` | "Decision rows applied" omits DF-03, DF-04, DF-22 and DF-31, which the files cite (`test_record.py:1460`, `record.py:829` names the DF-22 proposal `dry_run_shadow_reset`, `test_launch.py:738`). "Design line ranges" omits D 741 (cited at `launch.py:121`, `test_launch.py:148`) and D 640-647 (`find_orca` timeout rule) | Lists incomplete against the citations in the files |
| m-7 | minor | `src/superclaude/cli/issue_watch/record.py:826-829` | Docstring ties the `dry_run_shadow_reset` warning to "design line 449". Line 449 says only that "a warning line is written"; the name is a [PROPOSAL] from DF-22, not the design | Cite DF-22 for the name |
| m-8 | minor | `tests/issue_watch/test_record.py:591` | `test_ac22_save_fsyncs_the_state_directory_last__nfr005`: the directory fsync is required by NFR-011 ("a parent-directory fsync", spec line 225) and design 7.6 | Label should be `nfr011` |
| m-9 | minor | `src/superclaude/cli/issue_watch/record.py:24-29` against design line 239 | Design 5.3 lets `record` import `predicates` "types only"; the module imports `format_utc`, `parse_utc` and `valid_issue_number` (functions) as well as `ApprovalResult`. Not recorded as a deviation in the file or the decision register. Behaviour is unaffected | Record the reading, or import types only |

Other notes (not graded as findings, no fix required):

- `test_launch.py:517,589,596,622` call `agent_session_operation_unknown` "the lost-reply code". Design 841 and C16 mark that meaning UNVERIFIED. Wording only; the fixture note already says "assumed, not captured".
- `record.py:427-433` (`disabled_since`) uses `os.stat`, which follows symlinks, while `disabled()` uses `lexists`. For a dangling `DISABLED` symlink `disabled()` is True and `disabled_since()` is None, so `status` would show a null `disabled_since` while the switch is on. No test covers this (`test_record.py:797` checks only `disabled()`). Outside this lens; passed to the behaviour lenses.
- `launch.py` documents "caches nothing" (design 614 puts the per-cycle cache in `OrcaLauncher`); the departure is OQ-41a in the task file but the code does not cite it.
- `test_marker_contract.py:24` reads the real `~/.claude`; an older installed copy lacking the marker would fail the test. DF-46 allows this by design.

## Citation sweep result (what held up)

Every line-range citation in `launch.py`, `record.py`, `test_launch.py` and `test_record.py` was opened and matched: D 449, 625, 627-636, 629-634, 636, 689, 741; design sections 5.3, 5.4, 6.2 step 14, 7.1-7.6, 8.4, 9.2, 9.3; `origin_repo.py` 65-69 and 86-99; `install_user_setup.py` 35 and 216-219; `swarm/atomic.py` 14 and 33; C2, C3, C4, C16, C18, C19 rows; FR-009, 012, 013, 014, 015, 019, 023, 024, 025, 026, 028; NFR-005, 008, 011; AC-7 to AC-13, 16 to 18, 22 and 25; DF-01, 11, 15, 17, 21, 31, 36, 42, 43, 44, 46, 54; OQ-40, 47, 48.

## Actions Taken

None. `fix_authorization: false`; only this report file was written.

## Recommendations

1. Fix B-1: narrow the `topics` sentence in `launch.py:148-149` and `test_find_orca_parity.py:7-12` (and note the same wording in DF-36) to non-empty str and dict.
2. Fix B-2: derive the Orca reply bodies in `_id_reply` and the no-id case from `orca_launch_success.json` or `OPERATION_ID_PATHS[0]`.
3. Optionally fold the minor notes into the same fix pass; none of them fails a review and none is rechecked later.

## QA Complete

