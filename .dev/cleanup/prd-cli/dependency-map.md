# Dependency map: remove the `prd` command-line pipeline (6.0.0, PR 1)

Measured on 2026-11-17 at `c873befec` (branch `clayphi/v6-prd-cli`, based on `integration`). Method: `git grep` over tracked files (patterns for `cli/prd`, `superclaude prd`, `superclaude.cli.prd`, `prd_group`, `PrdExecutor` and friends, quoted `"prd"`, CLI-roster lists), plus a read of every hit. Codegraph disconnected mid-session, so callers were checked with `git grep` and Grep (an import of the package needs `superclaude.cli.prd` or `from .prd`, and both searches are exact).

What stays: the interactive `prd` skill (`src/superclaude/skills/prd/`, `/prd`), the PRD templates, and everything that handles a PRD as an input document (`roadmap`, `tasklist`, `tdd`, `--prd-file`).

## A. Delete (32 files, matches the plan's count)

| Path | Files |
|---|---|
| `src/superclaude/cli/prd/` | 15 (`__init__`, `_artifact_patterns`, `commands`, `config`, `diagnostics`, `executor`, `filtering`, `gates`, `inventory`, `logging_`, `models`, `monitor`, `process`, `prompts`, `tui`) |
| `tests/cli/prd/` | 17 (`__init__` plus 16 test files) |

Nothing else in `src/` imports the package. The only import of it is the registration in `main.py` (B1).

## B. Edit outside the package (needed for the removal to leave no broken reference)

| # | Reference | Change |
|---|---|---|
| B1 | `src/superclaude/cli/main.py:539-541` | Delete the `from superclaude.cli.prd.commands import prd_group` line and `main.add_command(prd_group, name="prd")`. |
| B2 | `src/superclaude/cli/eval/orchestrator.py:10-12` | Docstring says the scheduler mirrors `cli/prd/executor.py:774-802`. Reword so it no longer points at removed code. |
| B3 | `src/superclaude/hooks/scripts/reject-workspace-writes.sh:39-62` | Delete the FU-003 branch that rejects repo-root `prd-<slug>/` writes (its message and comments name `superclaude prd run` and `cli/prd/config.py`). The skill-creator workspace branch above it stays. Mirror `.claude/hooks/` follows from `make sync-dev` (not staged). |
| B4 | `src/superclaude/agents/reuse-auditor.md:22` | Motivating-case sentence names "`prd`'s `_bind_specs`". Reword to a generic description; the worked examples at lines 85 and 97 name only the function, which is a label, and stay. |
| B5 | `tests/cli/test_cli_registration.py:41` | Remove `"prd"` from `EXPECTED_TOP_LEVEL_COMMANDS` (the test runs `<name> --help` for each, so it would fail). |
| B6 | `tests/cli/reflect/test_cli_smoke.py:3` | Docstring "Mirrors `tests/cli/prd/test_cli_smoke.py`". Reword. |
| B7 | `tests/troubleshoot/backtest/test_replay_executor.py:81` | A LIVE import (`from superclaude.cli.prd import gates`) in `test_backtest_resolve_callable_module_level_function`. Point it at another module-level function that stays (`superclaude.cli.pipeline.gates.gate_passed`), keeping the assertions that matter (not class-bound, signature read). |
| B8 | `tests/skills/fixtures/review_severity_cap_edits.yaml` (row C-152 at ~1255-1263; header comment line 21) and `review_severity_sweep_edits.yaml` (rows S-107, S-108 at ~880-895) | These rows assert text inside `cli/prd/models.py` and `cli/prd/prompts.py`; `test_review_severity_rule.py` reads each row's file, so deleting the package would make `test_e_every_cap_edits_row_holds` and `test_j_every_sweep_edits_row_holds` fail. Remove the three rows and the `cli/prd/models.py` mention in the header. |
| B9 | `.dev/review-severity-rule/cap-edits.yaml`, `sweep-edits.yaml` | Tracked byte-copies that `test_ej_fixtures_are_byte_copies_of_the_plan_tables` compares with the fixtures. Apply the identical edit (B8) so the byte-copy test stays green. |
| B10 | `tests/skills/test_review_severity_rule.py:281,288` | Row counts 161 → 160 (cap) and 139 → 137 (sweep). |
| B11 | `docs/developer-guide/review-severity-rule.md:69` and `:94` | Delete the "prd CLI" row of the where-it-applies table; update "161 cap-edit or 139 sweep-edit rows" to 160 and 137. |
| B12 | `docs/developer-guide/technical-architecture.md:315` | Remove `prd` from the list of pipeline commands. |
| B13 | `docs/guides/prd-skill-release-guide.md:135-148` | Delete the "`superclaude prd` (headless CLI)" subsection. The rest of the guide is about the skill and stays. |
| B14 | `PROJECT_INDEX.json:46,94`; `PROJECT_INDEX.md:36` | Remove `prd` from the CLI groups list and the `cli` subpackages list. Line 110 of the JSON and line 75 of the MD name the skill and stay. |

## C. Looked at and NOT changed (with the reason)

| Reference | Why it stays |
|---|---|
| `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `core/WORKER-CONTRACT.md`, `core/CLAUDE.md`, `docs/user-guide/commands.md`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/**` | Every `prd` there is the interactive skill `/prd` or the PRD document, never the command line pipeline. Nothing names `superclaude prd`. |
| `src/superclaude/skills/prd/**`, `src/superclaude/templates/**/prd_template.md` | The interactive skill and its templates. |
| `src/superclaude/skills/sc-crash-recovery/refs/pipelines.md` | Describes the skill's task-file layout (`TASK-PRD-<ts>`), not the CLI. |
| `src/superclaude/cli/roadmap/**`, `cli/tasklist/**`, `tests/roadmap/test_prd_*.py`, `tests/tasklist/test_prd_*.py`, `tests/cli/test_tdd_extract_prompt.py` | PRD as an input document (`--prd-file`, `detect_input_type`). |
| `tests/troubleshoot/backtest/test_backtest_e1.py`, `_e2.py`, `_e4.py`, `replay_executor.py` (docstrings), `tests/troubleshoot/e2e-backtest-scenarios.md` | The `from superclaude.cli.prd import ...` lines are inside snippet strings that run in a subprocess against an OLD checked-out commit (`run_prefix_replay_snippet`), so they do not import the live tree. They record historical bugs. They skip when the old commits are absent. |
| `docs/testing/v5.0.0/**`, `docs/designs/prd-spec-flag.md`, `docs/releases/**`, `CHANGELOG.md` | Historical records (issue 571 rule). |
| Tracked `.dev/**` (task packages, troubleshoot, reflect, reviews, eval-workspaces such as `prd-cli-audit`, research, experiments, brainstorms) | Dated working records of past work, not live references (about 400 tracked files). Nothing in `src/`, `tests/` or CI reads them, except the two byte-copy yaml files in B9. |
| `.github/workflows/*`, `Makefile`, `pyproject.toml`, `scripts/` | No reference to the package (checked with `git grep -i prd`). |
| `.claude/settings.json` | Registers the hook script by name only. |

## D. Install and routing surface

- Entry point: the `prd` Click group is added only in `main.py` (B1); no setuptools entry point, no installer list, no doctor check names it.
- `superclaude install` copies skills, commands, agents, hooks; the `prd` skill directory is untouched.
- Mirrors: `.claude/hooks/reject-workspace-writes.sh` (gitignored, regenerated by `make sync-dev`). `plugins/superclaude/` carries no copy of any file in B.

## E. Acceptance checks derived from this map

1. `superclaude --help` does not list `prd`; `superclaude prd` exits with "No such command".
2. `git grep -i -E 'cli[./]prd|superclaude prd|superclaude\.cli\.prd|prd_group|PrdExecutor'` outside the "historical" set in section C returns nothing.
3. `tests/skills/test_review_severity_rule.py`, `tests/cli/test_cli_registration.py`, `tests/troubleshoot/backtest/` stay green.
4. Full suite: failures equal baseline; pass count drops only by the 16 removed test files' tests.

## F. Outcome (2026-11-17)

All of section A and B was applied. Two additions found while implementing, both inside B8/B9: the cap fixture's trailer (`totals:`) also carried `rows`, `by_group.prd-core` and `by_kind.cap` counts, updated from 161/5/111 to 160/4/110 in both byte copies. Section C stayed as listed; the leftover search (`git grep`, outside `.dev/`, `docs/releases`, `docs/testing/v5.0.0`, `docs/designs`, `CHANGELOG.md`) finds only the historical-replay files `tests/troubleshoot/backtest/{replay_executor.py,test_backtest_e1.py,test_backtest_e2.py,test_backtest_e4.py}`.
