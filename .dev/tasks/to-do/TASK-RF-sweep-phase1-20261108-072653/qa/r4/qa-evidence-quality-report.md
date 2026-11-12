# QA Report: R4 evidence-quality lens (citations into six repo files)

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` after items 5.1 to 5.11 (R4 re-anchor to master `5dc29d23`)
**Date:** 2026-11-08
**Phase:** report-validation (evidence-quality lens), fix cycle N/A
**Fix authorization:** false. No file was edited except this report.
**Checkout:** `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`, HEAD `5dc29d23b`. The six target files have no working-tree diff against HEAD; only the DESIGN and its three review files are untracked.

## Scope and method

DESIGN is 1041 lines on disk (wc -l). I read it in chunks of at most 150 lines (lines 1-39, 40-159, 284-289, 445-519, 636-659, 660-729, 727-757, 810-859, 922-981, 980-1041). Lines 160-283, 290-444, 520-635 and 760-809 were not read in full; I covered them with whole-file regex scans for every `line N`, `lines N-M`, `:N` and `file ... line N` citation (output listed with line numbers), and each hit outside the six files was attributed to its real target (SPEC, GAPS, PANEL, FIXREVIEW, REPORT, ccsession, graph.md and similar).

I then opened each cited line of the six files with `sed -n` or `awk NR` and compared the text DESIGN says it holds with the text on disk. The six files and their sizes now: `WORKER-CONTRACT.md` 327 lines, `test_worker_contract.py` 3195, `main.py` 569, `HOW-WE-WORK.md` 405, `commands.md` 1534, `CHANGELOG.md` 577. I did not rely on r4-reanchor.md or research/07 and 08 for any verdict; I compared them to disk afterwards.

## Citation table (every DESIGN citation into the six files, re-read on this checkout)

| # | DESIGN line | Citation | Text DESIGN says is there | Text on disk | Holds |
|---|---|---|---|---|---|
| 1 | 28 | `main.py` 519-565 | deferred subcommand block | 519 `from superclaude.cli.sprint import sprint_group ... deferred subcommand registration`; 565 last `add_command` | yes |
| 2 | 28 | `main.py` 563, 565 | `issue-watch` pair | 563 `from superclaude.cli.issue_watch.cli import issue_watch_group`; 565 `main.add_command(issue_watch_group, name="issue-watch")` | yes |
| 3 | 28 | `main.py` 568 | `if __name__ == "__main__":` | 568 exact | yes |
| 4 | 932, 968 | `main.py` "after line 565" | insertion point after last `add_command` | 565 is the last `add_command`; 566-567 blank | yes |
| 5 | 670 | `WORKER-CONTRACT.md` 273 | fan-in rule paragraph | 273 `For N input Tasks feeding one merge Task ...` (271 is `### Fan-in rule`) | yes |
| 6 | 670 | `WORKER-CONTRACT.md` 275 | `### Worked example: gate hit, answer, new Task` | 275 exact | yes |
| 7 | 672, 829, 1041 | `WORKER-CONTRACT.md` 110 | "the sweep", cadence "at most once every 5 minutes" | 110 `**The sweep.** After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep ...` (under `### Liveness supervision`, heading at 95) | yes |
| 8 | 672 | `WORKER-CONTRACT.md` 151 | the L1 probe row | 151 `\| L1 probe \| Read-only: ...` | yes |
| 9 | 699, 717, 820, 944, 970 | `WORKER-CONTRACT.md` 23 | never-as-worker line, mentions decision D3 | 23 `- **Never-as-worker list**: ... plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers ...` | yes |
| 10 | 684 | test 25 | `RULE_PHRASES` dict | 25 `RULE_PHRASES = {` | yes |
| 11 | 684 | test 165-172, 173 | `"WC-15"` entry; `"heartbeats"` entry | 165 `"WC-15": (` ... 172 `),`; 173 `"heartbeats": (` | yes |
| 12 | 685 | test 382-391 | `NEVER_AS_WORKER`, 8 entries today, 9 after | 382 `NEVER_AS_WORKER = (` ... 391 `)`; 8 entries (agent, git, help, issue, pm, spawn, swarm-wizard, pr-submit) | yes |
| 13 | 685 | test 1081-1082 | parametrized removal test | 1081 `@pytest.mark.parametrize("cmd", NEVER_AS_WORKER)`; 1082 `def test_never_as_worker_check_fails_when_command_removed` | yes |
| 14 | 686 | test 912 | `test_never_as_worker_list_names_all_seven_commands` | 912 exact; only reference in non-`.dev` files | yes |
| 15 | 687 | test 1318, 1322 | load test def; `assert "load" not in UNATTENDED_COMMANDS` | 1318 def; 1322 exact | yes |
| 16 | 687, 693 | test 837, 831-839 | equality check; `_check_no_unattended_sections` | 837 `assert set(have) == set(UNATTENDED_COMMANDS), (`; 831 def, 839 `)`; globs `Path(_THIS.COMMANDS_DIR).glob("*.md")`, `COMMANDS_DIR` = `src/superclaude/commands` (line 20) | yes |
| 17 | 688 | test 89 | `"`/sc:spawn` and `/sc:swarm-wizard`, "` phrase | 89 `"`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, "` | yes |
| 18 | 692 | test 1556 | `_check_p2_set`, exactly 31 entries | 1556 def; 1564 `assert len(expect) == 31` | yes |
| 19 | 694 | test 1940-1944, 1953-1955, 2016 | `AUDIT_ROOTS`; categories; `WRITE_VERB_CLASSIFICATION` | 1940 `AUDIT_ROOTS = (` ... 1944 `)` (skills, commands, agents); 1953-1955 `_CATEGORY_RE` with the five categories; 2016 `WRITE_VERB_CLASSIFICATION = {` | yes |
| 20 | 695 | test 1966 | `_is_gh_api_post` | 1966 def | yes |
| 21 | 696 | test 209-219, 228-237 | `liveness-sweep-and-states`; `liveness-ladder-and-restart` | 209 key ... 219 `),`; 228 key ... 237 `),` | yes |
| 22 | 697 | test 755-762 | `_check_rule` needs ident on the phrase line | 755 def ... 762; 760-762 asserts `ident in line and phrases[0] in line` | yes |
| 23 | 703 | test 765 | `_check_never_as_worker`, one term line | 765 def; 766-767 assert exactly one line | yes |
| 24 | 711 | `HOW-WE-WORK.md` 318-337 | `<!-- other-commands:v1 -->` table | 318 open marker, 320-321 header, 322-333 twelve rows, 337 `<!-- /other-commands -->` | yes (marker to marker) |
| 25 | 711 | `HOW-WE-WORK.md` 333 | `/sc:spawn` row | 333 `\| `/sc:spawn` \| Requested decomposition ...` (last row; table is alphabetical, so sweep after spawn keeps order) | yes |
| 26 | 712 | `HOW-WE-WORK.md` 396, 403 | `## Orca coordination`; never-workers bullet | 396 exact; 403 `- **Some commands are never workers.** ...` | yes |
| 27 | 716 | `commands.md` 105, 115 | `### 8. UTILITIES`; `/sc:issue` row | 105 exact; 115 `\| [`/sc:issue`](#scissue---...` | yes |
| 28 | 718 | `CHANGELOG.md` 5 | `## [Unreleased]` | 5 exact; 7 `### ccsession: ...` topic heading; 9 and 19 `#### Fixed/Added (...)` match R8's heading style | yes |

All 28 citation groups hold. No line number DESIGN cites in these six files is moved, off by one or pointing at different text.

## Claims tied to the cited lines (beyond the line number)

- WC-16 pins (DESIGN 684): the four phrases `WC-16. Coordinator loop`, `On every coordinator wake`, `it is never posted`, `It never stops watching on its own` each occur verbatim in the WC-16 block at DESIGN 675-678. The heading line carries `WC-16` and the first phrase, so `_check_rule` (test 760-762) is satisfied.
- Line 23 replacement (DESIGN 701): compared word for word with the current line 23. The only difference is the inserted `` `/sc:sweep`, `` after `` `/sc:spawn` `` (and the moved `and`). Every other sentence is identical. It stays one line, as `_check_never_as_worker` (test 766-767) needs, and the new order matches the edited phrase at test 89.
- "Giving 9 entries" (DESIGN 685): 8 entries on disk, so 9 is right.
- Stale anchors: a whole-file scan of DESIGN for the old values (`line 156`, `158`, `545`, `865`, `470`, `398`, `624`, `245-254`, `1090`, `1098`, `1103`, `1166`, `after line 561`, `519-561`) returns no hit. `after line 565` occurs twice (932, 968).
- WC-14: four hits remain (668, 829, 852, 1041). 668 and 1041 name master's worker rule (contract lines 63 and 64 are in `## 3. Worker-session duties`); 829 and 852 are the labelled historical names `WC-14 (WC-16 in this design)`. No coordinator-loop use of WC-14 remains.
- Host facts (DESIGN 27, 30, 729): `src/superclaude/cli/sweep/`, `tests/sweep` and any `sweep*` file under `src/` do not exist; `/opt/Orca/resources/app.asar.unpacked/out/package.json` line 5 is `"version": "1.4.245-aidev02.780594c521aa"`; `.gitignore` has no `sweeps` entry and line 254 is `.dev/sprint-state/`.

## Out-of-assignment citations spot-checked (all hold)

`graph.md` line 9 (`allowed-tools: Skill, Bash(codegraph init --yes *), ...`) and line 41 (`## Activation`); `.gitignore:254`; developer guide line 991 (never-as-worker list, no `/sc:sweep`); `tests/core/test_how_we_work_routing_table.py:27` (`_OTHER_COMMANDS = {`, 12 members, matching the 12 table rows); `tests/recommend/test_routing_refresh.py:33` (`{"graph", "impact", "issue"}`) and `:648` (`assert shipped - _POST_REFRESH_ADDITIONS == active`); `tests/commands/test_routing_plugin_parity.py:38` (`filecmp.cmp(..., shallow=False)`); `src/superclaude/cli/recommend/__init__.py:12-20` (lazy `__getattr__`).

## Input artifacts compared with disk

- research/07 (contract side): every old-to-new anchor I opened holds on disk (contract 9, 23, 62-64, 71, 95, 110, 124, 151, 201, 213, 244, 246, 250, 273, 275, 283, 289, 304; test 25, 89, 155-173, 209-237, 374, 382-391, 416, 438, 746, 748, 755-765, 831-839, 907-913, 1044-1045, 1081-1082, 1318, 1322, 1355, 1556, 1940-1955, 1966, 1981, 2005, 2016, 3126-3150). Its claim that a second `"WC-14"` key would override the worker entry is consistent with the dict entries at test 156 and 165.
- research/08 (routing side): main.py, HOW-WE-WORK, commands.md and CHANGELOG anchors all hold, including the in-place text changes at HOW-WE-WORK 329 and commands.md 115.
- r4-reanchor.md: every row of its two citation tables matches disk. Coverage and range gaps are in F1 and F2.
- r4-mechanical.md: its recorded command outputs match the current DESIGN (1041 lines; section map lines 666, 705, 727, 741, 766, 818, 854, 881, 961, 980; `Total: 9 deviations.` at 834; `Total: 23 open items.` at 1010; WC-14 hits 668, 829, 852, 1041; the five `at most once every 5 minutes` lines 672, 677, 712, 829, 1041). One wording nit in F3.
- r4-wc14-hits.md: its Before/After lists are consistent with the final state (4 hits). It quotes `1000:Total: 23 open items.` at its 5.3 snapshot; the line later moved to 1010, which r4-mechanical records correctly.

## Findings

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `phase-outputs/discovery/r4-reanchor.md:66` lists "19 hit lines" (28, 63, 654, 670, 699, 711 to 718, 729, 820, 932, 944, 968, 1041); its tables at lines 68-127 never list DESIGN 829 (D6: `contract line 110`), 970 (rollback: `the line 23 never-as-worker entry`) or 672 as a first-table row (672 is only covered by the "section 8 (line 110)" and "(line 151)" rows). | The citation re-check is not exhaustive: two DESIGN lines that cite contract lines 110 and 23 were never recorded as read. The cited lines do hold (rows 7 and 9 above), so no DESIGN defect follows. | Add one row each for DESIGN 829 and 970 to the table in r4-reanchor.md, citing contract lines 110 and 23. |
| F2 | MINOR | `r4-reanchor.md:39` says "Section 8 is lines 666-695" and its stale-anchor grep at line 41 runs `sed -n '666,695p'`. Section 8 runs 666 to 703 (`## 9.` is at DESIGN 705). | The stale-anchor grep skipped DESIGN 696-704, which holds contract line 23 (699) and `_check_never_as_worker` line 765 (703). I re-ran the scan over the whole file and found no stale anchor, so the claim is true but was under-tested. | Widen the recorded range to `666,704p`, or state that the whole file was scanned. |
| F3 | MINOR | `phase-outputs/test-results/r4-mechanical.md:147` says the cadence phrase is "in section 8 (2 lines) and in the WC-16 block (1)". Its own grep (lines 99-100) shows section 8 has lines 672 and 677, and 677 is the block. | Wording double-counts line 677. The pass result is right. | Reword to "section 8 (672, 677; 677 is the WC-16 block), R2 (712), D6 (829) and the R4 row (1041)". |

MINOR findings never fail the gate.

## Not verified (outside this lens or forbidden tools)

- PR #422 merge commit `2327fbd3` and the `495eb96d` ancestry result (DESIGN 668, 942): needs `git`, which this task limits to grep, sed, awk and wc. Not a citation into the six files.
- SPEC, GAPS, PANEL, FIXREVIEW, REPORT, ccsession and README line citations (DESIGN 19-23, 32, 49-67, 84-116, 502-517, 755-757, 815-816, 824-831, 856): not in the six-file assignment.
- Whether the WC-16 text trips any other pin in `test_worker_contract.py` (for example forbidden-word or repo-setup checks): a behaviour question for the other lenses, not a line-citation question.

## Checks

| id | check | result |
|---|---|---|
| C1 | `main.py` 519-565, 563, 565, 568 and "after line 565" (DESIGN 28, 932, 968) | PASS |
| C2 | `WORKER-CONTRACT.md` line 23 text and D3 mention (DESIGN 699, 717, 820, 944, 970) | PASS |
| C3 | `WORKER-CONTRACT.md` lines 110 and 151 (DESIGN 672, 829, 1041) | PASS |
| C4 | `WORKER-CONTRACT.md` lines 273 and 275 (DESIGN 670) | PASS |
| C5 | `test_worker_contract.py` lines 25, 89, 165-172, 173 (DESIGN 684, 688) | PASS |
| C6 | `test_worker_contract.py` lines 382-391 (8 entries, 9 after) and 1081-1082 (DESIGN 685) | PASS |
| C7 | `test_worker_contract.py` lines 912, 837, 1318, 1322 (DESIGN 686, 687) | PASS |
| C8 | `test_worker_contract.py` lines 1556 (31 entries) and 831-839 with `COMMANDS_DIR` glob (DESIGN 692, 693) | PASS |
| C9 | `test_worker_contract.py` lines 1940-1944, 1953-1955, 1966, 2016 (DESIGN 694, 695) | PASS |
| C10 | `test_worker_contract.py` lines 209-219, 228-237, 755-762, 765 (DESIGN 696, 697, 703) | PASS |
| C11 | `HOW-WE-WORK.md` lines 318-337, 333, 396, 403 (DESIGN 711, 712) | PASS |
| C12 | `commands.md` lines 105 and 115 (DESIGN 716) | PASS |
| C13 | `CHANGELOG.md` line 5 and topic-heading style (DESIGN 718) | PASS |
| C14 | The four WC-16 pin phrases occur verbatim in the WC-16 block (DESIGN 684 vs 675-678) | PASS |
| C15 | Line-23 replacement text differs from disk only by the inserted command (DESIGN 701) | PASS |
| C16 | No stale old anchor or `after line 561` text remains anywhere in DESIGN | PASS |
| C17 | r4-reanchor.md re-check covers every DESIGN citation into the six files and its range covers section 8 | FAIL (MINOR only: F1, F2) |
| C18 | r4-mechanical.md and r4-wc14-hits.md outputs match the current DESIGN | PASS (wording nit F3 is MINOR) |
| C19 | research/07 and research/08 anchors hold on disk | PASS |
| C20 | Out-of-assignment citations (graph.md, .gitignore, dev guide 991, three test files, recommend `__init__`) and host facts hold | PASS |
| C21 | Whole-file scan finds no other DESIGN line citation into the six files (the remaining `line N` hits point at SPEC, GAPS, PANEL, FIXREVIEW, REPORT, ccsession) | PASS |

## Self-audit

Zero BLOCKING or MAJOR findings is credible here because each of the 28 citation groups was opened on disk and compared by text, and the three MINOR findings come from the gate artifacts, not DESIGN. Places where a defect could still hide: the unread DESIGN stretches (160-283, 290-444, 520-635, 760-809) were scanned by regex only; and citations to SPEC, GAPS and the other non-assigned sources were not opened.

**Confidence:** Verified: 21/21 | Unverifiable: 0 (three claim groups outside the lens are listed above, not counted as checks) | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 18 | Grep: 9 | Glob: 1 | Bash: 17 (all read-only: sed -n, awk NR, grep, wc, ls)
No orca or orca-ide command was run and no network call was made. No `uv` command was needed because no Python ran.

Verdict: PASS
Blocking count: 0
