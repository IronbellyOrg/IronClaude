# Dependency map: remove cli-portify (6.0.0, PR 4 of issue 571)

Measured 2026-11-17 on `clayphi/v6-cli-portify` at `da12c4d76` (= `origin/integration`, so PRs 1, 2, 5, 6, 7, 8, 10 and the small fixes are already in).
Method: `git grep -iE portify` over all tracked files, `git ls-files | grep -i portify`, codegraph (`codegraph_callers cli_portify_group`, `codegraph_impact PortifyProcess`), plus import search for `cli_portify` across `src/` and `tests/`. Mirrors: `.claude/` is gitignored and produced by `make sync-dev` (which never deletes, so the stale copies are removed by hand); `plugins/superclaude/` and the root `commands/` folder hold no cli-portify command or skill (only the routing-guide copy below).

## Kept-module check (note 1 of the prompt)

No kept module imports `cli/cli_portify`. The only importer in `src/` is `src/superclaude/cli/main.py:537-539`, the registration this PR removes. `cli/pipeline` (shared runner), `reflect`, `swarm`, `audit`, the eval harness and `/sc:implement` import nothing from it. `PortifyProcess` is used only inside `cli_portify` and in `tests/pipeline/test_process_stdin.py` (a test of the portify subclass, not of `ClaudeProcess`). The codegraph impact list also shows `scripts/eval_workflow_vs_task_builder.py`, `tests/cli/eval/test_workflow_vs_task_builder_companion.py` and `roadmap/semantic_layer.py`; those are name collisions on `run` (grep for `PortifyProcess` finds none there), so they need no change.

## A. Files deleted (whole)

| Path | Files | Notes |
|---|---|---|
| `src/superclaude/cli/cli_portify/` (incl. `steps/`) | 21 + 8 tracked | package, ~288 KB |
| `src/superclaude/commands/cli-portify.md` | 1 | `/sc:cli-portify` |
| `src/superclaude/skills/sc-cli-portify-protocol/` (SKILL.md, `__init__.py`, `decisions.yaml`, `refs/` x3) | 6 | skill, ~83 KB |
| `tests/cli_portify/` (incl. `integration/`, `fixtures/`) | 31 + 2 + 2 | ~386 KB |
| `docs/guides/cli-portify-and-pipeline-runner-guide.md` | 1 | whole guide is about portify (sections 1-3, 5, 7-8); nothing links to it; its 'pipeline foundation' sections describe `cli/pipeline` for portify authors |
| `scripts/check-ref-staleness.py` | 1 | only checks the portify skill refs against `cli/pipeline` models; nothing calls it |
| `.claude/commands/sc/cli-portify.md`, `.claude/skills/sc-cli-portify-protocol/` | untracked | mirror, remove by hand (sync-dev does not delete) |

## B. Files edited (path:line -> change)

### Code
- `src/superclaude/cli/main.py:537,539` -> drop the import and `main.add_command(cli_portify_group)`.
- `src/superclaude/cli/recommend/prompts.py:38` -> drop key `"cli-portify"` from `CLASSIFICATION_KEYS`; `:68` -> drop its line in `CLASSIFIER_PROMPT`.

### Core docs and routing guide (both copies of the routing guide must stay byte-identical)
- `src/superclaude/core/HOW-WE-WORK.md:254` (routing row 'Workflow-to-CLI specification'), `:267` (the 'Portification and optional referrals' bullet; keep the referral sentences that stay true), `:380` (`cli-portification-spec` row) -> remove / reword.
- `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:254,267,380` -> byte copy of the above.
- `src/superclaude/core/WORKER-CONTRACT.md:330` (list of 13 P2 commands -> 12, drop cli-portify), `:334` (the 'four P2 commands with a required brief flag ... 16 rows' sentence -> three, 15 rows), `:343` (table row).
- `src/superclaude/core/CLAUDE.md` -> no portify mention; check the converted-command counts after the edit (no change expected).
- `src/superclaude/templates/documents/release-spec-template.md:244`, `src/superclaude/examples/release-spec-template.md:248` -> the 'Auto-populated by `sc:cli-portify` Phase 3c' note becomes a neutral sentence; `.claude/templates/documents/release-spec-template.md` is the mirror (sync-dev).

### User and developer docs
- `docs/user-guide/commands.md:60` (table row), `:216-231` (the section) -> remove.
- `docs/developer-guide/technical-architecture.md:315` -> drop `cli-portify` from the list of CLI commands.
- `docs/developer-guide/review-severity-rule.md:48` (B4 row), `:70` (table row), `:104` (bullet about `--max-convergence`) -> remove; renumber nothing else.
- `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:114` -> the example `/sc:cli-portify` in the `src/superclaude` rule (also `CLAUDE.md:97`): replace with another command that works on this repo's source by design (for example `/sc:cleanup-audit`... check wording against `sc-post-release`, which does read repo source), or just drop the example.
- `CLAUDE.md:97` -> same example removal.
- `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1315,1318,1840,1989` -> drop cli-portify from the command lists and counts (the four lines name it among converted commands).
- `docs/generated/contributor-knowledge-base/architecture-guide.md:256`, `components-guide.md:184`, `docs/generated/sprint-cli/04-gates-validation.md:198`, `07-skills-commands.md:181` -> remove the line / sentence naming it.
- `PROJECT_INDEX.md:36,68,97`, `PROJECT_INDEX.json:46,94` -> drop `cli-portify` / `cli_portify/` from the lists.
- `KNOWLEDGE.md:185` -> follows the test-class rename in section C (`TestCliPortifyRegression` -> `TestDispatchTableRegression`).
- `CHANGELOG.md:234` -> past entry, NOT edited (historical record).

### Scripts
- `scripts/run-fidelity-batch.sh:33-34`, `scripts/run-fidelity-batch-refactored.sh:30-31,62,76,134-135` -> remove the two `v2.24*-cli-portify-cli-*` release entries and fix the counts in their comments (10 -> 8 releases, batches).

### Tests (edited, kept)
- `tests/cli/test_cli_registration.py:33` -> drop `"cli-portify"` from `EXPECTED_TOP_LEVEL_COMMANDS`.
- `tests/unit/test_cli_install.py:115` (command file list), `:228-232` (skill file list), `:801` (docstring that cites `cli-portify/resolution.py`) -> remove / reword.
- `tests/core/test_how_we_work_routing_table.py:299` (`sc:cli-portify` in a not-members set -> drop), `:685` (`S11` case -> retire), `:879-881` (portify assertions in a shared test -> drop those three lines), `_EXPECTED_IDS` (`cli-portification-spec`), plus any id count.
- `tests/recommend/test_routing_refresh.py` -> retire case S11 in the id list and docstring; add `cli-portify` to `_POST_REFRESH_REMOVALS` (the frozen command record keeps listing it, as for spawn, build, improve).
- `tests/recommend/fixtures/routing_refresh_cases.json:221-241` (case S11) -> remove; `:678` (frozen command disposition row) stays, like the other removed commands; check the `checks` T-table and `contract_gaps` C04 usage.
- `tests/skills/test_sc_recommend_routing_contract.py:280` -> drop `"cli-portify"` from the expected `CLASSIFICATION_KEYS`.
- `tests/skills/test_worker_contract.py:499` (`P2_COMMANDS`), `:669-680` (`UNATTENDED_EXPECT` entry), `:970` (`P2_NEW_BRIEF_ROWS`), `:1771` (`P2_GATES` row), the `len(...) == 13/28` pins in `_check_p2_set` -> 12 / 27, and the 'four ... 16 rows' pin if any.
- `tests/pipeline/test_process_stdin.py:1,19,41-117` -> remove `PortifyProcess` import, class `TestPortifyAnchor`, and any helper left unused (`_stdin_echo_argv`, `patch`) ; update the module docstring.
- `tests/skills/fixtures/review_severity_cap_edits.yaml:20-21,1093-1203` -> remove the 20 `portify` rows (C-132..C-151) and the group mention in the header; `tests/skills/test_review_severity_rule.py:281` row count 160 -> 140. `.dev/review-severity-rule/cap-edits.yaml` is the byte-twin that `test_ej_fixtures_are_byte_copies_of_the_plan_tables` compares against, so it gets the same edit (it is a plan table pinned by a test, not a narrative record).
- `tests/audit/test_wiring_integration.py:1,5,29,81...` -> rename fixture `cli_portify_fixture` and reword the docstring (it models the `step_runner=None` bug pattern; the test itself is for `cli/audit` and stays).
- `tests/roadmap/test_fingerprint.py:9,93,108,305-326`, `test_integration_contracts.py:7,98,114,281-360`, `test_obligation_scanner.py:8,84,334-350`, `test_anti_instinct_integration.py:8,127-133` -> rename the `CLI_PORTIFY_*` constants and `TestCliPortifyRegression` classes and reword comments (these roadmap tests stay until PR 11; only the names change).
- `tests/roadmap/test_parser_consistency.py:216-218` -> the assertion `(_SRC_ROOT / "cli_portify" / "utils.py").exists()` goes (that directory is gone); keep the audit half.
- `tests/roadmap/fixtures/recurrence/retry_contract/retry_loop_no_terminal_case.md:17` and `.expected.json:6` -> they name `v2.24-cli-portify` as the incident source. Check which test reads them and whether the text is asserted; reword to a neutral release label if not pinned.

## C. Not edited (historical records or frozen records)

`docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries, everything under `.dev/` except the one pinned plan table above (work records, experiments, frozen task packages, e.g. `.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/`), and the frozen command record row in `routing_refresh_cases.json` (as for earlier removals). `CHANGELOG.md` gets no new entry (the release PR does that).

## D. Install and registration surfaces checked, nothing to change

`pyproject.toml`, `Makefile`, `.github/`, `src/superclaude/hooks/` (incl. `launch-level-guard.sh`, which never named cli-portify), `install*.py`, `doctor`, root `commands/`, `agents/`, `skills/`, `plugins/superclaude/{commands,skills}`: no mention (`git grep -i portify`). Skills and commands are discovered by directory, so deleting the directories un-installs them for new installs; installed copies in existing workspaces are the retire step (PR 12).

## E. Generator-Constraint check

Deleted: `src/superclaude/cli/cli_portify/gates.py` and `tests/cli_portify/test_portify_gates.py` (a gates file; the PR body needs a `## Generator-Constraint Considered` section). No `structural_checkers.py` or `*_validator.py` is touched (check again at commit time with `git diff --name-only --diff-filter=DM origin/integration`).
