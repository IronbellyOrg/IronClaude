# QA Report - Task Integrity (lens: phase-structure)

**Topic:** GitHub issue watcher task file (TASK-RF-issue-watcher-20261107-150955), template 02
**Date:** 2026-11-08
**Phase:** task-integrity (QA_MODE task-integrity, LENS phase-structure)
**Fix cycle:** N/A (first review; fix_authorization: false, report only)
**Task file:** `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md` (925 lines)
**Authority:** `research/06-gap-fill-decisions.md` (Section 2 phase plan, Tables 1.2 and 1.6)

Report is appended incrementally. Verdict at the end.

---

## Scope of reading

All 925 lines of the task file were read (paged Reads), plus research/06 Tables 1.2 and 1.6, Section 2 and rows DF-07, DF-08, DF-56; BUILD-REQUEST.md; template 02 (frontmatter, Part 2 skeleton, I15); task-builder SKILL.md rule 15 and the POST-reflect placement lines; and the cited repository anchors (spot-checked with a batch script and Grep).

## Items Reviewed (the 18 lens checks)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete and well-formed | PASS | Parsed with PyYAML (`uv run --offline --no-sync python -I`): id, title, status, created, type, template, tracks, spec_path, qa_intensity=standard, reflect_post_mode=skill all non-empty; `reflect_pre` is a dict with the 7 template keys; `start_commit` and `executor_model_class` are absent from the YAML (they appear only in prose at lines 150, 762, 923). No CR characters. |
| 2 | Mandatory template sections | PASS | Task Overview (68), Key Objectives (74), Prerequisites & Dependencies (85), Execution Context with References / Source Areas / Key Constraints / Handoff / Frontmatter protocol (104-150), Detailed Task Instructions (152), Task Log (778) with Task Summary, Open Questions, Execution Log, per-phase Findings, Phase Gate Findings, Follow-Up Items, Deviations from Process, Reflect Depth Derivation. No separate Post-Completion section (anti-orphaning respected). |
| 3 | Phase dependencies and module build order | PASS | P1 setup; P2 runner, predicates, audit; P3 github; P4 record; P5 launch; P6 cycle; P7 cli + main.py; P8 cross-cutting tests; P9 runbook + final gates; P10 commit + POST. Identical to research/06 Section 2 and research/05 build order. DF-56 conftest split verified: part 1 (2.4) imports only `runner`; part 2 (4.2) after `record`; part 3 (5.3) after `launch`; part 4 (6.4) after `cycle`/`github`; part 5 (8.1) stubs. The 13 fixtures: 11 created in P3 after `github.py` (3.1 precedes 3.2-3.5), 2 in P5 after `launch.py` (5.1 precedes 5.2). |
| 4 | Research before build before test | PASS | Research complete (Prerequisites, line 90); each phase builds the module before its tests; the cross-cutting tests (P8) come after all modules (P2-P7). |
| 5 | Task-completion items in the final phase | PASS | 10.1 validation, 10.5 summary, 10.6 POST reflect, 10.7 Done, 10.8 staging all inside Phase 10 (lines 736-776). |
| 6 | Task Log present | PASS | Lines 778-923. |
| 7 | Item count | PASS | `grep -c '^- \[ \]'` = 176 and `^\*\*Step` = 176. Per phase: P1 8, P2 11, P3 11+12 gate, P4 7, P5 11+12 gate, P6 11, P7 9+12 gate, P8 12+12 gate, P9 19+13 final+8 M4, P10 8 (sum 176). Matches the Reflect Depth Derivation (line 923) and the BUILD-REQUEST expectation of about 160. |
| 8 | Open Questions and remaining gaps; 29 DEVIATION rows | PASS | OQ-1..OQ-29 map 1:1 to the 29 `**yes**` rows of research/06 (extracted by script: DF-01,02,03,04,05,06,07,09,10,12,13,15,17,18,20,22,24,25,27,28,29,42,43,44,48,50,55,57,60); the same 29 ids appear in both M4 prompts (lines 713, 716, 719) and in Step 9.18. Q1-Q4, the DF-08 tension, implementation readings (OQ-36..41a), remaining gaps (OQ-42..46) and staleness corrections are present. |
| 9 | QA gates M3 / I19 / I20 / I22; 4x6 + 7 + 3 = 34 | PASS (with notes) | Grep of the gate spawn items: Gate A lines 270-285 (6), Gate B 376-391 (6), Gate C 488-503 (6), Gate D 570-585 (6), Final 673-691 (6 lens + 1 domain lens = 7), M4 713-719 (3) = 34. Each gate has aggregate, agents, consolidate, ONE fix agent (`fix_authorization: true`), 2 report-only verifiers, verdict with regression-then-monotonicity halt text and a 2-cycle cap. See M-9, M-10 for placement and post-fix notes. |
| 10 | TB-Add-1 placeholders | PASS | `grep -nE 'TBD|TODO|FIXME'` = no match; every item has context, action, output, verification and completion-gate text. |
| 11 | TB-Add-3 blocked items reference their OQ by index | FAIL | `grep OQ-` finds OQ ids only in lines 802-864; no item Context cites one (line 923 admits it). Steps 10.2-10.4 depend on the inferred commit authority OQ-7/OQ-35. See I-3. |
| 12 | TB-Add-4 dependencies form a DAG | PASS | All item-to-item references point backwards (3.G9 reads the 3.G8 output; 3.G12 re-performs 3.G8-3.G11 "in this same item"; 8.2 uses 8.1; the forward mentions in 1.3 -> 10.2 and 7.1 -> 7.2 are statements, not inputs). No cycle found. |
| 13 | TB-Add-5 granularity | PASS (with note) | Phase 6 and 7 prefaces justify splitting `cycle.py` (3 items) and `cli.py` (2 items); the build request mandates one item per source file. See M-13 for `run_cycle` (Step 6.2). |
| 14 | TB-Add-6 uniform verification format | PASS (with note) | Every item uses the same "ensuring ..." clause and the same two closing sentences; no item uses a `Verify:` prefix, so the format is uniform though not the literal `Verify:` form. No task-level Acceptance Criteria list exists. |
| 15 | TB-Add-7 Source Areas reappear; no file:line in block | PASS | Source Areas (lines 113-120): package, `main.py`, `tests/issue_watch` + `tests/conftest.py`, runbook, `atomic`/`write_prepared_bytes` (4.1), `_ORCA_CLIS`/`_find_orca` (5.1, 5.6), `origin_repo.py` (5.1, 5.7), `claim.md`/`claim-comment.md` (5.8), pyproject/Makefile/test.yml/.pre-commit (1.5, 9.1, 9.9). Regex `[A-Za-z_/.]+\.(py|md|toml|yml):[0-9]+` over lines 104-126 = 0 matches. The optional `src/|/.*:[0-9]+` spot check hits one line (108, the verbatim GOAL, paths without line numbers) - tolerated. |
| 16 | TB-Add-8 evidence binding | PASS | 53 `evidence-absence` comments cover all 53 file-creating or appending items (1.6, 1.7, 2.1-2.8, 3.1-3.7, 4.1-4.5, 5.1-5.8, 6.1-6.9, 7.1, 7.2, 7.4, 7.5, 8.1-8.8, 9.1, 9.2); items on existing code carry file:line. A batch check of about 40 cited anchors (test.yml:22/29/47, pyproject:16/114/135/174-184, Makefile:109/166/356-358, main.py:559-565, atomic.py:14/33, install_user_setup.py:35/198-221, origin_repo.py:65-99, claim.md:29, claim-comment.md:23, the test precedents, design lines 11/95/218/224/751/759/761/765/766/868/898/233-242) found them accurate. |
| 17 | POST reflect (skill) penultimate, Done last, in final phase | PASS (with note) | 10.6 POST reflect is immediately before 10.7 Done (matches SKILL.md line 2310), both in P10. A NON-BLOCKING staging item 10.8 follows Done (allowed by SKILL.md rule 15 and DF-07 item 6), so the prose "penultimate item" and "Done item last" is loose. See M-5. |
| 18 | Gate commands match research/06 Table 1.2; D1/D2/D3 | FAIL (one blocking contradiction) | G-1..G-11 compared with Table 1.2 (G-2 file list, G-3 `--offline --with "pytest-xdist>=3.5,<4"`, G-5 pinned `ruff@0.15.20` plus the full-tree format check at P9, G-6 order verify-deps / sync-dev / verify-sync, G-7 pattern, G-10 three commands, G-11 greps): textually equal. Per-phase commands match Section 2 except P7 has no G-1 item (M-7). No item contradicts D1 (workspace poller; cron is FU-2), D2 (claim-only prompt) or D3 (`type(n) is int`, 1..999999999). Blocking: the "no SKIP" rule of G-1/G-3 cannot be met because Step 5.8 prescribes skips (I-1). |

## Issues Found

Blocking = IMPORTANT (wrong behaviour, false claim, unsatisfiable gate, missing required safeguard). Minor = notes, never re-checked.

### Blocking

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | IMPORTANT | Step 5.8 (line 357) versus Steps 8.2 (530), 8.9 (551), 8.10 (553-554), 9.4 (618), 9.6 (623-624) and the "any skipped or xfailed test is a finding" sentence in the gate-command lens prompts at lines 270, 376, 488, 570, 673 | Step 5.8 tells the executor to skip the `.claude/skills/sc-issue-protocol/` and `~/.claude/skills/sc-issue-protocol/` parametrizations "when the folders are absent, which is normal in CI and in this checkout". Verified on this checkout: `.claude/skills/sc-issue-protocol` does not exist (`ls` error) so at least one SKIPPED result is guaranteed. Table 1.2 row G-3 and Steps 8.10 and 9.6 require "zero skipped tests" (and 8.9 and 9.4 "no SKIP"); Step 8.2 calls its own filesystem skip "the only skip"; every Gate B, C, D and Final lens prompt classes a skipped test as a finding. The executor therefore cannot satisfy G-3 or the QA gates, and the gate record (Step 9.19) would either be false or the task would HALT on its own design. `make sync-dev` (Step 9.10) only creates the `.claude/` copy AFTER the G-3 runs of 8.10 and 9.6. | In Step 5.8 remove all skipping: replace the two conditional parametrizations with ONE non-parametrized test that loops over the copies that exist (`.claude/skills/sc-issue-protocol/` and `~/.claude/skills/sc-issue-protocol/`) and asserts the marker in each, passing vacuously when a folder is absent; keep the two tracked `src/` copies as required assertions. Delete the words "skip those two parametrizations" and state "no `pytest.skip`, `skipif` or `xfail` anywhere in `tests/issue_watch/` except the single filesystem skip of Step 8.2". Also change Step 8.2 so its "only skip" claim stays true. (Alternative, weaker: keep the skips and add the named exemption to G-3, Steps 8.9/8.10/9.4/9.6 and the five lens prompts.) |
| I-2 | IMPORTANT | Steps 9.17 (line 657) and 9.18 (line 660), ordered after the full gate run 9.4-9.16 and before 9.19 | Both items fix a GAP "in the right file" (9.17 may add a missing test, 9.18 may edit any file) and say only "re-running Step 9.4" (G-1) afterwards. Research/06 DF-08 and the P9 checkpoint say a fix made after a gate passed is re-checked with G-4 and G-5; the same-phase G-3 xdist run (9.6, no SKIP), G-5 format check (9.8), G-7/G-8 greps (9.12, 9.13), G-11 hygiene (9.16) and, for a runbook edit, the runbook check (9.3) and G-2 (9.5) are not re-run. Step 9.19 then writes `final-gate-record.md` with every row "PASS" copied from result files that predate the fix, and the Final gate lens agents are told to compare against those records. A new or edited test file would never have been seen by G-3, G-5, G-7 or G-11. | In both items replace "re-running Step 9.4" with: "re-running Steps 9.4, 9.6, 9.7, 9.8, 9.12, 9.13 and 9.16 (G-1, G-3, G-4, G-5, G-7, G-8, G-11) and, when `docs/designs/issue-watcher-setup.md` changed, Steps 9.3 and 9.5, and overwriting the corresponding `p9-*` result files before Step 9.19 is written". (Alternative: move 9.17 and 9.18 ahead of Step 9.4.) |
| I-3 | IMPORTANT | Steps 10.2, 10.3, 10.4 (lines 746, 749, 752); also Step 6.2 (OQ-36, OQ-39), 2.2 (OQ-37, OQ-38), 5.1 (OQ-40) | TB-Add-3. The Open Questions record that the checkpoint-commit authority is "inferred, to be confirmed by the owner" (OQ-7, OQ-35) and that "Steps 10.2 to 10.4 are the only items to remove" if the owner objects, yet none of the three commit items cites OQ-7 or OQ-35, and Step 10.7's Done condition ("no unresolved blocking item") cannot tell the executor whether OQ-7 counts. The task itself admits the gap (line 923: "no item Context cites an OQ id"). The executor commits to the branch without being told that the authority is unconfirmed or what to do about it. The implementation readings OQ-36 to OQ-40 are likewise implemented in items that never name them. | Add to the Context of 10.2, 10.3 and 10.4: "Depends on OQ-7 and OQ-35 (checkpoint-commit authority is inferred from the coordinator brief): proceed with the commit unless the owner has withdrawn it in this session; if withdrawn, skip 10.2-10.4 and run 10.6 with a base the owner names." In Step 10.7 add: "OQ-7/OQ-35 are not blocking unless the owner withdrew the commit". Add "(OQ-36, OQ-39)" to 6.2, "(OQ-37, OQ-38)" to 2.2 and "(OQ-40)" to 5.1 so the reading is traceable. |

### Minor (notes, not re-checked)

| # | Severity | Location | Issue | Suggested Fix |
|---|----------|----------|-------|---------------|
| M-5 | MINOR | Task Overview (line 72), Key Objective 6 (line 83), Step 10.6 title, BUILD-REQUEST line 32 | Prose says the POST reflect is "the penultimate item" and the Done item "last", but 10.8 (NON-BLOCKING staging) follows Done and reflect is third from last. Allowed by SKILL.md rule 15 and DF-07 item (6), so only the wording is off. | Say "immediately before the Done item" and "the last blocking item". |
| M-6 | MINOR | Step 9.F1 (line 670) and Step 10.5 (line 755) | Count slips: 9.F1 calls `gate-[abcd]-verdict.md` "the five verdict files" (the glob matches four; the Final and M4 verdicts do not exist yet) and 10.5 lists "the five gate verdicts" although the task has six gates (A, B, C, D, Final, M4). | Replace "five" with "four" in 9.F1 and "six" in 10.5. |
| M-7 | MINOR | Phase 7 (lines 447-478) versus research/06 Section 2 row P7 | Section 2 lists G-1 among the P7 commands and says every phase ends with G-1; Phase 7 has G-9, G-2, G-4, G-5 but no G-1 item (G-2 contains `tests/issue_watch/`, so coverage exists, but there is no `p7-g1-*` record). | Add one sentence to 7.7: "this run includes the G-1 selection and serves as the P7 G-1 record". |
| M-8 | MINOR | Phase 8 intro (line 524) | Phases 4, 6 and 9 begin with "Before Step N.1 read gate-X-verdict.md; if it does not say PASS, stop"; Phase 8 has no such check (its predecessor gate is Gate C). Resume after a session rollover loses the guard. | Add "Before Step 8.1 read `phase-outputs/plans/gate-c-verdict.md`; if it does not say PASS, log the blocker in the Phase 8 Findings section and stop." |
| M-9 | MINOR | Gate A / C placement (lines 262, 480) and OQ-34 | Gates cover two phases, so P3 consumes P2 modules (`github` imports `runner`, `predicates`) and P7 consumes P6 (`cli` imports `cycle`) before the covering gate runs; the gate texts say "placed after Phase N per template I15", which I15 (line 636: a gate between a phase and any dependent phase) does not literally support. The placement follows the approved DF-08 and BUILD-REQUEST, but OQ-34 records only the sizing tension. | Add one sentence to OQ-34 recording the placement choice (per-phase G-1 and G-5 mitigate it; fix agents may edit Phases 2-7). |
| M-10 | MINOR | Steps 3.G12, 5.G12, 8.G12 versus 7.G12, 9.F13, 9.M8 | Post-fix re-runs of Gates A, B and D omit `make lint` (G-4); Gates C, Final and M4 include it. DF-08 says G-4 and G-5. The next phase's `make lint` (Steps 5.10, 7.8, 9.7) catches the gap. | Add `make lint` to the post-fix list of 3.G12, 5.G12 and 8.G12. |
| M-11 | MINOR | Step 1.3 (line 167) versus DF-07 item (1) | DF-07 says the origin/master SHA and merge-base are "written to the Task Log"; Step 1.3 writes only `discovery/git-baseline.md`. | Add "and append one line to the Phase 1 Findings section". |
| M-12 | MINOR | Step 6.3 (line 421) | "the first name of `_ORCA_CLIS` that `which` resolves" does not say where `_ORCA_CLIS` comes from; Step 6.1 forbids imports from `superclaude` other than the listed package modules and Step 8.8 will flag a direct import from `install_user_setup` in `cycle`. | Say "via `launch._ORCA_CLIS` (Step 5.6 pins identity with the original)". |
| M-13 | MINOR | Steps 2.2, 2.3, 3.1, 4.1, 5.1, 6.2, 7.1 | TB-Add-5/atomicity. Each is a single item with 600-1,800 words of embedded spec and several functions. Phases 6 and 7 justify splitting `cycle.py` and `cli.py`, and the build request requires one item per file, but `run_cycle` (15 steps, Step 6.2) carries no single-item justification. | Either split 6.2 into "steps 1-9" and "steps 10-15" items, or add to the Phase 6 preface: "run_cycle is one item because its 15 steps share local state; write it helper by helper". |
| M-14 | MINOR | Items 2.10, 3.8, 4.6, 5.9, 6.10, 8.9 versus 1.8 | "fix ... and re-run until PASSED" has no bound, whereas Step 1.8 says "re-run once". | Cap at two fix attempts, then log the blocker. |
| M-15 | MINOR | TB-Add-6 (all items) | No `Verify:` prefix and no Acceptance Criteria list; uniform "ensuring" wording instead. | None required; note only. |
| M-16 | MINOR | Steps 9.4 and 9.5 | `tests/issue_watch/` runs twice on an unchanged tree (G-2 contains G-1). Required by Table 1.2, so justified. | None. |
| M-17 | MINOR | Execution Context spot check | `grep -E "src/|/.*:[0-9]+"` over lines 104-126 hits line 108 (the verbatim GOAL), which names `src/superclaude/cli/issue_watch/` and `main.py` without line numbers. The BUILD-REQUEST mandates the verbatim GOAL, so tolerated. | None. |

## Actions Taken

None (fix_authorization: false). The only file written is this report.

## Summary

- Lens checks: 16 of 18 PASS (checks 9, 13, 14 and 17 carry minor notes), 2 FAIL (check 11 TB-Add-3 via I-3; check 18 gate commands / no-SKIP via I-1). Issue I-2 is a phase-ordering defect found under checks 3 and 18.
- Blocking issues: 3 (all IMPORTANT): I-1, I-2, I-3. No CRITICAL.
- Minor notes: 13 (M-5 to M-17).
- Confidence: Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (the verdict above is limited by the 3 blocking findings, not by coverage).
- Tool engagement: Read: 27 | Grep: 14 | Glob: 1 | Bash: 7 (one Bash call used a generated `/tmp/ironclaude-batch.*` script, removed afterwards; PyYAML parse of the frontmatter; item counts per phase; research/06 DEVIATION extraction). No web research, so no Tavily or fallback calls.
- Self-audit: findings can be traced to cited line numbers and to commands run (ls of `.claude/skills/sc-issue-protocol`, grep of `OQ-`, grep of the gate spawn items, per-range `^- \[ \]` counts). The gate-agent total 34 and the 29 DEVIATION ids were recomputed, not copied.

## Recommendations

1. Fix I-1 first (rewrite Step 5.8 without skips); it makes G-1/G-3 and four QA gates unsatisfiable on the executor's host.
2. Fix I-2 (extend the re-run list in 9.17 and 9.18) so the final gate record cannot be stale.
3. Fix I-3 (OQ-7/OQ-35 cross-references in 10.2-10.4, 10.7).
4. Optionally fold in M-5 to M-14 in the same edit pass; they are notes and need no re-check.

## QA Complete

VERDICT: FAIL

