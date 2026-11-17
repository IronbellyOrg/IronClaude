# T1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md` (22 lines: the stage 1 plan request; a byte copy of `stage-requests/stage1-request.md` in the program folder)
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (4 phases, 16 tasks, schema workflow-plan/1.2, 226 lines). Cited below as PLAN:<line>.
Author of this card: the reflect orchestrator, a self-review. It did not write the plan; the plan came from a `/sc:workflow` run in another session (executor class unknown). The T2 reviewers exist to break the self-review bias.
Program spec: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`, cited as SPEC:<line>. Base plan report: `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md` (8 blocking findings; F3, F4, F5, F6, F9, F12, F13, F15 touch stage 1).

## Coverage and acceptance

Pass 1 found 0 labelled ids in source.md, so every requirement is an inferred row (Pass 2: 24 rows from the requirements-analyst agent, `artifacts/pass2-requirements-analyst.yaml`; the script confirmed every quote is a verbatim substring of its cited source.md line). The deterministic containment rule matched 16 of 24 (`coverage_pct_union` 0.6667, `S_dev_density` 0.3333); it is noisy on prose. It put INF-018 (T2 non-strict) on Task 3 and INF-022 (no carrier edit) on Task 6, both wrong. A manual read maps the 8 unmatched rows to the plan: INF-002, 004, 005, 023 and 024 to the Constraints block (PLAN:20-23), INF-003 to the task numbering (15 tasks plus the exit task), INF-008 to the absence of any gate prose after Phase 4, INF-020 to PLAN:24.

Source request items and where the plan answers them:
- Constraints (new files only, digest rows stay legacy, stage 2 only after owner go): PLAN:20.
- Task 13 allow-list without the phrases, listing the auggie file, `refs/rule.md` and six stage 4 files, plugin mirror deferred: Task 3, PLAN:59 and PLAN:65-66.
- Task 12 `rule.md` with GR5 and the grep acceptance for the old sentence: Task 2, PLAN:49 (the line carves out "outside the one fenced digest's own text"; source.md:13 asks for "prints nothing").
- Task 15/all refs, no `.dev/` or `artifacts/` path: Task 5, PLAN:87. Registry 11/1/2/5: Task 6, PLAN:96-100. T3/T2 scope and temporary-tree tests: Task 15, PLAN:209-215. Exit summary: Task 16, PLAN:217-226.
- "Acceptance lines that a later task makes false get an end point": stated at PLAN:24; applied once (PLAN:65 "until the stage 4 package"); not applied to PLAN:115 (see O1).

## Deviation and risk observations

- O1 (acceptance check falsified by a later task, no end point): Task 7's acceptance line says `grep -rn "follow_ups" src/superclaude/cli/review` "shows only the new module and its command wiring" (PLAN:115). Task 10 must "Reuse the reader of Task 7" (PLAN:148), Task 12 writes the ledger row's `classifier` column (PLAN:171) and Task 13 tags ledger rows (PLAN:183), so `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py` all name `follow_ups`. No task creates a command wiring for `follow_ups` itself. The line is false from Task 10 on and carries no "until Task N" (PLAN:24, source.md:17).
- O2 (a defining file the repository does not hold): Task 3 requires 12 family rows "each naming a defining file that exists in the repository" (PLAN:62) and Task 15's T4 re-checks that each row names an existing file and a label in it (PLAN:209). The stoprule family (SPEC:740) is defined by `refs/rubric.md` of the `sc-spec-panel-stoprule-protocol` skill and by the `finding-grader` agent. Neither is under `src/superclaude/` (`ls src/superclaude/skills`, `ls src/superclaude/agents`: no match; SPEC:582 says finding-grader exists only under `~/.claude/agents/`). The only repository copies sit under `.dev/experiments/346-validation/phase5/final-bundle/builds/stoprule/`, and Task 5 forbids any `.dev/` path inside the skill folder (PLAN:87).
- O3 (allow-list content is narrower than the scan it feeds): Task 3's "Merge-rule allow-list" lists the auggie file, `refs/rule.md` and the six stage 4 files (PLAN:59, PLAN:65), and stage3-request.md:14 has the stage 3 scan read exactly that list. SPEC:845 lists `cli/roadmap/remediate_parser.py` as "Not changed", and that file holds `higher severity wins` (remediate_parser.py:55 and :301); `cli/pipeline/fmea_classifier.py:304` and `:323` hold `highest severity`. T5 scans all of `src/` (SPEC:920), so the stage 3 scan fails on those two files unless the section also lists them.
- O4 (acceptance weaker than the request): PLAN:49 allows the old definition sentence "inside the one fenced digest's own text"; source.md:13 asks for a grep that prints nothing over the skill folder. REQ-01's digest (SPEC:195-207) does not contain the old sentence, so the carve-out is vacuous but leaves room to keep it.
- O5 (mirror not re-synced): `make verify-sync` is required to report the new folder in sync at Task 1 (PLAN:40), but Tasks 2 to 6 add files to the folder afterwards; no later task or the exit summary re-runs `make sync-dev` or `make verify-sync` (PLAN:25 says to run sync-dev after editing). `verify-sync` diffs every skill folder (Makefile:166-180).
- O6 (no fixed table shape for a file that code reads): Task 9's `ReviewerJudge` and Task 12's disagreement matrix read the reviewer's label "through the scale map" (PLAN:136, PLAN:171) and Task 15's T4 parses its rows (PLAN:209), but Task 3 fixes only the column meanings in prose (PLAN:59), not the table layout or whether paths are install-relative or `src/`-relative (T3 forbids `src/superclaude` in carriers, PLAN:209).
- O7 (state not in the spec's ledger contract): `sweep-flagged` is an item state in Task 4 (PLAN:78) and Task 7 (PLAN:110), but the spec's item-state table has eight states and not this one (SPEC:379-390); it comes from the stage 2 request. An installed reference would also name stage numbers.
- O8 (spec stage 1 item without a task): SPEC:945 lists "ledger adapters" in stage 1; no task builds or drops them (SPEC:404 leaves the mapping to `review-ledger/1` to the plan; Task 7 only runs the reuse audit, PLAN:110).

## Structural observations

- Constraints say "new files only" (PLAN:20), but Task 12 edits `src/superclaude/cli/review/__init__.py` (PLAN:171) and Task 14 edits `src/superclaude/cli/doctor.py` and `tests/unit/test_cli_doctor.py` (PLAN:197). Wording, not an edit of a carrier.
- Task 10 says `Depends on: Task 9` (PLAN:146) while its body reuses the reader of Task 7 (PLAN:148). `/sc:implement` runs in file order, so no failure follows.
- Task 9 acceptance asks `verdict` to agree with "the sketch" on 6,400 combinations (PLAN:139); the sketch and `truth_table.py` sit in the program folder under `.dev/tasks/to-do/`, which moves to `done/` when archived.
- Task 15 T2 fails on any file holding "a fence opener" without a registry row (PLAN:209); the skill's own other files (SKILL.md, registry.yaml, follow-up-ledger.md) must therefore avoid writing the fence text.

## Checked and found sound

- 11 `digest` carriers exist under `src/superclaude/`, the old definition sentence is in exactly those 11 files (`grep -rln` over `src` and `plugins`), none contains `src/superclaude` (T3 can pass at `legacy`), and the cap sentence is at `pragmatic.md:227`. The 2 `pointer-only` source files exist; the 5 spec-panel variants are installed-only (`src/superclaude/commands` holds only `spec-panel.md`).
- SPEC:195-207 is the digest (REQ-01 with the REQ-02 and REQ-03 sentences and the cap sentence); SPEC:289-304 has 14 worked cases; SPEC:350-367 has the 16 Items columns of Task 4; SPEC:735-748 has the 12 families; 7 tasklist lines (1439, 1450, 1531, 1567, 1571, 1610, 1614) hold "High or Medium" or "Medium (blocking)".
- `classify` is a free subcommand name; modules export `command` and are listed in a tuple (`cli/review/__init__.py:1-36`); `tests/unit/test_cli_install.py` checks baseline members for presence only, so a new skill folder breaks no inventory; `lint-architecture` only pairs `sc-*-protocol` skills with commands (Makefile:362+); PyYAML is a declared dependency (`pyproject.toml:38`); `origin_repo.py`, `ledger.py`, `findings_v2.py`, `card_convert.py`, `doctor.py::run_doctor` and the named doctor tests exist.
- Findings of the base report: F4 (analysis template is no carrier row, PLAN:96), F5 and F12 (T3 exemptions, PLAN:209-215), F13 (scale map without the phrases, PLAN:66), F15 (no `.dev/` path, PLAN:87) are resolved in this plan; F6 only in part (O1); F3 only in part (O3).

## Recommendations

- Give PLAN:115 an end point ("until Task 10") or reword it to name the allowed importers; add the command wiring or drop that phrase.
- Name an in-repository defining file for the stoprule row, or exempt installed-only rows from Task 3's file-exists line and T4, and say which.
- List `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` in the allow-list section, or have the scale-map code-assigned row feed the scan.
- Add a final `make sync-dev` / `make verify-sync` line to Task 16 and state the scale-map table layout in Task 3.

## Self-reported confidence

0.72 (a self-review; O2 and O3 rest on file listings and greps I ran, the downstream effect of O3 on stage 3 is inference from SPEC:920 and stage3-request.md:14).
