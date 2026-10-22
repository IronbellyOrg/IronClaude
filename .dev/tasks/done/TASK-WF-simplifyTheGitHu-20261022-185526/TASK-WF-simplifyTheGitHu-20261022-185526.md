---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-simplifyTheGitHu-20261022-185526
version: "2"
priority: Medium
created_date: "2026-10-22"
---

# Simplify the GitHub Actions workflows

Source: ./source.md
Goal: `.github/workflows/` loses three dead or duplicate workflow files and the remaining workflows lose duplicated setup, dead steps, and redundant Python versions, while every PR to master/integration still runs the same checks.

Revision note (version 2): folds in the pre-execution reflection fixes R-1 to R-5 (report: `.dev/reflect/pre-TASK-WF-simplifyTheGitHu-20261022-185526-20261022185804/REPORT.md`, merged findings M-1 to M-12), applied at the user's request. Tasks were renumbered: the new Task 1 is the required-checks check, and every former Task N is now Task N+1.

## Constraints

- Scope is `.github/workflows/` only, including `.github/workflows/README.md`. No other repo file changes. Task evidence files go under `./artifacts/` in this package.
- Checks that must still run on every PR to master/integration after all tasks: full pytest (with `make sync-dev` before it), ruff check, ruff format --check, pytest plugin check (plugin load + fixtures grep), make sync-dev before make verify-sync, make lint-architecture, make verify-deps, superclaude install + superclaude doctor --verbose, swarm imm/inv marker lanes, coverage XML upload to Codecov, the Contract #3 PR-body check, and the boundary-guard warning plus job summary.
- Line numbers below were read at planning time (2026-10-22) and shift as earlier tasks edit `test.yml`; locate steps by their `name:` value.
- YAML validity check for every edited workflow: `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <file>` (run `actionlint <file>` too if it is installed).
- Do not change the Python test suite, Makefile, or pyproject.toml. The pyproject classifiers for 3.11/3.12 stay as they are.

## Phase 1: Confirm safety, then remove dead workflows and dead steps

## Task 1: Confirm no required status check depends on a check name this plan removes or renames

Before any workflow edit, query branch protection and rulesets for both target branches and save the raw output (stdout and stderr) to `./artifacts/t1-required-checks.txt`:
- `gh api repos/IronbellyOrg/IronClaude/branches/master/protection 2>&1`
- `gh api repos/IronbellyOrg/IronClaude/branches/integration/protection 2>&1`
- `gh api repos/IronbellyOrg/IronClaude/rules/branches/master 2>&1`
- `gh api repos/IronbellyOrg/IronClaude/rules/branches/integration 2>&1`

Read the output by message text, not by HTTP status: "Branch not protected" and "Branch not found" both mean no required checks on that branch, and `[]` from a rules query means no rulesets. The check names this plan removes, renames, or path-filters are: `Test on Python 3.10`, `Test on Python 3.11`, `Test on Python 3.12`, `Lint and Format Check`, `Pytest Plugin Check`, `Dependency Allow-list (AC3)`, `Quick Test (Python 3.10)`, `Multi-language README Quality Assessment`, and `Generator-Constraint Considered (Contract #3)`. If any of them is a required status check (classic protection `required_status_checks.contexts`, or a ruleset `required_status_checks` rule), stop the plan and report which one. If `gh` is unavailable or unauthenticated, record that in the artifact and stop; do not guess. (Planning-time result, 2026-10-22: master "Branch not protected", integration "Branch not found", master rules `[]`.)

Acceptance criteria:
- `./artifacts/t1-required-checks.txt` exists and contains the output of all four commands.
- The artifact ends with a one-line conclusion naming each of the nine check names as not required, or the plan stopped and the report names the required check.

## Task 2: Delete readme-quality-check.yml

Depends on: Task 1

Delete `.github/workflows/readme-quality-check.yml`. Reason (source item 1): it scores `README-zh.md`, `README-ja.md`, `README-kr.md` and a `Docs/**` path, none of which exist in the repo (only lowercase `docs/` exists), and it installs `beautifulsoup4` and `pyyaml` that its embedded script never imports.

Acceptance criteria:
- `.github/workflows/readme-quality-check.yml` no longer exists.
- No other file was changed by this task.

## Task 3: Delete publish-pypi.yml

Depends on: Task 1

Delete `.github/workflows/publish-pypi.yml`. Reason (source item 2): CLAUDE.md states the fork installs from git (`pipx install git+https://github.com/IronbellyOrg/IronClaude`) and the PyPI `superclaude` package is the upstream project.

Acceptance criteria:
- `.github/workflows/publish-pypi.yml` no longer exists.
- No other file was changed by this task.

## Task 4: Remove the dead framework checkout and plugin.json entry from pull-sync-framework.yml

In `.github/workflows/pull-sync-framework.yml` (source item 10):
- Delete the step named `Checkout Framework Repository (Source)` (planning-time lines 43-48), because `scripts/sync_from_framework.py` clones its own copy in `_clone_framework` (line 643) and never reads `framework-src`.
- In the `Commit and Push Changes` step, remove `plugin.json` from the `for p in commands/ agents/ .claude-plugin/plugin.json plugin.json` loop (planning-time line 103), because the repo has no root `plugin.json`.
- In the same step, reword or delete the comment directly above the loop (planning-time line 99, "ルートの plugin.json を追加…", i.e. "add root plugin.json"), which goes stale once the root `plugin.json` entry is gone.
- Leave every other step unchanged.

Acceptance criteria:
- `grep -n 'framework-src' .github/workflows/pull-sync-framework.yml` returns nothing.
- The add loop reads `for p in commands/ agents/ .claude-plugin/plugin.json; do`.
- `grep -n 'plugin.json' .github/workflows/pull-sync-framework.yml` shows no line that refers to a root `plugin.json`.
- The file parses with the YAML validity check from Constraints.

## Phase 2: Consolidate test.yml

## Task 5: Run the test job on Python 3.10 only, once, with coverage

Depends on: Task 1

In `.github/workflows/test.yml`, job `test` (source items 7 and 11):
- Remove the `strategy:` block with the `python-version: ["3.10", "3.11", "3.12"]` matrix; the job runs on Python 3.10. Set the job `name:` to `Test on Python 3.10`.
- Replace the whole `Set up Python ${{ matrix.python-version }}` step (planning-time lines 23-26): give it the literal name `Set up Python 3.10` and `python-version: "3.10"`. Task 6 later replaces this step with setup-uv; this edit keeps the file valid in between.
- Delete the steps `Verify UV installation` and `Verify package installation`.
- Replace the two steps `Run tests` and `Run tests with coverage` with one step that runs `pytest -v --tb=short --color=yes --cov=superclaude --cov-report=xml --cov-report=term`.
- Remove the `if: matrix.python-version == '3.10'` condition from the `Upload coverage to Codecov` step and keep the step otherwise unchanged.
- Keep the `make sync-dev` step and its comment before the pytest step.

Acceptance criteria:
- `grep -n 'matrix.python-version\|3\.11\|3\.12' .github/workflows/test.yml` returns nothing.
- Job `test` contains exactly one step that invokes `pytest`, and that command includes `--cov=superclaude --cov-report=xml`.
- In job `test`, the step that runs `make sync-dev` comes before the only `pytest` step.
- `Upload coverage to Codecov` still uploads `./coverage.xml` with `fail_ci_if_error: false`.
- The file parses with the YAML validity check from Constraints.

## Task 6: Replace the curl uv installer and setup-python pair with astral-sh/setup-uv in a venv

Depends on: Task 5

In `.github/workflows/test.yml` (source item 6), in every job that currently has both an `actions/setup-python@v5` step and an `Install UV` step running `curl -LsSf https://astral.sh/uv/install.sh | sh` (jobs `test`, `swarm-marker-matrix`, `lint`, `plugin-check`, `verify-deps`, `doctor-check`):
- Replace that pair with one `astral-sh/setup-uv@v<major>` step with inputs `python-version: "3.10"` and `activate-environment: true`. Reason: per the setup-uv README (Context7 `/astral-sh/setup-uv`, checked 2026-10-22, latest release v10.3.x), `python-version` only sets `UV_PYTHON` and `activate-environment` defaults to `false`; without the venv, `uv pip install --system` would target the runner's own Python rather than 3.10.
- Use the `@v<major>` tag form, matching every other action in this repo and the workflows README rule "Pin action versions (@v4, @v5)". Before writing it, confirm the major tag exists with `gh api repos/astral-sh/setup-uv/git/ref/tags/v<major>`; if it does not, use the full release tag instead and say so in the artifact.
- Change every `uv pip install --system -e ".[dev]"` to `uv pip install -e ".[dev]"`, and `uv pip list --system` to `uv pip list`, so `pytest`, `ruff`, `make`, and `superclaude` run from the activated venv in later steps.
- In job `doctor-check` (origin/master 43cb0116 added these after planning), the `Set up Node` and `Install Claude CLI` steps sit between `Set up Python` and `Install UV`, and the job also sets `permissions: contents: read` and checkout `persist-credentials: false`. Keep all four unchanged; put the setup-uv step where `Set up Python` was, before `Set up Node`.
- Note in the artifact that `make verify-deps` (Makefile: `uv run python scripts/verify_deps.py`) will now audit the venv holding the full `[dev]` dependency set, where today it audits a runtime-only `.venv`. The current baseline already lists that set, so it is expected to pass; this is a deliberate widening, not a regression.

Record in `./artifacts/t6-setup-uv-docs.md`: the doc source consulted, the major tag chosen, the tag-existence command output, and the verify-deps widening note.

Acceptance criteria:
- `grep -n 'install.sh\|setup-python\|--system' .github/workflows/test.yml` returns nothing.
- Every job that previously installed uv now has exactly one `astral-sh/setup-uv@` step with `python-version: "3.10"` and `activate-environment: true`.
- `./artifacts/t6-setup-uv-docs.md` exists and shows the tag-existence check succeeded for the tag used.
- Job `doctor-check` still runs `superclaude install` followed by `superclaude doctor --verbose`, and still has its `Set up Node`, `Install Claude CLI`, `permissions: contents: read` and `persist-credentials: false` lines.
- The file parses with the YAML validity check from Constraints.
- On the PR's first CI run, every job's setup log reports Python 3.10, and `doctor-check` and the `make verify-deps` step pass. A failure here is a defect of this task.

## Task 7: Merge lint, plugin-check and verify-deps into one job that also runs verify-sync and lint-architecture

Depends on: Task 6

In `.github/workflows/test.yml` (source items 3 and 4), replace the three jobs `lint`, `plugin-check` and `verify-deps` with one job `lint` (name `Lint, Plugin, Sync and Dependency Checks`). It does checkout, the setup-uv step from Task 6, and the dependency install once, then runs these steps in order:
- `ruff check src/ tests/`
- `ruff format --check src/ tests/`
- `pytest --trace-config 2>&1 | grep -q "superclaude"` with the existing success/failure echo
- `pytest --fixtures | grep -E "(confidence_checker|self_check_protocol|reflexion_pattern|token_budget|pm_context)"`
- `make verify-deps`
- `make sync-dev`
- `make verify-sync`
- `make lint-architecture`

The last three come from `.github/workflows/quick-check.yml` (steps `Sync src/superclaude/ → .claude/ mirrors`, `Verify component sync (src/ ↔ .claude/)`, `Lint architecture policy`). In job `test-summary`, change `needs:` to `[test, swarm-marker-matrix, lint, doctor-check]`. Its check script is replaced wholesale in Task 9, so leave it otherwise untouched here.

Acceptance criteria:
- `.github/workflows/test.yml` has no job keys `plugin-check:` or `verify-deps:`.
- Job `lint` has exactly one `astral-sh/setup-uv@` step and exactly one dependency-install step, and both come before the eight commands.
- Job `lint` runs all eight commands listed above, with `make sync-dev` before `make verify-sync`.
- `test-summary.needs` lists exactly `test`, `swarm-marker-matrix`, `lint`, `doctor-check`.
- The file parses with the YAML validity check from Constraints.

## Task 8: Delete quick-check.yml

Depends on: Task 7

Delete `.github/workflows/quick-check.yml` (source item 3). Everything it ran is now covered by `test.yml`: unit tests by the full `pytest` run in job `test`; ruff check/format, plugin load, verify-sync and lint-architecture by job `lint`.

Acceptance criteria:
- `.github/workflows/quick-check.yml` no longer exists.
- `grep -n 'make verify-sync\|make lint-architecture' .github/workflows/test.yml` returns one match each.

## Task 9: Shrink the test-summary check

Depends on: Task 7

In `.github/workflows/test.yml`, job `test-summary` (source item 5): keep the job, its `name`, `runs-on`, `needs`, and `if: always()`. Replace the `Check test results` step's multi-branch script with a step that has `if: contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled')` and `run: exit 1`. By the spec's choice, a skipped dependency no longer fails the aggregate.

Acceptance criteria:
- Job `test-summary` still has `if: always()` and the `needs` list from Task 7.
- Its only step has the `contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled')` condition and runs `exit 1`.
- No `needs.<job>.result != "success"` comparisons remain in the file.
- The file parses with the YAML validity check from Constraints.

## Phase 3: Simplify the PR guard workflows

## Task 10: Replace the Contract #3 detect step with a paths filter

Depends on: Task 1

In `.github/workflows/contract3-generator-constraint-lint.yml` (source item 8):
- Add `paths: ['**/gates.py', '**/structural_checkers.py', '**/*_validator.py']` under `on.pull_request`, keeping `types: [opened, edited, synchronize, reopened]` and `branches: [master, integration]`.
- Delete the `Detect validator/gate surface changes` step (planning-time lines 34-52).
- Delete the checkout step. This is a deliberate extension of spec item 8, which only said to drop `fetch-depth`: once the detect step is gone, the remaining step reads only `PR_BODY` from the event and needs no repository files.
- Remove `if: steps.detect.outputs.triggered == 'true'` from the PR-body step.
- Collapse the seven `::error::` echo lines (planning-time lines 63-69) into one `::error::` line that still names the trigger files and the required `## Generator-Constraint Considered` heading.
- Update the header comment to describe the paths filter instead of the detect step. Note in it that GitHub skips path-filtered workflows on diffs over 3,000 files when the matching file is not among the first 3,000; the old detect step had no such limit.

Acceptance criteria:
- `grep -n 'steps.detect\|fetch-depth\|git diff\|actions/checkout' .github/workflows/contract3-generator-constraint-lint.yml` returns nothing.
- The file has exactly one `::error::` line, and the heading regex `^##[[:space:]]+Generator-Constraint Considered[[:space:]]*$` is unchanged.
- The header comment mentions the 3,000-file path-filter limit.
- The file parses with the YAML validity check from Constraints.

## Task 11: Merge the three boundary-guard steps into one

In `.github/workflows/boundary-guard.yml` (source item 9), replace the steps `List boundary files changed in this PR`, `Annotate boundary touch` and `Write job summary` (planning-time lines 45-112) with one step. Pass base and head SHAs through `env:` as `BASE_SHA: ${{ github.event.pull_request.base.sha }}` and `HEAD_SHA: ${{ github.event.pull_request.head.sha }}`. The step does these things in this order:
- Emit the existing `::warning title=Mechanical-merge boundary touched::...` annotation text unchanged, as the first command, so a later failure cannot suppress it.
- Append the summary heading and four-guard list to `$GITHUB_STEP_SUMMARY`, then the `### Files touched in this PR` heading and an opening code fence.
- Run `git diff --name-only "$BASE_SHA" "$HEAD_SHA" -- <the five boundary paths> >> "$GITHUB_STEP_SUMMARY" || echo "(diff unavailable)" >> "$GITHUB_STEP_SUMMARY"` outside any heredoc.
- Append the closing code fence and the reviewer checklist.

If quoted heredocs (`<<'EOF'`) carry the static text, use plain backticks inside them. The original `echo` lines escape backticks as `` \` `` on 7 lines (14 escape sequences, planning-time lines 80, 84, 87, 90, 103, 107, 111), and copying those escapes into a quoted heredoc would print stray backslashes. Do not use unquoted heredocs for text containing backticks. Remove the `mapfile` and `GITHUB_OUTPUT` round trip. Keep the checkout with `fetch-depth: 0`, the `on.pull_request.paths` list, and the header comment.

Before committing, render the step locally: run its script body with `GITHUB_STEP_SUMMARY` pointing at a temporary file and real or dummy SHAs, and compare the result with the old three steps' rendered summary. The only allowed difference is the empty-file-list case: the old step printed one blank line inside the code fence, the new one prints none. Save both renders and the comparison to `./artifacts/t11-render-diff.txt`.

Acceptance criteria:
- `grep -n 'mapfile\|GITHUB_OUTPUT\|steps.changed' .github/workflows/boundary-guard.yml` returns nothing.
- The job has exactly two steps: checkout and the merged step.
- The merged step executes `git diff --name-only` as a command (not as literal text), and its first command emits the `::warning` annotation.
- The warning text, the four-guard list and all five reviewer checklist items render unchanged in `$GITHUB_STEP_SUMMARY`, as shown by `./artifacts/t11-render-diff.txt`, and the render contains no stray backslash before a backtick.
- The file parses with the YAML validity check from Constraints.

## Phase 4: Document the result

## Task 12: Update the workflows README

Depends on: Task 2, Task 3, Task 8, Task 9

Update `.github/workflows/README.md` (source item 12):
- Remove the `quick-check.yml`, `publish-pypi.yml` and `readme-quality-check.yml` sections.
- Describe `test.yml` as: one Python 3.10 test job with coverage upload, the swarm imm/inv lanes, one merged lint job (ruff check, ruff format, plugin check, verify-deps, sync-dev, verify-sync, lint-architecture), the doctor check, and the test-summary aggregate.
- Add one-line entries for `boundary-guard.yml`, `contract3-generator-constraint-lint.yml` and `pull-sync-framework.yml`.
- Redraw the CI/CD pipeline diagram so it no longer shows a Quick Check box or Python 3.11/3.12.
- In the Troubleshooting section, replace the `curl ... install.sh` explanation with the setup-uv action from Task 6.
- In "Adding a New Workflow", change "Follow existing structure (checkout, setup-python, install UV)" (planning-time line 143) to "checkout, astral-sh/setup-uv".
- In Maintenance, replace "Edit `matrix.python-version` in `test.yml`" with the setup-uv `python-version` input. In "Modifying Test Strategy", remove the `quick-check.yml` line and change "test.yml: For comprehensive validation (full matrix)" (planning-time line 156) so it no longer says "full matrix".
- In Best Practices, remove "Fail fast: Use `-x` flag in pytest for quick-check", and remove or reword "Matrix testing: Test on multiple Python versions" (planning-time line 164). Keep "Pin action versions (@v4, @v5)".

`scripts/README.md` also mentions a deleted workflow. It is outside this plan's scope: list it in the implementation report as a leftover and do not edit it.

Acceptance criteria:
- `grep -rn 'quick-check\|publish-pypi\|readme-quality-check\|3\.11\|3\.12\|install\.sh' .github/` returns nothing.
- `grep -n 'setup-python\|Matrix testing\|full matrix' .github/workflows/README.md` returns nothing.
- The README names every workflow file that still exists in `.github/workflows/`, and no file that does not.
