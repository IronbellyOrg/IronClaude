# QA Report: Downstream-actionability lens (item 7.26, rf-qa-qualitative)

**Date:** 2026-11-11
**Phase:** decisions gate, downstream-actionability lens
**fix_authorization:** false (report-only; no file edited except this report)
**Method:** read every listed input in chunks of at most 150 lines, then re-checked the live files they cite (DESIGN, WORKER-CONTRACT.md, test_worker_contract.py, pragmatic.md, .gitignore, fixtures). Acted as the developer of steps 1.2 to 1.6 (items 8.3, 8.4, 8.12, 9.1) and 1.17 to 1.19 (items 12.1 to 12.3).

## Value ledger (what the developer needs, and where it comes from)

| Value | Source | Verified against | Status |
|---|---|---|---|
| Window default `6h`, activity only | OQ-5 record:34; DESIGN 7.4:571, 7.5:607 | consistent in DESIGN, 8.12, 9.1, 10.5 | OK |
| Output default `<root>/.dev/sweeps/`, UTC `<YYYYMMDD-HHMMSS>-sweep.md` | OQ-2 record:34; DESIGN 3.2 line 105 ("UTC, SweepContext.now"); item 8.6 anchor | `.gitignore:254` is `.dev/sprint-state/`, no `sweeps` entry yet | OK |
| Rule id `WC-16` (not WC-1, not occupied WC-14/15) | OQ-3 record:37; DESIGN 8:677-680 | `WORKER-CONTRACT.md:23`, `:110`, `:271-275` match items 12.1/12.2; `test_worker_contract.py:25, 86-92, 165, 173, 382-390, 912, 1322` match item 12.3 (8 entries now, 9 after) | OK |
| Four pin phrases | DESIGN 8:686 | all four occur in the DESIGN rule text (lines 677-679) | OK |
| Field names (`dispatch.dispatchedAt/completedAt/status`, `projection.liveness.verdict`, `worktrees[].path`, `page.limit/total/hasMore/nextCursor`) | 1.0a-facts.md:11-25, 29-40 | present in `captured-worker-show-1.json`, `captured-worker-list.json:391-394`, `captured-worktree-ps.json:13,242-243` | OK |
| Time formats | facts row 23 | fixture `dispatchedAt` `2026-11-11 19:35:55`, `completedAt` ISO `...Z`; both accepted by DESIGN 7.2:470 | OK |
| `RUN_ID_RE = run_[0-9a-f]{12}`, `DISPATCH_ID_RE = ctx_[0-9a-f]{12}` | facts row 2 | all 10 Run ids in OQ-8 record, `run_000000000000`, and 5 fixture dispatch ids match | OK |
| Page size 100, no cursor template, full page = truncated, total lower bound | OQ-17 record:38; DESIGN 17 item 5 (line 995); facts:56 | consistent; `ALLOWED_ORCA` stays 10 (DESIGN 7.3:526-537) | OK |
| Join field (`session_join`) | facts rows 1, 22 and "Need" table | fixtures: pane key and handle both equal the tab-map entry | **AMBIGUOUS (F1)** |
| Orca version compare | facts row 15; DESIGN 7.1:426, 7.5:611-612 | no compare rule anywhere | **MISSING (F2)** |

## Checks

| Check | Description | Result |
|-------|-------------|--------|
| C1 | Window default (6h, activity-only) is explicit and consistent across OQ-5, DESIGN, items 8.12, 9.1, 10.5 | PASS |
| C2 | Output default, file name and UTC rule are explicit and consistent (OQ-2, DESIGN 3.2, items 8.6, 9.1) | PASS |
| C3 | Rule id WC-16 and every anchor for steps 1.17 to 1.19 hold against live WORKER-CONTRACT.md and test_worker_contract.py | PASS |
| C4 | Field names in the facts file exist in the captured fixtures | PASS |
| C5 | Time formats are stated and accepted by DESIGN 7.2 time parsing | PASS |
| C6 | Id regexes match every captured and recorded id | PASS |
| C7 | Page size, cursor refusal and truncation rule agree across OQ-17, facts, DESIGN 7.3 and open item 5 | PASS |
| C8 | Join field is selected unambiguously for models/classify/probes | FAIL (F1) |
| C9 | Orca version string and its comparison rule are actionable for report.py and test_report.py | FAIL (F2) |
| C10 | Eight prerequisite records plus OQ-17 are RESOLVED, agree with owner-decisions.md and facts; no OQ-18 file, consistent with facts:55 | PASS |
| C11 | R5 edit is consistent in DESIGN 7.3, 11, 12, 13 (D10), 15.1, GQ-109 row (line 66) and section 18 R5 row (line 1047) | PASS |
| C12 | D9/OQ-7 record points at DESIGN section 13 row D9 line 836 and open item 22 (line 1012), both live (only the row location and wording prefix were compared, not the whole quote byte for byte) | PASS |
| C13 | Captured fixtures agree with SOURCES.md and with the join claims (tab-map files 1 to 5 vs worker-show 1 to 5, pane key `:` vs `+`, handle line 3) | PASS |
| C14 | Style 7.10 (pragmatic.md:22-26 plus six qualified sites 57, 62, 64, 73, 84, 94) is actionable in skill item 11.3 body | PASS (notes F5, F6) |
| C15 | The same rule is actionable in test item 11.4 (seven restatement sites, positive and negative cases) | PASS (notes F5, F6) |
| C16 | Items 8.3, 8.4, 8.12, 9.1 contain every value they need or point to a file that does | PASS (notes F3, F4, F7) |
| C17 | Items 12.1 to 12.3 are actionable at current HEAD | PASS |
| C18 | Rule 5 inputs (`in_progress`, `agentWait`) are honestly recorded as unverified with DESIGN fallback | PASS (note F3) |

## Findings

### F1 (MAJOR): the join field for `session_join` is never chosen
- Evidence: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md:11` says the join values are `assigneePaneKey` "and" `assigneeHandle`; the "Need" table at line 34 says "`assigneePaneKey` ... **or** `assigneeHandle`". DESIGN `docs/designs/orchestrator-mode.md:457` types `session_join: str | None` (one value); `:460` stores `TabMapEntry.file_name` with `:` already written as `+`; `:497` compares `session_join` to `file_name` or `terminal_handle`. Item 8.3 (task file line 1438) repeats `session_join: str | None` without naming the source.
- Why it matters: a pane key contains `:`, the stored `file_name` contains `+`. A developer who stores `assigneePaneKey` unchanged gets zero joins (every row becomes "tab map join not observable"); one who stores `assigneeHandle` gets direct equality with `terminal_handle`. Nothing says which, or where the `:` to `+` step lives. The fixtures do hold both joins (worker-show-1..5 vs tab-map-1..5), so the data is fine; the instruction is missing. The error would only surface at the item 9.3 live check.
- Smallest fix: add one line to `1.0a-facts.md` (rows 1 and 22 and the "Need" table): "`session_join` = `result.dispatch.assigneeHandle`, compared by equality with `TabMapEntry.terminal_handle`; `assigneePaneKey` is not stored" (or name the pane key plus the `:` to `+` rule).

### F2 (MAJOR): no rule for comparing the live Orca version to `CHECKED_ORCA_VERSION`, and the DESIGN test string is stale
- Evidence: facts row 15 (`1.0a-facts.md:22`) records the live version `1.4.245-aidev02.9cfecdd30b2a` and says the suffix changed from the design's `780594c521aa`. DESIGN line 30 and the `test_report.py` row (line 761) still use `1.4.245-aidev02.780594c521aa`. `CHECKED_ORCA_VERSION = "1.4.245"` (line 426). Lines 611-612 pick "unlikely" or "UNVERIFIED" with no comparison rule. Item 10.5 (task file line 1812) repeats the old string.
- Why it matters: exact equality makes "unlikely" unreachable for any real build (the suffix already changed once); a loose prefix test (for example `startswith("1.4.245")`) would also accept `1.4.2450`. That line is a safety claim about lock risk, so the wrong reading is either a useless line or a false-safe one. Item 8.12 gives the developer nothing to decide with.
- Smallest fix: state the rule in `1.0a-facts.md` row 15 or in item 8.12 (for example "text before the first `-` equals `CHECKED_ORCA_VERSION`"), and make item 10.5 test the live string `1.4.245-aidev02.9cfecdd30b2a` as well as `1.4.246` and a missing file.

### F3 (MINOR): Rule 5 cannot match, by DESIGN's own vocabulary
DESIGN 7.2:491 needs `status == "in_progress"`; DESIGN 15.1:907 lists the status values as `pending, dispatched, completed, failed, circuit_broken`; the capture saw only `completed` (`captured-worker-show-1.json:21`). Facts row 6 and DESIGN open item 6 (line 996) already say "Rule 5 cannot match; rows fall to the fallback", so the developer is told what to do. Note only: item 8.4 should be coded to the DESIGN literal and the working class stays unreachable in Phase 1.

### F4 (MINOR): the facts "field names" table omits several names step 1.3/1.4 need
Missing: the WC-13 `parent` path (`result.projection.parent`, null in fixtures), the `worker-list` row keys (`dispatchId`, `runId`, `workerState`, `dispatchStatus`, `agentTerminalHandle`; the last equals `assigneeHandle`, so a list row alone can carry a handle for rows past the 50-call show cap). All are in `captured-worker-list.json` and `readonly-probe.md`, so the developer can find them; listing them would save a hunt. Also the pinned banner `[Orca rows: 100 shown; ... (paging not yet captured)]` (DESIGN 7.5:616, test row 761) is slightly stale now that `page.nextCursor` was captured; it is a pinned string, leave it.

### F5 (MINOR): style to skill to test, small gaps in the traced rule
Traced and confirmed equal in substance: the five conditions and the exempt reply (pragmatic.md:23), assignment source and non-sources (:24), exclusions and stderr handling (:25), scope (:26), six qualifier sites (grep count 6 at lines 57, 62, 64, 73, 84, 94), and item 11.3 / 11.4 text. Gaps:
1. Item 11.3 step (4) is worded so that printing counts and the path appears only in the exempt case; it does not say what a non-exempt reply prints (counts, path, ordinary table, no advice). Add one clause.
2. "Summary counts" is undefined. `summary` also carries `total_is_lower_bound` and `bound_reached` (DESIGN 7.4:590-591); printing only per-class counts could drop the lower-bound caveat. Name the fields.
3. Condition (5) says the report was "Read successfully"; item 11.3 says read "in chunks of at most 150 lines" without "until the end of the file" or the `Report complete` last line.

### F6 (MINOR): one clause is pinned by 11.4 but not required by 11.3
pragmatic.md:25 ends with "There is no general exemption for coordinators, for other skills or for file output." Item 11.4 pins "no general all-coordinator/all-skill/file exemption" without saying which source; item 11.3 does not require the skill to repeat it. If 11.4 asserts it against the skill, 11.3 as written fails it. Say "style only" in 11.4, or add the clause to 11.3. Also the style says "`sc-sweep-protocol` skill" (directory name) while item 11.3 sets frontmatter `name: sc:sweep-protocol` (matches the graph pattern); 11.4 should key on the directory name.

### F7 (MINOR): stale line numbers in item text
Item 8.12 cites DESIGN lines 634, 636, 638, 740 from the unrevised design; the current lines are 643, 645, 647 (and the "not frozen" ban is in the section 11 test row, not line 740). The Phase 8 preamble tells the executor to re-locate by heading, so this does not block.

## Self-audit
- Reliance: relied on the earlier mechanical record (`decisions-mechanical.md`, Run 2 C1 to C9, S1 to S8 PASS) only for counts I then re-checked: qualifier count 6 and the seven site line numbers by reading pragmatic.md lines 1-110; fixture file set by Glob (19 `captured-*.json` plus SOURCES.md, matching the Run 2 list).
- Independent checks (not taken from any prior report): fixture join values by grep across worker-show-1..5, tab-map-1..5 and the list rows; live anchors in WORKER-CONTRACT.md and test_worker_contract.py; DESIGN 7.1 to 7.6, 8, 10, 11, 15, 17, 18 and the addendum read directly; regexes tested by eye against all recorded ids.
- Limits: no code was run; not byte-compared: the full D9 quote and the full OQ quotes; future skill/test files do not exist and were not demanded; the SPEC file is the DESIGN file itself (BUILD-REQUEST SPEC_PATH), so no separate SPEC was read.
- Tool engagement: Read 33, Grep 11, Glob 5, Bash 0. No web research.

Verdict: FAIL
Blocking count: 2
