# QA Report - Research Gate (Lens: Evidence Quality)

**Topic:** Issue #339 Phase 1 MDTM task research (orchestrator mode, R3-B1/B2/B3 first)
**Date:** 2026-11-08
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**fix_authorization:** false (report only; no research file edited)
**Assigned files:** 01-file-inventory.md, 02-patterns-conventions.md, 03-integration-points.md, 04-design-fixes-r3.md, 05-test-verification.md, 06-template-examples.md

---

## Progress log

- Report created. Reading research files next.
- Read all six files in full (01: 354 lines, 02: 169, 03: 120, 04: 232, 05: 157, 06: 164), in chunks of 150 lines or fewer, plus `research-notes.md` (67 lines). All six carry `Status: Complete` and a `## Summary` section.
- `research-notes.md:9` says `CLI_MODE: false (reflect_post_mode: skill)` and `:62` says `QA_INTENSITY full`. Both are used below.
- First-pass suspicions to verify: (a) 01 C11 lists only the design's 4 pins for `test_worker_contract.py`, while 03 IP-2 says a fifth pin breaks; (b) 02 section 9 names `tests/cli/sweep/` while 01/05 and the design name `tests/sweep/`; (c) 02 section 5 "34 of 34 files" vs "the lazy `__init__.py` files do not have it"; (d) 06 recommends standard-intensity gate counts while the notes set full; (e) Orca bundle byte offsets in 04.
- Spot-check wave 1 (01/03 anchors, 13 blocks): every anchor in `main.py`, `WORKER-CONTRACT.md`, `HOW-WE-WORK.md`, both routing tests, `test_routing_plugin_parity.py`, `commands.md`, the developer guide, `CHANGELOG.md`, `.gitignore`, `graph.md` and `test_worker_contract.py` read as claimed. `cmp` of the two HOW-WE-WORK copies: identical. Suspicion (a) CONFIRMED: `test_worker_contract.py:86-92` pins the old line-23 text word for word.
- Spot-check wave 2 (design lines): all 16 rows of the 04 drift table match the current design; every quoted edit anchor in 04 exists verbatim and once (494 x4, 497, 739, 815, 853, 1011).
- Spot-check wave 3 (02 code cites, 13 blocks): all match, except two small errors noted below (34 of 34; graph.md:16).
- Spot-check wave 4 (04 bundle): 20 byte offsets read with `dd`; all 20 land on the claimed token. Field list of `hG`, the `E6e`/`gG` return shape, 59 `completed_at` hits, zero `startedAt`/`endedAt` in the `hG`/`gG` range, projection file size 9,892 bytes, Orca version `1.4.245-aidev02.780594c521aa` and the `worker-list --help` text all confirmed.
- Spot-check wave 5 (05 test anchors, 15 blocks) and wave 6 (06 template/TB/example cites, 14 blocks): all match. `uv pip list`: click 8.5.1, pytest 9.2.0, no pytest-xdist, as 05 says.

---

## Overall Verdict: FAIL

3 IMPORTANT (blocking), 0 CRITICAL, 7 MINOR. The evidence itself is strong: of about 215 cited `file:line` references and bundle offsets re-read (well over 20 percent), 213 say what is claimed. The FAIL comes from one unresolved cross-file contradiction, one unclosed gap with a wrong source, and gate-count guidance written for the wrong QA intensity.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | 6/6 files `Status: Complete` (line 5 or 6 of each) with a `## Summary` section; read in full |
| 2 | Evidence density | PASS | All six rate Dense (over 80 percent of claims carry path plus line or symbol). Spot-checked about 215 cites across six waves; 2 wrong (MINOR M3, M4) |
| 3 | Scope coverage | PASS | Every `research-notes.md:15-24` EXISTING_FILES entry is covered: main.py (01 C1, 02 s1), WORKER-CONTRACT (01 C2, 03 IP-1), test_worker_contract (01 C11, 03 IP-2), both HOW-WE-WORK copies (01 C3-C4, 03 IP-4/5), routing tests (01 C5-C6, 03), commands.md, dev guide, CHANGELOG, .gitignore (01 C7-C10, 03 IP-4/6), review-3 and inv-005 (04), template 02 (06) |
| 4 | Doc cross-validation tags | PASS (note) | No file uses the bracket tags `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` (grep count 0 in all six). Design claims are cross-checked in plain words (CONFIRMED, Unverified, DESIGN GAP, "flag"). Every code contradiction I found is flagged in at least one file. Format only: MINOR M6 |
| 5 | Contradiction resolution | FAIL | 01 vs 03 on the `test_worker_contract.py` pins (IMPORTANT I-1); 02 vs design on test folder (M1); 05 vs design on the rename (M5) |
| 6 | Gap severity | FAIL | `SessionRow` ten #409 dimensions: deferred by 01 to researchers 3/4, covered by neither, and the named source (the SPEC) does not hold the names (IMPORTANT I-2) |
| 7 | Depth appropriateness (Deep) | PASS | 04 traces the Dispatch time fields end to end: SQLite schema @1776005, insert @1629395/@1630462, projection `hG` @1421905, handler @1447759, CLI print, then into the 7.2 model and fixtures |
| 8 | Integration point coverage | PASS | 03 covers contract, pins, R1-R8 with their tests, write-verb audit, sync targets; all anchors re-read |
| 9 | Pattern documentation | PASS | 02 and 05 document registration, lazy `__getattr__`, seams, mocks, AST guard, atomic publish precedents, drift-test helpers; re-read |
| 10 | Incremental writing | PASS | Files show staged structure (sections, per-section evidence lines, forward references between researchers); file mtimes 07:31 to 07:35 in research order |
| 11 | Gate guidance vs stated intensity (lens add-on) | FAIL | 06 counts follow standard; notes say full (IMPORTANT I-3) |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | IMPORTANT | 01 C11 table (lines 289-300), D table step 1.19 (line 336), edit counts (line 346), Summary (line 353) | 01 says every anchor is CONFIRMED and lists 4 edits to `test_worker_contract.py` (lines 155, 254, 545, 865). It misses the fifth pin that 03 IP-2 (lines 45-50) found: `test_worker_contract.py:86-92` pins `` "`/sc:spawn` and `/sc:swarm-wizard`, " `` verbatim, and the design's new line 23 (`orchestrator-mode.md:684`) reads `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard` ``, so `test_contract_states_rule[never-as-worker]` fails. I re-read both. The two files disagree and neither says which wins. A builder using 01's checklist-ready table writes a failing step 1.19. | Merge note or 01 fix: step 1.19 has 5 edits; add `:89` (new phrase per 03 line 49) in the same commit as the line-23 change. |
| I-2 | IMPORTANT | 01 B2 gap line 45, Summary line 354 | 01 defers "the ten #409 dimensions of `SessionRow`" to "the SPEC (researcher 3/4 scope)". No other file covers them. The SPEC (`merged-requirements.md:235`) does not list them either: it says "the ten #409 dimensions defaulting to `unknown` (REPORT step 1.2)". The names live in `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md:1245` (`lifecycle`, `phase`, `health`, `approval`, `freshness`, `result`, ... from `data-dictionary.md:19-28`). Without that pointer, the step 1.2 item either sends the executor to a source that lacks the names or invites invented field names. | Add one finding: the ten dimension names and values are in REPORT line 1245 (step 1.2 row); the step 1.2 item must cite it. |
| I-3 | IMPORTANT | 06 section 11 item 2 (line 132), Summary (line 158) | 06 sizes every gate at standard intensity ("3 structural + 3 content + 1 domain = 7 (I22, T02:831)"; "standard: 7 per final gate, 2 fidelity, 2 verifiers"). `research-notes.md:62` sets `QA_INTENSITY full`. At full, I19 applies unchanged (T02:704, T02:838-839): a 500-1500-line gated output needs 4+4=8 (T02:713), larger outputs 10 or 12; M4 must partition across 3-4 fidelity agents when sources exceed 1000 lines (T02:788; design 1013 + SPEC 653 lines); partitioning starts above 6 files (T02:745); double QA is not disabled (T02:827, 836 disable it only at lite and standard). A builder copying 06's counts gets gates TB Rule 16 (TB:2365) calls MALFORMED. | Restate the gate shapes for full intensity: per-gate counts from T02:710-715 by gated output size, intermediate gates at least 5 (T02:737-741), fidelity 3-4 agents, no double-QA waiver. |
| M1 | MINOR | 02 section 9 table, line 157 | Names `tests/cli/sweep/` as the test folder. The design names `tests/sweep/` (`orchestrator-mode.md:726`), as do 01 and 05. 02 hedges at line 159. | Use `tests/sweep/`. |
| M2 | MINOR | 02 section 5, line 62 | "34 of 34 files" and "the two `__init__.py` files ... (`recommend/__init__.py`, `tasklist/__init__.py`)". Actual: 34 of 36 `.py` files in reflect, recommend and swarm have `from __future__ import annotations`; the two without it are `reflect/__init__.py` and `recommend/__init__.py`. `tasklist` is outside the counted set. | Correct the count and the file names. |
| M3 | MINOR | 02 section 8.2, line 115 | Says `graph.md:16` names both `~/.claude/...` and the project `.claude/...` copy. `graph.md:16` names `~/.claude/CODEGRAPH.md` and a `src/superclaude/core/CODEGRAPH.md` fallback, not a project `.claude/` copy. `sc-graph-protocol/SKILL.md:15` is correct and is the model 02 recommends. Copying `graph.md:16` would put a `src/superclaude/` substring into `sweep.md`, which the design test forbids (`orchestrator-mode.md:657`). | Drop the `graph.md:16` cite. |
| M4 | MINOR | 04 lines 197 and 207 | Cite DESIGN line 285 for "the run continues on disk sources"; line 285 is blank, the text is at line 286. | 285 -> 286. |
| M5 | MINOR | 05 section 6, line 70 | "renaming the test is optional". The design requires it (`orchestrator-mode.md:679`); 01 and 03 say so. | Say the rename is a design deliverable. |
| M6 | MINOR | all six files | No `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` bracket tags; plain-word equivalents are used consistently. | None needed for the builder; format only. |
| M7 | MINOR | 06 section 10, line 125 | "skill mode (per the BUILD_REQUEST topic)". There is no BUILD_REQUEST in the task folder; the source is `research-notes.md:9`. | Cite `research-notes.md:9`. |

## Verified-correct highlights (evidence for the PASS rows)

- 04 bundle offsets, all exact: `workerShow` @1447759, `hG` @1421905, `assigneeHandle` @1422020, `assigneePaneKey` @1422053, `retryOfDispatchId` @1422174, `dispatchedAt` @1422409, `completedAt` @1422438, `createdAt` @1422465, `gG` @1422710, schema @1776005, `dispatched_at TEXT` @1777908, `$nt` @1629395 with guards @1629916 and @1630095, `ert` @1630462 ending `'pending', ?, datetime('now'))` near @1630756, handle update @1840874, `coordinator_runs ... completed_at` @1619766, `T6e` @1421588 (04 says "~1421600").
- 04 ccsession cites (`ccsession:566-613`), SPEC FR-010 (`merged-requirements.md:104`), review-3 (83-123) and inv-005 (28, 81) read as claimed.
- 03 IP-2 fifth-pin finding, IP-3 write-verb audit (`test_worker_contract.py:1090-1105, 1131, 1166, 2199, 2203`), IP-5 copy tests, IP-7 Makefile ranges: correct.
- 05 auto-marker risk (`pytest_plugin.py:216-222` uses the full path), `__init__.py` folder facts, CI lines (`test.yml:29, 38, 47, 102, 106, 127, 131, 135, 142`): correct.
- 06 template and TB cites (T02:6, 159-170, 467, 704, 710-715, 854-868, 1100, 1427; TB:1002, 1072-1077, 2142, 2170-2172, 2203-2208, 2219, 2288, 2305, 2312-2314, 2345-2373; `task/SKILL.md:183-184`; the three example task files): correct.

## Not re-run

- 05 line 149 (`--collect-only` on `tests/cli`, 2472 tests): not re-run, to avoid creating caches. Not counted against the file.

## Summary

- Checks passed: 8 / 11
- Checks failed: 3 (items 5, 6, 11)
- Critical issues: 0; Important: 3; Minor: 7
- Issues fixed in-place: 0 (fix_authorization false)

## Confidence

- **Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 13 | Grep: 5 | Glob: 0 | Bash: 16 (13 bounded batch scripts plus 3 single reads). No web research.

## Recommendations

- Before synthesis or the builder runs: resolve I-1 (5 pins for step 1.19), add the I-2 pointer (REPORT line 1245 for the ten dimensions), and restate I-3 gate counts for full intensity.
- The R3-B1/B2/B3 material in 04 is ready to use as the first task items: every quoted anchor exists once in the current design, and the static Orca evidence holds.

## QA Complete

VERDICT: FAIL
