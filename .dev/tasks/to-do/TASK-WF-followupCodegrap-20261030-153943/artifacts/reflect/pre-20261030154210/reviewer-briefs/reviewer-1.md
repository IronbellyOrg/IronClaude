# Reviewer 1 brief (persona: analyzer)

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

## Spec contradictions

- **T1-14** | important | spec-inherited | source.md:69 vs source.md:118,19,202 | Where the push happens is contradictory. §2.1 puts "commit + push" in `open`, after `prove`. §2.3 has the PR step run on `always() && <branch was pushed>`, opening a `stage=aborted` draft when prove aborts; that only works if the push happens before prove (Coder's push, then proof, then PR order, source.md:19). The static test orders the push only after `fetch`. If the push follows prove, an aborted prove skips the push and the `stage=aborted` path can never run. | State the order explicitly: fetch ok, bump, commit, push, then tests, prove, body, and PR with `if: always() && steps.push.outcome == 'success'`. Add a static check that the push step comes before the prove step.
- **T1-15** | important | spec-inherited | source.md:44,51; plan:24 vs source.md:146-147; src/superclaude/cli/install_mcp.py:21,23 | "stdlib only / imports only stdlib modules" conflicts with the `prove` stages that need `install_codegraph.MCP_TOOLS` and `install_mcp._codegraph_entry(launcher)`. `install_mcp` imports `click` at install_mcp.py:21 and `from . import install_codegraph` at :23, so the script cannot meet the rule unless it hides the import (lazy import, which passes the weak grep, T1-09) or calls it in a subprocess. | Allow `superclaude.cli.install_codegraph` and `superclaude.cli.install_mcp` explicitly (installed by `uv pip install -e ".[dev]"`), or have the prove child `python -c` print both values as JSON. Amend the T2 import check to match.
- **T1-16** | important | spec-inherited | source.md:143 vs source.md:281-283; src/superclaude/cli/install_codegraph.py:67-68 | The sandbox paths disagree: `HOME=<tmp>` but `PATH=<tmp>/home/.local/bin:...`, while `local_bin_link()` is `HOME/.local/bin/codegraph`. With HOME=<tmp> the PATH entry points at a directory that does not exist. With HOME=<tmp>/home, T3's `rm -rf "$H"` leaves the rest of `<tmp>` (the index project copy) behind. | Fix the layout: `HOME=<tmp>/home`, `PATH=<tmp>/home/.local/bin:/usr/bin:/bin`, `home=` reports `<tmp>/home`, and cleanup removes `<tmp>`. Or drop `/home` everywhere.
- **T1-17** | important | spec-inherited | source.md:166,417,100-101 | Four problems with the infrastructure counter. (a) `gh run list --limit 3 --json conclusion` called from inside a run lists the current, still-running run first with an empty conclusion [INFERRED from gh run list ordering], so it never sees three `failure` values. (b) Behaviour and integrity runs also end red, so three such runs open "cannot reach upstream". (c) That issue is then closed at the first preflight pass even though upstream was never the cause. (d) An invalid `min_age_days` exits 2, the infrastructure code, so a typo in a manual input counts as an outage. | Count with `--status completed --limit 2` plus the current run's own result, and tag infra runs (step summary or run name) so only infra conclusions count. Exit 1 for invalid input.
- **T1-18** | important | spec-inherited | source.md:101 vs source.md:127,351 | `check --tag` "skips selection", but the candidate set is "strictly newer than the pin". T7's dry run passes `tag=v1.6.2`, the current pin, and expects `fetch` `result=ok` and `prove` `result=pass`. Nothing says `check --tag <pin>` returns `candidate`, and R16 (source.md:197) has no such case. | State that `--tag` accepts a tag >= the pin (equal only with `dry_run`), and add an R16 case.
- **T1-19** | minor | spec-inherited | source.md:110 vs source.md:133 | Each matrix leg runs "from a fresh checkout of `master`", yet an existing `codegraph/bump-<tag>` must be re-proved at that branch's head. | Say the leg checks out the bump branch when `route` returns a re-prove.
- **T1-20** | minor | spec-inherited | source.md:44 vs source.md:103 | Row F6 lists subcommands `check, fetch, bump, prove, body`, but §2.2 also defines `route`. | Add `route` to F6.
- **T1-22** | minor | spec-inherited | source.md:419 vs source.md:24 | The Decisions row says "fact 3 shows 20 literal copies", but fact 3 lists 22 (12 + 2 + 1 + 3 + 2 + 1 + 1). A grep in this worktree confirms all 22 locations. | Change it to 22.
- **T1-23** | minor | spec-inherited | source.md:402-407 | §7 items are numbered 1, 2, 3, 6, 4, 5. | Renumber them.
- **T1-24** | minor | spec-inherited | source.md:168 | The fingerprint includes "branch head SHA", but integrity and infrastructure artifacts have no branch. | Define it as the `master` HEAD SHA for artifacts without a branch.
- **T1-25** | minor | spec-inherited | source.md:110-114,202 | `if:`, permissions and timeout are set "on the job" (singular), yet §2.3 needs at least two jobs (a `check` job and a matrix job). The static test's "job `if` names ..." is ambiguous. | Require the `if:` and permissions on every job, and check every job in the static test.

## Feasibility vs code

- **T1-26** | critical | spec-inherited | source.md:112,115,145-147; .github/workflows/test.yml:144 | "The `prove` step gets no token" does not protect the token. `actions/checkout@v4` saves the job token, which here has `contents: write`, in `$GITHUB_WORKSPACE/.git/config` by default [INFERRED: checkout's default `persist-credentials: true`]. `prove` then runs the third-party codegraph binary (`init`, `query`, `serve --mcp`, `install --print-config`) on the same runner, and it can read that file and push to any unprotected branch. The repo already uses `persist-credentials: false` at test.yml:144. | Set `persist-credentials: false` on checkout, and push with `GH_TOKEN` given only to the push step (for example `git -c http.extraheader=...`). Add a static check. Or run `prove` in a separate job with `permissions: contents: read`.
- **T1-21** | important | spec-inherited | source.md:92,46,103 | "The workflow executes the actions" means the YAML must handle 9 or more action types (`open_pr`, `comment`, `mark_ready`, `retitle`, `open_issue`, `close_superseded`, `close_issue`, branch delete, label) in bash or jq. That code is covered only by the static YAML test, which contradicts "Thin: every decision lives in F6" and the unit-tested design (§2.1). | Add an `apply` subcommand that runs the actions through `_gh` with `--repo "$GITHUB_REPOSITORY"` enforced, give it a test (R18b), and extend the `--repo` check to the script.
- **T1-27** | important | plan | plan:35; `git status --short` (package untracked) | The branch switch conflicts with `/sc:implement`'s own state. If the package is committed on `ironbelly/codegraph-release-monitor` (the T1-01 fix), `git switch -c ... origin/master` removes the plan and `progress.md` from the working tree mid-run, and an uncommitted ledger edit blocks the switch. If the package stays untracked, `git cherry-pick` aborts with "untracked working tree files would be overwritten". [INFERRED: when `/sc:implement` writes its ledger] | Commit the planning files and the ledger right before the switch, and re-commit the ledger after the cherry-pick. Or create the feature branch in a new worktree under `.dev/worktrees/` and run `/sc:implement` there.
- **T1-28** | minor | plan | plan:35; `git log origin/master` = `2f10a0e1 feat: replace codebase-memory and Serena with codegraph (#323) (#329)` | The precondition is already met: #329 is on `origin/master`, and `git diff --stat e62ed152 origin/master` on every file the plan names is empty, so the cited line numbers still hold. The plan's "post one comment and wait" path cannot be followed by `/sc:implement` anyway. | Replace "wait" with "stop as blocked".
- **T1-29** | minor | spec-inherited | src/superclaude/cli/install_codegraph.py:273-278,308,339 | `acquire` reuses any copy that already prints the pinned version (`discover`) and downloads only the runner's asset (`linux-x64`). So the "real verified download" (source.md:143) proves one of the four hashes; the other three rest on `SHA256SUMS` plus the attestation. The child `PATH` (`/usr/bin:/bin`) has no venv `python`. | Have `_run` launch `sys.executable`, assert `shutil.which("codegraph", path=child_PATH)` is None, and say in the PR body which asset was proved by install.
- **T1-30** | minor | spec-inherited | source.md:187 | R6 runs `ruff format --check -` through `subprocess`. `ruff` is not on the bare PATH here (`command -v ruff` finds nothing); it works only inside the `uv run` venv. | Find it with `shutil.which("ruff")` and skip with a reason if it is missing.
- **T1-31** | minor | spec-inherited | source.md:112,202 | [INFERRED] `gh attestation verify` with `GITHUB_TOKEN` may need `attestations: read`, but the static test requires the permissions to be exactly the four listed, so the fix cannot be added. | Confirm in the T7 dry run. If it is needed, add it to §2.3 and to the static test together.
- **T1-32** | minor | spec-inherited | source.md:138,185 | The replay days (08-04, 09-09, 10-17) depend on the time of day of `now` compared with each `published_at` (an exact-seconds rule). A daily `now` at 00:00 UTC could move a bump by one day. | Set `now = <date>T06:23:00Z` to match the cron, and record the real `published_at` timestamps in `releases.json`.
- **T1-33** | minor | plan | tests/unit/test_cli_doctor.py:3-15,241,287 | `test_cli_doctor.py` does not import `install_codegraph`, so deriving `_stub`'s default and the `"the pin is ..."` assertion needs a new import. Task 2 does not say so. | Name the import (`from superclaude.cli import install_codegraph`).
- Checked and correct (no finding): fact-3 line numbers (`tests/cli/test_install_codegraph.py:38,45,96,151,171,175,237,270,639,640,659,691`, `test_cli_doctor.py:241,287`, `test_update_command.py:355`, docs `:9,28,31` / `:29,43`, `CHANGELOG.md:35`, `install_codegraph.py:39`); `install_codegraph.py:26-35,186-190,271-365,328-330`; `install_mcp.py:854-874` (`_codegraph_entry(command: Path)`; `_run_argv` at :804); `test_u2_pin_integrity` at :126-141 reading the `.dev/` evidence file at :132; `.gitignore:238` (`.dev/worktrees/`); `tests/skills/test_workflow_archive.py:26-28`; `pyyaml` in `pyproject.toml:38` and `scripts/dependency_baseline.txt:56`; `test.yml` (`setup-uv@v10.3.2`, Python 3.10, `activate-environment`, `workflow_dispatch`); `codegraph query` usage at `evidence/p2-layer2.sh:44`; the workflows README lists 3 workflows; `tests/cli/fixtures/` does not exist yet (new); `python_files = ["test_*.py"]` (pyproject.toml:109), so `fake_mcp_server.py` is not collected.

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
### src/superclaude/cli/install_codegraph.py:1-60
```python
"""Pinned, checksum-verified acquisition of the codegraph binary (stdlib only).

Discovery reuses a copy that already prints the pinned version (no network).
Acquisition downloads the pinned release tarball, checks its SHA-256 against the
table below, extracts it with strict member checks and records everything it
creates in a receipt *before* creating it, so removal never guesses ownership.
Registration with Claude Code lives in ``install_mcp.install_codegraph_mcp``.
"""

from __future__ import annotations

import hashlib
import http.client
import json
import os
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Callable

VERSION = "1.6.2"
TAG = f"v{VERSION}"
SHA256 = {
    "linux-x64": "ef0af416092128fb1ccc723786000b7edf4a6971fe604acd08bf966e4f37b828",
    "linux-arm64": "c8c6be292be21d00dea26bad8b28d434731cf612fb8cc475dc10f5b3038b5b64",
    "darwin-x64": "53d1a4d1a9af31d6cec11b346df2ae792087081e13f623f583e27783c1e7f9bc",
    "darwin-arm64": "d74d1bfb4060db63ec3c2b72c4e17f76c31978af3bad6ace4370d1501ac0662e",
}
# Chosen by the schema-cost check in .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md
MCP_TOOLS = "node,search,callers,callees,impact,files,status"

DOWNLOAD_TIMEOUT = 60
VERSION_TIMEOUT = 10
_MAX_MEMBERS = 20_000  # the v1.6.2 tarball has 1380
_MAX_BYTES = 2 * 1024**3

# run(argv, timeout) -> (returncode, stdout); the bounded argv runner of install_mcp
Runner = Callable[[list, float], tuple]


def asset_name() -> str | None:
    """``linux-x64`` style asset name for this machine, or None when unsupported."""
    system = {"linux": "linux", "darwin": "darwin"}.get(platform.system().lower())
    arch = {"x86_64": "x64", "amd64": "x64", "aarch64": "arm64", "arm64": "arm64"}.get(
        platform.machine().lower()
    )
    return f"{system}-{arch}" if system and arch else None


def codegraph_dir() -> Path:
    return Path.home() / ".codegraph"


def receipt_path() -> Path:
    return codegraph_dir() / ".superclaude-receipt.json"
```
### src/superclaude/cli/install_codegraph.py:271-365
```python
def acquire(run: Runner) -> tuple:
    """Return ``(ok, message, absolute launcher path)``; never raises for expected faults."""
    winner = discover(run)
    if winner is not None:
        write_pointer(winner)
        warning = _path_warning(winner)
        note = f"\n{warning}" if warning else ""
        return True, f"using codegraph {VERSION} at {winner}{note}", winner

    asset = asset_name()
    if asset is None or asset not in SHA256:
        system, machine = platform.system(), platform.machine()
        return (
            False,
            f"codegraph {TAG} has no supported automatic install for "
            f"{system}/{machine}; install it yourself so that `codegraph --version` "
            f"prints {VERSION}, then rerun superclaude install.",
            None,
        )

    home = codegraph_dir()
    vdir = home / "versions" / TAG
    launcher = vdir / "bin" / "codegraph"
    receipt = read_receipt()
    listed = receipt is not None and str(vdir) in receipt["version_dirs"]
    if os.path.lexists(vdir) and not listed:
        # upstream's own install.sh put it there: use it only if it is the pin
        if reports_pinned_version(run, launcher):
            real = Path(os.path.realpath(launcher))
            write_pointer(real)
            return True, f"using existing codegraph {VERSION} at {real}", real
        return _fail(
            "extract",
            f"{vdir} exists but its codegraph does not print {VERSION}; "
            f"remove it and rerun superclaude install",
        )

    url = f"https://github.com/colbymchenry/codegraph/releases/download/{TAG}/codegraph-{asset}.tar.gz"
    home.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(dir=home, prefix=".dl-"))
    try:
        archive = tmp / f"codegraph-{asset}.tar.gz"
        try:
            _download(url, archive, DOWNLOAD_TIMEOUT)
        except (
            urllib.error.URLError,
            http.client.HTTPException,
            OSError,
            TimeoutError,
            ValueError,
        ) as exc:
            return _fail(
                "download",
                f"{url} ({type(exc).__name__}). Download it yourself, check its "
                f"SHA-256 is {SHA256[asset]}, extract it so that `codegraph --version` "
                f"prints {VERSION} on PATH, then rerun superclaude install.",
            )
        got = hashlib.sha256(archive.read_bytes()).hexdigest()
        if got != SHA256[asset]:
            return _fail("checksum", f"expected {SHA256[asset]}, got {got} for {url}")
        extracted = tmp / "x"
        prefix = f"codegraph-{asset}"
        try:
            with tarfile.open(archive, "r:gz") as tar:
                _extract(tar, _check_members(tar, prefix), extracted)
        except (tarfile.TarError, OSError, ValueError, EOFError) as exc:
            return _fail("extract", f"{type(exc).__name__}: {exc}")
        new_dir = extracted / prefix
        if not reports_pinned_version(run, new_dir / "bin" / "codegraph"):
            return _fail("extract", f"the extracted codegraph does not print {VERSION}")

        receipt = receipt or {"version_dirs": [], "links": {}}
        receipt.update(tag=TAG, sha256=got, complete=False)
        if str(vdir) not in receipt["version_dirs"]:
            receipt["version_dirs"].append(str(vdir))  # record before creating
        _write_receipt(receipt)
        vdir.parent.mkdir(parents=True, exist_ok=True)
        if listed and os.path.lexists(vdir):
            shutil.rmtree(vdir)  # an interrupted earlier run left it
        os.rename(new_dir, vdir)
        notes = _flip_links(receipt, vdir)
        receipt.update(complete=True, fresh=True)
        _write_receipt(receipt)
    except OSError as exc:
        return _fail("extract", f"{type(exc).__name__} while installing into {home}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    real = Path(os.path.realpath(launcher))
    write_pointer(real)
    parts = [f"installed codegraph {VERSION} (SHA-256 verified) at {vdir}", *notes]
    warning = _path_warning(real)
    if warning:
        parts.append(warning)
    return True, "\n".join(parts), real
```
### src/superclaude/cli/install_mcp.py:1-30
```python
"""
MCP Server Installation Module for SuperClaude

Installs and manages MCP servers using the latest Claude Code API.
Based on the installer logic from commit d4a17fc but adapted for modern Claude Code.
"""

import json
import os
import platform
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click

from . import install_codegraph

# AIRIS MCP Gateway - Unified MCP solution (recommended)
AIRIS_GATEWAY = {
    "name": "airis-mcp-gateway",
    "description": "Unified MCP gateway with 60+ tools, HOT/COLD management, 98% token reduction",
    "transport": "sse",
    "endpoint": "http://localhost:9400/sse",
```
### src/superclaude/cli/install_mcp.py:854-925
```python
_CODEGRAPH_ENV_KEYS = {
    "CODEGRAPH_TELEMETRY",
    "CODEGRAPH_NO_UPDATE_CHECK",
    "CODEGRAPH_MCP_TOOLS",
}
_CODEGRAPH_REMOVE = "claude mcp remove codegraph --scope user"


def _codegraph_entry(command: Path) -> dict:
    """The exact user-scope entry (spec 2.4); the tool list comes from MCP_TOOLS."""
    return {
        "type": "stdio",
        "command": str(command),
        "args": ["serve", "--mcp"],
        "alwaysLoad": True,
        "env": {
            "CODEGRAPH_TELEMETRY": "0",
            "CODEGRAPH_NO_UPDATE_CHECK": "1",
            "CODEGRAPH_MCP_TOOLS": install_codegraph.MCP_TOOLS,
        },
    }


def _codegraph_entry_kind(entry: dict, expected: dict) -> str:
    """equal | owned (only fields IronClaude writes, so safe to replace) | user."""
    if entry == expected:
        return "equal"
    env = entry.get("env", {})
    owned = (
        set(entry) <= set(expected)
        and entry.get("type", "stdio") == "stdio"
        and entry.get("args") == ["serve", "--mcp"]
        and isinstance(entry.get("command"), str)
        and isinstance(env, dict)
        and set(env) <= _CODEGRAPH_ENV_KEYS
    )
    return "owned" if owned else "user"


def _claude_user_entry_cmd(*args: str) -> bool:
    """One bounded ``claude mcp`` call; no output or exception text is kept."""
    try:
        return _exec_claude(["claude", "mcp", *args, "--scope", "user"], 60) == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _add_user_entry(name: str, entry: dict) -> bool:
    return _claude_user_entry_cmd("add-json", name, json.dumps(entry))


def _restore_user_entry(name: str, previous: dict, attempted: dict) -> bool:
    known, current = read_user_mcp_entry(name)
    if not known:
        return False
    if current == previous:
        return True
    if current is not None:
        # A timed-out add may have written our entry. Do not overwrite a third
        # party's concurrent edit when its contents cannot be attributed to us.
        if current != attempted or not _claude_user_entry_cmd("remove", name):
            return False
    if not _add_user_entry(name, previous):
        return False
    known, current = read_user_mcp_entry(name)
    return known and current == previous


def install_codegraph_mcp(
    *, scope: str = "user", dry_run: bool = False
) -> tuple[bool, str]:
    """Required install phase: reuse or download the pinned codegraph, then register it."""
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
