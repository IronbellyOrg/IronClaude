---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-ripOutTheFramewo-20261023-134610
version: "1"
priority: Medium
created_date: "2026-10-23"
---

# Remove upstream sync automation and coverage uploads

Source: ./source.md
Goal: Remove the fork's upstream framework sync automation and external coverage upload while retaining pytest coverage measurement and all content previously imported from upstream.

## Constraints

- This is a plan only. Implementation starts separately with `/sc:implement`.
- Before implementation edits, use a dedicated feature branch in this checkout, never `master` or `integration`. Preserve pre-existing work and record the starting commit, branch, and working-tree status in `./artifacts/t1-baseline.txt` for later comparisons.
- Limit changes outside `.dev/` to deleting `.github/workflows/pull-sync-framework.yml`, `scripts/sync_from_framework.py`, and `docs/.framework-sync-commit`, and editing `.github/workflows/test.yml` and `.github/workflows/README.md` as described below. If execution discovers additional tracked references, report them instead of silently broadening the file list or accepting an incomplete final check.
- Do not modify `src/superclaude/templates/documents/readme_template.md`, including its generic coverage badge. Do not alter pytest configuration or coverage dependencies in `pyproject.toml`.
- Do not revert content brought in by previous upstream syncs, including commands, agents, and plugin metadata. Do not run the sync script as a check: it clones and rewrites content.
- Do not close PR 283 in `IronbellyOrg/IronClaude` or delete `sync/framework` on `origin`. The implementation's final report must list both as untouched, pending the user's explicit approval for any later cleanup. Do not claim their live remote state without checking it.
- No commit, push, or PR creation is authorized by this plan. Any subsequently authorized PR must target `IronbellyOrg/IronClaude`, never the public parent repository, and must follow the repository's pre-PR checks.
- Use UV for any Python checks. Keep task-owned evidence and runnable checks under `./artifacts/`. Final independent whole-plan verification and archiving belong to the executor, not to a separate task.

## Phase 1: Remove the two automated integrations

## Task 1: Delete the framework sync workflow, script, and state file

Read `./source.md` and the three deletion targets. Recheck tracked references and script consumers before deleting anything. Planning-time searches found references only within the deletion targets and the two workflow files edited by this plan; searches of tests found no consumers of the script's named classes. These searches are evidence, not a reason to skip a fresh check.

After recording the baseline required by Constraints, delete exactly `.github/workflows/pull-sync-framework.yml`, `scripts/sync_from_framework.py`, and `docs/.framework-sync-commit`. Deleting the workflow removes both its scheduled and manual entry points; do not replace it with another sync mechanism. Leave previously synced repository content intact. Record deletion and reference-check evidence in `./artifacts/t1-removal.log`.

Acceptance criteria:
- All three target files are absent, including symlinks, and the diff against the recorded starting commit shows their deletion. No other content is changed by this task.
- The deleted workflow's only external script call was the deleted sync script, and its sync-state reads/writes targeted the deleted marker; fresh reference searches identify no surviving caller that requires changes outside the two workflow files named in this plan. Any unexpected caller is reported as a blocker, not ignored.
- Existing upstream-derived commands, agents, and plugin metadata have no implementation changes. PR 283 and the remote `sync/framework` branch receive no mutation.

## Task 2: Remove the coverage upload without changing coverage measurement

Depends on: Task 1

Read `./source.md`, `.github/workflows/test.yml`, and the baseline in `./artifacts/t1-baseline.txt`. Remove only the complete test-job step named `Upload coverage to Codecov`, including its action and all inputs. Preserve the `Run tests with coverage` step and its exact command:

```text
pytest -v --tb=short --color=yes --cov=superclaude --cov-report=xml --cov-report=term
```

Do not change other steps, jobs, triggers, permissions, or test configuration. Write a small runnable check at `./artifacts/check_test_workflow.py`, executed with `uv run python`, and save its command and result in `./artifacts/t2-workflow-check.log`. Use the existing PyYAML dependency from `pyproject.toml`; do not add dependencies or tracked test files for this removal-only change.

Acceptance criteria:
- The named upload step and all its inputs are gone. The file otherwise equals the starting-commit version with only that exact step block removed; the check asserts this directly so unrelated changes cannot slip through.
- The runnable check parses the surviving YAML and asserts the test job retains exactly one `Run tests with coverage` step with the exact command above, preserving both XML and terminal coverage output.
- `pyproject.toml` and the protected README template are unchanged from the baseline. No coverage measurement options, dependencies, or test jobs are removed.
- The runnable check exits successfully and its recorded output demonstrates the assertions ran. This is a local workflow check, not a claim that a hosted GitHub Actions run has occurred.

## Phase 2: Align the workflow documentation

## Task 3: Remove documentation for the retired integrations

Depends on: Task 2

Read `./source.md`, `.github/workflows/README.md`, and the updated `.github/workflows/test.yml`. Make these targeted documentation deletions and wording changes:
- Remove section 4, `pull-sync-framework.yml - Framework Sync`, including its scheduling and pull-request description.
- Remove the `Upload coverage to Codecov` bullet from the test-job list.
- Change the Coverage Reporting sentence to say that coverage reports are generated on Python 3.10, without an external-upload claim. Retain the local coverage instructions and command unchanged.
- Remove the entire `Coverage upload fails` troubleshooting subsection. Both existing bullets concern the removed upload step: its non-blocking setting and repository token.
- Remove the now-obsolete `Non-blocking coverage` best-practice item about upload errors and renumber the remaining best-practice items without other edits.

Record the documentation checks, scope diff, and final reference search command and exit status in `./artifacts/t3-reference-check.log`.

Acceptance criteria:
- The workflow inventory lists the three remaining workflows, the coverage section still documents local measurement, and no documentation claims a coverage upload or provides troubleshooting for a deleted integration.
- Run the following tracked-working-tree search after all three tasks. Success means exit code 1 with no matches; exit code 0 means remaining references and any other nonzero exit is a failed check. Do not hide errors with `|| true`.

```bash
git grep -n -i -E 'pull-sync-framework|sync_from_framework|framework-sync-commit|codecov' -- . ':!.dev' ':!src/superclaude/templates/documents/readme_template.md'
```

- Separately confirm the protected template remains byte-identical to the starting commit, including its generic badge. The search exception does not authorize edits to it.
- The final implementation diff outside `.dev/` contains exactly the three requested deletions and the two workflow-file edits, with no reversion of earlier synced content. Task 2's runnable workflow check still passes.
- The final implementation report names PR 283 in `IronbellyOrg/IronClaude` and `origin`'s `sync/framework` branch as untouched and pending the user's approval for any later closure or deletion. It reports observed local checks separately from any hosted CI work that was not run.
