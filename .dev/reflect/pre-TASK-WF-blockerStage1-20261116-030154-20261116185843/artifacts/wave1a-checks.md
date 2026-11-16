# Wave 1A grounding record (UC-1, read-only checks)

Run folder: `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116185843/`. `PLAN:n` is a line of the plan file `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (254 lines). `SPEC:n` is a line of `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (1224 lines). Every check below was a read-only command run from the repository root on 2026-11-16 (two batch scripts under `/tmp`, removed afterwards, plus a path scan with `uv run python`).

Read in full by the orchestrator: the plan, `source.md` (55 lines), `artifacts/codegraph-grounding.md`, the first and second `REPORT.md`, `stage-requests/revision2-brief.md`, `stage-requests/README.md`, `OPEN-QUESTIONS.md`, the stage 2 plan, and SPEC:1-1224 (sections 0 to 17 and Appendix A).

Codegraph run state: `codegraph_status` at 2026-11-16T19:09Z: index_state fresh (3646 files, 0 added, 0 modified, 0 removed), worktree_root and projectPath `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`. The index covers Python, YAML, JavaScript and TypeScript and no Markdown, and the checks were file-existence, grep and count checks over Markdown, Python and JSON, so the Grep/Read floor was the evidence and no `graph:*` token is recorded.

## Results (one line per check)

| Check | Result |
|---|---|
| Plan structure | 16 tasks (`## Task 1` to `## Task 16`), 4 phases (PLAN:32, 118, 145, 216), 16 `Acceptance criteria:` labels, 15 `Depends on:` lines (Tasks 2 to 16) all pointing to a lower task number (PLAN:47 to PLAN:246); no checkbox or numbered line; no `/home/` or `.dev/tasks/to-do` prefix in the plan; `uv run python /tmp/gate_check.py` (read first, read-only) prints `TASK-WF-blockerStage1-20261116-030154 16 tasks 4 phases PASS` |
| `source.md` | equals `stage-requests/stage1-request.md` byte for byte (`cmp`) |
| Backticked paths in the plan | 66 exist; the absent ones are all files this package creates (skill folder files, 6 modules, `classifier_thresholds.json`, 7 test files, `./artifacts/` files) or files of other packages (`stage0-summary-for-owner.md`, `stage0a-result.md`) or short forms of existing files; no missing path |
| Stage 0 outputs the plan reads | the stage 0 plan writes `./artifacts/stage0-summary-for-owner.md` and `./artifacts/stage0a-result.md`; the 58.5 percent and kappa 0.27 figures and the M, C, E at-chance finding are in `08-test/results.md` lines 22, 74, 87 |
| `07-classifier/truth_table.py`, `02-brainstorm/blocker_truth_table_sketch.py` | both exist; `verdict(s, m, c, w, e, d)` and `tri`, `wrong` are defined in the sketch |
| Definition sentence "Grade every review finding as blocking or minor" | 11 files in `src/`, 0 in `plugins/`, exactly the 11 digest carriers of Task 6; no file holds a `review-severity:digest` fence yet |
| Merge-rule phrases (`highest severity`, `more severe rating`, `higher severity`) | 13 files: `agents/rf-analyst.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `cli/pipeline/fmea_classifier.py`, `cli/roadmap/remediate_parser.py`, `skills/operational-guide/SKILL.md`, `skills/readme/SKILL.md`, `skills/sc-auggie-review-protocol/SKILL.md`, `skills/task/SKILL.md`, `skills/tdd/refs/build-request-template.md`, `skills/tech-reference/SKILL.md`, `templates/documents/agent_template_analysis.md`, `templates/documents/agent_template_qa.md`; the allow-list of PLAN:66 covers every one that stays after stage 3 |
| `src/superclaude` inside the 11 digest carriers | 0 in each (so T3 passes at `legacy`); 1 in `commands/spec-panel.md` (a `pointer-only` row, exempt) |
| Tasklist Medium count | `grep -c -i "High or Medium\|High and Medium\|Medium (blocking)\|High/Medium"` over `skills/sc-tasklist-protocol/SKILL.md` prints 9 (PLAN:72 says 9) |
| Pragmatic cap sentence | the sentence quoted at PLAN:49 matches one line of `output-styles/pragmatic.md` |
| `cli/review/__init__.py` tuple | nine names (`panel_cmd`, `merge_cmd`, `ledger_cmd`, `telemetry_cmd`, `lint_cmd`, `estimate_cmd`, `cluster_cmd`, `verify_cmd`, `manifest_cmd`); `lint_cmd` and `estimate_cmd` have no module; `tests/review/test_review_cli.py:44-47` asserts the help lists named subcommands by inclusion, so `classify` breaks nothing |
| `cli/review/data/` | exists, 9 tracked JSON files; `pyproject.toml` wheel `include = ["src/**", ...]`, so a new JSON file ships |
| Name collisions | no `classifier*`, `classify*`, `safety_route*`, `follow_ups*` module under `cli/review/`; no `sc-review-severity` skill; none of the 7 planned test files exists |
| `origin_repo.py` | `class ClaimError` (line 77) and `def read_origin()` (line 156) exist; `read_origin` runs `git remote get-url origin` through `subprocess`, so Task 8's injected resolver and its by-path load test are consistent |
| Existing tests named by tasks | `tests/cli/test_update_command.py`, `tests/unit/test_cli_doctor.py`, `tests/cli/test_install_retired_mcp.py`, `tests/review/test_review_cli.py` exist; `tests/unit/test_cli_install.py` checks a baseline list by presence, so a new skill folder breaks nothing |
| Scale-map feasibility | every `repo` family named at PLAN:62 has an existing defining file and its native labels are present (case-insensitive) in it; the two stoprule files exist installed (`~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md`, `~/.claude/agents/finding-grader.md`) |
| Carrier diff | `git diff --stat HEAD` over the PLAN:248 carrier list prints nothing today |
| Registry count | spec carriers: 11 digest rows exist as files; 2 pointer-only and the canonical row exist or are created by the plan; 5 installed-only spec-panel variants are not in `src/` |
| `make` targets | `doctor` (Makefile:23), `lint` (48), `sync-dev` (109), `verify-sync` (166), `lint-architecture` (362) exist |
