# Refactoring Plan: merged reviewer card (UC-1 pre-execution review of TASK-WF-issueSummary-20261125-175231)

## Overview
- Base variant: Variant 2 (`variant-2-original.md`, reviewer 2, qa lens, opus class). Score 0.8193 against 0.7023 (`base-selection.md`).
- Incorporated: Variant 1 (`variant-1-original.md`): fix wording, the raw-resume Blocking (Missing) grade, the live-route wording, the F4 dismissal, the unresolved-link note; and the debate rulings of `debate-transcript.md` and the probe warnings of `invariant-probe.md`.
- Output: `../merged-review-card.md` (one level above this folder, the `adversarial/` folder). Merge log: `merge-log.md` (this folder).
- Change count: 20 planned (rows 1-13 as changes 2-14, header, adherence summary, notes sections); 5 rejected alternatives listed at the end.
- Risk: Low to Medium. The merged card is a review card (text); no repository file is touched.
- Path key to carry into the card: PLAN = `/home/coder/workspaces/worktrees/IronClaude/issue-765/.dev/tasks/to-do/TASK-WF-issueSummary-20261125-175231/TASK-WF-issueSummary-20261125-175231.md`; SPEC = `.../source.md` in the same folder; every other path is under `/home/coder/workspaces/worktrees/IronClaude/issue-765/`.

## Output shape (every change below fills one part of it)
1. Provenance comment block (as the adversarial skill's provenance rules require) and `# Reflect Reviewer — Merged Deviation Findings`.
2. Header lines: merged persona (analyzer + qa), total deviations 13, path key.
3. `## Deviations`: one table `| # | Category | Location | What diverged | Evidence (file:line) | Severity |`, Blocking rows first. Every row's "What diverged" starts with its grade prefix (`**Blocking (Decision):**`, `**Blocking (Missing):**`, `**Medium:**`, `**Note:**`) and ends with `**Fix:** <one sentence>`. Severity label: HIGH on Blocking rows, MEDIUM on Medium rows, LOW on Notes. Category is `Drift` on every row. Each row carries a `<!-- Source: ... -->` provenance tag placed on the line after the table row (HTML comments between table rows break the table, so put the tags in a `## Provenance of rows` list after the table instead).
4. `## Adherence summary`, `## Notes` (verdict, confidence, judge ruling, confirmed correct, not verified, probe warnings carried, reviewer metadata).

## Planned Changes

### Change #1: header and path key
Source: V2 header, lines 1-5 of `variant-2-original.md`. Target: top of the card. Approach: replace. Text: persona "merged: analyzer (V1, haiku class) and qa (V2, opus class)"; total deviations 13; keep V2's path key sentence. Risk: Low.

### Changes #2-#14: the 13 rows (final text below; copy, do not reword grades or file:line cites)

**Row 1** (source: V2 row 1, V1 row 4, C-001, U-001, INV-016, A-001; base row, rewritten) — Location `PLAN:76-77, PLAN:89` — Grade **Blocking (Missing)**, label HIGH.
What diverged: "The spec asks the implementer to 'Run the three targeted test files, the required broader regression/lint/format gates and sync checks' (`SPEC:32`). No task runs the full test suite (`make test`, which is `uv run pytest`) or the project lint gate (`make lint`, which adds `lint-architecture`). The plan runs the three named test files (`PLAN:76`), `uv run ruff check` and `uv run ruff format --check` (`PLAN:77`; the commands name no path, so they cover the whole project, but the criterion text says 'for the two changed test files'), and `make verify-sync` (`PLAN:89`). Affected action: the final checks of Tasks 4 and 5. Consequence: 21 test files mention ccsession (case-sensitive count; 24 case-insensitive) and only 3 run. One of the others, `tests/core/test_orca_session_launch_guidance.py`, pins the README's '### Orca session launches' section: required phrases, and the paragraph after `commands' internal Agent-tool subagents.` must start with 'Every Orca worktree gets an agent' and match `core/CLAUDE.md`. Task 5 adds a sentence to the Orca part of the README (`PLAN:85`). The break is conditional: a sentence placed in README lines 409-426 passes every plan check and fails the full suite; the safe zone is README lines 392-408. **Fix:** add `uv run pytest`, `make lint` and `uv run ruff format --check .` (never `make format`, which rewrites files) to Task 5's acceptance criteria after the README edit, each as 'no new failure compared with a baseline run before Task 2 at the recorded commit', and keep the README cross-reference in lines 392-408."
Evidence: `SPEC:32`; `Makefile:13-15`, `Makefile:48-50`, `Makefile:52-55`; `tests/core/test_orca_session_launch_guidance.py:15-16`, `:40-62`; `src/superclaude/skills/ccsession-tag/README.md:409-426`; `PLAN:77`.

**Row 2** (source: V1 row 1, V2 row 2, C-002, U-002, INV-014, INV-015, A-003) — Location `PLAN:98, PLAN:101, PLAN:22` — **Blocking (Missing)**, HIGH.
What diverged: "Task 6 reads the switch from a Claude process 'started through ccsession after the change', but no task puts the changed launcher where the live route finds it. `ccsession-orca` runs the `ccsession` that sits next to its own resolved path; the installer links `~/.local/bin/ccsession` and `ccsession-orca` to the installed skill copy; `make sync-dev` writes only this checkout's `.claude/`. Constraint `PLAN:22` says `wire_ccsession` 'copies the launcher unchanged'; it creates links (and copies `session-name.sh` and the env example). A plain `superclaude install` skips an existing skill folder; only `superclaude update`, `install --force`, `update.sh` or the skill's own `install.sh` replace it, and any of those changes every ccsession launch on the host (`update` also reinstalls core files, commands, agents, hooks and settings). Verified: the mechanism. Not verified: the installed launcher's current contents and the coordinator's Orca configuration. Consequence: completing Tasks 1-5 does not establish the prerequisite of Task 6's check; the executor would either fail it or run a host-wide refresh from an unmerged branch. **Fix:** before Task 6 collects evidence, record which launcher the process runs and show it contains the export, either by launching the checkout's launcher by absolute path or after an owner-authorised refresh that the plan names, and change `PLAN:22` to say `wire_ccsession` links the installed launcher."
Evidence: `src/superclaude/skills/ccsession-tag/ccsession-orca:44-54`; `src/superclaude/cli/install_ccsession.py:13-16`, `:56-57`, `:61-71`; `Makefile:109-111`; `src/superclaude/cli/install_skills.py:102-104`; `src/superclaude/cli/main.py:206`, `:402`; `src/superclaude/cli/install_skill.py:48`, `:52`; `src/superclaude/skills/ccsession-tag/install.sh:41`; `PLAN:22`.

**Row 3** (source: V2 row 3, C-005, INV-002, INV-003) — Location `PLAN:98, PLAN:101-102` — **Blocking (Decision)**, HIGH.
What diverged: "Criterion `PLAN:101` can be met by any Claude process started through ccsession 'in an existing terminal'. The spec asks for the coordinator's own process: 'the new coordinator process starts with the switch set' (`SPEC:7`) and 'Live coordinator Claude PID ... `/proc/<pid>/environ`' (`SPEC:31`); the analysis says to check the switch 'in its actual PID's initial environment and require `=1`'. Only the message check has a 'not run, partial' fallback (`PLAN:102`). Two further gaps in the same criterion: the `grep -x '...=1'` line also appears when the parent shell already held `=1`, so a live pass does not show the override works (only the unit tests do); and a coordinator started before the change shows no line, which is neither 'unavailable' nor a failure of the change. Consequence: two terminal launches, even of the checkout's launcher, satisfy `PLAN:101` while the real coordinator, for example one whose Orca command is plain `claude`, lacks the switch; this contradicts the Goal at `PLAN:15`. **Fix:** make `PLAN:101` require the exact switch line from the coordinator's own Claude PID after a fresh and a resumed coordinator launch that started after the change, with the PID, its start time and the launch route recorded, a `0` set in the launching shell for at least one launch so the line shows the override, terminal launches as supporting evidence only, and the same 'not run, partial' outcome that `PLAN:102` gives the message check."
Evidence: `SPEC:7`, `SPEC:31`; `.dev/issues/765/analysis/analyze-ccsession.md:25`; `PLAN:15`, `PLAN:98`, `PLAN:101-102`; `src/superclaude/skills/ccsession-tag/ccsession:2412-2416`.

**Row 4** (source: V2 row 5, U-003, INV-018) — Location `PLAN:60, PLAN:66, PLAN:26` — **Blocking (Decision)**, HIGH.
What diverged: "Task 3 says to extend the `_orca_env` fake 'record by the one variable'. That fake already records the sorted names of every environment variable (`env_names`), plus `base_url`, `topic`, `origin` and the arguments. Criterion `PLAN:66` ('only the one named variable is captured') and Constraint `PLAN:26` are therefore false for the test the plan prescribes. Names only, no secret values, so this is not a Safety finding. **Fix:** give the new wrapper tests their own fake Claude that writes `FAKE_CLAUDE_RECORD` with the arguments and the one switch only, passed as `CLAUDE_BIN` through `_orca_env`'s extra arguments, and leave the existing record untouched for the existing tests."
Evidence: `tests/unit/test_ccsession_tag.py:1833-1839`, `:1861-1875`, `:1988-1990`, precedent `:6156-6163`; `PLAN:26`, `PLAN:60`, `PLAN:66`.

**Row 5** (source: V1 row 3, V2 rows 12-13, C-004, U-006, INV-008, INV-011, INV-012) — Location `PLAN:60, PLAN:63` — **Blocking (Missing)**, HIGH.
What diverged: "The spec asks to cover 'untagged/raw-resume, labeled resume and new-label launches, both with and without an explicit model' (`SPEC:21`), and the analysis lists 'raw untagged resume arguments' as a test input. Task 3's six forms are print-mode untagged (`-p x`), labelled new and labelled resumed launches (`_LAUNCH_CASES`); none passes a raw `--resume <id>`, so the plan's 20-case check can pass without the spec-named input. Raw resume is how Orca resumes a coordinator (`ccsession-orca:90`, `:228-231`, `:263`, and the tab reopen at `:189`). The same exec lines carry the export, so protection is not in doubt; the missing item is the required coverage. Two conditions on the fix: raw-resume cases must not be appended to `_LAUNCH_CASES`, because `test_ccsession_tag.py:1489` asserts `('--resume' in launched) == transcript` over that list; and `PLAN:63` is an exact count (6 forms x 3 states + 2 wrapper cases = 20), so the total must be restated. **Fix:** add a separate raw-resume case list (`--resume <id>` with and without `--profile claude`, across the three starting states), make the wrapper's untagged case `--resume <id>` with no carried name and assert its record has no `--name`, and state the new total in `PLAN:63`."
Evidence: `SPEC:21`; `.dev/issues/765/analysis/analyze-ccsession.md:23`; `tests/unit/test_ccsession_tag.py:1465-1472`, `:1489`; `src/superclaude/skills/ccsession-tag/ccsession-orca:90`, `:189`, `:228-231`, `:263`; `src/superclaude/skills/ccsession-tag/ccsession:2447-2451`; `PLAN:60`, `PLAN:63`.

**Row 6** (source: V1 row 2, V2 row 4, C-003, X-001, INV-017; judge ruling) — Location `PLAN:46, PLAN:51-52` — **Medium**, MEDIUM.
What diverged: "Task 2 adds a header line 'near lines 143-154 ... so `ccsession --help` readers see it'. `show_help` prints the header from line 2 and stops at the line `# The wrapper always runs`, which is line 143, so a line placed in 143-154 never appears in `--help` and the stated reason is false. The only related check (`--help` exits 0, `PLAN:51`) cannot detect it. The advocates split on the grade (Blocking (Decision) versus Medium); ruling: Medium, because neither the spec nor the analysis mentions help output, no acceptance criterion reads it and no later task uses it. **Fix:** put the line above line 143 (the options block ends at line 136), add 'the `--help` output contains it' to the criteria, and carve it out of `PLAN:52` ('unchanged in behavior'); or drop the claim."
Evidence: `src/superclaude/skills/ccsession-tag/ccsession:143`, `:2270-2271`; `PLAN:46`, `PLAN:51-52`.

**Row 7** (source: V2 row 11, U-007) — Location `PLAN:33` — **Medium**, MEDIUM.
What diverged: "Task 1's route trace names only `ccsession-orca` lines 261 and 263. It leaves out the tab-reopen execs at lines 186 and 189, which Orca uses to relaunch a coordinator's tab after a restart; line 189 passes `--resume` into ccsession's untagged branch. Both still go through ccsession, so protection holds, but the scope record and the tests do not name them. **Fix:** add both execs to Task 1's trace and say they reach ccsession."
Evidence: `src/superclaude/skills/ccsession-tag/ccsession-orca:164-190`; `PLAN:33`.

**Row 8** (source: probe INV-009) — Location `PLAN:33, PLAN:38, PLAN:46` — **Medium**, MEDIUM.
What diverged: "Task 1's criterion says every cited `file:line`, including the six exec lines, 'matches the live file'. Task 2 inserts a comment and an export at `ccsession:2438-2440` (and a header line), which shifts every later line, so the artifact is true only when Task 1 finishes. **Fix:** cite the pre-change commit `a6fec24` or anchor each line by its text."
Evidence: `PLAN:33`, `PLAN:38`, `PLAN:46`; `src/superclaude/skills/ccsession-tag/ccsession:2438-2440`, `:2448`, `:2518`.

**Row 9** (source: probe INV-004) — Location `PLAN:89` — **Medium**, MEDIUM.
What diverged: "`make verify-sync` also calls `uv run python -c \"from superclaude.cli.install_hooks ...\"` and `jq`; if either is unavailable its prefixes come out empty and it sets drift regardless of this change, and it fails by design before `make sync-dev` has populated `.claude/`. The baseline clause in the fix to row 1 covers pytest, lint and format only. **Fix:** run `make sync-dev` and `make verify-sync` once before Task 2 and record the result as the baseline for Task 5."
Evidence: `Makefile:308-309`, `:329`; `PLAN:89`.

**Row 10** (source: probe INV-016) — Location `PLAN:77` — **Medium**, MEDIUM.
What diverged: "The criterion says `uv run ruff check` and `uv run ruff format --check` 'report nothing for the two changed test files', but the commands have no path, so any pre-existing finding elsewhere fails the check for a reason that has nothing to do with this change. **Fix:** either scope both commands to the two changed files or keep them repo-wide and compare with the recorded baseline."
Evidence: `PLAN:77`; `pyproject.toml:177-182`.

**Row 11** (source: V2 row 7, U-005) — Location `PLAN:89` — **Note**, LOW.
What diverged: "'`git status --short` shows no path under `.claude/`' cannot show whether ignored mirror files changed, because `.claude/*` is ignored except `settings.json` and a few cache paths. The real guard is `make verify-sync` in the same criterion. **Fix:** describe the status check as covering only files git does not ignore."
Evidence: `.gitignore:127-128`, `:130-135`; `PLAN:89`.

**Row 12** (source: V1 Notes, U-011) — Location `SPEC:37-38` — **Note**, LOW.
What diverged: "The relative links `analysis/analyze-ccsession.md` and `accuracy-check.md` in the copied spec do not resolve inside the task package; the originals are under `.dev/issues/765/`. **Fix:** copy them into the package or use paths that resolve from it."
Evidence: `SPEC:37-38`; `.dev/issues/765/analysis/analyze-ccsession.md:1`.

**Row 13** (source: V2 row 1, U-010, INV-007; correction) — Location `reviewer-2-card.md row 1` — **Note**, LOW.
What diverged: "Count corrections carried from the debate: the number of test files mentioning ccsession is 21 (case-sensitive) or 24 (case-insensitive), not 16 as one card said; it is supporting evidence for row 1, not an acceptance number. **Fix:** state the counting rule or drop the number from the finding."
Evidence: `tests/` (grep of `test_*.py`, orchestrator-run, 21 files); `.dev/reflect/pre-issueSummary-20261125175726/adversarial/adversarial/invariant-probe.md` INV-007.

### Change #15: Adherence summary (replace V2's)
Recount from real instructions. Units audited: 42 (the 41 matrix rows plus `SPEC:25`). Seven rows (INF-001, INF-017 to INF-022) are effort estimates and place no requirement on the plan; they are not counted. Of the other 35 units: 29 adherent; 6 not (INF-041 row 1; INF-002, INF-004 and INF-009, the live coordinator proof and fresh/resumed verification, rows 2 and 3; INF-023 row 5; `SPEC:25` row 4). Category counts: Authorized expansion 0, Necessary deviation 0, Drift 13 rows (5 Blocking, 5 Medium, 3 Note), Regression 0. State that unit counts are not finding counts.

### Change #16: Notes (rewrite)
- Verdict: FAIL (rows 1-5 are Blocking). Self-confidence: 0.80, from the two cards' 0.94 and 0.85 reduced for the unverified items below.
- Judge ruling on the one open dispute: row 6 graded Medium (reason above).
- Confirmed correct (from V2's list, with the "16 test files" statement removed): the six `exec "$CLAUDE_BIN"` lines (2448, 2450, 2509, 2511, 2516, 2518); env file sourced at `ccsession:1082-1086`; the insertion point between 2438 and 2440; `ccsession-orca` lines 261 and 263; `ic` lines 128 and 130; the WORKER-CONTRACT wait command at line 102; no existing test name contains 'reap'; the switch is absent from the repo outside `.dev/`; the export position is sound (INV-001).
- Not verified: whether Claude Code removes the switch from the environment of its children (inheritance, V2 row 6, left out of the table); the real Claude Code runtime switch; the installed launcher's contents; the coordinator's Orca configuration; live access; whether any `.claude/` file besides `settings.json` is tracked.
- Probe warnings carried (7 MEDIUM, 2 LOW unaddressed; none HIGH): INV-002, 003 folded into row 3; INV-004 row 9; INV-008 row 5; INV-009 row 8; INV-015 row 2; INV-016 row 10; INV-007 row 13; INV-014 row 2.
- Dismissals kept: the first-pass card's `_label_run` wording point (F4) is not a defect; its live-action ownership point (F6) is replaced by row 3.
- Reviewer metadata: reviewer 1's header says haiku class while its self-report names an OpenAI model; the self-report is not proof of model diversity.
- Coverage: the lexical matrix matched 19 of 41 rows (0.4634); most unmatched rows are covered in meaning by Constraints; the five Blocking rows are the substantive gaps.

### Change #17: provenance list (new section `## Provenance of rows`)
One bullet per row: `Row N: base V2 row X / V1 row Y, debate points ..., merged per Change #K`. Plus the standard header comments (`<!-- Provenance: This document was produced by /sc:adversarial -->`, `<!-- Base: Variant 2 (reviewer 2, qa, opus class) -->`, `<!-- Merge date: ... -->`).

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach was kept or the item excluded |
|---|---|---|
| S-002 | V1's text-only grades with a MEDIUM label on every row | V2's HIGH/MEDIUM/LOW labels that follow the grade read better; labels are not grades, no defect either way. |
| U-008, U-009, U-010, U-012 | V2 rows 8-10 and V1's INF-009 bookkeeping as plan-table rows | They audit the brief or the first-pass card, not the plan; only the count correction survives as row 13. |
| U-004 | V2 row 6 (inheritance of the switch by child processes) as a Medium row | Unverified against Claude Code; kept in Notes under 'Not verified'. |
| U-006 | V2 row 12 as its own row | Folded into row 5's fix (a `--resume <id>` untagged wrapper case forces `ccsession-orca:263`). |
| C-003 | V1's Blocking (Decision) grade | Nothing the plan or spec rests on reads the help line (INV-017); Medium by ruling. |

## Risk Summary
- Rows 1-5 are copied with their grades from the debate; a wrong grade would change the verdict only if row 5 or row 1 were demoted, and both rest on spec lines (`SPEC:21`, `SPEC:32`).
- Rollback: the two original cards stay untouched in `../reviewer-cards/`.

## Review Status
Auto-approved (no `--interactive`). Timestamp 2026-11-25T19:20:00Z.
