# QA Report: R4 completeness lens

**Topic:** R4 re-anchor of `docs/designs/orchestrator-mode.md` (items 5.1 to 5.11), base `e8db2fe6` to master `5dc29d23`
**Date:** 2026-11-09
**Phase:** report-validation (completeness lens, adversarial)
**Fix cycle:** N/A (`fix_authorization: false`; no file edited except this report)
**Partition note:** one lens of 9 agents. Cross-file checks outside the completeness lens are not made here.

Files read: DESIGN (1041 lines on disk; sections 1, 7.6, 8 to 18 read in full, chunks of at most 150 lines), research/07, research/08, `r4-mechanical.md`, `r4-wc14-hits.md`, `r4-reanchor.md`. Every cited anchor was re-read on disk by me, not taken from those reports.

## Requirement-by-requirement result

R4 list from the BUILD-REQUEST (eight items):

| # | R4 requirement | DESIGN text found | Mark |
|---|---|---|---|
| 1 | WC-16 everywhere | Rule renamed in sections 1 (lines 5, 13), 8 (666, 668, 672, 675, 684, 697), 9 (712 R2, 718 R8), 10 (732), 12 (794), 13 (829, 852), 15.2 (943), 16 (970), 17 (1005, 1006), 18 (1041). `grep WC-14` now returns 4 lines: 668 (master worker rule, kept), 829 and 852 (named as "WC-14 (WC-16 in this design)", historical), 1041 (R4 row naming master's WC-14). No coordinator-loop hit remains. | PRESENT |
| 2 | Cadence alignment | Line 677 (WC-16 text): "On every coordinator wake, at most once every 5 minutes (the cadence of "The sweep." under `### Liveness supervision`)"; "It sweeps on every wake" is gone. Line 672 states the change and that WC-16 does not reword contract lines 110 and 151. Line 712 (R2): "sweeps on every wake, at most once every 5 minutes". Line 829 (D6) records it. Line 696 forbids rewording `liveness-sweep-and-states` and `liveness-ladder-and-restart`. Contract line 110 on disk reads "After every wake or timeout, at most once every 5 minutes", so the alignment is true. | PRESENT |
| 3 | Re-anchoring | Contract anchors 23, 110, 151, 273, 275 and test anchors 25, 89, 165, 173, 209-219, 228-237, 382-391, 755-762, 765, 831-839, 837, 912, 1081-1082, 1318, 1322, 1556, 1940-1944, 1953-1955, 1966, 2016 all read on disk and match the DESIGN text. Routing and doc anchors (HOW-WE-WORK 318, 333, 337, 396, 403, 404; commands.md 105, 115; dev guide 991; CHANGELOG 5; `.gitignore` 254; test files `test_how_we_work_routing_table.py:27`, `test_routing_refresh.py:33,648`, `test_routing_plugin_parity.py:38`; `graph.md` 9 and 41) match. No old 156/158/245-254/545/624/865/470/398 anchor remains in section 8 (r4-reanchor grep, and I read lines 666-703). | PRESENT |
| 4 | `main.py` after 565 | Line 28 (519-565; last pair `issue-watch` at 563 and 565; `__main__` at 568), line 932 (step 1.7 "after line 565"), line 968 (rollback). `grep 'after line 561\|519-561'` returns 0; `after line 565` returns 2. On disk `main.py` has the `issue-watch` pair at 563-565 and `__main__` at 568. | PRESENT |
| 5 | No `## Unattended mode` | Lines 655, 664 (test assertion) and 693 (`_check_no_unattended_sections`, 831-839, equality at 837, glob of every command file). Matches test source. | PRESENT |
| 6 | `UNATTENDED_EXPECT` 31 | Line 692: `_check_p2_set` (1556) asserts exactly 31 entries, so `sweep` is never added. Test source line 1564 says `not 31`. Line 687 adds `assert "sweep" not in UNATTENDED_COMMANDS` at 1322. | PRESENT |
| 7 | Write-verb classification | Line 694: `AUDIT_ROOTS` 1940-1944, the five categories at 1953-1955, `WRITE_VERB_CLASSIFICATION` at 2016, `never-worker` available once `/sc:sweep` is on the list. Line 695: a `read-only` `gh api` entry must not look like a post (`_is_gh_api_post`, 1966). Test source matches. | PRESENT |
| 8 | Step 1.16a record-only | Lines 668, 915, 942, 943, 1006. Four points; gate satisfied once the record exists; none of "wait for", "follow-up PR", "rebase", "is open" on those lines (I re-grepped). I ran the two ancestor checks read-only: `2327fbd3` is an ancestor of HEAD (exit 0) and `495eb96d` is not an ancestor of `origin/master` (exit 1), so points (2) and (3) are true as written. | PRESENT |

WC-14 locations of research/07 line 100:

| Location (old line) | DESIGN text now | Mark |
|---|---|---|
| Design 663-680, section 8 heading | line 666 `## 8. WC-16 and the never-as-worker list` | PRESENT |
| Design 663-680, text block | line 675 `### WC-16. Coordinator loop`; all four pin phrases occur verbatim in 675-677 (re-grepped: 1 hit each) | PRESENT |
| Design 663-680, pins | line 684 `"WC-16": ("WC-16", [...])`, placed after `"WC-15"` (165-172) and before `"heartbeats"` (173); five pins at 684-688 | PRESENT |
| Design 695, R2 bullet | line 712 "WC-16 in `~/.claude/WORKER-CONTRACT.md`" | PRESENT |
| Design 701, R8 changelog | line 718, `WC-16` in the `#### Added (sweep)` list | PRESENT |
| Design 777, FR-023 row | line 794 "WC-16 and the never-as-worker addition (8)" | PRESENT |
| Design 926, step 1.17 | line 943 "WC-16 in `src/superclaude/core/WORKER-CONTRACT.md`" | PRESENT |
| `.gitignore` comment (research/01:285) | line 732 "(WC-16)" | PRESENT |
| research/03:15 | maps to line 668 plus 666 (master WC-14/WC-15 are worker duties; next ID is WC-16) | PRESENT |
| research/03:24 | maps to line 670 (placement after contract line 273, before 275) | PRESENT |
| research/03:34 | maps to line 684 (pin key and phrases) | PRESENT |
| research/03:112 | maps to line 688 (fifth pin, `RULE_PHRASES["never-as-worker"]` at 89) | PRESENT |
| research/03:118 | maps to lines 685 and 701 (`NEVER_AS_WORKER`, 9 entries; line 23 text) | PRESENT |

The research/03 and research/01 lines are research inputs, not DESIGN text. They still say WC-14 and the old line numbers (research/03 has 19 WC-14 hits, research/01 has 5). The DESIGN carries the correct counterpart for each, so none of them is a DESIGN gap (see MINOR F-5).

## Findings

No BLOCKING and no MAJOR finding. Five MINOR notes (they do not fail the gate).

| ID | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| F-1 | MINOR | `docs/designs/orchestrator-mode.md:1041` says the SPEC and REPORT draft names were marked "in 13 and 14". Section 14 (lines 854-879) holds no `WC-1x` text (grep of that range: 0). Only section 13 (829, 852) carries the marks. | The R4 revision-log row overclaims one section. | Change "in 13 and 14" to "in 13". |
| F-2 | MINOR | `tests/skills/test_worker_contract.py:798-803, 813-828` (`_check_repo_setup_gated` fails on a contract code span starting `make`, `bash`, `sh`, `uv`, `python` and the like). research/07 section (e) lists it. Section 8 constraints (690-697) and row 1041 ("recorded the master test constraints") omit it. | The final WC-16 text has no such span (its only spans are `/sc:sweep` and `### Liveness supervision`), so nothing fails today, but a later edit to WC-16 (it still needs owner approval) could trip it unrecorded. | Add one bullet to the line 690-697 list: a code span in WC-16 starting with a launcher word needs the child-setup gate phrases. |
| F-3 | MINOR | Line 688 gives the "from" text of pin 5 as `"`/sc:spawn` and `/sc:swarm-wizard`, "` with a leading quote. Test line 89 is `"`/sc:agent`, `/sc:git`, ... `/sc:spawn` and `/sc:swarm-wizard`, "`. | The leading quote reads as the whole literal; it is a substring. The "to" text is right and agrees with the new line 23 at line 701. | Say "the tail of the line 89 literal" or quote the whole literal. |
| F-4 | MINOR | Line 677 relates WC-16 to contract line 110 by cadence only. research/07 section 4(c) asked WC-16 to say either that `/sc:sweep` is how the line 110 sweep is run, or how the two relate. | A reader could run `/sc:sweep` as a second sweep beside the line 110 liveness sweep. The cadence is aligned, so requirement 2 is met, but identity is unstated. | Owner decision at GQ-11: add "This run is part of that sweep, not a second one" or "it runs in addition to it". |
| F-5 | MINOR | research/03:15, :24, :34, :112, :118 and research/01:285 still say WC-14; research/01 (3 hits) and research/02 (4 hits) still say "after 561" or "519-561". No stale marker in those files. | A later reader of all research could copy the old ID or line. research/07 and research/08 do supersede them. | Leave as is (inputs are not edited) and have the `/task-builder` BUILD-REQUEST name research/07 and 08 as the override. |

One further observation, not graded: no step in section 15.2 owns adding a `WRITE_VERB_CLASSIFICATION` row if `sweep.md` or the skill text ever hits `WRITE_VERB_RE`. The constraint is conditional and the designed text (7.6) contains no `git` or `gh` verb, so requirement 7 is met as written.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | DESIGN on disk is 1041 lines and matches the line count in `r4-mechanical.md` | PASS |
| C2 | R4-1: no coordinator-loop mention of WC-14 remains; WC-16 present in sections 1, 8, 9, 10, 12, 13, 15, 16, 17, 18 | PASS |
| C3 | The 4 remaining WC-14 hits (668, 829, 852, 1041) are all worker-rule or historical-name uses | PASS |
| C4 | research/07:100 location: section 8 heading, text block, pins (666, 675, 684) | PASS |
| C5 | research/07:100 location: R2 bullet (712) | PASS |
| C6 | research/07:100 location: R8 changelog row (718) | PASS |
| C7 | research/07:100 location: FR-023 row (794) | PASS |
| C8 | research/07:100 location: step 1.17 (943) | PASS |
| C9 | research/07:100 location: `.gitignore` comment (732) | PASS |
| C10 | research/07:100 research/03 lines mapped to DESIGN text (with F-5 noted) | PASS |
| C11 | R4-2: cadence aligned with contract line 110 in WC-16, R2 and D6; lines 110 and 151 not reworded (F-4 noted) | PASS |
| C12 | R4-3: contract and test-file anchors re-read on disk (contract 23, 110, 151, 273, 275; test file 29 anchors) | PASS |
| C13 | R4-3: routing, doc, `.gitignore` and `graph.md` anchors re-read on disk | PASS |
| C14 | R4-4: `main.py` after 565 at lines 28, 932, 968; no 561 text left; disk matches | PASS |
| C15 | R4-5: no `## Unattended mode` (655, 664, 693) | PASS |
| C16 | R4-6: `UNATTENDED_EXPECT` 31 (692) matches test line 1564 | PASS |
| C17 | R4-7: write-verb classification constraints (694, 695) match test source | PASS |
| C18 | R4-8: step 1.16a record-only on every 1.16a line; ancestor claims true | PASS |
| C19 | Five pins listed; new pin key `"WC-16"`, four phrases verbatim in the text, `_check_rule` ident rule met on heading line | PASS |
| C20 | Mechanical re-run: em-dash 0, TODO/TBD 0, 18 numbered sections, `Total: 9 deviations.` (834), `Total: 23 open items.` (1010) | PASS |
| C21 | Section 18 R4 row accurate (F-1: one overclaim, MINOR) | PASS (with 1 MINOR) |
| C22 | Self-audit: no BLOCKING or MAJOR found despite adversarial stance; each PRESENT mark cites a line I read | PASS |

## Confidence

Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 20 | Grep: 12 | Glob: 0 | Bash: 7 (all read-only `sed -n`, `grep`, `git merge-base --is-ancestor`, `git cat-file`; no `orca`, no network)
Tool-engagement minimum: Read + Grep + Glob = 32, above 22 checks.

## Recommendations

- Proceed. Optionally apply F-1 and F-2 in the next DESIGN edit; they are one-line changes.
- F-4 belongs in the GQ-11 owner approval of the WC-16 text.

Verdict: PASS
Blocking count: 0
