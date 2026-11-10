# Gate 3 Consolidated Findings — Phase 6, cycle 0

**Report:** `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/RESEARCH-REPORT-pre-push-guard.md` (1425 lines at review time)
**Cycle:** 0 (first Gate 3 review)
**Date:** 2026-11-08
**Inputs:** the seven lens reports in `qa/`. Their abbreviations below:
- TC = `qa-lens-template-conformance.md`: FAIL, 0/3/9
- IC = `qa-lens-internal-consistency.md`: FAIL, 0/2/9
- EQ = `qa-lens-evidence-quality.md`: FAIL, 0/3/9
- AC = `qa-lens-actionability.md`: FAIL, 1/10/6
- DA = `qa-lens-domain-accuracy.md`: FAIL, 0/2/5
- CC = `qa-lens-crossref-chain.md`: FAIL, 0/4/6
- FR = `qa-lens-finding-reproducibility.md`: FAIL, 0/6/5

**Rules applied:**
- Each finding appears once. A merged duplicate lists every lens that raised it, using the lens's own finding number.
- No severity is lowered.
- MINOR findings are notes and do not block.

Checked by the consolidator before writing:
- `seed-brief.md` line 59 reads: "Issue #440 edits `tests/hooks/test_launch_level_guard.py` in another worktree. Keep the L2 tests in new files where possible."
- File 04 has `## E0` (line 9), `### F0` (line 1799), `### F1` (line 1895) and `### F4` (line 2126).
- The report has `[CONTRADICTION` markers or pointers at lines 384, 466, 662, 1140, 1279 and 1331.

## Blocking findings (CRITICAL and IMPORTANT)

| # | Severity | Source lens | Affected section | Finding | Proposed fix |
|---|---|---|---|---|---|
| 1 | CRITICAL | AC1 | §7 (identity variant A-i); §8 steps 1.2 and 2.4 | Step 1.2 writes a machine-specific install-time uv directory into the hook's `PATH`. Step 2.4 treats a hook as owned only if its full bytes equal the installed guard source. The plan's own installs can therefore never match and are reported `foreign-pre-push`. No step says where the uv directory is recorded. | Choose one approach and write it into 1.2, 2.4 and the matching SC rows: (a) the hook bytes stay identical to the packaged source, and the uv directory is read at run time from a named owned file, with a named reason when that file is missing; or (b) ownership means "packaged template with exactly one substituted `PATH=` line", with that line's exact format and the comparison rule. |
| 2 | IMPORTANT | TC1, IC1, EQ1, DA1, CC3, FR1 | §2.5(c) marker at line 384; pointers at 466 (§2.6 row 3), 662 (G-26), 1331 (R9); also §4.5, Phase 2.2, §8.8 | An unresolved `[CONTRADICTION]` remains. The report calls `git rev-parse --path-format=absolute --git-path hooks/pre-push` both [UNVERIFIED] and resolved. EQ1 adds that web-01 D3 ran only from the linked worktree. DA1 re-ran the command on 2.47.3 in a /tmp sandbox and got `<common-dir>/hooks/pre-push` from both the main checkout and a linked worktree, and `<worktree-root>/myhooks/pre-push` with `core.hooksPath=myhooks`. FR1 notes that D3's setup is prose only. | Resolve the marker at line 384. Linked worktree: verified by web-01 D3a-e (cite web-01 lines 193-205). Main checkout: either cite the Gate 3 sandbox re-run (`qa/qa-lens-domain-accuracy.md` finding 1), or re-run it in a fresh `mktemp -d` /tmp sandbox and cite the command and output; if neither, tag that one case [UNVERIFIED]. Give D3's setup (mktemp sandbox, `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`, init, worktree `wt`, `git config core.hooksPath myhooks`). Delete the marker text, remove the "see the [CONTRADICTION]" pointers at 466, 662 and 1331, and make §2.6 row 3, G-26, §4.5, Phase 2.2, §8.8 and R9 state the same status. |
| 3 | IMPORTANT | TC2, IC2, EQ2, AC5, DA2, CC4, FR5 | §8.6 Phase 6.7; marker at line 1140; §9 rows 7, 8, 29 (pointer at 1279) | An unresolved `[CONTRADICTION]` remains on where the L1 regression tests go. Phase 6.7 names `tests/hooks/test_launch_level_guard_with_identity.py`; rows 7, 8 and 29 name `tests/hooks/test_launch_level_guard.py`. Both files exist. EQ2 and CC4 note that `test_launch_level_guard.py` is the main L1 suite. AC5 notes that seed brief line 59 says issue #440 edits that file in another worktree and that L2 tests should go in new files where possible. The sentence "no other L1 test file was listed" is false. | Resolve with the seed-brief constraint. New L2 tests and new L1 bypass-regression cases go in a new test file named in Phase 6.7 (for example `tests/hooks/test_launch_pre_push_guard.py`, plus one named file for the L1 cases). Explain that `test_launch_level_guard.py` is the main L1 suite but is being edited by #440 (cite seed-brief line 59), and that `..._with_identity.py` covers L1 with identity. Use the same file names in Phase 6.7 and rows 7, 8 and 29, including the row 29 `uv run pytest` command. Delete the marker at 1140, its pointer at 1279, and the false sentence. |
| 4 | IMPORTANT | TC3 | §8.1-8.7 | No phase has the template's **Goal:** or **Dependencies:** line, so dependencies between phases are implicit. | Add a **Goal:** line and a **Dependencies:** line under each phase header 8.1-8.7. |
| 5 | IMPORTANT | EQ3 | §6 Option table "Cons" row (line 920) | Cited path does not exist: `.dev/brainstorms/20261105-170229-launch-level-hook/refactor-plan.md:1158`. | Change it to `.dev/brainstorms/20261105-170229-launch-level-hook/adversarial/adversarial/refactor-plan.md:1158`. |
| 6 | IMPORTANT | AC2 | §8 step 2.1 (publisher) | The step does not name the file the publisher reads the guard bytes from at run time, or the `l2_status` reason when that file is missing. | Name the source file (for example the installed `~/.claude/hooks/...` copy written by `_copy_scripts`) and add a reason value for "guard source missing". |
| 7 | IMPORTANT | AC3 | §8 steps 2.7 and 3.2 | Step 2.7 (register in `_FRESHNESS_SCRIPTS`, `install_hooks.py` 42-94) is marked conditional. The `Makefile` "Installer Registration" check (lines 307-319) flags any unregistered `src/superclaude/hooks/scripts/*.sh`, so step 3.2 (`make verify-sync`) fails without it. | Make 2.7 unconditional when the guard lives in `hooks/scripts/`, and order it right after 1.1. Otherwise, name the other location in 1.1. |
| 8 | IMPORTANT | AC4 | §7 / §8 Phase 2 (keep-don't-replace, full-byte ownership) | No upgrade path exists. A hook from an older packaged version stops matching byte for byte, is reported foreign, and is never replaced. | Add a step with a version marker and an upgrade rule: a hook that matches a known earlier owned version (by stored hash) is replaced through the same no-replace publication path. Say where the earlier versions or hashes are kept. |
| 9 | IMPORTANT | AC6 | §8 step 4.2 (`l2_status`) | The step gives no new return type and lists none of the consumers that must change. | Give the signature or closed value set, and add one sub-step for each consumer AC6 lists: `session_report` (ow:1065), `cmd_launch` `l2_notes` (ow:1312), `sc-issue-protocol/refs/claim.md:120`, `commands/issue.md`, `sc-issue-protocol/SKILL.md`, `docs/user-guide/commands.md`, both design docs, and the test assertions in `tests/skills/test_issue_orca_worktree.py` (1672, 1691-1692) and `tests/skills/test_issue_protocol.py`. Verify each path with Grep before citing it. |
| 10 | IMPORTANT | AC7 | §8 step 1.9 | The step reuses `GUARD_VERSION_LINE` (ow:804, `"# launch-level-guard-version: 1"`), which is the L1 guard's version and is checked by `enforcement_preflight` (950-951). That ties the L1 and L2 versions together. | Define a separate L2 version constant with its own header text, and name the function that checks it. |
| 11 | IMPORTANT | AC8 | §3.5 success criteria SC-1 to SC-23 | These planned behaviours have no pass/fail criterion: the Phase 5 L1 refusal tokens (`.git/hooks` tamper, `--config-env`, `GIT_CONFIG_*`, `GIT_CONFIG_PARAMETERS`, `-c hook.pre-push.*`), both states of the IR-7 switch, the `hookspath-set` reason, and the recheck before each launch. SC-18 does not give exact reason strings. | Add SC rows, each with a command, an input and the exact expected output or exit code. List the exact reason strings in SC-18. |
| 12 | IMPORTANT | AC9 | §8 step tables (all phases) | There is no "done when" or expected-outcome column. Step 6.6 leaves two options open, 7.4 gives no replacement text, and 3.1, 3.2, 5.3 and 5.5 have no observable done condition. | Add a "Done when" column with an observable result for each step. Choose the 6.6 option, and give the 7.4 replacement doc text. |
| 13 | IMPORTANT | AC10 | §8 step 4.4; G-17 (line 653); R3 (line 1325) | The default (off) is decided, but no switch mechanism is proposed, so step 4.4 cannot start. | Propose a concrete mechanism that keeps the decided default, labelled a proposal (for example a module constant in `orca_worktree.py` guarding the commented refusal at 1309-1310), and name the test that turns it on. |
| 14 | IMPORTANT | AC11 | §7 bypass table (line 1025) vs §8 steps 5.4 and 6.7 | No step fixes the escaped `$'core.hooks\x50ath'` spelling passed through `-c`, yet 6.7 asks for tests of those evasions. | Add a 5.4 sub-step: decode `$'...'` ANSI-C quoting before the token match, or refuse `-c` values that contain `$'`. Make 6.7 test both spellings. If this is left as an accepted limit, say so in §7 and §9 and drop it from 6.7. |
| 15 | IMPORTANT | CC1 | §2.1 (lines 136, 145) → §4 → §8.5 | Unlisted wrappers before `git` (`chrt`, `taskset`, `find -exec`, `uv run`; wrapper list at guard line 549) are an L1 bypass that appears in no gap, step or open question. G-13 and L1-5 cover only the underscore prefix, and Phase 5.3 leaves line 549 alone. | Widen G-13 and L1-5, or add an L1 gap for the wrapper list at line 549. Extend Phase 5.3 to it, add a wrapper case to 6.7, and add the form to the §7 bypass table and §9 row 8. |
| 16 | IMPORTANT | CC2 | §2.3 (line 284) → §4 / §8.4 / §8.6 | When a ccsession warning is also present, `W-L2-ABSENT` appears only in `detail` (`launch_result` 1203-1220; pinned at `tests/skills/test_issue_orca_worktree.py:1554`). With the refusal off by default, this masks the only L2 signal. No gap or step covers it. | Add a gap for the masking. In 8.8/8.9, map it to a Phase 4.3 sub-step that decides visibility, plus a 6.11 test case with both warnings present, or record it as an accepted limit in a new §9 row. |
| 17 | IMPORTANT | FR2 | T-4 (line 489); §6.5 note (line 980); Phase 1.5 (line 1078); DOC-8 / BP-14 / Phase 7.1 | The six-field-record finding drives the `rsplit(" ", 3)` design, but web-01 G5 gives its setup only in prose (no hook body, repository commands or push command). | Re-run G5 in a fresh `mktemp -d` /tmp sandbox with a local bare remote and isolated config. Write the exact commands, hook body and output into the report (or an appendix) and cite them. If it cannot be reproduced, say so and lower the evidence level. |
| 18 | IMPORTANT | FR3 | T-4 (line 489); §6.5 note (line 980); Phase 1.5 (line 1078) | "A naive four-variable `read` lets the protected push through" is stated as observed, but the source only infers it. | Reword all three places as an inference ("would see `ago}` as field 3; inferred, not executed"), or add an executed sandbox experiment showing the push exit status and the remote ref before and after. |
| 19 | IMPORTANT | FR4 | W2-15 (line 797); §5.5 (line 869); §6.1 Pros (line 919); §6.4 (line 961); §7 (line 1015); Phase 2.1 (line 1088) | "Proven end to end on git 2.47.3" rests on web-02 Area 3, whose `exp.py` driver was not kept. The printed output shows no remote-ref listing, so "remote ref unchanged" is asserted, not shown. | Weaken the claim in all six places to "publish_exec verified; push refusal observed by exit code only". Alternatively, re-run in a fresh /tmp sandbox with the commands and a before/after `for-each-ref` of the bare remote, and cite them. |
| 20 | IMPORTANT | FR6 | §2.5 source note (line 314) | The setup note omits the isolation (`HOME=$S/home`, `GIT_CONFIG_NOSYSTEM=1`, 04 E0) and the ambient variables disclosed at 04 line 13 (`GIT_CONFIG_COUNT=2`, `CLAUDECODE`, `CCSESSION_LAUNCH_ID`). 04 E0 runs `chmod +x` on `x.sh` and `hook-logging.sh` before showing how they are created. | Add the setup and ambient-variable sentence to line 314. In the report, note where `x.sh` and `hook-logging.sh` are defined (04 lines 84-147), so a reader following E0 is not stuck. |

Blocking count: 20

## Notes (MINOR, non-blocking)

| # | Severity | Source lens | Affected section | Finding | Proposed fix |
|---|---|---|---|---|---|
| N1 | MINOR | TC4 | ToC | Sub-entries are paraphrased, have no anchors, and are incomplete. | Regenerate from the real headers. |
| N2 | MINOR | TC5 | §10.1 | Agent Type column is missing. | Add it. |
| N3 | MINOR | TC6, EQ12 | §10.4 / §10.5 (line 1416) | QA list is deferred to the Task Log, and `reflect/post/` does not exist yet. | List the `qa/` files by name, and mark `reflect/post/` as created later. |
| N4 | MINOR | TC7 | §5.1, §5.2 | Relevance and relationship values are outside the template vocabulary. | Normalise them, and move qualifiers to notes. |
| N5 | MINOR | TC8 | §6 | Option labels, Effort scale and comparison rows differ from the template, and 6.4/6.5 come before the comparison. | Align with the template. |
| N6 | MINOR | TC9 | §7 | **Recommended approach:** and **Rationale:** labels are absent. | Rename. |
| N7 | MINOR | TC10 | §4.1 | "—" placeholder cells. | Write the actual state or "n/a (resolved)". |
| N8 | MINOR | TC11 | Header (lines 25-27) | Non-template Source key and Tags paragraphs. | Keep (note only). |
| N9 | MINOR | TC12 | §10 (line 1382) | The OQ-1 to OQ-20 to §9 mapping is not shown. | Add the mapping, or drop the claim. |
| N10 | MINOR | IC3, EQ8 | §2, §3.3, §8 Phases 1.1, 1.3, 2.1, 2.4-2.6 | 01 section pointers are wrong. | publish(), ownership and self-test → 01 §6; copies and installed path → 01 §8; PID-namespace caveat → its actual section. |
| N11 | MINOR | IC4 | G-27 vs §8.8 / row 24 | Open vs Partly resolved. | Align. |
| N12 | MINOR | IC5 | §7 vs G-6 | The quote is inexact, and the decision owner varies. | Quote exactly, and name one owner. |
| N13 | MINOR | IC6 | §6 diagram vs W2-5 | `path.c` 402-403 vs 402-405. | Use one range. |
| N14 | MINOR | IC7 | §5.4 R6 row | The config.worktree hooksPath test is mapped to SCs that do not cover it. | Add an SC or remap. |
| N15 | MINOR | IC8, EQ9 | §10.1 (line 1343), §9.4 (line 1362) | File 04 range given as "E1-E31, F1-F3"; actual is E0-E31 and F0-F4. "15 of 17" refers to 04 line 2281, not the 8-row §2.5 table. | Correct the range, and name the source table of the count. |
| N16 | MINOR | IC9 | G-43 vs §9 row 33 | The two D19 "no code" lists differ. | Use one list. |
| N17 | MINOR | IC10 | §4.1, §8.9 | Severity differs across gap families. | State which family governs. |
| N18 | MINOR | IC11, EQ10 | §2.5(a), T-1, SC-1; L-6, W2-9, Phase 2.1, 6.4 | E2 is missing from the table; ENOTSUP vs EOPNOTSUPP. | Add E2; use "EOPNOTSUPP (errno 95; Python's ENOTSUP)". |
| N19 | MINOR | EQ4, FR7 | T-6, SC-12, G-42, Phases 1.7 and 6.2, row 32 | The 3001-branch result is cited only as "QA sandbox"; 3000 vs 3001 wording. | Cite `qa/qa-research-qualitative-report.md` F8 and Self-Audit b1 (lines 53, 73), and use one wording. |
| N20 | MINOR | EQ5 | Tag key (line 27); §3.6 D19 rows; §7.4 | Sandbox observations are tagged [CODE-VERIFIED]. | Re-tag them [OBSERVED 2.47.3]. |
| N21 | MINOR | EQ6 | T-4, T-6, L-6 | Tags not in the key. | Use the defined tags. |
| N22 | MINOR | EQ7 | §3.6 D19 rows 12, 15, 19, 36, 37/39, 66, 67, 81; line 625 | [CODE-VERIFIED] with no file:line. | Copy the file:line from file 03. |
| N23 | MINOR | EQ11 | §10 (line 1359) | `released` is listed as a verdict. | Say "ordinary (with an optional `released` reason)". |
| N24 | MINOR | AC12 | Step 1.3 | Timeout value and mechanism are not given. | Give them. |
| N25 | MINOR | AC13 | SC-12, SC-13 | No way given to observe the stdin drain. | Name the method. |
| N26 | MINOR | AC14 | SC-23 | Conditional on A-i, although A-i is recommended. | Make it unconditional or tie it to its §9 row. |
| N27 | MINOR | AC15 | Steps 2.6, 6.1, 6.3 | Test fixtures are not named. | Name `LocalPushFixture` (`tests/hooks/test_launch_job_identity.py` ~1175) and the governed-session fixtures. |
| N28 | MINOR | AC16 | Step 6.4 | `test_ir6_l2_status_follows_the_git_hook_path` is at line 1696. | Correct the line. |
| N29 | MINOR | AC17 | Step 2.3 | `git config --get core.hooksPath` has no `-C <wt>`. | Add `-C <wt>`. |
| N30 | MINOR | DA3 | §9 row 27 | Row 27 says "by process ancestry"; the shipped selector uses the kernel session id. | Reword. |
| N31 | MINOR | DA4 | §2.4 (line 298), G-20 | `install_hooks.py` has 611 lines, not 612. | Correct. |
| N32 | MINOR | DA5 | §2.2 (line 191) | The publish call is at line 305. | Cite 301-305. |
| N33 | MINOR | DA6, FR11 | §9 row 1, §9.4 (line 1347) | 04 line 1530 now holds the corrected text; 04 also has wrong internal pointers at 1530 and 1699. | Say "pre-Gate-1 text", and record the 04 errata in §9.4. |
| N34 | MINOR | DA7 | §9 (line 1316) | "ext4" is not evidenced; `stat -f` reports ext2/ext3. | Say "ext-family". |
| N35 | MINOR | CC5 | §6-§8 vs §5 | No shared W1/W2 IDs with the web-01 letter IDs. | Add a crosswalk column or cite both. |
| N36 | MINOR | CC6 | §7 vs §6.6 | The A-i reason and the bypass-owner table do not trace to the 6.6 comparison. | Label their source (6.5, S4 gaps). |
| N37 | MINOR | CC7 | §8.8 Where column | The S9 row is omitted for G-12, 13, 14, 16, 19, 20, 37, 39, 41, 42, and R13/R14 for G-22/23. | Add them. |
| N38 | MINOR | CC8 | §9 intro (line 1267) | The claim that each row names its G-n is false for rows 20, 21, 34-40. | Add the IDs, or narrow the sentence. |
| N39 | MINOR | CC9 | §2.6 mapping (lines 457-472) | The mapping is incomplete and inaccurate. | Item 9 → rows 13, 14, 16 and R7; item 2 → rows 24, 34, 40 and R6; reword the intro. |
| N40 | MINOR | CC10 | §3.6 vs §9 row 33 | D19-82 is classed two ways. | Move it to the observed "no code" group. |
| N41 | MINOR | FR8 | §2.2 (line 155) | Identity experiments are cited with wildcards; the hook body is not shown. | Cite 01 §7 lines 138-168. |
| N42 | MINOR | FR9 | §2.3 | The `l2_status` probe script is not shown. | Add the invocation, or note that it is absent. |
| N43 | MINOR | FR10 | §8 diagram (lines 1064-1067) | The stdin-parse step and the "exit → abort → ref unchanged" step are missing. | Extend the diagram. |

Total: 1 CRITICAL, 19 IMPORTANT, 43 MINOR notes. This is 62 consolidated findings, down from 83 raw lens findings after merging duplicates.
