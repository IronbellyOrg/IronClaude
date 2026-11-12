# Research Cross-Validation Report (completeness-verification, cross-validation lens)

**Topic:** Task-builder track 1, issue #339 Phase 1 (orchestrator mode), design fixes R3-B1, R3-B2, R3-B3
**Date:** 2026-11-08
**Files analyzed:** 01-file-inventory.md, 02-patterns-conventions.md, 03-integration-points.md, 04-design-fixes-r3.md, 05-test-verification.md, 06-template-examples.md
**Status:** Complete

---

## Files read

All six assigned files were read in full (01: 354 lines, 02: 169, 03: 120, 04: 232, 05: 157, 06: 164). Each has `Status: Complete` and a Summary section. Disputed claims were spot-checked against the repo (Read, Grep, Glob, one read-only batch script).

## Overlap checks requested in the prompt

| # | Overlap | Files | Result | Repo evidence |
|---|---|---|---|---|
| O1 | Line anchors | 01 vs 03 | AGREE. Every shared anchor matches: `WORKER-CONTRACT.md` :23, :61, :154, :156, :158; `HOW-WE-WORK.md` :318, :333, :335, :337, :396, :403, :404; `commands.md` :105, :115, :116; developer guide :991; `.gitignore` :254 (01 says :255-257 "follow with the e2e-reflect entry", 03 says they "continue the sprint-state block": same fact); `test_how_we_work_routing_table.py` :24 markers, :27-40 set; `test_routing_refresh.py` :33, :648 | Verified: `WORKER-CONTRACT.md` grep hits at 23, 61, 154, 156, 158; `.gitignore:254` `.dev/sprint-state/`, :257 `.dev/e2e-reflect/**/sprint-state/`; `test_how_we_work_routing_table.py:24` `_OTHER_BEGIN`, :27-40 set with `sc:spawn` at :33; `test_routing_refresh.py:33`, :647-648 |
| O2 | `test_worker_contract.py` never-as-worker test name and list count | 03 vs 05 (and 01) | Name and count AGREE (`test_never_as_worker_list_names_all_seven_commands` at :545; `NEVER_AS_WORKER` :245-254 has 8 entries, 9 after the append). DISAGREE on two points: (a) the set of pins to edit (finding B-1 below), (b) whether the rename is required (minor m1) | Verified `tests/skills/test_worker_contract.py:86-92`, :155, :245-254 (8 entries, `/sc:pr-submit` last), :545, :865; design :677-680 |
| O3 | CHANGELOG heading format | 01 vs 03 | AGREE. Both say `[Unreleased]` uses `### <title>` + `#### Added (<topic>)`, not a bare `### Added`, and both recommend following the file over design :701 | Verified `CHANGELOG.md:5` `## [Unreleased]`, :7 `### ccsession: ...`, :9 `#### Fixed (...)`, :19 `#### Added (...)`, :33 `#### Added (...)`; design :701 says "One `### Added` entry" |
| O4 | Permission syntax in `allowed-tools` | 02 vs design 7.6 | AGREE. 01 B8 and 02 8.1 quote the design literal `Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*), Read` (design :652); design :657 says the test asserts "the two `allowed-tools` literals exactly". 02's house-style note is accurate: in `src/superclaude/{commands/*.md,skills/*/SKILL.md}` the colon-star form appears only in `commands/help.md:6`; every other `Bash(...)` uses space-star (`graph.md:9`, `sc-swarm-wizard-protocol/SKILL.md:7` and others). 02 recommends keeping the design literal or changing design and test together. No contradiction | Grep over commands and skills; design :652, :657 |
| O5 | `tests/sweep/__init__.py` need | 05 (vs 01) | 05 claim VERIFIED: `tests/cli/test_cli_registration.py` exists and `tests/cli/__init__.py` does not, so a `tests/sweep/test_cli_registration.py` without a package `__init__.py` collides by basename. 01 counts "Seven new files under `tests/sweep/`" from design :726 and defers the question to 05. Adding `__init__.py` makes 8, a small design deviation (minor m4) | Glob: only `tests/cli/test_cli_registration.py` matched; `tests/cli/__init__.py`, `tests/commands/__init__.py`, `tests/sweep/` absent |
| O6 | Step 1.4a ordering | 01 vs 05 | Mostly AGREE. Design :911 puts 1.4a (gate 1.2, "The first code commit") before 1.8 (:916, conftest). 01 flags that `test_readonly.py` at 1.4a precedes `conftest.py` (1.8) and `collect` (1.4). 05 hedges ("with 1.8, or with 1.4a if that step lands first") and maps the 1.4a argv test to `patch_git` from the 1.8 conftest without noting that it does not exist yet (minor m5) | Design :908-917 |
| O7 | Review-3 line shift | 04 | VERIFIED as a uniform +6. Review 3 cites line 54 (now 60, GQ-103(3)), 449 (now 455, `OrcaObservation`), 451 (now 457, `TranscriptTail`), 488 (now 494, "A path-B join therefore also needs session identity"), 733 (now 739, "four incomplete cases"), 1005 (now 1011, cycle 2 `R2-B1` row; `### Fix cycle 2` heading at 1005) | `orchestrator-mode-review-3.md:9-11, 42-44`; design :60, :455, :457, :494, :739, :1005, :1011 |

## Blocking findings

### B-1. The pin set for `tests/skills/test_worker_contract.py` conflicts across 01, 03 and 05 (conflicting count; 01 and 05 are wrong)

- **03 (IP-2, "DESIGN GAP")** says five edits are needed: the design's four (design :677-680) plus `RULE_PHRASES["never-as-worker"]` at :86-92, whose phrase at :89 pins the old line-23 text word for word.
- **01** lists only the design's four. C11 table (no row for :86-92), D table row 1.19 "lines 155, 254, 545, 865", and the edit count "`test_worker_contract.py` 4". 01 calls its D table "Checklist-ready".
- **05** section 6 and the section 10 row for step 1.19 also name only `NEVER_AS_WORKER` and `RULE_PHRASES` (WC-14).
- **Code check (03 is right).** `tests/skills/test_worker_contract.py:86-92` is `"never-as-worker": ("**Never-as-worker list**", ["`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, " "plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers"])`. The new line 23 at design :684 reads "`/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`", so the old phrase no longer occurs and `test_contract_states_rule[never-as-worker]` fails.
- **Why blocking.** A builder working from 01's checklist-ready table, or from 05's test map, writes a step 1.19 that leaves a failing test. The edit counts are a false claim against the code.
- **Fix.** In 01 C11, the D table row 1.19 and the edit counts, and in 05 sections 6 and 10, add the :89 phrase edit as the fifth pin. Change it to "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, " (03 IP-2). Note it as a deviation from design section 8, which lists four pins. It lands in the same step as the line-23 edit (or the step right after it, with no test run in between).

## Minor findings (do not cause FAIL)

- **m1. Rename required or optional.** 05 section 6 calls renaming `test_never_as_worker_list_names_all_seven_commands` "optional". Design :679, 01 C11 and 03 IP-2 make it a required edit. Follow the design.
- **m2. Step grouping for green intermediate tests (01 vs 03).** 03's ordering constraints want WC-14, line 23, all pins and R7 in one step. They also want R5 to land no later than the step that creates `sweep.md` (1.14), and R1 + R4 + R3 in one commit. 01's D table follows the design's split (1.17 / 1.18 / 1.19; 1.20 after 1.14, design :929; 1.22 after 1.21, design :931). 01 C6 also explains 1.20's gate as "This is why 1.20 is gated on 1.14 (`sweep.md` existing)". That gets the dependency backwards. `test_routing_refresh.py:647-648` passes with `"sweep"` added before `sweep.md` exists (a set difference with a non-member), and it FAILS from 1.14 until 1.20 lands. The design only runs the full suite at 1.27 (design :938), so the split is legal. But any per-step test item (06 L3, 05 section 11) run inside those windows fails. The builder should merge the steps as 03 says, or keep those tests out of the windows.
- **m3. Test location.** 02 section 9 names `tests/cli/sweep/`. Design section 11, 01 and 05 use `tests/sweep/`. 02 marks its own choice as inferred. Use `tests/sweep/`.
- **m4. `tests/sweep/__init__.py`.** 05 is right that it is needed (O5). It makes 8 new files, not the "Seven" at design :726, so record it as a design deviation. 05's "with 1.8, or 1.4a if that step lands first" should be settled: in the design table, 1.4a (:911) comes before 1.8 (:916), so it is created at 1.4a.
- **m5. 1.4a test fakes and discovery.** 01 B9 flags that 1.4a's `test_readonly.py` needs recording fakes before `conftest.py` (1.8), and per-worktree discovery before `collect` (1.4). 05 section 10 maps the 1.4a argv test to `patch_git` "above", which is the 1.8 conftest. Neither file resolves this. The builder must choose: local fakes inside `test_readonly.py` at 1.4a, or move the per-worktree assertion to 1.11.
- **m6. Drift-test template.** 02 8.5 models `tests/commands/test_sweep_command.py` on `test_graph_command.py`, and 05 section 6 on `test_impact_command.py`. The two are compatible (same helper shapes). Pick one.
- **m7. Step count.** 06 section 2 says "steps 1.1-1.28 from design section 15". The design table runs to 1.29 (:940), plus 1.0a, 1.0b, 1.4a, 1.16a, 1.24a and 1.24b (01 D table). Use 01's list.
- **m8. 01 interfaces are pre-R3.** 01 B2 (`OrcaObservation`, `TranscriptTail`) and B4 (the `read_transcript_tail` comment) copy the design as it stands today. 04 R3-B1 adds `dispatch_started`, `dispatch_ended`, `dispatch_status` and `first_record_ts`, the UTC parse rule and a new comment. Because the R3 fixes run first, the code items must cite the fixed design, not 01's copy.
- **m9. R3-B1 gate before R3-B2 edit (04 vs 06).** 06 section 11 orders B1 edit, B1 gate, B2 edit, B2 gate. 04 R3-B1 edit 4 drops the transcript outcome ("and that transcript is None with the same note") and adds "Several matching rows follow the R3-B2 rule below". The transcript outcome for that case is then restored only by the R3-B2 edit. The B1 gate prompt should say that the B2 rule follows. Otherwise B1 reviewers may flag a missing outcome, or a forward reference to a rule that is not there yet.

## Checklist

| # | Check | Result |
|---|---|---|
| 1 | Findings about the same files and APIs agree | Mostly yes. One disagreement on the pin set (B-1) |
| 2 | No contradictory claim between files | One blocking contradiction (B-1). Minor ones: m1, m2, m3, m6, m7 |
| 3 | Shared dependencies documented the same way | Yes for `main.py` registration (01 C1 = 02 section 1, identical text), the lazy `__getattr__` (01 B1 = 02 section 2), `_publish` in `commands.py` (01 B6 = 02 section 7), the `integration` marker (01 C12 defers to 05, and 05 verifies `pyproject.toml:119`), and the four real-git assertions (01 B9 = 03 IP-6 = 05 section 8) |
| 4 | Integration-point descriptions match | Yes for R1-R8 anchors and the `.gitignore` placement. The step grouping differs (m2). 03 IP-3 (write-verb audit) appears only in 03, with no conflict |

## Gap list

1. B-1: add the `RULE_PHRASES["never-as-worker"]` phrase edit (`tests/skills/test_worker_contract.py:89`) to 01 (C11, D row 1.19, edit count 4 to 5) and to 05 (sections 6 and 10), and mark it as a deviation from design section 8.

VERDICT: FAIL

