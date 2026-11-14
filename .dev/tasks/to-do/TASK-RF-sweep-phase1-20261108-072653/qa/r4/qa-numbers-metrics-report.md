# QA Report: Numbers lens (R4 gate, DESIGN items 5.1 to 5.11)

**Topic:** `docs/designs/orchestrator-mode.md` (1041 lines on disk) numeric claims against source
**Date:** 2026-11-09
**Phase:** doc-qualitative, numbers and metrics lens (9-agent R4 gate, domain lens, research/09 Gap 5)
**Fix cycle:** N/A (first review). `fix_authorization: false`: no file edited except this report.

Inputs read: DESIGN (sections 1, 6, 7.3, 7.6, 8, 9, 11 rows, 13, 15.2, 16, 17, 18 and every line cited below), research/07 (lines 1-150), research/08 (lines 1-125), `r4-mechanical.md` (1-150), `r4-wc14-hits.md` (1-110), `r4-reanchor.md` (1-129), plus the source files for the recount: `tests/skills/test_worker_contract.py` (cited regions only) and `src/superclaude/core/WORKER-CONTRACT.md`. Spot checks also read the SPEC, PANEL, FIXREVIEW, GAPS, REPORT, `main.py`, `HOW-WE-WORK.md`, `commands.md`, `CHANGELOG.md`, `.gitignore`, `ccsession` at the lines DESIGN cites.

Constraint note: Bash was limited to read-only `grep`, `sed -n`, `awk` and `wc`, so no `git` command was run. Commit ids in DESIGN (`2327fbd3`, `495eb96d`, `5dc29d23`, `e8db2fe6`) are checked only against research/07 and research/08 text, not against git.

---

## Recount (the numbers the task named)

| Number | DESIGN states | Source on disk | Result |
|---|---|---|---|
| Entries in `NEVER_AS_WORKER` after the edit | "giving 9 entries" (DESIGN:685) | tuple at `test_worker_contract.py:382-391` holds 8 strings (`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard`, `/sc:pr-submit` at 390); 8 + `/sc:sweep` = 9. No `len(NEVER_AS_WORKER)` or `== 8` assert exists anywhere in the file (grep) | Supported |
| Entries in `UNATTENDED_EXPECT` | "exactly 31 entries" (DESIGN:692) | awk over lines 438-746 counts 31 top-level keys; `_check_p2_set` at 1556-1565 asserts `len(expect) == 31` | Supported |
| P1 + P2 split behind the 31 | not stated in DESIGN | `P1_COMMANDS` = 16 names, `P2_COMMANDS` = 15 names (lines 396-432), 15 P2 `UNATTENDED_EXPECT` keys; research/07:11 "the 15 P2 conversions" | Supported (15 P2 conversions) |
| Pin edits | "(five edits)" (DESIGN:682) | five bullets at DESIGN:684-688; r4-reanchor.md:44 also counts 5 | Supported in section 8; NOT carried to section 16 (finding N-1) |
| Cadence | "at most once every 5 minutes" (DESIGN:672, 677, 712, 829, 1041) | `WORKER-CONTRACT.md:110` "After every wake or timeout, at most once every 5 minutes"; `### Liveness supervision` header at line 95 | Supported; no unbounded "sweeps on every wake" remains (grep of "every wake" returns only quoted-and-dropped text at 672/829 and the bounded forms) |
| `Total: 9 deviations.` | DESIGN:834 | table rows D1 to D9 at DESIGN:824-832 | Supported |
| `Total: 23 open items.` | DESIGN:1010 | table rows numbered 1 to 23 at DESIGN:984-1008 (awk counted 23 rows, last = 23) | Supported |
| Em-dash | 0 | `grep -c` on U+2014 returns 0; no U+2013 either | Supported |

---

## Issues Found

| id | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| N-1 | MAJOR | `docs/designs/orchestrator-mode.md:970` against `:682-688` | Section 8 says the test file takes **five** pin edits: (1) `RULE_PHRASES["WC-16"]`, (2) `NEVER_AS_WORKER` entry, (3) the rename, (4) the `assert "sweep" not in UNATTENDED_COMMANDS`, (5) the `RULE_PHRASES["never-as-worker"]` phrase at test line 89. The section 16 rollback row names only four test edits: "the `RULE_PHRASES` entry, the `NEVER_AS_WORKER` entry, the `UNATTENDED_COMMANDS` assertion (design) and the test rename". Pin 5 (line 89) is the one R4 added (DESIGN:1041 "added the fifth pin"), and the rollback row was not updated. Following the row literally reverts the contract line 23 (row item "the line 23 never-as-worker entry") but leaves the line-89 phrase containing `/sc:sweep`; `_check_rule` (`test_worker_contract.py:755-758`) then fails `test_contract_states_rule[never-as-worker]` because the phrase is no longer in the contract text. So the documented rollback produces a red test on the reverted tree, and the rollback check on DESIGN:979 would report it only after the fact. | In DESIGN:970 replace "the `RULE_PHRASES` entry" with "the `RULE_PHRASES["WC-16"]` entry, the `RULE_PHRASES["never-as-worker"]` phrase at test line 89" so all five pins are named. |

### Minor notes (never fail the gate)

| id | Severity | Location | Note | Smallest fix |
|---|---|---|---|---|
| N-2 | MINOR | `phase-outputs/test-results/r4-mechanical.md:147` | Check 4 says the cadence phrase is "in section 8 (2 lines) and in the WC-16 block (1)". The grep it quotes (lines 98-104 of that file) returns 5 hits: 672 and 677 (both section 8; 677 IS the WC-16 block, so it is counted twice), 712 (R2), 829 (D6), 1041 (R4). The PASS verdict is right, the arithmetic wording is not. | Reword to "5 hits: 672 and 677 (section 8, 677 is the WC-16 block), 712, 829, 1041". |
| N-3 | MINOR | `phase-outputs/discovery/r4-wc14-hits.md:109` | Records `Total: 23 open items.` at line 1000; DESIGN now has it at 1010 (r4-mechanical.md:139 has the current 1010). A dated snapshot, not a defect in DESIGN. | None needed; optionally note "at that time". |
| N-4 | MINOR | `docs/designs/orchestrator-mode.md:693` | Says `_check_no_unattended_sections` "globs every `src/superclaude/commands/*.md`"; the code at `test_worker_contract.py:834` globs `_THIS.COMMANDS_DIR`. Same set in practice; wording only. | Say "globs the commands directory". |

---

## Checks

| id | Check | Result |
|---|---|---|
| C1 | `NEVER_AS_WORKER` has 8 entries today (`test_worker_contract.py:382-391`) and 9 after appending `/sc:sweep` (DESIGN:685) | PASS |
| C2 | Removal test is parametrized over the tuple (`:1081-1082`), so entry 9 is covered with no further edit, as DESIGN:685 says; no hard-coded length assert exists | PASS |
| C3 | `UNATTENDED_EXPECT` has 31 entries (awk count; `_check_p2_set` `:1564`), so DESIGN:692 holds and `sweep` must not be added | PASS |
| C4 | P1 = 16, P2 = 15, 16 + 15 = 31; 15 P2 conversions (`:396-432`; research/07:11) | PASS |
| C5 | Section 8 states five pin edits and lists exactly five (DESIGN:682-688) | PASS |
| C6 | The five-pin count is carried consistently to every other place that enumerates the pins (section 16 row at DESIGN:970; test-plan row `:761`; step 1.19 row) | FAIL (N-1) |
| C7 | The four WC-16 `RULE_PHRASES` phrases occur verbatim in the final text at DESIGN:675-677, and the heading carries `WC-16` as `_check_rule` (`:759-762`) requires | PASS |
| C8 | Cadence "at most once every 5 minutes" equals `WORKER-CONTRACT.md:110`; present in WC-16 (677), R2 (712), D6 (829), R4 (1041); "three changes" at DESIGN:672 matches the three listed | PASS |
| C9 | `Total: 9 deviations.` equals rows D1 to D9 | PASS |
| C10 | `Total: 23 open items.` equals rows 1 to 23 | PASS |
| C11 | Em-dash count 0 (and no en-dash) | PASS |
| C12 | All 27 test-file anchors in section 8 (25, 89, 165-173, 209-219, 228-237, 382-391, 755-762, 765, 831-839, 912, 1081-1082, 1318-1322, 1556, 1940-1944, 1953-1955, 1966, 2016) match the file | PASS |
| C13 | Contract anchors 23, 110, 151, 273, 275 match; fan-in "fewer than 2" (273), "third brief-guard refusal" (244, "at most 2 brief fixes"), "ready Task it did not create" (246), "frozen plan" (250) match the WC-16 escalation list | PASS |
| C14 | Re-anchored non-contract lines: `main.py` 519/559/561/563/565/568, `HOW-WE-WORK.md` 318/333/337/396/403, `commands.md` 105/115, dev-guide 991, `CHANGELOG.md` 5, test files `test_how_we_work_routing_table.py:27`, `test_routing_refresh.py:33,648`, `test_routing_plugin_parity.py:38`, `.gitignore:254`, `recommend/__init__.py:12-20`; `after line 565` occurs twice (932, 968), no `after line 561` | PASS |
| C15 | SPEC, PANEL, FIXREVIEW, GAPS, REPORT line anchors DESIGN cites (95-120, 130-144, 175, 177, 199-200, 231, 236, 240, 253, 259, 261, 269, 295-299, 319-321, 335, 380, 388, 392, 404-410, 420, 440-454, 587-607, 637; PANEL 289-296; FIXREVIEW 103-112; GAPS 124-138; REPORT 1237) | PASS |
| C16 | Counts in sections 6, 7.3, 11: 8 templates and 7 verbs; `1 + 3R + 1 + 50`; 2 Runs of 40 give 25 each; nine boundary fixtures = 3 limits (SPEC:297) x 3; seven `tests/sweep/` files (six tests + `conftest.py`); three existing test files edited; five list-incomplete cases (3 SPEC + tab map + Run not confirmed); seven `test_fr010_*` (3 + 3 + notes order); 50 / 90 s / 120 s / 6 h per SPEC FR-003, FR-020, NFR-007 | PASS |
| C17 | Mechanical reports (`r4-mechanical.md`, `r4-wc14-hits.md`, `r4-reanchor.md`) agree with the DESIGN on disk: 1041 lines, section map line numbers, `Total` lines at 834 and 1010, WC-14 hits 668, 829, 852, 1041, 19 re-anchor hits | PASS (notes N-2, N-3) |
| C18 | Sizing: DESIGN is 1041 lines, inside the 500-1500 row of research/09 Gap 5 (1013 at build time) | PASS |

---

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt, so I fell back to standalone behaviour. I relied on nothing from rf-qa. I did not re-run `r4-mechanical.md`'s checks by trusting them; each was re-derived below.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- `NEVER_AS_WORKER` and `UNATTENDED_EXPECT` recount, verified by `sed -n 382,391p`, an awk key count over lines 438-746 (31), and a Read of `_check_p2_set` at `:1556-1565`.
- Five-pin consistency across sections, verified by a grep for `RULE_PHRASES|NEVER_AS_WORKER|UNATTENDED_COMMANDS|all_seven|every_listed` in DESIGN, which exposed DESIGN:970 naming four test edits (N-1).
- Cadence, verified by reading `WORKER-CONTRACT.md:95` and `:110` and grepping DESIGN for "every wake|once every|cadence".
- Deviation and open-item totals, verified by reading the tables and counting rows (9 and 23).
- Line anchors, verified one by one with `sed -n` against the test file, contract, `main.py`, docs and SPEC (C12 to C15).

**Confidence:** Verified: 18/18 | Unverifiable: 0 (commit ids not checked against git, see constraint note; they are not numbers the lens recounts) | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 10 | Grep: 9 | Glob: 0 | Bash: 17. Tool calls exceed the 18 checks only through batched spot checks; each call maps to a check above. One stray no-op Edit call against `/dev/null` was made by mistake and changed nothing.

Skeptic's note: 0 numeric defects in the headline recount would be suspicious, so I looked for stale counts left by the R4 re-anchor. One was found (N-1). The remaining numbers were each checked against a file, not against an earlier QA report.

---

Verdict: FAIL

Blocking count: 1
