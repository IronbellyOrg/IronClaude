# QA Report - Research Gate (Gap Detection Lens)

**Topic:** Issue #339 Phase 1 MDTM task file (orchestrator mode), first items fix R3-B1, R3-B2, R3-B3
**Date:** 2026-11-08
**Phase:** research-gate
**Lens:** gap-detection
**Fix cycle:** N/A
**Fix authorization:** false (report only)
**Assigned files:** 01-file-inventory.md, 02-patterns-conventions.md, 03-integration-points.md, 04-design-fixes-r3.md, 05-test-verification.md, 06-template-examples.md

Status: Complete (see end of file)

---

## Working notes (appended as the review proceeds)

- Read scope map `research-notes.md` (66 lines) and design sections 15, 16, 17, 18 (`docs/designs/orchestrator-mode.md:864-1013`).
- 01-file-inventory.md (354 lines, read all): covers every NEW and EXISTING file in step table 1.1 to 1.24b with anchors. Lists step artifacts of 1.0a, 1.0b, 1.4, 1.16a, 1.29 only as filenames (line 210). Rows 1.25 to 1.29 collapsed to "no file edits ... verify" (line 344). Sections 16 and 17 appear only as line ranges (lines 21-22).
- 02-patterns-conventions.md (169 lines, read all): names `tests/cli/sweep/` as the test location (line 157), which contradicts the design's `tests/sweep/` (design 15.2 rows 1.8 to 1.13). Researcher flags it as an inference (line 159).
- 03-integration-points.md (120 lines, read all): strong. Finds a fifth pin the design misses (`RULE_PHRASES["never-as-worker"]`, line 45-50), the AC-0.9 write-verb audit (IP-3), and that R5 must land no later than the step that creates `sweep.md` (line 68, 109). That conflicts with the design step table, where R5 is step 1.20 after 1.14 to 1.16. Does not pick up the `worker-show` "may write the database" note that 04 line 67 hands to researcher 3.
- 04-design-fixes-r3.md (232 lines, read all): exact edit text and fixtures for R3-B1 (9 edits, 10 fixtures), R3-B2 (5 edits, 7 fixtures), R3-B3 (4 edits, 4 fixtures), plus per-finding QA gates (section 5). Actionable.
- 05-test-verification.md (157 lines, read all): strong on pytest config, `tests/sweep/__init__.py` need, guard risk, CI xdist. Step 1.28 grep narrowed to the two sweep files (line 148). No coverage of 1.29, 1.0a, 1.16a.
- 06-template-examples.md (164 lines, read all): good template rules and human-gate encoding. Maps only 1.0a, 1.0b and 1.16a to gate patterns (lines 106-110); defers the 1.0a allowlist to "the integration researcher" (line 109), which 03 never covers. Puts capture and decision outputs under `phase-outputs/` (lines 99, 109), not the design's `.dev/tasks/<pkg>/artifacts/`.
- Independent checks run by this reviewer (Bash, read-only): `git log HEAD..origin/master` shows the branch is 20+ commits behind the fork master, including #422 (merged 2026-11-07T14:15:58Z, merge `2327fbd3`) and #434 "add the v1 worker-liveness rules to the worker contract". On `origin/master`, `WORKER-CONTRACT.md:63` is already `WC-14. No turn ends between chain steps` and `:64` is `WC-15`; `tests/skills/test_worker_contract.py:156` and `:165` already hold `"WC-14"` and `"WC-15"` pins; the fan-in rule moved to `:271`; `main.py` last registration is now `issue-watch` at `:565`. `git diff --stat HEAD origin/master` changes 7 of the 11 files the design edits (`WORKER-CONTRACT.md` 148 lines, `test_worker_contract.py` 994 lines).
- `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks} | wc -l` = 168 hits today.
- `.dev/orca-command-refactor/decisions/APPROVED.md` exists (Glob). No research file reads it or states the GQ-10, GQ-35, GQ-61, GQ-63 questions.
- `pipx` is at `/home/coder/.local/bin/pipx`; a global `superclaude` is at `/home/coder/.local/bin/superclaude`.
- `Makefile` uses `rsync --delete` only in the plugin-repo target (lines 81-86), not in `sync-dev`.

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (6 files, Status Complete, Summary present) | PASS | All six have `Status: Complete` (line 5 of each) and a `## Summary` section |
| 2 | Evidence density | PASS (Dense) | Every file cites file:line; spot checks of design 659-686, 864-1013 and inv-005:81 match the citations |
| 3 | Scope coverage against the step table 1.0a to 1.29 | FAIL | Steps 1.0a (as a procedure), 1.0b (decision content), 1.16a, 1.29 and the 1.4 live check have no research; see C1, I1 to I4 |
| 4 | Doc cross-validation tags | PASS | Doc-sourced claims carry Unverified / UNVERIFIED tags (04 sections 2.5, 3.6, 4.5; 02:98; 05:33, 59) |
| 5 | Contradiction resolution | FAIL | 03:15 "Free next ID: WC-14" is false on `origin/master`; 02:157 vs design on test location; 06:99/109 vs design artifact paths |
| 6 | Gap severity | FAIL | One CRITICAL, five IMPORTANT gaps below |
| 7 | Depth (Deep tier: one end-to-end flow) | PASS | 04 traces the Orca bundle `worker-show` to `OrcaObservation` to the classify window rule end to end |
| 8 | Integration point coverage | FAIL | 03 is strong on the branch, but no file checks the fork master the PR must rebase onto (CLAUDE.md pre-PR check 2) |
| 9 | Pattern documentation | PASS | 02 and 05 document registration, lazy `__getattr__`, seams, AST guard, command/skill pins |
| 10 | Incremental writing | PASS | Files show section-by-section growth and in-line cross-researcher hand-offs (03:50, 04:67) |
| L1 | Rollback (design 16) | MINOR gap | Only a line range in 01:21 |
| L2 | Open items (design 17) | FAIL | Items 16 to 19 have no coverage; see I5 |
| L3 | Actionability for a task builder | PASS with exceptions | 03 and 04 are ready to paste; 01 anchors are stale against master (C1) |
| L4 | Test coverage for modified areas | PASS with exceptions | 05 maps every new test file; 1.28 and 1.29 checks are unresolved (I3, I5) |

## Summary

- Checks passed: 8 of 14 (with exceptions noted)
- Checks failed: 6
- Critical issues: 1
- Important issues: 5
- Minor issues: 4
- Issues fixed in-place: 0 (fix_authorization false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| C1 | CRITICAL | 03-integration-points.md IP-1 (line 15) and Summary; 01-file-inventory.md C1, C2, C11; design section 8 | Every anchor was checked on the branch HEAD (`e8db2fe6`, #420), which is 20+ commits behind `origin/master`. On the fork master, WC-14 and WC-15 already exist (`WORKER-CONTRACT.md:63-64`, from #434), with pins at `test_worker_contract.py:156,165`. The design's `### WC-14. Coordinator loop` and the `RULE_PHRASES["WC-14"]` pin would collide with a live rule. The fan-in anchor moved from 156 to 271, `main.py` "after line 561" is now before `issue-watch` (565), and 7 of the 11 edited files changed. CLAUDE.md pre-PR check 2 forces a rebase onto `origin/master`, so the task would be built on false anchors and a taken rule ID. | Re-run the anchor checks of 01 (section C) and 03 (IP-1, IP-2, IP-4) against `origin/master`. Record the WC-14 collision as a design defect for the owner (rename to the next free ID and update design 8, 12 and 16, GQ-11, R7 and every pin). The task file needs an early item that rebases (or re-anchors on master content) before step 1.1, and the R3 fix phase or step 1.0b must carry the new rule-ID decision. |
| I1 | IMPORTANT | No research file; 06:110 only gives an encoding | Step 1.16a was not researched. PR #422 is MERGED (2026-11-07T14:15:58Z, merge `2327fbd3`) but not in this branch, so 06's "not-merged / not-found then HALT" branch does not fit the real case. The "#409 diff check" named in the step table (design line 925) is defined in no research file. #434, which actually took WC-14, is not named by the design at all. | Add research that runs `gh pr view 422 --repo IronbellyOrg/IronClaude --json state,files`, lists the overlap with WC-14, the never-as-worker list and `test_worker_contract.py`, defines the #409 diff check from the SPEC, and covers #434 and #436. Give 1.16a its real branches: merged and in base, merged but not in base (rebase first), open. |
| I2 | IMPORTANT | 06 section 9; research-notes AMBIGUITIES | Step 1.0b: no file states what GQ-10, GQ-35, GQ-61 and GQ-63 ask, their options, or which steps each gates (only GQ-11 to 1.17 is known, design 661, 926). Nobody read `.dev/orca-command-refactor/decisions/APPROVED.md` (exists), which the step requires. 06's own pattern needs "the options verbatim" in each decision file, so the builder cannot write those items. The D9 sign-off gate on step 1.3 (open item 22) depends on the same item. | Add a short research note quoting each GQ question and options from `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/gaps-and-questions.md` and the SPEC, the steps each one gates, the D9 text (design 13), and what `APPROVED.md` already decides. Use the design path `.dev/tasks/<pkg>/artifacts/owner-decisions.md`. |
| I3 | IMPORTANT | 01:344 ("no file edits ... verify"); 06 section 9 | Step 1.29 (manual `superclaude sweep --help` under a pipx install) and the step 1.4 live check (`sweep-live-check-1.4.json`, needs an existing Run) have no research. A global `superclaude` is installed at `/home/coder/.local/bin/superclaude` and pipx exists, so a naive `pipx install` of the branch replaces the user's working install. No file says how to install into an isolated pipx home or suffix, how `/task` encodes a manual step, or how 1.29 closes open item 18. | Research the isolated pipx form (temporary `PIPX_HOME` and `PIPX_BIN_DIR`, or `--suffix`) and how to remove it after, and map both 1.4 and 1.29 to the L1/L3 plus L5 HALT encoding of 06 section 9, with design artifact paths. |
| I4 | IMPORTANT | 06:109 (defers the allowlist), 06:99 and 109 (paths); 03 (no coverage) | Step 1.0a is not researched as a procedure. 06 hands the allowlist to "the integration researcher", and 03 does not cover it. Missing: the forbidden verbs list (no `worker-read`, `gate-list`, `check`, `inbox`, `--include-remote`, `--agent-wait`, `git stash`), the once-before and once-after `worker-show` and `task-list` identity check that stops the build on a difference, the 13 capture items mapped to open items, transcript reading for open item 16, and the sanitization of fixtures copied to `tests/sweep/fixtures/` (design 868-896). 06 also puts the output under `phase-outputs/discovery/`, but the design requires `.dev/tasks/<pkg>/artifacts/readonly-probe.md` (design 876, 958). | Add one research section that turns design 15.1 into a step list with literal commands, the stop rule, the per-item open-item closure, sanitization rules, and the design's artifact paths. Reconcile 06's `phase-outputs/` paths with the design (design paths win). |
| I5 | IMPORTANT | 01:21-22 (line ranges only); 05:148 | Design section 17 is not mapped to the task. Items 16, 17, 18 and 19 have no coverage. Item 19 asks for the byte-limit rationale "recorded in the task package", which is a deliverable with no item source. Item 17 could be closed now (`sync-dev` has no `--delete`; only the plugin target uses `rsync --delete`, Makefile 81-86). Step 1.28 runs the grep over all five dirs with "every hit justified", but 168 hits exist today and 05:148 narrows the grep to the two sweep files without saying this departs from the design. | Add an open-item table (item, closing step, gate, behaviour until closed, task item that records it). For 1.28, record the 168-hit baseline and specify the check as "no new unjustified hit compared with the baseline", or state the narrowing as a deviation for the owner. |
| M1 | MINOR | none | Design section 16 rollback has no research coverage. It is not an executed step, but its rows and check could go into the task's Execution Context. | Optional: summarize section 16 in the build request. |
| M2 | MINOR | 02:157 | Names `tests/cli/sweep/` as the test location, against the design's `tests/sweep/`. 01 and 05 use the design path, and 02:159 flags it as an inference. | Builder uses `tests/sweep/`. |
| M3 | MINOR | 04:67 to 03 | 04 hands the `worker-show` "may write the database" fact (inv-005:81) to researcher 3, and 03 drops it. Design open item 11 and the 1.0a before-and-after check already cover it. | Carry the note into the 1.0a item text. |
| M4 | MINOR | 06:152 | The design names commit points (1.4a "the first code commit", 1.23 "in the same commit as 1.21"), but the repo rule is "commit only when asked". 06 raises this only for the POST reflect diff range. | Builder states how commits are authorized, or replaces "same commit" with "same staged change". |

## Actions Taken

None. fix_authorization is false.

## Recommendations

- Resolve C1 first. It changes the WC rule ID, every contract anchor and the design text, so it should become a fourth design fix (or a 1.0b owner decision) before the task file is built.
- Fill I1 to I5 with one gap-fill researcher pass, scoped to: fork-master anchors, 1.16a, the 1.0b decision content, 1.0a, 1.4 and 1.29 procedures, and the open-item map.
- Keep 03 and 04 as they are; they are the strongest inputs.

## Confidence Gate

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 14 | Grep: 4 | Glob: 1 | Bash: 6
- Unchecked items: none. Unverifiable items: none.
- Scenarios that could still hide issues: I did not read the SPEC (`merged-requirements.md`) or `gaps-and-questions.md` in full, so I did not check whether the GQ items gate more steps than design line 988 says. I did not diff HOW-WE-WORK, `commands.md` or `CHANGELOG.md` line by line on master, only their change counts.

Status: Complete

VERDICT: FAIL

