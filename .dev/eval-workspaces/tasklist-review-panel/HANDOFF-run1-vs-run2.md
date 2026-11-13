# Hand-off report: run 1 vs run 2 comparison

Date: 2026-11-13. Same brief both times (the `/tech-research` hand-off prompt for unifying the tasklist Review Panel with reflect Tier 2).

| | Run 1 | Run 2 |
|---|---|---|
| File | `HANDOFF-review-panel-unification.md` (commit 4a22d7421) | `HANDOFF-review-panel-unification-run2.md` |
| Session model | Tier 1b (Sonnet 5.5) orchestrator | Tier 1a (Opus 5.5) orchestrator; all agents pinned to Opus |
| Method | 3 read-only investigation agents; the orchestrator wrote the report with the whole session's context | 3 new read-only investigation agents and a new writer agent, none of which could open run 1's report or notes. The orchestrator did not write any of run 2's text; it only corrected one wrong date |
| Full tech-research task-file machinery | No | No (same method, so model and independence are the main differences) |
| Length | 315 lines | 544 lines |
| Evidence notes | `handoff-notes/run1/` | `handoff-notes/run2/` |

## 1. Verdict

**Use run 2 as the main hand-off.** It is longer and more precise, and it catches four facts run 1 got wrong or missed, two of which change the unification plan (rows 1 and 2 below). Run 1 has a few points run 2 dropped (section 4). Each claim below was checked against the source.

## 2. Where run 1 was wrong or missed something important (checked on 2026-11-13)

| # | Topic | Run 1 said | Run 2 said | Check | Impact |
|---|---|---|---|---|---|
| 1 | Master has moved | Branch changes no product code (true) and treated the branch-base code as current | Branch is 11 commits behind origin/master. **d2d8a2d16 (#519, "Stage 0-2 of the Tier 2 review panel")** and 167184c6b (#518, tier decisions) changed 40 files under `src/superclaude/cli/review` and `tests/review` (+8,026 lines): `findings_v2.py` (same 12-200 anchor limits), `cluster.py`, `hard_exclude`/`strict_distinct`, reflect panel templates | Confirmed: `git log HEAD..origin/master`; `git diff --stat ec259f1b7 origin/master -- src/superclaude/cli/review tests/review` = 40 files, +8,026 | **High.** The reflect Tier 2 panel the other session is merging with already landed on master on top of this code. Run 1's defect list cites line numbers that are stale on master, and it never mentions that master's `findings_v2.py` keeps the anchor limit (the largest measured loss). |
| 2 | Where tasklist review runs today | "No tasklist review step exists in sc-tasklist or sc-workflow" (run 1 D14) | Tasklist review runs through reflect: sc:workflow Wave 4 runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` (advisory); sc-tasklist Stage 10.5 runs `/sc:reflect --mode pre --remediate` per phase | Confirmed: `sc-workflow-protocol/SKILL.md:60, :76`; `sc-tasklist-protocol/SKILL.md:1630` | **High.** Run 1's search only looked for `superclaude review`. The "no regression" baseline is reflect UC-1, which is advisory, not "no review at all". Run 2 turns this into requirement U11 and open decision DO4. |
| 3 | Audit summaries | "outputs in audit-A..F (summaries in summary.md)" | Only audit-A and audit-D have a `summary.md`; B, C, E, F hold scripts and `flags.tsv`, and their conclusions live in COMBO-REPORT lines 290-298 | Confirmed: `ls analysis/audits/*/summary.md` gives 2 files | Medium: a reader following run 1 would look for four files that do not exist. |
| 4 | Helper scripts committed in 4a22d7421 | "Only files that reference this eval were copied" | `snap.py`, `drift-b3.py`, `rlog-r3.sh` belong to a different eval (`brainstorm-reflect-panel`), and `snap.py` writes into that other worktree | Confirmed: `grep -l brainstorm-reflect-panel tools/tmp-scripts/*` gives those 3 files | Low-medium: the filter in run 1 matched them on a shared path string. They are harmless as files, but `snap.py` must not be run from here. |
| 5 | Run-reviewer harness bugs | Described the ladder as fixed | Three open bugs: `expected_model` is overwritten on fallback, so the identity check cannot see a ladder swap; attempt files overwrite each other across fallback models; `BLOCK_OK` only checks the fence line, never parses it | From run 2's reading of `run-reviewer.sh:57-87`; not re-checked line by line here | Medium for anyone reusing the harness. |
| 6 | Raw-file count | 3,041 untracked files, "about 1.48 GB" | Same 3,041, but `RAW-TRANSCRIPTS-NOT-COMMITTED.md` says 2,916 raw files; the two counts do not reconcile; per-attempt meta files are also uncommitted, contrary to that note | Not re-checked | Low; an open housekeeping item. |
| 7 | Reproducibility | Not raised | Several committed analysis scripts read or `exec` copies in `/tmp` (`final-table.py`, `three-way.py`, `b9-table.py`, `doubles.py`, `issue-setup.py`), so the numbers cannot be regenerated from the commit alone | From run 2 (H10); not re-checked | Medium. |
| 8 | Test count | 299 passed, with a self-contradicting per-file count | 304 passed (13 files, 159 functions, 304 collected), per-file table | Run 2's command includes `test_review_brief_placement.py`, which run 1 left out | Low; run 2 is the more complete run. |

## 3. Where run 2 adds depth run 1 lacked

- **Retractions table** (run 2 section 2.3): every number that must not be reused, including the corrupted-judge "8/14, 5/8" headline that run 1 never named.
- **Merge defects split finer:** chaining and ref-mismatch splitting are separate (D4, D5). Missing-anchor rows are counted (46, 13 blocking), and a clearing defect is found (D3, the docstring contradicts the code). A single re-review reviewer can downgrade a blocker (D9), and `merge` always exits 0 (D12).
- **Panel facts:** gateway resolution picks duplicate models in 26 of 40 `@live7` run ids. The gateway `launch` map is empty. muse-ember (the default panel's model) is missing from the tier data. So the product panel cannot launch the recommended panels today (P1-P5, K5).
- **Brief versus parser:** the brief states the 200-character anchor limit, yet luna, ember and wonder still broke it, so an instruction alone does not fix the drop. The claim, refs, id and MINOR-blocking limits are not in the brief at all (B-2).
- **18 numbered requirements** (U1-U18) with must and should levels, including a regression benchmark target (ember + 2x luna: 1.83/14, 0.17/8, 1.83 wrong blockers, 0.83/2, ~64k tokens).
- **Decision log with dates** (DM1-DM18) and 11 open decisions with owners.
- **Questions aimed at master's #519 code** (Q1-Q3): does `findings_v2` still drop whole findings, does `cluster.py` chain, do `hard_exclude`/`strict_distinct` fix duplicates.

## 4. What run 1 has that run 2 dropped or weakened (keep these)

| Item | Run 1 location | Status in run 2 |
|---|---|---|
| `lint_cmd` and `estimate_cmd` are registered but missing, and the `ModuleNotFoundError` is swallowed (`__init__.py:19-32`) | Run 1 D13 | Not in the report (it is in run 2's panel notes) |
| The review-ledger skill, the `spec-panel-ledger`/`-stoprule` commands and the `finding-grader` agent exist only as experiment copies under `.dev/experiments/346-validation/phase5/final-bundle/builds/` | Run 1 D14 and Q7 | Not in the report |
| A one-table model-by-role summary (sonnet, luna, ember, haiku, grok, terra/sol, glm, Qwen, wonder, never-run models) | Run 1 section 2.3 | Spread across run 2's R14-R18 and R20; no single table |
| The pilot's fixed decision rule and its result (only arm C passes, by one defect) | Run 1 R5 | Run 2 R12 gives the efficiency figure, not the rule outcome |
| The "missing-requirement is Medium by instruction but may be blocking in the schema" conflict | Run 1 D9 | Run 2 covers severity conflicts (B-3) but not this one specifically |

## 5. Agreement (both runs, independently)

Both runs agree on the following:

- **Ceiling:** about 2-2.5 of 14 defects for every panel.
- **Panel guidance:** default ember + 2x luna; sonnet + 2x luna as an optional quality tier only; haiku + 2x luna best on real blocking.
- **Biggest loss:** the 200/300-character drop at merge (49 blocking findings lost, 4 verdict flips).
- **Source-blind reviews:** 156 of 665 runs never opened source.md, because the brief names no source document.
- **Merge design:** one reviewer's `blocking` flag decides the verdict, with no calibrator in this panel, unlike reflect.
- **Tasklist ids:** `T01.02` is lost as a reference.
- **Duplicates:** `distinct_across_slots` falls back to duplicate models silently.
- **Telemetry:** defined but written by nothing in the product.
- **Product code:** this branch changes none of it.

## 6. Recommended action

Hand the other session **run 2** (`HANDOFF-review-panel-unification-run2.md`) together with section 4 of this file. Before planning, it should re-check run 2's D1-D13 and P1-P7 against origin/master (#519), because both runs cite the old branch-base code. Separately, `tools/tmp-scripts/snap.py`, `drift-b3.py` and `rlog-r3.sh` belong to another eval and could be removed from this folder. That is a deletion, so it waits for the owner.
