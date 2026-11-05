# Refactoring Plan (merge of the three reviewer cards onto base Variant 1)

## Overview
- Base: Variant 1 (reviewer-1 analyzer card). Incorporated: Variant 3 and Variant 2 strengths, plus the invariant-probe MEDIUM findings.
- Output: a merged reflection verdict `merged-verdict.yaml` (required plan notes RN-*, executor notes EN-*, owner questions OQ-*, rejected/downgraded findings, convergence and probe results).
- Approval: auto-approved (non-interactive run).
- Standing rule: the plan package is never edited from reflect findings (workflow rule). The required notes are handed to the /sc:implement run as written context and become acceptance conditions of that run.

## Planned Changes

Required plan notes (blocking until satisfied by the implementation; source: debate X-001 plus Round 2 convergence)

| Change | Source | Target task(s) | Content | Risk |
|---|---|---|---|---|
| RN-1 | V1 F1; V2 R2 point (b); V3 F4; INV-003 | Tasks 1, 3, 4, 7 | An invalid CCSESSION_NAME, an invalid or empty --auto-name result (control character, over 245 bytes, folder name with a leading dot or 4-byte characters), or an unexpected --ask status never stops Claude from starting. Fallback order: drop the bad name with a stderr warning, then auto-name, then plain untagged start. Criteria and tests: folder with a leading dot, name with a tab, 300-character CCSESSION_NAME, name equal to a saved label (decide and assert: new auto-name, never a silent resume), failing --auto-name (unwritable topics dir) still reaches the fake Claude, exit status never 2 | Medium |
| RN-2 | V1 F10; V3 F4; X-003; INV-002 | Tasks 3, 4, 7 | Do not lift Claude `--name`/`-n` into ccsession's --name. A launch whose own Claude arguments carry --name/-n (or `--name=`) counts as name-carried: no question, no auto-name, arguments pass through unchanged. CCSESSION_NAME is the supported explicit name, validated (RN-1) and unset before exec. This replaces Task 3 criterion 2 and the Task 7 `--name x` case; report the change to the owner (OQ-2) | Medium |
| RN-3 | V1 F12; V3 F1; INV-006 | Task 1 | Dispatch --auto-name in the early fast-path case (ccsession:597-628) after ensure_names_migrated, so option-shaped task text is not consumed by the argument loop (ccsession:648-723); tests for the texts `--model`, `--claude-args`, `--shim`, `--tier=x` | Low |
| RN-4 | V3 F2; V1 F6, F7; V2 F2; V3 R2 new | Task 5 | Task 5 names these additionally: the two Enter reopen tests (`test_orca_a_new_tab_or_a_rerun_is_still_asked`, `test_orca_relaunch_whose_conversation_is_gone_is_asked`) move to the auto-named result; `test_orca_invalid_name_asks_again` is rewritten; the Ctrl+C line-mode test drops its "the prompt" argument; `test_orca_saved_name_is_listed_and_resumes_before_the_prompt` becomes `--name demo "fix it"` form; CCSESSION_NAME is added to the env exclusion lists in test_ccsession_tag.py and test_ccsession_tiers.py. The sentence "keep the relaunch reopen tests as they are" applies only to tests that do not press Enter | Low |
| RN-5 | V1 F2, F5 (required per V3) | Tasks 2, 4 | Read the typed line with `IFS= read -r`, test the raw line for control characters and the 245-byte rule before any trimming; put `--` before an exit-3 message that starts with `-`; tests: leading tab, trailing tab, mid-line tab, "- a list", "--version" | Medium |
| RN-6 | V3 new point; INV-010 | Task 4 | ccsession-orca unsets CCSESSION_ASK_TIMEOUT and CCSESSION_NAME before the final exec (the one-second timeout test sets the variable while the record must not contain it) | Low |
| RN-7 | V1 F11; A-004; INV-005 | Task 3 | Classification covers `--session-id=*`, `--prefill=*`, `--name=*`, a trailing --name with no value, and values of known value-taking options (--model, --permission-mode, --add-dir, --allowedTools, --mcp-config) are not counted as a task; unknown options fail safe (counted as task); tests for one of each form | Medium |
| RN-8 | V2 F1 | Task 6 | Add a test with CCSESSION_ASK_TIMEOUT=2 asserting the hint reads "auto-named after 2s", plus the default-hint test, so a default left unlimited fails | Low |
| RN-9 | V1 F14; V2 F5; V3 F8; INV-004 | Task 1 | The auto-name stamp carries seconds or a short random part; when the 80-character cap applies, the folder name and task words are cut first and the stamp is kept; a "-2" suffix is allowed to exceed the cap or the cap is 76; test: two calls in the same minute with no saved topic give different labels | Low |
| RN-10 | V3 F3 | Task 7 | The executor, not the tests, writes ./artifacts/launch-paths.md from the final `pytest -k orca -v` output; no test opens a path outside tmp_path | Low |
| RN-11 | V3 F5 | Tasks 2, 11 | ccsession-orca passes the auto-name hint; the default hint of ask_session_name stays as today for other callers; the Task 11 Coder handoff states that the 30 s default now applies to the New Terminal hook too | Low |
| RN-12 | V2 F3 | Task 9 | Acceptance criterion also pins the `--session-id` statement (README.md:266) | Low |

Executor notes (not blocking; follow where cheap)
- EN-1 (V1 F3): second paste probe with a 100-200 ms wait under `stty -icanon min 0 time 0`, both probes inside if/&& lists because set -e is on (ccsession:98).
- EN-2 (V1 F4; INV-011): drain the rest of a paste with python3 and raw bytes (bash 3.2 has no `read -t 0.2`, ccsession:1426); cap or refuse text above about 128 KiB.
- EN-3 (V1 F13): capture the --ask status with `rc=0; name=$(...) || rc=$?`; keep a `trap 'exit 130' INT` around the capture; tests accept exactly 130 and check ICANON afterwards.
- EN-4 (V1 F9): verify `--version`, `--help` and non-session subcommands (mcp, doctor, update, install) pass through untagged; V1 gave no evidence that Orca sends them.
- EN-5 (INV-009): a launch carrying CCSESSION_NAME is name-carried and therefore skips the pull request 355 reopen; document it.
- EN-6 (V3 F6, F7): write the Task 4 rule as one ordered decision list; state that `-k orca` is expected to fail until Task 5.

## Changes NOT Being Made
- V1 F1 auto-name half as a blocker: Task 1 already requires validate_label; kept as RN-1's folder-name case only.
- V1 F3, F8, F9, F13 (no evidence): downgraded to executor notes or folded into RN-6.
- V3 F4 class "authorized": rejected; the lift is a plan-author decision and is now dropped (RN-2).
- V2 F5 hook-suffix mitigation: rejected as a guarantee; the suffix exists in ccsession (sync_name, ccsession:336-337, 391-398) but renames the list only.
- No change to the plan package itself.

## Owner questions to report
- OQ-1: print mode (-p/--print) and CCSESSION_AUTOSTART=0 stay untagged (plan-author decision, V3 keep; calibrator suggested it may be drift for `-p <prompt>`).
- OQ-2: RN-2 reverses the plan Constraint that lifts Claude --name; a Claude --name now passes through unchanged and counts as name-carried.
- OQ-3 (INV-001, HIGH, addressed as a documented condition): nothing in this repo makes an orchestrator pass a task or name; a task typed after the question appears is still read as a name (ccsession:1482-1489). Owner decision (a) accepts this; Task 9 and Task 11 must say so.

## Review Status
auto-approved
