# Codebase context: 346-stoprule

Tier: fallback_1 (auggie MCP not available in this session; codegraph index fresh, 2482 files; native Grep and Read). Read on 2026-11-08 in worktree bs346-stoprule (origin/master).

## The 427 contract (current text)
- `src/superclaude/commands/spec-panel.md:256-264` `## Review Loop`, 7 bullets: Mode, Grading (CRITICAL and FR-8/FR-9 blocking; MAJOR blocking only if it names a concrete wrong outcome), Verdict (last line `verdict: PASS|FAIL`, written by the reviewer), Cap (`review: N of 3`, canonical cap text, HALT at review 3 FAIL), Re-review output (`resolved|open|regressed` table, `origin=changed|unchanged`), Reviser contract (`Reviser brief`), Precedence.
- `spec-panel.md:328-330` FR-8 (any GAP row is MAJOR minimum), FR-9 (blank behaviour is MAJOR minimum), FR-10 (table must be complete): a mechanical upward severity floor that the 427 Grading bullet keeps as blocking.
- `spec-panel.md:82` severity scale: CRITICAL provably wrong, MAJOR ambiguous or incomplete under attack, MINOR inferable.
- `docs/designs/spec-panel-review-loop.md:143`: "every rule here is prose read by a model. The tests prove the text is present".
- Test pinning the 427 text: `tests/skills/test_spec_panel_review_loop.py`; cap constants `tests/skills/test_review_severity_rule.py:215-219` (`CANONICAL_CAP_TEXT`, `AT_CAP_CLAUSES`).

## Prior art for a computed verdict and severity derivation
- `src/superclaude/skills/sc-implement-protocol/refs/qa.md:37-81`: severity derived by the parent from four yes/no checklist answers, each with an anchor the parent Reads back as a file check; "The reviewer's prose label ... is never read. There is no second model pass" (`:79`).
- `qa.md:95-97` Verdict owner: the reviewer returns no verdict; the parent computes it from parent-confirmed blocking findings.
- `qa.md:150-170` origin computed from exact line text: `inherited`, `late` (present in an earlier reviewed tree and not flagged), `fix-induced`, `new`. In implement a `late` BLOCKER still blocks ("never capped", `:167`); a non-blocking late finding is a note. The stoprule theme's demotion of late-found blockers is a deliberate departure from this.
- `qa.md:186` later reviews cannot re-open accepted text with a lower-severity finding.

## Prior art for an independent second grader
- `src/superclaude/agents/confidence-calibrator.md:3,21` (model: sonnet): re-grades a card against a rubric with the formation context stripped; "Apply the rubric mechanically".
- `src/superclaude/agents/evidence-validator.md:23-35` (model: sonnet): re-reads every citation, independent of upstream, read-only; "A false PASS here is worse than a false FAIL".
- `src/superclaude/agents/rf-qa.md:379-` Fix Cycle phase (427 bullet 5 points to its steps 1-5).

## Scripts and install surface
- Skills ship scripts invoked as `uv run --no-project python "<skill base>/scripts/<name>.py"` (`src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:54`, `scripts/archive_workspace.py`, tested in `tests/skills/test_workflow_archive.py`). A command file has no scripts folder, so a script for a command needs a companion skill folder.
- `src/superclaude/cli/install_commands.py:60-80`: install copies command files, skipping existing ones without `--force`; a new command name installs without touching existing files.

## Observed reviewer behaviour (experiment reports, read-only)
- Arm B flg-r2 R3 (`exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round3.md:84-90`): one blocking finding N12, origin=changed, on text the N5 fix wrote; has quote, mechanism and a stated wrong outcome.
- Control ctl-r1 R3 (`exp346-ab-ctl-r1/.../spec-panel-round3.md:164,169-170,188`): every Boundary-Table GAP carried as MAJOR under FR-8; two expert disagreements (minor vs MAJOR) both recorded MAJOR; R3-8 "Present in the round-2 input, not flagged then" graded blocking.
- Arm B disposition round 2 (`exp346-ab-flg-r2/.../disposition-round2.md`): 15 of 15 findings applied including 9 minor, because the brief says to apply confirmed findings.
