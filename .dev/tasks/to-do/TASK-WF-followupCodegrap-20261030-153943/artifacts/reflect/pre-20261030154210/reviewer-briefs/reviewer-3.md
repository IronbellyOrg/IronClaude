# Reviewer 3 brief (persona: refactorer)

You are a read-only Tier-2 reviewer for a /sc:reflect UC-1 (pre-execution) run. Plan under review = the tasklist in your grounding hunks (cite it as plan:<line>); driving spec = source.md (cite source.md:<line>); repo files cite as path:line. Start adversarial: assume defects exist. Verify each T1 finding in your slice (confirm, refute with evidence, or correct its severity) and add NEW findings the T1 card missed. Classify each finding's origin as plan or spec-inherited, and its deviation class vs the spec as one of authorized | necessary | drift | regression (regression = the plan contradicts a spec acceptance criterion or constraint). Do not execute anything.

## T1 card excerpt

## Summary

Verdict: **NOT READY. Revise before `/sc:implement`.** Confidence: 0.80.

Two critical defects. (1) Task 1 cherry-picks a `docs(plan): codegraph release monitor` commit that does not exist: every planning file is untracked, so `test -n "$PLAN"` aborts the first task (T1-01). (2) The workflow design leaves the `contents: write` job token in `.git/config` while `prove` runs the third-party codegraph binary on the same runner, so the "no token in prove" control has no effect (T1-26).

The important defects group into four kinds:
- Evidence paths: the plan's `./artifacts/` resolves to the project-root folder, which is never staged, and `$PKG` is unbound in the spec's acceptance blocks under `set -u` (T1-02, T1-03).
- Weak or racy post-merge checks: either-or grep, wrong run id, no merge gate (T1-04, T1-05, T1-06).
- Spec contradictions: push ordering, stdlib-only versus `install_mcp`, sandbox HOME/PATH layout, the infra counter, and `--tag` with the current pin (T1-14 to T1-18).
- Plan gaps: the YAML action executor is untested (T1-21), the branch switch breaks `/sc:implement`'s own state (T1-27), Task 5 drops the matrix and `dry_run` rules (T1-34), and tasks point to commands instead of stating them (T1-40).

Coverage is otherwise good: every spec section §0-§7 and every Decisions row maps to a plan task. The cited code line numbers all hold on `origin/master`, and #329 is already merged (2f10a0e1).

## Stand-alone defects

- **T1-40** | important | plan | plan:118,132,55,68,110 | Several tasks point to commands instead of stating them. Task 7 says "same command as Task 1", Task 8 needs Task 7's PR URL, and the Task 2 mutation check, Task 3 import check and Task 6 awk check appear only as "source §4 T1/T2/T5". `/sc:implement` reviews each task against its own body plus Constraints, so the exact commands are not checkable. | Write the literal command blocks into each task.
- **T1-41** | minor | plan | plan:63,76 | Tasks 3 and 4 do not name the files they read: `src/superclaude/cli/install_codegraph.py` (input of `read_pin`/`rewrite_pin`, `acquire`, `MCP_TOOLS`) and `src/superclaude/cli/install_mcp.py` (`_codegraph_entry` :862, `_run_argv` :804). | Add a "Reads:" line naming both.
- **T1-42** | minor | plan | plan:92 | Task 5 does not name `.github/workflows/test.yml`, which is both the setup precedent and the dispatch target that needs `workflow_dispatch`. | Name it.
- **T1-43** | minor | plan | plan:76 | Task 4 describes the live harness in prose only. The `REAL_SUM` / `jq` guard, the `home=` parse and the sandbox delete are in source.md:277-284 and not in the task. | Write the block into Task 4, corrected for T1-03, T1-12 and T1-16.

## Structural signals

- S_scope = 8 (plan `## Task 1` to `## Task 8`).
- S_domains = 4: code (`scripts/codegraph_release.py`), tests (`tests/cli/...`, `tests/unit/test_cli_doctor.py`), docs (`docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`, `.github/workflows/README.md`, `CHANGELOG.md`) and ci (`.github/workflows/codegraph-release-monitor.yml`). Config: none (`pyproject.toml`, `Makefile` and the dependency baseline stay unchanged, source.md:51).
- Live and external surfaces: GitHub API, `gh attestation`, upstream downloads, a post-merge workflow dispatch, and issue #323 comments in every task.

Severity counts: critical 2 (T1-01, T1-26); important 14 (T1-02, 03, 04, 05, 06, 14, 15, 16, 17, 18, 21, 27, 34, 40); minor 27. Total 43.

## Grounding hunks

### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/TASK-WF-followupCodegrap-20261030-153943.md:1-138
```markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-followupCodegrap-20261030-153943
version: "1"
priority: Medium
created_date: "2026-10-30"
---

# codegraph upstream release monitor (follow-up to Phase 2, issue #323)

Source: ./source.md
Goal: A scheduled workflow in `IronbellyOrg/IronClaude` finds an eligible newer `colbymchenry/codegraph` release, verifies it (SHA-256 against `SHA256SUMS` plus `gh attestation verify -R colbymchenry/codegraph`), rewrites the pin in `src/superclaude/cli/install_codegraph.py`, proves it in an isolated HOME, and opens a PR on `IronbellyOrg/IronClaude` only, with the release notes; the bump logic lives in `scripts/codegraph_release.py` with offline unit tests.

## Constraints

- Precondition: PR #329 (https://github.com/IronbellyOrg/IronClaude/pull/329) is merged to `master`; work happens on `ironbelly/feat-codegraph-release-monitor`, branched from `origin/master` (source §0 "Scope", §4 T0).
- PRs only on `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3` (fallback `gh pr create --repo IronbellyOrg/IronClaude`); never a bare `gh pr create`, also inside the workflow; never push to `upstream` (source §6 hard rules).
- Never stage a `.claude/` path; `.dev/tasks` is always staged with `git add .dev/tasks`, the package and its `artifacts/` included; feature branch only.
- Never run `superclaude install`, `claude mcp add/remove`, `./update.sh` or `codegraph install` without `--print-config` against the real HOME; every live proof uses a sandbox HOME (source §2.5, §6).
- Never edit historical `.dev/` artifacts (`.dev/codegraph-migration/evidence/P2-*`); never run `tests/cli/eval/`; after a full-suite run restore `.dev/releases/current/cliEval/evidence/T02.15/perf.json` with `git checkout --`.
- No new dependency: stdlib plus the `gh` CLI; `scripts/codegraph_release.py` imports only stdlib modules (source §1 "Not changed").
- The workflow never merges, approves or auto-merges a PR and never pushes to `master`; it never pushes or force-pushes an existing branch (source §2.4, decision M-c).
- Every acceptance command runs from the worktree root under `bash -euo pipefail`, one condition per line, negative checks as `if cmd; then exit 1; fi`; every `uv run pytest` uses `-p no:cacheprovider` (source §0 "Evidence rule").
- Task evidence goes under `./artifacts/` in this package; delivery files are repo-relative.
- After each task's commit, post the source §5 progress comment on issue #323 with `gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file <file>`, and nowhere else.
- Decisions the executor meets follow source §6 (simple: self; mid: `/sc:adversarial --compare ... --depth quick`; complex: `/sc:adversarial --compare ...`), logged in `.dev/codegraph-migration/decisions/MX-log.md`.

## Phase 1: Preconditions and a single-source pin

## Task 1: Create the feature branch from master and record the test baseline

Implements source §4 T0. Confirm PR #329 is merged (`gh pr view 329 --repo IronbellyOrg/IronClaude --json state --jq .state` prints `MERGED`; if not, post one issue #323 comment and wait, source §7 item 1). Run `git fetch origin`, `git switch -c ironbelly/feat-codegraph-release-monitor origin/master`, then cherry-pick the planning commit found with `git log --format=%H -1 --grep '^docs(plan): codegraph release monitor' ironbelly/codegraph-release-monitor`. Set `PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1)` and `mkdir -p "$PKG/artifacts"`. Run `make sync-dev`, then the full suite excluding `tests/cli/eval` and write the sorted failing test ids to `./artifacts/baseline-failures.txt` with the exact command in source §4 T0; restore `perf.json`. Print the current `VERSION` line of `src/superclaude/cli/install_codegraph.py`; a value other than `1.6.2` is allowed (source §4 T0 commit note).

Acceptance criteria:
- `git branch --show-current` prints `ironbelly/feat-codegraph-release-monitor` and `git merge-base --is-ancestor origin/master HEAD` exits 0.
- `.dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md` exists on the branch (the planning commit was cherry-picked).
- `./artifacts/baseline-failures.txt` exists (it may be empty when the suite is green).
- `test -z "$(git status --short -- src tests scripts docs .github CHANGELOG.md)"` exits 0.
- Committed as `chore(tasks): record the test baseline for the codegraph release monitor (#323)` with `.dev/tasks` staged.

## Task 2: Make the codegraph pin a one-file change in tests and docs

Depends on: Task 1

Implements source §1 rows F1-F5 and §4 T1 (fact 3 in source §0 lists every literal). Create `tests/cli/fixtures/codegraph-SHA256SUMS.txt` as a copy of `.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt` (header line plus the four `codegraph-<asset>.tar.gz` lines) and point `test_u2_pin_integrity` in `tests/cli/test_install_codegraph.py` at it; leave the `.dev/` file unchanged. Replace every literal `1.6.2` / `v1.6.2` in `tests/cli/test_install_codegraph.py` (lines 38, 45, 96, 151, 171, 175, 237, 270, 639, 640, 659, 691 at `e62ed152`), `tests/unit/test_cli_doctor.py` (241, 287) and `tests/cli/test_update_command.py` (355) with `install_codegraph.VERSION` / `install_codegraph.TAG` (`cg.VERSION` / `cg.TAG` where the module is imported as `cg`). Add `test_no_pinned_version_literals_in_tests` asserting those three files contain no literal of the current `install_codegraph.VERSION`. In `docs/user-guide/mcp-installation.md` (lines 9, 28, 31) and `docs/reference/mcp-server-guide.md` (lines 29, 43) replace the literal version with "the pinned version" and say how to read it (`superclaude install --list` prints `codegraph MCP (pinned vX.Y.Z; user scope)`). Do not edit `src/superclaude/cli/install_codegraph.py`.

Acceptance criteria:
- `cmp <(tail -n +2 .dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt) <(tail -n +2 tests/cli/fixtures/codegraph-SHA256SUMS.txt)` prints nothing.
- `uv run pytest -p no:cacheprovider -q tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py tests/cli/test_install_mcp_registry.py` passes.
- `git grep -n -E '1\.6\.2' -- tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py docs/user-guide/mcp-installation.md docs/reference/mcp-server-guide.md` prints nothing.
- `uv run ruff check` and `uv run ruff format --check` on the three test files pass; `git diff --quiet -- src/superclaude/cli/install_codegraph.py .dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt` exits 0.
- Committed as `test(codegraph): derive the pinned version from install_codegraph in tests and docs`; then the post-commit mutation check in source §4 T1 (throwaway worktree `.dev/worktrees/m-mutation`, `VERSION = "9.9.9"`, the three test files pass with only `test_u2_pin_integrity` deselected, worktree removed) passes, with its output saved to `./artifacts/t2-mutation.log`.

## Phase 2: Offline-tested release logic

## Task 3: Add the pure bump logic in scripts/codegraph_release.py with unit tests

Depends on: Task 2

Implements source §2.2 (constants and every pure function: `parse_version`, `read_pin`, `pick_candidates`, `parse_sha256sums`, `rewrite_pin`, `render_sums_fixture`, `tool_problems`, `entry_drift`, `build_body`, `classify`, `route`, `fingerprint`), the selection rules of source §2.4 (two lines, `MIN_AGE_DAYS = 14`, no fallback, per-version branch `codegraph/bump-<tag>`, declined versions, supersede, deleted releases, stall warning at 28 days), the classification and routing tables of source §2.5, and the body rules of source §2.6. Create `scripts/codegraph_release.py` (stdlib only, not packaged), `tests/cli/test_codegraph_release.py` (loads the script with `importlib.util.spec_from_file_location`, precedent `tests/skills/test_workflow_archive.py:26-28`) and fixtures `tests/cli/fixtures/codegraph_release/releases.json`, `tests/cli/fixtures/codegraph_release/SHA256SUMS` and `tests/cli/fixtures/codegraph_release/print-config-claude.txt`, built as source §4 T2 describes. Tests: R1-R11 and R17-R19 of source §3, including the boundary ages, the no-fallback case, the backport case, the pending-major-plus-eligible-minor case and the 2026 replay (bumps on 08-04 to v1.5.0, 09-09 to v1.6.0, 10-17 to v1.6.2).

Acceptance criteria:
- `uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release.py` passes and covers R1-R11 and R17-R19 (one test function or parametrized case per listed case).
- `uv run ruff check` and `uv run ruff format --check` on `scripts/codegraph_release.py tests/cli/test_codegraph_release.py` pass.
- The stdlib-only import check in source §4 T2 exits 0 (no import outside the listed stdlib modules).
- `rewrite_pin` on the real `install_codegraph.py` changes exactly five lines and its output passes `ruff format --check -` (test R6).
- Committed as `feat(codegraph): add offline-tested release bump logic`.

## Task 4: Add the I/O subcommands, the stdio MCP client and the live harness proof

Depends on: Task 3

Implements source §2.2 I/O wrappers (`_gh`, `_run`, `mcp_tool_names`) and CLI subcommands `check`, `fetch`, `bump`, `prove`, `body`, `route`, plus the five proof stages and the isolation asserts of source §2.5. Edit `scripts/codegraph_release.py` and `tests/cli/test_codegraph_release.py`; create `tests/cli/fixtures/codegraph_release/fake_mcp_server.py`. Tests R12-R16 of source §3. Then run the live block of source §4 T3 on the current pin with a sandbox HOME (record the real `~/.claude.json` `.mcpServers` hash first): `check` writes `result=none`, `fetch --tag v1.6.2` verifies hashes and attestations, `prove --keep` passes all five stages and reports `home=`, and that sandbox binary's `install --print-config claude` output replaces `tests/cli/fixtures/codegraph_release/print-config-claude.txt`; delete the sandbox. Save the proof log as `./artifacts/live-prove.log` and the check and fetch outputs as `./artifacts/live-check.txt` and `./artifacts/live-fetch.txt`.

Acceptance criteria:
- `uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release.py` passes, including R12-R16.
- `uv run ruff check` and `uv run ruff format --check` on `scripts/codegraph_release.py tests/cli/test_codegraph_release.py tests/cli/fixtures/codegraph_release/fake_mcp_server.py` pass.
- `./artifacts/live-check.txt` contains the line `result=none`; `./artifacts/live-fetch.txt` contains `result=ok`; `./artifacts/live-prove.log` shows all five stages passing and the prove output contains `result=pass`.
- `tests/cli/fixtures/codegraph_release/print-config-claude.txt` contains `"mcpServers"` and comes from the real v1.6.2 binary.
- The real `~/.claude.json` `.mcpServers` hash after the run equals the hash before it; `git diff --quiet -- src/superclaude/cli/install_codegraph.py` exits 0.
- Committed as `feat(codegraph): verify, prove and describe a codegraph release candidate`, with `.dev/tasks` staged.

## Phase 3: Scheduled workflow

## Task 5: Add .github/workflows/codegraph-release-monitor.yml and its static test

Depends on: Task 4

Implements source §2.3 (triggers `schedule` cron `23 6 * * *` and `workflow_dispatch` inputs `dry_run`, `tag`, `min_age_days`; job `if: github.repository == 'IronbellyOrg/IronClaude'`; permissions exactly `contents`, `pull-requests`, `issues`, `actions` write; concurrency group; `ubuntu-latest`, 30 minutes; checkout, `astral-sh/setup-uv@v10.3.2` with Python 3.10, `uv pip install -e ".[dev]"`; one step per subcommand; push only after `fetch` passed; PR via `gh pr create --repo "$GITHUB_REPOSITORY"` with `--draft` when `route` says so; PR step `if: always()`; `gh workflow run test.yml --ref <branch>`; optional `CODEGRAPH_MONITOR_ASSIGNEE` variable; no token in the `prove` step) and the failure steps of source §2.5 (label step with `continue-on-error: true`; infrastructure counter via `gh run list ... --json conclusion`). Create `tests/cli/test_codegraph_release_workflow.py` with the static checks listed in source §3 (precedent `tests/swarm/test_merge_boundary_guards.py`, `yaml.safe_load`).

Acceptance criteria:
- `uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release_workflow.py` passes and checks every item in the source §3 workflow paragraph (triggers and inputs, job `if`, exact permissions, `--repo "$GITHUB_REPOSITORY"` on every `gh pr create`, no `SuperClaude-Org`, no token in `prove`, `always()` on the PR step, no force push, push gated on `fetch` `result == 'ok'`, label step `continue-on-error`, no `gh pr merge` and no `--auto`).
- `grep -n 'SuperClaude-Org' .github/workflows/codegraph-release-monitor.yml` prints nothing, and no `gh pr create` line lacks `--repo "$GITHUB_REPOSITORY"`.
- `uv run ruff check` and `uv run ruff format --check` on `tests/cli/test_codegraph_release_workflow.py` pass; `actionlint` passes too if it is on PATH.
- Committed as `ci(codegraph): add the scheduled codegraph release monitor`.

## Phase 4: Documentation and delivery

## Task 6: Document the monitor in the workflows README, CHANGELOG and MCP install guide

Depends on: Task 5

Implements source §1 rows F10, F11 and the F5 paragraph, and source §4 T5. Add a `codegraph-release-monitor.yml` section to `.github/workflows/README.md`; add an `## [Unreleased]` Added entry to `CHANGELOG.md` (do not edit the historical v1.6.2 line); add a "How the pin is updated" paragraph to `docs/user-guide/mcp-installation.md` covering what the monitor does, the selection rules of source §2.4 (14 days, newest only, majors as drafts), what each failure produces (source §2.5) and the manual run `gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude -f dry_run=true`.

Acceptance criteria:
- `grep -q 'codegraph-release-monitor.yml' .github/workflows/README.md` exits 0.
- The `## [Unreleased]` section of `CHANGELOG.md` mentions "codegraph release monitor" (the awk check in source §4 T5 exits 0).
- `grep -q 'codegraph-release-monitor' docs/user-guide/mcp-installation.md` exits 0, and the paragraph names the 14-day rule, the draft for majors, the integrity issue and the manual dry-run command.
- Committed as `docs(codegraph): document the codegraph release monitor`.

## Task 7: Run the final gate and open the PR on IronbellyOrg/IronClaude

Depends on: Task 6

Implements source §4 T6. Run `make sync-dev`, the full suite excluding `tests/cli/eval` into `./artifacts/final-failures.txt` (same command as Task 1), restore `perf.json`, and re-run `uv run python scripts/codegraph_release.py prove` on the final tree into `./artifacts/final-prove.log`. Do the repo CLAUDE.md pre-PR checks (`git remote -v`; `gh repo view --json nameWithOwner -q .nameWithOwner` prints `IronbellyOrg/IronClaude`; `git fetch origin && git log master..origin/master`, rebase onto `origin/master` if the fork moved). Then open the PR in Claude Code with `/sc:pr-submit --monitor 3 --head ironbelly/feat-codegraph-release-monitor --title "feat(codegraph): scheduled codegraph release monitor (#323)" --body "<summary, test evidence, live proof log path, link to the spec>"`. List the debate items flagged for the user (source `## Decisions`, last paragraph) and source §7 item 5 (Coder bake) in the issue #323 comment.

Acceptance criteria:
- `comm -13 ./artifacts/baseline-failures.txt ./artifacts/final-failures.txt` prints nothing (no new failure).
- `./artifacts/final-prove.log` and the prove output show `result=pass`.
- `uv run ruff check src/ tests/ scripts/codegraph_release.py`, `uv run ruff format --check src/ tests/ scripts/codegraph_release.py` and `make verify-sync` pass; `test -z "$(git status --short -- src tests scripts docs .github CHANGELOG.md)"` exits 0.
- The PR URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/` and is recorded in `./artifacts/pr-url.txt`.

## Phase 5: Post-merge live run

## Task 8: Run the merged monitor on master and record both runs

Depends on: Task 7

Implements source §4 T7, only after a person merged the Task 7 PR (source §7 item 2). Dispatch `gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude --ref master -f dry_run=true -f tag=v1.6.2`, watch it with `gh run watch <id> --repo IronbellyOrg/IronClaude --exit-status`, then dispatch one normal run. Save both run URLs and the relevant log lines to `./artifacts/post-merge-runs.md`, and post the final issue #323 comment with both URLs.

Acceptance criteria:
- The dry run exits 0 and its log shows `fetch` `result=ok` and `prove` `result=pass`; it opens no PR and no issue.
- The normal run exits 0 with `result=none`, or, if a release became eligible, opens exactly one PR whose URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`.
- `gh pr list --repo IronbellyOrg/IronClaude --search 'bump codegraph pin' --state open` shows at most one open PR per tag.
- `./artifacts/post-merge-runs.md` holds both run URLs and the cited log lines.
```
### .github/workflows/test.yml:1-40
```yaml
name: Tests

on:
  push:
    branches: [master, integration]
  pull_request:
    branches: [master, integration]
  workflow_dispatch:

jobs:
  test:
    name: Test on Python 3.10
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up uv and Python 3.10
        uses: astral-sh/setup-uv@v10.3.2
        with:
          python-version: "3.10"
          activate-environment: true

      - name: Install dependencies
        run: |
          uv pip install -e ".[dev]"
          uv pip list

      - name: Sync src/superclaude/ → .claude/ mirrors
        # Required: several audit tests assert byte-identical parity between
        # src/superclaude/{skills,agents,commands,hooks,templates} and the
        # .claude/ mirrors. Mirrors are gitignored, so CI must materialise them
        # before pytest runs.
        run: |
          make sync-dev

      - name: Run tests with coverage
        run: |
          pytest -v --tb=short --color=yes --cov=superclaude --cov-report=xml --cov-report=term
```
### .github/workflows/test.yml:130-175
```yaml
  doctor-check:
    name: SuperClaude Doctor Check
    runs-on: ubuntu-latest
    # `superclaude install` runs the required codegraph phase (it downloads the pinned,
    # checksum-verified codegraph release and registers it through the Claude CLI) and then
    # retires stale user-scope MCP registrations; keep the token read-only and out of
    # .git/config while it runs.
    permissions:
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Set up uv and Python 3.10
        uses: astral-sh/setup-uv@v10.3.2
        with:
          python-version: "3.10"
          activate-environment: true

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: "22"

      # The codegraph phase of `superclaude install` needs `claude --version` to succeed before it
      # downloads or registers anything, and registers codegraph with `claude mcp add-json`; the
      # retire step uses the same CLI. Without this step the job would fail at the codegraph phase.
      - name: Install Claude CLI
        run: |
          npm install -g @anthropic-ai/claude-code@2.1.286
          claude --version

      - name: Install dependencies
        run: |
          uv pip install -e ".[dev]"

      - name: Install native components
        run: |
          superclaude install

      - name: Run doctor command
        run: |
          superclaude doctor --verbose
```

## Coverage slice

Coverage: Pass 1 parsed 0 ids; Pass 2 inferred 338 rows (artifacts/inferred-requirements.yaml); containment matched 111 (coverage_pct_union 0.3284, artifacts/coverage-matrix.yaml); by-reference triage of the 227 unmatched rows (artifacts/unmapped-triage.yaml):
```yaml
total_unmapped: 227
covered_by_reference: 222
needs_review:
- INF-042
- INF-043
- INF-045
- INF-046
- INF-047
```
The 5 needs-review rows are spec §2.1 (source.md:57-72): no plan task cites §2.1.
