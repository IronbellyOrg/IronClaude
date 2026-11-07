---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-specPanelReviewL-20261107-090418
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# Review Loop contract for /sc:spec-panel (issue 346)

Source: ./source.md
Goal: `/sc:spec-panel` accepts `--re-review <prior-findings-file> --baseline <saved-copy>`, carries a seven-bullet `## Review Loop` section (grading, verdict line, 3-review cap, scoped re-review output, reviser contract, brief precedence), the routing guide and the two release guides tell users to save a copy and re-review with the flags, and one new text-presence test pins the wording.

## Constraints

- Edit canonical files under `src/superclaude/` and the named `plugins/superclaude/` mirrors by hand; run `make sync-dev` afterwards. Never stage anything under `.claude/`. Stage `.dev/tasks` with the work.
- Do not change `src/superclaude/output-styles/pragmatic.md`, any `sc-implement-protocol` file, or `WORKER-CONTRACT.md`. Do not touch `docs/user-guide/flags.md` or `commands/sc-help.md` (the generic `--iterations` rows).
- The literal bullet text comes from section 5 of ./source.md and must be copied byte for byte; each bullet is ONE line. If an existing matcher in `tests/skills/test_review_severity_rule.py` flags a bullet, change the minimum wording and keep the literals the new test asserts (source section 9, T3 to T8), updating the test in the same change.
- Installed primitives must not name `src/superclaude/` paths. Do not add a size limit, a monotonic halt or an installer change (source section 11).
- Handoff notes for the pull request, not tasks: the body uses `Refs` for issue 346 (the causal link is unproven), and it says that the new command text reaches an existing host only after `superclaude install --force` or `update`.

## Phase 1: Command text

## Task 1: Add the Usage tail and the Review Loop section to the source command

Edit `src/superclaude/commands/spec-panel.md`. Append ` [--re-review <prior-findings-file> --baseline <saved-copy>]` to the Usage line (line 22, inside the first text fence), after `[--format standard|structured|detailed]` (source section 4). Insert the `## Review Loop` section, copied from the fenced block in section 5 of ./source.md (heading, blank line, seven one-line bullets, Mode through Precedence), immediately before the `## Output Formats` heading (line 254 before the edit), with a blank line before and after.

Acceptance criteria:
- The Usage line ends with the new tail and nothing else on that line changed.
- `## Review Loop` appears exactly once, before `## Output Formats`, followed by exactly seven lines that start with a digit, a period and a bold label, in the order Mode, Grading, Verdict, Cap, Re-review output, Reviser contract, Precedence.
- The section contains `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` and `HALT and escalate to the user with the open blocking findings`, and no `src/superclaude` path.
- `uv run pytest tests/skills/test_review_severity_rule.py` passes; the output is saved to ./artifacts/t1-severity-test.log.

## Task 2: Apply the same two blocks in place to the plugin copy

Depends on: Task 1

Edit `plugins/superclaude/commands/spec-panel.md` in place: the same Usage tail on line 22 and the same `## Review Loop` section before its `## Output Formats` heading (line 254). Do not byte-copy the `src/` file over it: the plugin copy already differs from `src/superclaude/commands/spec-panel.md` by one word at line 219 ("Sequential" there, "Native reasoning" in `src/`), and that difference stays.

Acceptance criteria:
- The Usage tail and the section text in the plugin file are identical to the ones in the source command file.
- A `diff` of the two command files shows only the pre-existing line-219 word difference; the diff is saved to ./artifacts/t2-spec-panel-diff.txt.
- `uv run pytest tests/skills/test_review_severity_rule.py` still passes.

## Phase 2: Routing guide and release guides

## Task 3: Replace the review-loop sentence in the routing guide

Edit `src/superclaude/core/HOW-WE-WORK.md` line 65. Replace the text from "ask Claude to apply them to the PRD" to the end of the line with the sentence in the text fence of section 6 of ./source.md ("save a copy of the PRD, ask Claude to apply them to the PRD, then run it again with `--re-review <this report> --baseline <the saved copy>`; stop after 2 fix cycles (3 reviews) and decide with the open blocking findings."). Keep the "It only reports. Decide which findings to accept, " prefix. Change no other line; the file stays ASCII.

Acceptance criteria:
- Line 65 contains `--re-review`, `--baseline` and `save a copy of the PRD`, and the file no longer contains `until no critical findings remain`.
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py` passes (no routing row id or level-table change); output saved to ./artifacts/t3-routing-tests.log.

## Task 4: Byte-copy the routing guide to the plugin refs

Depends on: Task 3

Copy the edited `src/superclaude/core/HOW-WE-WORK.md` byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`.

Acceptance criteria:
- `cmp` of the two files reports no difference.
- `uv run pytest tests/commands/test_routing_plugin_parity.py` passes; output saved to ./artifacts/t4-parity-test.log.

## Task 5: Replace the old sentence in the two release guides

Edit `docs/guides/prd-skill-release-guide.md` line 493 and `docs/guides/tdd-skill-release-guide.md` line 501. Each line reads `It only reports. Decide which findings to accept, ask Claude to apply them to the PRD, then run the same command again until no critical findings remain.` Apply the same replacement as in Task 3 (keep the "It only reports. Decide which findings to accept, " prefix; same new tail sentence). Read each line first and change nothing else.

Acceptance criteria:
- Both lines carry `--re-review`, `--baseline` and `save a copy of the PRD` and keep the "It only reports." prefix.
- Run from the repo root: `grep -c -F -- "until no critical findings remain" src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md docs/guides/prd-skill-release-guide.md docs/guides/tdd-skill-release-guide.md`. It prints one `<path>:<count>` line per file, and all four lines end in `:0` (grep then exits 1, which is the expected result). The four lines and the exit code are saved to ./artifacts/t5-old-sentence-search.txt in this package's `artifacts/` folder (not the repo-root `artifacts/`).

## Phase 3: Regression test

## Task 6: Add the text-presence test for the Review Loop

Depends on: Task 2
Depends on: Task 4
Depends on: Task 5

Create `tests/skills/test_spec_panel_review_loop.py` following section 9 of ./source.md. Import `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES` from `tests.skills.test_review_severity_rule`; define a local whitespace flatten (`" ".join(text.split())`); resolve the repo root with `Path(__file__).resolve().parents[2]`. Parametrize over the two spec-panel files (`src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`) for tests T1 to T9 (Usage tail, section position, seven single-line bullets in order, cap literals, vocabulary literals, project-first rf-qa lookup literal, the three literals from the spec review, the precedence sentence, no `src/superclaude` inside the section). Add test T10 for the guide sentence: in both HOW-WE-WORK copies the line containing `It only reports.` contains `--re-review`, `--baseline` and `save a copy of the PRD`, and `until no critical findings remain` appears in neither HOW-WE-WORK copy nor in the two release guides. Do not assert that the whole `spec-panel.md` lacks a `src/superclaude` path (line 218 names one).

Acceptance criteria:
- `uv run pytest tests/skills/test_spec_panel_review_loop.py` passes; output saved to ./artifacts/t6-new-test.log.
- Each literal is its own assertion or parametrized case. One mutation run is recorded in ./artifacts/t6-mutation.log: back up `src/superclaude/commands/spec-panel.md` to ./artifacts/, delete the phrase `never fall back to a first review` from the real file, run the new test and see only the matching case fail, then restore the file from the backup and confirm with `cmp` that it is identical to the backup.
- `uv run ruff format --check` with the repo's pinned ruff and `make lint` report no problem for the new test file.

## Phase 4: Sync and final state

## Task 7: Sync the dev copies and confirm repository state

Depends on: Task 6

Run `make sync-dev` so the changed command is copied into the untracked `.claude/` tree, then `make verify-sync`. Run `make lint` and the repo's pinned ruff format check on the changed Python file. Run the keep-green tests named in section 9 of ./source.md: `tests/skills/test_review_severity_rule.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/core/test_claude_md_routing_block.py`, `tests/skills/test_primitive_dual_surface_lookup.py`, `tests/docs/test_onboarding_deck.py`, `tests/skills/test_worker_contract.py`.

Acceptance criteria:
- `make verify-sync`, `make lint` and the ruff format check pass; their output is saved to ./artifacts/t7-sync-lint.log.
- All seven keep-green test files pass together with the new test file; output saved to ./artifacts/t7-tests.log.
- From the repo root, run `git diff --name-only HEAD -- . ':!.dev'` and `git ls-files --others --exclude-standard -- . ':!.dev'`; save their combined, de-duplicated list (`sort -u`) and both exit codes to ./artifacts/t7-changed-files.txt in this package's `artifacts/` folder (not the repo-root `artifacts/`). Every listed path is one of these 8: `src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/guides/prd-skill-release-guide.md`, `docs/guides/tdd-skill-release-guide.md`, `tests/skills/test_spec_panel_review_loop.py`, `docs/designs/spec-panel-review-loop.md` (plus `tests/skills/test_review_severity_rule.py` only if the Task 1 log records a Constraints matcher wording change). The 7 delivery paths (all of the 8 except the design doc) are all listed; the design doc may be absent only because it was committed before Task 1 started. No listed path is under `.claude/`, ends in `pragmatic.md` or `WORKER-CONTRACT.md`, contains `sc-implement-protocol`, or is `docs/user-guide/flags.md` or `commands/sc-help.md`. `git diff --cached --name-only -- .claude` prints nothing, and its output is appended to the same file.
