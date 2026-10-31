# Reviewer 2 brief (persona: qa)

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

## Coverage gaps

Format: id | severity | origin | citation | claim | fix.

- **T1-34** | important | plan | plan:92 vs source.md:110 | Task 5 drops the two-line run model (one matrix leg per line, `max-parallel: 1`, fresh checkout per leg) and the `dry_run` semantics (run check, fetch, bump, tests and prove; print diff and body; no push, no PR, no issue). A reviewer checking Task 5 against its own body cannot flag a workflow that handles only one line or pushes during a dry run. | Add both rules to Task 5 and a static check that every push, PR, issue and label step is gated on `inputs.dry_run != true`.
- **T1-35** | minor | plan | plan:92 vs source.md:115,117-120 | Task 5 omits the commit author and message format, `fetch-depth: 0`, `GH_TOKEN` only on `gh` steps, the `stage=aborted` behaviour draft, the CI link in the PR body and the step summary on every path. | List them in Task 5.
- **T1-36** | minor | plan | plan:95 vs source.md:202 | Task 5's acceptance summary of the static test leaves out "the schedule passes no `min_age_days`", "every `run:` that calls the script uses `scripts/codegraph_release.py`", `--force-with-lease` and "the push step comes after the `fetch` step". | List every §3 workflow check one by one.
- **T1-37** | minor | plan | plan:17-29 vs source.md:31,210 | The Constraints drop two rules: run `git status --short` after every task and treat unintended tracked changes as defects, and stage `.dev/codegraph-migration/decisions/MX-*` when a decision is taken. | Add both to Constraints.
- **T1-38** | minor | plan | plan:76 vs source.md:102,148 | Task 4 names the §2.5 stages and isolation asserts but not three rules: kill daemons by process group, cap the log at the first 200 lines per step, and use the `fetch` order (byte length against the API `size`, then sums, then hash, then attestation on 5 files). | Name them in Task 4.
- **T1-39** | minor | plan | plan:48 vs source.md:43 | Task 2 drops the F5 docs pointer to `install_codegraph.py:26-27` as the source of the pin. | Add it.
- See also T1-06 (Task 8 has no merge gate) and T1-13 (two dropped acceptance checks).

## Acceptance-command defects

- **T1-01** | critical | spec-inherited | source.md:219-221; plan:35 | The planning commit that Task 1 cherry-picks does not exist. `git log --oneline --all --grep 'docs(plan)'` returns only the Phase 1 and Phase 2 plan commits (5285492f, 7952062e, 21ea7cf8, 79239d00). The spec, the decisions `M-*`, `review/M-result.md` and this task package are all untracked (`git status --short`). So `test -n "$PLAN"` fails and Task 1 aborts, and no task creates that commit. | Add a step before the switch that commits the planning files on `ironbelly/codegraph-release-monitor` with subject `docs(plan): codegraph release monitor (#323)`, listing exact paths (spec, `decisions/M-*`, `review/M-result.md`, `.dev/tasks/to-do/TASK-WF-followupCodegrap-*`). Never stage `.claude/`.
- **T1-02** | important | plan | plan:26-27,40,55,81,118,121-124,138 | The plan writes evidence to `./artifacts/...`, but every acceptance command runs from the worktree root (plan:26). That path is the project-root `artifacts/`, which the user's CLAUDE.md says is never staged, and not `$PKG/artifacts/`, where the spec puts it (source.md:31,225). The baseline and the final gate (plan:121) would then compare files outside `.dev/tasks`, and the evidence is never committed. | Replace every `./artifacts/` with `"$PKG/artifacts/"`, and define `PKG` in each block (T1-03).
- **T1-03** | important | spec-inherited | source.md:233,296,336 | `$PKG` is used in the T0 and T6 acceptance blocks and in the T3 copy step, but it is defined only in the T0 change block (source.md:223). Each block runs separately under `bash -euo pipefail`, so `set -u` aborts with "unbound variable". | Open every block that uses `PKG` with `PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* \| head -1); test -d "$PKG"`.
- **T1-04** | important | spec-inherited | source.md:354; plan:135 | `grep -E 'result=(pass\|ok)'` succeeds when either line is present, so a dry run where `fetch` passed and `prove` failed meets "fetch ok AND prove pass". "Opens no PR and no issue" has no command at all. | Save the log, then run `grep -q 'result=ok'` and `grep -q 'result=pass'` as separate lines, plus `test -z "$(gh pr list --repo IronbellyOrg/IronClaude --head codegraph/bump-v1.6.2 --state all --json number -q '.[].number')"`.
- **T1-05** | important | spec-inherited | source.md:351-353 | Race: `gh run list --limit 1` right after `gh workflow run` can return the previous (for example scheduled) run, because the new run is not listed yet. The watch then checks the wrong run. | Record `T=$(date -u +%FT%TZ)` before dispatch, then poll in a bounded loop: `gh run list --workflow codegraph-release-monitor.yml --event workflow_dispatch --json databaseId,createdAt` until a run with `createdAt > T` appears.
- **T1-06** | important | spec-inherited | source.md:347-357; plan:130-132 | Task 8 is "only after a person merged" but has no mechanical gate. `/sc:implement` runs it right after Task 7, when the workflow file is not on `master` yet, so `gh workflow run codegraph-release-monitor.yml --ref master` fails (the workflow is not on the default branch). | Make the first line `test "$(gh pr view "$(cat "$PKG/artifacts/pr-url.txt")" --repo IronbellyOrg/IronClaude --json state -q .state)" = MERGED`, stopping as blocked otherwise. Or move T7 out of this plan into a post-merge note.
- **T1-07** | minor | spec-inherited | source.md:355-357; plan:136 | The normal run is dispatched but never watched, so "exits 0 with `result=none`" is never checked. | Resolve its run id (T1-05), then run `gh run watch --exit-status` and grep its log for `result=none`.
- **T1-08** | minor | spec-inherited | source.md:253-258 | Under `-e`, a failing pytest in the mutation check skips `git worktree remove`. `.dev/worktrees/m-mutation` stays, and the retry's `git worktree add` fails. | Put `trap 'git worktree remove --force "$M" 2>/dev/null \|\| true' EXIT` before the add.
- **T1-09** | minor | spec-inherited | source.md:269; plan:68 | The stdlib-only check `grep -nE '^(import\|from) '` misses indented (lazy) imports, so a lazy `import click` passes. It also falsely flags `import os, sys`. | Check with `ast` (every `Import`/`ImportFrom` node) against the allowlist plus the explicit package exception from T1-15.
- **T1-10** | minor | spec-inherited | source.md:306; plan:96 | The `gh pr create` / `--repo` grep is line-based. A YAML `gh pr create \` with `--repo` on the next line fails a correct workflow, and a `gh pr create` inside the Python script (T1-21) is never checked. | Join continuation lines in the static test, and apply the same check to `scripts/codegraph_release.py`.
- **T1-11** | minor | plan | plan:66,81,111,135 | Four plan criteria have no command: "covers R1-R11 ... one test per case", "shows all five stages passing", "the paragraph names the 14-day rule ...", "opens no PR and no issue". | Give each one: for example `uv run pytest --collect-only -q ... \| grep -c`, a grep for each stage's pass line, and greps for `14`, `draft`, `integrity` and the dry-run command.
- **T1-12** | minor | plan | plan:76,81; source.md:279 | Task 4 requires `live-fetch.txt` to contain `result=ok`, but the spec's `fetch` call writes no file and the plan gives no redirect. The fixed `/tmp/m-fetch` may also hold a stale `.verified` from an earlier attempt. | Use `rm -rf /tmp/m-fetch`, then `fetch --tag v1.6.2 --dir /tmp/m-fetch --github-output "$PKG/artifacts/live-fetch.txt"`.
- **T1-13** | minor | plan | plan:95-97 vs source.md:304; plan:109-111 vs source.md:321 | The plan drops two acceptance lines: the YAML parse check (`yaml.safe_load` of the workflow) in Task 5, and the negative `SuperClaude-Org/SuperClaude_Framework/pull` link check in Task 6. | Copy both into the plan.

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
Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/source.md:5-32
```markdown
## 0. Goal, inputs and evidence rule

**Goal.** A scheduled GitHub workflow in `IronbellyOrg/IronClaude` keeps IronClaude's pinned codegraph version current. When `colbymchenry/codegraph` publishes an eligible newer release, the workflow verifies it (SHA-256 against the release's `SHA256SUMS`, plus `gh attestation verify -R colbymchenry/codegraph`), rewrites the pin in its single source location, proves the candidate in an isolated HOME, and opens a pull request on `IronbellyOrg/IronClaude` only (never upstream) with the release notes. Coder picks the new values up through its existing IronClaude SHA bump (coordinator decision; not reopened here).

**Scope.** Follow-up to Phase 2 of issue #323 (https://github.com/IronbellyOrg/IronClaude/issues/323). Not part of Phase 2: PR #329 (https://github.com/IronbellyOrg/IronClaude/pull/329) lands first. **Precondition for execution: PR #329 is merged to `master`; the executor branches from `origin/master` after that (T0).** The pin, the installer and every test this spec changes exist only on #329's head (`ironbelly/feat-codememory-codegraph-init`, read at `e62ed152`).

**Inputs read for this spec (2026-10-30):**
- `.dev/codegraph-migration/orchestration/README.md:24-33` (run rules).
- `.dev/codegraph-migration/research/codegraph-evaluation.md` §1 (`:11-25`: platforms, `SHA256SUMS` per release, attestations SLSA v1.0 Build L2 on bundles and `SHA256SUMS`, `gh attestation verify` needs GitHub auth), §5.1 (`:113-127`), §5.6 (`:203-217`), §5.9 (`:238-240`: `codegraph install --print-config claude` prints the entry with no writes), §6 (`:248-287`, gaps the user accepted), §7 (`:289-314`, single IronClaude pin; "a test-time drift check comparing IronClaude's MCP entry with a recorded `codegraph install --print-config claude` fixture", `:310`).
- `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md` §2.3-§2.4 (`:73-111`), §5 acceptance-block rules (`:445`), §6 (`:742-760`), §7 (`:762-783`), §8 (`:785-805`).
- `src/superclaude/cli/install_codegraph.py:26-35` (`VERSION = "1.6.2"`, `TAG = f"v{VERSION}"`, the 4-entry `SHA256` dict at `:28-33`, `MCP_TOOLS = "node,search,callers,callees,impact,files,status"` at `:35`), `:271-365` (`acquire`), `:186-190` (`_download`, the one network call).
- `src/superclaude/cli/install_mcp.py:854-874` (`_CODEGRAPH_ENV_KEYS`, `_codegraph_entry(command)`: `type`, `command`, `args ["serve","--mcp"]`, `alwaysLoad: true`, `env` with telemetry off, update check off and `CODEGRAPH_MCP_TOOLS`).
- `tests/cli/test_install_codegraph.py:1-141` (conventions: `box` autouse fixture sets HOME and PATH to tmp dirs, `_download` is the one network fake, `stub()`/`tarball()` builders; `test_u2_pin_integrity` at `:126-141` reads `.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt`).
- `.github/workflows/test.yml` (jobs `test`, `swarm-marker-matrix`, `lint`, `doctor-check`, `test-summary`; `setup-uv@v10.3.2`, Python 3.10, `ruff check src/ tests/`, `ruff format --check src/ tests/`; `on: workflow_dispatch` present). `tests/swarm/test_merge_boundary_guards.py:38,46,175` is the precedent for a static workflow test (`yaml.safe_load` of a workflow file; `pyyaml` is in `scripts/dependency_baseline.txt:56`). `tests/skills/test_workflow_archive.py:26-28` is the precedent for loading a script by path with `importlib.util.spec_from_file_location`.
- Coder's monitor, `gh api repos/IronbellyOrg/Coder/contents/.github/workflows/ironclaude-upstream-monitor.yml -H 'Accept: application/vnd.github.raw'` (daily cron plus `workflow_dispatch`; neutral exit with a step summary when the upstream API fails; idempotency by branch `auto/ironclaude-bump-<sha7>` and "open PR exists or remote branch exists" skip; push branch, then proof, then PR; ready PR on PASS, DRAFT PR plus best-effort `needs-build-proof` label on FAIL; `always()` on the PR step so a pushed branch is never orphaned).

**Facts verified for this spec (2026-10-30):**
1. Upstream releases (`gh api 'repos/colbymchenry/codegraph/releases?per_page=8'`): v1.6.2 2026-10-03, v1.6.1 09-29, v1.6.0 08-26, v1.5.0 07-21, v1.4.1 07-10, v1.4.0 07-10, v1.3.1 07-09, v1.3.0 07-07; none prerelease or draft; 7 assets each (6 archives plus `SHA256SUMS`). `releases/latest` is v1.6.2, equal to the pin today. Release note bodies are long: v1.6.2 is 76,281 characters, over GitHub's 65,536-character PR body limit.
2. `--print-config <id>` exists: `src/bin/codegraph.ts:2803` on upstream `main` (`.option('--print-config <id>', 'Print MCP config snippet for the named agent and exit (no file writes)')`), handled at `:2814-2824`. For `claude` it prints `# Add to <path>\n\n<JSON {"mcpServers":{"codegraph":{...}}}>\n` (`src/installer/targets/claude.ts:241-245`). The parser must skip the `#` line.
3. **The pin is not single-source today.** `git grep -n -E '1\.6\.2|v1\.6\.2' -- ':!.dev' ':!.claude'` finds the version as literals in `tests/cli/test_install_codegraph.py:38,45,96,151,171,175,237,270,639,640,659,691`, `tests/unit/test_cli_doctor.py:241,287`, `tests/cli/test_update_command.py:355`, `docs/user-guide/mcp-installation.md:9,28,31`, `docs/reference/mcp-server-guide.md:29,43`, `CHANGELOG.md:35`, and `install_codegraph.py:39` (a comment). `test_u2_pin_integrity` also compares the table with a `.dev/` evidence file. A bump that rewrites only `install_codegraph.py` would fail CI. T1 fixes this first.
4. Repo settings (`gh api repos/IronbellyOrg/IronClaude/actions/permissions/workflow`): `default_workflow_permissions: read`, `can_approve_pull_request_reviews: true` (Actions may create PRs). The repo is public, default branch `master`. Existing labels: bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix.
5. GitHub rule (https://docs.github.com/en/actions/concepts/security/github_token): events caused by `GITHUB_TOKEN` do not start new workflow runs, except `workflow_dispatch` and `repository_dispatch`; PRs opened or updated with the token start runs in an approval-required state. So the bump PR's `Tests` workflow would wait for approval; the monitor dispatches `test.yml` on the bump branch instead (`test.yml` has `workflow_dispatch`).
6. Coder side (`.dev/codegraph-migration/handoff/coder-handoff-prompt.md:16`): Coder is told to read `MCP_TOOLS`, `VERSION` and `SHA256` from `install_codegraph.py` at the pinned IronClaude SHA in tests and registrations. Whether Coder's image bake also derives the codegraph version and hashes from that file (rather than hard-coding v1.6.2, `:25`, `:47`) is UNVERIFIED. If it hard-codes them, the first Coder IronClaude-SHA bump after a codegraph bump fails Coder's offline contract test (`--network=none`, Phase 2 spec `:787`), which blocks that Coder PR safely but needs a Coder-side fix. Recorded as human item 5 (§7), not as a change to this plan.
7. Release age uses `published_at`. GitHub's REST docs (https://docs.github.com/en/rest/releases/releases) define `created_at` as "the date of the commit used for the release, and not the date when the release was drafted or published"; `published_at` is nullable (drafts). `gh` 2.103.3 (local) has `gh label create --force`, `gh run list --workflow ... --json conclusion`, `gh pr ready` and `gh attestation verify -R`.
8. The user's "about two weeks" rule for new dependency versions is coordinator-stated. Negative evidence: `grep -rn -i 'two weeks\|14 days\|release age\|minimum age' ~/.claude/*.md` found nothing; the closest rule on disk is the harness rule that external script versions must be at least two weeks old.

**Evidence rule for the executor.** Every acceptance block runs from the worktree root under `bash -euo pipefail` and must exit 0 only if its criterion passes; one condition per line; a negative check is written `if cmd; then exit 1; fi` (same rule as Phase 2 spec `:445`). Every `uv run pytest` uses `-p no:cacheprovider`. Run `git status --short` after each task: a modified tracked file the task did not intend to change is a defect to fix before committing. Never run `tests/cli/eval/` (it rewrites `.dev/releases/current/cliEval/evidence/T02.15/perf.json`, README `:27`); after any full-suite run, restore that file with `git checkout --`. `$PKG` is this plan's task package, found by its stable id prefix wherever `/sc:implement` keeps it: `PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1)`; task evidence goes under `$PKG/artifacts/`, which `git add .dev/tasks` stages.

```
### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/source.md:33-52
```markdown
## 1. Preflight: files that change

Line numbers are from `e62ed152` (PR #329's head). After #329 merges they should be unchanged, but the executor locates each seam by the named function, constant or literal, not by line.

| # | File | Change | Task |
|---|---|---|---|
| F1 | `tests/cli/fixtures/codegraph-SHA256SUMS.txt` (new) | Copy of `.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt` (header comment line plus the four `codegraph-<asset>.tar.gz` lines). The test fixture the bump rewrites; the `.dev/` evidence file stays untouched as history (README `:12`, historical `.dev/` artifacts stay untouched). | T1 |
| F2 | `tests/cli/test_install_codegraph.py` | `test_u2_pin_integrity` reads F1 instead of the `.dev/` file. Every literal `1.6.2` / `v1.6.2` in fixtures and assertions (`:38,45,96,151,171,175,237,270,639,640,659,691`) becomes `cg.VERSION` / `cg.TAG` (default arguments become `None` resolved to `cg.VERSION` inside, or f-strings). | T1 |
| F3 | `tests/unit/test_cli_doctor.py` | `_stub(version="1.6.2")` (`:241`) and `"the pin is 1.6.2"` (`:287`) derive from `install_codegraph.VERSION`. | T1 |
| F4 | `tests/cli/test_update_command.py` | `"codegraph MCP (pinned v1.6.2; user scope):"` (`:355`) derives from `install_codegraph.TAG`. | T1 |
| F5 | `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md` | Replace the literal version (`:9,28,31` and `:29,43`) with "the pinned version" plus how to read it (`superclaude install --list` prints `codegraph MCP (pinned vX.Y.Z; user scope)`; `install_codegraph.py:26-27` is the source). Add one short "How the pin is updated" paragraph to `mcp-installation.md` naming the monitor (T5). | T1, T5 |
| F6 | `scripts/codegraph_release.py` (new, stdlib only) | The bump logic (§2.2) as pure functions plus a small CLI with subcommands `check`, `fetch`, `bump`, `prove`, `body`. Not packaged (maintainer tooling, like `scripts/verify_deps.py`). | T2, T3 |
| F7 | `tests/cli/test_codegraph_release.py` (new) and `tests/cli/fixtures/codegraph_release/` (new: `releases.json`, `SHA256SUMS`, `print-config-claude.txt`, `fake_mcp_server.py`) | Offline unit tests for F6 (§3). The script is loaded with `importlib.util.spec_from_file_location` (precedent `tests/skills/test_workflow_archive.py:26-28`). | T2, T3 |
| F8 | `.github/workflows/codegraph-release-monitor.yml` (new) | The scheduled workflow (§2.3). Thin: every decision lives in F6. | T4 |
| F9 | `tests/cli/test_codegraph_release_workflow.py` (new) | Static checks of F8 with `yaml.safe_load` (precedent `tests/swarm/test_merge_boundary_guards.py:38,175`). | T4 |
| F10 | `.github/workflows/README.md` | New section "codegraph-release-monitor.yml" (the file lists every workflow; today 3). | T5 |
| F11 | `CHANGELOG.md` | `## [Unreleased]` Added entry for the monitor. The historical v1.6.2 line (`:35`) is not edited. | T5 |

**Not changed, with the reason:** `src/superclaude/cli/install_codegraph.py` (only the bot's bump PRs rewrite `VERSION` and `SHA256`; the `_MAX_MEMBERS` comment at `:39` names v1.6.2 as a past measurement and stays true); `src/superclaude/cli/install_mcp.py` (the drift check reads `_codegraph_entry`; it does not change it); `.github/workflows/test.yml` (dispatched, not edited); `pyproject.toml`, `Makefile`, `scripts/dependency_baseline.txt` (no new dependency: stdlib plus the `gh` CLI that GitHub-hosted runners provide); any primitive under `src/superclaude/{commands,skills,agents,core,hooks,templates}` (none changes, so no `make sync-dev` step is needed and no `.claude/` path is ever staged); `.dev/codegraph-migration/evidence/*` (history).

```
### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/source.md:53-173
```markdown
## 2. Design

### 2.1 Shape

One stdlib script holds every decision and is unit-tested offline; the workflow only sequences its subcommands, handles git and `gh pr`, and writes summaries (Coder's monitor keeps its logic inline in YAML; this design deliberately does not, so the logic is testable). Flow of one scheduled run:

```text
check  -> no eligible candidate on either line: summary "pinned vA is current (vB waiting, eligible <UTC time>)", exit 0
       -> upstream unreachable: infrastructure outcome (§2.5)
       -> candidate per line (within-major, higher-major; §2.4) -> idempotency gate (§2.4: branch codegraph/bump-<tag>)
fetch  -> download SHA256SUMS + 4 tarballs, length + hash check, gh attestation verify on all 5 files
          -> integrity failure: issue only, stop (§2.5)
bump   -> rewrite install_codegraph.py VERSION + SHA256, rewrite tests/cli/fixtures/codegraph-SHA256SUMS.txt
tests  -> uv run pytest on the codegraph test files (the bump must keep them green; a failure is a behaviour failure)
prove  -> isolated HOME: acquire (real verified download), --version, index fixture, tools/list, print-config drift
body   -> PR body: old/new pin, hashes, attestation result, proof result, release notes (budgeted; link only for a major)
open   -> commit + push the new branch (never before verification), gh pr create --repo "$GITHUB_REPOSITORY":
          ready (within-major, proof passed) | draft (major, always) | draft "[proof failed: <stage>]" (behaviour failure);
          then dispatch test.yml on the branch
```

### 2.2 `scripts/codegraph_release.py`

Constants: `REPO = "colbymchenry/codegraph"`, `ASSETS = ("linux-x64", "linux-arm64", "darwin-x64", "darwin-arm64")` (asserted equal to `set(install_codegraph.SHA256)` in a test, so the two never drift), `PIN_FILE = src/superclaude/cli/install_codegraph.py`, `SUMS_FIXTURE = tests/cli/fixtures/codegraph-SHA256SUMS.txt`, `MIN_AGE_DAYS = 14` (§2.4, decision M-b), `NOTES_BUDGET = 60_000` characters.

Pure functions (no I/O; every branch unit-tested):

| Function | Contract |
|---|---|
| `parse_version(tag) -> tuple[int, int, int] \| None` | Accepts only `vMAJOR.MINOR.PATCH` (digits). Anything else (prerelease suffixes, other tags) returns None and is ignored. |
| `read_pin(text) -> tuple[str, dict]` | From the `install_codegraph.py` text: exactly one line `^VERSION = "(\d+\.\d+\.\d+)"$` and exactly one `SHA256 = {` block of four `"<asset>": "<64 hex>",` lines. Any other count raises `ValueError` naming the line. |
| `pick_candidates(releases, pin_version, now, *, min_age_days) -> dict` | Input: the GitHub releases JSON list. Rules of §2.4. Returns one entry per line (`within`, `major`), each `{"tag": <tag or None>, "reason": <text>, "waiting": <tag or None>, "eligible_at": <UTC ISO or None>, "stalled": <bool>}`, plus `skipped` (tag, reason) for every ignored release. |
| `parse_sha256sums(text) -> dict` | The four `codegraph-<asset>.tar.gz` lines (`<64 lowercase hex>  <name>`); other lines (Windows zips) ignored; a missing, duplicated or malformed line for one of the four raises. |
| `rewrite_pin(text, version, hashes) -> str` | Replaces exactly the `VERSION` line and the four dict lines, keeping indentation and quoting byte-for-byte, so `ruff format --check` stays clean. Post-condition checked in the function: `read_pin(result) == (version, hashes)` and the diff touches only those five lines. |
| `render_sums_fixture(tag, sums_text, fetched_at) -> str` | Header comment (same format as F1's first line, naming the tag, the UTC time and the source) plus the four asset lines sorted by name, as `test_u2_pin_integrity` parses them (`splitlines()[1:]`). |
| `tool_problems(names, mcp_tools) -> list[str]` | Compares the `tools/list` names with `{"codegraph_" + t for t in mcp_tools.split(",")}`: one message per missing tool and per extra tool. Empty list = pass. |
| `entry_drift(expected, print_config_text) -> list[str]` | Drops lines starting with `#`, parses the JSON, takes `mcpServers.codegraph`, and compares it with `expected` (IronClaude's `_codegraph_entry(...)`) on every key except `command` (IronClaude registers an absolute realpath, upstream the bare name) and `env` (IronClaude-only keys). One message per differing or new key. Empty list = no drift. |
| `build_body(...) -> str` | PR body (§2.6). Never exceeds 65,000 characters: release notes are added newest-first until `NOTES_BUDGET` is used, the rest replaced by links; for a major, links only. |
| `classify(events) -> "infrastructure" \| "integrity" \| "behaviour" \| None` | Fail-closed classifier over the recorded stage results (§2.5 classification table). Anything that fits no row is `integrity`. |
| `route(outcome, line, tag, existing) -> list[action]` | Pure router: from the outcome (`pass`, `integrity`, `behaviour`, `infrastructure`), the line (`within`, `major`), the tag and the existing artifacts found by their keys (open or closed PR on `codegraph/bump-<tag>`, open issue with a marker, stored fingerprint, last 3 run conclusions) returns the actions to take (`open_pr(ready\|draft, title)`, `comment(pr\|issue, text)`, `mark_ready`, `retitle`, `open_issue(title, marker)`, `close_superseded(pr)`, `close_issue(marker)`, `noop`). The workflow executes the actions; it decides nothing itself. |
| `fingerprint(outcome, stage, first_error_line, head_sha) -> str` | Stored in an HTML comment `<!-- codegraph-monitor-fp:<value> -->` in the artifact body or its last bot comment; a run comments only when it changed. |

I/O wrappers (thin; tests replace them through `monkeypatch`):
- `_gh(args, timeout) -> (code, stdout)`: the one subprocess entry for `gh` (argv list, no shell, bounded, the same shape as `install_codegraph.Runner`). Used for `gh api rate_limit` (the preflight), `gh api --paginate 'repos/colbymchenry/codegraph/releases?per_page=100'`, `gh release download <tag> -R colbymchenry/codegraph -p SHA256SUMS -p 'codegraph-<asset>.tar.gz' ... -D <dir>`, and `gh attestation verify <file> -R colbymchenry/codegraph` (once per file, 5 files).
- `_run(argv, *, env, cwd, timeout)`: bounded subprocess for `codegraph` and `python` in `prove`.
- `mcp_tool_names(binary, cwd, env, timeout=60) -> list[str]`: newline-delimited JSON-RPC over stdio: `initialize`, `notifications/initialized`, `tools/list`; kills the process on exit or timeout. Same protocol as `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs:1-30`, ported to Python so the workflow needs no Node and does not depend on a `.dev/` evidence file.

CLI (each subcommand prints a human summary to stdout, appends `key=value` lines to the file named by `--github-output` when given, and exits 0 on success or "nothing to do", 1 on a failed check, 2 on an infrastructure error):
- `check [--min-age-days N] [--tag vX.Y.Z]` -> `result=none|candidate|infrastructure`, `previous`, `within_tag`, `major_tag` (each empty when that line has nothing), `stalled=true|false`. `--min-age-days` rejects anything but a whole number >= 0 (exit 2 before any download). `--tag` skips selection (manual run; still refuses a tag that is not a published, non-draft, non-prerelease release) and puts it on the line its major selects.
- `fetch --tag vX.Y.Z --dir D` -> `result=ok|integrity|infrastructure`, `stage=preflight|download|sums|hash|attestation`, plus `asset`, `expected`, `actual` on a hash failure. Order: download, check each file's byte length equals the release API asset `size`, parse sums, hash each tarball against its sums line, attestation for the four tarballs and `SHA256SUMS` (W4 §1 `:21`: both carry attestations). Retries and classification follow §2.5.
- `route --outcome ... --line ... --tag ... --github-output F` -> prints the §2.2 `route` actions as JSON lines for the workflow to execute (it reads existing PRs, issues and run conclusions through `_gh` first).
- `bump --tag vX.Y.Z --dir D` -> rewrites the pin file and F1 from the verified `D/SHA256SUMS`; refuses to run unless `fetch` left `D/.verified` (written last by `fetch`, containing the tag).
- `prove [--keep]` -> `result=pass|fail`, `stage=install|version|index|tools|drift`, plus `home=<sandbox HOME>` when `--keep` leaves it in place. Runs against the working tree (after `bump`, or on the current pin for a dry run); see §2.5.
- `body --tag vX.Y.Z --previous vA.B.C --proof <log> --out <file>` -> writes the PR body.

### 2.3 Workflow `.github/workflows/codegraph-release-monitor.yml`

- `name: codegraph release monitor`; `on: schedule: - cron: "23 6 * * *"` (daily, off the hour) and `workflow_dispatch` with inputs `dry_run` (boolean, default false: run check, fetch, bump, tests and prove, then print the diff and body; no push, no PR, no issue), `tag` (string, optional: passed to `check --tag`) and `min_age_days` (string, optional, default empty = 14; passed to `check --min-age-days`, decision M-b). When both lines have a candidate, the bump, proof and PR steps run once per line, sequentially, each from a fresh checkout of `master` (a job matrix over the `check` outputs, `max-parallel: 1`).
- `if: github.repository == 'IronbellyOrg/IronClaude'` on the job, so forks and the upstream parent never run it.
- `permissions:` `contents: write` (push the branch), `pull-requests: write` (open, edit, mark ready, close the PR), `issues: write` (integrity and infrastructure issues, label, §2.5), `actions: write` (dispatch `test.yml`; also covers the read of the last run conclusions for the infrastructure counter). Everything else none (repo default is `read`, fact 4).
- Optional repository variable `CODEGRAPH_MONITOR_ASSIGNEE` (a GitHub login): when set, every PR and issue the monitor opens is assigned to it (the owner is an organisation, so there is no single owner login; M-c item 5). When unset, nothing is assigned.
- `concurrency: { group: codegraph-release-monitor, cancel-in-progress: false }`; `runs-on: ubuntu-latest`; `timeout-minutes: 30` (four tarballs of about 63 MB each, one real install, one index).
- Steps: `actions/checkout@v4` (`fetch-depth: 0`); `astral-sh/setup-uv@v10.3.2` with Python 3.10 and `activate-environment: true` (same as `test.yml`); `uv pip install -e ".[dev]"`; then the §2.1 flow, one step per subcommand, each gated on the previous step's outputs. `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` only on steps that call `gh`. The `prove` step gets no token in its env (it runs third-party code; Coder strips tokens the same way).
- Idempotency: §2.4 "Branches and idempotency" and §2.5 keys; the workflow only executes the `route` actions.
- Commit: author `github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>`, message `chore(deps): bump codegraph pin to <tag>` with body lines `Old: <previous>`, `New: <tag>`, `Release: https://github.com/colbymchenry/codegraph/releases/tag/<tag>`, `Verified: SHA256SUMS hashes and gh attestation verify (5 files)`.
- PR: `gh pr create --repo "$GITHUB_REPOSITORY" --base master --head <branch> --title "<title from route>" --body-file <body>` plus `--draft` when `route` says so (never a bare `gh pr create`: repo CLAUDE.md rule; `$GITHUB_REPOSITORY` is `IronbellyOrg/IronClaude` because of the job `if:`). The branch is pushed only after `fetch` passed, so it never carries unverified hashes (M-c; unlike Coder, which pushes first). The step that opens the PR uses `if: always() && <branch was pushed>` so a pushed branch is never left without a PR (Coder pattern); if the proof step aborted unexpectedly, the PR opens as a behaviour-failure draft (`stage=aborted`).
- CI on the bump branch: after the PR exists, `gh workflow run test.yml --repo "$GITHUB_REPOSITORY" --ref <branch>` (fact 5). The PR body says CI was dispatched and links the Actions page filtered by branch.
- Step summary on every path (none, skipped, pass, behaviour failure, integrity failure, infrastructure failure), so a run is readable without logs.

### 2.4 Candidate selection

Rules from decisions M-a (`decisions/M-major-versions/recommendation.md`) and M-b (`decisions/M-release-age/recommendation.md`); see `## Decisions`.

- **Release list:** `gh api --paginate 'repos/colbymchenry/codegraph/releases?per_page=100'` (30 releases exist today, W4 §1; paginate so the list is never cut). Never the `releases/latest` endpoint or flag.
- **Candidate set:** drop drafts, prereleases, tags `parse_version` rejects (each logged with its reason in the summary), and releases without `published_at`. Keep releases strictly newer than the pin by semver. Order by semver, never by date.
- **Two lines, evaluated separately every run:** (1) the *within-major line*: releases with the pin's major; (2) the *higher-major line*: releases with a higher major. A pending major never blocks a minor or patch bump. One run can act on both lines.
- **Pick per line:** the highest-semver release in that line. It is eligible when `now_utc - published_at >= MIN_AGE_DAYS * 86400` seconds (inclusive, exact seconds), `MIN_AGE_DAYS = 14`. If it is younger, that line does nothing this run: **no fallback** to an older eligible release (an older one is usually the release upstream already patched).
- **Manual override:** `workflow_dispatch` input `min_age_days` (a whole number, 0 or more; any other value fails the run before any download; scheduled runs always use 14). It changes only the age; pick, verification, proof and human merge stay the same. The summary and the PR body record the override and its value. The `tag` input bypasses the pick for a manual re-proof (§2.2 `check --tag`).
- **Within-major path:** verify, rewrite, proof; ready PR on a passed proof, titled `chore(deps): bump codegraph pin to <tag>`.
- **Higher-major path:** the same verify, rewrite and proof on the same code path; the PR is **always a draft**, even on a passed proof, titled `codegraph MAJOR <tag>: manual review`. Its body carries the proof log, hashes and attestation result, a **link** to the release notes (not the text), and a checklist: "read the breaking changes"; "check the Phase 3 skills that call codegraph tools (`rg -l 'codegraph_' src/superclaude`)"; "check `MCP_TOOLS` still names the tools those skills use". Label `codegraph-major` only if it already exists (labels are best-effort; none exists today, fact 4). A person marks it ready and merges, or closes it to decline.
- **Branches and idempotency (M-c rule, reconciled with M-a; see `## Decisions` row "Branch rule"):** one branch per version, `codegraph/bump-<tag>`, on both lines. The monitor never pushes or force-pushes a branch that already exists. If `codegraph/bump-<tag>` exists, the run re-proves that branch head and reports by comment only when the fingerprint changed (§2.5). One open PR per line at a time: when a newer tag becomes the line's candidate, the monitor opens its PR and closes the line's older open bot PR with the comment "superseded by `<new tag>`"; it deletes the older branch only if every commit since `master` is the bot's. This keeps M-a's "never a duplicate PR per line" without force-pushes. An open major draft that conflicts after a 1.x bump merges is left for the person reviewing it (the re-proof comment says "rebase needed" when `git merge-tree` reports a conflict) or is superseded by the next release of that major.
- **Declined version:** if the PR for `codegraph/bump-<tag>` was closed without merging (`gh pr list --repo "$GITHUB_REPOSITORY" --head codegraph/bump-<tag> --state closed --json number,mergedAt`), later runs do nothing for that tag on either line; a newer release (for example `v2.0.1`) is a new candidate. A PR the monitor itself closed as superseded counts the same.
- **Reporting:** the summary names, per line, the release that is waiting and the UTC time it becomes eligible, and adds `::warning::` when the oldest release newer than the pin is at least 28 days old (`2 * MIN_AGE_DAYS`) and the run bumped nothing on that line. Reporting never changes the pick.
- **Pulled or re-tagged releases:** a re-created release has a new `published_at`, so its clock restarts; a deleted release drops out of the set on the next run. If an open bot PR targets a tag that no longer exists upstream, the monitor comments once "release `<tag>` was deleted upstream; close this PR" (fingerprinted) and leaves it to a person; it never merges or silently closes it (simple decision; M-b flagged item 4).

Replay check (from M-b): with the pin below v1.3.0 and daily runs over 2026, the rule bumps on 08-04 to v1.5.0, 09-09 to v1.6.0 and 10-17 to v1.6.2; today (2026-10-30) it bumps nothing (v1.6.2 is the pin).

### 2.5 Proof and failure handling

`prove` (isolated, never the real HOME; asserts at start that the child `HOME` from `tempfile.mkdtemp()` differs from the parent's `Path.home()` and that `codegraph` is not on the child `PATH`):
1. **install**: child process `python -c` with `HOME=<tmp>`, `PATH=<tmp>/home/.local/bin:/usr/bin:/bin`, `CODEGRAPH_TELEMETRY=0`, `DO_NOT_TRACK=1`, `CODEGRAPH_NO_UPDATE_CHECK=1`, running `install_codegraph.acquire(runner)` from the working tree (so the rewritten pin, the real download URL and the real SHA-256 check are what users will run). Pass = `ok` and the returned launcher exists.
2. **version**: `<launcher> --version` prints exactly the new `VERSION`.
3. **index**: a fresh `git init -q` directory holding a copy of `src/superclaude/cli/install_codegraph.py`; `codegraph init --yes` exits 0; `codegraph query acquire` exits 0 and its output names `install_codegraph.py` (same pattern as Phase 2 layer 2 step 4, `evidence/p2-layer2.sh`).
4. **tools**: `mcp_tool_names(launcher, project, env + {"CODEGRAPH_MCP_TOOLS": install_codegraph.MCP_TOOLS})`; `tool_problems(...)` must be empty: every `MCP_TOOLS` tool is listed and nothing else is (Phase 2 relied on an explicit list hiding every other tool, F2 merged method, so an extra tool is a regression too).
5. **drift**: `<launcher> install --print-config claude` (no file writes, fact 2) exits 0; `entry_drift(install_mcp._codegraph_entry(launcher), stdout)` must be empty.
Every step's command, exit code and the first 200 lines of output go to the proof log; the temp dir is deleted unless `--keep`. Any daemon the index or MCP run started is killed by process group on exit (codegraph's daemon outlives the client, W4 §5.7 `:221`).

**Failure outcomes (decision M-c, `decisions/M-proof-failure/recommendation.md`; merged rule `decisions/M-proof-failure/adversarial/M-proof-failure-merged.md`).** Never both an issue and a PR for one failure: exactly one artifact per class.

Classification (fail closed, `classify`):

| Observation | Class |
|---|---|
| `gh api rate_limit` fails, or a download is still short or erroring after one retry | infrastructure |
| A complete download (exit 0, byte length equals the release API asset `size`) whose SHA-256 mismatches its `SHA256SUMS` line twice (re-downloaded once) | integrity |
| `gh attestation verify` fails twice while the `rate_limit` preflight succeeds | integrity |
| `tests`, install, version, index, tools or drift fails after integrity passed, or the proof step aborted | behaviour |
| Anything else, or ambiguous | integrity |

| Class | Artifact | Key (how later runs find it) | Later runs |
|---|---|---|---|
| Integrity | **Issue only.** No branch, no PR, no hash written anywhere. Title `codegraph <tag>: integrity check failed`, no label. Body: run URL, asset, expected and actual hash or the attestation output, reproduce commands (`gh release download <tag> -R colbymchenry/codegraph ...`, `sha256sum -c`, `gh attestation verify ...`). Assigned to `CODEGRAPH_MONITOR_ASSIGNEE` when set. | HTML marker `<!-- codegraph-monitor:<tag>:integrity -->` in the body (never the title) | Comment only when the fingerprint changed. The monitor **never closes** it; only a person does. A later pass for the same tag still opens its PR, which links the issue. A newer release adds a link comment and leaves it open. |
| Behaviour | **Draft PR only, no issue.** Branch `codegraph/bump-<tag>` (verified hashes only). Title = the pass-path title plus ` [proof failed: <stage>]` (within-major `chore(deps): bump codegraph pin to <tag> [proof failed: tools]`; major `codegraph MAJOR <tag>: manual review [proof failed: tools]`, so "major review" and "proof failed" stay distinct, M-a item 5). Label `needs-codegraph-proof`, created with `gh label create needs-codegraph-proof --force --repo "$GITHUB_REPOSITORY"` and applied in a step with `continue-on-error: true` (the draft state is the gate; the label is best effort). Body: stage, proof log tail, run URL, reproduce commands. | branch name `codegraph/bump-<tag>` | Re-prove the branch head; comment only when the fingerprint changed. If the proof passes at the head **and** the head's `SHA256` table equals the hashes verified in the same run: remove the ` [proof failed: ...]` title suffix and the label, and mark ready (`gh pr ready`) on the within-major line only (a major stays draft, M-a). If the table differs, stay draft and comment. |
| Infrastructure | `::warning::` plus a step summary; the job ends with a **failed** conclusion so the counter can see it. | marker `<!-- codegraph-monitor:infra -->` | On the 3rd failed run in a row (`gh run list --repo "$GITHUB_REPOSITORY" --workflow codegraph-release-monitor.yml --limit 3 --json conclusion`, all `failure`), open one issue `codegraph monitor: cannot reach upstream` (or comment on the open one when the fingerprint changed), with the three run URLs. The first run whose preflight passes closes that issue. |

Fingerprint = class, stage, first error line, branch head SHA (`fingerprint`, §2.2). A run whose fingerprint equals the stored one is a no-op for that artifact.

### 2.6 PR body

Sections, in order: one-line summary (`codegraph <previous> -> <tag>`, MAJOR/minor/patch); a table of the four assets with their new SHA-256 and "matches SHA256SUMS: yes"; "Attestation: `gh attestation verify -R colbymchenry/codegraph` passed for 5 files"; proof result with the five stages and a link to the run; "CI: `test.yml` dispatched on this branch" with the link; "Coder: merges reach Coder through its IronClaude SHA bump; Coder's codegraph bake must read `VERSION` and `SHA256` from `src/superclaude/cli/install_codegraph.py` at that SHA" (fact 6); then "Release notes" for every release after the old pin up to the new tag, newest first, each under its own heading with its URL, cut at `NOTES_BUDGET` characters with "(truncated; full notes: <URL>)". A major PR (§2.4) carries links to those releases instead of their text, plus its review checklist. A PR opened with a `min_age_days` override says so with the value. A behaviour-failure draft adds the failed stage, the log tail and reproduce commands at the top. Every body ends with the fingerprint marker (§2.5). Release-note text is untrusted third-party content: it is placed in the body only through `--body-file`, never interpolated into a shell command.

```
### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/source.md:174-207
```markdown
## 3. Tests

All offline: no test touches the network, the real HOME, the real `gh` or a real `codegraph` (same rule as `tests/cli/test_install_codegraph.py:3-5`). `_gh` and `_run` are replaced with recording fakes; HOME points at `tmp_path`.

**`tests/cli/test_codegraph_release.py` (T2, T3):**

| ID | Case |
|---|---|
| R1 | `parse_version`: `v1.6.2` -> (1,6,2); `v2.0.0` -> (2,0,0); `1.6.2`, `v1.6`, `v1.7.0-rc.1`, `nightly` -> None. |
| R2 | `read_pin` on the real `install_codegraph.py` returns `(install_codegraph.VERSION, install_codegraph.SHA256)`; a copy with two `VERSION` lines, a missing asset line, or a 63-hex digest raises `ValueError`. |
| R3 | `ASSETS` equals `set(install_codegraph.SHA256)`. |
| R4 | `pick_candidates` on `fixtures/codegraph_release/releases.json` (the real 8-release list of fact 1 plus synthetic entries, each case sets a fixed `now`): equal pin -> nothing; empty list; only drafts or prereleases; unparsable tag skipped with reason; a release without `published_at` skipped; age 14 days minus 1 s (not eligible), exactly 14 days (eligible), 14 days plus 1 s; newest too young with an older eligible release -> nothing (no fallback) and `waiting` names the newest; a backport published after a higher version (semver order wins, not date); a re-created release (new `published_at` restarts the clock); `min_age_days=0`; a pending `v2.0.0` alongside an eligible `v1.7.1` -> both lines set; stall warning at 28 days; the M-b 2026 replay (pin below v1.3.0, daily `now` from 07-01 to 10-30: bumps exactly on 08-04 to v1.5.0, 09-09 to v1.6.0, 10-17 to v1.6.2). |
| R5 | `parse_sha256sums` on `fixtures/codegraph_release/SHA256SUMS` (the real v1.6.2 file, 6 archives) returns the four tarball digests; missing asset, duplicate line, uppercase or short hex each raise. |
| R6 | `rewrite_pin` on the real `install_codegraph.py` text with `1.7.0` and four fake digests: `read_pin(result)` matches; `difflib` shows exactly 5 changed lines; the result passes `ruff format --check` (run `ruff format --check -` on it via `subprocess` with stdin); `TAG` line unchanged (it derives from `VERSION`). |
| R7 | `rewrite_pin` then `importlib` load of the rewritten copy from `tmp_path`: module `VERSION`, `TAG` and `SHA256` equal the new values. |
| R8 | `render_sums_fixture` output parsed exactly as `test_u2_pin_integrity` does (`splitlines()[1:]`, `line.split()`) yields the four assets. |
| R9 | `tool_problems`: exact set passes; one missing tool, one extra tool (`codegraph_explore`) each give one message. |
| R10 | `entry_drift` on `fixtures/codegraph_release/print-config-claude.txt` (the real v1.6.2 output shape: `# Add to ...` line plus JSON with `type`, `command: "codegraph"`, `args`, `alwaysLoad`) against `install_mcp._codegraph_entry(Path("/x/codegraph"))`: no drift. Changed `args`, `alwaysLoad: false`, a new upstream key (`"timeout": 30`), and invalid JSON each report drift. |
| R11 | `build_body`: three releases with 40,000-character notes: body <= 65,000 characters, newest notes complete, the rest replaced by "(truncated; full notes: <URL>)"; the body contains every asset hash and the Coder line. |
| R12 | `fetch` with a fake `_gh` that writes fixture files: OK path writes `.verified` last; a complete tarball whose bytes do not match its sums line on both the first download and the one re-download -> `result=integrity`, `stage=hash`, no `.verified`; a mismatch that clears on re-download passes; a short download (length differs from the asset `size`) after one retry -> `infrastructure`; attestation failure on any of the 5 files on both attempts with the `rate_limit` preflight passing -> `integrity`, `stage=attestation`; download failure after one retry -> `infrastructure`. |
| R13 | `bump` refuses without `.verified` or with a different tag in it (exit 1, no file changed); with it, rewrites both files in a `tmp_path` copy of the repo layout. |
| R14 | `mcp_tool_names` against `fixtures/codegraph_release/fake_mcp_server.py` (a 30-line stdio JSON-RPC server that lists tools named by its env) returns those names; a server that never answers is killed within the timeout and raises. |
| R15 | `prove` with `_run` and `mcp_tool_names` faked: each stage failure sets the matching `stage=`; it refuses to run when the computed child HOME equals the parent HOME. |
| R16 | CLI: `--github-output <file>` gets `key=value` lines; `check` with a failing `_gh` exits 2 with `result=infrastructure`; a non-integer or negative `--min-age-days` exits 2 before any `_gh` download call. |
| R17 | `classify` (9 cases, M-c merged §9): rate-limit failure; short download after retry; download error after retry; hash mismatch twice on a complete download; hash mismatch once then match (passes); attestation failure twice with preflight OK; attestation failure with preflight failing (infrastructure); tools failure after integrity passed (behaviour); an unknown observation (integrity). |
| R18 | `route` (15 cases): within-major pass -> ready PR with the plain title; major pass -> draft with `codegraph MAJOR`; integrity -> issue only with the marker, no branch action; behaviour within-major -> draft with ` [proof failed: <stage>]` and label; behaviour major -> draft with both markers in the title; second run, same fingerprint -> `noop`; second run, changed fingerprint -> one comment; existing branch -> re-prove and comment, never push; later pass on a behaviour draft with an equal table -> retitle and mark ready (within-major) / retitle only (major); later pass with a different table -> stay draft and comment; newer tag on a line with an open PR -> open new PR and `close_superseded`; closed-unmerged PR for the tag -> `noop`; integrity issue open and then a pass for the same tag -> PR links the issue and the issue stays open; 3rd failed run in a row -> infra issue; first preflight pass with an infra issue open -> `close_issue`. |
| R19 | Deleted release: an open bot PR whose tag is no longer in the release list gets one fingerprinted comment and is never closed by the monitor. |

**`tests/cli/test_codegraph_release_workflow.py` (T4):** `yaml.safe_load` of the workflow: `on` has `schedule` and `workflow_dispatch` with inputs `dry_run`, `tag` and `min_age_days`; the schedule passes no `min_age_days`; job `if` names `IronbellyOrg/IronClaude`; `permissions` is exactly `{contents: write, pull-requests: write, issues: write, actions: write}`; every `gh pr create` line contains `--repo "$GITHUB_REPOSITORY"`; no step text contains `SuperClaude-Org`; the `prove` step has no `GH_TOKEN`/`GITHUB_TOKEN` in its `env`; every `run:` that calls the script uses `scripts/codegraph_release.py`; the PR-open step's `if` starts with `always()`; no `git push` uses `--force` or `--force-with-lease` (M-c: never push an existing branch); the `git push` step comes after the `fetch` step and is gated on `fetch` `result == 'ok'`; the label step has `continue-on-error: true`; the workflow contains no `gh pr merge` and no `--auto`.

**Existing tests kept green (T1):** `tests/cli/test_install_codegraph.py`, `tests/unit/test_cli_doctor.py`, `tests/cli/test_update_command.py`, `tests/cli/test_install_mcp_registry.py`. T1 adds a version-agnostic guard: `test_u2_pin_integrity` now reads F1, and a new test `test_no_pinned_version_literals_in_tests` asserts that the three test files contain no literal of the current `install_codegraph.VERSION` (the guard that keeps the next bump a one-file change).

**Live, opt-in (T3, T6):** `uv run python scripts/codegraph_release.py prove` on the current pin, in an isolated HOME, with the network: install, version, index, tools and drift pass for v1.6.2. This is the harness's own proof and also the §2.5 drift check against today's release. Not part of `pytest`.

```
### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/source.md:208-359
```markdown
## 4. Task breakdown (execution order)

Each task ends at a conventional commit point; after each commit, post the §5 issue comment. Stage only the files the task names plus `.dev/tasks` (`git add .dev/tasks`, always staged) and, when a decision was taken, `.dev/codegraph-migration/decisions/MX-*`; never a `.claude/` path.

**T0. Branch from master after #329 merges; record the baseline.**
Files: none in source. `$PKG/artifacts/baseline-failures.txt` (new; `$PKG` per §0).
Change: confirm PR #329 is merged, create the feature branch from `origin/master`, bring this plan onto it, record the full-suite failure baseline (the suite was not green at Phase 2's base, README `:42`).
```bash
test "$(gh pr view 329 --repo IronbellyOrg/IronClaude --json state --jq .state)" = MERGED
git fetch origin
git switch -c ironbelly/feat-codegraph-release-monitor origin/master
PLAN=$(git log --format=%H -1 --grep '^docs(plan): codegraph release monitor' ironbelly/codegraph-release-monitor)
test -n "$PLAN"
git cherry-pick "$PLAN"
grep -n '^VERSION = ' src/superclaude/cli/install_codegraph.py    # the plan was written against "1.6.2"; another value is fine (see Commit note)
PKG=$(ls -d .dev/tasks/*/TASK-WF-followupCodegrap-* | head -1); test -d "$PKG"; mkdir -p "$PKG/artifacts"
make sync-dev
{ uv run pytest -p no:cacheprovider -q -rfE --tb=no tests --ignore=tests/cli/eval 2>&1 || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort > "$PKG/artifacts/baseline-failures.txt"
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json 2>/dev/null || true
```
Acceptance:
```bash
test "$(git branch --show-current)" = ironbelly/feat-codegraph-release-monitor
git merge-base --is-ancestor origin/master HEAD
test -f .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md
test -f "$PKG/artifacts/baseline-failures.txt"
test -z "$(git status --short -- src tests scripts docs .github CHANGELOG.md)"
```
Commit: `chore(tasks): record the test baseline for the codegraph release monitor (#323)` (stages `.dev/tasks`, which holds the baseline). If the planning commit's pin line is no longer `1.6.2` on master (someone bumped it by hand), continue: nothing in this plan depends on the value, only the T1 literal lists change (simple decision).

**T1. Make the pin a one-file change.**
Files: `tests/cli/fixtures/codegraph-SHA256SUMS.txt` (new), `tests/cli/test_install_codegraph.py`, `tests/unit/test_cli_doctor.py`, `tests/cli/test_update_command.py`, `docs/user-guide/mcp-installation.md`, `docs/reference/mcp-server-guide.md`.
Change: F1-F5 (§1): copy the evidence checksum lines into F1 and point `test_u2_pin_integrity` at it; replace every pinned-version literal in the three test files with `cg.VERSION` / `cg.TAG` (or `install_codegraph.VERSION` / `.TAG`); add `test_no_pinned_version_literals_in_tests` (§3); docs say "the pinned version" and how to read it.
Acceptance:
```bash
cmp <(tail -n +2 .dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt) <(tail -n +2 tests/cli/fixtures/codegraph-SHA256SUMS.txt)
uv run pytest -p no:cacheprovider -q tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py tests/cli/test_install_mcp_registry.py
if git grep -n -E '1\.6\.2' -- tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py docs/user-guide/mcp-installation.md docs/reference/mcp-server-guide.md; then exit 1; fi
uv run ruff check tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py
uv run ruff format --check tests/cli/test_install_codegraph.py tests/unit/test_cli_doctor.py tests/cli/test_update_command.py
git diff --quiet -- src/superclaude/cli/install_codegraph.py .dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt
```
Commit: `test(codegraph): derive the pinned version from install_codegraph in tests and docs`
Post-commit mutation check (proves the one-file property on the committed tree, in a throwaway worktree under the canonical `.dev/worktrees/`, which is gitignored at `.gitignore:238`; never edits the real worktree). Only `test_u2_pin_integrity` is deselected, because `9.9.9` has no matching checksum lines; every other test must pass with the bumped literal. If it fails, fix the missed literal and amend the T1 commit before T2.
```bash
M=.dev/worktrees/m-mutation
git worktree add -q --detach "$M" HEAD
sed -i 's/^VERSION = "[0-9.]*"$/VERSION = "9.9.9"/' "$M/src/superclaude/cli/install_codegraph.py"
grep -q '^VERSION = "9.9.9"$' "$M/src/superclaude/cli/install_codegraph.py"
(cd "$M" && uv run pytest -p no:cacheprovider -q tests/unit/test_cli_doctor.py tests/cli/test_update_command.py tests/cli/test_install_codegraph.py --deselect tests/cli/test_install_codegraph.py::test_u2_pin_integrity)
git worktree remove --force "$M"
```

**T2. Pure bump logic and its unit tests.**
Files: `scripts/codegraph_release.py` (new), `tests/cli/test_codegraph_release.py` (new), `tests/cli/fixtures/codegraph_release/releases.json`, `tests/cli/fixtures/codegraph_release/SHA256SUMS`, `tests/cli/fixtures/codegraph_release/print-config-claude.txt` (new).
Change: §2.2 constants and every pure function (including `classify`, `route`, `fingerprint`); §2.4 rules; §2.5 tables; tests R1-R11 and R17-R19. Fixture sources: `releases.json` from `gh api 'repos/colbymchenry/codegraph/releases?per_page=8' --jq '[.[] | {tag_name, published_at, draft, prerelease, html_url, body: (.body[:2000]), assets: [.assets[] | {name, size}]}]'` plus synthetic entries appended by hand (documented in a `_comment` key); `SHA256SUMS` from `gh release download v1.6.2 -R colbymchenry/codegraph -p SHA256SUMS`; `print-config-claude.txt` from the T3 live run, or, if T3 has not run yet, written from `claude.ts:241-245` and replaced by the real output in T3 (simple decision).
Acceptance:
```bash
uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release.py
uv run ruff check scripts/codegraph_release.py tests/cli/test_codegraph_release.py
uv run ruff format --check scripts/codegraph_release.py tests/cli/test_codegraph_release.py
if grep -nE '^(import|from) ' scripts/codegraph_release.py | grep -vE ' (__future__|argparse|datetime|difflib|hashlib|json|os|re|shutil|signal|subprocess|sys|tempfile|time|pathlib|typing|importlib)( |$|\.)'; then exit 1; fi
```
Commit: `feat(codegraph): add offline-tested release bump logic`

**T3. I/O subcommands, MCP client and live harness proof.**
Files: `scripts/codegraph_release.py`, `tests/cli/test_codegraph_release.py`, `tests/cli/fixtures/codegraph_release/fake_mcp_server.py` (new), `tests/cli/fixtures/codegraph_release/print-config-claude.txt` (real output).
Change: `_gh`, `_run`, `mcp_tool_names`, subcommands `check`, `fetch`, `bump`, `prove`, `body`, `route` (§2.2, §2.5, §2.6); tests R12-R16. Then the live proof on the current pin, isolated HOME, network on:
```bash
REAL_SUM=$(jq -S '.mcpServers' "$HOME/.claude.json" | sha256sum | cut -d' ' -f1)
uv run python scripts/codegraph_release.py check --github-output /tmp/m-check.txt     # expect result=none today (v1.6.2 is the pin)
uv run python scripts/codegraph_release.py fetch --tag v1.6.2 --dir /tmp/m-fetch      # live hash + attestation check of the current pin
uv run python scripts/codegraph_release.py prove --keep --github-output /tmp/m-prove.out > /tmp/m-prove.log   # live 5-stage proof on the current pin
H=$(sed -n 's/^home=//p' /tmp/m-prove.out); test -n "$H"                              # prove --keep reports the kept sandbox HOME as home=<path>
HOME="$H" CODEGRAPH_TELEMETRY=0 CODEGRAPH_NO_UPDATE_CHECK=1 "$H/.local/bin/codegraph" install --print-config claude > tests/cli/fixtures/codegraph_release/print-config-claude.txt
rm -rf "$H"
test "$(jq -S '.mcpServers' "$HOME/.claude.json" | sha256sum | cut -d' ' -f1)" = "$REAL_SUM"   # the real HOME's MCP servers are unchanged
```
Acceptance:
```bash
uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release.py
uv run ruff check scripts/codegraph_release.py tests/cli/test_codegraph_release.py tests/cli/fixtures/codegraph_release/fake_mcp_server.py
uv run ruff format --check scripts/codegraph_release.py tests/cli/test_codegraph_release.py tests/cli/fixtures/codegraph_release/fake_mcp_server.py
grep -q '^result=none$' /tmp/m-check.txt
grep -q '^result=pass$' /tmp/m-prove.out
grep -q '"mcpServers"' tests/cli/fixtures/codegraph_release/print-config-claude.txt
git diff --quiet -- src/superclaude/cli/install_codegraph.py
```
Commit: `feat(codegraph): verify, prove and describe a codegraph release candidate`. Copy `/tmp/m-prove.log` to `$PKG/artifacts/live-prove.log` and stage it with this commit (evidence for the issue comment).

**T4. The scheduled workflow and its static test.**
Files: `.github/workflows/codegraph-release-monitor.yml` (new), `tests/cli/test_codegraph_release_workflow.py` (new).
Change: §2.3 exactly, plus the §2.5 failure steps; R-workflow checks (§3).
Acceptance:
```bash
uv run pytest -p no:cacheprovider -q tests/cli/test_codegraph_release_workflow.py
uv run python -c 'import yaml,sys; yaml.safe_load(open(".github/workflows/codegraph-release-monitor.yml"))'
if grep -n 'SuperClaude-Org' .github/workflows/codegraph-release-monitor.yml; then exit 1; fi
if grep -nE 'gh pr create' .github/workflows/codegraph-release-monitor.yml | grep -v -- '--repo "\$GITHUB_REPOSITORY"'; then exit 1; fi
uv run ruff check tests/cli/test_codegraph_release_workflow.py
uv run ruff format --check tests/cli/test_codegraph_release_workflow.py
```
If `actionlint` is on PATH, also run `actionlint .github/workflows/codegraph-release-monitor.yml` (optional; it is not installed by this plan).
Commit: `ci(codegraph): add the scheduled codegraph release monitor`

**T5. Documentation.**
Files: `.github/workflows/README.md`, `CHANGELOG.md`, `docs/user-guide/mcp-installation.md`.
Change: F10, F11, the F5 "How the pin is updated" paragraph (what the monitor does, the §2.4 rules, what a failure produces, how to run it by hand: `gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude -f dry_run=true`).
Acceptance:
```bash
grep -q 'codegraph-release-monitor.yml' .github/workflows/README.md
awk '/^## \[Unreleased\]/{f=1;next} /^## \[/{f=0} f' CHANGELOG.md | grep -qi 'codegraph release monitor'
grep -q 'codegraph-release-monitor' docs/user-guide/mcp-installation.md
if grep -n 'SuperClaude-Org/SuperClaude_Framework/pull' docs/user-guide/mcp-installation.md .github/workflows/README.md; then exit 1; fi
```
Commit: `docs(codegraph): document the codegraph release monitor`

**T6. Final gate and PR.**
Files: none new.
Change: full-suite comparison against the T0 baseline; the T3 live proof re-run on the final tree; open the PR with `/sc:pr-submit --monitor 3`.
```bash
make sync-dev
{ uv run pytest -p no:cacheprovider -q -rfE --tb=no tests --ignore=tests/cli/eval 2>&1 || true; } | { grep -E '^(FAILED|ERROR) ' || true; } | sed 's/ - .*//' | sort > /tmp/m-final-failures.txt
git checkout -- .dev/releases/current/cliEval/evidence/T02.15/perf.json 2>/dev/null || true
uv run python scripts/codegraph_release.py prove --github-output /tmp/m-prove-final.out > /tmp/m-prove-final.log
```
Acceptance:
```bash
test -z "$(comm -13 "$PKG/artifacts/baseline-failures.txt" /tmp/m-final-failures.txt)"   # no new failure
grep -q '^result=pass$' /tmp/m-prove-final.out
uv run ruff check src/ tests/ scripts/codegraph_release.py
uv run ruff format --check src/ tests/ scripts/codegraph_release.py
make verify-sync
test -z "$(git status --short -- src tests scripts docs .github CHANGELOG.md)"
test "$(gh repo view --json nameWithOwner -q .nameWithOwner)" = IronbellyOrg/IronClaude
```
Then, in Claude Code: `/sc:pr-submit --monitor 3 --head ironbelly/feat-codegraph-release-monitor --title "feat(codegraph): scheduled codegraph release monitor (#323)" --body "<summary, test evidence, live proof log path, link to this spec>"` (fallback only if it cannot run: `gh pr create --repo IronbellyOrg/IronClaude --base master --head ironbelly/feat-codegraph-release-monitor ...`). Before it: the repo CLAUDE.md pre-PR checks (`git remote -v`; `git fetch origin && git log master..origin/master`, rebase onto `origin/master` if the fork moved). After it: the returned URL must start with `https://github.com/IronbellyOrg/IronClaude/pull/`.
Commit point: none new (the PR carries T0-T5); the issue comment links the PR.

**T7. Post-merge live check (after the human merges, §7 item 2).**
Files: none.
Change: run the monitor once on `master` in dry-run mode with the current pin forced, then once normally.
```bash
gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude --ref master -f dry_run=true -f tag=v1.6.2
RUN=$(gh run list --repo IronbellyOrg/IronClaude --workflow codegraph-release-monitor.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN" --repo IronbellyOrg/IronClaude --exit-status
gh run view "$RUN" --repo IronbellyOrg/IronClaude --log | grep -E 'result=(pass|ok)'
gh workflow run codegraph-release-monitor.yml --repo IronbellyOrg/IronClaude --ref master
```
Acceptance: the dry run exits 0 with `fetch` `result=ok` and `prove` `result=pass` in its log; the normal run exits 0 with `result=none` (or, if a release became eligible meanwhile, opens exactly one PR on `IronbellyOrg/IronClaude` whose URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`); `gh pr list --repo IronbellyOrg/IronClaude --search 'bump codegraph pin' --state open` shows at most one PR per tag.
Commit point: none; final issue comment with both run URLs.

```
### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/source.md:360-380
```markdown
## 5. Progress reporting on issue #323

After each commit point in §4 (T0, T1, T2, T3, T4, T5), after T6 opens the PR, and after T7, post exactly one comment on issue #323. Nowhere else (no PR comments for progress, no Slack). Body file, so the shell does not mangle it:

```bash
cat > /tmp/m-progress.md <<'EOF'
**codegraph release monitor (follow-up to Phase 2) progress: <task id and name>**

- Commit: <short sha> `<conventional commit subject>` on `ironbelly/feat-codegraph-release-monitor`
- Done: <one line per change>
- Tests: `<exact acceptance command>` -> <N passed / failure summary>
- Live evidence: <none | path under .dev/codegraph-migration/evidence/ | run URL>
- Decisions taken: <none | .dev/codegraph-migration/decisions/MX-<slug>/>
- Next: <next task>
EOF
gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file /tmp/m-progress.md
rm /tmp/m-progress.md
```

A failed acceptance run is reported as failed with its summary, never as done. The T6 and T7 comments link the PR and run URLs; a PR URL must start with `https://github.com/IronbellyOrg/IronClaude/pull/`.

```
### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/source.md:381-399
```markdown
## 6. Autonomy rules for the executor

The executor works without stopping to ask.

| Decision size | Example | Method |
|---|---|---|
| Simple: one obvious answer, or forced by a pinned test or a verified fact | helper names, message wording, fixture layout, summary text, cron minute | decide yourself |
| Mid: two or more viable options with real trade-offs, local to one task | how to kill a codegraph daemon the proof started; how to budget release notes; whether `check` paginates past 30 releases | write each option to `.dev/codegraph-migration/decisions/MX-<slug>/option-<x>.md` (under 40 lines each) and spawn an agent (Agent tool) that runs `/sc:adversarial --compare <files> --depth quick` |
| Complex: changes a §Decisions outcome, the single-pin rule, the PR target, the proof's five stages, or anything Coder consumes (`VERSION`, `SHA256`, `MCP_TOOLS` format in `install_codegraph.py`) | auto-merging bump PRs; moving the pin to a data file; dropping the attestation check | same, without `--depth quick` (`/sc:adversarial --compare <files>`, default standard depth) |

Follow the adversarial recommendation. Record every autonomous decision, in the commit that applies it, as a row in `.dev/codegraph-migration/decisions/MX-log.md` (create on first use): decision, options considered, method (self / adversarial quick / adversarial full), rationale, decision folder. Mention the folder in the next issue comment.

Hard rules (no decision overrides them):
- PRs only on `IronbellyOrg/IronClaude`, through `/sc:pr-submit --monitor 3` (fallback `gh pr create --repo IronbellyOrg/IronClaude`); never push to `upstream`; never a bare `gh pr create`, also inside the workflow.
- Never stage a `.claude/` path (only `.claude/settings.json` is tracked, and this plan does not change it); always `git add .dev/tasks`; feature branch only.
- Never run `superclaude install`, `claude mcp add/remove`, `./update.sh` or `codegraph install` (without `--print-config`) against the real HOME; `prove` and the live T3 run use a sandbox HOME and the T3 block checks the real `.mcpServers` is unchanged.
- Never edit `.dev/codegraph-migration/evidence/P2-*` or other historical `.dev/` artifacts; never run `tests/cli/eval/`; restore `.dev/releases/current/cliEval/evidence/T02.15/perf.json` after a full run.
- The workflow never merges, approves or auto-merges a PR, and never pushes to `master`.

```
### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/source.md:400-408
```markdown
## 7. Human intervention (minimal list)

1. **Precondition:** PR #329 merged to `master` (the executor checks it in T0 and waits, posting one issue comment, if it is not).
2. Merging the monitor PR (T6) to `master`; the executor runs T7 after it.
3. Every bump PR the monitor opens later is merged by a person (by design; the workflow never merges). A major draft is marked ready by a person after its checklist; an integrity issue is closed by a person after investigating (possible tampering upstream: do not change a hash by hand to make it pass).
6. Optional, once: set the repository variable `CODEGRAPH_MONITOR_ASSIGNEE` to the GitHub login that should be assigned monitor PRs and issues (`gh variable set CODEGRAPH_MONITOR_ASSIGNEE --repo IronbellyOrg/IronClaude --body <login>`). Without it nothing is assigned, and notification of drafts is UNVERIFIED (M-c item 6).
4. A GitHub auth failure for `gh` on the executor's machine (the executor cannot log in for the user).
5. Coder side, non-blocking for this plan: confirm that Coder's codegraph image bake reads `VERSION` and `SHA256` from `src/superclaude/cli/install_codegraph.py` at its pinned IronClaude SHA (fact 6, UNVERIFIED). If it hard-codes v1.6.2, the first Coder IronClaude-SHA bump after a codegraph bump fails Coder's offline contract test until Coder fixes its bake. The executor states this in the T6 issue comment; the fix is Coder's.

```
### .dev/tasks/to-do/TASK-WF-followupCodegrap-20261030-153943/source.md:409-429
```markdown
## Decisions

| Decision | Options considered | Method | Rationale |
|---|---|---|---|
| (a) Major versions: automatic or manual review | A: bump like minors (ready PR); B: issue only, manual bump; C: full automated PR, always draft | adversarial quick (`decisions/M-major-versions/recommendation.md`; C 0.875, B 0.832, A 0.697; convergence 92.9%, 13/14) | C merged with B's per-major candidate selection: a major gets the same verify and proof but always a draft PR titled `codegraph MAJOR <tag>: manual review` with a Phase 3 checklist and linked notes; within-major bumps keep flowing while a major waits. The proof checks tool names and the entry shape, not tool semantics, so a major needs a person (§2.4). |
| (b) Minimum release age | A: none; B: 14 days, newest eligible with fallback; C: 7 days, latest only | adversarial quick (`decisions/M-release-age/recommendation.md`; B 0.819, C 0.806, A 0.685; convergence 100%, 14/14) | B's 14 days (the user's two-week rule) with C's no-fallback: bump only to the highest-semver release once it is at least 14 days old, never to an older one; `min_age_days` dispatch input for a one-off security fix; stall warning at 28 days (§2.4). |
| (c) What a failed proof produces | A: draft PR + label; B: issue only; C: split by failure class | adversarial quick (`decisions/M-proof-failure/recommendation.md`; C 0.748, B 0.760, A 0.606; B and C within 5%, C won the debate-points tiebreaker 9 to 5; convergence 100%, 18/18) | Never both: integrity failure -> issue only, no branch (unverified hashes never sit on a branch; the pin is the only trust anchor, `install_codegraph.py:328-330`); behaviour failure -> draft PR with ` [proof failed: <stage>]` and label `needs-codegraph-proof`; infrastructure -> warning, issue after 3 failed runs in a row (§2.5). |
| Branch rule (conflict between (a) and (c)) | M-a merged rule: one fixed branch per line, rebuilt and force-pushed each run (`decisions/M-major-versions/recommendation.md:21`); M-c merged rule: one branch per version `codegraph/bump-<tag>`, never push an existing branch (`decisions/M-proof-failure/recommendation.md:37-41`) | self (reconciliation) | M-c's rule governs pushes because branch and push behaviour is the scope of that decision and it keeps unverified or human-edited branches from being overwritten; M-a's stated goal (never a duplicate PR per line, majors never block minors) is kept by superseding the older open PR on the same line. Cost accepted: a major draft that conflicts after a 1.x merge is rebased by its reviewer or superseded by the next release. Both sources cited here; neither file was edited. |
| Infrastructure counter (M-c open item N-006) | 1: infra run ends failed, count with `gh run list --json conclusion`; 2: neutral exit, counter stored in a run artifact | self | Option 1 needs no stored state and uses a verified `gh` flag (fact 7); a red run is the honest state when upstream cannot be reached. Any 3 failed runs in a row escalate, which is wanted (the monitor is broken either way). |
| Where the bump logic lives | inline YAML (Coder style); package module under `src/superclaude/cli/`; `scripts/codegraph_release.py` | self | The brief requires offline unit tests; `scripts/` is not installed to users (maintainer tooling, precedent `scripts/verify_deps.py`) and the by-path import has a precedent (`tests/skills/test_workflow_archive.py:26-28`). |
| Single-source pin | bump rewrites every copy (tests, docs); tests and docs derive from `install_codegraph.py` | self | The brief names one source location; fact 3 shows 20 literal copies. T1 removes them once and adds a guard test, so a bump touches the pin file plus its checksum fixture only. |
| Checksum record for `test_u2_pin_integrity` | keep reading and rewrite the `.dev/` evidence file; drop the check; copy to `tests/cli/fixtures/` | self | `.dev/` evidence is history and stays untouched (README `:12`); the test keeps catching hand-typed hashes; the bot rewrites the fixture from the same verified `SHA256SUMS`. |
| MCP `tools/list` client | reuse `.dev/codegraph-migration/evidence/p2-mcp-tools.mjs` (needs Node); Python port in the script | self | CI must not depend on a `.dev/` evidence file; Python lets the unit tests fake the server (R14); no Node step needed. |
| `tools/list` check strictness | every `MCP_TOOLS` tool present (brief); exact set (present and nothing extra) | self | Phase 2's schema-cost decision relied on an explicit list hiding every other tool (`decisions/F2-schema-cost-method/recommendation.md`, X-25 hard stop), so an extra listed tool is a regression too. |
| Drift check fields | whole-entry compare; compare all keys except `command` and `env` | self | IronClaude deliberately registers an absolute command and its own env keys (`install_mcp.py:862-874`); every other key (`type`, `args`, `alwaysLoad`, any new key) must match upstream's `--print-config claude`. |
| CI on bot PRs | rely on PR-triggered `Tests` (approval-gated); dispatch `test.yml` on the branch | self | Fact 5: `GITHUB_TOKEN` PRs start runs only in an approval-required state; `workflow_dispatch` always runs. |
| Release notes in the PR body | full text; link only; budgeted text plus links | self | Fact 1: one release's notes exceed the 65,536-character body limit; within-major PRs carry up to 60,000 characters newest-first plus links; majors carry links (M-a). |
| Open PR for a deleted upstream release (M-b item 4) | close automatically; comment and leave | self | Never close or merge on the bot's own judgment of an upstream deletion; one fingerprinted comment tells the reviewer. |
| Runner | self-hosted (Coder); `ubuntu-latest` | self | `test.yml` already runs every job on `ubuntu-latest`; no Docker or private network is needed. |

Items the debates flagged for the user (none blocks execution; the executor follows the merged rules and lists them in the T6 issue comment): M-a items 1-6 (`decisions/M-major-versions/recommendation.md:44-51`), M-b items 1-5 (`decisions/M-release-age/recommendation.md:56-62`; item 4 decided above, item 5 verified as fact 7), M-c items 1-8 (`decisions/M-proof-failure/recommendation.md:66-77`; item 3 decided above, item 5 handled by `CODEGRAPH_MONITOR_ASSIGNEE`, item 7 verified as fact 7, item 8 handled by the distinct titles in §2.5).
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
