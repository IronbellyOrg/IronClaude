---
mode: pre
tier: 1
claim_class: static_defect
evidence_class: source_static
verdict_direction: AFFIRM
self_reported_confidence: 0.80
spec: .dev/tasks/to-do/TASK-WF-design-20261126-162939/source.md
tasklist: .dev/tasks/to-do/TASK-WF-design-20261126-162939/TASK-WF-design-20261126-162939.md
---

# T1 reflection card (UC-1, plan vs design)

## Scope and what was read

The plan has 8 phases and 38 tasks (`TASK-WF-design-20261126-162939.md:32` onward). Lines 1-150 (constitution, Phases 1 to 4 up to Task 11) were read line by line. Tasks 12 to 38 were checked structurally only (plan gate, a dependency-order script, design-term counts), not read line by line. The design (`source.md`, 529 lines) was read by section heading and by targeted Grep.

## Coverage map (Step 1B.0)

- Pass 1 (`ID_REGEX`, parsed): the only family it matches in the design is `T-nn` (the design's test ids): 27 distinct, 25 named somewhere in the plan, 2 not named (`T-14` at `source.md:407`, `T-18` at `source.md:458`). `coverage_pct` = 25/27 = 0.9259.
- Pass 2 (inferred rows): the design's own label families that `ID_REGEX` does not match: FR (122 distinct), NFR (18), DD (11), AC (21). Each row quotes the first design line that carries the id (`artifacts/coverage-pass1.json`). Ranges such as `FR-060..FR-063` were expanded. DD: 11 of 11 named in the plan. FR: 79 of 122. NFR: 10 of 18. AC: 7 of 21.
- Union: 132 of 199 ids are named in the plan text, `coverage_pct_union` = 0.6633, 67 unmapped. `inferred_count` (172) is larger than `parsed_count` (27), so the parse-density guard fires: `coverage_degraded: parsed-sparse`.
- Reading of the gap: most unmapped ids are cited only inside the design's summary rows (`source.md:15-19`, one row per component C1 to C5), the P7 row (`source.md:473`) and the traceability table (`source.md:517`). A term check of the design's mechanisms against the plan found every major mechanism named in the plan (Q8a, R0, L0, commits.md, stage-plan, check-message, resolve-check, reconcile, snapshot, abandon, adopt, vcs_contract, E-RESUME-NEEDED, S23, sync-dev, DD-9, DD-10, DD-11). So the id gap is mostly "the plan does not cite the id", and only a semantic read of each design section can say whether any requirement has no task. That read is left to Tier 2.

## Candidate findings

F1 (Medium, may be blocking at implement time). Plan Constraint line 29 says "No code or text uses `--no-verify`, `-n` on commit, `SKIP=`, `commit-tree` or `--amend`" (`TASK-WF-design-20261126-162939.md:29`). Task 3 must write those strings into `FORBIDDEN_FLAGS` (`:60`), and later tasks quote them in acceptance checks (`:172`, `:193`). The implement protocol treats `## Constraints` items as global constraints whose breach, when the reviewer can quote the text, is a blocking `quoted-constraint-breach` (`src/superclaude/skills/sc-implement-protocol/SKILL.md:106`, `refs/qa.md:52`). A strict reviewer can read the deny-list as "text that uses `--no-verify`". Fix: reword line 29 to say no command or argv the code runs, and no recommendation in the primitives, uses them, and that deny-lists and tests of refusals are allowed.

F2 (Note). Declared dependencies are incomplete. Task 6 (`:88-90`) adds a verb to `vcs.py` and uses `vcs_plan.py` but depends only on Task 3; Task 8 (`:110-112`) wires a verb into `vcs.py` and depends on Task 7; Tasks 9 to 12 (`:122-124`, `:132-134`, `:142-144`, `:152`) extend `vcs_plan.py` (created by Task 4, `:66-68`) without depending on Task 4. `vcs.py` is created by Task 5 (`:77-79`). `/sc:implement` ignores `depends-on` and runs source order unless a set is marked `independent` (`SKILL.md:92`, `:110`), and the plan marks none, so execution is unaffected. Script output: `artifacts/dependency-check.txt` (other lines in that file are the ambiguous name `SKILL.md` and forward mentions of files a task only links to, not defects).

F3 (information). Open items O1 to O7 (`source.md:519-529`) stay open by design; the plan does not resolve O1 (DD-11 reading) and says so in the design, so Task 12 and the T-22 test depend on the owner's reading.

## Risk surface

Blast radius the plan names and covers: the pinned STOP-table format test and the "No other `E-*` codes" sentence (implement `SKILL.md` and `tests/skills/test_task_workspace_lifecycle.py`), the write-verb scan and its classification rows, plugin byte parity, the routing row and fixture S23, and the unchanged-file rules for `archive_workspace.py` and `scripts/worktree_cleanup.py` (pre-check: `artifacts/codegraph-grounding.md`, 73 checks, all OK). Untested invariant: real hook-framework behavior (UNVERIFIED, handled by the emulator in Task 2).

## Recommendations

1. Edit `TASK-WF-design-20261126-162939.md:29` as in F1; success check: no sentence in the plan forbids text that Tasks 3, 14 and 16 must write.
2. Add `Task 4` to the `Depends on:` lines of Tasks 9 to 12 and `Task 4`, `Task 5` to Tasks 6 and 8; success check: `artifacts/dependency-check.txt` rerun shows no `NO-DEP-ON-CREATOR` row for `vcs_plan.py` or `vcs.py`.
3. Tier 2 should read each design section against the tasks (the qa reviewer has the whole design in its brief).
