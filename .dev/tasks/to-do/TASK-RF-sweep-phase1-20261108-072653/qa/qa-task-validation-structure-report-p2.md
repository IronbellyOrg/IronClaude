# QA Report: Task Integrity, Structure Lens (Partition 2 of 2: Phases 8 to 14 and Task Log)

**Topic:** TASK-RF-sweep-phase1-20261108-072653
**Date:** 2026-11-08
**Phase:** task-integrity
**Lens:** phase-structure
**Fix cycle:** N/A
**Fix authorization:** false (report only)

[PARTITION NOTE: Cross-file checks limited to Phases 8 to 14 and the Task Log. Phases 1 to 7 are read only where needed to check dependency order.]

---

## Overall Verdict: FAIL

Two IMPORTANT findings (missing `### Follow-Up Items` section; Phases 11 and 12 have no QA gate under a PER_PHASE requirement). Ten MINOR notes.

## Sources read

- Task file lines 1-205 (frontmatter, Execution Context, QA Gate Protocol) and 1265-2479 (Phases 8 to 14, Task Log), in chunks of at most 160 lines.
- `BUILD-REQUEST.md` (full).
- `docs/designs/orchestrator-mode.md:898-942` (section 15.2 step table) and `:705-714` (section 10).
- `research/09-gap-fill.md` Gap 5 (gate sizing, lines 176-224).
- `~/.claude/templates/workflow/02_mdtm_template_complex_task.md` (Task Log sections, lines 1445-1512).
- `~/.claude/skills/task-builder/SKILL.md:2215-2234` (canonical POST runner arm).
- Cited anchors re-read: `WORKER-CONTRACT.md:23,110,271,273,275`; `main.py:561-569`; `HOW-WE-WORK.md:318-337,396,403-404`; `docs/user-guide/commands.md:105-116`; `CHANGELOG.md:5,7,19`; `.gitignore:248-262`; `tests/skills/test_worker_contract.py:25,86-92,165-173,382-391,438,912,1322`; `pytest_plugin.py:216-222`; `pyproject.toml:117-121`; `recommend/__init__.py:12-20`; `test_conflict_scripts.py:46,48,63`; developer guide `:991`; `test_routing_plugin_parity.py:38`; `tests/recommend/test_routing_refresh.py:25-40,615-660`; `tests/core/test_how_we_work_routing_table.py:20-60`. All matched the task's citations.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Implementation order follows DESIGN 15.2, step dependencies hold | PASS (1 MINOR) | Task order 1.1 (8.2), 1.2 (8.3), 1.3 (8.4), 1.4a (8.5-8.9), 1.4 (8.10), 1.5 (8.12), 1.6 (9.1), 1.7 (9.2), 1.8-1.13 (10.1-10.7), 1.14-1.16 (11.1-11.3), 1.20 (11.4), 1.17-1.19 (12.1-12.3), 1.24a (12.4), 1.22/1.21/1.23/1.24/1.24b (13.1-13.6), 1.25-1.29 (14.1-14.8) matches every "Gate before the step" cell at DESIGN:906-940. The step 1.4a test (8.9) comes after its fakes (8.8). R5 (11.4) comes after `sweep.md` (11.1): see M1. |
| 2 | Validation item after each implementation phase | PASS (1 MINOR) | 8.13, 9.4, 10.8, 11.5, 12.5, 13.8, 14.1-14.5. The live check 9.3 runs before 9.4: see M2. |
| 3 | Testing items name test files and commands | PASS | 8.9, 10.2-10.7, 11.3, 11.4, 13.3, 13.4 each name the file and a `uv run pytest <file> -v` command with a saved output path. |
| 4 | QA gates follow M3 with I19/I22 full counts; final >= 10; fidelity reads source and output | FAIL | Sizes: impl-core 7, impl-cli 7, tests 7, docs 8, final 10 (14.10-14.19), fidelity 4 (14.29-14.32) reading DESIGN, SPEC and the inventory files; 1 fix agent and 2 verifiers per cycle; 2 cycles. All inside research/09:224. But Phases 11 and 12 have no gate: see I2. |
| 5 | Anti-orphaning final order, no Post-Completion section | PASS | 14.42 summary, 14.43 diff file, 14.44 POST reflect (penultimate), 14.45 Done (last). `grep 'Post-Completion'` in the task file: no section. |
| 6 | POST reflect is the skill-mode dedicated-subagent form, completion contract, no `--executor-model`, no handoff or HALT form | PASS | 14.44 runner prompt equals `task-builder/SKILL.md:2223-2231` with only the documented substitutions (`--diff` filled per OQ-12). `--executor-model` appears only in the "Do NOT pass" sentence. EV-3 on-disk check and depth/tier floor present. |
| 7 | Task Log has Open Questions (OQ-n), Execution Log, Phase Findings, Follow-Up Items | FAIL | Open Questions OQ-1 to OQ-14 (2455-2470), Execution Log (2389), Phase 1-14 Findings (2397-2451) present. No Follow-Up Items section: see I1. |
| 8 | TB-Add-1: no TBD, TODO, FIXME | PASS | `grep -nE '\bTBD\b|\bTODO\b|\bFIXME\b'`: hits only at lines 285-1003 (Phases 2 to 6), all quoted grep targets inside checks, none in 1265-2479. |
| 9 | TB-Add-4: dependencies are a DAG | PASS | Forward mentions (8.5 to 8.10, 8.8 to 10.1, 8.9 to 10.4) are hand-off notes, not back-edges; loop-backs (9.3 re-run, 13.4 re-copy, 14.1-14.5 re-runs) re-execute earlier items and do not depend on later ones. |
| 10 | TB-Add-5: multi-file items split | PASS (1 MINOR) | Most items touch one file. 10.1 and 12.3 are compound: see M8. |
| 11 | TB-Add-6: `Verify:` prefix throughout | PASS | 153 items in Phases 8-14 (29+20+24+5+5+25+45), 153 Verification fields, all start `Verify:`. Only off-form line in the file is 998 (Phase 6, out of this partition): see M10. |
| 12 | TB-Add-8: code-citing Context has `file:line` or evidence-absence comment | PASS (1 MINOR) | Code-editing items cite `file:line` (verified above). `evidence-absence` count in the file is 0, so items creating new files or naming modules without lines carry neither: see M7. Citation format is minor. |
| 13 | Item count sensible for scope | PASS | 153 items over 7 phases; the bulk is the gate machinery that QA_INTENSITY full and the BUILD-REQUEST require (one agent per item). Implementation items are one per file. |

## Summary

- Checks passed: 11 / 13 (5 of them with MINOR notes)
- Checks failed: 2
- Critical issues: 0
- Important issues: 2
- Minor issues: 10
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I1 | IMPORTANT | Task Log, task file 2387-2479 | No Follow-Up Items section. Template 02 requires `### Follow-Up Items Identified` (`02_mdtm_template_complex_task.md:1506`) and its Post-Completion check logs gaps there (`:1429`). Real follow-ups exist but are stranded in Notes and OQ text: the WC-9 lock retry (IronbellyOrg/IronClaude#446, line 2474), the branch (b) master-contract fix PR for `WORKER-CONTRACT.md:110` (OQ-1, line 2457), and opening the PR via `/sc:pr-submit --monitor 3` (line 2475). | Add `### Follow-Up Items Identified` with those three entries in the template form (`[Priority] description - Identified in Step X.Y`), and have 14.42 copy any new follow-ups there. |
| I2 | IMPORTANT | Phases 11 and 12 (1792-1872); Key Constraints gate folder list (line 156) | BUILD-REQUEST line 30 sets `QA_GATE_REQUIREMENTS: PER_PHASE`, but Phases 11 and 12 end at their validation items with no gate; the docs gate (13.9-13.25) reviews them only after Phase 13 has built on them. Item 13.1 writes the R2 bullet that cites WC-16, so a WC-16 defect found by 13.11 forces rework in both phases. | Smallest fix: merge Phases 11 to 13 into one phase ("Command, skill, contract and routing surface") so the existing 8-agent docs gate is that phase's gate. Otherwise add a gate after Phase 12 covering 11 and 12 with its own `qa/<gate>/` folder. |
| M1 | MINOR | 11.4 (line 1817) | Routing row R5 (`_POST_REFRESH_ADDITIONS`) lands three items after `sweep.md` is created (11.1). `active` comes from the frozen fixture (`test_routing_refresh.py:646`), so adding `"sweep"` early is harmless, while in the 11.1-11.3 window `tests/recommend` is red. No item in that window runs it, so no false result follows. | Move 11.4 to right after 11.1 (DESIGN gate "1.14 before 1.20" still holds). |
| M2 | MINOR | 9.3 (line 1490) | The live check runs `superclaude sweep run` against the real repo before the Phase 9 lint and tests (9.4) and before the `_publish` tests (10.7). A 9.4 failure forces a second live run that needs the OQ-8 Run to still exist. | Put 9.3 after 9.4. |
| M3 | MINOR | 14.29-14.41 vs 14.28 | The fidelity gate runs after the final gate has passed. Fidelity fixes (14.34, 14.38) re-run 14.1-14.5 only, so a fidelity fix can reopen a final-gate finding without any final-gate lens seeing it; only the POST reflect catches it. | State that a fidelity fix touching code re-runs the final-gate lens agents whose inputs it changed, or run the fidelity gate before the final gate. |
| M4 | MINOR | 14.6-14.7 | The OQ-10 pipx decision request is first raised in Phase 14, which adds a second human HALT late in the run. | Record the OQ-10 request in Phase 7 with the other owner decisions; keep 14.8 as the run step. |
| M5 | MINOR | 14.45 (line 2378) | The action ticks the item before running `git add .dev/tasks` and its verification, and it adds no completion line to `### Execution Log` (template `:1445`). It also sets Done without checking that no `phase-outputs/plans/OQ-*-decision.md` still says `status: PENDING` (earlier HALT items gate this, so the risk is low). | Run `git add .dev/tasks` and the checks first, append the Execution Log line, add a `grep -L 'status: RESOLVED'` check on the OQ files, then tick. |
| M6 | MINOR | 14.12 (line 2138) | The validation-evidence lens tells a report-only agent to re-run pytest and ruff "read-only in effect"; both write caches (`.pytest_cache`, `__pycache__`, `.ruff_cache`). | Reword to "writes only tool caches and your report". |
| M7 | MINOR | 8.7, 8.11, 9.7, 13.13, 14.2, 14.18 | TB-Add-8: these Context fields name code surfaces (a new file, `probes.py`, `commands.py`, `src/superclaude/cli/issue_watch/`) with no `file:line` and no `<!-- evidence-absence: ... -->` comment; the file has 0 such comments. | Add `<!-- evidence-absence: new file, no source line yet -->` (or a `file:line`) to each. |
| M8 | MINOR | 10.1 (line 1622), 12.3 (line 1851) | TB-Add-5: 10.1 extends `conftest.py`, adds fixture files and edits `SOURCES.md`; 12.3 makes five pin edits plus a conditional `WRITE_VERB_CLASSIFICATION` row and a test run in one paragraph. | Split 10.1 into conftest and fixtures items; split the classification grep and row out of 12.3. |
| M9 | MINOR | 8.6 (line 1305) | The Context says the sprint-state block is `.gitignore:250-254`; on disk `.dev/pr-monitor/` is line 250, and the sprint-state block runs 252-257 (`.dev/e2e-reflect/**/sprint-state/` at 257). Inserting after 254 splits that block. It follows DESIGN section 10 ("line 254"), so behaviour is fine. | Correct the range to 252-257; optionally insert after 257 and note the deviation. |
| M10 | MINOR | line 998 (Phase 6, partition 1) | `Verification: Verify on branch (b):` breaks the `Verify:` prefix form. Reported here for the partition-1 reviewer. | Reword to `Verify: on branch (b), ...`. |

## Actions Taken

None. fix_authorization is false; the task file was not edited.

## Recommendations

- Resolve I1 and I2 before running `/task`; both are small edits to the task file.
- Apply M1 and M2 in the same pass; each is one item move.

## Confidence Gate

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 12 | Grep: 4 | Glob: 0 | Bash: 7 (one batch script of 15 read-only blocks, BATCH_OK)
- No web research was performed.

## QA Complete

VERDICT: FAIL
